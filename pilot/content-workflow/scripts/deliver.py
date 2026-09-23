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
import readiness_check  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--allow-fixture", action="store_true", help="permit delivery of a run marked fixture: true (tests only)")
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    try:
        report = readiness_check.run_check(run_dir, "delivery", run_validators=True)
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
    copied = []
    for source, name in ((export_path, export_path.name), (run_dir / "readiness-report.json", "readiness-report.json"), (run_dir / "run.json", "run.json"), (run_dir / run.get("draft", {}).get("path", "draft.md"), "draft.md")):
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
