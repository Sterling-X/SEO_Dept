#!/usr/bin/env python3
"""Deterministic readiness check for a content-workflow run.

Usage:
  readiness_check.py <run-dir> [--stage intake|delivery] [--json <path>] [--quiet]

Exit codes: 0 = READY (or intake complete), 1 = INCOMPLETE, 2 = usage or unreadable run.

The check proves mechanical facts only: pins and hashes, presence of required resources,
voice routing, citation pairing in draft and export, absence of placeholders, draft/export
parity, well-formed and current review records, resolved findings, round limits. It
records legal and editorial judgments; it cannot verify them.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cw_common as cw  # noqa: E402


class Reasons:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, code: str, detail: str) -> None:
        self.items.append({"code": code, "detail": detail})

    def codes(self) -> list[str]:
        return [item["code"] for item in self.items]


def load_run(run_dir: Path) -> dict:
    path = run_dir / "run.json"
    if not path.is_file():
        raise FileNotFoundError(f"run.json not found in {run_dir}")
    run = cw.load_json(path)
    if run.get("schema") != cw.RUN_SCHEMA:
        raise ValueError(f"run.json schema must be {cw.RUN_SCHEMA}")
    return run


def intake_checks(repo_root: Path, run_dir: Path, run: dict, reasons: Reasons) -> dict:
    facts: dict = {}
    for key in ("run_id", "client", "jurisdiction", "page_type", "voice", "skills", "sources", "draft", "export", "citations", "reviews", "rounds"):
        if key not in run:
            reasons.add("INTAKE_MISSING_FIELD", f"run.json is missing {key}")
    client = run.get("client") or {}
    for key in ("name", "domain", "slug"):
        if not cw.norm_ws(str(client.get(key, ""))):
            reasons.add("INTAKE_MISSING_FIELD", f"client.{key} is empty")
    if not cw.norm_ws(str(run.get("jurisdiction", ""))):
        reasons.add("INTAKE_MISSING_FIELD", "jurisdiction is empty")
    page_type = run.get("page_type") or {}
    if not page_type.get("kind"):
        reasons.add("INTAKE_MISSING_FIELD", "page_type.kind is empty")
    elif page_type.get("kind") in ("situational", "core-hub", "procedural") and not page_type.get("architecture_node_id"):
        reasons.add("INTAKE_MISSING_FIELD", f"page_type.architecture_node_id is required for kind {page_type.get('kind')}")
    rounds = run.get("rounds") or {}
    max_rounds = rounds.get("max_repair_rounds")
    if not isinstance(max_rounds, int) or not 0 <= max_rounds <= 2:
        reasons.add("INTAKE_MISSING_FIELD", "rounds.max_repair_rounds must be an integer from 0 to 2")

    # Skill pins and required resources
    skills = run.get("skills") or []
    if not skills:
        reasons.add("SKILL_PIN_MISSING", "at least one skill must be pinned by path and sha256")
    facts["skills"] = []
    for skill in skills:
        name, rel, want = skill.get("name"), skill.get("path"), skill.get("sha256")
        if not name or not rel or not want:
            reasons.add("SKILL_PIN_MISSING", f"skill entry {skill!r} needs name, path, sha256")
            continue
        path = repo_root / rel
        entry = {"name": name, "path": rel, "pinned_sha256": want, "actual_sha256": None, "required_files_missing": []}
        if not path.is_file():
            reasons.add("SKILL_PATH_MISSING", f"{name}: {rel} does not exist")
        else:
            actual = cw.sha256_file(path)
            entry["actual_sha256"] = actual
            if actual != want:
                reasons.add("SKILL_HASH_MISMATCH", f"{name}: pinned {want[:12]}… but file is {actual[:12]}…")
            manifest_path = path.parent / "pilot-manifest.json"
            if manifest_path.is_file():
                try:
                    manifest = cw.load_json(manifest_path)
                except (OSError, json.JSONDecodeError) as error:
                    reasons.add("SKILL_RESOURCE_MISSING", f"{name}: pilot-manifest.json unreadable ({error})")
                    manifest = {}
                for required in manifest.get("required_files", []):
                    if not (path.parent / required).exists():
                        entry["required_files_missing"].append(required)
                        reasons.add("SKILL_RESOURCE_MISSING", f"{name}: required resource {required} is missing")
                if manifest.get("validators"):
                    facts.setdefault("skill_validators_declared", []).append(name)
                    facts.setdefault("skill_validator_names", set()).update(str(v.get("name")) for v in manifest["validators"] if v.get("name"))
            pinned_files = skill.get("files") or {}
            if not pinned_files and manifest_path.is_file():
                reasons.add("SKILL_PIN_MISSING", f"{name}: pin has no files map; re-run pin.py so every required resource is hashed")
            for rel_file, want_file in pinned_files.items():
                file_path = path.parent / rel_file
                if not file_path.exists():
                    reasons.add("SKILL_RESOURCE_MISSING", f"{name}: pinned resource {rel_file} is missing")
                elif file_path.is_file() and cw.sha256_file(file_path) != want_file:
                    reasons.add("SKILL_HASH_MISMATCH", f"{name}: resource {rel_file} changed since it was pinned")
        facts["skills"].append(entry)

    # Source pins
    sources = run.get("sources") or []
    seen_ids: set[str] = set()
    facts["sources"] = []
    for source in sources:
        sid, rel, want = source.get("id"), source.get("path"), source.get("sha256")
        if not sid or not rel or not want:
            reasons.add("SOURCE_MISSING", f"source entry {source!r} needs id, path, sha256")
            continue
        if sid in seen_ids:
            reasons.add("SOURCE_MISSING", f"duplicate source id {sid}")
        seen_ids.add(sid)
        path = run_dir / rel
        entry = {"id": sid, "path": rel, "kind": source.get("kind"), "pinned_sha256": want, "actual_sha256": None}
        if not path.is_file():
            reasons.add("SOURCE_MISSING", f"{sid}: {rel} does not exist in the run directory")
        else:
            actual = cw.sha256_file(path)
            entry["actual_sha256"] = actual
            if actual != want:
                reasons.add("SOURCE_HASH_MISMATCH", f"{sid}: pinned {want[:12]}… but file is {actual[:12]}…")
        facts["sources"].append(entry)
    source_by_id = {s.get("id"): s for s in sources if s.get("id")}

    if page_type.get("kind") in ("situational", "core-hub", "procedural"):
        kinds = [s.get("kind") for s in sources]
        if "client-facts" not in kinds:
            reasons.add("INTAKE_MISSING_SOURCE", "no pinned source of kind client-facts")
        if "legal-authority" not in kinds:
            reasons.add("INTAKE_MISSING_SOURCE", "no pinned source of kind legal-authority")
        if not (run.get("citations") or []):
            reasons.add("INTAKE_MISSING_SOURCE", "no expected citations declared")
    if facts.get("skill_validators_declared"):
        declared_names = {str(v.get("name")) for v in ((run.get("export") or {}).get("validators") or []) if v.get("name")}
        missing_names = sorted(facts.get("skill_validator_names", set()) - declared_names)
        if missing_names:
            reasons.add("VALIDATORS_UNDECLARED", f"pinned skill(s) {facts['skill_validators_declared']} require validators {missing_names} but run.json export.validators does not declare them by name")
    facts.pop("skill_validator_names", None)

    # Voice route
    routing = cw.load_json(cw.PILOT_ROOT / "canonical" / "client-routing.json")
    routes = routing.get("routes", {})
    voice = run.get("voice") or {}
    domain = cw.norm_ws(str(client.get("domain", ""))).lower()
    declared_skill = voice.get("skill")
    brief_id = voice.get("approved_brief_source_id")
    facts["voice"] = {"domain": domain, "routed_skill": routes.get(domain), "declared_skill": declared_skill, "approved_brief_source_id": brief_id}
    if domain in routes:
        expected = routes[domain]
        if declared_skill != expected:
            reasons.add("VOICE_MISMATCH", f"domain {domain} routes to {expected}; run.json declares {declared_skill!r}")
        skill_file = repo_root / routing.get("voice_skill_root", ".agents/skills") / expected / "SKILL.md"
        if not skill_file.is_file():
            reasons.add("VOICE_SKILL_MISSING", f"routed voice skill file {skill_file.relative_to(repo_root)} is missing")
    else:
        if declared_skill:
            reasons.add("VOICE_MISMATCH", f"domain {domain} has no route in client-routing.json; a voice skill ({declared_skill}) cannot be assigned by inference")
        brief = source_by_id.get(brief_id) if brief_id else None
        if not brief or brief.get("kind") != "voice-brief":
            reasons.add("VOICE_UNROUTED", f"domain {domain} is unrouted and no approved voice brief (kind voice-brief) is pinned as a source")

    # Citation pins
    citations = run.get("citations") or []
    ids = [c.get("id") for c in citations]
    if ids != list(range(1, len(ids) + 1)):
        reasons.add("CITATION_MISMATCH", f"run.json citations must be numbered 1..n; found {ids}")
    if len(citations) > 6:
        reasons.add("CITATION_MISMATCH", f"{len(citations)} citations exceed the six-source limit")
    for citation in citations:
        source = source_by_id.get(citation.get("source_id"))
        if not source:
            reasons.add("CITATION_MISMATCH", f"citation [{citation.get('id')}] references unpinned source {citation.get('source_id')!r}")
        elif source.get("url") and source.get("url") != citation.get("url"):
            reasons.add("CITATION_MISMATCH", f"citation [{citation.get('id')}] URL differs from pinned source {source.get('id')} URL")
        if not citation.get("url") or not citation.get("label"):
            reasons.add("CITATION_MISMATCH", f"citation [{citation.get('id')}] needs label and url")
    return facts


def evaluate_reviews(run_dir: Path, run: dict, draft_sha: str | None, export_sha: str | None, reasons: Reasons) -> dict:
    records: list[tuple[Path, dict]] = []
    fixture_run = bool(run.get("fixture", False))
    for path in cw.review_files(run_dir):
        try:
            record = cw.load_json(path)
        except (OSError, json.JSONDecodeError) as error:
            reasons.add("REVIEW_INVALID", f"{path.name}: unreadable ({error})")
            continue
        problems = cw.validate_review_record(record)
        if problems:
            reasons.add("REVIEW_INVALID", f"{path.name}: " + "; ".join(problems))
            continue
        if bool(record.get("fixture", False)) != fixture_run:
            reasons.add("FIXTURE_FLAG", f"{path.name}: record fixture={record.get('fixture', False)} but run fixture={fixture_run}")
            continue
        records.append((path, record))

    max_rounds = int((run.get("rounds") or {}).get("max_repair_rounds", 2))
    for path, record in records:
        if int(record.get("round", 0)) > max_rounds:
            reasons.add("ROUNDS_EXCEEDED", f"{path.name}: round {record.get('round')} exceeds max_repair_rounds {max_rounds}")

    summary: dict = {"required": [], "findings": [], "accepted_risks": []}
    declared_required = (run.get("reviews") or {}).get("required") or []
    required = list(cw.REQUIRED_REVIEW_FLOOR) + [k for k in declared_required if k not in cw.REQUIRED_REVIEW_FLOOR]
    current_sources = {
        s.get("id"): (cw.sha256_file(run_dir / s["path"]) if (run_dir / s.get("path", "")).is_file() else None)
        for s in run.get("sources") or []
    }
    draft_path = run_dir / (run.get("draft") or {}).get("path", "draft.md")
    draft_text = draft_path.read_text(encoding="utf-8") if draft_path.is_file() else ""
    latest_by_kind: dict[str, tuple[Path, dict]] = {}
    for path, record in sorted(records, key=lambda item: cw.record_order_key(item[1])):
        latest_by_kind[cw.record_kind(record)] = (path, record)
    for kind in required:
        if kind not in cw.REQUIRED_REVIEW_KINDS:
            reasons.add("REVIEW_INVALID", f"unknown required review kind {kind}")
            continue
        entry = {"review": kind, "file": None, "verdict": None, "current": False, "notice": cw.JUDGMENT_NOTICE if not kind.startswith("mechanical") else "deterministic record; re-run by this check"}
        if kind not in latest_by_kind:
            reasons.add("REVIEW_MISSING", f"required review {kind} has no record")
            summary["required"].append(entry)
            continue
        path, record = latest_by_kind[kind]
        entry.update({"file": path.name, "verdict": record.get("verdict"), "round": record.get("round")})
        if kind.endswith("-checkpoint"):
            # A required checkpoint proves the checkpoint happened; it is bound to an earlier draft by design,
            # so only presence and shape are required here. Its findings still flow into the resolution rules.
            entry["current"] = "not-applicable (checkpoint)"
            entry["notice"] = "checkpoint presence only; findings evaluated below"
            summary["required"].append(entry)
            continue
        subject = record.get("subject") or {}
        current = bool(draft_sha) and subject.get("draft_sha256") == draft_sha
        if kind.startswith("mechanical"):
            current = current and bool(export_sha) and subject.get("export_sha256") == export_sha
            if record.get("verdict") != "pass":
                reasons.add("MECHANICAL_RECORD_FAILED", f"{path.name}: mechanical verdict is {record.get('verdict')}")
        recorded_sources = subject.get("sources_sha256") or {}
        stale_sources = [sid for sid, digest in current_sources.items() if recorded_sources.get(sid) != digest]
        if current and stale_sources:
            current = False
            reasons.add("REVIEW_STALE", f"{path.name}: pinned source(s) {stale_sources} changed after this review was recorded")
        if not current:
            reasons.add("REVIEW_STALE", f"{path.name}: reviewed draft {str(subject.get('draft_sha256'))[:12]}… / export {str(subject.get('export_sha256'))[:12]}… but current draft is {str(draft_sha)[:12]}… / export {str(export_sha)[:12]}…")
        entry["current"] = current
        if current and not kind.startswith("mechanical"):
            if record.get("verdict") in ("not-ready", "fail"):
                reasons.add("REVIEW_VERDICT_BLOCKING", f"{path.name}: {record['role']} verdict is {record['verdict']}")
            if record["role"] == "legal-reviewer":
                bad_rows = [row for row in record.get("verification_log", []) or [] if str(row.get("result", "")).strip().lower() in ("unverifiable", "correction-needed", "corrected")]
                if bad_rows:
                    reasons.add("LEGAL_LOG_UNVERIFIED", f"{path.name}: {len(bad_rows)} Verification Log row(s) are Unverifiable or Correction-needed: " + "; ".join(str(r.get("claim", ""))[:60] for r in bad_rows[:3]))
            # Re-apply the recorder's integrity rules so a hand-written record cannot bypass them.
            prior_ids = {
                str(f.get("id")) for _p, r in records
                if r.get("role") == record["role"] and cw.record_order_key(r) < cw.record_order_key(record)
                for f in r.get("findings", [])
            }
            for finding in record.get("findings", []):
                quote = ((finding.get("passage") or {}).get("quote")) or ""
                if quote and cw.norm_ws(quote).casefold() not in cw.norm_ws(draft_text).casefold():
                    reasons.add("REVIEW_INVALID", f"{path.name}: finding {finding.get('id')} quotes a passage not in the current draft")
                resolution = finding.get("resolution") or {}
                if (resolution.get("status") == "fixed-verified" and int(record.get("round", 0)) == 0 and record.get("stage") == "final"
                        and finding.get("severity") in ("blocking", "major") and str(finding.get("id")) not in prior_ids):
                    reasons.add("REVIEW_INVALID", f"{path.name}: finding {finding.get('id')} is fixed-verified in an initial final review without a prior checkpoint finding")
        summary["required"].append(entry)

    # Finding resolution: the latest record per role governs each id it raised.
    by_role: dict[str, list[dict]] = {}
    for _path, record in records:
        by_role.setdefault(record["role"], []).append(record)
    for role, role_records in by_role.items():
        if role == "mechanical-qa":
            continue  # mechanical records are gated by currency and verdict; failed checks are re-run, not carried as findings
        role_records.sort(key=cw.record_order_key)
        latest = role_records[-1]
        latest_ids = {str(f["id"]) for f in latest.get("findings", [])}
        state: dict[str, dict] = {}
        for record in role_records:
            for finding in record.get("findings", []):
                state[str(finding["id"])] = {"finding": finding, "round": record.get("round"), "stage": record.get("stage")}
        for fid, info in state.items():
            finding = info["finding"]
            severity = finding.get("severity")
            resolution = finding.get("resolution") or {}
            status = resolution.get("status") if fid in latest_ids else "dropped"
            note = cw.norm_ws(str(resolution.get("note") or ""))
            verified_against = resolution.get("verified_against_draft_sha256")
            row = {"role": role, "id": fid, "severity": severity, "status": status, "last_seen_round": info["round"], "last_seen_stage": info["stage"]}
            summary["findings"].append(row)
            if severity == "blocking":
                ok = (status == "fixed-verified" and verified_against == draft_sha) or (status == "withdrawn" and len(note) >= 10)
                if not ok:
                    why = status
                    if status == "fixed-verified" and verified_against != draft_sha:
                        why = "fixed-verified against a different draft hash (stale verification)"
                    reasons.add("FINDING_BLOCKING_UNRESOLVED", f"{role} {fid}: {why}")
            elif severity == "major":
                if status in ("open", "dropped", "fixed-unverified", "disputed"):
                    reasons.add("FINDING_MAJOR_UNDISPOSED", f"{role} {fid}: {status}")
                elif status == "fixed-verified" and verified_against != draft_sha:
                    reasons.add("FINDING_MAJOR_UNDISPOSED", f"{role} {fid}: fixed-verified against a different draft hash")
                elif status == "coordinator-accepted":
                    if len(note) < 40:
                        reasons.add("FINDING_MAJOR_UNDISPOSED", f"{role} {fid}: coordinator-accepted needs a rationale of at least 40 characters")
                    else:
                        summary["accepted_risks"].append({"role": role, "id": fid, "rationale": note})
    return summary


def run_check(run_dir: Path, stage: str, *, run_validators: bool = True) -> dict:
    repo_root = cw.find_repo_root()  # anchored on the pilot's own location; run dirs may live anywhere
    run = load_run(run_dir)
    reasons = Reasons()
    report: dict = {
        "schema": cw.READINESS_SCHEMA,
        "run_id": run.get("run_id"),
        "stage": stage,
        "checked_at": cw.now_iso(),
        "fixture": bool(run.get("fixture", False)),
        "hashes": {"run_json": cw.sha256_file(run_dir / "run.json")},
        "intake": intake_checks(repo_root, run_dir, run, reasons),
        "mechanical": [],
        "validators": [],
        "recorded_judgments": [],
        "findings": [],
        "accepted_risks": [],
        "notice": (
            "Mechanical checks prove hashes, presence, pairing, and record shape. Recorded legal and "
            "editorial verdicts are judgments bound to the hashes present when the record was written; "
            "this tool cannot verify that a judgment was correct or that the record was produced by the "
            "named reviewer. Attorney review before publication remains required for legal content."
        ),
    }
    if stage == "delivery":
        draft_path = run_dir / (run.get("draft") or {}).get("path", "draft.md")
        export_rel = (run.get("export") or {}).get("path")
        export_path = run_dir / export_rel if export_rel else None
        draft_sha = cw.sha256_file(draft_path) if draft_path.is_file() else None
        export_sha = cw.sha256_file(export_path) if export_path and export_path.is_file() else None
        report["hashes"].update({"draft": draft_sha, "export": export_sha})
        if draft_sha is None:
            reasons.add("DRAFT_MISSING", f"{draft_path.name} is missing")
        if export_sha is None:
            reasons.add("EXPORT_MISSING", f"export {export_rel!r} is missing")
        checks, validators = cw.mechanical_checks(repo_root, run_dir, run, run_declared_validators=run_validators)
        report["mechanical"] = [c.as_dict() for c in checks]
        report["validators"] = validators
        for check in checks:
            if check.status != "fail":
                continue
            code = {
                "citations": "CITATION_MISMATCH", "placeholders": "PLACEHOLDER_UNRESOLVED", "parity": "EXPORT_PARITY",
                "client-name": "CLIENT_NAME_MISSING", "forbidden": "FORBIDDEN_TERM", "validator": "VALIDATOR_FAILED",
                "validators": "VALIDATOR_SKIPPED", "export": "EXPORT_MISSING", "draft": "DRAFT_MISSING",
            }.get(check.name.split("-")[0], "MECHANICAL_FAILED")
            if code in ("EXPORT_MISSING", "DRAFT_MISSING") and code in reasons.codes():
                continue
            reasons.add(code, f"{check.name}: {check.detail}")
        summary = evaluate_reviews(run_dir, run, draft_sha, export_sha, reasons)
        report["recorded_judgments"] = summary["required"]
        report["findings"] = summary["findings"]
        report["accepted_risks"] = summary["accepted_risks"]
    report["reasons"] = reasons.items
    report["status"] = ("READY" if stage == "delivery" else "INTAKE-COMPLETE") if not reasons.items else "INCOMPLETE"
    return report


def print_report(report: dict) -> None:
    print(f"content-workflow readiness [{report['stage']}] run={report.get('run_id')} status={report['status']}")
    hashes = report.get("hashes", {})
    for key in ("draft", "export"):
        if hashes.get(key):
            print(f"  {key} sha256: {hashes[key]}")
    for check in report.get("mechanical", []):
        print(f"  MECHANICAL {check['status'].upper():7} {check['check']}: {check['detail']}")
    for judgment in report.get("recorded_judgments", []):
        print(f"  RECORDED   {judgment['review']}: file={judgment.get('file')} verdict={judgment.get('verdict')} current={judgment.get('current')} ({judgment.get('notice')})")
    for risk in report.get("accepted_risks", []):
        print(f"  ACCEPTED RISK {risk['role']} {risk['id']}: {risk['rationale']}")
    for reason in report.get("reasons", []):
        print(f"  REASON {reason['code']}: {reason['detail']}")
    print(f"  NOTICE {report['notice']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--stage", choices=("intake", "delivery"), default="delivery")
    parser.add_argument("--json", type=Path, default=None, help="write the JSON report here (default: <run>/readiness-report.json for delivery)")
    parser.add_argument("--no-validators", action="store_true", help="skip run-declared validator commands")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    try:
        report = run_check(run_dir, args.stage, run_validators=not args.no_validators)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 2
    target = args.json or (run_dir / ("readiness-report.json" if args.stage == "delivery" else "intake-report.json"))
    cw.dump_json(target, report)
    if not args.quiet:
        print_report(report)
        print(f"  report: {target}")
    return 0 if report["status"] in ("READY", "INTAKE-COMPLETE") else 1


if __name__ == "__main__":
    sys.exit(main())
