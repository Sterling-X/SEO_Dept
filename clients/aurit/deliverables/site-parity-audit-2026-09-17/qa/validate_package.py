#!/usr/bin/env python3
"""Offline consistency checks for the Aurit parity-audit handoff."""

from __future__ import annotations

import collections
import json
import pathlib
import zipfile
from xml.etree import ElementTree


QA_DIR = pathlib.Path(__file__).resolve().parent
DELIVERABLE_DIR = QA_DIR.parent
REPO_ROOT = pathlib.Path(__file__).resolve().parents[5]
JSON_PATH = DELIVERABLE_DIR / "data" / "crawl-comparison.json"
REPORT_PATH = DELIVERABLE_DIR / "aurit-full-site-parity-audit.md"
TECHNICAL_PATH = DELIVERABLE_DIR / "technical-crawl-appendix.md"
WORKBOOK_PATH = (
    REPO_ROOT
    / "outputs"
    / "aurit-parity-audit-2026-09-17"
    / "aurit-full-site-parity-audit.xlsx"
)

EXPECTED_COUNTS = {
    "mapped": 170,
    "exact": 0,
    "near_match": 1,
    "changed": 169,
    "staging_only": 5,
    "live_only": 22,
}
EXPECTED_SHEETS = [
    "Summary",
    "Page Comparison",
    "Field Changes",
    "URL Gaps",
    "Broken Links",
    "Redirects",
    "Cross-Environment",
    "Orphan-Like",
    "Rendered QA",
    "URL Inventory",
    "Methodology",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def direct_page_count(site: dict[str, object]) -> int:
    return sum(
        page.get("status") == 200
        and bool(page.get("is_html"))
        and page.get("redirect_count") == 0
        for page in site["pages"]
    )


def check_json() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    require(data["comparison"]["counts"] == EXPECTED_COUNTS, "comparison counts changed")
    require(direct_page_count(data["live"]) == 192, "live direct-page count changed")
    require(direct_page_count(data["staging"]) == 175, "staging direct-page count changed")
    require(data["live"]["sitemaps"]["unique_url_count"] == 189, "live sitemap count changed")
    require(data["staging"]["sitemaps"]["unique_url_count"] == 171, "staging sitemap count changed")
    methods = collections.Counter(
        match["mapping_method"] for match in data["comparison"]["matches"]
    )
    require(methods == {"exact-path": 161, "unique-slug": 9}, "mapping mix changed")
    for name in ("live", "staging"):
        closure = data[name]["graph_closure"]
        require(closure["closed"], f"{name} graph is not closed")
        require(
            closure["unrecorded_internal_targets"] == [],
            f"{name} has unrecorded internal targets",
        )


def check_markdown() -> None:
    report = REPORT_PATH.read_text(encoding="utf-8")
    technical = TECHNICAL_PATH.read_text(encoding="utf-8")
    for expected in (
        "170 mapped direct-page pairs",
        "169 are mechanically changed",
        "22 live-only",
        "5 staging-only",
        "Across the 161 same-path direct pages, 86 titles differ",
        "Sixty-eight direct, indexable staging sitemap URLs had zero inlinks in the static discovered corpus versus ten on live",
    ):
        require(expected in report, f"report control missing: {expected}")
    for expected in (
        "- Graph closure: closed",
        "- Unrecorded same-host internal targets: 0",
        "- Internally linked final-404 targets: 25",
        "- Internally linked final-404 targets: 9",
        "- Orphan-like direct/indexable sitemap pages: 68",
        "- Orphan-like direct/indexable sitemap pages: 10",
    ):
        require(expected in technical, f"technical control missing: {expected}")


def check_workbook() -> None:
    require(WORKBOOK_PATH.is_file(), "workbook is missing")
    spreadsheet_namespace = {
        "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    }
    with zipfile.ZipFile(WORKBOOK_PATH) as archive:
        require(archive.testzip() is None, "workbook ZIP CRC check failed")
        workbook_xml = ElementTree.fromstring(archive.read("xl/workbook.xml"))
        sheets = workbook_xml.find("m:sheets", spreadsheet_namespace)
        require(sheets is not None, "workbook sheet list missing")
        names = [sheet.attrib["name"] for sheet in sheets]
        require(names == EXPECTED_SHEETS, "workbook sheet order changed")
        table_files = [
            name
            for name in archive.namelist()
            if name.startswith("xl/tables/table") and name.endswith(".xml")
        ]
        require(len(table_files) == 10, "workbook table count changed")
        formula_count = 0
        pane_count = 0
        formula_errors = (
            b"#REF!",
            b"#DIV/0!",
            b"#VALUE!",
            b"#NAME?",
            b"#N/A",
            b"#NUM!",
            b"#NULL!",
            b"#SPILL!",
            b"#CALC!",
        )
        for name in archive.namelist():
            if not (name.startswith("xl/worksheets/sheet") and name.endswith(".xml")):
                continue
            content = archive.read(name)
            require(not any(error in content for error in formula_errors), f"formula error in {name}")
            root = ElementTree.fromstring(content)
            formula_count += len(root.findall(".//m:f", spreadsheet_namespace))
            pane_count += len(root.findall(".//m:pane", spreadsheet_namespace))
        require(formula_count == 11, "workbook formula count changed")
        require(pane_count >= 10, "expected frozen panes are missing")


def main() -> None:
    check_json()
    check_markdown()
    check_workbook()
    print("PASS: JSON, report, technical appendix, and XLSX controls reconcile")


if __name__ == "__main__":
    main()
