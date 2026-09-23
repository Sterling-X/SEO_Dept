#!/usr/bin/env python3
"""LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL. PILOT CANDIDATE v1.

Baseline: .agents/skills/family-law-situational-pages/scripts/office/validate.py (hash in
../../pilot-manifest.json). Added: placeholder grammar scan, citation-marker set/order/count
checks, Sources-row id and label parity with the manifest.

Structural validator for the demonstrated FL-M008 Situational DOCX route.
General ZIP/XML checks reuse ordinary OOXML concepts proven by the local Core
validator; the page contract here is independently scoped to Situational copy.

Usage:
  python3 scripts/office/validate.py page.docx --manifest workflow-input.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


sys.dont_write_bytecode = True
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"w": W_NS, "r": R_NS, "pr": PKG_REL_NS}
PLACEHOLDER_PATTERNS = [
    re.compile(r"\[(?!\d+\])[^\]\n]{1,120}\]"),
    re.compile(r"\{\{[^}\n]{0,120}\}\}"),
    re.compile(r"<<[^>\n]{0,120}>>"),
    re.compile(r"\b(?:TODO|TBD|FIXME|XXX|PLACEHOLDER)\b"),
    re.compile(r"\bTK\b"),
    re.compile(r"lorem ipsum", re.IGNORECASE),
]


def find_placeholder(text: str) -> str | None:
    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(text or "")
        if match:
            return match.group(0)
    return None


def q(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def load_xml(archive: zipfile.ZipFile, member: str, errors: list[str]) -> ET.Element | None:
    try:
        return ET.fromstring(archive.read(member))
    except KeyError:
        errors.append(f"Required OOXML part is missing: {member}")
    except ET.ParseError as error:
        errors.append(f"Malformed XML in {member}: {error}")
    return None


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))


def paragraph_style(paragraph: ET.Element) -> str | None:
    style = paragraph.find("w:pPr/w:pStyle", NS)
    return style.get(q(W_NS, "val")) if style is not None else None


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*", text))


def text_from_runs(runs: list[dict] | None) -> str:
    return "".join(str(run.get("text") or "") for run in (runs or []))


def manifest_text(manifest: dict) -> str:
    parts: list[str] = []
    for block in manifest.get("content", []):
        if block.get("type") in {"h2", "h3"}:
            parts.append(str(block.get("text") or ""))
        elif block.get("type") == "p":
            parts.append(text_from_runs(block.get("runs")))
        elif block.get("type") in {"ul", "ol"}:
            parts.extend(text_from_runs(item.get("runs")) for item in block.get("items", []))
    return " ".join(parts)


def style_run_values(styles: ET.Element, style_id: str) -> tuple[str | None, str | None, str | None]:
    if style_id == "Normal":
        run_props = styles.find(".//w:docDefaults/w:rPrDefault/w:rPr", NS)
        para_props = styles.find(".//w:docDefaults/w:pPrDefault/w:pPr", NS)
    else:
        style = styles.find(f".//w:style[@w:styleId='{style_id}']", NS)
        if style is None:
            return None, None, None
        run_props = style.find("w:rPr", NS)
        para_props = style.find("w:pPr", NS)
    font = None
    size = None
    before = None
    if run_props is not None:
        fonts = run_props.find("w:rFonts", NS)
        size_node = run_props.find("w:sz", NS)
        if fonts is not None:
            font = fonts.get(q(W_NS, "ascii")) or fonts.get(q(W_NS, "hAnsi"))
        if size_node is not None:
            size = size_node.get(q(W_NS, "val"))
    if para_props is not None:
        spacing = para_props.find("w:spacing", NS)
        if spacing is not None:
            before = spacing.get(q(W_NS, "before"))
    return font, size, before


def report(document: Path, errors: list[str], warnings: list[str], facts: dict[str, object]) -> None:
    print(f"FL-M008 structural validation: {document}")
    for key, value in facts.items():
        print(f"  {key}: {value}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print("PASS: FL-M008 Situational DOCX structure is valid for the tested local contract.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the local FL-M008 Situational DOCX structure.")
    parser.add_argument("document", type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    facts: dict[str, object] = {}
    document_path = args.document.resolve()
    manifest_path = args.manifest.resolve()

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: Cannot read manifest {manifest_path}: {error}")
        return 2

    if manifest.get("schema_version") != 2 or manifest.get("workflow") != "situational-fl-m008-local-replacement":
        errors.append("Manifest is not schema_version 2 for workflow situational-fl-m008-local-replacement.")
    meta = manifest.get("meta") or {}
    synthetic = meta.get("synthetic_fixture") is True
    expected_name = (
        r"^synthetic-high-conflict-divorce-situational\.docx$"
        if synthetic
        else r"^[a-z0-9]+(?:-[a-z0-9]+)*-high-conflict-divorce-situational\.docx$"
    )
    if not re.fullmatch(expected_name, document_path.name):
        errors.append("DOCX filename does not match the scoped FL-M008 naming contract.")

    try:
        archive = zipfile.ZipFile(document_path)
    except (OSError, zipfile.BadZipFile) as error:
        print(f"ERROR: Not a readable DOCX ZIP package: {error}")
        return 2

    with archive:
        corrupt = archive.testzip()
        if corrupt:
            errors.append(f"DOCX ZIP integrity failed at member: {corrupt}")
        names = set(archive.namelist())
        required_parts = {
            "[Content_Types].xml",
            "_rels/.rels",
            "word/document.xml",
            "word/styles.xml",
            "word/numbering.xml",
            "word/_rels/document.xml.rels",
        }
        for member in sorted(required_parts - names):
            errors.append(f"Required OOXML part is missing: {member}")

        document = load_xml(archive, "word/document.xml", errors)
        styles = load_xml(archive, "word/styles.xml", errors)
        numbering = load_xml(archive, "word/numbering.xml", errors)
        rels = load_xml(archive, "word/_rels/document.xml.rels", errors)
        load_xml(archive, "[Content_Types].xml", errors)
        if document is None or styles is None or numbering is None or rels is None:
            report(document_path, errors, warnings, facts)
            return 1

        if "word/comments.xml" in names:
            comments = load_xml(archive, "word/comments.xml", errors)
            if comments is not None and comments.findall(".//w:comment", NS):
                errors.append("Comments remain in the DOCX package.")
        if document.findall(".//w:commentRangeStart", NS) or document.findall(".//w:commentRangeEnd", NS):
            errors.append("Comment markers remain in document.xml.")
        if document.findall(".//w:ins", NS) or document.findall(".//w:del", NS):
            errors.append("Tracked insertions or deletions remain in document.xml.")

        section = document.find(".//w:sectPr", NS)
        if section is None:
            errors.append("Section properties are missing.")
        else:
            page_size = section.find("w:pgSz", NS)
            margins = section.find("w:pgMar", NS)
            size = (
                page_size.get(q(W_NS, "w")) if page_size is not None else None,
                page_size.get(q(W_NS, "h")) if page_size is not None else None,
            )
            facts["page_size_dxa"] = f"{size[0]} x {size[1]}"
            if size != ("12240", "15840"):
                errors.append(f"Page size must be US Letter 12240 x 15840 DXA; found {size}.")
            if margins is None:
                errors.append("Page margins are missing.")
            else:
                actual = {side: margins.get(q(W_NS, side)) for side in ("top", "right", "bottom", "left")}
                facts["margins_dxa"] = actual
                if any(value != "1440" for value in actual.values()):
                    errors.append(f"All margins must be 1440 DXA; found {actual}.")

        expectations = {
            "Normal": ("Arial", "24", None),
            "Heading1": ("Arial", "36", "240"),
            "Heading2": ("Arial", "30", "360"),
            "Heading3": ("Arial", "26", "280"),
            "Source": ("Arial", "24", None),
        }
        for style_id, (font_expected, size_expected, before_minimum) in expectations.items():
            font, size, before = style_run_values(styles, style_id)
            if font != font_expected or size != size_expected:
                errors.append(f"{style_id} must use {font_expected} {int(size_expected) / 2:g} pt; found font={font}, size={size}.")
            if before_minimum is not None and (before is None or int(before) < int(before_minimum)):
                errors.append(f"{style_id} spacing-before must be at least {before_minimum} DXA; found {before}.")

        paragraphs = document.findall(".//w:body/w:p", NS)
        nonempty = [
            (index, paragraph, paragraph_text(paragraph).strip(), paragraph_style(paragraph))
            for index, paragraph in enumerate(paragraphs)
            if paragraph_text(paragraph).strip()
        ]
        heading_levels = {"Heading1": 1, "Heading2": 2, "Heading3": 3}
        headings = [(index, heading_levels[style], text) for index, _p, text, style in nonempty if style in heading_levels]
        h1s = [(index, text) for index, level, text in headings if level == 1]
        facts["h1_count"] = len(h1s)
        if len(h1s) != 1:
            errors.append(f"Exactly one styled H1 is required; found {len(h1s)}.")
        elif h1s[0][1] != meta.get("h1"):
            errors.append("Styled H1 does not match manifest meta.h1.")

        previous_level = 0
        for _index, level, text in headings:
            if previous_level and level > previous_level + 1:
                errors.append(f"Heading hierarchy skips from H{previous_level} to H{level} before {text!r}.")
            previous_level = level

        if h1s:
            h1_index = h1s[0][0]
            after_h1 = [item for item in nonempty if item[0] > h1_index]
            opening = after_h1[:2]
            if len(opening) != 2 or any(item[3] in heading_levels for item in opening):
                errors.append("H1 must be followed immediately by two non-heading opening paragraphs.")
            if any(item[1].find("w:pPr/w:numPr", NS) is not None for item in opening):
                errors.append("The two opening paragraphs must not be lists.")

        expected_h2 = [block.get("text") for block in manifest.get("content", []) if block.get("type") == "h2"] + ["Sources"]
        actual_h2 = [text for _index, level, text in headings if level == 2]
        facts["h2_count"] = len(actual_h2)
        if actual_h2 != expected_h2:
            errors.append(f"H2 sequence does not match manifest plus final Sources; found {actual_h2!r}.")
        if not actual_h2 or actual_h2[-1] != "Sources":
            errors.append("Sources must be the final H2.")

        sources_heading_indexes = [index for index, level, text in headings if level == 2 and text == "Sources"]
        if sources_heading_indexes:
            sources_heading_index = sources_heading_indexes[0]
            source_rows = [item for item in nonempty if item[0] > sources_heading_index]
            expected_source_rows = len(manifest.get("sources", [])) or 1
            facts["source_rows"] = len(source_rows)
            if len(source_rows) != expected_source_rows:
                errors.append(
                    f"Expected {expected_source_rows} Source row(s) after Sources; found {len(source_rows)}."
                )
            manifest_sources = manifest.get("sources", [])
            if manifest_sources:
                for row_item, source in zip(source_rows, manifest_sources):
                    row_match = re.match(r"^\[(\d+)\]\s*(.*?)\s*\|", row_item[2])
                    if not row_match:
                        errors.append(f"Sources row does not follow the [n] label | URL format: {row_item[2][:80]!r}.")
                        continue
                    if int(row_match.group(1)) != int(source.get("id", -1)):
                        errors.append(f"Sources row id [{row_match.group(1)}] does not match manifest source id {source.get('id')}.")
                    if re.sub(r"\s+", " ", row_match.group(2)).strip() != re.sub(r"\s+", " ", str(source.get("label", ""))).strip():
                        errors.append(f"Sources row [{row_match.group(1)}] label does not match the manifest label.")
            source_style_size = style_run_values(styles, "Source")[1]
            for _index, paragraph, text, style in source_rows:
                if style != "Source":
                    errors.append(f"Source row must use the Source paragraph style: {text[:80]!r}.")
                for run in paragraph.findall(".//w:r", NS):
                    if not paragraph_text(run).strip():
                        continue
                    size_node = run.find("w:rPr/w:sz", NS)
                    effective_size = (
                        size_node.get(q(W_NS, "val")) if size_node is not None else source_style_size
                    )
                    if effective_size != "24":
                        errors.append(
                            f"Source row text must be Arial 12 pt (w:sz=24); found {effective_size} in {text[:80]!r}."
                        )

        expected_manifest_words = count_words(manifest_text(manifest))
        doc_consumer_parts: list[str] = []
        if h1s:
            h1_index = h1s[0][0]
            sources_indexes = [index for index, level, text in headings if level == 2 and text == "Sources"]
            sources_index = sources_indexes[0] if sources_indexes else len(paragraphs)
            doc_consumer_parts = [
                paragraph_text(paragraph)
                for index, paragraph in enumerate(paragraphs)
                if h1_index < index < sources_index
            ]
        actual_words = count_words(" ".join(doc_consumer_parts))
        facts["consumer_words"] = actual_words
        if actual_words != expected_manifest_words:
            errors.append(f"DOCX consumer word count {actual_words} does not match manifest count {expected_manifest_words}.")
        if not 1100 <= actual_words <= 1700:
            errors.append(f"Consumer copy must contain 1,100–1,700 words; found {actual_words}.")
        consumer_text = " ".join(doc_consumer_parts)
        marker_ids = [int(value) for value in re.findall(r"\[(\d+)\]", consumer_text)]
        expected_ids = [int(source.get("id")) for source in manifest.get("sources", []) if source.get("id") is not None]
        first_seen = list(dict.fromkeys(marker_ids))
        facts["citation_markers"] = marker_ids
        if first_seen != expected_ids:
            errors.append(f"Citation markers by first appearance {first_seen} do not match manifest source order {expected_ids}.")
        for marker_id in set(marker_ids):
            if marker_ids.count(marker_id) != 1:
                errors.append(f"Citation marker [{marker_id}] appears {marker_ids.count(marker_id)} times; each source is cited exactly once.")
        full_text = " ".join(paragraph_text(paragraph) for paragraph in paragraphs)
        placeholder = find_placeholder(full_text)
        if placeholder:
            errors.append(f"Unresolved placeholder detected: {placeholder!r}.")

        expected_list_items = sum(len(block.get("items", [])) for block in manifest.get("content", []) if block.get("type") in {"ul", "ol"})
        numbered_paragraphs = [paragraph for paragraph in paragraphs if paragraph.find("w:pPr/w:numPr", NS) is not None]
        facts["list_items"] = len(numbered_paragraphs)
        if len(numbered_paragraphs) != expected_list_items:
            errors.append(f"DOCX list item count {len(numbered_paragraphs)} does not match manifest {expected_list_items}.")
        body_text = " ".join(paragraph_text(paragraph) for paragraph in paragraphs)
        if re.search(r"[●▪◦]", body_text):
            errors.append("Unicode bullet text remains in document content.")

        rel_map: dict[str, tuple[str, str | None]] = {}
        for relationship in rels.findall("pr:Relationship", NS):
            if (relationship.get("Type") or "").endswith("/hyperlink"):
                rel_map[relationship.get("Id") or ""] = (
                    relationship.get("Target") or "",
                    relationship.get("TargetMode"),
                )
        hyperlink_nodes = document.findall(".//w:hyperlink", NS)
        external_links: list[str] = []
        for hyperlink in hyperlink_nodes:
            rid = hyperlink.get(q(R_NS, "id"))
            if not rid:
                continue
            if rid not in rel_map:
                errors.append(f"Hyperlink relationship {rid} is missing from document.xml.rels.")
                continue
            target, mode = rel_map[rid]
            if mode != "External":
                errors.append(f"Hyperlink relationship {rid} is not marked External.")
            external_links.append(target)
        expected_hyperlinks = len(manifest.get("link_manifest", [])) + 2 * len(manifest.get("sources", []))
        facts["external_hyperlinks"] = len(external_links)
        if len(external_links) != expected_hyperlinks:
            errors.append(f"Expected {expected_hyperlinks} external hyperlink occurrences; found {len(external_links)}.")

        for label in (
            "Retained implementation URL:",
            "Canonical URL:",
            "Title tag:",
            "Meta description:",
            "CMS page title:",
            "Open Graph / Twitter title:",
            "Open Graph / Twitter description:",
            "H1:",
            "Robots:",
            "Media note:",
            "Architecture:",
        ):
            if label not in body_text:
                errors.append(f"Publisher metadata label is missing: {label}")

    report(document_path, errors, warnings, facts)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
