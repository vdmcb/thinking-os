#!/usr/bin/env python3
"""Plugin marketplace checks: manifest consistency between marketplace.json, each plugin's plugin.json, its skills, and its listing icon."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
RESERVED_NAMES = {
    "claude-code-marketplace",
    "claude-code-plugins",
    "claude-plugins-official",
    "anthropic-marketplace",
    "anthropic-plugins",
    "agent-skills",
    "knowledge-work-plugins",
    "life-sciences",
    "first-party-plugins",
}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
ICON_MIN_PX = 512
ICON_MAX_PX = 2048
ICON_MAX_BYTES = 2 * 1024 * 1024


def load(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid JSON at {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def field(obj: dict, key: str, context: str) -> object:
    value = obj.get(key)
    require(value is not None, f"{context}: missing required field {key!r}")
    return value


def check_name(name: object, context: str) -> None:
    require(isinstance(name, str), f"{context}: name must be a string")
    require(bool(NAME_RE.fullmatch(name)), f"{context}: name {name!r} must be lowercase kebab-case")
    require(len(name) <= 64, f"{context}: name {name!r} exceeds 64 characters")
    require(name not in RESERVED_NAMES, f"{context}: name {name!r} is reserved by Anthropic")


def check_icon(plugin_root: Path, context: str) -> None:
    """The plugin directory uses .claude-plugin/icon.png as the listing icon: a square PNG, 512 to 2048 px, under 2 MB."""
    icon = plugin_root / ".claude-plugin" / "icon.png"
    require(icon.is_file(), f"{context}: missing listing icon at {icon.relative_to(ROOT)}")
    data = icon.read_bytes()
    require(len(data) < ICON_MAX_BYTES, f"{context}: icon.png must be under 2 MB")
    require(data[:8] == PNG_SIGNATURE and data[12:16] == b"IHDR", f"{context}: icon.png is not a PNG")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    require(width == height, f"{context}: icon.png must be square, found {width}x{height}")
    require(ICON_MIN_PX <= width <= ICON_MAX_PX,
            f"{context}: icon.png must be {ICON_MIN_PX} to {ICON_MAX_PX} px on each side, found {width}")


def check_plugin(entry: dict) -> str:
    name = entry["name"]
    check_name(name, f"marketplace.json entry {name!r}")
    source = field(entry, "source", f"marketplace.json entry {name!r}")
    require(isinstance(source, str) and source.startswith("./"),
            f"{name}: source must be a relative path; Cowork GitHub sync does not support npm, archive, or command sources")
    plugin_root = (ROOT / source).resolve()
    require(plugin_root.is_relative_to(ROOT),
            f"{name}: source {source!r} resolves outside the repository")
    require(plugin_root != ROOT,
            f"{name}: source must be a plugin folder, not the repository root; "
            "the whole root would ship and be scanned, including evals, tests, and CLAUDE.md")
    require(plugin_root.is_dir(), f"{name}: source path {source!r} does not exist")
    manifest = plugin_root / ".claude-plugin" / "plugin.json"
    require(manifest.is_file(), f"{name}: no plugin manifest at {manifest.relative_to(ROOT)}")
    plugin = load(manifest)
    require(isinstance(plugin, dict), f"{name}: plugin manifest must be a JSON object")

    check_name(field(plugin, "name", "plugin.json"), "plugin.json")
    require(plugin["name"] == name,
            f"{name}: marketplace entry name does not match plugin.json name {plugin['name']!r}")
    plugin_version = field(plugin, "version", "plugin.json")
    require(isinstance(plugin_version, str) and SEMVER_RE.fullmatch(plugin_version) is not None,
            "plugin.json: version must be plain semver (MAJOR.MINOR.PATCH)")
    plugin_description = field(plugin, "description", "plugin.json")
    require(isinstance(plugin_description, str) and bool(plugin_description.strip()),
            "plugin.json: description must be a non-empty string")
    if "version" in entry:
        require(isinstance(entry["version"], str) and SEMVER_RE.fullmatch(entry["version"]) is not None,
                f"{name}: marketplace version must be plain semver (MAJOR.MINOR.PATCH)")
        require(entry["version"] == plugin_version,
                f"{name}: marketplace version {entry['version']!r} drifted from plugin.json {plugin_version!r}; "
                "Cowork auto-sync fires on version bumps, so both must move together")

    skills_value = plugin.get("skills", "./skills/")
    require(isinstance(skills_value, str) and skills_value.startswith("./"),
            "plugin.json: skills must be a relative './' path")
    skills_dir = (plugin_root / skills_value).resolve()
    require(skills_dir.is_relative_to(plugin_root),
            f"plugin.json: skills path {skills_value!r} resolves outside the plugin folder; installed plugins cannot reach it")
    require(skills_dir.is_dir(), f"plugin.json: skills path {skills_value!r} does not exist")
    shipped = sorted(p.parent.name for p in skills_dir.glob("*/SKILL.md"))
    require(len(shipped) >= 1, "plugin.json: skills directory contains no SKILL.md packages")
    stray = sorted(d.name for d in skills_dir.iterdir() if d.is_dir() and not (d / "SKILL.md").is_file())
    require(not stray, f"skills/ contains directories without SKILL.md that would ship broken: {stray}")

    check_icon(plugin_root, name)
    return f"plugin {name!r} v{plugin_version} from {source} with skills: {', '.join(shipped)}"


def main() -> int:
    marketplace = load(ROOT / ".claude-plugin" / "marketplace.json")
    require(isinstance(marketplace, dict), "marketplace.json: must be a JSON object")

    check_name(field(marketplace, "name", "marketplace.json"), "marketplace.json")
    owner = field(marketplace, "owner", "marketplace.json")
    require(isinstance(owner, dict), "marketplace.json: owner must be an object")
    owner_name = field(owner, "name", "marketplace.json owner")
    require(isinstance(owner_name, str) and bool(owner_name.strip()),
            "marketplace.json: owner.name must be a non-empty string")
    entries = field(marketplace, "plugins", "marketplace.json")
    require(isinstance(entries, list) and all(isinstance(e, dict) for e in entries),
            "marketplace.json: plugins must be an array of objects")
    require(len(entries) >= 1, "marketplace.json: needs at least one plugin entry")

    entry_names = [field(e, "name", "marketplace.json plugin entry") for e in entries]
    require(len(entry_names) == len(set(entry_names)), "marketplace.json: plugin names must be unique")

    for entry in entries:
        print(f"OK: marketplace {marketplace['name']!r} serves {check_plugin(entry)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
