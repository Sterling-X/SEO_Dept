#!/usr/bin/env python3
"""Run the deterministic mechanical QA on a run and write a hash-bound mechanical record.

Usage: mechanical_qa.py <run-dir> [--round N] [--stage final|checkpoint] [--no-validators] [--force]

The record is evidence that the mechanical checks and any run-declared validators were
executed against specific file hashes. It is not legal or editorial clearance.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cw_common as cw  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--round", type=int, default=0, dest="round_")
    parser.add_argument("--stage", choices=("checkpoint", "final"), default="final")
    parser.add_argument("--no-validators", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    repo_root = cw.find_repo_root()
    run = cw.load_json(run_dir / "run.json")
    draft_path = run_dir / (run.get("draft") or {}).get("path", "draft.md")
    export_rel = (run.get("export") or {}).get("path")
    export_path = run_dir / export_rel if export_rel else None
    checks, validators = cw.mechanical_checks(repo_root, run_dir, run, run_declared_validators=not args.no_validators)
    failed = [c for c in checks if c.status == "fail"]
    record = {
        "schema": cw.REVIEW_SCHEMA,
        "fixture": bool(run.get("fixture", False)),
        "role": "mechanical-qa",
        "stage": args.stage,
        "round": args.round_,
        "kind": "mechanical",
        "verdict": "pass" if not failed else "fail",
        "subject": {
            "draft_sha256": cw.sha256_file(draft_path) if draft_path.is_file() else None,
            "export_sha256": cw.sha256_file(export_path) if export_path and export_path.is_file() else None,
            "sources_sha256": {s.get("id"): (cw.sha256_file(run_dir / s["path"]) if (run_dir / s.get("path", "")).is_file() else None) for s in run.get("sources") or []},
        },
        "reviewer": {"runtime": "script", "agent": "mechanical_qa.py", "agent_file": "pilot/content-workflow/scripts/mechanical_qa.py", "agent_file_sha256": cw.sha256_file(Path(__file__).resolve())},
        "recorded_at": cw.now_iso(),
        "findings": [
            {
                "id": f"M{index + 1}",
                "severity": "blocking",
                "passage": {"location": check.name, "quote": (check.detail or check.name)[:400].ljust(8, ".")},
                "issue": f"mechanical check {check.name} failed",
                "evidence": {"check": check.name, "detail": check.detail},
                "requested_correction": "fix the underlying file and re-run mechanical QA",
                "resolution": {"status": "open", "verified_against_draft_sha256": None, "verified_by": None, "note": None},
            }
            for index, check in enumerate(failed)
        ],
        "checks": [c.as_dict() for c in checks],
        "validators": validators,
        "notice": "Mechanical evidence only. Not legal or editorial clearance.",
    }
    if not record["subject"]["draft_sha256"]:
        print("ERROR: draft is missing; nothing to bind the record to")
        return 2
    target = run_dir / "reviews" / f"mechanical-{args.stage}-r{args.round_}.json"
    if target.exists() and not args.force:
        print(f"REFUSED: {target} exists; use --force to overwrite")
        return 1
    if target.exists():
        superseded = target.parent / "superseded" / f"{target.stem}.{cw.now_iso().replace(':', '')}.json"
        superseded.parent.mkdir(parents=True, exist_ok=True)
        target.rename(superseded)
        print(f"superseded record kept at {superseded.relative_to(run_dir)}")
    cw.dump_json(target, record)
    for check in checks:
        print(f"  {check.status.upper():7} {check.name}: {check.detail}")
    print(f"mechanical QA {record['verdict'].upper()} -> {target.relative_to(run_dir)} (draft {record['subject']['draft_sha256'][:12]}…) — {record['notice']}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
