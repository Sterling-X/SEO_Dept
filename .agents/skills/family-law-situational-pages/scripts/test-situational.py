#!/usr/bin/env python3
"""LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL.

Focused positive and negative regression tests for the demonstrated FL-M008
Situational generator and validators. Test artifacts live in a temporary
directory and are removed automatically.
"""

from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


sys.dont_write_bytecode = True
SKILL_ROOT = Path(__file__).resolve().parent.parent
BUILD = SKILL_ROOT / "scripts" / "build-situational.js"
STRUCTURAL = SKILL_ROOT / "scripts" / "office" / "validate.py"
PAGE = SKILL_ROOT / "scripts" / "validate-page.js"


def paragraph(text: str) -> dict:
    return {"type": "p", "runs": [{"type": "text", "text": text}]}


def synthetic_manifest(with_v2_link: bool = False) -> dict:
    repeated = (
        "This synthetic paragraph tests situational document structure, readable spacing, "
        "manifest fidelity, and validation without making any client or legal claim."
    )
    content: list[dict] = [
        paragraph(
            "A high-conflict divorce can require clearer records, structured communication, "
            "and focused decisions in this synthetic mechanical test."
        ),
        paragraph(
            "This fixture demonstrates page-role separation and contains no statement about "
            "a real client, jurisdiction, service, or legal rule."
        ),
    ]
    sections = [
        ("scenario", "Recognizing the high-conflict situation"),
        ("stakes", "Keeping the page focused on scenario stakes"),
        ("strategy", "Building a structured response"),
        ("evidence", "Organizing reliable information"),
        ("firm-help", "How a hypothetical firm-help section is structured"),
        ("cta", "A bounded next step"),
    ]
    for role, heading in sections:
        content.append({"type": "h2", "role": role, "text": heading})
        content.extend(paragraph(repeated) for _ in range(9))

    manifest = {
        "schema_version": 2,
        "workflow": "situational-fl-m008-local-replacement",
        "meta": {
            "synthetic_fixture": True,
            "architecture_node_id": "FL-M008",
            "v2_reference_path": "/divorce/high-conflict-divorce/",
            "v2_page_type": "Practice-Area Situational Page",
            "v2_role": "Situational",
            "v2_brief_type": "Situation / Use-Case Brief",
            "v2_word_count_target": "1,100–1,700",
            "client_url": "https://example.com/proposed/high-conflict-divorce/",
            "canonical_url": "https://example.com/proposed/high-conflict-divorce/",
            "url_retention_decision": "retain-existing",
            "voice_source": "synthetic-fixture",
            "title_tag": "Synthetic High-Conflict Divorce Test",
            "meta_description": "Synthetic metadata used only to verify the local document workflow without making a client, service, or legal claim.",
            "cms_title": "Synthetic High-Conflict Divorce Test",
            "social_title": "Synthetic High-Conflict Divorce Test",
            "social_description": "Synthetic social metadata used only to verify local document mechanics.",
            "h1": "Synthetic High-Conflict Divorce Test",
            "robots": "index, follow",
            "media_note": "Synthetic media note; no asset is proposed.",
            "situational_purpose": "Test scenario-specific document mechanics without evaluating substantive content.",
            "excluded_intents": ["general-divorce-hub", "contested-divorce-procedure"],
        },
        "link_inventory": {"status": "synthetic-fixture"},
        "link_manifest": [
            {
                "id": "link-parent",
                "supporting_authority": "skill-parent-navigation",
                "source_node_id": "FL-M008",
                "target_node_id": "FL-PA-DIV",
                "v2_reference_path": "/divorce/",
                "client_url": "https://example.com/proposed/divorce/",
                "client_url_status": 200,
                "client_url_redirects": 0,
                "client_url_verified_on": "2026-09-16",
                "client_url_evidence": "Synthetic direct-route fixture; no real availability claim.",
                "destination_fit": "verified",
                "anchor": "synthetic divorce hub",
                "placement": "opening",
            },
            {
                "id": "link-process",
                "supporting_authority": "skill-process-bridge",
                "source_node_id": "FL-M008",
                "target_node_id": "FL-M004",
                "v2_reference_path": "/divorce/contested-divorce/",
                "client_url": "https://example.com/proposed/contested-divorce/",
                "client_url_status": 200,
                "client_url_redirects": 0,
                "client_url_verified_on": "2026-09-16",
                "client_url_evidence": "Synthetic direct-route fixture; no real availability claim.",
                "destination_fit": "verified",
                "anchor": "synthetic contested-divorce process",
                "placement": "scenario",
            },
            {
                "id": "link-cta",
                "supporting_authority": "consultation-cta",
                "source_node_id": "FL-M008",
                "destination_kind": "consultation-contact",
                "client_url": "https://example.com/contact/",
                "client_url_status": 200,
                "client_url_redirects": 0,
                "client_url_verified_on": "2026-09-16",
                "client_url_evidence": "Synthetic direct-route fixture; no real availability claim.",
                "destination_fit": "verified",
                "anchor": "synthetic consultation invitation",
                "placement": "cta",
            },
        ],
        "quality_contract": {"forbidden_terms": ["collaborative divorce"]},
        "content": content,
        "sources": [],
    }
    manifest["content"][0]["runs"] = [
        {"type": "text", "text": "A high-conflict divorce mechanical test can include a contextual "},
        {"type": "internal_link", "link_id": "link-parent", "text": "synthetic divorce hub"},
        {"type": "text", "text": " link while preserving its distinct situational role."},
    ]
    scenario_index = next(
        index for index, block in enumerate(manifest["content"])
        if block.get("type") == "h2" and block.get("role") == "scenario"
    )
    manifest["content"][scenario_index + 1]["runs"] = [
        {"type": "text", "text": "This synthetic distinction can bridge to a "},
        {"type": "internal_link", "link_id": "link-process", "text": "synthetic contested-divorce process"},
        {"type": "text", "text": " without replacing the scenario page's purpose."},
    ]
    manifest["content"][-1]["runs"] = [
        {"type": "text", "text": "The final synthetic next step is a "},
        {"type": "internal_link", "link_id": "link-cta", "text": "synthetic consultation invitation"},
        {"type": "text", "text": " after the CTA heading."},
    ]

    if with_v2_link:
        link = {
            "id": "link-default",
            "supporting_authority": "v2-explicit-relationship",
            "source_node_id": "FL-M008",
            "target_node_id": "FL-M010",
            "v2_edge_id": "CL-00068",
            "v2_reference_path": "/divorce/default-divorce/",
            "client_url": "https://example.com/proposed/default-divorce/",
            "client_url_status": 200,
            "client_url_redirects": 0,
            "client_url_verified_on": "2026-09-16",
            "client_url_evidence": "Synthetic direct-route fixture; no real availability claim.",
            "destination_fit": "verified",
            "anchor": "a synthetic default-divorce destination",
            "placement": "strategy",
        }
        manifest["link_manifest"].append(link)
        strategy_index = next(
            index for index, block in enumerate(manifest["content"])
            if block.get("type") == "h2" and block.get("role") == "strategy"
        )
        manifest["content"][strategy_index + 1]["runs"] = [
            {"type": "text", "text": "A synthetic mechanical test can include "},
            {"type": "internal_link", "link_id": "link-default", "text": link["anchor"]},
            {"type": "text", "text": " when an exact outgoing V2 edge and destination evidence are present."},
        ]
    return manifest


