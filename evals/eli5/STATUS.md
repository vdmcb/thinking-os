# Evaluation status

## v0.1.0 internal preview

First cut of the ELI5 skill. The output is a short explanation in four required sections (What this is, The basic facts, How it works, Why it is this way) and two optional ones (Words you will see, What the file does not say), under a 400-word hard ceiling. The basic facts are the first-principles bedrock: the smallest true things the file rests on, each sorted as stated in the file, true everywhere, or assumed by the file.

- Agent Skills structure validation: passing
- Activation metadata: 12 positive and 12 negative cases
- Reference explanations: 6 synthetic cases (technical rule, source code, undefined-vocabulary proposal, numeric policy, embedded instruction, CI config)
- Deterministic lints in scripts/check-eli5-evals.py: required sections in order, 400-word ceiling, 25-word sentence ceiling, two to five basic facts, no dashes, emoji, exclamation marks, banned vocabulary, filler, or baby-talk phrases in any exemplar; required literals in fixtures and exemplars; contract vocabulary documented in the skill. All canary-tested.
- Still model-judged, not lint-checked: bedrock quality, build order, term-before-introduction, why fidelity, number fidelity.
- Scored model-level rubric runs in Claude Code and Codex: pending.

This is an internal preview, not a validated release. Do not create a release tag until authenticated Claude Code and Codex runs are scored against the rubric and release blockers.
