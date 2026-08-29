#!/usr/bin/env python3
"""Deterministic checks for Understand evaluation metadata."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evals" / "understand"


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid JSON at {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    cases = load_json(EVAL / "cases.json")
    invariants = load_json(EVAL / "expected-invariants.json")

    positive = cases.get("activation", {}).get("positive", [])
    negative = cases.get("activation", {}).get("negative", [])
    minimum = invariants.get("minimum_activation_cases_per_class", 10)
    require(len(positive) >= minimum, f"Need at least {minimum} positive activation cases")
    require(len(negative) >= minimum, f"Need at least {minimum} negative activation cases")

    all_activation = positive + negative
    ids = [item.get("id") for item in all_activation]
    require(all(ids), "Every activation case needs an id")
    require(len(ids) == len(set(ids)), "Activation case ids must be unique")
    for item in all_activation:
        require(bool(item.get("prompt", "").strip()), f"Activation case {item['id']} needs a prompt")
        require(bool(item.get("reason", "").strip()), f"Activation case {item['id']} needs a reason")

    output_cases = cases.get("output_cases", [])
    require(len(output_cases) >= 5, "Need at least five output-quality cases")
    output_ids = [item.get("id") for item in output_cases]
    require(len(output_ids) == len(set(output_ids)), "Output case ids must be unique")

    for item in output_cases:
        fixture = EVAL / item["fixture"]
        expected = EVAL / item["expected"]
        require(fixture.is_file(), f"Missing fixture: {fixture}")
        require(expected.is_file(), f"Missing expected reference: {expected}")
        source = fixture.read_text(encoding="utf-8")
        for literal in item.get("required_literals", []):
            require(literal in source, f"Fixture {fixture.name} is missing required literal {literal!r}")
        reference = expected.read_text(encoding="utf-8")
        for literal in item.get("expected_required_literals", []):
            require(
                literal in reference,
                f"Expected reference {expected.name} is missing required literal {literal!r}",
            )

    required_sections = invariants.get("required_sections", [])
    require(
        len(required_sections) >= 5,
        "required_sections must define the five default-output sections",
    )

    skill = (ROOT / "skills" / "understand" / "SKILL.md").read_text(encoding="utf-8")
    output_format = (ROOT / "skills" / "understand" / "references" / "output-format.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    examples = (ROOT / "skills" / "understand" / "references" / "examples.md").read_text(encoding="utf-8")
    for section in required_sections:
        require(
            section in skill or section in output_format,
            f"required_sections entry is undocumented: {section}",
        )

    reference_analysis_sections = invariants.get("reference_analysis_sections", [])
    require(
        len(reference_analysis_sections) >= 7,
        "reference_analysis_sections must define the seven optional reference-analysis headers",
    )
    for section in reference_analysis_sections:
        require(
            section in output_format,
            f"reference_analysis_sections entry is undocumented in output-format.md: {section}",
        )

    question_requirements = invariants.get("question_requirements", [])
    require(len(question_requirements) >= 6, "Question contract must define at least six quality requirements")
    for literal in ("Claim challenged", "Source", "Pushback", "Why the answer matters", "Answer required"):
        require(literal in output_format, f"Question output field is undocumented: {literal}")

    forbidden_questions = invariants.get("forbidden_generic_question_patterns", [])
    require(len(forbidden_questions) >= 5, "Need at least five forbidden generic question patterns")

    voice = invariants.get("cognitive_load", {})
    require(bool(voice), "Invariants must define the cognitive_load contract")
    voice_doc = ROOT / voice.get("reference", "skills/understand/references/core/writing.md")
    require(voice_doc.is_file(), f"Missing human-voice reference: {voice_doc}")
    voice_text = voice_doc.read_text(encoding="utf-8")
    for literal in ("read-aloud test", "One idea per sentence", "chatbot residue"):
        require(literal in voice_text, f"Human-voice rule is undocumented: {literal}")

    audit_prompt = ROOT / "skills" / "understand" / "references" / "audit-prompt.md"
    require(audit_prompt.is_file(), f"Missing audit-prompt reference: {audit_prompt}")
    audit_text = audit_prompt.read_text(encoding="utf-8")
    for literal in ("SUPPORTED", "UNSUPPORTED", "STRETCH", "MISQUOTE", "direction"):
        require(literal in audit_text, f"Audit verdict vocabulary is undocumented: {literal}")
    for literal in ("audit-prompt.md", "evaluative", "in production"):
        require(literal in skill, f"Audit stage is undocumented in SKILL.md: {literal}")
    audit = invariants.get("audit", {})
    require(audit.get("independent_agent_required") is True, "Invariants must require an independent audit agent")
    require(audit.get("source_read_passes") == 1, "Invariants must limit source reading to one pass")
    require(audit.get("auditor_source_access") is False, "The auditor must not receive the original source")
    require(
        audit.get("audit_basis") == "evidence packet captured during the single source-read pass",
        "The audit basis must be the evidence packet from the single source-read pass",
    )
    require(audit.get("missing_packet_evidence_verdict") == "UNVERIFIABLE", "Packet gaps need an explicit verdict")
    require(audit.get("max_rounds") == 3, "Audit rounds must be capped at three")
    ordinal = {1: "first", 2: "second", 3: "third"}[audit["max_rounds"]]
    for literal in (f"after the {ordinal} round", "deletion"):
        require(literal in skill, f"Audit round cap is undocumented in SKILL.md: {literal}")
        require(literal in audit_text, f"Audit round cap is undocumented in audit-prompt.md: {literal}")
    for literal in ("evidence packet", "Never give the auditor the original asset", "UNVERIFIABLE"):
        require(literal in skill, f"Single-read audit contract is undocumented in SKILL.md: {literal}")
    for literal in ("EVIDENCE_PACKET", "Do not open, extract, render", "UNVERIFIABLE", "Never reopen or re-extract"):
        require(literal in audit_text, f"Single-read audit contract is undocumented in audit-prompt.md: {literal}")
    visible_run = invariants.get("visible_run", {})
    require(visible_run.get("initial_announcement") == 1, "Visible run must have one initial announcement")
    require(visible_run.get("max_progress_updates") == 2, "Visible run must cap progress updates at two")
    require(visible_run.get("progress_threshold_seconds") == 60, "Visible run progress threshold must be 60 seconds")
    require(visible_run.get("command_narration_forbidden") is True, "Visible run must forbid command narration")
    for literal in ("at most two outcome-level progress updates", "Never narrate commands", "one initial pass"):
        require(literal in skill, f"Visible run contract is undocumented: {literal}")

    # Deterministic cognitive-load lint over every expected output exemplar.
    # Exemplars teach the format; an AI-patterned exemplar would teach the
    # pattern. Fixtures are exempt: they simulate the documents under review
    # and may legitimately contain every pattern we ban.
    import re
    core_lint = load_json(ROOT / "core" / "lint.json")
    forbidden_chars = sorted(set(core_lint["forbidden_characters"]) | set(voice.get("forbidden_characters", [])))
    forbidden_words = sorted(set(core_lint["forbidden_words"]) | set(voice.get("forbidden_words", [])))
    forbidden_phrases = sorted(set(core_lint["forbidden_phrases"]) | set(voice.get("forbidden_phrases", [])))
    emoji_re = re.compile(
        "[\U0001F000-\U0001FAFF\U00002700-\U000027BF\U0001F1E6-\U0001F1FF\u2B00-\u2BFF\u2600-\u26FF]"
    )
    for exemplar in sorted((EVAL / "expected").glob("*.md")):
        text = exemplar.read_text(encoding="utf-8")
        low = text.lower()
        # Quoted source text is verbatim by contract (see references/core/writing.md),
        # so forbidden characters are exempt inside straight double-quoted spans.
        outside_quotes = re.sub(r'"[^"\n]*?"', "", text)
        for ch in forbidden_chars:
            require(
                ch not in outside_quotes,
                f"{exemplar.name}: forbidden character {ch!r} outside quoted text (cognitive-load lint)",
            )
        for word in forbidden_words:
            require(
                not re.search(rf"\b{re.escape(word)}\b", low),
                f"{exemplar.name}: forbidden word {word!r} (cognitive-load lint)",
            )
        for phrase in forbidden_phrases:
            require(phrase not in low, f"{exemplar.name}: forbidden phrase {phrase!r} (cognitive-load lint)")
        require(
            not emoji_re.search(text),
            f"{exemplar.name}: emoji or decorative symbol (cognitive-load lint)",
        )

    qlang = invariants.get("question_language", {})
    require(bool(qlang), "Invariants must define the question_language contract")
    jargon = qlang.get("forbidden_in_v2_exemplar_questions", [])
    v2_from = int(qlang.get("applies_to_expected_files_numbered_from", 14))
    for exemplar in sorted((EVAL / "expected").glob("*.md")):
        m = re.match(r"(\d+)-", exemplar.name)
        if not m or int(m.group(1)) < v2_from:
            continue
        text = exemplar.read_text(encoding="utf-8")
        low = text.lower()
        for term in jargon:
            require(
                term not in low,
                f"{exemplar.name}: analyst jargon {term!r} in a v2 exemplar (question-language lint)",
            )
        ceiling = invariants.get("core_packet", {}).get("hard_ceiling_words", 600)
        words = len(text.split())
        require(
            words <= ceiling,
            f"{exemplar.name}: {words} words exceeds the {ceiling}-word default-output ceiling (budget lint)",
        )
        for literal in ("Stance:", "Q1:", "Q2:", "Q3:", "## Follow-up questions"):
            require(literal in text, f"{exemplar.name}: missing {literal!r} (structure lint)")
        require("\nHeld: " in text, f"{exemplar.name}: missing source-specific held line (structure lint)")
        followups = text.split("## Follow-up questions", 1)[1]
        numbered = re.findall(r"(?m)^[123]\. ", followups)
        require(
            len(numbered) == 3,
            f"{exemplar.name}: expected exactly three numbered follow-up questions",
        )

    core = invariants.get("core_packet", {})
    require(bool(core), "Invariants must define the core_packet contract")
    require(core.get("hard_ceiling_words") == 600, "Default output hard ceiling must be 600 words")
    require(
        core.get("answered_question_roles") == ["state", "decision", "resources"],
        "Answered questions must cover state, decision, and resources",
    )
    require(
        core.get("follow_ups_do_not_repeat_answered_questions") is True,
        "Follow-up questions must not repeat answered questions",
    )
    require(core.get("held_line_required") is True, "Default output must end with a held line")
    require(core.get("reference_analysis_on_request_only") is True, "Reference analysis must be on-request only")
    understand_summary = readme.split("## Understand", 1)[1].split("## ELI5", 1)[0]
    understand_use = readme.split("## Use", 1)[1].split("## Five-minute smoke test", 1)[0]
    understand_smoke = readme.split("## Five-minute smoke test", 1)[1].split(
        "## Five-minute smoke test for ELI5", 1
    )[0]
    good_output_example = examples.split("### Good output shape", 1)[1].split("### Bad output", 1)[0]
    for section_name, section in (
        ("Understand summary", understand_summary),
        ("Understand use section", understand_use),
        ("Understand smoke test", understand_smoke),
    ):
        require("`Held:`" in section, f"README {section_name} must document the final `Held:` line")
    require("\nHeld: " in good_output_example, "Good output example must include the final Held: line")
    for literal in ("600 words", "Follow-up questions", "Stance:", "Q1:", "Q2:", "Q3:",
                    "Evidence-first", "Responsiveness", "Genericity"):
        require(literal in output_format, f"Default output contract is undocumented: {literal}")
    for literal in ("first principles", "evidence-first", "separate pass"):
        require(literal in skill.lower(), f"Understand workflow is undocumented in SKILL.md: {literal}")

    qgen = invariants.get("question_generation", {})
    require(bool(qgen), "Invariants must define the question_generation contract")
    require(qgen.get("order") == ["evidence-first", "audit-fallback"], "Question generation must be evidence-first")

    status_conflict_requirements = invariants.get("value_status_conflict_requirements", [])
    require(
        len(status_conflict_requirements) >= 3,
        "Value-status conflicts must define detection, classification, and propagation requirements",
    )
    status_contract = (skill + "\n" + output_format + "\n" + (
        ROOT / "skills" / "understand" / "references" / "understanding-contract.md"
    ).read_text(encoding="utf-8")).lower()
    for literal in ("contradictory status cues", "unknown status", "dependent calculations"):
        require(literal in status_contract, f"Value-status conflict behavior is undocumented: {literal}")

    comparison_requirements = invariants.get("option_comparison_requirements", [])
    require(
        len(comparison_requirements) >= 4,
        "Option comparisons must define selection logic, common-basis tests, missing-cell handling, and pushback",
    )
    for literal in ("option-selection logic", "common comparison basis", "missing cells"):
        require(literal in status_contract, f"Asymmetric option-comparison behavior is undocumented: {literal}")

    evidence_reach_requirements = invariants.get("evidence_reach_requirements", [])
    require(
        len(evidence_reach_requirements) >= 4,
        "Evidence reach must define direct support, inferential hops, downstream limits, and pushback",
    )
    for literal in ("narrowest proposition", "inferential hops", "evidence-to-claim bridge"):
        require(literal in status_contract, f"Evidence-reach behavior is undocumented: {literal}")

    authorization_requirements = invariants.get("authorization_perimeter_requirements", [])
    require(
        len(authorization_requirements) >= 4,
        "Authorization perimeter must distinguish the request, implied commitments, commitment dimensions, and pushback",
    )
    for literal in ("authorization perimeter", "explicit decision", "implied commitments", "authorization schedule"):
        require(literal in status_contract, f"Authorization-perimeter behavior is undocumented: {literal}")

    accountability_requirements = invariants.get("operational_accountability_requirements", [])
    require(
        len(accountability_requirements) >= 4,
        "Operational accountability must distinguish monitoring, authority, exception response, and escalation",
    )
    for literal in ("end-to-end accountability", "decision rights", "accountability and exception matrix"):
        require(literal in status_contract, f"Operational-accountability behavior is undocumented: {literal}")

    counting_unit_requirements = invariants.get("counting_unit_requirements", [])
    require(
        len(counting_unit_requirements) >= 4,
        "Counting units must define identity drift, safe comparison, denominator alignment, and pushback",
    )
    for literal in ("counting-unit identity", "counting-unit dictionary", "population bridge", "double counting"):
        require(literal in status_contract, f"Counting-unit behavior is undocumented: {literal}")

    # The private benchmark must never enter the repository. Synthetic document
    # fixtures are generated in temporary directories during tests, so committed
    # PDF files are unnecessary for this preview.
    ignored_artifact_roots = {".git", ".tmp", ".cache", "node_modules", "dist"}
    committed_pdf_candidates = [
        path
        for path in ROOT.rglob("*.pdf")
        if not ignored_artifact_roots.intersection(path.relative_to(ROOT).parts)
    ]
    require(
        not committed_pdf_candidates,
        "PDF artifacts are forbidden in the repository: "
        + ", ".join(str(path.relative_to(ROOT)) for path in committed_pdf_candidates),
    )

    logo = ROOT / "assets" / "rebeldot-logo.svg"
    packaged_license = ROOT / "skills" / "understand" / "LICENSE"
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require(logo.is_file() and logo.stat().st_size > 0, "RebelDot logo asset is missing")
    require(packaged_license.is_file() and packaged_license.stat().st_size > 0, "Packaged skill license is missing")
    require("main supporter" in readme.lower(), "README must identify the main supporter")

    print(
        f"Evaluation metadata valid: {len(positive)} positive activation cases, "
        f"{len(negative)} negative activation cases, {len(output_cases)} output cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