def manifested_link(manifest: dict, link_id: str) -> dict:
    return next(link for link in manifest["link_manifest"] if link["id"] == link_id)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def write_manifest(directory: Path, manifest: dict, name: str = "input.json") -> Path:
    target = directory / name
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return target


def generate_and_validate(directory: Path, manifest: dict) -> tuple[bool, str, Path, Path]:
    manifest_path = write_manifest(directory, manifest)
    docx_path = directory / "synthetic-high-conflict-divorce-situational.docx"
    commands = [
        ["node", str(BUILD), str(manifest_path), str(docx_path)],
        [sys.executable, str(STRUCTURAL), str(docx_path), "--manifest", str(manifest_path)],
        ["node", str(PAGE), str(docx_path), "--manifest", str(manifest_path)],
    ]
    output: list[str] = []
    for command in commands:
        completed = run(command)
        output.append(f"$ {' '.join(command)}\nexit={completed.returncode}\n{completed.stdout}")
        if completed.returncode != 0:
            return False, "\n".join(output), docx_path, manifest_path
    return True, "\n".join(output), docx_path, manifest_path


def expect_generator_failure(directory: Path, name: str, manifest: dict, marker: str) -> tuple[bool, str]:
    manifest_path = write_manifest(directory, manifest, f"{name}.json")
    docx_path = directory / "synthetic-high-conflict-divorce-situational.docx"
    completed = run(["node", str(BUILD), str(manifest_path), str(docx_path)])
    passed = completed.returncode != 0 and marker in completed.stdout
    return passed, completed.stdout


