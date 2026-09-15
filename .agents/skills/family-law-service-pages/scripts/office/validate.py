#!/usr/bin/env python3
"""LOCAL REPLACEMENT structural validator for Core Practice-Area Hub DOCX files.

The source package named this interface but did not include an implementation.
This validator checks only deterministic requirements stated in SKILL.md, the
local Core template, and the supplied manifest. It does not assess prose,
strategy, visual quality, legal accuracy, or live publication status.

Usage: python3 validate.py <document.docx> --manifest <input.json>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"w": W_NS, "r": R_NS, "pr": PKG_REL_NS}


def q(namespace: str, local: str) -> str:
    return f"{{{namespace}}}{local}"


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*", text)


def split_sentences(text: str, protected_phrases: tuple[str, ...] = ()) -> list[str]:
    """Split prose without treating common legal-citation periods as boundaries."""

    marker = "\ue000"
    protected = text
    for phrase in sorted(protected_phrases, key=len, reverse=True):
        if phrase:
            protected = protected.replace(phrase, phrase.replace(".", marker))
    protected = re.sub(
        r"\b(?:Ala|Ariz|Ark|Cal|Colo|Conn|Del|Fla|Ga|Ill|Ind|Kan|Ky|La|Mass|Mich|Minn|Miss|Mo|Mont|Neb|Nev|Okla|Or|Pa|Tenn|Tex|Vt|Va|Wash|Wis|Wyo|Stat|sec|secs|ch|para|paras|subsec|subsecs|No|Nos|Inc|Co|LLC|Ct|App|Rev|Code|v)\.",
        lambda match: match.group(0)[:-1] + marker,
        protected,
        flags=re.IGNORECASE,
    )
    protected = re.sub(
        r"(?:\b[A-Z]\.){2,}",
        lambda match: match.group(0).replace(".", marker),
        protected,
    )
    protected = re.sub(r"(?<=\d)\.(?=\d)", marker, protected)
    return [
        sentence.replace(marker, ".").strip()
        for sentence in re.split(r"(?<=[.!?])\s+", protected)
        if sentence.strip()
    ]


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))


def paragraph_style(paragraph: ET.Element) -> str | None:
    style = paragraph.find("w:pPr/w:pStyle", NS)
    return style.get(q(W_NS, "val")) if style is not None else None


def load_xml(archive: zipfile.ZipFile, name: str, errors: list[str]) -> ET.Element | None:
    try:
        return ET.fromstring(archive.read(name))
    except KeyError:
        errors.append(f"Required OOXML part is missing: {name}")
    except ET.ParseError as error:
        errors.append(f"OOXML part is not parseable ({name}): {error}")
    return None


def style_values(styles: ET.Element, style_id: str) -> tuple[str | None, str | None, str | None, str | None]:
    if style_id == "Normal":
        run_props = styles.find("w:docDefaults/w:rPrDefault/w:rPr", NS)
        para_props = styles.find("w:docDefaults/w:pPrDefault/w:pPr", NS)
    else:
        style = styles.find(f".//w:style[@w:styleId='{style_id}']", NS)
        if style is None:
            return None, None, None, None
        run_props = style.find("w:rPr", NS)
        para_props = style.find("w:pPr", NS)
    font = None
    size = None
    before = None
    after = None
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
            after = spacing.get(q(W_NS, "after"))
    return font, size, before, after


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Core Hub DOCX package and its manifest.")
    parser.add_argument("document", type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    document_path = args.document.resolve()
    manifest_path = args.manifest.resolve()

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: Cannot read manifest {manifest_path}: {error}")
        return 2

    if manifest.get("workflow") != "core-hub" or manifest.get("schema_version") != 1:
        errors.append("Manifest is not schema_version 1 for workflow core-hub.")
    meta = manifest.get("meta") or {}
    synthetic = meta.get("synthetic_fixture") is True
    filename_pattern = (
        r"^synthetic-[a-z0-9]+(?:-[a-z0-9]+)*-core\.docx$"
        if synthetic
        else r"^[a-z0-9]+(?:-[a-z0-9]+)*-[a-z0-9]+(?:-[a-z0-9]+)*-core\.docx$"
    )
    if not re.fullmatch(filename_pattern, document_path.name):
        errors.append("DOCX filename does not match the Core Hub naming contract.")

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
        for required in (
            "[Content_Types].xml",
            "_rels/.rels",
            "word/document.xml",
            "word/styles.xml",
            "word/numbering.xml",
            "word/_rels/document.xml.rels",
        ):
            if required not in names:
                errors.append(f"Required OOXML part is missing: {required}")

        document = load_xml(archive, "word/document.xml", errors)
        styles = load_xml(archive, "word/styles.xml", errors)
        numbering = load_xml(archive, "word/numbering.xml", errors)
        rels = load_xml(archive, "word/_rels/document.xml.rels", errors)
        load_xml(archive, "[Content_Types].xml", errors)

        if document is None or styles is None or numbering is None or rels is None:
            print_report(document_path, errors, warnings, {})
            return 1

        if "word/comments.xml" in names:
            comments = load_xml(archive, "word/comments.xml", errors)
            if comments is not None and comments.findall(".//w:comment", NS):
                errors.append("Comments remain in the DOCX package.")
        if (
            document.findall(".//w:commentRangeStart", NS)
            or document.findall(".//w:commentRangeEnd", NS)
            or document.findall(".//w:commentReference", NS)
        ):
            errors.append("Comment markers remain in document.xml.")
        if document.findall(".//w:ins", NS) or document.findall(".//w:del", NS):
            errors.append("Tracked insertions or deletions remain in document.xml.")

        section = document.find(".//w:sectPr", NS)
        if section is None:
            errors.append("Section properties are missing.")
        else:
            page_size = section.find("w:pgSz", NS)
            margins = section.find("w:pgMar", NS)
            actual_size = (
                page_size.get(q(W_NS, "w")) if page_size is not None else None,
                page_size.get(q(W_NS, "h")) if page_size is not None else None,
            )
            if actual_size != ("12240", "15840"):
                errors.append(f"Page size must be US Letter 12240×15840 DXA; found {actual_size}.")
            if margins is None:
                errors.append("Page margins are missing.")
            else:
                actual_margins = {side: margins.get(q(W_NS, side)) for side in ("top", "right", "bottom", "left")}
                if any(value != "1440" for value in actual_margins.values()):
                    errors.append(f"All margins must be 1440 DXA; found {actual_margins}.")

        style_expectations = {
            "Normal": ("Arial", "24", None),
            "Heading1": ("Arial", "36", "240"),
            "Heading2": ("Arial", "30", "360"),
            "Heading3": ("Arial", "26", "280"),
        }
        style_results: dict[str, tuple[str | None, str | None, str | None, str | None]] = {}
        for style_id, (font_expected, size_expected, before_minimum) in style_expectations.items():
            found = style_values(styles, style_id)
            style_results[style_id] = found
            font, size, before, _after = found
            if font != font_expected or size != size_expected:
                errors.append(f"{style_id} must use {font_expected} {int(size_expected) / 2:g} pt; found font={font}, size={size}.")
            if before_minimum is not None and (before is None or int(before) < int(before_minimum)):
                errors.append(f"{style_id} spacing-before must be at least {before_minimum} DXA; found {before}.")

        paragraphs = document.findall(".//w:body/w:p", NS)
        nonempty = [(index, paragraph, paragraph_text(paragraph).strip(), paragraph_style(paragraph)) for index, paragraph in enumerate(paragraphs)]
        nonempty = [item for item in nonempty if item[2]]
        heading_levels = {"Heading1": 1, "Heading2": 2, "Heading3": 3}
        headings = [(index, heading_levels[style], text) for index, _paragraph, text, style in nonempty if style in heading_levels]
        h1_count = sum(1 for _index, level, _text in headings if level == 1)
        if h1_count != 1:
            errors.append(f"Exactly one styled H1 is required; found {h1_count}.")
        previous_level = 0
        for _index, level, text in headings:
            if previous_level and level > previous_level + 1:
                errors.append(f"Heading hierarchy skips from H{previous_level} to H{level} before {text!r}.")
            previous_level = level

        h1_indexes = [index for index, level, _text in headings if level == 1]
        if h1_indexes:
            h1_sequence_position = next(
                position for position, item in enumerate(nonempty) if item[0] == h1_indexes[0]
            )
            following = nonempty[h1_sequence_position + 1 : h1_sequence_position + 3]
            if (
                len(following) != 2
                or any(item[3] in heading_levels for item in following)
                or any(item[1].find("w:pPr/w:numPr", NS) is not None for item in following)
            ):
                errors.append("H1 must be followed immediately by two non-empty, non-list opening paragraphs.")

        manifest_headings = {
            block.get("role"): block.get("text")
            for block in manifest.get("content", [])
            if block.get("type") == "h2" and block.get("role")
        }
        h2_texts = [text for _index, level, text in headings if level == 2]
        role_positions: dict[str, int] = {}
        for role in ("firm-help", "faq", "cta"):
            expected = manifest_headings.get(role)
            matches = [index for index, level, text in headings if level == 2 and text == expected]
            if not expected or len(matches) != 1:
                errors.append(f"Manifested H2 role {role} is missing or not represented exactly once in the DOCX.")
            else:
                role_positions[role] = matches[0]

        if len(role_positions) == 3 and not (
            role_positions["firm-help"] < role_positions["faq"] < role_positions["cta"]
        ):
            errors.append("Required H2 roles must appear in firm-help, FAQ, then CTA order.")

        h2_indexes = sorted(index for index, level, _text in headings if level == 2)

        def section_end(start: int) -> int:
            return next((index for index in h2_indexes if index > start), len(paragraphs))

        for role in ("firm-help", "faq", "cta"):
            if role not in role_positions:
                continue
            start = role_positions[role]
            end = section_end(start)
            body_items = [
                item
                for item in nonempty
                if start < item[0] < end and item[3] not in heading_levels
            ]
            if not body_items:
                errors.append(f"Required {role} section has no body content in the DOCX.")

        faq_heading = manifest_headings.get("faq")
        if faq_heading in h2_texts:
            faq_start = role_positions.get("faq")
            faq_end = section_end(faq_start) if faq_start is not None else len(paragraphs)
            faq_questions = [
                (index, text)
                for index, level, text in headings
                if faq_start is not None and faq_start < index < faq_end and level == 3
            ]
            if not faq_questions:
                errors.append("Hub FAQ H2 has no H3 question beneath it.")
            for question_position, question_text in faq_questions:
                next_heading = next(
                    (
                        index
                        for index, _level, _text in headings
                        if question_position < index < faq_end
                    ),
                    faq_end,
                )
                answers = [
                    item
                    for item in nonempty
                    if question_position < item[0] < next_heading and item[3] not in heading_levels
                ]
                if not answers:
                    errors.append(f"FAQ question has no body answer: {question_text!r}.")

        sources = manifest.get("sources") or []
        source_start_index: int | None = None
        if sources:
            if not h2_texts or h2_texts[-1] != "Sources":
                errors.append("Sources must be the final H2 when citations exist.")
            source_headings = [index for index, level, text in headings if level == 2 and text == "Sources"]
            if len(source_headings) == 1:
                source_start_index = source_headings[0]
                source_paragraphs = [
                    item
                    for item in nonempty
                    if item[0] > source_headings[0] and item[3] not in heading_levels
                ]
                if len(source_paragraphs) != len(sources):
                    errors.append(
                        f"Sources section must contain one paragraph per source; expected {len(sources)}, "
                        f"found {len(source_paragraphs)}."
                    )
                normal_size = style_results.get("Normal", (None, None, None, None))[1]
                for _index, paragraph, source_text, _style in source_paragraphs:
                    for run in paragraph.findall(".//w:r", NS):
                        if not paragraph_text(run).strip():
                            continue
                        size_node = run.find("w:rPr/w:sz", NS)
                        effective_size = size_node.get(q(W_NS, "val")) if size_node is not None else normal_size
                        if effective_size != "24":
                            errors.append(
                                f"Sources text must use 12 pt body size; found {effective_size!r} in {source_text[:60]!r}."
                            )
                            break
        elif "Sources" in h2_texts:
            errors.append("DOCX contains a Sources H2 but the manifest has no sources.")

        content_start_index = h1_indexes[0] if h1_indexes else 0
        content_end_index = source_start_index if source_start_index is not None else len(paragraphs)
        actual_content = [
            item for item in nonempty if content_start_index <= item[0] < content_end_index
        ]
        expected_content: list[tuple[str, str]] = []
        for block in manifest.get("content") or []:
            block_type = block.get("type")
            if block_type in {"h1", "h2", "h3"}:
                expected_content.append((f"Heading{block_type[1]}", str(block.get("text") or "")))
            elif block_type == "p":
                expected_content.append(
                    ("paragraph", "".join(str(run.get("text") or "") for run in block.get("runs") or []))
                )
            elif block_type in {"ul", "ol"}:
                for item in block.get("items") or []:
                    expected_content.append(
                        ("list", "".join(str(run.get("text") or "") for run in item.get("runs") or []))
                    )
        if len(actual_content) != len(expected_content):
            errors.append(
                f"DOCX/manifest paragraph inventory differs: expected {len(expected_content)}, "
                f"found {len(actual_content)}."
            )
        for position, (actual, expected) in enumerate(zip(actual_content, expected_content), start=1):
            _index, paragraph, actual_text, actual_style = actual
            expected_kind, expected_text = expected
            actual_kind = (
                actual_style
                if actual_style in heading_levels
                else "list"
                if paragraph.find("w:pPr/w:numPr", NS) is not None
                else "paragraph"
            )
            if actual_kind != expected_kind:
                errors.append(
                    f"DOCX/manifest structure differs at content paragraph {position}: "
                    f"expected {expected_kind}, found {actual_kind}."
                )
            if actual_text != expected_text:
                errors.append(
                    f"DOCX/manifest text differs at content paragraph {position}."
                )

        expected_list_items = sum(
            len(block.get("items") or [])
            for block in manifest.get("content", [])
            if block.get("type") in {"ul", "ol"}
        )
        numbered_paragraphs = [p for p in paragraphs if p.find("w:pPr/w:numPr", NS) is not None]
        if len(numbered_paragraphs) != expected_list_items:
            errors.append(f"Expected {expected_list_items} true list paragraphs; found {len(numbered_paragraphs)}.")
        for paragraph in paragraphs:
            text = paragraph_text(paragraph).lstrip()
            if (text.startswith("•") or re.match(r"^\d+[.)]\s", text)) and paragraph.find("w:pPr/w:numPr", NS) is None:
                errors.append(f"Typed list marker found instead of OOXML numbering: {text[:60]!r}.")

        discipline_paragraphs = [
            (index, text)
            for index, _paragraph, text, style in nonempty
            if (
                content_start_index <= index < content_end_index
                and style not in heading_levels
                and not text.startswith("SYNTHETIC WORKFLOW FIXTURE")
            )
        ]
        for index, text in discipline_paragraphs:
            source_identifiers = tuple(str(source.get("identifier") or "") for source in sources)
            sentence_texts = split_sentences(text, source_identifiers)
            if len(sentence_texts) > 3:
                errors.append(f"Body paragraph {index + 1} exceeds 3 sentences ({len(sentence_texts)}).")
            for sentence in sentence_texts:
                sentence_words = len(words(sentence))
                if sentence_words > 30:
                    errors.append(
                        f"Body paragraph {index + 1} has a sentence over 30 words "
                        f"({sentence_words}): {sentence[:80]!r}."
                    )

        relationship_map: dict[str, tuple[str, str | None, str | None]] = {}
        for relationship in rels.findall("pr:Relationship", NS):
            relationship_map[relationship.get("Id", "")] = (
                relationship.get("Target", ""),
                relationship.get("TargetMode"),
                relationship.get("Type"),
            )
        hyperlink_targets: list[str] = []
        for hyperlink in document.findall(".//w:hyperlink", NS):
            relationship_id = hyperlink.get(q(R_NS, "id"))
            visible = "".join(node.text or "" for node in hyperlink.findall(".//w:t", NS)).strip()
            if not relationship_id:
                errors.append("DOCX contains a hyperlink without an external manifest relationship.")
                continue
            if relationship_id not in relationship_map:
                errors.append(f"Hyperlink {relationship_id} has no relationship target.")
                continue
            target, target_mode, rel_type = relationship_map[relationship_id]
            if not visible:
                errors.append(f"Hyperlink {relationship_id} has no visible anchor text.")
            if target_mode != "External" or not (rel_type or "").endswith("/hyperlink"):
                errors.append(f"Hyperlink {relationship_id} is not an external OOXML hyperlink relationship.")
            if not re.match(r"^https?://", target):
                errors.append(f"Hyperlink {relationship_id} target is not HTTP(S): {target!r}.")
            hyperlink_targets.append(target)

        target_counts = Counter(hyperlink_targets)
        expected_targets = Counter(link.get("target_url") for link in manifest.get("link_manifest") or [])
        for source in sources:
            expected_targets[source.get("url")] += 2
        for target, expected_count in expected_targets.items():
            actual_count = target_counts[target]
            if actual_count != expected_count:
                errors.append(
                    f"Manifested hyperlink target {target!r} expected {expected_count} occurrence(s), "
                    f"found {actual_count}."
                )
        for target, actual_count in (target_counts - expected_targets).items():
            errors.append(
                f"Unmanifested DOCX hyperlink target {target!r} appears {actual_count} time(s)."
            )

        document_text = " ".join(paragraph_text(paragraph) for paragraph in paragraphs)
        content_text = " ".join(item[2] for item in actual_content)
        word_count = len(words(content_text))
        if not 1800 <= word_count <= 2600:
            errors.append(f"V2 Core Hub word target is 1,800–2,600; DOCX manifest content contains {word_count} words.")

        local_detail_pattern = re.compile(r"\[LOCAL DETAIL:\s*[^\]\s][^\]]*\]", flags=re.IGNORECASE)
        local_details = local_detail_pattern.findall(document_text)
        unmatched_local_detail_text = local_detail_pattern.sub("", document_text)
        if re.search(r"\[LOCAL DETAIL", unmatched_local_detail_text, flags=re.IGNORECASE):
            errors.append("Malformed local-detail marker found; use [LOCAL DETAIL: description].")
        run_local_details: list[str] = []
        for run in document.findall(".//w:r", NS):
            run_text = paragraph_text(run)
            markers = local_detail_pattern.findall(run_text)
            if not markers:
                continue
            run_local_details.extend(markers)
            bold = run.find("w:rPr/w:b", NS)
            bold_value = bold.get(q(W_NS, "val")) if bold is not None else None
            if bold is None or str(bold_value).lower() in {"0", "false", "off"}:
                errors.append(f"Local-detail marker must be bold: {markers[0]!r}.")
        if Counter(run_local_details) != Counter(local_details):
            errors.append("Each local-detail marker must be contained in one bold text run.")
        if local_details:
            warnings.append(
                "Documented [LOCAL DETAIL] markers require editorial resolution before publication: "
                f"{sorted(set(local_details))}."
            )
        placeholders = re.findall(
            r"\[(?:INSERT|TBD|CLIENT NAME|FIRM NAME|DATE|MARKET)[^\]]*\]|\b(?:TODO|FIXME|LOREM IPSUM)\b",
            document_text,
            flags=re.IGNORECASE,
        )
        if placeholders:
            errors.append(f"Unresolved placeholder markers found: {sorted(set(placeholders))}.")

        header_parts = [name for name in names if re.fullmatch(r"word/header\d+\.xml", name)]
        footer_parts = [name for name in names if re.fullmatch(r"word/footer\d+\.xml", name)]
        if not header_parts:
            errors.append("Local Core contract requires a header part; none was found.")
        if not footer_parts:
            errors.append("Local Core contract requires a footer part; none was found.")
        else:
            footer_text = "".join(archive.read(name).decode("utf-8", errors="replace") for name in footer_parts)
            if "PAGE" not in footer_text or "NUMPAGES" not in footer_text:
                warnings.append("Footer page fields could not be confirmed by literal field text; verify in render.")

        stats = {
            "words": word_count,
            "headings": len(headings),
            "lists": len(numbered_paragraphs),
            "hyperlinks": len(hyperlink_targets),
            "manifest_links": len(manifest.get("link_manifest") or []),
            "sources": len(sources),
        }
        print_report(document_path, errors, warnings, stats)
        return 1 if errors else 0


def print_report(document: Path, errors: list[str], warnings: list[str], stats: dict[str, int]) -> None:
    print(f"\n=== Core Hub structural validation: {document.name} ===\n")
    if stats:
        print(
            "Inventory: "
            + " | ".join(f"{key}={value}" for key, value in stats.items())
        )
        print()
    if errors:
        print(f"FAIL ({len(errors)}):")
        for error in errors:
            print(f"  ✗ {error}")
    else:
        print("PASS: Supported deterministic Core Hub checks cleared.")
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  ⚠ {warning}")
    print("\nScope: structure and manifest mechanics only; not editorial, SEO, visual, publication, or legal clearance.")


if __name__ == "__main__":
    sys.exit(main())
