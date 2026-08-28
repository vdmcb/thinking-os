#!/usr/bin/env python3
"""Failure-path tests for the local plugin marketplace validator."""

from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-plugin.py"
SPEC = importlib.util.spec_from_file_location("check_plugin", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {SCRIPT}")
check_plugin = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_plugin)


class PluginManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name).resolve()
        (self.root / ".claude-plugin").mkdir()
        for skill in ("understand", "eli5"):
            skill_dir = self.root / "skills" / skill
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(f"# {skill}\n", encoding="utf-8")
        self.plugin = {
            "name": "thinking-os",
            "version": "0.1.0",
            "description": "Portable cognitive skills",
            "skills": "./skills/",
        }
        self.marketplace = {
            "name": "thinking-os",
            "owner": {"name": "vdmcb"},
            "plugins": [
                {
                    "name": "thinking-os",
                    "source": "./",
                    "version": "0.1.0",
                }
            ],
        }
        check_plugin.ROOT = self.root

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_manifests(self) -> None:
        (self.root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(self.plugin), encoding="utf-8"
        )
        (self.root / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps(self.marketplace), encoding="utf-8"
        )

    def run_valid(self) -> None:
        self.write_manifests()
        with redirect_stdout(io.StringIO()):
            self.assertEqual(check_plugin.main(), 0)

    def assert_invalid(self, expected: str) -> None:
        self.write_manifests()
        with self.assertRaisesRegex(SystemExit, expected):
            check_plugin.main()

    def test_accepts_repository_manifests(self) -> None:
        self.run_valid()

    def test_rejects_non_string_plugin_name_cleanly(self) -> None:
        self.plugin["name"] = 42
        self.assert_invalid("name must be a string")

    def test_rejects_non_object_owner_cleanly(self) -> None:
        self.marketplace["owner"] = "vdmcb"
        self.assert_invalid("owner must be an object")

    def test_rejects_non_array_plugin_entries_cleanly(self) -> None:
        self.marketplace["plugins"] = {"name": "thinking-os"}
        self.assert_invalid("plugins must be an array of objects")

    def test_rejects_marketplace_and_manifest_name_drift(self) -> None:
        self.marketplace["plugins"][0]["name"] = "different-name"
        self.assert_invalid("marketplace entry name does not match")

    def test_rejects_marketplace_source_escape(self) -> None:
        self.marketplace["plugins"][0]["source"] = "./../outside"
        self.assert_invalid("resolves outside the repository")

    def test_rejects_skills_path_escape(self) -> None:
        self.plugin["skills"] = "./../outside"
        self.assert_invalid("skills path .* resolves outside the repository")


if __name__ == "__main__":
    unittest.main()
