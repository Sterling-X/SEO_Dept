#!/usr/bin/env python3
"""Generate the Claude and Codex agent adapters from the canonical role files.

Canonical text lives in canonical/roles/<role>.md. This script wraps it in each host's
definition format so that one copy of the role instructions exists. Run with --check to
verify the generated files on disk match the canonical sources (used by the test suite).

Formats verified against official documentation on 2026-09-23:
- Claude Code subagents: Markdown with YAML frontmatter (name, description, tools,
  disallowedTools) in .claude/agents/. `tools` is an allowlist; omitting Agent removes
  the ability to spawn subagents.
- Codex custom agents: TOML in .codex/agents/ with required name, description,
  developer_instructions and optional sandbox_mode (read-only | workspace-write).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PILOT_ROOT = Path(__file__).resolve().parents[1]
ROLES_DIR = PILOT_ROOT / "canonical" / "roles"
CLAUDE_DIR = PILOT_ROOT / "adapters" / "claude" / "agents"
CODEX_DIR = PILOT_ROOT / "adapters" / "codex" / "agents"

ROLES = {
    "content-writer": {
        "codex_name": "content_writer",
        "description": (
            "Pilot content writer for a content-workflow run directory. Drafts and corrects one "
            "client page from the pinned page-writing skill, exactly one domain-routed client voice, "
            "approved client facts, and pinned legal sources; produces candidate drafts and "
            "corrections only. Use only when the content-workflow coordinator dispatches drafting or "
            "correction work for a specific run directory."
        ),
        "claude_tools": ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "WebFetch", "WebSearch"],
        "claude_disallowed": ["Agent", "Task", "NotebookEdit"],
        "codex_sandbox": "workspace-write",
        "claude_note": (
            "Host note (Claude Code): paths are relative to the repository root. You have Bash for "
            "the pinned skill's generator and validators only; write only inside the run directory. "
            "Your tool allowlist omits the Agent tool, so you cannot delegate."
        ),
        "codex_note": (
            "Host note (Codex): paths are relative to the repository root. Your sandbox is "
            "workspace-write; write only inside the run directory. Codex does not enforce the "
            "no-delegation rule by configuration, so you must not spawn agents."
        ),
    },
    "legal-reviewer": {
        "codex_name": "legal_reviewer",
        "description": (
            "Pilot read-only legal reviewer. Independently verifies material legal claims, "
            "jurisdiction, exceptions, dates, and citation support against current primary authority "
            "fetched live, and returns structured findings with evidence. Does not edit the draft. "
            "Use only when the content-workflow coordinator dispatches a legal checkpoint, final "
            "review, or recheck for a run directory."
        ),
        "claude_tools": ["Read", "Grep", "Glob", "WebFetch", "WebSearch"],
        "claude_disallowed": ["Agent", "Task", "Write", "Edit", "NotebookEdit", "Bash"],
        "codex_sandbox": "read-only",
        "claude_note": (
            "Host note (Claude Code): paths are relative to the repository root. You hold Read, Grep, "
            "Glob, WebFetch, and WebSearch only. You cannot compute hashes, run validators, or write "
            "files; the coordinator records your findings with scripts/record_review.py. Your tool "
            "allowlist omits the Agent tool, so you cannot delegate. WebFetch returns a processed rendering "
            "of a page, not its raw text: take every verbatim excerpt from the research record's stored "
            "text (research/EV<n>.txt) and use your own fetch to corroborate that the live page still says "
            "it; confirm the operative subsection is inside the stored text before recording Confirmed, and "
            "otherwise record Flagged and ask the coordinator for a record of the subsection URL."
        ),
        "codex_note": (
            "Host note (Codex): paths are relative to the repository root. Your sandbox is read-only; "
            "do not attempt writes. Codex does not enforce the no-delegation rule by configuration, "
            "so you must not spawn agents. The coordinator records your findings."
        ),
    },
    "editorial-reviewer": {
        "codex_name": "editorial_reviewer",
        "description": (
            "Pilot read-only editorial reviewer. Evaluates usefulness, client specificity, brand "
            "fidelity against the one domain-routed voice source, structure, unsupported promises, "
            "and compliance with the brief, and returns structured findings with evidence. Does not "
            "edit the draft. Use only when the content-workflow coordinator dispatches an editorial "
            "checkpoint, final review, or recheck for a run directory."
        ),
        "claude_tools": ["Read", "Grep", "Glob", "WebFetch"],
        "claude_disallowed": ["Agent", "Task", "Write", "Edit", "NotebookEdit", "Bash", "WebSearch"],
        "codex_sandbox": "read-only",
        "claude_note": (
            "Host note (Claude Code): paths are relative to the repository root. You hold Read, Grep, "
            "Glob, and WebFetch only. You cannot write files; the coordinator records your findings "
            "with scripts/record_review.py. Your tool allowlist omits the Agent tool, so you cannot "
            "delegate."
        ),
        "codex_note": (
            "Host note (Codex): paths are relative to the repository root. Your sandbox is read-only; "
            "do not attempt writes. Codex does not enforce the no-delegation rule by configuration, "
            "so you must not spawn agents. The coordinator records your findings."
        ),
    },
}

GENERATED_BANNER = (
    "GENERATED FILE. Source of truth: pilot/content-workflow/canonical/roles/{role}.md. "
    "Regenerate with: python3 pilot/content-workflow/scripts/build_adapters.py"
)


def canonical_text(role: str) -> str:
    return (ROLES_DIR / f"{role}.md").read_text(encoding="utf-8").rstrip() + "\n"


def render_claude(role: str) -> str:
    spec = ROLES[role]
    lines = [
        "---",
        f"name: {role}",
        f"description: {spec['description']}",
        f"tools: {', '.join(spec['claude_tools'])}",
        f"disallowedTools: {', '.join(spec['claude_disallowed'])}",
        "---",
        "",
        f"<!-- {GENERATED_BANNER.format(role=role)} -->",
        "",
        spec["claude_note"],
        "",
        canonical_text(role),
    ]
    return "\n".join(lines)


def toml_basic(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')


def render_codex(role: str) -> str:
    spec = ROLES[role]
    instructions = spec["codex_note"] + "\n\n" + canonical_text(role)
    lines = [
        f"# {GENERATED_BANNER.format(role=role)}",
        f'name = "{spec["codex_name"]}"',
        'description = "' + toml_basic(spec["description"]).replace('"', '\\"') + '"',
        f'sandbox_mode = "{spec["codex_sandbox"]}"',
        'developer_instructions = """',
        toml_basic(instructions).rstrip("\n"),
        '"""',
        "",
    ]
    return "\n".join(lines)


def targets() -> list[tuple[Path, str]]:
    out: list[tuple[Path, str]] = []
    for role, spec in ROLES.items():
        out.append((CLAUDE_DIR / f"{role}.md", render_claude(role)))
        out.append((CODEX_DIR / f"{spec['codex_name']}.toml", render_codex(role)))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify generated files match canonical sources")
    args = parser.parse_args()
    drift: list[str] = []
    for path, content in targets():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                drift.append(str(path.relative_to(PILOT_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"wrote {path.relative_to(PILOT_ROOT)}")
    if args.check:
        if drift:
            print("DRIFT: " + ", ".join(drift))
            return 1
        print(f"OK: {len(targets())} adapter files match canonical sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
