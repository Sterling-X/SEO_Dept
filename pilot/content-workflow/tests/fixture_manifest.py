#!/usr/bin/env python3
"""Synthetic FL-M008 generator manifests for the readiness tests (fixture only).

Builds on the candidate skill's own production-shaped synthetic manifest so the fixture
exercises the real generator and validators. Every value is invented: the client
"Gómez & Núñez Family Law, P.A." (accented on purpose), the jurisdiction "Exampleland", the
statutes, and the URLs. v0 carries the two defects the fixture reviews raise (an absolute legal
claim, a missing approved role descriptor); v1 is the revised draft.
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PILOT_ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = PILOT_ROOT / "candidates" / "skills" / "family-law-situational-pages-pilot-v1"
_spec = importlib.util.spec_from_file_location("candidate_test_situational", CANDIDATE / "scripts" / "test-situational.py")
_harness = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_harness)

FIRM = "Gómez & Núñez Family Law, P.A."
CLIENT_HOST = "https://gomez-nunez-law.example"
SOURCES = [
    {"id": 1, "label": "Exampleland Stat. § 12.345, Dissolution of marriage", "url": "https://legislature.exampleland.example/statutes/12.345"},
    {"id": 2, "label": "Exampleland Stat. § 12.350, Parenting time", "url": "https://legislature.exampleland.example/statutes/12.350"},
    {"id": 3, "label": "Exampleland Family Court Rule 7, Case management", "url": "https://courts.exampleland.example/rules/family/7"},
]
REPEAT_CLAIM = "Written findings on the parenting schedule also shape how any later request to change it is judged."
STAKES_V0 = "Courts in Exampleland must always order equal parenting time, so the schedule is not something you can influence."
STAKES_V1 = "Courts in Exampleland start from a presumption of equal parenting time, but a parent can rebut it with evidence and the court must make written findings."
FIRM_HELP_V0 = f"{FIRM} represents people in high-conflict divorce matters in Exampleland. María Gómez-Núñez builds a plan around the pattern in your case: what to document, what to stop responding to, and which requests belong in front of the court."
FIRM_HELP_V1 = f"{FIRM} represents people in high-conflict divorce matters in Exampleland. María Gómez-Núñez, the founder and managing attorney, builds a plan around the pattern in your case: what to document, what to stop responding to, and which requests belong in front of the court."


def _text(text: str) -> dict:
    return {"type": "text", "text": text}


def _cite(source_id: int) -> list[dict]:
    return [_text(" "), {"type": "citation", "source_id": source_id, "text": f"[{source_id}]"}]


def base_manifest() -> dict:
    manifest = _harness.production_shaped_manifest()
    manifest["meta"].update({
        "firm_name": FIRM,
        "jurisdiction": "Exampleland",
        "voice_source": "sources/voice-brief.md (approved voice brief; domain unrouted)",
        "client_url": f"{CLIENT_HOST}/divorce/high-conflict-divorce/",
        "canonical_url": f"{CLIENT_HOST}/divorce/high-conflict-divorce/",
        "title_tag": "Exampleland High-Conflict Divorce Lawyer | Gómez & Núñez",
        "meta_description": "High-conflict divorce requires a focused plan. Learn how Exampleland handles parenting, financial, and safety disputes, and how Gómez & Núñez Family Law can help.",
        "cms_title": "High-Conflict Divorce in Exampleland",
        "social_title": "Exampleland High-Conflict Divorce Lawyer | Gómez & Núñez",
        "social_description": "Synthetic fixture metadata for the content-workflow pilot tests.",
        "h1": "High-Conflict Divorce in Exampleland",
    })
    for link in manifest["link_manifest"]:
        link["client_url"] = link["client_url"].replace("https://example.com/proposed", CLIENT_HOST).replace("https://example.com", CLIENT_HOST)
    manifest["sources"] = [
        {**source, "authority": "official-primary", "status": 200, "verified_on": "2026-09-23", "verification_evidence": "SYNTHETIC FIXTURE; nothing was fetched"}
        for source in SOURCES
    ]
    content = manifest["content"]
    # The harness placed [1] after the first stakes paragraph and [2] two paragraphs into strategy;
    # move [1] into the opening, put the stakes claim under [2], and add [3] in strategy.
    for block in content:
        for run_list in ([block.get("runs")] if block.get("type") == "p" else [item.get("runs") for item in block.get("items", [])]):
            if run_list:
                block_runs = [r for r in run_list if r.get("type") != "citation"]
                if block_runs and block_runs[-1].get("type") == "text" and block_runs[-1]["text"] == " ":
                    block_runs.pop()
                run_list[:] = block_runs
    content[0]["runs"].extend(_cite(1))
    stakes_index = next(i for i, b in enumerate(content) if b.get("type") == "h2" and b.get("role") == "stakes")
    content[stakes_index + 1]["runs"] = [_text(STAKES_V0), *_cite(2)]
    strategy_index = next(i for i, b in enumerate(content) if b.get("type") == "h2" and b.get("role") == "strategy")
    content[strategy_index + 1]["runs"] = [_text("Ask the court for a case-management order that sets communication and disclosure requirements early."), *_cite(3)]
    firm_index = next(i for i, b in enumerate(content) if b.get("type") == "h2" and b.get("role") == "firm-help")
    content[firm_index + 1]["runs"] = [_text(FIRM_HELP_V0)]
    # A later material claim supported by the same authority reuses source number 2 (repeated citation).
    content[strategy_index + 3]["runs"] = [_text(REPEAT_CLAIM), *_cite(2)]
    manifest["quality_contract"] = {"forbidden_terms": ["collaborative divorce", "Sterling Lawyers"]}
    return manifest


def manifest_v0() -> dict:
    return base_manifest()


def manifest_v1() -> dict:
    manifest = base_manifest()
    for block in manifest["content"]:
        for run in block.get("runs", []):
            if run.get("type") == "text" and run["text"] == STAKES_V0:
                run["text"] = STAKES_V1
            if run.get("type") == "text" and run["text"] == FIRM_HELP_V0:
                run["text"] = FIRM_HELP_V1
    return manifest


def inject_text(manifest: dict, needle: str, replacement: str) -> dict:
    manifest = copy.deepcopy(manifest)
    hits = 0
    for block in manifest["content"]:
        for run in block.get("runs", []):
            if run.get("type") == "text" and needle in run["text"]:
                run["text"] = run["text"].replace(needle, replacement)
                hits += 1
    if not hits:
        raise ValueError(f"needle not found: {needle!r}")
    return manifest
