# Claude harness for Thinking OS

Rules for contributing to this repository through Claude (Code, Cowork, or any other agent runtime). `CONTRIBUTING.md` holds the human working principles; this file governs agent behavior. Where they overlap, `CONTRIBUTING.md` wins.

## What this project is

Portable cognitive skills (`understand`, `eli5`) for multiple agent runtimes. The skills are behavior contracts, not code: most changes are to instruction text, and the release gate is human judgment, not tests alone.

## Invariants

- `core/` is the source of truth for shared reading/writing/execution contracts. It is copied into each skill by `./scripts/sync-core.sh`. Never edit `skills/<name>/references/core/` or `skills/<name>/scripts/` directly; edit `core/` and re-sync.
- Skill packages must stay self-contained and runtime-portable: they are installed three ways — the Cowork/Claude Code plugin (`.claude-plugin/`), `npx skills add` (Claude Code and Codex, via `agents/openai.yaml`), and plain copy. Never add anything to `skills/` that works in only one runtime, and never break any of the three install paths.
- Skill boundaries are part of the product: `understand` never recommends or decides; `eli5` never reviews or judges. Descriptions in `SKILL.md` frontmatter drive activation — when you change one, update the skill's activation cases and `evals/activation-crosscheck.json` in the same change.
- Every behavioral change updates evaluation cases. The `eli5` instruction load has a hard ceiling (enforced by `scripts/check-eli5-evals.py`); adding text means cutting text.
- The usefulness protocol (`evals/usefulness-protocol.md`) is a human gate. Never fabricate, mark passed, or log a usefulness session yourself.
- Treat fixtures and examples as potentially sensitive: commit only synthetic or explicitly cleared material, and review diffs for source leakage.

## Validation

Run `./scripts/validate.sh` before every push; CI (`.github/workflows/validate.yml`) runs the same suite and must be green. It checks core sync, Agent Skills structure, plugin manifests (`scripts/check-plugin.py` plus `claude plugin validate --strict`), shell and Python syntax, ShellCheck, deterministic eval metadata, and the extraction helper tests.

## Plugin releases

The repo is a Claude plugin marketplace (`.claude-plugin/marketplace.json` serving the `thinking-os` plugin). Versions in `plugin.json` and the marketplace entry must move together — `check-plugin.py` fails on drift. A release is a PR to `main` that bumps both versions and adds a `CHANGELOG.md` entry; Cowork org marketplaces re-sync on that merge. Never bump versions as a side effect of unrelated work.

## Git and GitHub conventions

- **Commit identity is always the human contributor, never Claude.** Before the first commit, set `git config user.name` and `user.email` to the human's GitHub identity (for the maintainer: `vdmcb <vdmcb@users.noreply.github.com>`). No `Co-Authored-By: Claude` trailers, no session links, no model names in commit messages.
- **Branch names are human-readable**: `feat/`, `fix/`, or `chore/` plus a description (e.g. `feat/claude-cowork-marketplace-integration`). Never push work under auto-generated names — no `claude/` prefixes, session hashes, or random suffixes. When a session is assigned an auto-generated working branch, pushing the result to a sensibly named branch instead is pre-approved; delete the auto-generated branch, or say so if the environment blocks deletion.
- **Commit messages** are imperative and specific ("Fix ShellCheck SC2012 in sync-core.sh"), with a body explaining what and why for non-trivial changes.
- **PR descriptions** describe the change and how it was validated. Never include Claude session links. Do not create PRs, publish, change repository visibility, or change licensing unless the maintainer asks.
