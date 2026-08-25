#!/usr/bin/env python3
"""Deterministic checks for ELI5: eval metadata, exemplar lint, contract documentation, instruction load."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals" / "eli5"
SKILL_DIR = ROOT / "skills" / "eli5"

EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\U00002700-\U000027BF\U0001F1E6-\U0001F1FF⬀-⯿☀-⛿]")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid JSON at {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.is_file(), f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def sentences(text: str) -> list[str]:
    """Prose sentences, ignoring headings and the status line; each line or bullet is its own unit."""
    parts: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith(">"):
            continue
        stripped = re.sub(r"^(\d+\.|[-*])\s+", "", stripped)
        parts.extend(re.split(r"(?<=[.?])\s+", stripped))
    return [p for p in parts if p.strip()]


def section_body(text: str, title: str) -> str:
    match = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def bullets(body: str) -> list[str]:
    return [line.strip()[2:] for line in body.splitlines() if line.strip().startswith("- ")]


def numbered(body: str) -> list[str]:
    return [line for line in body.splitlines() if re.match(r"\s*\d+\.\s", line)]


# --- eval metadata -----------------------------------------------------------

def check_activation(cases: dict, invariants: dict) -> tuple[int, int]:
    positive = cases["activation"]["positive"]
    negative = cases["activation"]["negative"]
    minimum = invariants["minimum_activation_cases_per_class"]
    require(len(positive) >= minimum, f"Need at least {minimum} positive activation cases")
    require(len(negative) >= minimum, f"Need at least {minimum} negative activation cases")
    ids = [item.get("id") for item in positive + negative]
    require(all(ids) and len(ids) == len(set(ids)), "Activation case ids must be present and unique")
    for item in positive + negative:
        require(bool(item.get("prompt", "").strip()), f"Activation case {item['id']} needs a prompt")
        require(bool(item.get("reason", "").strip()), f"Activation case {item['id']} needs a reason")
    return len(positive), len(negative)


def check_output_cases(cases: dict, invariants: dict) -> int:
    output_cases = cases["output_cases"]
    require(len(output_cases) >= invariants["minimum_output_cases"], "Too few output-quality cases")
    ids = [item.get("id") for item in output_cases]
    require(all(ids) and len(ids) == len(set(ids)), "Output case ids must be present and unique")
    for item in output_cases:
        source = read(EVAL / item["fixture"])
        reference = read(EVAL / item["expected"])
        for literal in item.get("required_literals", []):
            require(literal in source, f"Fixture {item['fixture']} is missing required literal {literal!r}")
        for literal in item.get("expected_required_literals", []):
            require(literal in reference, f"Expected {item['expected']} is missing required literal {literal!r}")
    return len(output_cases)


# --- exemplar lint -------------------------------------------------------------

def check_exemplar(path: Path, invariants: dict, lint: dict) -> None:
    text = read(path)
    low = text.lower()
    name = path.name
    core = invariants["core_output"]

    headings = re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
    required = invariants["required_sections"]
    optional = invariants["optional_sections"]
    for section in required:
        require(section in headings, f"{name}: missing required section '{section}' (structure lint)")
    positions = [headings.index(section) for section in required]
    require(positions == sorted(positions), f"{name}: required sections are out of order (structure lint)")
    for heading in headings:
        require(heading in required or heading in optional, f"{name}: unexpected section '{heading}' (structure lint)")

    facts = bullets(section_body(text, "The basic facts"))
    steps = numbered(section_body(text, "How it works"))
    terms = bullets(section_body(text, "Words you will see"))
    limits = core["basic_facts_count"]
    require(limits["minimum"] <= len(facts) <= limits["maximum"],
            f"{name}: {len(facts)} basic facts, expected {limits['minimum']}-{limits['maximum']} (structure lint)")
    limits = core["terms_count"]
    require(limits["minimum"] <= len(terms) <= limits["maximum"],
            f"{name}: {len(terms)} terms, expected {limits['minimum']}-{limits['maximum']} (structure lint)")

    # How it works: numbered steps, or one or two sentences saying the file gives no mechanism.
    how = section_body(text, "How it works").strip()
    if steps:
        limits = core["steps_count"]
        require(limits["minimum"] <= len(steps) <= limits["maximum"],
                f"{name}: {len(steps)} steps, expected {limits['minimum']}-{limits['maximum']} (structure lint)")
    else:
        require("does not describe" in how, f"{name}: How it works has no steps and does not say the file describes no mechanism (structure lint)")
        require(len(sentences(how)) <= 2, f"{name}: How it works without steps must be one or two sentences (structure lint)")
        require("the document" not in how.lower() or "describe" in how.lower(),
                f"{name}: How it works narrates the document (structure lint)")

    # Budget follows ideas, not pages.
    ideas = len(facts) + len(steps) + len(terms)
    words = len(text.split())
    ceiling = core["hard_ceiling_words"]
    for tier in core["word_ceiling_by_idea_count"]:
        if ideas <= tier["max_ideas"]:
            ceiling = tier["max_words"]
            break
    require(words <= ceiling, f"{name}: {words} words exceeds the {ceiling}-word ceiling for {ideas} ideas (budget lint)")

    # A glossary term is a lookup for the file; it is not used earlier in the explanation.
    if terms:
        before = text[: text.index("## Words you will see")]
        before_low = before.lower()
        for term_line in terms:
            term = term_line.split(":", 1)[0].strip().lower()
            require(term and not re.search(rf"(?<![\w/]){re.escape(term)}(?![\w/-])", before_low),
                    f"{name}: glossary term {term!r} is used before the glossary (term lint)")

    # A basic fact is not a claim the file makes.
    for fact in facts:
        require(not re.match(r"(the (file|deck|memo|document) (says|claims|states))", fact.lower()),
                f"{name}: basic fact is a claim attributed to the file, not bedrock: {fact[:60]!r} (bedrock lint)")

    for sentence in sentences(text):
        count = len(sentence.split())
        require(count <= core["max_words_per_sentence"],
                f"{name}: sentence of {count} words exceeds {core['max_words_per_sentence']}: {sentence[:60]!r} (sentence lint)")

    for ch in lint["forbidden_characters"]:
        require(ch not in text, f"{name}: forbidden character {ch!r} (cognitive-load lint)")
    for word in lint["forbidden_words"]:
        require(not re.search(rf"\b{re.escape(word)}\b", low), f"{name}: forbidden word {word!r} (cognitive-load lint)")
    for phrase in lint["forbidden_phrases"]:
        require(phrase not in low, f"{name}: forbidden phrase {phrase!r} (cognitive-load lint)")
    require(not EMOJI_RE.search(text), f"{name}: emoji or decorative symbol (cognitive-load lint)")
    require("|" not in text, f"{name}: table or pipe character (structure lint)")
    for retired in invariants.get("retired_labels", []):
        require(retired not in low, f"{name}: retired label {retired!r} (label lint)")
    for line in text.splitlines():
        if "**" in line:
            require(line.lstrip().startswith(">"), f"{name}: bold outside the status line (typography lint)")


# --- contract documentation ---------------------------------------------------

def headings_of(text: str) -> set[str]:
    return {h.strip() for h in re.findall(r"^#{1,3} (.+)$", text, flags=re.MULTILINE)}


def check_skill_documentation(invariants: dict) -> None:
    skill = read(SKILL_DIR / "SKILL.md")
    contract = read(SKILL_DIR / "references" / "eli5-contract.md")
    output_format = read(SKILL_DIR / "references" / "output-format.md")
    first_principles = read(ROOT / invariants["first_principles"]["reference"])
    writing = read(ROOT / invariants["cognitive_load"]["reference"])
    execution = read(ROOT / invariants["execution"]["reference"])
    template = read(SKILL_DIR / "assets" / "eli5-explanation.md")

    for section in invariants["required_sections"] + invariants["optional_sections"]:
        require(section in headings_of(output_format), f"Output format does not document section '{section}'")
        require(section in headings_of(template), f"Template does not include section '{section}'")
    for label in invariants["labels"]:
        require(label in contract and label in output_format, f"Label must appear in both contract and output format: {label!r}")

    core = invariants["core_output"]
    for tier in core["word_ceiling_by_idea_count"]:
        require(f"up to {tier['max_ideas']}" in output_format and f"{tier['max_words']} words" in output_format,
                f"Output format must document the {tier['max_words']}-word tier for up to {tier['max_ideas']} ideas")
    require(f"{core['hard_ceiling_words']} words" in output_format, "Output format must state the hard ceiling")

    skill_headings = headings_of(skill)
    for heading in ("The run", "Pick the subject", "Find the bedrock", "Choose the numbers", "Translate the words", "Follow-up", "Failure"):
        require(any(h.endswith(heading) for h in skill_headings), f"SKILL.md lacks the '{heading}' section")
    for heading in ("The visible run", "Held layers"):
        require(heading in headings_of(execution), f"Execution contract lacks the '{heading}' section")
    for heading in ("Reader burden is the binding constraint", "Budgets follow ideas, not pages", "The read-aloud test"):
        require(heading in headings_of(writing), f"Core writing contract lacks the '{heading}' section")
    for heading in ("Tests", "Worked examples"):
        require(heading in headings_of(first_principles), f"First-principles reference lacks the '{heading}' section")
    for kind in invariants["first_principles"]["bedrock_kinds"]:
        require(kind in first_principles.lower(), f"First-principles reference does not name bedrock kind: {kind}")
    for example in ("proposal", "config", "mechanism", "code"):
        require(example in first_principles.lower(), f"First-principles worked examples lack a {example} case")
    require("No baby talk" in output_format, "Output format must carry the baby-talk rule")
    require("does not describe" in output_format, "Output format must allow a no-mechanism How it works")
    require("main path" in contract and "main path" in output_format, "Number selection rule must be documented")
    require("untrusted" in skill.lower(), "SKILL.md must treat source content as untrusted")
    require((ROOT / invariants["usefulness_gate"]["protocol"]).is_file(), "Missing usefulness protocol")
    require((ROOT / invariants["execution"]["audit"]).is_file(), "Missing run audit script")
    require((ROOT / invariants["cross_skill_activation"]).is_file(), "Missing cross-skill activation cases")
    require((SKILL_DIR / "LICENSE").stat().st_size > 0, "Packaged eli5 license is missing")
    require((SKILL_DIR / "agents" / "openai.yaml").is_file(), "Codex metadata is missing")


def check_instruction_load(invariants: dict) -> str:
    load = invariants["instruction_load"]
    always = sum(len(read(ROOT / f).split()) for f in load["always_loaded"])
    require(always <= load["max_always_loaded_words"],
            f"eli5 always-loaded instructions are {always} words; ceiling is {load['max_always_loaded_words']} (instruction-load lint)")
    reported = sum(len(read(ROOT / f).split()) for f in load.get("reported_only", []))
    return f"instruction load: eli5 {always} words (ceiling {load['max_always_loaded_words']}), understand {reported} words (reported only)"


def check_usefulness_log(invariants: dict) -> str:
    log = load_json(ROOT / invariants["usefulness_gate"]["log"])
    sessions = log.get("sessions", [])
    passed = 0
    for s in sessions:
        for key in ("date", "reader", "source_type", "material_surprises", "followup_from_held", "run_clean", "passed"):
            require(key in s, f"Usefulness session missing field {key!r}")
        passed += bool(s["passed"])
    need = invariants["usefulness_gate"]["minimum_sessions_before_release"]
    return f"usefulness gate: {passed} of {need} passing sessions logged"


def main() -> int:
    cases = load_json(EVAL / "cases.json")
    invariants = load_json(EVAL / "expected-invariants.json")
    shared = load_json(ROOT / invariants["cognitive_load"]["shared_lint"])
    voice = invariants["cognitive_load"]
    lint = {
        "forbidden_characters": shared["forbidden_characters"] + voice["additional_forbidden_characters"],
        "forbidden_words": shared["forbidden_words"] + voice["additional_forbidden_words"],
        "forbidden_phrases": shared["forbidden_phrases"] + voice["additional_forbidden_phrases"],
    }

    positive, negative = check_activation(cases, invariants)
    outputs = check_output_cases(cases, invariants)
    exemplars = sorted((EVAL / "expected").glob("*.md"))
    require(exemplars, "No expected exemplars found")
    for exemplar in exemplars:
        check_exemplar(exemplar, invariants, lint)
    check_skill_documentation(invariants)
    load_line = check_instruction_load(invariants)
    gate_line = check_usefulness_log(invariants)
    require("eli5" in read(ROOT / "README.md").lower(), "README must document the eli5 skill")

    print(f"ELI5 evaluation metadata valid: {positive} positive, {negative} negative activation cases, "
          f"{outputs} output cases, {len(exemplars)} exemplars linted; {load_line}; {gate_line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
