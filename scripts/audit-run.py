#!/usr/bin/env python3
"""Audit a Claude Code transcript for the execution contract in core/references/execution.md.

Usage: scripts/audit-run.py TRANSCRIPT.jsonl [--skill eli5] [--all]

Finds each run of the skill (a user turn that invokes it) and reports, for the assistant
turns until the next user turn: tool calls, and every call that the contract forbids or
discourages. Exit status is 1 when any run has a violation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VIOLATIONS = [
    ("prints the source", re.compile(r"\b(cat|less|more|head|tail|bat)\b(?!\s*>)[^|&;>]*\.(txt|md|pdf|csv)\b")),
    ("diagnostic before reading", re.compile(r"\b(pdfinfo|pdfimages|pdffonts|exiftool)\b")),
    ("scratch draft", re.compile(r"\b(draft|scratch)[\w-]*\.(md|txt)\b")),
    ("lint run on output", re.compile(r"check-[\w-]*evals\.py|wc -w")),
    ("page audit", re.compile(r"split\(['\"]\\f['\"]\)|form feed|page count", re.IGNORECASE)),
]
ALLOWED_EXTRACTION = re.compile(r"\b(pdftotext|extract-document\.sh|check-prerequisites\.sh)\b")


def turns(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def user_text(entry: dict) -> str:
    content = entry.get("message", {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
    return ""


def is_tool_result(entry: dict) -> bool:
    content = entry.get("message", {}).get("content")
    return isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content)


def tool_uses(entry: dict):
    for c in entry.get("message", {}).get("content", []) or []:
        if isinstance(c, dict) and c.get("type") == "tool_use":
            yield c.get("name", ""), c.get("input", {}) or {}


def audit(path: Path, skill: str, include_all: bool) -> int:
    runs = []
    current = None
    for entry in turns(path):
        kind = entry.get("type")
        if kind == "user" and not is_tool_result(entry):
            text = user_text(entry).strip()
            first = text.splitlines()[0] if text else ""
            invoked = first.startswith((f"/{skill}", f"${skill}")) or re.match(rf"Base directory for this skill: .*/{skill}\b", first) is not None
            if invoked or (include_all and current is None):
                label = "skill launch" if first.startswith("Base directory") else first[:80]
                current = {"prompt": label, "calls": [], "findings": []}
                runs.append(current)
            elif current is not None:
                current = None
        elif kind == "assistant" and current is not None:
            for name, inp in tool_uses(entry):
                cmd = inp.get("command", "") if name == "Bash" else ""
                current["calls"].append((name, cmd[:120].replace("\n", " ")))
                for label, pattern in VIOLATIONS:
                    if name == "Bash" and pattern.search(cmd):
                        current["findings"].append((label, cmd[:100].replace("\n", " ")))
                if name in ("Write", "Edit") and re.search(r"draft|scratch", str(inp.get("file_path", ""))):
                    current["findings"].append(("scratch draft", str(inp.get("file_path", ""))[:100]))
    if not runs:
        print(f"No {skill} runs found in {path.name}")
        return 0
    status = 0
    for i, run in enumerate(runs, 1):
        extractions = sum(1 for name, cmd in run["calls"] if name == "Bash" and ALLOWED_EXTRACTION.search(cmd))
        bash = sum(1 for name, _ in run["calls"] if name == "Bash")
        print(f"run {i}: {run['prompt']!r}")
        print(f"  tool calls: {len(run['calls'])} (Bash {bash}, extraction {extractions})")
        if extractions > 1:
            run["findings"].append(("more than one extraction command", f"{extractions} extraction calls"))
        if run["findings"]:
            status = 1
            for label, detail in run["findings"]:
                print(f"  VIOLATION {label}: {detail}")
        else:
            print("  clean")
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--skill", default="eli5")
    parser.add_argument("--all", action="store_true", help="treat every user turn as a run start")
    args = parser.parse_args()
    if not args.transcript.is_file():
        print(f"Transcript not found: {args.transcript}", file=sys.stderr)
        return 2
    return audit(args.transcript, args.skill, args.all)


if __name__ == "__main__":
    sys.exit(main())
