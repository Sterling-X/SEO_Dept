#!/usr/bin/env python3
"""Route likely substantive SEO prompts to shared lesson headings.

This hook is deliberately read-only. It does not log prompts, read transcripts or
client files, invoke agents, decide that a lesson applies, or persist a lesson.
Any behavior change must use a new versioned filename and update the trusted hook
definition instead of modifying this helper in place after trust.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


CONTEXT_CUES = {
    "seo", "search", "ranking", "keyword", "crawl", "index", "canonical",
    "content", "page", "site", "website", "metadata", "internal", "link",
    "local", "conversion", "lead", "client", "architecture", "cluster",
    "family", "divorce", "workflow", "reviewer", "learning", "lesson",
    "skill", "deliverable", "docx", "attribution", "migration",
}
ACTION_CUES = {
    "audit", "assess", "build", "change", "complete", "create", "diagnose",
    "draft", "evaluate", "implement", "optimize", "plan", "prioritize",
    "produce", "recommend", "reconcile", "repair", "review", "revise",
    "strategy", "update", "verify", "workflow", "write",
}
MINOR_PATTERNS = (
    re.compile(r"^what (?:is|does) seo\??$", re.IGNORECASE),
    re.compile(r"^(?:define|explain) seo\.?$", re.IGNORECASE),
)
SOURCE_SPECS = (
    (
        ".agents/skills/recursive-self-improvement/references/learning-records.md",
        {3},
    ),
    ("docs/seo-skill-local-adaptations.md", {2}),
)
STOPWORDS = {
    "about", "after", "again", "against", "also", "before", "being", "between",
    "from", "have", "into", "only", "other", "should", "their", "there", "these",
    "this", "through", "using", "with", "without", "your",
}
ROUTING_STOPWORDS = STOPWORDS | ACTION_CUES | {
    "adaptation", "candidate", "client", "content", "correction", "current",
    "learning", "lesson", "local", "page", "record", "review", "reviewer",
    "site", "skill", "verification", "website", "workflow",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) >= 3 and token not in STOPWORDS
    }


def _is_likely_substantive(prompt: str) -> bool:
    cleaned = " ".join(prompt.split())
    if not cleaned or len(cleaned) > 100_000:
        return False
    if any(pattern.fullmatch(cleaned) for pattern in MINOR_PATTERNS):
        return False
    tokens = _tokens(cleaned)
    return bool(tokens & CONTEXT_CUES) and bool(tokens & ACTION_CUES)


def _headings(path: Path, levels: set[int]) -> list[tuple[str, str]]:
    if not path.is_file():
        return []
    results: list[tuple[str, str]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if match and len(match.group(1)) in levels:
            title = re.sub(r"[`*_]", "", match.group(2)).strip()
            results.append((title[:160], f"{path.as_posix()}:{line_number}"))
    return results


def _candidate_headings(root: Path, prompt: str, limit: int = 4) -> list[tuple[str, str]]:
    prompt_tokens = _tokens(prompt) - ROUTING_STOPWORDS
    candidates: list[tuple[int, str, str]] = []
    for relative_path, levels in SOURCE_SPECS:
        source = root / relative_path
        for title, location in _headings(source, levels):
            overlap = prompt_tokens & (_tokens(title) - ROUTING_STOPWORDS)
            if overlap:
                candidates.append((len(overlap), title, location.replace(f"{root.as_posix()}/", "")))
    candidates.sort(key=lambda item: (-item[0], item[2], item[1].lower()))
    return [(title, location) for _, title, location in candidates[:limit]]


def _build_context(root: Path, prompt: str) -> str:
    candidates = _candidate_headings(root, prompt)
    lines = [
        "SEO learning-loop checkpoint (candidate routing only; AGENTS.md remains authoritative).",
        "Before a substantive decision, open only the owning records that match the task and confirm each lesson's scope and state. Candidate headings are pointers, not proof that a lesson applies.",
    ]
    if candidates:
        lines.append("Candidate shared records:")
        lines.extend(f"- {location} — {title}" for title, location in candidates)
    else:
        lines.append("No shared-record heading matched. Search the selected owning skill and relevant learning/adaptation records only if the assignment is substantive.")
    lines.extend(
        [
            "If the work meets AGENTS.md's independent-review criteria, invoke the read-only seo_reviewer without waiting for the user to name it; reconcile findings against evidence and retain unresolved disagreement.",
            "Do not create a lesson from routine completion or agreement. Persist only a demonstrated reusable correction and keep the review/repair loop bounded.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if payload.get("hook_event_name") != "UserPromptSubmit":
            return 0
        prompt = payload.get("prompt")
        if not isinstance(prompt, str) or not _is_likely_substantive(prompt):
            return 0
        root = Path(__file__).resolve().parents[2]
        context = _build_context(root, prompt)
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit",
                        "additionalContext": context[:3_200],
                    }
                },
                separators=(",", ":"),
            )
        )
    except (OSError, ValueError, TypeError):
        # This advisory router must fail open and must never block a user prompt.
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
