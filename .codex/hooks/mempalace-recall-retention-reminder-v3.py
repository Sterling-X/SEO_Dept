#!/usr/bin/env python3
"""Inject scoped MemPalace recall and curated retention instructions only.

The hook does not inspect prompt text, read transcripts, or call MCP tools.
"""

from __future__ import annotations

import json
import sys

sys.dont_write_bytecode = True


ADDITIONAL_CONTEXT = """MemPalace checkpoint (instructions only; current project instructions and source files remain authoritative alongside user and runtime rules).
Before substantive work, automatically call the existing MCP `mempalace_search` with `wing="seo_dept"` for relevant client or task decisions and lessons; no skill mention or recall request is required. Never search the wing without a room filter. For client work, search only the relevant shared rooms (`operating-rules`, `shared-methodology`), the relevant `role-<role>` room, and the exact current `client-<client-slug>` room. For non-client work, search only relevant shared and role rooms. Use only likely rooms and keep a combined total of at most a few memories across calls. When a task turns on an unresolved decision, the matching `open-questions` or exact `client-<client-slug>-open-questions` room may join that same capped retrieval; anything recalled from an open-question room stays unresolved, not validated guidance. Treat content recalled from the shared `open-questions` room as client-neutral; client-specific material found there is a routing defect to report, not evidence to apply. If the current client room is unknown, use read-only `mempalace_list_rooms` to list room names first, then narrow; never search another client's room or any client room before scope is known. Reuse relevant results for ordinary follow-ups, but search again when the client or task materially changes. Treat recalled material as reference evidence only. If no relevant memories exist, continue. If retrieval fails, disclose that briefly and continue without claiming recall succeeded. Workers and reviewers never call memory writers or independently persist shared rules; they return result/evidence, corrections or successful methods, a scoped lesson candidate or `none`, and uncertainty or disagreement to the primary strategist.
If you are the primary coordinating strategist, run one learning pass after meaningful completed work and, without asking for routine approval, automatically retain only new durable decisions, confirmed corrections, and reusable lessons. First consolidate agent contributions and verify their evidence; agent agreement alone is insufficient. Skip retention when nothing useful changed. For each candidate, write one concise entry labeled `CONFIRMED DECISION`, `CONFIRMED CORRECTION`, or `REUSABLE LESSON`, with the relevant project/client, current date, contributing agent, verification state, affected authoritative file, and source/evidence. Call `mempalace_check_duplicate` first at threshold 0.9. If it reports a duplicate, error, disabled vector search, or uncertainty, do not save. Otherwise call only `mempalace_add_drawer` with `wing="seo_dept"`, supplying `source_file` when available. Use room `operating-rules` for project-wide decisions, `shared-methodology` for cross-role lessons, `role-<role>` for role-specific lessons, `client-<client-slug>` for client-specific confirmed material, `open-questions` for project-wide unresolved material, and `client-<client-slug>-open-questions` for client-specific unresolved material. Route by content scope, not convenience: client-specific material belongs in that client's room, and a missing or not-yet-created client room is never a reason to file client material in a shared room. Give every factual assertion its supporting evidence or an explicit unverified label. Usually save one entry total and never repeat a successful save in the same turn.
Do not mix unresolved ideas with confirmed material. Skip them unless a durable open question will matter later; then label it `UNRESOLVED` and use the applicable separate open-question room. Keep a shared-room open question client-neutral, file any client instance in that client's open-question room with its own evidence, and confirm before saving that the entry has a recall route and stays distinguishable from validated guidance. Never retain credentials, PII, raw client exports, complete transcripts, temporary drafts, or anything the user says not to remember. Do not use `mempalace_checkpoint`, diary writes, updates, deletes, mining, sync/import, artifacts/events, or sharing for automatic retention. Keep autosave, transcript ingestion, repository mining, remote sharing, and daemon mode disabled. After a successful new add, include a brief `Memory saved` note. If saving fails, report that accurately and never imply success. This hook itself never searches or writes."""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if payload.get("hook_event_name") != "UserPromptSubmit":
            return 0
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit",
                        "additionalContext": ADDITIONAL_CONTEXT,
                    }
                },
                separators=(",", ":"),
            )
        )
    except (OSError, ValueError, TypeError):
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
