#!/usr/bin/env python3
"""Record a reviewer's structured findings as a hash-bound review record.

Usage:
  record_review.py <run-dir> --input <findings.json> --runtime claude|codex|human --agent <name>
                   [--stage checkpoint|final] [--round N] [--agent-file <path>] [--force]

The input is the JSON object a reviewer returned (schema in
canonical/review-findings-schema.md). This script:
- validates the shape,
- rejects any finding whose quoted passage is not found in the current draft,
- stamps the current draft, export, and pinned-source hashes as the review subject,
- records which agent definition file was used (and its hash),
- writes reviews/<role>-<stage>-r<round>.json, refusing to overwrite without --force.

It never judges the content of a finding. Run it immediately after the reviewer returns,
before any file in the run changes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cw_common as cw  # noqa: E402

DEFAULT_AGENT_FILES = {
    ("claude", "legal-reviewer"): ".claude/agents/legal-reviewer.md",
    ("claude", "editorial-reviewer"): ".claude/agents/editorial-reviewer.md",
    ("codex", "legal_reviewer"): ".codex/agents/legal_reviewer.toml",
    ("codex", "editorial_reviewer"): ".codex/agents/editorial_reviewer.toml",
}
AGENT_ROLE = {
    "legal-reviewer": "legal-reviewer", "legal_reviewer": "legal-reviewer",
    "editorial-reviewer": "editorial-reviewer", "editorial_reviewer": "editorial-reviewer",
}


def quote_present(quote: str, draft_text: str) -> bool:
    return cw.norm_ws(quote).casefold() in cw.norm_ws(draft_text).casefold()


def build_record(run_dir: Path, run: dict, payload: dict, *, runtime: str, agent: str, stage: str | None, round_: int | None, agent_file: str | None, repo_root: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    role = payload.get("role") or AGENT_ROLE.get(agent)
    if role not in ("legal-reviewer", "editorial-reviewer"):
        errors.append("role must be legal-reviewer or editorial-reviewer for this recorder (mechanical records come from mechanical_qa.py)")
    if agent in AGENT_ROLE and AGENT_ROLE[agent] != role:
        errors.append(f"agent {agent} is a {AGENT_ROLE[agent]} but the payload declares role {role}")
    stage = stage or payload.get("stage")
    round_ = payload.get("round") if round_ is None else round_
    draft_path = run_dir / (run.get("draft") or {}).get("path", "draft.md")
    if stage != "predraft" and not draft_path.is_file():
        errors.append(f"draft not found: {draft_path}")
        return {}, errors
    if stage == "predraft" and int(round_ or 0) == 0 and (draft_path.is_file() or (run_dir / "manifest.json").is_file()):
        errors.append("a round-0 predraft record must be written before any draft or manifest exists; verification has to precede drafting")
    draft_text = draft_path.read_text(encoding="utf-8") if draft_path.is_file() else ""
    export_rel = (run.get("export") or {}).get("path")
    export_path = run_dir / export_rel if export_rel else None
    sources_sha = {}
    for source in run.get("sources") or []:
        path = run_dir / source.get("path", "")
        sources_sha[source.get("id")] = cw.sha256_file(path) if path.is_file() else None

    agent_rel = agent_file or DEFAULT_AGENT_FILES.get((runtime, agent))
    if runtime in ("claude", "codex") and not agent_rel:
        errors.append(f"agent {agent!r} is not a known pilot agent for runtime {runtime}; pass --agent-file with the definition actually used")
    agent_abs = (repo_root / agent_rel) if agent_rel else None
    record = {
        "schema": cw.REVIEW_SCHEMA,
        "fixture": bool(run.get("fixture", False)),
        "role": role,
        "stage": stage,
        "round": round_,
        "kind": "judgment",
        "judgment_notice": cw.JUDGMENT_NOTICE,
        "verdict": payload.get("verdict"),
        "subject": {
            "draft_sha256": cw.sha256_file(draft_path) if draft_path.is_file() else None,
            "export_sha256": cw.sha256_file(export_path) if export_path and export_path.is_file() else None,
            "sources_sha256": sources_sha,
        },
        "reviewer": {
            "runtime": runtime,
            "agent": agent,
            "agent_file": agent_rel,
            "agent_file_sha256": cw.sha256_file(agent_abs) if agent_abs and agent_abs.is_file() else None,
        },
        "recorded_at": cw.now_iso(),
        "findings": payload.get("findings", []),
        "verification_log": payload.get("verification_log", []),
        "checks_not_performed": payload.get("checks_not_performed", []),
        "learning_contribution": payload.get("learning_contribution", {}),
    }
    if payload.get("fixture") and not run.get("fixture"):
        errors.append("input is marked fixture but the run is not a fixture; refusing to record a fixture review for a real deliverable")
    echoed = ((payload.get("subject") or {}).get("draft_sha256")) if isinstance(payload.get("subject"), dict) else None
    if echoed and echoed != record["subject"]["draft_sha256"]:
        errors.append(f"reviewer echoed draft hash {str(echoed)[:12]}… but the current draft is {record['subject']['draft_sha256'][:12]}…; the draft changed after the review")
    prior_ids: set[str] = set()
    for prior_path in cw.review_files(run_dir):
        try:
            prior = cw.load_json(prior_path)
        except (OSError, json.JSONDecodeError):
            continue
        if prior.get("role") == role and prior.get("stage") in ("predraft", "checkpoint") and int(prior.get("round", 0)) <= int(round_ or 0):
            prior_ids.update(str(f.get("id")) for f in prior.get("findings", []) if isinstance(f, dict))
    if agent_rel and not (agent_abs and agent_abs.is_file()):
        errors.append(f"agent definition file {agent_rel} does not exist (activation missing?)")
    errors.extend(cw.validate_review_record(record))
    for finding in record["findings"] if isinstance(record["findings"], list) else []:
        if not isinstance(finding, dict):
            continue
        quote = ((finding.get("passage") or {}).get("quote")) or ""
        resolution = finding.get("resolution") or {}
        if stage == "predraft":
            pass  # a predraft finding quotes the planned claim text the coordinator supplied; there is no draft to match
        elif quote and resolution.get("status") in ("open", "fixed-unverified", "disputed") and not quote_present(quote, draft_text):
            errors.append(f"finding {finding.get('id')}: quoted passage not found in the current draft: {cw.norm_ws(quote)[:80]!r}")
        if finding.get("category") in cw.PROTECTED_CATEGORIES and resolution.get("status") == "fixed-verified":
            corrected = cw.norm_ws(str(resolution.get("corrected_text") or ""))
            if len(corrected) < 20:
                errors.append(f"finding {finding.get('id')}: a {finding.get('category')} finding needs resolution.corrected_text of at least 20 characters (the revised passage you re-read)")
            elif corrected.casefold() == cw.norm_ws(quote).casefold():
                errors.append(f"finding {finding.get('id')}: corrected_text is identical to the passage the finding targeted")
            elif not quote_present(corrected, draft_text):
                errors.append(f"finding {finding.get('id')}: corrected_text is not in the current draft")
        if resolution.get("status") == "fixed-verified":
            # A reviewer without Bash cannot compute the hash; null means "the draft I just re-read".
            if not resolution.get("verified_against_draft_sha256"):
                resolution["verified_against_draft_sha256"] = record["subject"]["draft_sha256"]
            if not resolution.get("verified_by"):
                resolution["verified_by"] = agent
            if resolution["verified_against_draft_sha256"] != record["subject"]["draft_sha256"]:
                errors.append(f"finding {finding.get('id')}: fixed-verified against a hash other than the current draft")
            if (int(round_ or 0) == 0 and stage == "final" and finding.get("severity") in ("blocking", "major")
                    and str(finding.get("id")) not in prior_ids):
                # An initial final review can only verify a fix to a finding raised at a checkpoint.
                errors.append(f"finding {finding.get('id')}: fixed-verified is not valid in an initial (round 0) final review unless the id was raised in a prior checkpoint record")
        if resolution.get("status") == "coordinator-accepted":
            errors.append(f"finding {finding.get('id')}: reviewers do not set coordinator-accepted; the coordinator records that separately")
    return record, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--runtime", choices=("claude", "codex", "human"), required=True)
    parser.add_argument("--agent", required=True, help="agent name as used by the host (e.g. legal-reviewer or legal_reviewer)")
    parser.add_argument("--stage", choices=("predraft", "checkpoint", "final"))
    parser.add_argument("--round", type=int, dest="round_")
    parser.add_argument("--agent-file", help="repository-relative path of the agent definition actually used")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    repo_root = cw.find_repo_root()
    try:
        run = cw.load_json(run_dir / "run.json")
        payload = cw.load_json(args.input)
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 2
    record, errors = build_record(run_dir, run, payload, runtime=args.runtime, agent=args.agent, stage=args.stage, round_=args.round_, agent_file=args.agent_file, repo_root=repo_root)
    if errors:
        print("REFUSED: review record not written")
        for error in errors:
            print(f"  - {error}")
        return 1
    short = cw.ROLE_SHORT[record["role"]]
    target = run_dir / "reviews" / f"{short}-{record['stage']}-r{record['round']}.json"
    if target.exists() and not args.force:
        print(f"REFUSED: {target} exists; use --force to overwrite")
        return 1
    if target.exists():
        superseded = target.parent / "superseded" / f"{target.stem}.{cw.now_iso().replace(':', '')}.json"
        superseded.parent.mkdir(parents=True, exist_ok=True)
        target.rename(superseded)
        print(f"superseded record kept at {superseded.relative_to(run_dir)}")
    cw.dump_json(target, record)
    draft_label = (record["subject"].get("draft_sha256") or "no draft (predraft)")[:20]
    print(f"recorded {target.relative_to(run_dir)} (draft {draft_label}…, {len(record['findings'])} finding(s), verdict={record['verdict']}) — {cw.JUDGMENT_NOTICE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
