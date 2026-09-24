#!/usr/bin/env python3
"""Delivery command: refuse READY unless the full readiness check passes.

Usage: deliver.py <run-dir> [--out <dir>] [--allow-fixture]

Runs readiness_check.py at the delivery stage (which validates the exported document as
well as the draft), writes delivery-status.json in the run, and on READY copies the
export, run.json (without source contents), and the readiness report to the delivery
directory (default: pilot/content-workflow/deliveries/<run_id>/, Git-ignored). On
INCOMPLETE it copies nothing. It never edits records to reach READY.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cw_common as cw  # noqa: E402
import cw_research as rs  # noqa: E402
import readiness_check  # noqa: E402


def write_ledger(run_dir: Path, run: dict, report: dict) -> Path:
    """Reader-facing research ledger: sources retrieved, times, currency, live re-check, claims supported."""
    rows: list[dict] = []
    for path in cw.review_files(run_dir):
        try:
            record = cw.load_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        if record.get("role") == "legal-reviewer":
            rows.extend(r for r in record.get("verification_log") or [] if isinstance(r, dict))
    target = run_dir / "research-ledger.md"
    target.write_text(rs.ledger_markdown(run, report.get("research") or {}, rows), encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--allow-fixture", action="store_true", help="permit delivery of a run marked fixture: true (tests only)")
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    try:
        # Delivery always re-verifies research live; there is no offline delivery.
        report = readiness_check.run_check(run_dir, "delivery", run_validators=True, live_research=True)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 2
    if report.get("fixture") and not args.allow_fixture:
        report["reasons"].append({"code": "FIXTURE_DELIVERY", "detail": "run.json marks this run as a fixture; synthetic runs are not delivered (use --allow-fixture only in tests)"})
        report["status"] = "INCOMPLETE"
    cw.dump_json(run_dir / "readiness-report.json", report)
    readiness_check.print_report(report)
    status = {
        "schema": "content-workflow-delivery/v1",
        "run_id": report.get("run_id"),
        "status": report["status"],
        "decided_at": cw.now_iso(),
        "readiness_report": "readiness-report.json",
        "hashes": report.get("hashes", {}),
        "reasons": report.get("reasons", []),
        "accepted_risks": report.get("accepted_risks", []),
        "delivered_files": [],
        "notice": report["notice"],
    }
    if report["status"] != "READY":
        cw.dump_json(run_dir / "delivery-status.json", status)
        print(f"DELIVERY REFUSED: status {report['status']} with {len(report.get('reasons', []))} reason(s). Nothing was copied.")
        return 1
    run = cw.load_json(run_dir / "run.json")
    out = (args.out or (cw.PILOT_ROOT / "deliveries" / str(run.get("run_id")))).resolve()
    out.mkdir(parents=True, exist_ok=True)
    export_path = run_dir / run["export"]["path"]
    ledger_path = write_ledger(run_dir, run, report)
    copied = []
    for source, name in ((export_path, export_path.name), (run_dir / "readiness-report.json", "readiness-report.json"), (run_dir / "run.json", "run.json"), (run_dir / run.get("draft", {}).get("path", "draft.md"), "draft.md"), (ledger_path, "research-ledger.md")):
        if source.is_file():
            shutil.copy2(source, out / name)
            copied.append(str(out / name))
    status["delivered_files"] = copied
    status["delivery_dir"] = str(out)
    cw.dump_json(run_dir / "delivery-status.json", status)
    print(f"READY: delivered {len(copied)} file(s) to {out}")
    print(f"NOTICE: {report['notice']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
