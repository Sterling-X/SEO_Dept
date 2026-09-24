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
import render_inspect  # noqa: E402

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


PAYLOAD_TRANSFORM = None  # optional hook applied to every fixture payload before recording (set by tests)


def record(run_dir: Path, payload: dict | str, *, agent_file: str | None = None) -> Path:
    if isinstance(payload, str):
        payload = cw.load_json(FIXTURE / "reviews" / payload)
    run = cw.load_json(run_dir / "run.json")
    agent = "legal-reviewer" if payload["role"] == "legal-reviewer" else "editorial-reviewer"
    payload = copy.deepcopy(payload)
    if PAYLOAD_TRANSFORM is not None:
        payload = PAYLOAD_TRANSFORM(payload)
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


def render_and_attest(run_dir: Path, round_: int = 1) -> Path:
    """Render with the pinned wrapper and attach the synthetic fixture attestation (fixture runs only)."""
    completed = subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "render_inspect.py"), str(run_dir), "--round", str(round_), "--render", "--force"], text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(f"render failed: {completed.stdout}\n{completed.stderr}")
    record_path = run_dir / "reviews" / f"render-final-r{round_}.json"
    rec = cw.load_json(record_path)
    attestation = cw.load_json(FIXTURE / "render-attestation.template.json")
    attestation["pages"] = []
    for page in rec["render"]["pages"]:
        words = (run_dir / page["text_path"]).read_text(encoding="utf-8").split()
        quoted = " ".join(words[:5]) if len(words) >= 5 else "no text on page"
        attestation["pages"].append({"page": page["page"], "observation": f"FIXTURE observation: page opens with '{quoted}'; layout not actually viewed (synthetic attestation)"})
    attestation_path = run_dir / "render-attestation.json"
    cw.dump_json(attestation_path, attestation)
    render_inspect.attest(run_dir, record_path, attestation)
    return record_path


