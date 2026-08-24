# Evaluation status

## v0.2.0 internal preview: shared core, idea-count budget, the run, the follow-up

Changes driven by a live run on a 31-page deck (2026-08-24), where the output was within contract but the run was not: page diagnostics, the source printed to the terminal, a scratch draft linted three times in public. The framework had no rule for any of it.

- The skill now sits on the shared core (`core/`): reading, writing, and execution contracts are copied into the package by `scripts/sync-core.sh` and drift-checked in CI. The office-document extraction helper ships inside the package; the sibling dependency on `understand` is gone.
- Execution contract (core/execution.md): one announce line, silent reading with the file reader, one extraction command at most, no diagnostics unless the read is empty, no scratch drafts, no lint runs.
- Budget follows ideas: one basic fact, step, or term is one idea; 250 words for up to 9, 375 for up to 14, 500 for up to 19 (hard ceiling). Structural caps: 2-5 facts, 3-8 steps, 0-6 terms. The lint computes the idea count and applies the matching ceiling.
- The output is the first move: a required last section, Go deeper, names what was held for this file (side paths, numbers with locations, any step in more detail). Follow-up answers come from the held analysis under the same contract.
- Human usefulness protocol (evals/usefulness-protocol.md) is now the release gate: five sessions on real sources, two readers, no session with more than one material surprise, every follow-up answered from held analysis, no run that needs decoding.

State:

- Agent Skills structure validation: passing
- Activation metadata: 12 positive and 12 negative cases
- Reference explanations: 6 synthetic cases, each ending with a specific Go deeper section
- Deterministic lints in scripts/check-eli5-evals.py: sections in order with Go deeper last, idea-count budget, 25-word sentence ceiling, structural caps, no dashes, emoji, exclamation marks, banned vocabulary, filler, or baby-talk phrases; required literals; contract, execution, and usefulness-gate documentation. All canary-tested.
- Still model-judged: bedrock quality, build order, term-before-introduction, why fidelity, number fidelity, specificity of Go deeper, quality of the run.
- Usefulness sessions completed: 0 of 5.

## v0.1.0 internal preview

First cut: four required sections, two optional, 400-word hard ceiling, six synthetic cases, style lints. Superseded by v0.2.0.

This is an internal preview, not a validated release. Do not create a release tag until the usefulness gate is met and scored rubric runs exist for Claude Code and Codex.
