#!/usr/bin/env python3
"""Deterministic checks for ELI5 evaluation metadata and exemplars."""

from __future__ import annotations

import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals" / "eli5"
SKILL_DIR = ROOT / "skills" / "eli5"

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002700-\U000027BF\U0001F1E6-\U0001F1FF⬀-⯿☀-⛿]"
)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid JSON at {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.is_file(), f"Missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def sentences(text: str) -> list[str]:
    """Split prose into sentences, ignoring headings and list markers."""
    body: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith(">"):
            continue
        stripped = re.sub(r"^(\d+\.|[-*])\s+", "", stripped)
        body.append(stripped)
    parts: list[str] = []
    for line in body:
        # Each line or bullet is its own unit; a dot followed by whitespace ends a
        # sentence. Decimals and clock times carry no whitespace after the dot.
        parts.extend(re.split(r"(?<=[.?])\s+", line))
    return [p for p in parts if p.strip()]


def check_activation(cases: dict, invariants: dict) -> tuple[int, int]:
    positive = cases.get("activation", {}).get("positive", [])
    negative = cases.get("activation", {}).get("negative", [])
    minimum = invariants.get("minimum_activation_cases_per_class", 10)
    require(len(positive) >= minimum, f"Need at least {minimum} positive activation cases")
    require(len(negative) >= minimum, f"Need at least {minimum} negative activation cases")
    all_cases = positive + negative
    ids = [item.get("id") for item in all_cases]
    require(all(ids), "Every activation case needs an id")
    require(len(ids) == len(set(ids)), "Activation case ids must be unique")
    for item in all_cases:
        require(bool(item.get("prompt", "").strip()), f"Activation case {item['id']} needs a prompt")
        require(bool(item.get("reason", "").strip()), f"Activation case {item['id']} needs a reason")
    return len(positive), len(negative)


def check_output_cases(cases: dict, invariants: dict) -> int:
    output_cases = cases.get("output_cases", [])
    minimum = invariants.get("minimum_output_cases", 5)
    require(len(output_cases) >= minimum, f"Need at least {minimum} output-quality cases")
    ids = [item.get("id") for item in output_cases]
    require(all(ids) and len(ids) == len(set(ids)), "Output case ids must be present and unique")
    for item in output_cases:
        fixture = EVAL / item["fixture"]
        expected = EVAL / item["expected"]
        source = read(fixture)
        reference = read(expected)
        for literal in item.get("required_literals", []):
            require(literal in source, f"Fixture {fixture.name} is missing required literal {literal!r}")
        for literal in item.get("expected_required_literals", []):
            require(
                literal in reference,
                f"Expected reference {expected.name} is missing required literal {literal!r}",
            )
    return len(output_cases)


def check_exemplar(path: Path, invariants: dict) -> None:
    text = read(path)
    low = text.lower()
    name = path.name
    core = invariants["core_output"]
    voice = invariants["cognitive_load"]

    # Structure: required sections present, in order, as level-two headings.
    headings = re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
    required = invariants["required_sections"]
    optional = invariants.get("optional_sections", [])
    for section in required:
        require(section in headings, f"{name}: missing required section '{section}' (structure lint)")
    positions = [headings.index(section) for section in required]
    require(positions == sorted(positions), f"{name}: required sections are out of order (structure lint)")
    for heading in headings:
        require(
            heading in required or heading in optional,
            f"{name}: unexpected section '{heading}' (structure lint)",
        )

    # Budget.
    words = len(text.split())
    ceiling = core["hard_ceiling_words"]
    require(words <= ceiling, f"{name}: {words} words exceeds the {ceiling}-word ceiling (budget lint)")

    # Sentence length.
    max_sentence = core["max_words_per_sentence"]
    for sentence in sentences(text):
        count = len(sentence.split())
        require(
            count <= max_sentence,
            f"{name}: sentence of {count} words exceeds {max_sentence}: {sentence[:60]!r} (sentence lint)",
        )

    # Basic facts count.
    facts_block = re.search(r"^## The basic facts\n(.*?)(?=^## )", text, flags=re.MULTILINE | re.DOTALL)
    require(facts_block is not None, f"{name}: cannot locate 'The basic facts' section body (structure lint)")
    bullets = [line for line in facts_block.group(1).splitlines() if line.strip().startswith("- ")]
    limits = core["basic_facts_count"]
    require(
        limits["minimum"] <= len(bullets) <= limits["maximum"],
        f"{name}: {len(bullets)} basic facts, expected {limits['minimum']}-{limits['maximum']} (bedrock lint)",
    )

    # Cognitive-load lint: dashes, exclamation marks, emoji, banned words and phrases.
    for ch in voice["forbidden_characters"]:
        require(ch not in text, f"{name}: forbidden character {ch!r} (cognitive-load lint)")
    for word in voice["forbidden_words"]:
        require(
            not re.search(rf"\b{re.escape(word)}\b", low),
            f"{name}: forbidden word {word!r} (cognitive-load lint)",
        )
    for phrase in voice["forbidden_phrases"]:
        require(phrase not in low, f"{name}: forbidden phrase {phrase!r} (cognitive-load lint)")
    require(not EMOJI_RE.search(text), f"{name}: emoji or decorative symbol (cognitive-load lint)")

    # No tables, no bold outside the status line.
    require("|" not in text, f"{name}: table or pipe character (structure lint)")
    for line in text.splitlines():
        if "**" in line:
            require(
                line.lstrip().startswith(">"),
                f"{name}: bold outside the status line (typography lint)",
            )


def check_skill_documentation(invariants: dict) -> None:
    skill = read(SKILL_DIR / "SKILL.md")
    contract = read(SKILL_DIR / "references" / "eli5-contract.md")
    output_format = read(SKILL_DIR / "references" / "output-format.md")
    first_principles = read(ROOT / invariants["first_principles"]["reference"])
    voice_text = read(ROOT / invariants["cognitive_load"]["reference"])
    template = read(SKILL_DIR / "assets" / "eli5-explanation.md")

    for section in invariants["required_sections"] + invariants.get("optional_sections", []):
        require(section in output_format, f"Output format does not document section '{section}'")
        require(section in template, f"Template does not include section '{section}'")
    for label in invariants["labels"]:
        require(
            label in contract or label in output_format,
            f"Label is undocumented in the contract or output format: {label!r}",
        )
    ceiling = invariants["core_output"]["hard_ceiling_words"]
    require(f"{ceiling} words" in output_format, f"Output format must state the {ceiling}-word ceiling")
    require(f"{ceiling} words" in skill, f"SKILL.md must state the {ceiling}-word ceiling")
    for literal in ("bedrock", "first principles", "repeat-back", "The file does not say why"):
        require(literal.lower() in skill.lower(), f"SKILL.md does not document: {literal}")
    for kind in invariants["first_principles"]["bedrock_kinds"]:
        require(kind in first_principles.lower(), f"First-principles reference does not name bedrock kind: {kind}")
    for source in invariants["first_principles"]["bedrock_sources"]:
        require(source in first_principles, f"First-principles reference does not name bedrock source: {source}")
    for literal in ("repeat-back test", "One idea per sentence", "chatbot residue", "No baby talk"):
        require(literal in voice_text, f"Human-voice rule is undocumented: {literal}")
    require("untrusted" in skill.lower(), "SKILL.md must treat source content as untrusted")
    require(
        (SKILL_DIR / "LICENSE").is_file() and (SKILL_DIR / "LICENSE").stat().st_size > 0,
        "Packaged eli5 license is missing",
    )
    require((SKILL_DIR / "agents" / "openai.yaml").is_file(), "Codex metadata is missing")


def main() -> int:
    cases = load_json(EVAL / "cases.json")
    invariants = load_json(EVAL / "expected-invariants.json")

    positive, negative = check_activation(cases, invariants)
    outputs = check_output_cases(cases, invariants)

    exemplars = sorted((EVAL / "expected").glob("*.md"))
    require(exemplars, "No expected exemplars found")
    for exemplar in exemplars:
        check_exemplar(exemplar, invariants)

    check_skill_documentation(invariants)

    readme = read(ROOT / "README.md")
    require("eli5" in readme.lower(), "README must document the eli5 skill")

    print(
        f"ELI5 evaluation metadata valid: {positive} positive activation cases, "
        f"{negative} negative activation cases, {outputs} output cases, {len(exemplars)} exemplars linted"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
