#!/usr/bin/env python3
"""Record a coordinator disposition without editing a reviewer's record.

Usage: dispose_finding.py <run-dir> --role <legal-reviewer|editorial-reviewer> --id <E2> --accept --rationale "<40+ chars>"

Writes reviews/coordinator-dispositions.json (append-only list, each entry bound to the current
draft hash). The readiness check applies a disposition only to a `major` finding outside the
protected categories (legal-accuracy, citation, client-fact, promise), only while the draft hash
still matches, and reports it as an accepted risk. It never closes a blocking finding.
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
    parser.add_argument("--role", required=True, choices=("legal-reviewer", "editorial-reviewer"))
    parser.add_argument("--id", required=True)
    parser.add_argument("--accept", action="store_true", help="record coordinator-accepted (the only disposition this tool writes)")
    parser.add_argument("--rationale", required=True)
    args = parser.parse_args()
    if not args.accept:
        parser.error("--accept is required; other statuses belong to the raising reviewer")
    run_dir = args.run_dir.resolve()
    run = cw.load_json(run_dir / "run.json")
    draft_path = run_dir / (run.get("draft") or {}).get("path", "draft.md")
    if not draft_path.is_file():
        print("ERROR: no draft to bind the disposition to")
        return 2
    rationale = cw.norm_ws(args.rationale)
    if len(rationale) < 40:
        print("REFUSED: rationale must be at least 40 characters")
        return 1
    # Locate the finding as first raised, to refuse protected or blocking findings up front.
    first = None
    records = sorted((cw.load_json(path) for path in cw.review_files(run_dir)), key=cw.record_order_key)
    for record in records:
        if record.get("role") != args.role:
            continue
        for finding in record.get("findings", []):
            if str(finding.get("id")) == args.id and first is None:
                first = finding
    if first is None:
        print(f"REFUSED: no {args.role} finding {args.id} exists in reviews/")
        return 1
    if first.get("severity") != "major":
        print(f"REFUSED: {args.id} was raised as {first.get('severity')}; only major findings can be coordinator-accepted")
        return 1
    if (first.get("category") or "other") in cw.PROTECTED_CATEGORIES:
        print(f"REFUSED: {args.id} is a {first.get('category')} finding; it closes only through the raising reviewer's recheck")
        return 1
    target = run_dir / "reviews" / "coordinator-dispositions.json"
    payload = cw.load_json(target) if target.is_file() else {"schema": "content-workflow-dispositions/v1", "dispositions": []}
    payload["dispositions"].append({
        "role": args.role, "id": args.id, "status": "coordinator-accepted", "rationale": rationale,
        "draft_sha256": cw.sha256_file(draft_path), "decided_at": cw.now_iso(), "decided_by": "coordinator",
    })
    cw.dump_json(target, payload)
    print(f"recorded coordinator acceptance of {args.role} {args.id} against draft {cw.sha256_file(draft_path)[:12]}… -> {target.relative_to(run_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