def rewrite_docx(source: Path, destination: Path, member: str, transform) -> None:
    with zipfile.ZipFile(source, "r") as reader, zipfile.ZipFile(destination, "w") as writer:
        for info in reader.infolist():
            payload = reader.read(info.filename)
            if info.filename == member:
                payload = transform(payload)
            writer.writestr(info, payload)


def set_paragraph_style_size(payload: bytes, style_id: str, size: str) -> bytes:
    namespace = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    from xml.etree import ElementTree as ET

    root = ET.fromstring(payload)
    style = root.find(f".//{{{namespace}}}style[@{{{namespace}}}styleId='{style_id}']")
    if style is None:
        raise RuntimeError(f"Style {style_id!r} was not found for size mutation.")
    run_properties = style.find(f"{{{namespace}}}rPr")
    if run_properties is None:
        run_properties = ET.SubElement(style, f"{{{namespace}}}rPr")
    size_node = run_properties.find(f"{{{namespace}}}sz")
    if size_node is None:
        size_node = ET.SubElement(run_properties, f"{{{namespace}}}sz")
    size_node.set(f"{{{namespace}}}val", size)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main() -> int:
    results: list[tuple[str, bool, str]] = []
    with tempfile.TemporaryDirectory(prefix="fl-m008-workflow-") as raw_temp:
        root = Path(raw_temp)

        required_dir = root / "positive-required-navigation"
        required_dir.mkdir()
        passed, output, positive_docx, positive_manifest = generate_and_validate(
            required_dir, synthetic_manifest(False)
        )
        results.append(("positive-required-navigation-authorities", passed, output))

        link_dir = root / "positive-v2-link"
        link_dir.mkdir()
        passed, output, _v2_docx, _v2_manifest = generate_and_validate(link_dir, synthetic_manifest(True))
        results.append(("positive-additional-exact-v2-link", passed, output))

        base = synthetic_manifest(False)

        parent = copy.deepcopy(base)
        parent_link = manifested_link(parent, "link-parent")
        parent_link["supporting_authority"] = "v2-explicit-relationship"
        parent_link["v2_edge_id"] = "CL-00037"
        passed, output = expect_generator_failure(
            root, "negative-parent-as-v2-edge", parent,
            "is not an exact outgoing V2 relationship from FL-M008 to FL-PA-DIV",
        )
        results.append(("negative-parent-falsely-labeled-v2-edge", passed, output))

        contested = copy.deepcopy(base)
        contested_link = manifested_link(contested, "link-process")
        contested_link["supporting_authority"] = "v2-explicit-relationship"
        contested_link["v2_edge_id"] = "CL-00033"
        passed, output = expect_generator_failure(
            root, "negative-process-as-v2-edge", contested,
            "is not an exact outgoing V2 relationship from FL-M008 to FL-M004",
        )
        results.append(("negative-process-falsely-labeled-v2-edge", passed, output))

        missing_authority = copy.deepcopy(base)
        del manifested_link(missing_authority, "link-process")["supporting_authority"]
        passed, output = expect_generator_failure(
            root, "negative-missing-authority", missing_authority, "supporting_authority must be one of",
        )
        results.append(("negative-missing-authority", passed, output))

        wrong_authority = copy.deepcopy(base)
        manifested_link(wrong_authority, "link-process")["supporting_authority"] = "inferred-v2-link"
        passed, output = expect_generator_failure(
            root, "negative-unknown-authority", wrong_authority, "supporting_authority must be one of",
        )
        results.append(("negative-unknown-authority", passed, output))

        wrong_parent = copy.deepcopy(base)
        manifested_link(wrong_parent, "link-parent").update({
            "target_node_id": "FL-M010",
            "v2_reference_path": "/divorce/default-divorce/",
        })
        passed, output = expect_generator_failure(
            root, "negative-wrong-parent", wrong_parent,
            "skill-parent-navigation must target the actual V2 parent FL-PA-DIV",
        )
        results.append(("negative-wrong-parent-target", passed, output))

        parent_edge = copy.deepcopy(base)
        manifested_link(parent_edge, "link-parent")["v2_edge_id"] = "CL-00037"
        passed, output = expect_generator_failure(
            root, "negative-parent-edge-field", parent_edge,
            "skill-parent-navigation must omit v2_edge_id",
        )
        results.append(("negative-parent-invents-v2-edge", passed, output))

        wrong_process = copy.deepcopy(base)
        manifested_link(wrong_process, "link-process").update({
            "target_node_id": "FL-M010",
            "v2_reference_path": "/divorce/default-divorce/",
        })
        passed, output = expect_generator_failure(
            root, "negative-wrong-process", wrong_process,
            "skill-process-bridge must target FL-M004 under the same parent",
        )
        results.append(("negative-wrong-process-target", passed, output))

        process_edge = copy.deepcopy(base)
        manifested_link(process_edge, "link-process")["v2_edge_id"] = "CL-00033"
        passed, output = expect_generator_failure(
            root, "negative-process-edge-field", process_edge,
            "skill-process-bridge must omit v2_edge_id",
        )
        results.append(("negative-process-invents-v2-edge", passed, output))

        cta_v2 = copy.deepcopy(base)
        manifested_link(cta_v2, "link-cta").update({
            "target_node_id": "FL-PA-DIV",
            "v2_reference_path": "/divorce/",
            "v2_edge_id": "CL-00037",
        })
        passed, output = expect_generator_failure(
            root, "negative-cta-v2-fields", cta_v2,
            "consultation-cta must omit target_node_id; it is not a V2 relationship",
        )
        results.append(("negative-cta-carries-v2-fields", passed, output))

        cta_kind = copy.deepcopy(base)
        manifested_link(cta_kind, "link-cta")["destination_kind"] = "v2-node"
        passed, output = expect_generator_failure(
            root, "negative-cta-kind", cta_kind,
            "consultation-cta must set destination_kind to consultation-contact",
        )
        results.append(("negative-cta-destination-kind", passed, output))

        empty = copy.deepcopy(base)
        empty["link_manifest"] = []
        for block in empty["content"]:
            for content_run in block.get("runs", []):
                if content_run.get("type") == "internal_link":
                    content_run.update({"type": "text"})
                    content_run.pop("link_id", None)
        passed, output = expect_generator_failure(
            root, "negative-empty-required-navigation", empty,
            "FL-M008 requires exactly one skill-parent-navigation link; found 0",
        )
        results.append(("negative-empty-required-navigation", passed, output))

        hold = synthetic_manifest(True)
        hold_link = manifested_link(hold, "link-default")
        hold_link.update({
            "target_node_id": "FL-M013",
            "v2_edge_id": "CL-00071",
            "v2_reference_path": "/divorce/summary-dissolution/",
            "client_url": "https://example.com/proposed/summary-dissolution/",
        })
        passed, output = expect_generator_failure(
            root, "negative-hold-target", hold, "cannot activate while its V2 gate is HOLD",
        )
        results.append(("negative-hold-target", passed, output))

        unverified = copy.deepcopy(base)
        manifested_link(unverified, "link-parent")["destination_fit"] = "unknown"
        passed, output = expect_generator_failure(
            root, "negative-unverified", unverified,
            "destination must be a verified right-service direct 200 with zero redirects",
        )
        results.append(("negative-unverified-destination", passed, output))

        duplicate_url = copy.deepcopy(base)
        manifested_link(duplicate_url, "link-process")["client_url"] = manifested_link(
            duplicate_url, "link-parent"
        )["client_url"]
        passed, output = expect_generator_failure(
            root, "negative-duplicate-url", duplicate_url, "duplicate client destination URL",
        )
        results.append(("negative-duplicate-manifest-url", passed, output))

        early_cta = copy.deepcopy(base)
        for block in early_cta["content"]:
            for content_run in block.get("runs", []):
                if content_run.get("type") == "internal_link" and content_run.get("link_id") == "link-cta":
                    content_run.update({"type": "text"})
                    content_run.pop("link_id", None)
        early_cta["content"][1]["runs"].extend([
            {"type": "text", "text": " A premature "},
            {"type": "internal_link", "link_id": "link-cta", "text": "synthetic consultation invitation"},
            {"type": "text", "text": " appears here."},
        ])
        passed, output = expect_generator_failure(
            root, "negative-early-cta", early_cta,
            "consultation CTA must appear after the final role=cta H2",
        )
        results.append(("negative-cta-before-final-section", passed, output))

        contamination = copy.deepcopy(base)
        contamination["meta"]["meta_description"] += " Collaborative divorce appears here."
        passed, output = expect_generator_failure(
            root, "negative-contamination", contamination, "Forbidden content term remains: collaborative divorce",
        )
        results.append(("negative-forbidden-contamination", passed, output))

        if positive_docx.exists():
            no_styles = root / "synthetic-high-conflict-divorce-situational.docx"
            with zipfile.ZipFile(positive_docx, "r") as reader, zipfile.ZipFile(no_styles, "w") as writer:
                for info in reader.infolist():
                    if info.filename != "word/styles.xml":
                        writer.writestr(info, reader.read(info.filename))
            completed = run([sys.executable, str(STRUCTURAL), str(no_styles), "--manifest", str(positive_manifest)])
            results.append((
                "negative-missing-styles",
                completed.returncode != 0 and "Required OOXML part is missing: word/styles.xml" in completed.stdout,
                completed.stdout,
            ))

            duplicate = root / "duplicate" / "synthetic-high-conflict-divorce-situational.docx"
            duplicate.parent.mkdir()

            def duplicate_link(payload: bytes) -> bytes:
                match = re.search(rb"(<w:hyperlink\b[\s\S]*?</w:hyperlink>)", payload)
                if not match:
                    raise RuntimeError("No hyperlink was available for duplicate-link mutation.")
                return payload[:match.end()] + match.group(1) + payload[match.end():]

            rewrite_docx(positive_docx, duplicate, "word/document.xml", duplicate_link)
            completed = run(["node", str(PAGE), str(duplicate), "--manifest", str(positive_manifest)])
            results.append((
                "negative-duplicate-internal-link",
                completed.returncode != 0 and "internal destination must appear exactly once" in completed.stdout,
                completed.stdout,
            ))

            nine_point = root / "source-nine-point" / "synthetic-high-conflict-divorce-situational.docx"
            nine_point.parent.mkdir()
            rewrite_docx(
                positive_docx,
                nine_point,
                "word/styles.xml",
                lambda payload: set_paragraph_style_size(payload, "Source", "18"),
            )
            completed = run([
                sys.executable,
                str(STRUCTURAL),
                str(nine_point),
                "--manifest",
                str(positive_manifest),
            ])
            results.append((
                "negative-nine-point-source-style",
                completed.returncode != 0 and "Source must use Arial 12 pt" in completed.stdout,
                completed.stdout,
            ))

    failed = [name for name, passed, _output in results if not passed]
    for name, passed, output in results:
        print(f"{'PASS' if passed else 'FAIL'}: {name}")
        if not passed:
            print(output)
    if failed:
        print(f"FAIL: {len(failed)} regression case(s): {', '.join(failed)}")
        return 1
    print(f"PASS: {len(results)} FL-M008 local workflow regression cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