def build_export(run_dir: Path, manifest: dict) -> None:
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (run_dir / "export").mkdir(exist_ok=True)
    completed = subprocess.run(["node", str(SITUATIONAL / "scripts" / "build-situational.js"), str(run_dir / "manifest.json"), str(run_dir / "export" / EXPORT_NAME)], text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError(f"generator failed: {completed.stdout}\n{completed.stderr}")
    (run_dir / "draft.md").write_text(render_draft.render(manifest), encoding="utf-8")


def build_run(tmp: Path, *, run_transform=None, v1_transform=None, skip_final: bool = False, final_r0_payloads: tuple | None = None, render: bool = True) -> Path:
    """Simulate the workflow: pre-draft legal verification, checkpoint + initial final on v0, revision v1,
    rechecks, mechanical QA, and (unless render=False) the rendered-page inspection record."""
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
    record(run_dir, "legal-predraft-r0.json")
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
        if render:
            render_and_attest(run_dir, 0)
        return run_dir
    if not skip_final:
        record(run_dir, "legal-final-r1.json")
        record(run_dir, "editorial-final-r1.json")
        mechanical(run_dir, 1)
        if render:
            render_and_attest(run_dir, 1)
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
        self.assertTrue(judgments["legal-predraft"]["current"])
        self.assertTrue(judgments["render-final"]["current"])
        self.assertEqual(set(judgments), set(cw.required_review_floor(cw.load_json(run_dir / "run.json"))))
        self.assertIn("cannot verify", report["notice"])
        self.assertEqual(len(report["validators"]), 2)
        draft = (run_dir / "draft.md").read_text(encoding="utf-8")
        self.assertEqual(draft.count("[[2]]("), 2, "the fixture cites source 2 twice with one identity")

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
        run_dir = build_run(self.tmp, render=False)
        for path in (run_dir / "reviews").glob("legal-final-*.json"):
            path.unlink()
        report = check(run_dir)
        self.assertEqual(report["status"], "INCOMPLETE")
        self.assertIn("REVIEW_MISSING", codes(report))
        self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(report))

    def test_only_stale_legal_final_is_not_enough(self) -> None:
        run_dir = build_run(self.tmp, render=False)
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
                run_dir = build_run(self.fresh(), render=False)
                path = run_dir / "reviews" / "legal-final-r1.json"
                rec = cw.load_json(path)
                rec["findings"][0]["resolution"]["status"] = status
                cw.dump_json(path, rec)
                self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(check(run_dir)))

    def test_blocking_finding_dropped_from_latest_record_is_unresolved(self) -> None:
        run_dir = build_run(self.tmp, render=False)
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
        run_dir = build_run(self.tmp, v1_transform=wrong_url, render=False)
        report = check(run_dir)
        self.assertIn("CITATION_MISMATCH", codes(report))
        details = " ".join(r["detail"] for r in report["reasons"] if r["code"] == "CITATION_MISMATCH")
        self.assertIn("12.999", details)
        self.assertIn("draft", details)
        self.assertIn("export", details)

    def test_plain_marker_in_draft_is_a_citation_mismatch(self) -> None:
        run_dir = build_run(self.tmp, render=False)
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
                run_dir = build_run(self.fresh(), render=False)
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
        run_dir = build_run(self.tmp, render=False)
        rec = cw.load_json(run_dir / "reviews" / "legal-final-r1.json")
        rec["round"] = 3
        cw.dump_json(run_dir / "reviews" / "legal-final-r3.json", rec)
        self.assertIn("ROUNDS_EXCEEDED", codes(check(run_dir)))

    def test_fixture_records_rejected_in_non_fixture_run(self) -> None:
        run_dir = build_run(self.tmp, render=False)
        run = cw.load_json(run_dir / "run.json")
        run["fixture"] = False
        cw.dump_json(run_dir / "run.json", run)
        report = check(run_dir)
        self.assertIn("FIXTURE_FLAG", codes(report))
        self.assertIn("REVIEW_MISSING", codes(report))

    def test_major_finding_disposition(self) -> None:
        with self.subTest(case="coordinator-accepted without rationale"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "editorial-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][1]["resolution"] = {"status": "coordinator-accepted", "note": "ok"}
            cw.dump_json(path, rec)
            self.assertIn("FINDING_MAJOR_UNDISPOSED", codes(check(run_dir)))
        with self.subTest(case="coordinator-accepted on a protected client-fact finding is refused even with a rationale"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "editorial-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][1]["resolution"] = {"status": "coordinator-accepted", "note": "Client approved the shorter attorney descriptor in writing on 2026-09-23; see sources/client-facts.md."}
            cw.dump_json(path, rec)
            report = check(run_dir)
            self.assertIn("FINDING_MAJOR_UNDISPOSED", codes(report))
            self.assertIn("cannot be closed by coordinator acceptance", " ".join(r["detail"] for r in report["reasons"]))
        with self.subTest(case="coordinator acceptance of a major brand finding is recorded by dispose_finding.py, not by editing the record"):
            def e1_major(payload: dict) -> dict:
                payload = copy.deepcopy(payload)
                for f in payload["findings"]:
                    if f["id"] == "E1":
                        f["severity"] = "major"
                return payload
            global PAYLOAD_TRANSFORM
            PAYLOAD_TRANSFORM = e1_major  # E1 raised as major from the first record (origin governs)
            try:
                run_dir = build_run(self.fresh())
            finally:
                PAYLOAD_TRANSFORM = None
            self.assertIn("FINDING_MAJOR_UNDISPOSED", codes(check(run_dir)))
            completed = subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "dispose_finding.py"), str(run_dir), "--role", "editorial-reviewer", "--id", "E1", "--accept", "--rationale", "Register choice accepted for this fixture after comparing the approved voice brief; no client fact or legal claim is affected."], text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            report = check(run_dir)
            self.assertEqual(report["status"], "READY", report["reasons"])
            self.assertEqual(len(report["accepted_risks"]), 1)
            refused = subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "dispose_finding.py"), str(run_dir), "--role", "editorial-reviewer", "--id", "E2", "--accept", "--rationale", "Attempting to accept a client-fact finding, which the tool must refuse regardless of rationale length."], text=True, capture_output=True, check=False)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("closes only through the raising reviewer", refused.stdout)
        with self.subTest(case="major left open"):
            run_dir = build_run(self.fresh(), render=False)
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
        failed["findings"] = [{"id": "M1", "severity": "blocking", "category": "mechanical", "passage": {"location": "placeholders-draft", "quote": "bracket-token: [FIRM_NAME]"}, "issue": "mechanical check placeholders-draft failed", "evidence": {"check": "placeholders-draft"}, "requested_correction": "fix", "resolution": {"status": "open"}}]
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
        run_dir = build_run(self.tmp, run_transform=lower, render=False)
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
        run_dir = build_run(self.tmp, render=False)
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
        run_dir = build_run(self.tmp, render=False)
        path = run_dir / "reviews" / "legal-final-r1.json"
        rec = cw.load_json(path)
        rec["findings"][0]["passage"]["quote"] = "A sentence that the draft never contained."
        rec["findings"][0]["resolution"]["status"] = "open"
        cw.dump_json(path, rec)
        report = check(run_dir)
        self.assertIn("REVIEW_INVALID", codes(report))

    # -- refinements integrated from the comparison patch (2026-09-23) ---------------------
    def test_predraft_legal_verification_is_required_and_bound_to_sources(self) -> None:
        run_dir = build_run(self.tmp)
        report = check(run_dir)
        self.assertEqual(report["status"], "READY", report["reasons"])
        path = run_dir / "reviews" / "legal-predraft-r0.json"
        rec = cw.load_json(path)
        rec["verification_log"] = [row for row in rec["verification_log"] if "12.350" not in row["url"]]
        cw.dump_json(path, rec)
        report = check(run_dir)
        self.assertIn("LEGAL_PREDRAFT_COVERAGE", codes(report))
        rec = cw.load_json(path)
        rec["verification_log"].append({"claim": "extra", "url": "https://legislature.exampleland.example/statutes/12.350", "result": "Unverifiable", "accessed": "2026-09-23"})
        cw.dump_json(path, rec)
        self.assertIn("LEGAL_LOG_UNVERIFIED", codes(check(run_dir)))
        path.unlink()
        report = check(run_dir)
        self.assertIn("REVIEW_MISSING", codes(report))
        self.assertIn("legal-predraft", " ".join(r["detail"] for r in report["reasons"]))

    def test_checkpoints_are_required_for_family_law_pages(self) -> None:
        run_dir = build_run(self.tmp, render=False)
        (run_dir / "reviews" / "editorial-checkpoint-r0.json").unlink()
        report = check(run_dir)
        self.assertIn("REVIEW_MISSING", codes(report))
        self.assertIn("editorial-checkpoint", " ".join(r["detail"] for r in report["reasons"]))

    def test_render_inspection_is_required_and_bound_to_export(self) -> None:
        with self.subTest(case="missing render record"):
            run_dir = build_run(self.fresh(), render=False)
            report = check(run_dir)
            self.assertIn("REVIEW_MISSING", codes(report))
            self.assertIn("render-final", " ".join(r["detail"] for r in report["reasons"]))
        with self.subTest(case="export changed after inspection"):
            run_dir = build_run(self.fresh())
            tamper_docx(run_dir / "export" / EXPORT_NAME, "can rebut it with evidence", "can  rebut it with evidence")
            report = check(run_dir)
            stale = [r["detail"] for r in report["reasons"] if r["code"] == "REVIEW_STALE"]
            self.assertTrue(any("inspected export" in d for d in stale), stale)
        with self.subTest(case="uninspected page"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "render-final-r1.json"
            rec = cw.load_json(path)
            rec["render"]["pages"][-1]["inspected"] = False
            rec["render"]["pages"][-1]["observation"] = None
            cw.dump_json(path, rec)
            self.assertIn("RENDER_UNINSPECTED", codes(check(run_dir)))
        with self.subTest(case="page image changed after inspection"):
            run_dir = build_run(self.fresh())
            rec = cw.load_json(run_dir / "reviews" / "render-final-r1.json")
            image = run_dir / rec["render"]["pages"][0]["path"]
            with image.open("ab") as handle:
                handle.write(b"tamper")
            self.assertIn("RENDER_EVIDENCE_MISMATCH", codes(check(run_dir)))
        with self.subTest(case="pending verdict never passes"):
            run_dir = build_run(self.fresh(), render=False)
            completed = subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "render_inspect.py"), str(run_dir), "--round", "1", "--render"], text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            report = check(run_dir)
            self.assertIn("RENDER_FAILED", codes(report))
            self.assertIn("RENDER_UNINSPECTED", codes(report))
        with self.subTest(case="attestation refuses a short observation"):
            run_dir = build_run(self.fresh(), render=False)
            subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "render_inspect.py"), str(run_dir), "--round", "1", "--render"], text=True, capture_output=True, check=False)
            record_path = run_dir / "reviews" / "render-final-r1.json"
            pages = cw.load_json(record_path)["render"]["page_count"]
            bad = {"inspector": {"runtime": "human", "agent": "fixture-inspector"}, "verdict": "pass", "pages": [{"page": n, "observation": "ok"} for n in range(1, pages + 1)]}
            with self.assertRaises(SystemExit) as ctx:
                render_inspect.attest(run_dir, record_path, bad)
            self.assertIn("observation of at least 15", str(ctx.exception))

    def test_render_fail_then_reexport_then_pass_is_ready(self) -> None:
        run_dir = build_run(self.tmp, render=False)
        subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "render_inspect.py"), str(run_dir), "--round", "1", "--render"], text=True, capture_output=True, check=True)
        record_path = run_dir / "reviews" / "render-final-r1.json"
        rec = cw.load_json(record_path)
        words = (run_dir / rec["render"]["pages"][0]["text_path"]).read_text(encoding="utf-8").split()[:5]
        failing = {"inspector": {"runtime": "human", "agent": "fixture-inspector"}, "verdict": "fail",
                   "pages": [{"page": p["page"], "observation": f"FIXTURE: page shows '{' '.join((run_dir / p['text_path']).read_text(encoding='utf-8').split()[:5])}' with a clipped heading"} for p in rec["render"]["pages"]],
                   "findings": [{"id": "R1", "severity": "blocking", "category": "render", "passage": {"location": "page 1", "quote": " ".join(words)}, "issue": "heading clipped at the right margin", "evidence": {"page": 1}, "requested_correction": "re-export with corrected spacing", "resolution": {"status": "open"}}]}
        render_inspect.attest(run_dir, record_path, failing)
        report = check(run_dir)
        self.assertIn("RENDER_FAILED", codes(report))
        # "Fix" by re-exporting (same manifest here), re-render as round 2, attest pass with no findings.
        build_export(run_dir, fm.manifest_v1())
        record(run_dir, "legal-final-r1.json") if not (run_dir / "reviews" / "legal-final-r1.json").exists() else None
        mechanical(run_dir, 2)
        render_and_attest(run_dir, 2)
        report = check(run_dir)
        self.assertEqual(report["status"], "READY", report["reasons"])
        self.assertNotIn("FINDING_BLOCKING_UNRESOLVED", codes(report))

    def test_gate_reapplies_render_attestation_rules_to_hand_written_records(self) -> None:
        """A render record edited by hand must fail the same rules render_inspect.attest() enforces."""
        with self.subTest(case="page text changed after rendering"):
            run_dir = build_run(self.fresh())
            rec = cw.load_json(run_dir / "reviews" / "render-final-r1.json")
            text_path = run_dir / rec["render"]["pages"][0]["text_path"]
            text_path.write_text(text_path.read_text(encoding="utf-8") + " tampered", encoding="utf-8")
            report = check(run_dir)
            self.assertIn("RENDER_EVIDENCE_MISMATCH", codes(report))
            self.assertIn("text file missing or changed", " ".join(r["detail"] for r in report["reasons"]))
        with self.subTest(case="observation that does not quote the page"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "render-final-r1.json"
            rec = cw.load_json(path)
            rec["render"]["pages"][0]["observation"] = "Looks good, no clipping, fonts readable, spacing fine."
            cw.dump_json(path, rec)
            report = check(run_dir)
            self.assertIn("RENDER_UNINSPECTED", codes(report))
            self.assertIn("three consecutive words", " ".join(r["detail"] for r in report["reasons"]))
        with self.subTest(case="pass verdict with an open blocking render finding"):
            run_dir = build_run(self.fresh())
            path = run_dir / "reviews" / "render-final-r1.json"
            rec = cw.load_json(path)
            words = (run_dir / rec["render"]["pages"][0]["text_path"]).read_text(encoding="utf-8").split()[:5]
            rec["findings"] = [{"id": "R1", "severity": "blocking", "category": "render", "passage": {"location": "page 1", "quote": " ".join(words)}, "issue": "heading clipped at the right margin", "evidence": {"page": 1}, "requested_correction": "re-export", "resolution": {"status": "open"}}]
            cw.dump_json(path, rec)
            report = check(run_dir)
            self.assertIn("RENDER_FAILED", codes(report))
            self.assertIn("R1", " ".join(r["detail"] for r in report["reasons"]))
        with self.subTest(case="untampered record still passes"):
            run_dir = build_run(self.fresh())
            self.assertEqual(check(run_dir)["status"], "READY")

    def test_observation_match_ignores_attached_punctuation(self) -> None:
        page = "PROPOSED REPLACEMENT DRAFT | NOT PUBLISHED\nHigh-Conflict Divorce in Wisconsin\nA high-conflict divorce means your spouse's behavior decides."
        self.assertTrue(cw.observation_matches_page("H1 'High-Conflict Divorce in Wisconsin', two opening paragraphs; no clipping.", page))
        self.assertTrue(cw.observation_matches_page("banner reads \u201cNOT PUBLISHED\u201d, H1 present, (your spouse's behavior) visible", page))
        self.assertFalse(cw.observation_matches_page("Looks good, no clipping, fonts readable, spacing fine.", page))
        self.assertFalse(cw.observation_matches_page("Wisconsin divorce conflict high", page))

    def test_attestation_must_quote_the_page(self) -> None:
        run_dir = build_run(self.tmp, render=False)
        subprocess.run([sys.executable, str(PILOT_ROOT / "scripts" / "render_inspect.py"), str(run_dir), "--round", "1", "--render"], text=True, capture_output=True, check=True)
        record_path = run_dir / "reviews" / "render-final-r1.json"
        pages = cw.load_json(record_path)["render"]["page_count"]
        generic = {"inspector": {"runtime": "human", "agent": "fixture-inspector"}, "verdict": "pass", "pages": [{"page": n, "observation": "Looks good, no clipping, fonts readable, spacing fine."} for n in range(1, pages + 1)]}
        with self.assertRaises(SystemExit) as ctx:
            render_inspect.attest(run_dir, record_path, generic)
        self.assertIn("three consecutive words", str(ctx.exception))

    def test_finding_drift_and_reattribution_are_caught(self) -> None:
        with self.subTest(case="severity downgraded in the latest record"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][0]["severity"] = "minor"
            rec["findings"][0]["resolution"] = {"status": "open"}
            cw.dump_json(path, rec)
            report = check(run_dir)
            self.assertIn("FINDING_DRIFT", codes(report))
            self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(report), "origin severity governs")
        with self.subTest(case="closing record attributed to a different agent"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["reviewer"]["agent"] = "coordinator"
            rec["findings"][0]["resolution"]["verified_by"] = "coordinator"
            cw.dump_json(path, rec)
            self.assertIn("not by the raising reviewer", " ".join(r["detail"] for r in check(run_dir)["reasons"]))
        with self.subTest(case="corrected_text identical to the targeted passage"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][0]["resolution"]["corrected_text"] = rec["findings"][0]["passage"]["quote"]
            cw.dump_json(path, rec)
            self.assertIn("identical to the passage", " ".join(r["detail"] for r in check(run_dir)["reasons"]))

    def test_predraft_must_precede_drafting(self) -> None:
        run_dir = build_run(self.tmp, render=False)
        run = cw.load_json(run_dir / "run.json")
        payload = cw.load_json(FIXTURE / "reviews" / "legal-predraft-r0.json")
        _rec, errors = record_review.build_record(run_dir, run, payload, runtime="claude", agent="legal-reviewer", stage="predraft", round_=0, agent_file="pilot/content-workflow/adapters/claude/agents/legal-reviewer.md", repo_root=REPO_ROOT)
        self.assertTrue(any("precede drafting" in e for e in errors), errors)
        path = run_dir / "reviews" / "legal-predraft-r0.json"
        rec = cw.load_json(path)
        rec["subject"]["draft_sha256"] = "a" * 64
        cw.dump_json(path, rec)
        self.assertIn("LEGAL_PREDRAFT_LATE", codes(check(run_dir)))

    def test_supplementary_predraft_record_does_not_outrank_the_checkpoint(self) -> None:
        """A second pre-draft record (round 1, no findings) must not make the checkpoint's closures look dropped."""
        run_dir = build_run(self.tmp)
        self.assertEqual(check(run_dir)["status"], "READY")
        base = cw.load_json(run_dir / "reviews" / "legal-predraft-r0.json")
        supplementary = copy.deepcopy(base)
        supplementary["round"] = 1
        supplementary["findings"] = []
        supplementary["verification_log"] = [supplementary["verification_log"][0]]
        supplementary["recorded_at"] = "2099-01-01T00:00:00+00:00"
        cw.dump_json(run_dir / "reviews" / "legal-predraft-r1.json", supplementary)
        report = check(run_dir)
        self.assertEqual(report["status"], "READY", report["reasons"])
        self.assertFalse(any("dropped" in r["detail"] for r in report["reasons"]), report["reasons"])
        ordered = sorted((cw.load_json(p) for p in cw.review_files(run_dir) if cw.load_json(p)["role"] == "legal-reviewer"), key=cw.record_order_key)
        self.assertEqual([(r["stage"], r["round"]) for r in ordered][:3], [("predraft", 0), ("predraft", 1), ("checkpoint", 0)])

    def test_protected_findings_need_reviewer_evidence_to_close(self) -> None:
        with self.subTest(case="legal-accuracy fixed-verified without corrected_text"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][0]["resolution"].pop("corrected_text")
            cw.dump_json(path, rec)
            report = check(run_dir)
            self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(report))
            self.assertIn("without corrected_text", " ".join(r["detail"] for r in report["reasons"]))
        with self.subTest(case="corrected_text not in the draft"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][0]["resolution"]["corrected_text"] = "A correction that was only proposed, never applied."
            cw.dump_json(path, rec)
            self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(check(run_dir)))
        with self.subTest(case="withdrawn by the coordinator instead of the reviewer"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][0]["resolution"] = {"status": "withdrawn", "verified_by": "coordinator", "note": "Coordinator considers this acceptable after discussion."}
            cw.dump_json(path, rec)
            report = check(run_dir)
            self.assertIn("may withdraw", " ".join(r["detail"] for r in report["reasons"]))
        with self.subTest(case="blocking finding accepted by coordinator"):
            run_dir = build_run(self.fresh(), render=False)
            path = run_dir / "reviews" / "legal-final-r1.json"
            rec = cw.load_json(path)
            rec["findings"][0]["resolution"] = {"status": "coordinator-accepted", "note": "Coordinator accepts the residual risk of this statement of the presumption for this fixture run."}
            cw.dump_json(path, rec)
            self.assertIn("FINDING_BLOCKING_UNRESOLVED", codes(check(run_dir)))
        with self.subTest(case="recorder refuses protected fixed-verified without corrected_text"):
            run_dir = build_run(self.fresh(), skip_final=True)
            run = cw.load_json(run_dir / "run.json")
            payload = cw.load_json(FIXTURE / "reviews" / "legal-final-r1.json")
            payload["findings"][0]["resolution"].pop("corrected_text")
            _rec, errors = record_review.build_record(run_dir, run, payload, runtime="claude", agent="legal-reviewer", stage="final", round_=1, agent_file="pilot/content-workflow/adapters/claude/agents/legal-reviewer.md", repo_root=REPO_ROOT)
            self.assertTrue(any("corrected_text" in e for e in errors), errors)

    def test_source_ceiling_is_coverage_based(self) -> None:
        def seven(run: dict) -> None:
            for n in range(4, 8):
                run["sources"].append({"id": f"S{n}", "path": "sources/legal-exampleland-rule-7.md", "sha256": "", "kind": "legal-authority", "url": f"https://courts.exampleland.example/rules/family/{n + 3}", "label": f"Exampleland Family Court Rule {n + 3}"})
                run["citations"].append({"id": n, "source_id": f"S{n}", "label": f"Exampleland Family Court Rule {n + 3}", "url": f"https://courts.exampleland.example/rules/family/{n + 3}"})
            for source in run["sources"]:
                if not source["sha256"]:
                    source["sha256"] = cw.sha256_file(FIXTURE / "sources" / "legal-exampleland-rule-7.md")
        run_dir = build_run(self.fresh(), run_transform=seven, skip_final=True)
        report = check(run_dir, "intake")
        self.assertIn("SOURCE_CEILING", codes(report))
        run = cw.load_json(run_dir / "run.json")
        run["citations_ceiling_rationale"] = "Seven distinct authorities are each tied to a separate material claim in the pre-draft ledger; none can be dropped without leaving a claim unsupported."
        cw.dump_json(run_dir / "run.json", run)
        self.assertNotIn("SOURCE_CEILING", codes(check(run_dir, "intake")))
        run["citations"] += [{"id": n, "source_id": "S3", "label": "x", "url": "https://courts.exampleland.example/rules/family/7"} for n in range(8, 14)]
        cw.dump_json(run_dir / "run.json", run)
        self.assertIn("SOURCE_CEILING", codes(check(run_dir, "intake")))

    def test_export_with_tracked_changes_or_fields_is_unclean(self) -> None:
        run_dir = build_run(self.tmp, render=False)
        tamper_docx(run_dir / "export" / EXPORT_NAME, "<w:body>", '<w:body><w:p><w:ins w:id="9" w:author="x" w:date="2026-09-23T00:00:00Z"><w:r><w:t>inserted</w:t></w:r></w:ins></w:p>')
        report = check(run_dir)
        self.assertIn("EXPORT_UNCLEAN", codes(report))

    # -- recorder ----------------------------------------------------------------------
    def test_record_review_rejects_quote_not_in_draft(self) -> None:
        run_dir = build_run(self.tmp, skip_final=True)
        run = cw.load_json(run_dir / "run.json")
        payload = cw.load_json(FIXTURE / "reviews" / "legal-final-r1.json")
        payload["findings"][0]["passage"]["quote"] = "This sentence was never in the draft at all."
        payload["findings"][0]["resolution"] = {"status": "open"}
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

    def test_record_review_cli_records_predraft_before_any_draft_exists(self) -> None:
        """The command-line recorder must complete for a predraft record, whose subject has no draft hash."""
        run_dir = self.tmp / "predraft-only"
        shutil.copytree(FIXTURE / "sources", run_dir / "sources")
        run = cw.load_json(FIXTURE / "run.template.json")
        cw.dump_json(run_dir / "run.json", run)
        payload_path = run_dir / "legal-predraft-input.json"
        cw.dump_json(payload_path, cw.load_json(FIXTURE / "reviews" / "legal-predraft-r0.json"))
        completed = subprocess.run(
            [sys.executable, str(PILOT_ROOT / "scripts" / "record_review.py"), str(run_dir), "--input", str(payload_path),
             "--runtime", "claude", "--agent", "legal-reviewer", "--stage", "predraft", "--round", "0",
             "--agent-file", "pilot/content-workflow/adapters/claude/agents/legal-reviewer.md"],
            text=True, capture_output=True, check=False, cwd=REPO_ROOT,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("no draft (predraft)", completed.stdout)
        rec = cw.load_json(run_dir / "reviews" / "legal-predraft-r0.json")
        self.assertIsNone(rec["subject"]["draft_sha256"])

    # -- delivery ----------------------------------------------------------------------
    def test_deliver_refuses_incomplete_and_copies_nothing(self) -> None:
        run_dir = build_run(self.tmp, render=False)
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

    def test_activated_codex_copies_match_adapters_when_present(self) -> None:
        for name in ("content_writer", "legal_reviewer", "editorial_reviewer"):
            active = REPO_ROOT / ".codex" / "agents" / f"{name}.toml"
            if active.exists():
                self.assertFalse(active.is_symlink(), f"{active} must be a regular file; Codex does not follow symlinked agents")
                self.assertEqual(active.read_bytes(), (PILOT_ROOT / "adapters" / "codex" / "agents" / f"{name}.toml").read_bytes(), f"{active} drifted from its adapter; re-run activate.sh after build_adapters.py")

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
