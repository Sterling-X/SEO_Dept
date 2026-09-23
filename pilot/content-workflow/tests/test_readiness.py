#!/usr/bin/env python3
"""Tests for the content-workflow pilot readiness check, recorder, delivery, adapters, and candidates.

Run: python3 pilot/content-workflow/tests/test_readiness.py
Every run directory is assembled in a temporary directory from tests/fixtures/valid-run and
tests/fixture_manifest.py, using the candidate skill's real generator and validators. All content
is synthetic; no real deliverable or real review record is used.
"""

from __future__ import annotations

import copy
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True
TESTS_DIR = Path(__file__).resolve().parent
PILOT_ROOT = TESTS_DIR.parent
sys.path.insert(0, str(PILOT_ROOT / "scripts"))
sys.path.insert(0, str(TESTS_DIR))

import cw_common as cw  # noqa: E402
import deliver  # noqa: E402
import fixture_manifest as fm  # noqa: E402
import pin  # noqa: E402
import readiness_check  # noqa: E402
import record_review  # noqa: E402
import render_draft  # noqa: E402

REPO_ROOT = cw.find_repo_root(PILOT_ROOT)
FIXTURE = TESTS_DIR / "fixtures" / "valid-run"
CANDIDATES = PILOT_ROOT / "candidates" / "skills"
SITUATIONAL = CANDIDATES / "family-law-situational-pages-pilot-v1"
PINNED_SKILLS = [
    "pilot/content-workflow/candidates/skills/family-law-situational-pages-pilot-v1/SKILL.md",
    "pilot/content-workflow/candidates/skills/legal-content-accuracy-qa-pilot-v1/SKILL.md",
    "pilot/content-workflow/candidates/skills/family-law-red-team-qa-reviewer-pilot-v1/SKILL.md",
    "pilot/content-workflow/candidates/skills/qa-output-checker-pilot-v1/SKILL.md",
]
EXPORT_NAME = "exampleland-high-conflict-divorce-situational.docx"


def pin_skill(rel: str) -> dict:
    return pin.pin_skill(REPO_ROOT, rel)


def record(run_dir: Path, payload: dict | str, *, agent_file: str | None = None) -> Path:
    if isinstance(payload, str):
        payload = cw.load_json(FIXTURE / "reviews" / payload)
    run = cw.load_json(run_dir / "run.json")
    agent = "legal-reviewer" if payload["role"] == "legal-reviewer" else "editorial-reviewer"
    rec, errors = record_review.build_record(
        run_dir, run, payload, runtime="claude", agent=agent, stage=payload["stage"], round_=payload["round"],
        agent_file=agent_file or f"pilot/content-workflow/adapters/claude/agents/{agent}.md", repo_root=REPO_ROOT,
    )
    if errors:
        raise AssertionError(f"record_review refused {payload.get('role')} {payload.get('stage')} r{payload.get('round')}: {errors}")
    target = run_dir / "reviews" / f"{cw.ROLE_SHORT[rec['role']]}-{rec['stage']}-r{rec['round']}.json"
    cw.dump_json(target, rec)
    return target


def mechanical(run_dir: Path, round_: int = 1) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "mechanical_qa.py"), str(run_dir), "--round", str(round_), "--force"], text=True, capture_output=True, check=False)


