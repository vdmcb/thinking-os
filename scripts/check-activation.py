#!/usr/bin/env python3
"""Cross-skill activation checks: the boundary between skills, and each skill's cases against the other's."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid JSON at {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def norm(prompt: str) -> str:
    return " ".join(prompt.lower().split())


def main() -> int:
    cross = load(ROOT / "evals" / "activation-crosscheck.json")
    skills = cross["skills"]
    cases = cross["cases"]
    require(len(cases) >= 12, "Need at least twelve cross-skill activation cases")
    ids = [c["id"] for c in cases]
    require(len(ids) == len(set(ids)), "Cross-skill case ids must be unique")
    per_skill = {name: load(ROOT / "evals" / name / "cases.json")["activation"] for name in skills}
    positives = {name: {norm(c["prompt"]) for c in per_skill[name]["positive"]} for name in skills}
    negatives = {name: {norm(c["prompt"]) for c in per_skill[name]["negative"]} for name in skills}

    counts = {name: 0 for name in skills}
    counts["none"] = 0
    for case in cases:
        expected = case["expected"]
        require(expected in skills or expected == "none", f"{case['id']}: unknown expected skill {expected!r}")
        require(bool(case.get("reason", "").strip()), f"{case['id']}: needs a reason")
        counts[expected] += 1
        prompt = norm(case["prompt"])
        for name in skills:
            if name != expected:
                require(prompt not in positives[name],
                        f"{case['id']}: expected {expected} but {name} lists it as a positive activation case")
            if name == expected:
                require(prompt not in negatives[name],
                        f"{case['id']}: expected {expected} but {name} lists it as a negative activation case")
    for name in skills:
        require(counts[name] >= 4, f"Need at least four cross-skill cases expecting {name}")
    require(counts["none"] >= 2, "Need at least two cross-skill cases expecting no skill")

    # A prompt cannot be a positive for both skills.
    for a in skills:
        for b in skills:
            if a < b:
                overlap = positives[a] & positives[b]
                require(not overlap, f"Prompt is a positive activation case for both {a} and {b}: {sorted(overlap)}")

    print("Cross-skill activation valid: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
