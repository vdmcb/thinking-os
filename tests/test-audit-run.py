#!/usr/bin/env python3
"""Regression tests for skill-specific transcript audit rules."""

from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit-run.py"
SPEC = importlib.util.spec_from_file_location("audit_run", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {SCRIPT}")
audit_run = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_run)


class TranscriptAuditTests(unittest.TestCase):
    def run_audit(self, skill: str, command: str) -> tuple[int, str]:
        entries = [
            {"type": "user", "message": {"content": f"${skill} source.pdf"}},
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Bash", "input": {"command": command}},
                    ]
                },
            },
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            transcript = Path(temporary_directory) / "transcript.jsonl"
            transcript.write_text(
                "".join(json.dumps(entry) + "\n" for entry in entries),
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                status = audit_run.audit(transcript, skill, include_all=False)
        return status, output.getvalue()

    def test_understand_flags_optional_image_composition(self) -> None:
        status, output = self.run_audit("understand", "magick page.png contact-sheet.png")
        self.assertEqual(status, 1)
        self.assertIn("VIOLATION optional image composition", output)

    def test_eli5_does_not_inherit_understand_image_rule(self) -> None:
        status, output = self.run_audit("eli5", "magick page.png contact-sheet.png")
        self.assertEqual(status, 0)
        self.assertNotIn("optional image composition", output)

    def test_common_rule_still_applies_to_understand(self) -> None:
        status, output = self.run_audit("understand", "cat source.md")
        self.assertEqual(status, 1)
        self.assertIn("VIOLATION prints the source", output)


if __name__ == "__main__":
    unittest.main()
