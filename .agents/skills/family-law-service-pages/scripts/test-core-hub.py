#!/usr/bin/env python3
"""Regression checks for the local Core Hub generator/validator workflow.

Creates intentionally broken DOCX copies in a temporary directory and proves
that supported mechanical failures are rejected. Only logs are retained.

Usage: python3 test-core-hub.py <positive.docx> <manifest.json> <evidence-dir>
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


sys.dont_write_bytecode = True
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W_NS}


def rewrite_member(source: Path, destination: Path, member: str, transform) -> None:
    with zipfile.ZipFile(source, "r") as reader, zipfile.ZipFile(destination, "w") as writer:
        for info in reader.infolist():
            payload = reader.read(info.filename)
            if info.filename == member:
                payload = transform(payload)
            writer.writestr(info, payload)


def drop_member(source: Path, destination: Path, member: str) -> None:
    with zipfile.ZipFile(source, "r") as reader, zipfile.ZipFile(destination, "w") as writer:
        for info in reader.infolist():
            if info.filename != member:
                writer.writestr(info, reader.read(info.filename))


def require_replacement(payload: bytes, old: bytes, new: bytes) -> bytes:
    if old not in payload:
        raise RuntimeError(f"Mutation source not found: {old!r}")
    return payload.replace(old, new, 1)


def duplicate_first_hyperlink(payload: bytes) -> bytes:
    match = re.search(rb"(<w:hyperlink\b[\s\S]*?</w:hyperlink>)", payload)
    if not match:
        raise RuntimeError("No external hyperlink block found for duplicate-link mutation.")
    return payload[: match.end()] + match.group(1) + payload[match.end() :]


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))


def style_next_paragraph(payload: bytes, heading_text: str, style_id: str) -> bytes:
    root = ET.fromstring(payload)
    paragraphs = root.findall(".//w:body/w:p", NS)
    for position, paragraph in enumerate(paragraphs):
        if paragraph_text(paragraph) != heading_text:
            continue
        for candidate in paragraphs[position + 1 :]:
            if not paragraph_text(candidate).strip():
                continue
            paragraph_props = candidate.find("w:pPr", NS)
            if paragraph_props is None:
                paragraph_props = ET.Element(f"{{{W_NS}}}pPr")
                candidate.insert(0, paragraph_props)
            style = paragraph_props.find("w:pStyle", NS)
            if style is None:
                style = ET.Element(f"{{{W_NS}}}pStyle")
                paragraph_props.insert(0, style)
            style.set(f"{{{W_NS}}}val", style_id)
            return ET.tostring(root, encoding="utf-8", xml_declaration=True)
        break
    raise RuntimeError(f"Could not find a populated paragraph after heading {heading_text!r}.")


def style_section_body(payload: bytes, heading_text: str, style_id: str) -> bytes:
    root = ET.fromstring(payload)
    paragraphs = root.findall(".//w:body/w:p", NS)
    inside_section = False
    changed = 0
    for paragraph in paragraphs:
        text = paragraph_text(paragraph)
        paragraph_props = paragraph.find("w:pPr", NS)
        current_style = paragraph_props.find("w:pStyle", NS) if paragraph_props is not None else None
        current_style_id = current_style.get(f"{{{W_NS}}}val") if current_style is not None else None
        if text == heading_text:
            inside_section = True
            continue
        if not inside_section:
            continue
        if current_style_id == "Heading2":
            break
        if not text.strip() or current_style_id in {"Heading1", "Heading3"}:
            continue
        if paragraph_props is None:
            paragraph_props = ET.Element(f"{{{W_NS}}}pPr")
            paragraph.insert(0, paragraph_props)
        style = paragraph_props.find("w:pStyle", NS)
        if style is None:
            style = ET.Element(f"{{{W_NS}}}pStyle")
            paragraph_props.insert(0, style)
        style.set(f"{{{W_NS}}}val", style_id)
        changed += 1
    if not inside_section or changed == 0:
        raise RuntimeError(f"Could not restyle body content beneath heading {heading_text!r}.")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def set_source_run_size(payload: bytes, size: str) -> bytes:
    root = ET.fromstring(payload)
    paragraphs = root.findall(".//w:body/w:p", NS)
    inside_sources = False
    changed = 0
    for paragraph in paragraphs:
        text = paragraph_text(paragraph)
        if text == "Sources":
            inside_sources = True
            continue
        if not inside_sources or not text.strip():
            continue
        for run in paragraph.findall(".//w:r", NS):
            if not paragraph_text(run).strip():
                continue
            run_props = run.find("w:rPr", NS)
            if run_props is None:
                run_props = ET.Element(f"{{{W_NS}}}rPr")
                run.insert(0, run_props)
            size_node = run_props.find("w:sz", NS)
            if size_node is None:
                size_node = ET.SubElement(run_props, f"{{{W_NS}}}sz")
            size_node.set(f"{{{W_NS}}}val", size)
            changed += 1
    if changed == 0:
        raise RuntimeError("No source runs found for font-size mutation.")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def swap_text(payload: bytes, first: bytes, second: bytes) -> bytes:
    marker = b"__CORE_HUB_SWAP_MARKER__"
    if first not in payload or second not in payload or marker in payload:
        raise RuntimeError("Heading swap source was not unique and available.")
    return payload.replace(first, marker, 1).replace(second, first, 1).replace(marker, second, 1)


def swap_first_two_body_citation_targets(payload: bytes) -> bytes:
    root = ET.fromstring(payload)
    citation_links = [
        hyperlink
        for hyperlink in root.findall(".//w:hyperlink", NS)
        if re.fullmatch(r"\[\d+\]", paragraph_text(hyperlink).strip())
    ]
    if len(citation_links) < 2:
        raise RuntimeError("Fewer than two body citation hyperlinks were available for target-swap mutation.")
    relationship_key = f"{{{R_NS}}}id"
    first_id = citation_links[0].get(relationship_key)
    second_id = citation_links[1].get(relationship_key)
    if not first_id or not second_id or first_id == second_id:
        raise RuntimeError("The first two body citations do not have distinct relationship targets.")
    citation_links[0].set(relationship_key, second_id)
    citation_links[1].set(relationship_key, first_id)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def run_case(name: str, command: list[str], expected_marker: str, evidence_dir: Path) -> tuple[bool, int]:
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    log = f"$ {' '.join(command)}\nexit={completed.returncode}\n\n{completed.stdout}"
    (evidence_dir / f"{name}.txt").write_text(log, encoding="utf-8")
    passed = completed.returncode != 0 and expected_marker in completed.stdout
    return passed, completed.returncode


def run_positive(name: str, command: list[str], expected_marker: str, evidence_dir: Path) -> tuple[bool, int]:
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    log = f"$ {' '.join(command)}\nexit={completed.returncode}\n\n{completed.stdout}"
    (evidence_dir / f"{name}.txt").write_text(log, encoding="utf-8")
    passed = completed.returncode == 0 and expected_marker in completed.stdout
    return passed, completed.returncode


def run_positive_pipeline(
    name: str,
    commands: list[list[str]],
    expected_marker: str,
    evidence_dir: Path,
) -> tuple[bool, int]:
    output: list[str] = []
    final_code = 0
    for command in commands:
        completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        output.append(f"$ {' '.join(command)}\nexit={completed.returncode}\n\n{completed.stdout}")
        final_code = completed.returncode
        if completed.returncode != 0:
            break
    combined = "\n".join(output)
    (evidence_dir / f"{name}.txt").write_text(combined, encoding="utf-8")
    return final_code == 0 and expected_marker in combined, final_code


def run_negative_pipeline(
    name: str,
    setup_commands: list[list[str]],
    failing_command: list[str],
    expected_marker: str,
    evidence_dir: Path,
) -> tuple[bool, int]:
    output: list[str] = []
    for command in setup_commands:
        completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        output.append(f"$ {' '.join(command)}\nexit={completed.returncode}\n\n{completed.stdout}")
        if completed.returncode != 0:
            combined = "\n".join(output)
            (evidence_dir / f"{name}.txt").write_text(combined, encoding="utf-8")
            return False, completed.returncode
    completed = subprocess.run(
        failing_command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output.append(f"$ {' '.join(failing_command)}\nexit={completed.returncode}\n\n{completed.stdout}")
    combined = "\n".join(output)
    (evidence_dir / f"{name}.txt").write_text(combined, encoding="utf-8")
    return completed.returncode != 0 and expected_marker in completed.stdout, completed.returncode


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: python3 test-core-hub.py <positive.docx> <manifest.json> <evidence-dir>")
        return 2

    positive = Path(sys.argv[1]).resolve()
    manifest = Path(sys.argv[2]).resolve()
    evidence_dir = Path(sys.argv[3]).resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)
    skill_root = Path(__file__).resolve().parent.parent
    structural = skill_root / "scripts/office/validate.py"
    page_validator = skill_root / "scripts/validate-page.js"
    builder = skill_root / "scripts/build-core-hub.js"
    renderer = skill_root / "scripts/render-core-hub.sh"
    positive_results: list[tuple[str, bool, int, str]] = []
    results: list[tuple[str, bool, int, str]] = []

    ok, code = run_positive(
        "positive-structural",
        [sys.executable, str(structural), str(positive), "--manifest", str(manifest)],
        "PASS: Supported deterministic Core Hub checks cleared.",
        evidence_dir,
    )
    positive_results.append(("Structural validator accepts the fixture", ok, code, "PASS: Supported deterministic Core Hub checks cleared."))
    ok, code = run_positive(
        "positive-page-level",
        ["node", str(page_validator), str(positive)],
        "PASS: All hard rules cleared.",
        evidence_dir,
    )
    positive_results.append(("Recovered page validator accepts the fixture", ok, code, "PASS: All hard rules cleared."))

    validator_spec = importlib.util.spec_from_file_location("core_hub_validator", structural)
    if validator_spec is None or validator_spec.loader is None:
        raise RuntimeError("Could not load the structural validator for sentence-parser regression.")
    validator_module = importlib.util.module_from_spec(validator_spec)
    validator_spec.loader.exec_module(validator_module)
    citation_example = "Florida uses an income shares model to calculate child support. Fla. Stat. sec. 61.30 [1]"
    parsed_sentences = validator_module.split_sentences(citation_example)
    parser_ok = len(parsed_sentences) == 2
    parser_log = (
        "$ internal split_sentences regression\n"
        f"exit={0 if parser_ok else 1}\n\n"
        f"input={citation_example}\ncount={len(parsed_sentences)}\nparts={parsed_sentences!r}\n"
    )
    (evidence_dir / "positive-legal-citation-sentence-parser.txt").write_text(parser_log, encoding="utf-8")
    positive_results.append(("Legal citation abbreviations remain within two sentences", parser_ok, 0 if parser_ok else 1, "count=2"))

    with tempfile.TemporaryDirectory(prefix="core-hub-negative-") as temporary:
        temp = Path(temporary)
        base_manifest = json.loads(manifest.read_text(encoding="utf-8"))
        wrong_size = temp / positive.name
        duplicate_link = temp / positive.name
        em_dash = temp / positive.name
        broken_relationship = temp / positive.name
        unmanifested_link = temp / positive.name
        interrupted_opening = temp / positive.name
        reordered_roles = temp / positive.name
        empty_cta = temp / positive.name
        local_detail = temp / positive.name
        generic_placeholder = temp / positive.name
        missing_header = temp / positive.name
        missing_footer = temp / positive.name

        rewrite_member(
            positive,
            wrong_size,
            "word/document.xml",
            lambda payload: require_replacement(payload, b'w:w="12240"', b'w:w="12000"'),
        )
        ok, code = run_case(
            "negative-structural-page-size",
            [sys.executable, str(structural), str(wrong_size), "--manifest", str(manifest)],
            "Page size must be US Letter",
            evidence_dir,
        )
        results.append(("Wrong page size rejected by structural validator", ok, code, "Page size must be US Letter"))

        rewrite_member(positive, duplicate_link, "word/document.xml", duplicate_first_hyperlink)
        ok, code = run_case(
            "negative-page-duplicate-link",
            ["node", str(page_validator), str(duplicate_link)],
            "Single-Placement Rule violated",
            evidence_dir,
        )
        results.append(("Duplicate body URL rejected by recovered validator", ok, code, "Single-Placement Rule violated"))

        rewrite_member(
            positive,
            em_dash,
            "word/document.xml",
            lambda payload: require_replacement(
                payload,
                b"This synthetic hub shows",
                "This synthetic—hub shows".encode("utf-8"),
            ),
        )
        ok, code = run_case(
            "negative-page-em-dash",
            ["node", str(page_validator), str(em_dash)],
            "Em dashes",
            evidence_dir,
        )
        results.append(("Em dash rejected by recovered validator", ok, code, "Em dashes"))

        rewrite_member(
            positive,
            broken_relationship,
            "word/_rels/document.xml.rels",
            lambda payload: require_replacement(payload, b' TargetMode="External"', b""),
        )
        ok, code = run_case(
            "negative-structural-hyperlink-relationship",
            [sys.executable, str(structural), str(broken_relationship), "--manifest", str(manifest)],
            "not an external OOXML hyperlink relationship",
            evidence_dir,
        )
        results.append(("Broken hyperlink relationship rejected by structural validator", ok, code, "not an external OOXML hyperlink relationship"))

        rewrite_member(
            positive,
            unmanifested_link,
            "word/_rels/document.xml.rels",
            lambda payload: require_replacement(
                payload,
                b"https://example.com/divorce/collaborative-divorce/",
                b"https://example.com/unmanifested/",
            ),
        )
        ok, code = run_case(
            "negative-structural-unmanifested-hyperlink",
            [sys.executable, str(structural), str(unmanifested_link), "--manifest", str(manifest)],
            "Unmanifested DOCX hyperlink target",
            evidence_dir,
        )
        results.append(("Unmanifested functional URL rejected by structural validator", ok, code, "Unmanifested DOCX hyperlink target"))

        rewrite_member(
            positive,
            interrupted_opening,
            "word/document.xml",
            lambda payload: style_next_paragraph(
                payload,
                "Divorce Services: Synthetic Core Hub Fixture",
                "Heading2",
            ),
        )
        ok, code = run_case(
            "negative-structural-interrupted-opening",
            [sys.executable, str(structural), str(interrupted_opening), "--manifest", str(manifest)],
            "H1 must be followed immediately by two non-empty, non-list opening paragraphs",
            evidence_dir,
        )
        results.append(("Heading inserted into two-paragraph opening rejected", ok, code, "H1 must be followed immediately"))

        rewrite_member(
            positive,
            reordered_roles,
            "word/document.xml",
            lambda payload: swap_text(
                payload,
                b"How a Verified Firm Could Support the Reader",
                b"Next Step for This Synthetic Fixture",
            ),
        )
        ok, code = run_case(
            "negative-structural-required-role-order",
            [sys.executable, str(structural), str(reordered_roles), "--manifest", str(manifest)],
            "Required H2 roles must appear in firm-help, FAQ, then CTA order",
            evidence_dir,
        )
        results.append(("Reordered required sections rejected", ok, code, "Required H2 roles must appear"))

        rewrite_member(
            positive,
            empty_cta,
            "word/document.xml",
            lambda payload: style_section_body(
                payload,
                "Next Step for This Synthetic Fixture",
                "Heading3",
            ),
        )
        ok, code = run_case(
            "negative-structural-empty-cta",
            [sys.executable, str(structural), str(empty_cta), "--manifest", str(manifest)],
            "Required cta section has no body content",
            evidence_dir,
        )
        results.append(("Required CTA without body copy rejected", ok, code, "Required cta section has no body content"))

        local_detail_manifest = json.loads(json.dumps(base_manifest))
        local_detail_manifest["content"][1]["runs"] = [
            {"text": "[LOCAL DETAIL: synthetic warning test]", "bold": True},
            {"text": " "},
            *local_detail_manifest["content"][1]["runs"],
        ]
        local_detail_input = temp / "local-detail.json"
        local_detail_input.write_text(json.dumps(local_detail_manifest), encoding="utf-8")
        ok, code = run_positive_pipeline(
            "positive-structural-local-detail-warning",
            [
                ["node", str(builder), str(local_detail_input), str(local_detail)],
                [sys.executable, str(structural), str(local_detail), "--manifest", str(local_detail_input)],
            ],
            "Documented [LOCAL DETAIL] markers require editorial resolution before publication",
            evidence_dir,
        )
        positive_results.append(("Documented local-detail marker warns without inventing a hard failure", ok, code, "[LOCAL DETAIL] markers require editorial resolution"))

        unbold_local_manifest = json.loads(json.dumps(local_detail_manifest))
        unbold_local_manifest["content"][1]["runs"][0].pop("bold")
        unbold_local_input = temp / "unbold-local-detail.json"
        unbold_local_input.write_text(json.dumps(unbold_local_manifest), encoding="utf-8")
        ok, code = run_case(
            "negative-generator-unbold-local-detail",
            ["node", str(builder), str(unbold_local_input), str(temp / "synthetic-unbold-local-detail-core.docx")],
            "local-detail markers must be bold runs",
            evidence_dir,
        )
        results.append(("Unbold local-detail marker rejected", ok, code, "local-detail markers must be bold runs"))

        rewrite_member(
            positive,
            generic_placeholder,
            "word/document.xml",
            lambda payload: require_replacement(
                payload,
                b"This synthetic hub shows",
                b"[TBD] This synthetic hub shows",
            ),
        )
        ok, code = run_case(
            "negative-structural-generic-placeholder",
            [sys.executable, str(structural), str(generic_placeholder), "--manifest", str(manifest)],
            "Unresolved placeholder markers found",
            evidence_dir,
        )
        results.append(("Undocumented generic placeholder rejected", ok, code, "Unresolved placeholder markers found"))

        with zipfile.ZipFile(positive) as positive_archive:
            positive_names = positive_archive.namelist()
        header_member = next(name for name in positive_names if re.fullmatch(r"word/header\d+\.xml", name))
        footer_member = next(name for name in positive_names if re.fullmatch(r"word/footer\d+\.xml", name))
        drop_member(positive, missing_header, header_member)
        ok, code = run_case(
            "negative-structural-missing-local-header",
            [sys.executable, str(structural), str(missing_header), "--manifest", str(manifest)],
            "Local Core contract requires a header part",
            evidence_dir,
        )
        results.append(("Missing local-contract header rejected", ok, code, "Local Core contract requires a header part"))
        drop_member(positive, missing_footer, footer_member)
        ok, code = run_case(
            "negative-structural-missing-local-footer",
            [sys.executable, str(structural), str(missing_footer), "--manifest", str(manifest)],
            "Local Core contract requires a footer part",
            evidence_dir,
        )
        results.append(("Missing local-contract footer rejected", ok, code, "Local Core contract requires a footer part"))

        held_manifest = json.loads(json.dumps(base_manifest))
        held_manifest["link_manifest"][0].update(
            {
                "target_node_id": "FL-M013",
                "v2_reference_path": "/divorce/summary-dissolution/",
                "v2_page_type": "Practice-Area Procedural Page",
                "v2_role": "Core Procedure",
                "v2_requiredness": "Optional",
                "client_url": "https://example.com/divorce/summary-dissolution/",
            }
        )
        held_input = temp / "held-target.json"
        held_input.write_text(json.dumps(held_manifest), encoding="utf-8")
        ok, code = run_case(
            "negative-generator-held-v2-target",
            ["node", str(builder), str(held_input), str(temp / "synthetic-held-target-core.docx")],
            "cannot be linked while its gate is HOLD — ARCHITECTURE REVIEW",
            evidence_dir,
        )
        results.append(("V2-held child target rejected before generation", ok, code, "cannot be linked while its gate is HOLD"))

        conditional_manifest = json.loads(json.dumps(base_manifest))
        conditional_manifest["link_manifest"][0].update(
            {
                "target_node_id": "FL-M025",
                "v2_reference_path": "/divorce/military-divorce/",
                "v2_page_type": "Practice-Area Situational Page",
                "v2_role": "Situational",
                "v2_requiredness": "Conditional",
                "client_url": "https://example.com/divorce/military-divorce/",
            }
        )
        conditional_input = temp / "conditional-target.json"
        conditional_input.write_text(json.dumps(conditional_manifest), encoding="utf-8")
        ok, code = run_case(
            "negative-generator-unapproved-conditional-target",
            ["node", str(builder), str(conditional_input), str(temp / "synthetic-conditional-target-core.docx")],
            "requires target_gate_approval \"approved\" and target_gate_evidence",
            evidence_dir,
        )
        results.append(("Conditional child without gate evidence rejected", ok, code, "requires target_gate_approval"))

        approved_conditional_manifest = json.loads(json.dumps(conditional_manifest))
        approved_conditional_manifest["link_manifest"][0].update(
            {
                "target_gate_approval": "approved",
                "target_gate_evidence": "Synthetic regression evidence only; no client publication claim.",
            }
        )
        approved_conditional_input = temp / "approved-conditional-target.json"
        approved_conditional_input.write_text(json.dumps(approved_conditional_manifest), encoding="utf-8")
        ok, code = run_positive(
            "positive-generator-approved-conditional-target",
            [
                "node",
                str(builder),
                str(approved_conditional_input),
                str(temp / "synthetic-approved-conditional-target-core.docx"),
            ],
            "DOCX written:",
            evidence_dir,
        )
        positive_results.append(("Conditional child with explicit gate evidence can generate", ok, code, "DOCX written:"))

        mapped_manifest = json.loads(json.dumps(base_manifest))
        mapped_manifest["meta"].pop("synthetic_fixture", None)
        mapped_manifest["meta"].update(
            {
                "firm_name": "Example Organization (mapping regression only)",
                "jurisdiction": "Wisconsin",
                "voice_source": "synthetic-regression-only",
                "client_url": "https://example.com/wisconsin/divorce/",
                "client_url_status": 200,
                "client_url_redirects": 0,
                "client_url_verified_on": "2026-09-15",
                "client_url_evidence": "Ephemeral direct hub URL assertion for mapping regression only.",
            }
        )
        mapped_manifest["link_inventory"] = {
            "status": "reviewed",
            "evidence": "Ephemeral V2-to-client mapping regression using reserved example.com URLs.",
        }
        for link in mapped_manifest["link_manifest"]:
            link["client_url"] = link["client_url"].replace(
                "https://example.com/divorce/",
                "https://example.com/wisconsin/divorce/",
            )
            link["publication_state"] = "published"
            link["publication_evidence"] = "Ephemeral publication assertion for mapping regression only."
            link["client_jurisdiction"] = "Wisconsin"
            link["client_jurisdiction_evidence"] = "The synthetic client path is explicitly assigned to Wisconsin."
            link["client_url_status"] = 200
            link["client_url_redirects"] = 0
            link["client_url_verified_on"] = "2026-09-15"
            link["client_url_evidence"] = "Ephemeral direct child URL assertion for mapping regression only."
        mapped_input = temp / "mapped-client-urls.json"
        mapped_output = temp / "example-mapped-divorce-core.docx"
        mapped_input.write_text(json.dumps(mapped_manifest), encoding="utf-8")
        ok, code = run_positive_pipeline(
            "positive-client-url-mapping",
            [
                ["node", str(builder), str(mapped_input), str(mapped_output)],
                [sys.executable, str(structural), str(mapped_output), "--manifest", str(mapped_input)],
            ],
            "PASS: Supported deterministic Core Hub checks cleared.",
            evidence_dir,
        )
        positive_results.append(("A direct Wisconsin client URL may differ from its preserved V2 path", ok, code, "PASS: Supported deterministic Core Hub checks cleared."))

        wrong_v2_manifest = json.loads(json.dumps(mapped_manifest))
        wrong_v2_manifest["link_manifest"][0]["v2_reference_path"] = "/divorce/not-the-v2-path/"
        wrong_v2_input = temp / "wrong-v2-reference.json"
        wrong_v2_input.write_text(json.dumps(wrong_v2_manifest), encoding="utf-8")
        ok, code = run_case(
            "negative-generator-wrong-v2-reference",
            ["node", str(builder), str(wrong_v2_input), str(temp / "example-wrong-v2-divorce-core.docx")],
            "v2_reference_path must match V2 exactly",
            evidence_dir,
        )
        results.append(("A client mapping cannot change the V2 reference path", ok, code, "v2_reference_path must match V2 exactly"))

        wrong_jurisdiction_manifest = json.loads(json.dumps(mapped_manifest))
        wrong_jurisdiction_manifest["link_manifest"][0]["client_jurisdiction"] = "Illinois"
        wrong_jurisdiction_input = temp / "wrong-client-jurisdiction.json"
        wrong_jurisdiction_input.write_text(json.dumps(wrong_jurisdiction_manifest), encoding="utf-8")
        ok, code = run_case(
            "negative-generator-wrong-client-jurisdiction",
            ["node", str(builder), str(wrong_jurisdiction_input), str(temp / "example-wrong-jurisdiction-divorce-core.docx")],
            "client_jurisdiction must match meta.jurisdiction",
            evidence_dir,
        )
        results.append(("A same-origin client URL cannot be assigned to the wrong jurisdiction", ok, code, "client_jurisdiction must match meta.jurisdiction"))

        wrong_relationship_manifest = json.loads(json.dumps(mapped_manifest))
        wrong_relationship_manifest["link_manifest"][0]["relationship_type"] = "Location-hub service-list destination"
        wrong_relationship_input = temp / "wrong-v2-relationship.json"
        wrong_relationship_input.write_text(json.dumps(wrong_relationship_manifest), encoding="utf-8")
        ok, code = run_case(
            "negative-generator-wrong-v2-relationship",
            ["node", str(builder), str(wrong_relationship_input), str(temp / "example-wrong-relationship-divorce-core.docx")],
            "no directional V2 Location-hub service-list destination relationship",
            evidence_dir,
        )
        results.append(("A client URL cannot bypass the directional V2 relationship", ok, code, "no directional V2"))

        four_sentence_manifest = json.loads(json.dumps(base_manifest))
        four_sentence_manifest["content"][1]["runs"][0]["text"] += " This fourth sentence is a mechanical failure example."
        four_sentence_input = temp / "four-sentence.json"
        four_sentence_output = temp / "synthetic-four-sentence-core.docx"
        four_sentence_input.write_text(json.dumps(four_sentence_manifest), encoding="utf-8")
        ok, code = run_negative_pipeline(
            "negative-structural-four-true-sentences",
            [["node", str(builder), str(four_sentence_input), str(four_sentence_output)]],
            [sys.executable, str(structural), str(four_sentence_output), "--manifest", str(four_sentence_input)],
            "exceeds 3 sentences (4)",
            evidence_dir,
        )
        results.append(("Four true sentences rejected after citation-aware parsing", ok, code, "exceeds 3 sentences (4)"))

        sourced_manifest = json.loads(json.dumps(base_manifest))
        sourced_manifest["meta"].pop("synthetic_fixture", None)
        sourced_manifest["meta"].update(
            {
                "firm_name": "Example Organization (synthetic regression only)",
                "jurisdiction": "Synthetic test jurisdiction",
                "voice_source": "synthetic-regression-only",
                "client_url_status": 200,
                "client_url_redirects": 0,
                "client_url_verified_on": "2026-09-15",
                "client_url_evidence": "Ephemeral direct-URL assertion for a claim-free regression.",
            }
        )
        sourced_manifest["link_inventory"] = {
            "status": "reviewed",
            "evidence": "Ephemeral regression using reserved example.com destinations only.",
        }
        for link in sourced_manifest["link_manifest"]:
            link["publication_state"] = "published"
            link["publication_evidence"] = "Synthetic regression assertion only; not client or live-site evidence."
            link["client_jurisdiction"] = "Synthetic test jurisdiction"
            link["client_jurisdiction_evidence"] = "Ephemeral matching-market assertion for regression only."
            link["client_url_status"] = 200
            link["client_url_redirects"] = 0
            link["client_url_verified_on"] = "2026-09-15"
            link["client_url_evidence"] = "Ephemeral direct-URL assertion for regression only."
        sourced_manifest["sources"] = [
            {
                "id": f"format-source-{index}",
                "identifier": f"Synthetic source-format marker {index}",
                "url": f"https://example.com/source-formatting-{index}/",
            }
            for index in range(1, 10)
        ]
        opening_run = sourced_manifest["content"][1]["runs"][0]
        opening_run["text"] = opening_run["text"].removesuffix(".")
        sourced_manifest["content"][1]["runs"].append({"text": " "})
        for index in range(1, 10):
            sourced_manifest["content"][1]["runs"].append(
                {"text": f"[{index}]", "citation_id": f"format-source-{index}"}
            )
        sourced_manifest["content"][1]["runs"].append({"text": "."})
        sourced_input = temp / "sourced-formatting.json"
        sourced_output = temp / "example-test-divorce-core.docx"
        sourced_input.write_text(json.dumps(sourced_manifest), encoding="utf-8")
        ok, code = run_positive_pipeline(
            "positive-sourced-structural",
            [
                ["node", str(builder), str(sourced_input), str(sourced_output)],
                [sys.executable, str(structural), str(sourced_output), "--manifest", str(sourced_input)],
            ],
            "PASS: Supported deterministic Core Hub checks cleared.",
            evidence_dir,
        )
        positive_results.append(("Nine sources remain allowed and use the 12 pt Sources contract", ok, code, "PASS: Supported deterministic Core Hub checks cleared."))

        misordered_sources = json.loads(json.dumps(sourced_manifest))
        misordered_sources["sources"][0], misordered_sources["sources"][1] = (
            misordered_sources["sources"][1],
            misordered_sources["sources"][0],
        )
        for block in misordered_sources["content"]:
            items = [{"runs": block.get("runs") or []}] if block.get("type") == "p" else block.get("items") or []
            for item in items:
                for run in item.get("runs") or []:
                    if run.get("citation_id") == "format-source-1":
                        run["text"] = "[2]"
                    elif run.get("citation_id") == "format-source-2":
                        run["text"] = "[1]"
        misordered_input = temp / "misordered-sources.json"
        misordered_output = temp / "example-misordered-divorce-core.docx"
        misordered_input.write_text(json.dumps(misordered_sources), encoding="utf-8")
        ok, code = run_case(
            "negative-generator-citation-first-appearance",
            ["node", str(builder), str(misordered_input), str(misordered_output)],
            "Sources must be ordered by first in-body citation appearance",
            evidence_dir,
        )
        results.append(("Sources declared outside first-appearance order are rejected", ok, code, "Sources must be ordered by first in-body citation appearance"))

        swapped_citation_targets = temp / "example-swapped-citation-targets-divorce-core.docx"
        rewrite_member(
            sourced_output,
            swapped_citation_targets,
            "word/document.xml",
            swap_first_two_body_citation_targets,
        )
        ok, code = run_case(
            "negative-structural-citation-target-order",
            [sys.executable, str(structural), str(swapped_citation_targets), "--manifest", str(sourced_input)],
            "In-body citation hyperlinks must appear in [1] through [N] order and target the matching source URL",
            evidence_dir,
        )
        results.append(("Swapped citation hyperlink targets are rejected", ok, code, "In-body citation hyperlinks must appear in [1] through [N] order and target the matching source URL"))

        bad_source_size = temp / "example-bad-divorce-core.docx"
        rewrite_member(
            sourced_output,
            bad_source_size,
            "word/document.xml",
            lambda payload: set_source_run_size(payload, "22"),
        )
        ok, code = run_case(
            "negative-structural-source-font-size",
            [sys.executable, str(structural), str(bad_source_size), "--manifest", str(sourced_input)],
            "Sources text must use 12 pt body size",
            evidence_dir,
        )
        results.append(("Eleven-point Sources entry rejected", ok, code, "Sources text must use 12 pt body size"))

        stale_render_dir = temp / "stale-render"
        stale_render_dir.mkdir()
        (stale_render_dir / "page-99.png").write_bytes(b"stale regression marker")
        ok, code = run_case(
            "negative-renderer-stale-output-directory",
            [str(renderer), str(positive), "--output_dir", str(stale_render_dir), "--dpi", "144"],
            "Render output directory must be absent or empty",
            evidence_dir,
        )
        results.append(("Renderer rejects a stale output directory", ok, code, "Render output directory must be absent or empty"))

    summary_lines = [
        "# Core Hub Validator Test Summary",
        "",
        "Intentionally broken documents were created only in a temporary directory and removed after execution.",
        "",
        "## Positive fixture",
        "",
        "| Case | Expected pass observed | Exit | Required marker |",
        "|---|---|---:|---|",
    ]
    for label, passed, code, marker in positive_results:
        summary_lines.append(f"| {label} | {'Yes' if passed else 'No'} | {code} | `{marker}` |")
    summary_lines.extend(
        [
            "",
            "## Meaningful negative fixtures",
            "",
        "| Case | Expected failure observed | Exit | Required marker |",
        "|---|---|---:|---|",
        ]
    )
    for label, passed, code, marker in results:
        summary_lines.append(f"| {label} | {'Yes' if passed else 'No'} | {code} | `{marker}` |")
    summary_lines.extend(
        [
            "",
            "These tests demonstrate only the named mechanical detections. They do not evaluate legal accuracy, editorial quality, strategy, or rendered layout.",
            "",
        ]
    )
    (evidence_dir / "negative-test-summary.md").write_text("\n".join(summary_lines), encoding="utf-8")

    failed = [label for label, passed, _code, _marker in positive_results + results if not passed]
    if failed:
        print("FAILED negative tests:")
        for label in failed:
            print(f"  - {label}")
        return 1
    print(
        f"PASS: {len(positive_results)} positive checks passed and "
        f"{len(results)} meaningful negative cases produced their required failures."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
