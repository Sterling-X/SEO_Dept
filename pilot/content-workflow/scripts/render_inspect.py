#!/usr/bin/env python3
"""Render the exported DOCX with the pinned renderer and record a page-by-page inspection.

Two steps, both bound to the exact export hash:

  render_inspect.py <run-dir> --round N --render
      Renders <run>/export/<file>.docx into <run>/render/r<N>/ (must be absent or empty) through the
      pinned skill's render wrapper, hashes every page image, and writes
      reviews/render-final-r<N>.json with verdict "pending" and every page uninspected.

  render_inspect.py <run-dir> --round N --attest <attestation.json>
      Merges an inspector's per-page observations into that record. The attestation is
      {"inspector": {"runtime": "claude|codex|human", "agent": "..."},
       "verdict": "pass" | "fail",
       "pages": [{"page": 1, "observation": "what was actually seen"}, ...],
       "findings": [...]}   (optional; ids R1, R2, ...; category "render")
      Every rendered page needs an observation of at least 15 characters. Page hashes are
      re-verified against the files at attestation time. The record stays a recorded judgment:
      the tooling proves the pages exist and were hashed, not that anyone looked at them.

The wrapper is taken from the pinned skill whose directory contains scripts/render-situational.sh
(override with --wrapper). It fails closed on a changed renderer, missing tooling, or a
non-empty output directory; this script does not bypass those checks.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cw_common as cw  # noqa: E402


def find_wrapper(repo_root: Path, run: dict) -> Path | None:
    for skill in run.get("skills") or []:
        candidate = (repo_root / str(skill.get("path", ""))).parent / "scripts" / "render-situational.sh"
        if candidate.is_file():
            return candidate
    return None


def render(run_dir: Path, run: dict, round_: int, wrapper: Path, dpi: int, force: bool) -> tuple[Path, dict]:
    repo_root = cw.find_repo_root()
    export_path = run_dir / run["export"]["path"]
    if not export_path.is_file():
        raise SystemExit(f"ERROR: export not found: {export_path}")
    out_dir = run_dir / "render" / f"r{round_}"
    if out_dir.exists() and any(out_dir.iterdir()):
        if not force:
            raise SystemExit(f"REFUSED: {out_dir} is not empty; use --force to render into a fresh directory")
        stamp = cw.now_iso().replace(":", "")
        out_dir.rename(out_dir.with_name(f"r{round_}.superseded.{stamp}"))
    completed = subprocess.run([str(wrapper), str(export_path), "--output_dir", str(out_dir), "--dpi", str(dpi), "--emit_pdf"], text=True, capture_output=True, check=False, cwd=repo_root)
    tail = (completed.stdout + completed.stderr)[-2000:]
    if completed.returncode != 0:
        raise SystemExit(f"ERROR: render wrapper exited {completed.returncode}\n{tail}")
    pages = sorted(out_dir.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    if not pages:
        raise SystemExit(f"ERROR: no page images were produced in {out_dir}\n{tail}")
    lock = json.loads((wrapper.parent.parent / "renderer-tools.lock.json").read_text(encoding="utf-8"))
    codex_root = Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))
    renderer_file = codex_root / lock["renderer"]["relative_path"]
    observed_renderer_sha = cw.sha256_file(renderer_file) if renderer_file.is_file() else None
    # Per-page text (from the emitted PDF) lets an attestation be checked against what is actually on the page.
    pdf = next(iter(out_dir.glob("*.pdf")), None)
    if pdf is None:
        raise SystemExit(f"ERROR: the wrapper emitted no PDF in {out_dir}; page text cannot be extracted, so observations could not be bound to pages\n{tail}")
    page_texts = extract_page_texts(repo_root, pdf)
    if len(page_texts) != len(pages) or not all(text.strip() for text in page_texts):
        raise SystemExit(f"ERROR: page text extraction produced {len(page_texts)} text(s) for {len(pages)} page image(s), or an empty page text; refusing to record an unbindable render")
    for index, page in enumerate(pages):
        text = page_texts[index] if index < len(page_texts) else ""
        (out_dir / f"page-{index + 1}.txt").write_text(text, encoding="utf-8")
    record = {
        "schema": cw.REVIEW_SCHEMA,
        "fixture": bool(run.get("fixture", False)),
        "role": "render-inspector",
        "stage": "final",
        "round": round_,
        "kind": "judgment",
        "judgment_notice": "recorded inspection; the tooling proves the pages exist and were hashed, not that they were viewed",
        "verdict": "pending",
        "subject": {"draft_sha256": cw.sha256_file(run_dir / run.get("draft", {}).get("path", "draft.md")) if (run_dir / run.get("draft", {}).get("path", "draft.md")).is_file() else None, "export_sha256": cw.sha256_file(export_path), "sources_sha256": {}},
        "reviewer": {"runtime": "script", "agent": "render_inspect.py --render", "agent_file": "pilot/content-workflow/scripts/render_inspect.py", "agent_file_sha256": cw.sha256_file(Path(__file__).resolve())},
        "recorded_at": cw.now_iso(),
        "render": {
            "wrapper": str(wrapper.relative_to(repo_root)),
            "renderer_release": lock["renderer"]["package_version"],
            "renderer_sha256": observed_renderer_sha,
            "renderer_sha256_pinned": lock["renderer"]["sha256"],
            "dpi": dpi,
            "output_dir": str(out_dir.relative_to(run_dir)),
            "page_count": len(pages),
            "pages": [{"page": index + 1, "path": str(page.relative_to(run_dir)), "sha256": cw.sha256_file(page), "text_path": str((out_dir / f"page-{index + 1}.txt").relative_to(run_dir)), "text_sha256": cw.sha256_file(out_dir / f"page-{index + 1}.txt"), "inspected": False, "observation": None} for index, page in enumerate(pages)],
            "pdf": next((str(p.relative_to(run_dir)) for p in out_dir.glob("*.pdf")), None),
        },
        "findings": [],
        "checks_not_performed": ["visual inspection pending"],
    }
    return out_dir, record


def extract_page_texts(repo_root: Path, pdf: Path) -> list[str]:
    """Extract per-page text with the Core skill's isolated PyMuPDF interpreter (the renderer's own tooling)."""
    python_bin = repo_root / ".agents" / "skills" / "family-law-service-pages" / ".venv" / "bin" / "python"
    script = "import fitz,json,sys\nd=fitz.open(sys.argv[1])\nprint(json.dumps([p.get_text() for p in d]))"
    completed = subprocess.run([str(python_bin), "-c", script, str(pdf)], text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"ERROR: could not extract page text from {pdf}: {completed.stderr[-500:]}")
    return json.loads(completed.stdout)



def attest(run_dir: Path, record_path: Path, attestation: dict) -> dict:
    record = cw.load_json(record_path)
    inspector = attestation.get("inspector") or {}
    if inspector.get("runtime") not in ("claude", "codex", "human") or not inspector.get("agent"):
        raise SystemExit("ERROR: attestation.inspector needs runtime (claude|codex|human) and agent")
    observations = {int(item.get("page", 0)): cw.norm_ws(str(item.get("observation") or "")) for item in attestation.get("pages") or [] if isinstance(item, dict)}
    problems: list[str] = []
    for page in record["render"]["pages"]:
        image = run_dir / page["path"]
        if not image.is_file():
            problems.append(f"page {page['page']} image missing: {page['path']}")
            continue
        if cw.sha256_file(image) != page["sha256"]:
            problems.append(f"page {page['page']} image changed since rendering")
        observation = observations.get(page["page"], "")
        text_path = run_dir / str(page.get("text_path") or "")
        page_text = text_path.read_text(encoding="utf-8") if text_path.is_file() else ""
        if len(observation) < 15:
            problems.append(f"page {page['page']} has no observation of at least 15 characters")
        elif not text_path.is_file() or cw.sha256_file(text_path) != page.get("text_sha256"):
            problems.append(f"page {page['page']} text file missing or changed since rendering")
        elif not cw.observation_matches_page(observation, page_text):
            problems.append(f"page {page['page']} observation does not quote three consecutive words that appear on that page")
        else:
            page["inspected"] = True
            page["observation"] = observation
    extra = set(observations) - {p["page"] for p in record["render"]["pages"]}
    if extra:
        problems.append(f"attestation names pages that were not rendered: {sorted(extra)}")
    verdict = attestation.get("verdict")
    if verdict not in ("pass", "fail"):
        problems.append("attestation.verdict must be pass or fail")
    findings = attestation.get("findings") or []
    for finding in findings:
        finding.setdefault("category", "render")
    record["findings"] = findings
    record["verdict"] = verdict
    record["reviewer"] = {"runtime": inspector["runtime"], "agent": inspector["agent"], "agent_file": inspector.get("agent_file"), "agent_file_sha256": None}
    record["checks_not_performed"] = attestation.get("checks_not_performed") or []
    record["recorded_at"] = cw.now_iso()
    record["render"]["inspection_method"] = attestation.get("method") or "each page image opened and viewed at rendered resolution"
    if verdict == "pass" and cw.unresolved_render_findings(findings):
        problems.append("verdict pass with a blocking or major render finding that is not fixed-verified or withdrawn; a re-export needs a fresh render and inspection")
    if problems:
        raise SystemExit("REFUSED: " + "; ".join(problems))
    problems = cw.validate_review_record(record)
    if problems:
        raise SystemExit("REFUSED: " + "; ".join(problems))
    cw.dump_json(record_path, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--round", type=int, default=0, dest="round_")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--attest", type=Path)
    parser.add_argument("--wrapper", type=Path)
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    run = cw.load_json(run_dir / "run.json")
    record_path = run_dir / "reviews" / f"render-final-r{args.round_}.json"
    if args.render:
        wrapper = args.wrapper.resolve() if args.wrapper else find_wrapper(cw.find_repo_root(), run)
        if wrapper is None:
            print("ERROR: no pinned skill provides scripts/render-situational.sh; pass --wrapper")
            return 2
        if record_path.exists() and not args.force:
            print(f"REFUSED: {record_path} exists; use --force")
            return 1
        out_dir, record = render(run_dir, run, args.round_, wrapper, args.dpi, args.force)
        cw.dump_json(record_path, record)
        print(f"rendered {record['render']['page_count']} page(s) to {out_dir.relative_to(run_dir)} with renderer {record['render']['renderer_release']}; record {record_path.relative_to(run_dir)} verdict=pending")
        for page in record["render"]["pages"]:
            print(f"  page {page['page']}: {page['path']} sha256 {page['sha256'][:12]}… (inspect this image)")
        return 0
    if args.attest:
        if not record_path.is_file():
            print(f"ERROR: {record_path} does not exist; run --render first")
            return 2
        record = attest(run_dir, record_path, cw.load_json(args.attest))
        print(f"attested {record['render']['page_count']} page(s) by {record['reviewer']['runtime']}/{record['reviewer']['agent']}: verdict={record['verdict']} -> {record_path.relative_to(run_dir)}")
        return 0
    parser.error("choose --render or --attest")
    return 2


if __name__ == "__main__":
    sys.exit(main())