def build_export(run_dir: Path, manifest: dict) -> None:
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (run_dir / "export").mkdir(exist_ok=True)
    completed = subprocess.run(["node", str(SITUATIONAL / "scripts" / "build-situational.js"), str(run_dir / "manifest.json"), str(run_dir / "export" / EXPORT_NAME)], text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(f"generator failed: {completed.stdout}\n{completed.stderr}")
    (run_dir / "draft.md").write_text(render_draft.render(manifest), encoding="utf-8")


def build_run(tmp: Path, *, run_transform=None, v1_transform=None, skip_final: bool = False, final_r0_payloads: tuple | None = None) -> Path:
    """Simulate the workflow: checkpoint + initial final on v0, then revision v1, rechecks, mechanical."""
    run_dir = tmp / "run"
    shutil.copytree(FIXTURE / "sources", run_dir / "sources")
    (run_dir / "reviews").mkdir()
    run = cw.load_json(FIXTURE / "run.template.json")
    run["skills"] = [pin_skill(p) for p in PINNED_SKILLS]
    for source in run["sources"]:
        source["sha256"] = cw.sha256_file(run_dir / source["path"])
    if run_transform:
        run_transform(run)
    cw.dump_json(run_dir / "run.json", run)
    build_export(run_dir, fm.manifest_v0())
    record(run_dir, "legal-checkpoint-r0.json")
    record(run_dir, "editorial-checkpoint-r0.json")
    if final_r0_payloads is None:
        record(run_dir, "legal-final-r0.json")
        record(run_dir, "editorial-final-r0.json")
    manifest_v1 = fm.manifest_v1()
    if v1_transform:
        manifest_v1 = v1_transform(manifest_v1)
    build_export(run_dir, manifest_v1)
    if final_r0_payloads is not None:
        for payload in final_r0_payloads:
            record(run_dir, payload)
        mechanical(run_dir, 0)
        return run_dir
    if not skip_final:
        record(run_dir, "legal-final-r1.json")
        record(run_dir, "editorial-final-r1.json")
        mechanical(run_dir, 1)
    return run_dir


def check(run_dir: Path, stage: str = "delivery", *, run_validators: bool = True) -> dict:
    return readiness_check.run_check(run_dir, stage, run_validators=run_validators)


def codes(report: dict) -> list[str]:
    return [reason["code"] for reason in report["reasons"]]


def tamper_docx(path: Path, needle: str, replacement: str) -> None:
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as reader, zipfile.ZipFile(tmp, "w") as writer:
        for info in reader.infolist():
            payload = reader.read(info.filename)
            if info.filename == "word/document.xml":
                assert needle.encode("utf-8") in payload, needle
                payload = payload.replace(needle.encode("utf-8"), replacement.encode("utf-8"), 1)
            writer.writestr(info, payload)
    tmp.replace(path)


def _run_deliver(run_dir: Path, out: Path, *, allow_fixture: bool = True) -> int:
    argv = sys.argv
    sys.argv = ["deliver.py", str(run_dir), "--out", str(out)] + (["--allow-fixture"] if allow_fixture else [])
    try:
        return deliver.main()
    finally:
        sys.argv = argv


class ReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="cw-test-")
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def fresh(self) -> Path:
        return Path(tempfile.mkdtemp(dir=self.tmp))

    # -- positive ------------------------------------------------------------------
    def test_valid_generator_backed_run_with_accented_client_name_is_ready(self) -> None:
        run_dir = build_run(self.tmp)
        report = check(run_dir)
        self.assertEqual(report["status"], "READY", json.dumps(report["reasons"], indent=1, ensure_ascii=False))
        names = {c["check"]: c["status"] for c in report["mechanical"]}
        for name in ("client-name-draft", "client-name-export", "placeholders-draft", "placeholders-export", "citations-draft", "citations-export", "parity-headings", "parity-paragraphs", "parity-word-count", "validator-structural", "validator-page"):
            self.assertEqual(names.get(name), "pass", f"{name}: {names}")
        judgments = {j["review"]: j for j in report["recorded_judgments"]}
        self.assertTrue(judgments["legal-final"]["current"])
        self.assertEqual(judgments["legal-final"]["notice"], cw.JUDGMENT_NOTICE)
        self.assertIn("cannot verify", report["notice"])
        self.assertEqual(len(report["validators"]), 2)

    def test_accented_and_ampersand_names_are_not_placeholders(self) -> None:
        self.assertEqual(cw.scan_placeholders("Gómez & Núñez Family Law, P.A. with María Gómez-Núñez, Ærø and Đặng."), [])
        self.assertEqual(len(cw.scan_placeholders("Contact [FIRM_NAME] today")), 1)
        self.assertEqual(cw.scan_placeholders("cited once [1] and again [12]"), [])

    def test_intake_stage_passes_for_valid_run(self) -> None:
        run_dir = build_run(self.tmp, skip_final=True)
        report = check(run_dir, "intake")
        self.assertEqual(report["status"], "INTAKE-COMPLETE", report["reasons"])

    # -- required rejections ---------------------------------------------------------
    def test_missing_required_review(self) -> None:
        run_dir = build_run(self.tmp)
        for path in (run_dir / "reviews").glob("legal-final-*.json"):
            path.unlink()
        report = check(run_dir)
        self.assertEqual(report["status"], "INCOMPLETE")
        self.assertIn("REVIEW_MISSING", codes(report))
        self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(report))

    def test_only_stale_legal_final_is_not_enough(self) -> None:
        run_dir = build_run(self.tmp)
        (run_dir / "reviews" / "legal-final-r1.json").unlink()
        report = check(run_dir)
        self.assertIn("REVIEW_STALE", codes(report))
        self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(report))

    def test_draft_edited_after_review(self) -> None:
        run_dir = build_run(self.tmp)
        draft = run_dir / "draft.md"
        draft.write_text(draft.read_text(encoding="utf-8").replace("written findings.", "written findings in every case."), encoding="utf-8")
        report = check(run_dir)
        self.assertEqual(report["status"], "INCOMPLETE")
        stale = [r for r in report["reasons"] if r["code"] == "REVIEW_STALE"]
        self.assertGreaterEqual(len(stale), 3, "legal, editorial, and mechanical finals must all be stale")
        self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(report))
        self.assertIn("EXPORT_PARITY", codes(report), "draft and export now differ")

    def test_unresolved_blocking_finding(self) -> None:
        for status in ("open", "fixed-unverified", "disputed"):
            with self.subTest(status=status):
                run_dir = build_run(self.fresh())
                path = run_dir / "reviews" / "legal-final-r1.json"
                rec = cw.load_json(path)
                rec["findings"][0]["resolution"]["status"] = status
                cw.dump_json(path, rec)
                self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(check(run_dir)))

    def test_blocking_finding_dropped_from_latest_record_is_unresolved(self) -> None:
        run_dir = build_run(self.tmp)
        path = run_dir / "reviews" / "legal-final-r1.json"
        rec = cw.load_json(path)
        rec["findings"] = []
        cw.dump_json(path, rec)
        report = check(run_dir)
        self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(report))
        self.assertIn("dropped", " ".join(r["detail"] for r in report["reasons"]))

    def test_mismatched_citations_in_export(self) -> None:
        run_dir = build_run(self.tmp)
        tamper_docx(run_dir / "export" / EXPORT_NAME, ">[2]<", ">[3]<")
        report = check(run_dir)
        self.assertIn("CITATION_MISMATCH", codes(report))
        self.assertIn("VALIDATOR_FAILED", codes(report), "the candidate validators also reject the tampered export")
        self.assertIn("REVIEW_STALE", codes(report), "export changed after mechanical QA")

    def test_mismatched_citations_in_draft_sources(self) -> None:
        def wrong_url(manifest: dict) -> dict:
            manifest = copy.deepcopy(manifest)
            manifest["sources"][1]["url"] = "https://legislature.exampleland.example/statutes/12.999"
            return manifest
        run_dir = build_run(self.tmp, v1_transform=wrong_url)
        report = check(run_dir)
        self.assertIn("CITATION_MISMATCH", codes(report))
        details = " ".join(r["detail"] for r in report["reasons"] if r["code"] == "CITATION_MISMATCH")
        self.assertIn("12.999", details)
        self.assertIn("draft", details)
        self.assertIn("export", details)

    def test_plain_marker_in_draft_is_a_citation_mismatch(self) -> None:
        run_dir = build_run(self.tmp)
        draft = run_dir / "draft.md"
        text = draft.read_text(encoding="utf-8")
        text = re.sub(r"\[\[2\]\]\([^)]+\)", "[2]", text, count=1)
        draft.write_text(text, encoding="utf-8")
        report = check(run_dir)
        self.assertIn("CITATION_MISMATCH", codes(report))
        self.assertIn("plain text", " ".join(r["detail"] for r in report["reasons"]))

    def test_unresolved_placeholders(self) -> None:
        cases = {
            "local-detail": "[LOCAL DETAIL: county filing fee]",
            "bracket-token": "[FIRM_NAME]",
            "marker-word": "TBD",
            "mustache": "{{county}}",
        }
        for name, token in cases.items():
            with self.subTest(case=name):
                run_dir = build_run(self.fresh())
                draft = run_dir / "draft.md"
                draft.write_text(draft.read_text(encoding="utf-8").replace(fm.STAKES_V1, fm.STAKES_V1 + " " + token, 1), encoding="utf-8")
                tamper_docx(run_dir / "export" / EXPORT_NAME, fm.STAKES_V1, fm.STAKES_V1 + " " + token)
                report = check(run_dir)
                self.assertEqual(report["status"], "INCOMPLETE")
                self.assertIn("PLACEHOLDER_UNRESOLVED", codes(report))
                details = " ".join(r["detail"] for r in report["reasons"] if r["code"] == "PLACEHOLDER_UNRESOLVED")
                self.assertIn("placeholders-draft", details)
                self.assertIn("placeholders-export", details)
                self.assertIn("VALIDATOR_FAILED", codes(report), "candidate validators reject the placeholder too")

    def test_missing_required_dependency(self) -> None:
        with self.subTest(dep="skill hash mismatch"):
            run_dir = build_run(self.fresh(), skip_final=True)
            run = cw.load_json(run_dir / "run.json")
            run["skills"][0]["sha256"] = "0" * 64
            cw.dump_json(run_dir / "run.json", run)
            self.assertIn("SKILL_HASH_MISMATCH", codes(check(run_dir, "intake")))
        with self.subTest(dep="skill resource hash mismatch"):
            run_dir = build_run(self.fresh(), skip_final=True)
            run = cw.load_json(run_dir / "run.json")
            run["skills"][0]["files"]["scripts/validate-page.js"] = "0" * 64
            cw.dump_json(run_dir / "run.json", run)
            report = check(run_dir, "intake")
            self.assertIn("SKILL_HASH_MISMATCH", codes(report))
            self.assertIn("validate-page.js", " ".join(r["detail"] for r in report["reasons"]))
        with self.subTest(dep="skill pinned without resource hashes"):
            run_dir = build_run(self.fresh(), skip_final=True)
            run = cw.load_json(run_dir / "run.json")
            run["skills"][0].pop("files")
            cw.dump_json(run_dir / "run.json", run)
            self.assertIn("SKILL_PIN_MISSING", codes(check(run_dir, "intake")))
        with self.subTest(dep="skill path missing"):
            run_dir = build_run(self.fresh(), skip_final=True)
            run = cw.load_json(run_dir / "run.json")
            run["skills"][0]["path"] = "pilot/content-workflow/candidates/skills/does-not-exist/SKILL.md"
            cw.dump_json(run_dir / "run.json", run)
            self.assertIn("SKILL_PATH_MISSING", codes(check(run_dir, "intake")))
        with self.subTest(dep="skill required resource missing"):
            tmp = self.fresh()
            skill_dir = tmp / "broken-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("---\nname: broken\ndescription: test\n---\n", encoding="utf-8")
            cw.dump_json(skill_dir / "pilot-manifest.json", {"required_files": ["references/situational-template.md", "scripts/validate-page.js"]})
            run_dir = build_run(tmp, skip_final=True)
            run = cw.load_json(run_dir / "run.json")
            run["skills"].append({"name": "broken", "path": str(skill_dir / "SKILL.md"), "sha256": cw.sha256_file(skill_dir / "SKILL.md"), "files": {}})
            cw.dump_json(run_dir / "run.json", run)
            self.assertEqual(codes(check(run_dir, "intake")).count("SKILL_RESOURCE_MISSING"), 2)
        with self.subTest(dep="source file missing"):
            run_dir = build_run(self.fresh(), skip_final=True)
            (run_dir / "sources" / "legal-exampleland-rule-7.md").unlink()
            self.assertIn("SOURCE_MISSING", codes(check(run_dir, "intake")))
        with self.subTest(dep="source hash mismatch"):
            run_dir = build_run(self.fresh(), skip_final=True)
            path = run_dir / "sources" / "client-facts.md"
            path.write_text(path.read_text(encoding="utf-8") + "\n- Added after pinning.\n", encoding="utf-8")
            self.assertIn("SOURCE_HASH_MISMATCH", codes(check(run_dir, "intake")))
        with self.subTest(dep="pilot-manifest.json itself is pinned"):
            run_dir = build_run(self.fresh(), skip_final=True)
            run = cw.load_json(run_dir / "run.json")
            self.assertIn("pilot-manifest.json", run["skills"][0]["files"])
            run["skills"][0]["files"]["pilot-manifest.json"] = "0" * 64
            cw.dump_json(run_dir / "run.json", run)
            self.assertIn("SKILL_HASH_MISMATCH", codes(check(run_dir, "intake")))
        with self.subTest(dep="node_modules declared as required resources"):
            manifest = cw.load_json(SITUATIONAL / "pilot-manifest.json")
            self.assertIn("node_modules/docx/package.json", manifest["required_files"])
            self.assertEqual({v["name"] for v in manifest["validators"]}, {"structural", "page"})

    def test_missing_intake_fields_and_sources(self) -> None:
        def strip(run: dict) -> None:
            run["jurisdiction"] = ""
            run["client"]["slug"] = ""
            run["page_type"].pop("architecture_node_id")
        run_dir = build_run(self.tmp, run_transform=strip, skip_final=True)
        report = check(run_dir, "intake")
        self.assertEqual(codes(report).count("INTAKE_MISSING_FIELD"), 3)

        def no_sources(run: dict) -> None:
            run["sources"] = [s for s in run["sources"] if s["kind"] == "voice-brief"]
            run["citations"] = []
        run_dir = build_run(self.fresh(), run_transform=no_sources, skip_final=True)
        report = check(run_dir, "intake")
        self.assertEqual(codes(report).count("INTAKE_MISSING_SOURCE"), 3)

    def test_declared_validators_cannot_be_skipped_or_omitted(self) -> None:
        run_dir = build_run(self.tmp)
        report = check(run_dir, run_validators=False)
        self.assertIn("VALIDATOR_SKIPPED", codes(report))
        run = cw.load_json(run_dir / "run.json")
        run["export"]["validators"] = []
        cw.dump_json(run_dir / "run.json", run)
        self.assertIn("VALIDATORS_UNDECLARED", codes(check(run_dir, "intake")))
        run["export"]["validators"] = [{"name": "noop", "command": [sys.executable, "-c", "import sys; sys.exit(0)"]}]
        cw.dump_json(run_dir / "run.json", run)
        self.assertIn("VALIDATORS_UNDECLARED", codes(check(run_dir, "intake")), "a stand-in validator with the wrong name does not satisfy the skill's declaration")
        run["export"]["validators"] = [{"name": "structural", "command": [sys.executable, "-c", "import sys; sys.exit(3)"]}, {"name": "page", "command": [sys.executable, "-c", "import sys; sys.exit(0)"]}]
        cw.dump_json(run_dir / "run.json", run)
        report = check(run_dir)
        self.assertIn("VALIDATOR_FAILED", codes(report))
        self.assertEqual({v["name"]: v["exit_code"] for v in report["validators"]}, {"structural": 3, "page": 0})

    def test_voice_routing(self) -> None:
        with self.subTest(case="routed domain without the routed skill"):
            def routed(run: dict) -> None:
                run["client"]["domain"] = "sterlinglawyers.com"
            run_dir = build_run(self.fresh(), run_transform=routed, skip_final=True)
            self.assertIn("VOICE_MISMATCH", codes(check(run_dir, "intake")))
        with self.subTest(case="routed domain with the routed skill"):
            def routed_ok(run: dict) -> None:
                run["client"]["domain"] = "sterlinglawyers.com"
                run["voice"] = {"skill": "sterling-voice", "approved_brief_source_id": None}
            run_dir = build_run(self.fresh(), run_transform=routed_ok, skip_final=True)
            self.assertFalse({"VOICE_MISMATCH", "VOICE_UNROUTED", "VOICE_SKILL_MISSING"} & set(codes(check(run_dir, "intake"))))
        with self.subTest(case="unrouted domain with an inferred voice skill"):
            def inferred(run: dict) -> None:
                run["voice"] = {"skill": "sterling-voice", "approved_brief_source_id": None}
            run_dir = build_run(self.fresh(), run_transform=inferred, skip_final=True)
            self.assertIn("VOICE_MISMATCH", codes(check(run_dir, "intake")))
        with self.subTest(case="unrouted domain without an approved brief"):
            def no_brief(run: dict) -> None:
                run["voice"] = {"skill": None, "approved_brief_source_id": None}
            run_dir = build_run(self.fresh(), run_transform=no_brief, skip_final=True)
            self.assertIn("VOICE_UNROUTED", codes(check(run_dir, "intake")))

    def test_rounds_exceeded(self) -> None:
        run_dir = build_run(self.tmp)
        rec = cw.load_json(run_dir / "reviews" / "legal-final-r1.json")
        rec["round"] = 3
        cw.dump_json(run_dir / "reviews" / "legal-final-r3.json", rec)
        self.assertIn("ROUNDS_EXCEEDED", codes(check(run_dir)))

    def test_fixture_records_rejected_in_non_fixture_run(self) -> None:
        run_dir = build_run(self.tmp)
        run = cw.load_json(run_dir / "run.json")
        run["fixture"] = False
        cw.dump_json(run_dir / "run.json", run)
        report = check(run_dir)
        self.assertIn("FIXTURE_FLAG", codes(report))
        self.assertIn("REVIEW_MISSING", codes(report))

    def test_major_finding_disposition(self) -> None:
        with self.subTest(case="coordinator-accepted without rationale"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "editorial-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][1]["resolution"] = {"status": "coordinator-accepted", "note": "ok"}
            cw.dump_json(path, rec)
            self.assertIn("FINDING_MAJOR_UNDISPOSED", codes(check(run_dir)))
        with self.subTest(case="coordinator-accepted with rationale is an accepted risk"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "editorial-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][1]["resolution"] = {"status": "coordinator-accepted", "note": "Client approved the shorter attorney descriptor in writing on 2026-09-23; see sources/client-facts.md."}
            cw.dump_json(path, rec)
            report = check(run_dir)
            self.assertEqual(report["status"], "READY", report["reasons"])
            self.assertEqual(len(report["accepted_risks"]), 1)
        with self.subTest(case="major left open"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "editorial-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][1]["resolution"] = {"status": "open"}
            cw.dump_json(path, rec)
            self.assertIn("FINDING_MAJOR_UNDISPOSED", codes(check(run_dir)))

    # -- review findings from the independent reviewer (2026-09-23) -----------------------
    def test_mechanical_fail_then_pass_is_ready(self) -> None:
        run_dir = build_run(self.tmp)
        passing = cw.load_json(run_dir / "reviews" / "mechanical-final-r1.json")
        failed = copy.deepcopy(passing)
        failed.update({"round": 0, "verdict": "fail", "recorded_at": "2026-09-23T00:00:00+00:00"})
        failed["subject"]["draft_sha256"] = "1" * 64
        failed["findings"] = [{"id": "M1", "severity": "blocking", "passage": {"location": "placeholders-draft", "quote": "bracket-token: [FIRM_NAME]"}, "issue": "mechanical check placeholders-draft failed", "evidence": {"check": "placeholders-draft"}, "requested_correction": "fix", "resolution": {"status": "open"}}]
        cw.dump_json(run_dir / "reviews" / "mechanical-final-r0.json", failed)
        report = check(run_dir)
        self.assertEqual(report["status"], "READY", report["reasons"])

    def test_judgment_verdict_and_verification_log_block_delivery(self) -> None:
        with self.subTest(case="legal verdict not-ready with no findings"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["verdict"] = "not-ready"
            cw.dump_json(path, rec)
            self.assertIn("REVIEW_VERDICT_BLOCKING", codes(check(run_dir)))
        with self.subTest(case="editorial verdict not-ready"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "editorial-final-r1.json"
            rec = cw.load_json(path)
            rec["verdict"] = "not-ready"
            cw.dump_json(path, rec)
            self.assertIn("REVIEW_VERDICT_BLOCKING", codes(check(run_dir)))
        with self.subTest(case="legal log row Unverifiable"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["verification_log"].append({"claim": "case-management order", "authority": "Rule 7", "result": "Unverifiable", "accessed": "2026-09-23"})
            cw.dump_json(path, rec)
            self.assertIn("LEGAL_LOG_UNVERIFIED", codes(check(run_dir)))
        with self.subTest(case="ready-with-revisions with only a minor finding passes"):
            run_dir = build_run(self.fresh())
            self.assertEqual(check(run_dir)["status"], "READY")

    def test_checkpoint_finding_closed_at_initial_final_review(self) -> None:
        legal_final_r0 = cw.load_json(FIXTURE / "reviews" / "legal-final-r1.json")
        legal_final_r0["round"] = 0
        editorial_final_r0 = cw.load_json(FIXTURE / "reviews" / "editorial-final-r1.json")
        editorial_final_r0["round"] = 0
        # E2 was never raised at a checkpoint, so it cannot be closed at final r0; keep only E1 (minor, open).
        editorial_final_r0["findings"] = [f for f in editorial_final_r0["findings"] if f["id"] == "E1"]
        run_dir = build_run(self.tmp, final_r0_payloads=(legal_final_r0, editorial_final_r0))
        report = check(run_dir)
        self.assertEqual(report["status"], "READY", report["reasons"])
        # The same fixed-verified finding without a prior checkpoint record is refused by the recorder.
        run = cw.load_json(run_dir / "run.json")
        for path in (run_dir / "reviews").glob("legal-*.json"):
            path.unlink()
        _rec, errors = record_review.build_record(run_dir, run, legal_final_r0, runtime="claude", agent="legal-reviewer", stage="final", round_=0, agent_file="pilot/content-workflow/adapters/claude/agents/legal-reviewer.md", repo_root=REPO_ROOT)
        self.assertTrue(any("prior checkpoint" in e for e in errors), errors)

    def test_required_review_floor_cannot_be_lowered(self) -> None:
        def lower(run: dict) -> None:
            run["reviews"]["required"] = ["mechanical-final"]
        run_dir = build_run(self.tmp, run_transform=lower)
        for path in (run_dir / "reviews").glob("editorial-final-*.json"):
            path.unlink()
        report = check(run_dir)
        self.assertIn("REVIEW_MISSING", codes(report))
        self.assertIn("editorial-final", " ".join(r["detail"] for r in report["reasons"]))

    def test_required_checkpoint_kind_is_presence_only(self) -> None:
        def add_checkpoint(run: dict) -> None:
            run["reviews"]["required"] = ["legal-checkpoint"]
        run_dir = build_run(self.tmp, run_transform=add_checkpoint)
        report = check(run_dir)
        self.assertEqual(report["status"], "READY", report["reasons"])
        entry = next(j for j in report["recorded_judgments"] if j["review"] == "legal-checkpoint")
        self.assertEqual(entry["file"], "legal-checkpoint-r0.json")
        (run_dir / "reviews" / "legal-checkpoint-r0.json").unlink()
        report = check(run_dir)
        self.assertIn("REVIEW_MISSING", codes(report))

    def test_source_changed_after_review_is_stale(self) -> None:
        run_dir = build_run(self.tmp)
        path = run_dir / "sources" / "client-facts.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n- New office added after review.\n", encoding="utf-8")
        report = check(run_dir)
        self.assertIn("SOURCE_HASH_MISMATCH", codes(report))
        stale = [r["detail"] for r in report["reasons"] if r["code"] == "REVIEW_STALE"]
        self.assertTrue(any("client-facts" in d for d in stale), stale)

    def test_paragraph_parity_detects_export_text_change(self) -> None:
        run_dir = build_run(self.tmp)
        tamper_docx(run_dir / "export" / EXPORT_NAME, "can rebut it with evidence", "cannot rebut it with evidence")
        report = check(run_dir)
        details = " ".join(r["detail"] for r in report["reasons"] if r["code"] == "EXPORT_PARITY")
        self.assertIn("parity-paragraphs", details)
        self.assertIn("first divergence at #", details)

    def test_hand_written_record_fails_recorder_rules_at_delivery(self) -> None:
        run_dir = build_run(self.tmp)
        path = run_dir / "reviews" / "legal-final-r1.json"
        rec = cw.load_json(path)
        rec["findings"][0]["passage"]["quote"] = "A sentence that the draft never contained."
        cw.dump_json(path, rec)
        report = check(run_dir)
        self.assertIn("REVIEW_INVALID", codes(report))

    # -- recorder ----------------------------------------------------------------------
    def test_record_review_rejects_quote_not_in_draft(self) -> None:
        run_dir = build_run(self.tmp, skip_final=True)
        run = cw.load_json(run_dir / "run.json")
        payload = cw.load_json(FIXTURE / "reviews" / "legal-final-r1.json")
        payload["findings"][0]["passage"]["quote"] = "This sentence was never in the draft at all."
        _rec, errors = record_review.build_record(run_dir, run, payload, runtime="claude", agent="legal-reviewer", stage="final", round_=1, agent_file="pilot/content-workflow/adapters/claude/agents/legal-reviewer.md", repo_root=REPO_ROOT)
        self.assertTrue(any("not found in the current draft" in e for e in errors), errors)

    def test_record_review_rejects_role_agent_mismatch_and_echoed_hash(self) -> None:
        run_dir = build_run(self.tmp, skip_final=True)
        run = cw.load_json(run_dir / "run.json")
        payload = cw.load_json(FIXTURE / "reviews" / "legal-final-r1.json")
        _rec, errors = record_review.build_record(run_dir, run, payload, runtime="claude", agent="editorial-reviewer", stage="final", round_=1, agent_file="pilot/content-workflow/adapters/claude/agents/editorial-reviewer.md", repo_root=REPO_ROOT)
        self.assertTrue(any("declares role" in e for e in errors), errors)
        payload["subject"] = {"draft_sha256": "f" * 64}
        _rec, errors = record_review.build_record(run_dir, run, payload, runtime="claude", agent="legal-reviewer", stage="final", round_=1, agent_file="pilot/content-workflow/adapters/claude/agents/legal-reviewer.md", repo_root=REPO_ROOT)
        self.assertTrue(any("echoed draft hash" in e for e in errors), errors)

    def test_record_review_rejects_missing_agent_file(self) -> None:
        run_dir = build_run(self.tmp, skip_final=True)
        run = cw.load_json(run_dir / "run.json")
        payload = cw.load_json(FIXTURE / "reviews" / "editorial-checkpoint-r0.json")
        _rec, errors = record_review.build_record(run_dir, run, payload, runtime="codex", agent="editorial_reviewer", stage="checkpoint", round_=0, agent_file=".codex/agents/not-activated.toml", repo_root=REPO_ROOT)
        self.assertTrue(any("does not exist" in e for e in errors), errors)

    # -- delivery ----------------------------------------------------------------------
    def test_deliver_refuses_incomplete_and_copies_nothing(self) -> None:
        run_dir = build_run(self.tmp)
        for path in (run_dir / "reviews").glob("editorial-final-*.json"):
            path.unlink()
        out = self.tmp / "out"
        with redirect_stdout(io.StringIO()):
            code = _run_deliver(run_dir, out)
        self.assertEqual(code, 1)
        self.assertFalse(out.exists() and any(out.iterdir()))
        status = cw.load_json(run_dir / "delivery-status.json")
        self.assertEqual(status["status"], "INCOMPLETE")
        self.assertIn("REVIEW_MISSING", [r["code"] for r in status["reasons"]])

    def test_deliver_ready_copies_export_and_report(self) -> None:
        run_dir = build_run(self.tmp)
        out = self.tmp / "out"
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = _run_deliver(run_dir, out)
        self.assertEqual(code, 0, buffer.getvalue())
        self.assertTrue((out / EXPORT_NAME).is_file())
        self.assertTrue((out / "readiness-report.json").is_file())
        status = cw.load_json(run_dir / "delivery-status.json")
        self.assertEqual(status["status"], "READY")
        self.assertIn("cannot verify", status["notice"])

    def test_deliver_refuses_fixture_run_without_flag(self) -> None:
        run_dir = build_run(self.tmp)
        out = self.tmp / "out"
        with redirect_stdout(io.StringIO()):
            code = _run_deliver(run_dir, out, allow_fixture=False)
        self.assertEqual(code, 1)
        self.assertIn("FIXTURE_DELIVERY", [r["code"] for r in cw.load_json(run_dir / "delivery-status.json")["reasons"]])
        self.assertFalse(out.exists() and any(out.iterdir()))

    # -- shared design ------------------------------------------------------------------
    def test_adapters_match_canonical_roles(self) -> None:
        completed = subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "build_adapters.py"), "--check"], text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        for role in ("content-writer", "legal-reviewer", "editorial-reviewer"):
            canonical = (PILOT_ROOT / "canonical" / "roles" / f"{role}.md").read_text(encoding="utf-8").strip()
            self.assertIn(canonical, (PILOT_ROOT / "adapters" / "claude" / "agents" / f"{role}.md").read_text(encoding="utf-8"))
            self.assertIn(canonical, (PILOT_ROOT / "adapters" / "codex" / "agents" / f"{role.replace('-', '_')}.toml").read_text(encoding="utf-8"))

    def test_reviewer_adapters_are_read_only_and_cannot_delegate(self) -> None:
        import tomllib
        for role in ("legal-reviewer", "editorial-reviewer"):
            fm_text = (PILOT_ROOT / "adapters" / "claude" / "agents" / f"{role}.md").read_text(encoding="utf-8").split("---")[1]
            tools_line = next(line for line in fm_text.splitlines() if line.startswith("tools:"))
            tools = {t.strip() for t in tools_line.split(":", 1)[1].split(",")}
            self.assertFalse(tools & {"Agent", "Task", "Write", "Edit", "Bash", "NotebookEdit"}, tools)
            toml = tomllib.loads((PILOT_ROOT / "adapters" / "codex" / "agents" / f"{role.replace('-', '_')}.toml").read_text(encoding="utf-8"))
            self.assertEqual(toml["sandbox_mode"], "read-only")
            self.assertIn("must not spawn agents", toml["developer_instructions"])
        writer_fm = (PILOT_ROOT / "adapters" / "claude" / "agents" / "content-writer.md").read_text(encoding="utf-8").split("---")[1]
        self.assertNotIn("Agent", next(l for l in writer_fm.splitlines() if l.startswith("tools:")))

    def test_client_routing_matches_agents_md(self) -> None:
        routing = cw.load_json(PILOT_ROOT / "canonical" / "client-routing.json")["routes"]
        agents_md = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        section = agents_md.split("## Client voice routing", 1)[1].split("\n## ", 1)[0]
        pairs = dict(re.findall(r"`([a-z0-9.-]+)` → `([a-z-]+)`", section))
        self.assertEqual(pairs, routing)
        for skill in routing.values():
            self.assertTrue((REPO_ROOT / ".agents" / "skills" / skill / "SKILL.md").is_file(), skill)

    def test_placeholder_grammar_has_one_source(self) -> None:
        spec = cw.load_json(PILOT_ROOT / "canonical" / "placeholder-patterns.json")
        canon = [(p["regex"], bool(p["ignore_case"])) for p in spec["patterns"]]
        js = (SITUATIONAL / "scripts" / "validate-page.js").read_text(encoding="utf-8")
        py = (SITUATIONAL / "scripts" / "office" / "validate.py").read_text(encoding="utf-8")
        gen = (SITUATIONAL / "scripts" / "build-situational.js").read_text(encoding="utf-8")
        def js_patterns(src: str) -> list:
            block = re.search(r"const PLACEHOLDER_PATTERNS = \[(.*?)\];", src, re.S).group(1)
            return [(m.group(1), bool(m.group(2))) for m in re.finditer(r"^\s*/((?:\\.|[^/\n])+)/(i?),\s*$", block, re.M)]
        def py_patterns(src: str) -> list:
            block = re.search(r"PLACEHOLDER_PATTERNS = \[(.*?)\n\]", src, re.S).group(1)
            return [(m.group(1), bool(m.group(2))) for m in re.finditer(r're\.compile\(r"((?:\\.|[^"\n])+)"(, re\.IGNORECASE)?\)', block)]
        self.assertEqual(js_patterns(js), canon, "validate-page.js drifted from canonical/placeholder-patterns.json")
        self.assertEqual(js_patterns(gen), canon, "build-situational.js drifted from canonical/placeholder-patterns.json")
        self.assertEqual(py_patterns(py), canon, "office/validate.py drifted from canonical/placeholder-patterns.json")
        self.assertEqual([(p.pattern, bool(p.flags & re.IGNORECASE)) for _k, p in cw.PLACEHOLDER_PATTERNS], canon)

    def test_candidate_manifests_and_baseline_provenance(self) -> None:
        for candidate in sorted(CANDIDATES.iterdir()):
            manifest = cw.load_json(candidate / "pilot-manifest.json")
            self.assertEqual(manifest["status"], "candidate; not production default")
            for required in manifest["required_files"]:
                self.assertTrue((candidate / required).exists(), f"{candidate.name}: {required}")
            for rel, digest in manifest["baseline"]["files"].items():
                baseline_file = REPO_ROOT / manifest["baseline"]["path"] / rel
                self.assertTrue(baseline_file.is_file(), baseline_file)
                self.assertEqual(cw.sha256_file(baseline_file), digest, f"baseline drifted: {baseline_file}")
            name = re.search(r"^name:\s*(\S+)", (candidate / "SKILL.md").read_text(encoding="utf-8"), re.M).group(1)
            self.assertEqual(name, candidate.name)
            self.assertTrue((candidate / "CHANGES.md").is_file())

    def test_candidates_are_outside_discovery_paths(self) -> None:
        for candidate in CANDIDATES.iterdir():
            for root in (REPO_ROOT / ".agents" / "skills", REPO_ROOT / ".claude" / "skills"):
                self.assertFalse((root / candidate.name).exists(), f"{candidate.name} must not be in {root}")

    def test_candidate_situational_regression_suite(self) -> None:
        completed = subprocess.run([sys.executable, str(SITUATIONAL / "scripts" / "test-situational.py")], text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout[-4000:])
        self.assertIn("negative-plaintext-citation-marker-page", completed.stdout)
        self.assertIn("negative-bracket-placeholder-page", completed.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
