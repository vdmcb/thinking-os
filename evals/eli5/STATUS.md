# Evaluation status

## v0.3.0 internal preview: review fixes

Driven by a deep review of v0.2.0 (2026-08-24). Every finding maps to a check that now runs in CI or a script that runs on a transcript.

- **Subject, not document.** A new step picks the subject (the thing described; the file itself only for code and config). "How it works" may be one or two sentences saying the file describes no mechanism; the lint accepts that form and rejects narration of the document. `first-principles.md` gained tests (is it smaller, does anything stand on it, is it a claim) and worked examples for a proposal and a config. Exemplar 03 rewritten.
- **Labels name the source, not the truth.** "(true everywhere, not just here)" is retired for "(general knowledge, not from the file)". A basic fact that begins "the file says" fails the bedrock lint.
- **Numbers on the main path.** The contract now selects: main-path numbers enter exactly; others are held with their location. "Never cut a number" became "never cut a main-path number".
- **Glossary is a lookup.** A term listed under "Words you will see" may not be used earlier in the explanation; the lint checks it.
- **Duplication removed.** Baby-talk and typography rules each live in one place; `understand` steps 1 and 3 and its large-document procedure now delegate to `core/reading.md`.
- **Instruction load is measured.** The always-loaded set (SKILL, contract, output format, core writing, core execution) is capped at 3,500 words and the checker fails above it. `understand`'s load is reported, not gated.
- **Cross-skill activation.** `evals/activation-crosscheck.json` holds prompts that must activate exactly one skill; `scripts/check-activation.py` verifies them against both skills' cases and rejects a prompt that is positive for both.
- **Lint word lists are shared.** `core/lint.json` feeds both checkers; skill invariants add, never remove.
- **Documentation checks test headings, not phrases.**
- **The run is auditable.** `scripts/audit-run.py TRANSCRIPT.jsonl` finds each skill run in a Claude Code transcript and flags printed sources, diagnostics, scratch drafts, and lint runs. Run on the session that motivated v0.2.0, it reports 11 violations for that run and none for a clean one.
- **Usefulness sessions are logged.** `evals/eli5/usefulness-log.json` is read by the checker, which reports passing sessions against the gate of five.
- README gained a five-minute smoke test for ELI5.

Usefulness sessions completed: 0 of 5. Still model-judged: bedrock quality beyond the claim pattern, build order, why fidelity, number selection.


## v0.2.0 internal preview: shared core, idea-count budget, the run, the follow-up

Changes driven by a live run on a 31-page deck (2026-08-24), where the output was within contract but the run was not: page diagnostics, the source printed to the terminal, a scratch draft linted three times in public. The framework had no rule for any of it.

- The skill now sits on the shared core (`core/`): reading, writing, and execution contracts are copied into the package by `scripts/sync-core.sh` and drift-checked in CI. The office-document extraction helper ships inside the package; the sibling dependency on `understand` is gone.
- Execution contract (core/execution.md): one announce line, silent reading with the file reader, one extraction command at most, no diagnostics unless the read is empty, no scratch drafts, no lint runs.
- Budget follows ideas: one basic fact, step, or term is one idea; 250 words for up to 9, 375 for up to 14, 500 for up to 19 (hard ceiling). Structural caps: 2-5 facts, 3-8 steps, 0-6 terms. The lint computes the idea count and applies the matching ceiling.
- Held layers (side paths, numbers with locations, any step in more detail) are answered on request from the analysis already done, under the same contract. The explanation itself ends on its last fact; a trial of a printed Go deeper section was removed as unnecessary.
- Human usefulness protocol (evals/usefulness-protocol.md) is now the release gate: five sessions on real sources, two readers, no session with more than one material surprise, every follow-up answered from held analysis, no run that needs decoding.

State:

- Agent Skills structure validation: passing
- Activation metadata: 12 positive and 12 negative cases
- Reference explanations: 6 synthetic cases
- Deterministic lints in scripts/check-eli5-evals.py: sections in order, idea-count budget, 25-word sentence ceiling, structural caps, no dashes, emoji, exclamation marks, banned vocabulary, filler, or baby-talk phrases; required literals; contract, execution, and usefulness-gate documentation. All canary-tested.
- Still model-judged: bedrock quality, build order, term-before-introduction, why fidelity, number fidelity, quality of the run.
- Usefulness sessions completed: 0 of 5.

## v0.1.0 internal preview

First cut: four required sections, two optional, 400-word hard ceiling, six synthetic cases, style lints. Superseded by v0.2.0.

This is an internal preview, not a validated release. Do not create a release tag until the usefulness gate is met and scored rubric runs exist for Claude Code and Codex.
