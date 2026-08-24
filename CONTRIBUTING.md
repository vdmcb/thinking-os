# Contributing

Thinking OS is currently a private internal experiment.

## Working principles

- Preserve source faithfulness over impressive prose.
- Keep `understand` within the understanding boundary. Do not add recommendations or decision-making.
- Treat examples and fixtures as potentially sensitive. Commit only synthetic, anonymized, or explicitly cleared material.
- Keep one shared behavior contract for Claude Code and Codex.
- Add or update evaluation cases for every behavioral change.

## Development workflow

1. Create a focused branch.
2. Add a failing regression fixture or deterministic check where applicable.
3. Make the smallest implementation change.
4. Run `./scripts/validate.sh`.
5. Review the generated diff for source leakage, secrets, and behavioral drift.

Do not publish, change repository visibility, or apply an open-source license without maintainer approval.
