#!/usr/bin/env python3
"""Focused behavioral checks for seo-learning-loop-v1.py."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

import importlib.util


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".codex/hooks/seo-learning-loop-v1.py"
SPEC = importlib.util.spec_from_file_location("seo_learning_loop_v1", HOOK)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class LearningLoopHookTests(unittest.TestCase):
    def invoke(self, prompt: str) -> dict | None:
        payload = json.dumps(
            {
                "hook_event_name": "UserPromptSubmit",
                "prompt": prompt,
                "cwd": str(ROOT),
            }
        )
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=payload,
            text=True,
            capture_output=True,
            check=True,
            timeout=3,
        )
        return json.loads(result.stdout) if result.stdout else None

    def context(self, prompt: str) -> str:
        output = self.invoke(prompt)
        self.assertIsNotNone(output)
        return output["hookSpecificOutput"]["additionalContext"]

    def test_original_learning_loop_case_routes_to_meta_lesson(self) -> None:
        context = self.context(
            "Evaluate and complete the SEO strategist reviewer learning loop and recursive improvement workflow."
        )
        self.assertIn("Initial improvement-loop checks", context)
        self.assertIn("candidate routing only", context)
        self.assertNotIn("Discover tools without flooding context", context)

    def test_different_relevant_case_routes_to_bounded_fl_m008_record(self) -> None:
        context = self.context(
            "Review the FL-M008 Situational page workflow and verify its bounded navigation correction."
        )
        self.assertIn("FL-M008", context)
        self.assertIn("docs/seo-skill-local-adaptations.md", context)

    def test_substantive_prompt_without_heading_match_still_returns_checkpoint(self) -> None:
        context = self.context(
            "Diagnose a client SEO conversion decline using the supplied analytics evidence."
        )
        self.assertIn("No shared-record heading matched", context)
        self.assertIn("read-only seo_reviewer", context)

    def test_minor_seo_question_emits_nothing(self) -> None:
        self.assertIsNone(self.invoke("What is SEO?"))

    def test_minor_seo_edit_emits_nothing(self) -> None:
        self.assertIsNone(self.invoke("Correct one typo in the page title."))

    def test_unrelated_prompt_emits_nothing(self) -> None:
        self.assertIsNone(self.invoke("Convert 2 cups to milliliters."))

    def test_client_prompt_never_echoes_prompt_or_routes_to_client_files(self) -> None:
        context = self.context(
            "Evaluate the Fanash divorce content page strategy as a substantive SEO assignment."
        )
        self.assertNotIn("Fanash", context)
        self.assertNotIn("clients/", context)

    def test_malformed_input_fails_open(self) -> None:
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input="not json",
            text=True,
            capture_output=True,
            check=True,
            timeout=3,
        )
        self.assertEqual("", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
