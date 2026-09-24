#!/usr/bin/env python3
"""Focused checks for the MemPalace recall and retention reminder."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".codex/hooks/mempalace-recall-retention-reminder-v3.py"


class MemPalaceRecallReminderTests(unittest.TestCase):
    def invoke(self, payload: str) -> dict | None:
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=payload,
            text=True,
            capture_output=True,
            check=True,
            timeout=3,
        )
        return json.loads(result.stdout) if result.stdout else None

    def test_injects_bounded_recall_and_precedence_policy(self) -> None:
        prompt = "Review the current client SEO plan."
        output = self.invoke(
            json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "prompt": prompt,
                    "transcript_path": "/private/example/transcript.jsonl",
                }
            )
        )
        self.assertIsNotNone(output)
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("automatically call the existing MCP `mempalace_search`", context)
        self.assertIn('`wing="seo_dept"`', context)
        self.assertIn("at most a few", context)
        self.assertIn("no skill mention or recall request is required", context)
        self.assertIn("Never search the wing without a room filter", context)
        self.assertIn("exact current `client-<client-slug>`", context)
        self.assertIn("combined total of at most a few memories", context)
        self.assertIn("list room names first", context)
        self.assertIn("never search another client's room", context)
        self.assertIn("project instructions and source files remain authoritative", context)
        self.assertIn("If retrieval fails", context)
        self.assertNotIn(prompt, context)
        self.assertNotIn("transcript.jsonl", context)

    def test_injects_curated_automatic_retention_and_duplicate_gate(self) -> None:
        output = self.invoke(
            json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "prompt": "Continue the prior task.",
                }
            )
        )
        self.assertIsNotNone(output)
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("primary coordinating strategist", context)
        self.assertIn("Workers and reviewers never call memory writers", context)
        self.assertIn("a scoped lesson candidate or `none`", context)
        self.assertIn("run one learning pass", context)
        self.assertIn("consolidate agent contributions", context)
        self.assertIn("agent agreement alone is insufficient", context)
        self.assertIn("without asking for routine approval", context)
        self.assertIn("Skip retention when nothing useful changed", context)
        self.assertIn("project/client, current date", context)
        self.assertIn("source/evidence", context)
        self.assertLess(
            context.index("`mempalace_check_duplicate`"),
            context.index("`mempalace_add_drawer`"),
        )
        self.assertIn("threshold 0.9", context)
        self.assertIn("error, disabled vector search, or uncertainty, do not save", context)
        self.assertIn("contributing agent, verification state, affected authoritative file", context)
        self.assertIn("`shared-methodology`", context)
        self.assertIn("`role-<role>`", context)
        self.assertIn("`client-<client-slug>`", context)
        self.assertIn("`client-<client-slug>-open-questions`", context)

    def test_preserves_exclusions_and_restricts_automatic_writes(self) -> None:
        output = self.invoke(
            json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "prompt": "Finish a substantive but non-sensitive project task.",
                }
            )
        )
        self.assertIsNotNone(output)
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("UNRESOLVED", context)
        self.assertIn("credentials, PII, raw client exports, complete transcripts, temporary drafts", context)
        self.assertIn("anything the user says not to remember", context)
        self.assertIn("Do not use `mempalace_checkpoint`", context)
        self.assertIn("autosave, transcript ingestion, repository mining, remote sharing, and daemon mode disabled", context)
        self.assertIn("`Memory saved` note", context)
        self.assertIn("If saving fails, report that accurately", context)
        self.assertIn("This hook itself never searches or writes", context)

    def test_injects_scope_routing_evidence_and_open_question_recall(self) -> None:
        output = self.invoke(
            json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "prompt": "Wrap up and retain anything durable.",
                }
            )
        )
        self.assertIsNotNone(output)
        context = output["hookSpecificOutput"]["additionalContext"]
        # Retained open questions must have a recall route and stay unresolved.
        self.assertIn("may join that same capped retrieval", context)
        self.assertIn("stays unresolved, not validated guidance", context)
        # Routing follows content scope; a missing client room is not an excuse.
        self.assertIn("Route by content scope, not convenience", context)
        self.assertIn("never a reason to file client material in a shared room", context)
        # Every assertion carries evidence or an explicit unverified label.
        self.assertIn("supporting evidence or an explicit unverified label", context)
        # Shared-room open questions stay client-neutral and distinguishable.
        self.assertIn("Keep a shared-room open question client-neutral", context)
        self.assertIn("distinguishable from validated guidance", context)
        self.assertLess(
            context.index("may join that same capped retrieval"),
            context.index("Route by content scope, not convenience"),
        )

    def test_injected_context_fits_configured_codex_limit(self) -> None:
        cfg = json.loads((ROOT / ".codex/hooks.json").read_text())
        limits = [
            entry["additionalContextLimit"]
            for group in cfg["hooks"]["UserPromptSubmit"]
            for entry in group["hooks"]
            if "mempalace-recall-retention-reminder-v3" in entry["command"]
        ]
        self.assertEqual(len(limits), 1)
        output = self.invoke(
            json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "size check"})
        )
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertLessEqual(len(context), limits[0])
        # Also bound the raw payload, in case the host applies the limit pre-decode.
        raw = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "size"}),
            text=True,
            capture_output=True,
            check=True,
            timeout=3,
        ).stdout
        self.assertLessEqual(len(raw), limits[0])
        self.assertTrue(
            context.rstrip().endswith("This hook itself never searches or writes.")
        )

    def test_nonmatching_or_malformed_input_fails_open(self) -> None:
        self.assertIsNone(
            self.invoke(json.dumps({"hook_event_name": "SessionStart"}))
        )
        self.assertIsNone(self.invoke("not json"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
