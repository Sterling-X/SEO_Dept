#!/usr/bin/env python3
"""Shared helpers for the content-workflow pilot scripts.

Everything here is deterministic and mechanical: hashing, Markdown and DOCX text
extraction, citation pairing, placeholder scanning, run/review record loading.
Nothing here judges legal accuracy, editorial quality, or brand fidelity.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import subprocess
import unicodedata
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"w": W_NS, "r": R_NS, "pr": PKG_REL_NS}

PILOT_ROOT = Path(__file__).resolve().parents[1]
RUN_SCHEMA = "content-workflow-run/v1"
REVIEW_SCHEMA = "content-workflow-review/v1"
READINESS_SCHEMA = "content-workflow-readiness/v1"
JUDGMENT_NOTICE = "recorded judgment; not mechanically verified"
ROLE_SHORT = {"legal-reviewer": "legal", "editorial-reviewer": "editorial", "mechanical-qa": "mechanical", "render-inspector": "render"}
SHORT_ROLE = {v: k for k, v in ROLE_SHORT.items()}
STAGES = ("predraft", "checkpoint", "final")
REQUIRED_REVIEW_KINDS = {"legal-predraft", "legal-checkpoint", "editorial-checkpoint", "legal-final", "editorial-final", "mechanical-final", "render-final"}
FAMILY_LAW_KINDS = ("situational", "core-hub", "procedural")
SEVERITIES = ("blocking", "major", "minor", "note")
RESOLUTIONS = ("open", "fixed-verified", "fixed-unverified", "disputed", "withdrawn", "coordinator-accepted")
FINDING_ID_RE = re.compile(r"^[LEMR][0-9]{1,3}$")
FINDING_CATEGORIES = ("legal-accuracy", "citation", "client-fact", "promise", "brand", "structure", "brief", "mechanical", "render", "other")
# Findings in these categories are never closed by a coordinator note; only the raising reviewer's recheck
# (fixed-verified with corrected text present in the draft) or the reviewer's own withdrawal closes them.
PROTECTED_CATEGORIES = ("legal-accuracy", "citation", "client-fact", "promise")
SOURCE_GUIDELINE = 6
SOURCE_SANITY_LIMIT = 12
VERDICTS = ("ready", "ready-with-revisions", "not-ready", "pass", "fail", "pending")


def q(ns: str, name: str) -> str:
    return f"{{{ns}}}{name}"


def find_repo_root(start: Path | None = None) -> Path:
    here = (start or PILOT_ROOT).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "AGENTS.md").is_file() and (candidate / ".agents").is_dir():
            return candidate
    raise RuntimeError("Repository root not found (expected AGENTS.md and .agents/).")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def norm_ws(text: str) -> str:
    return nfc(re.sub(r"\s+", " ", text or "")).strip()


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


# ---------------------------------------------------------------- text models

WORD_RE = re.compile(r"\w+(?:['’]\w+)*", re.UNICODE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
SOURCES_HEADING_RE = re.compile(r"^#{1,6}\s+Sources\s*$", re.IGNORECASE)
SOURCE_ROW_RE = re.compile(r"^(?:[-*]\s+)?\[(\d+)\]\s*(.*?)\s*\|\s*<?(\S+?)>?\s*$")
# [[n]](url) hyperlinked marker, or a plain [n] marker that is not itself a Markdown link label.
CITATION_TOKEN_RE = re.compile(r"\[\[(\d+)\]\]\(([^)\s]+)\)|\[(\d+)\](?!\()")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MARKER_RE = re.compile(r"\[(\d+)\]")
MD_EMPHASIS_RE = re.compile(r"(\*\*|__|`)")
MD_LIST_PREFIX_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")

PLACEHOLDER_SPEC_PATH = PILOT_ROOT / "canonical" / "placeholder-patterns.json"


def load_placeholder_patterns() -> list[tuple[str, re.Pattern[str]]]:
    spec = json.loads(PLACEHOLDER_SPEC_PATH.read_text(encoding="utf-8"))
    return [
        (item["kind"], re.compile(item["regex"], re.IGNORECASE if item.get("ignore_case") else 0))
        for item in spec["patterns"]
    ]


PLACEHOLDER_PATTERNS: list[tuple[str, re.Pattern[str]]] = load_placeholder_patterns()
MAX_WORD_COUNT_TOLERANCE = 0.02


def required_review_floor(run: dict) -> tuple[str, ...]:
    """Reviews every run must carry. Family-law page kinds add the pre-draft legal verification and both
    drafting checkpoints; a DOCX export adds the rendered-page inspection."""
    floor = ["legal-final", "editorial-final", "mechanical-final"]
    kind = (run.get("page_type") or {}).get("kind")
    if kind in FAMILY_LAW_KINDS:
        floor = ["legal-predraft", "legal-checkpoint", "editorial-checkpoint"] + floor
    export_path = str((run.get("export") or {}).get("path") or "")
    if export_path.lower().endswith(".docx"):
        floor.append("render-final")
    return tuple(floor)


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text or ""))


def strip_markdown_inline(text: str) -> str:
    text = MD_LIST_PREFIX_RE.sub("", text)
    text = MD_EMPHASIS_RE.sub("", text)
    return text


@dataclass
class TextModel:
    kind: str
    headings: list[tuple[int, str]] = field(default_factory=list)
    body_text: str = ""
    body_markers: list[tuple[int, str | None]] = field(default_factory=list)
    sources: list[tuple[int, str, str]] = field(default_factory=list)
    word_count: int = 0
    has_sources_heading: bool = False
    body_paragraphs: list[str] = field(default_factory=list)
    unclean: list[str] = field(default_factory=list)


def parse_markdown_draft(raw: str) -> TextModel:
    model = TextModel(kind="markdown")
    lines = raw.splitlines()
    sources_index = next((i for i, line in enumerate(lines) if SOURCES_HEADING_RE.match(line)), None)
    body_lines = lines if sources_index is None else lines[:sources_index]
    source_lines = [] if sources_index is None else lines[sources_index + 1:]
    h1_index = next((i for i, line in enumerate(body_lines) if HEADING_RE.match(line) and len(HEADING_RE.match(line).group(1)) == 1), None)
    if h1_index is not None:
        body_lines = body_lines[h1_index:]  # anything before the H1 (a publisher block) is not consumer copy
    body_plain: list[str] = []
    paragraph_buffer: list[str] = []

    def flush() -> None:
        if paragraph_buffer:
            model.body_paragraphs.append(norm_ws(" ".join(paragraph_buffer)))
            paragraph_buffer.clear()

    for line in body_lines:
        if not line.strip():
            flush()
            continue
        heading = HEADING_RE.match(line)
        if heading:
            flush()
            text = norm_ws(strip_markdown_inline(MD_LINK_RE.sub(lambda m: m.group(1), heading.group(2))))
            model.headings.append((len(heading.group(1)), text))
            body_plain.append(text)
            model.body_paragraphs.append(text)
            continue

        def _token(match: re.Match[str]) -> str:
            if match.group(1):
                model.body_markers.append((int(match.group(1)), match.group(2)))
                return f"[{match.group(1)}]"
            model.body_markers.append((int(match.group(3)), None))
            return f"[{match.group(3)}]"

        plain = CITATION_TOKEN_RE.sub(_token, line)
        plain = MD_LINK_RE.sub(lambda m: m.group(1), plain)
        plain = strip_markdown_inline(plain)
        body_plain.append(plain)
        if MD_LIST_PREFIX_RE.match(line):
            flush()
            model.body_paragraphs.append(norm_ws(plain))
        else:
            paragraph_buffer.append(plain)
    flush()
    if sources_index is not None:
        model.has_sources_heading = True
        model.headings.append((len(HEADING_RE.match(lines[sources_index]).group(1)), "Sources"))
    for line in source_lines:
        row = SOURCE_ROW_RE.match(MD_LINK_RE.sub(lambda m: m.group(2) if m.group(1).strip() == m.group(2).strip() else m.group(1), line.strip()))
        if row:
            model.sources.append((int(row.group(1)), norm_ws(row.group(2)), row.group(3).strip()))
    model.body_text = nfc("\n".join(body_plain))
    model.word_count = count_words(model.body_text)
    return model


HEADING_STYLE_RE = re.compile(r"^(?:Heading|heading|Titre|Überschrift)\s*([1-6])$")


def parse_docx(path: Path) -> TextModel:
    model = TextModel(kind="docx")
    unclean_tags = {"ins": "tracked insertion", "del": "tracked deletion", "delText": "deleted text", "moveFrom": "tracked move", "moveTo": "tracked move", "rPrChange": "tracked formatting change", "pPrChange": "tracked formatting change", "fldSimple": "field code", "fldChar": "field code", "instrText": "field instruction", "vanish": "hidden text", "altChunk": "embedded alternate content", "commentRangeStart": "comment", "commentReference": "comment reference", "object": "embedded object"}
    seen_unclean: dict[str, int] = {}
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        for member in archive.namelist():
            if member.startswith("word/") and member.endswith(".xml") and "/_rels/" not in member and member not in ("word/styles.xml", "word/numbering.xml", "word/settings.xml", "word/fontTable.xml", "word/webSettings.xml", "word/theme/theme1.xml"):
                try:
                    part = ET.fromstring(archive.read(member))
                except ET.ParseError:
                    continue
                is_header_footer = member.startswith(("word/header", "word/footer"))
                for node in part.iter():
                    local_name = node.tag.split("}")[-1]
                    if local_name in unclean_tags:
                        if is_header_footer and local_name in ("fldSimple", "fldChar", "instrText"):
                            continue  # page-number fields in running headers and footers are legitimate
                        label = unclean_tags[local_name] + (f" in {member}" if member != "word/document.xml" else "")
                        seen_unclean[label] = seen_unclean.get(label, 0) + 1
        rel_map: dict[str, str] = {}
        if "word/_rels/document.xml.rels" in archive.namelist():
            rels = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
            for rel in rels.findall("pr:Relationship", NS):
                if (rel.get("Type") or "").endswith("/hyperlink"):
                    rel_map[rel.get("Id") or ""] = rel.get("Target") or ""
    model.unclean = [f"{label} x{count}" for label, count in sorted(seen_unclean.items())]
    paragraphs: list[tuple[int | None, str, list[tuple[str, str | None]]]] = []
    body = document.find("w:body", NS)
    for paragraph in (body.iter(q(W_NS, "p")) if body is not None else document.iter(q(W_NS, "p"))):
        style_node = paragraph.find("w:pPr/w:pStyle", NS)
        style = style_node.get(q(W_NS, "val")) if style_node is not None else ""
        level_match = HEADING_STYLE_RE.match(style or "")
        level = int(level_match.group(1)) if level_match else None
        text = "".join(node.text or "" for node in paragraph.iter(q(W_NS, "t")))
        links: list[tuple[str, str | None]] = []
        for hyperlink in paragraph.iter(q(W_NS, "hyperlink")):
            anchor = "".join(node.text or "" for node in hyperlink.iter(q(W_NS, "t")))
            links.append((anchor, rel_map.get(hyperlink.get(q(R_NS, "id")) or "")))
        paragraphs.append((level, text, links))

    sources_index = next(
        (i for i, (level, text, _links) in enumerate(paragraphs) if norm_ws(text).lower() == "sources" and level is not None),
        None,
    )
    if sources_index is None:
        sources_index = next((i for i, (_l, text, _k) in enumerate(paragraphs) if norm_ws(text).lower() == "sources"), None)
    body_paragraphs = paragraphs if sources_index is None else paragraphs[:sources_index]
    source_paragraphs = [] if sources_index is None else paragraphs[sources_index + 1:]
    h1_position = next((i for i, (level, text, _links) in enumerate(body_paragraphs) if level == 1 and norm_ws(text)), None)
    if h1_position is not None:
        body_paragraphs = body_paragraphs[h1_position:]  # a generator publisher block before the H1 is not consumer copy
    body_plain: list[str] = []
    for level, text, links in body_paragraphs:
        if norm_ws(text):
            model.body_paragraphs.append(norm_ws(text))
        if level is not None and norm_ws(text):
            model.headings.append((level, norm_ws(text)))
        available = list(links)
        for match in MARKER_RE.finditer(text):
            marker = match.group(0)
            url = None
            for index, (anchor, target) in enumerate(available):
                if anchor.strip() == marker:
                    url = target
                    available.pop(index)
                    break
            model.body_markers.append((int(match.group(1)), url))
        body_plain.append(text)
    if sources_index is not None:
        model.has_sources_heading = True
        level = paragraphs[sources_index][0]
        model.headings.append((level if level is not None else 2, "Sources"))
    for _level, text, links in source_paragraphs:
        row = SOURCE_ROW_RE.match(norm_ws(text))
        if not row:
            continue
        url = row.group(3)
        for _anchor, target in links:
            if target:
                url = target
                break
        model.sources.append((int(row.group(1)), norm_ws(row.group(2)), url))
    model.body_text = nfc("\n".join(body_plain))
    model.word_count = count_words(model.body_text)
    return model


# ------------------------------------------------------------ mechanical checks

@dataclass
class CheckResult:
    name: str
    status: str  # pass | fail | skipped
    detail: str = ""

    def as_dict(self) -> dict:
        return {"check": self.name, "status": self.status, "detail": self.detail}


def scan_placeholders(text: str) -> list[dict]:
    hits: list[dict] = []
    for kind, pattern in PLACEHOLDER_PATTERNS:
        for match in pattern.finditer(text or ""):
            start = max(0, match.start() - 30)
            hits.append({"kind": kind, "match": match.group(0), "context": norm_ws(text[start:match.end() + 30])})
    return hits


def citation_issues(model: TextModel, expected: list[dict], label: str) -> list[str]:
    issues: list[str] = []
    expected_ids = [int(item["id"]) for item in expected]
    if expected_ids != list(range(1, len(expected_ids) + 1)):
        issues.append(f"run.json citations are not numbered 1..n: {expected_ids}")
    by_id = {int(item["id"]): item for item in expected}
    marker_ids = [marker_id for marker_id, _url in model.body_markers]
    first_seen: list[int] = []
    for marker_id in marker_ids:
        if marker_id not in first_seen:
            first_seen.append(marker_id)
    if first_seen != expected_ids:
        issues.append(f"{label}: body citation markers (first appearance) {first_seen} do not equal expected {expected_ids}")
    for marker_id in set(marker_ids):
        if marker_id not in by_id:
            issues.append(f"{label}: marker [{marker_id}] has no matching citation in run.json")
    for expected_id in expected_ids:
        if expected_id not in marker_ids:
            issues.append(f"{label}: source [{expected_id}] is never cited in the body")
    if model.kind == "docx":
        for marker_id, url in model.body_markers:
            expected_url = by_id.get(marker_id, {}).get("url")
            if url is None:
                issues.append(f"{label}: marker [{marker_id}] is not a hyperlink in the export")
            elif expected_url and url != expected_url:
                issues.append(f"{label}: marker [{marker_id}] links to {url}, expected {expected_url}")
    else:
        for marker_id, url in model.body_markers:
            expected_url = by_id.get(marker_id, {}).get("url")
            if url is None:
                issues.append(f"{label}: marker [{marker_id}] is plain text; the draft must use the hyperlinked form [[{marker_id}]](url)")
            elif expected_url and url != expected_url:
                issues.append(f"{label}: marker [{marker_id}] links to {url}, expected {expected_url}")
    if not model.has_sources_heading:
        issues.append(f"{label}: no Sources heading found")
    source_ids = [source_id for source_id, _label, _url in model.sources]
    if source_ids != expected_ids:
        issues.append(f"{label}: Sources entries {source_ids} do not equal expected {expected_ids}")
    for source_id, source_label, url in model.sources:
        want = by_id.get(source_id)
        if not want:
            continue
        if norm_ws(source_label).casefold() != norm_ws(want.get("label", "")).casefold():
            issues.append(f"{label}: Sources [{source_id}] label {source_label!r} does not match expected {want.get('label')!r}")
        if url != want.get("url"):
            issues.append(f"{label}: Sources [{source_id}] URL {url} does not match expected {want.get('url')}")
    return issues


def run_validators(repo_root: Path, run_dir: Path, validators: list[dict]) -> list[dict]:
    results: list[dict] = []
    for validator in validators or []:
        command = [str(part).replace("{run_dir}", str(run_dir)).replace("{repo_root}", str(repo_root)) for part in validator.get("command", [])]
        if not command:
            results.append({"name": validator.get("name", "?"), "command": [], "exit_code": None, "output_tail": "empty command"})
            continue
        try:
            completed = subprocess.run(command, cwd=repo_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False, timeout=600)
            exit_code, output = completed.returncode, completed.stdout
        except (OSError, subprocess.TimeoutExpired) as error:
            exit_code, output = None, f"{type(error).__name__}: {error}"
        results.append({"name": validator.get("name", "?"), "command": command, "exit_code": exit_code, "output_tail": (output or "")[-1500:]})
    return results


def mechanical_checks(repo_root: Path, run_dir: Path, run: dict, *, run_declared_validators: bool = True) -> tuple[list[CheckResult], list[dict]]:
    """Deterministic checks on draft and export. Returns (checks, validator_results)."""
    checks: list[CheckResult] = []
    validators: list[dict] = []
    draft_path = run_dir / run.get("draft", {}).get("path", "draft.md")
    export_path = run_dir / run.get("export", {}).get("path", "")
    citations = run.get("citations", [])
    client_name = norm_ws(run.get("client", {}).get("name", ""))
    forbidden = [norm_ws(term).casefold() for term in run.get("forbidden_terms", []) if norm_ws(term)]
    parity = run.get("parity", {}) or {}
    tolerance = min(float(parity.get("word_count_tolerance", MAX_WORD_COUNT_TOLERANCE)), MAX_WORD_COUNT_TOLERANCE)
    compare_headings = bool(parity.get("compare_headings", True))

    draft_model = export_model = None
    if draft_path.is_file():
        checks.append(CheckResult("draft-present", "pass", str(draft_path.relative_to(run_dir))))
        draft_model = parse_markdown_draft(draft_path.read_text(encoding="utf-8"))
    else:
        checks.append(CheckResult("draft-present", "fail", f"missing {draft_path}"))
    if run.get("export", {}).get("path") and export_path.is_file():
        checks.append(CheckResult("export-present", "pass", str(export_path.relative_to(run_dir))))
        try:
            export_model = parse_docx(export_path)
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as error:
            checks.append(CheckResult("export-readable", "fail", f"{type(error).__name__}: {error}"))
    else:
        checks.append(CheckResult("export-present", "fail", f"missing {export_path}"))

    if export_model is not None:
        checks.append(CheckResult("export-clean", "fail" if export_model.unclean else "pass", "; ".join(export_model.unclean) if export_model.unclean else "no fields, revisions, comments, hidden text, or embedded content"))
    for label, model in (("draft", draft_model), ("export", export_model)):
        if model is None:
            continue
        issues = citation_issues(model, citations, label)
        checks.append(CheckResult(f"citations-{label}", "fail" if issues else "pass", "; ".join(issues) if issues else f"{len(citations)} citation(s) paired with Sources"))
        hits = scan_placeholders(model.body_text + "\n" + "\n".join(f"[{i}] {l} | {u}" for i, l, u in model.sources))
        checks.append(CheckResult(f"placeholders-{label}", "fail" if hits else "pass", "; ".join(f"{h['kind']}: {h['match']}" for h in hits[:10]) if hits else "none"))
        if client_name:
            present = client_name.casefold() in norm_ws(model.body_text).casefold()
            checks.append(CheckResult(f"client-name-{label}", "pass" if present else "fail", f"{client_name!r} {'found' if present else 'not found'}"))
        if forbidden:
            haystack = norm_ws(model.body_text).casefold()
            found = [term for term in forbidden if term in haystack]
            checks.append(CheckResult(f"forbidden-terms-{label}", "fail" if found else "pass", ", ".join(found) if found else "none"))

    if draft_model is not None and export_model is not None:
        if compare_headings:
            same = [h for h in draft_model.headings] == [h for h in export_model.headings]
            checks.append(CheckResult("parity-headings", "pass" if same else "fail", "heading sequences equal" if same else f"draft={draft_model.headings} export={export_model.headings}"))
        else:
            checks.append(CheckResult("parity-headings", "skipped", "run.json parity.compare_headings=false"))
        base = max(draft_model.word_count, 1)
        delta = abs(draft_model.word_count - export_model.word_count) / base
        checks.append(CheckResult("parity-word-count", "pass" if delta <= tolerance else "fail", f"draft={draft_model.word_count} export={export_model.word_count} delta={delta:.3%} tolerance={tolerance:.1%}"))
        draft_paragraphs = [strip_markdown_inline(p) for p in draft_model.body_paragraphs]
        draft_paragraphs = [norm_ws(p) for p in draft_paragraphs if norm_ws(p)]
        export_paragraphs = [p for p in export_model.body_paragraphs if p]
        if draft_paragraphs == export_paragraphs:
            checks.append(CheckResult("parity-paragraphs", "pass", f"{len(draft_paragraphs)} consumer-copy paragraphs identical after normalization"))
        else:
            first = next((i for i, (a, b) in enumerate(zip(draft_paragraphs, export_paragraphs)) if a != b), min(len(draft_paragraphs), len(export_paragraphs)))
            a = draft_paragraphs[first] if first < len(draft_paragraphs) else "(missing)"
            b = export_paragraphs[first] if first < len(export_paragraphs) else "(missing)"
            checks.append(CheckResult("parity-paragraphs", "fail", f"draft has {len(draft_paragraphs)} paragraphs, export {len(export_paragraphs)}; first divergence at #{first + 1}: draft={a[:80]!r} export={b[:80]!r}"))

    declared = run.get("export", {}).get("validators", []) or []
    if declared and not run_declared_validators:
        checks.append(CheckResult("validators-declared", "fail", f"{len(declared)} validator(s) declared in run.json but not executed in this check"))
    elif declared:
        validators = run_validators(repo_root, run_dir, declared)
        for result in validators:
            ok = result["exit_code"] == 0
            checks.append(CheckResult(f"validator-{result['name']}", "pass" if ok else "fail", f"exit={result['exit_code']}"))
    return checks, validators


# ------------------------------------------------------------- record loading


_WORD_RE = re.compile(r"[^\W_]+(?:[-'’][^\W_]+)*", re.UNICODE)


def _content_words(text: str) -> list[str]:
    """Casefolded word tokens with surrounding punctuation removed (quotes, commas, brackets, section signs)."""
    return _WORD_RE.findall(norm_ws(text).casefold())


def observation_matches_page(observation: str, page_text: str) -> bool:
    """True when the observation quotes at least three consecutive words that appear on the page text.

    Punctuation attached to a word (an opening quote, a trailing comma) does not break the match;
    the words themselves must appear in the same order on the page.
    """
    words = _content_words(observation)
    haystack = " " + " ".join(_content_words(page_text)) + " "
    return any(" " + " ".join(words[i:i + 3]) + " " in haystack for i in range(len(words) - 2))


def unresolved_render_findings(findings: list) -> list[str]:
    """Ids of blocking/major render findings that are neither fixed-verified nor withdrawn."""
    return [str(f.get("id")) for f in findings or [] if isinstance(f, dict) and f.get("severity") in ("blocking", "major")
            and (f.get("resolution") or {}).get("status", "open") not in ("fixed-verified", "withdrawn")]


def review_files(run_dir: Path) -> list[Path]:
    """Review records only; the coordinator-dispositions file lives beside them but is not a record."""
    reviews = run_dir / "reviews"
    return sorted(p for p in reviews.glob("*.json") if p.name != "coordinator-dispositions.json") if reviews.is_dir() else []


def validate_review_record(record: dict) -> list[str]:
    problems: list[str] = []
    if record.get("schema") != REVIEW_SCHEMA:
        problems.append(f"schema must be {REVIEW_SCHEMA}")
    if record.get("role") not in ROLE_SHORT:
        problems.append("role must be legal-reviewer, editorial-reviewer, or mechanical-qa")
    if record.get("stage") not in STAGES:
        problems.append("stage must be predraft, checkpoint, or final")
    if record.get("stage") == "predraft" and record.get("role") != "legal-reviewer":
        problems.append("only the legal reviewer records a predraft review")
    if not isinstance(record.get("round"), int) or record.get("round") < 0:
        problems.append("round must be a non-negative integer")
    if record.get("verdict") not in VERDICTS:
        problems.append(f"verdict must be one of {VERDICTS}")
    subject = record.get("subject")
    if not isinstance(subject, dict):
        problems.append("subject is required")
    elif record.get("stage") != "predraft" and not subject.get("draft_sha256"):
        problems.append("subject.draft_sha256 is required")
    elif record.get("stage") == "predraft" and not isinstance(subject.get("sources_sha256"), dict):
        problems.append("a predraft record must carry subject.sources_sha256")
    if record.get("role") == "render-inspector":
        render = record.get("render")
        if not isinstance(render, dict) or not isinstance(render.get("pages"), list) or not render.get("pages"):
            problems.append("render-inspector records must carry render.pages")
        elif not (subject or {}).get("export_sha256"):
            problems.append("render-inspector records must carry subject.export_sha256")
    reviewer = record.get("reviewer")
    if not isinstance(reviewer, dict) or reviewer.get("runtime") not in ("claude", "codex", "script", "human") or not reviewer.get("agent"):
        problems.append("reviewer.runtime and reviewer.agent are required")
    if not record.get("recorded_at"):
        problems.append("recorded_at is required")
    findings = record.get("findings")
    if not isinstance(findings, list):
        problems.append("findings must be a list")
        findings = []
    seen: set[str] = set()
    for index, finding in enumerate(findings):
        prefix = f"findings[{index}]"
        if not isinstance(finding, dict):
            problems.append(f"{prefix} must be an object")
            continue
        fid = str(finding.get("id", ""))
        if not FINDING_ID_RE.match(fid):
            problems.append(f"{prefix}.id {fid!r} must match [LEMR]<n>")
        if fid in seen:
            problems.append(f"{prefix}.id {fid!r} duplicated within the record")
        seen.add(fid)
        if finding.get("severity") not in SEVERITIES:
            problems.append(f"{prefix}.severity must be one of {SEVERITIES}")
        if finding.get("category") not in FINDING_CATEGORIES:
            problems.append(f"{prefix}.category must be one of {FINDING_CATEGORIES}")
        passage = finding.get("passage")
        if not isinstance(passage, dict) or len(norm_ws(passage.get("quote", ""))) < 8 or not passage.get("location"):
            problems.append(f"{prefix}.passage needs location and a quote of at least 8 characters")
        if len(norm_ws(finding.get("issue", ""))) < 8:
            problems.append(f"{prefix}.issue is required")
        if not isinstance(finding.get("evidence"), dict):
            problems.append(f"{prefix}.evidence must be an object")
        if "requested_correction" not in finding:
            problems.append(f"{prefix}.requested_correction is required")
        resolution = finding.get("resolution")
        if not isinstance(resolution, dict) or resolution.get("status") not in RESOLUTIONS:
            problems.append(f"{prefix}.resolution.status must be one of {RESOLUTIONS}")
    if record.get("role") == "mechanical-qa" and not isinstance(record.get("checks"), list):
        problems.append("mechanical-qa records must carry a checks list")
    return problems


def record_kind(record: dict) -> str:
    return f"{ROLE_SHORT.get(record.get('role'), '?')}-{record.get('stage')}"


def record_order_key(record: dict) -> tuple:
    """Workflow order of review records.

    Pre-draft records have no draft to bind to, so every one of them (whatever its round number;
    a supplementary pre-draft record is recorded as a later round) precedes every record that
    reviews a draft. Among draft-bound records the order is round, then stage, then time.
    """
    stage_rank = {"predraft": 0, "checkpoint": 1, "final": 2}.get(record.get("stage"), 2)
    draft_bound = 0 if record.get("stage") == "predraft" else 1
    return (draft_bound, int(record.get("round", 0)), stage_rank, str(record.get("recorded_at", "")))
