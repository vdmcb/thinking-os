# Changelog

Plugin releases follow semantic versioning. The version lives in
`.claude-plugin/plugin.json` and the matching marketplace entry in
`.claude-plugin/marketplace.json`; the two must move together
(`scripts/check-plugin.py` enforces this). Cowork organization
marketplaces with "Sync automatically" enabled re-sync when a pull
request containing a version bump merges to `main`, so every release
is a PR that bumps both files and adds an entry here.

## [Unreleased]

- `understand` skill 2.1.1 (plugin version unchanged): the independent audit
  is capped at three rounds, with round three limited to deleting or
  downgrading unsupported claims; page-less sources (HTML, Markdown, text)
  are cited by their nearest heading; `evals/understand/RESULTS-2026-08-28.md`
  records the five-document live trial as derived data. Each source asset is
  now read once into an evidence packet that the independent auditor reuses;
  long runs permit at most two outcome-level progress updates, and PDF reading
  avoids contact-sheet and image-composition detours.

## [0.1.0] - 2026-08-28

- Initial plugin marketplace release.
- Packages the `understand` (2.1.0) and `eli5` (0.3.0) skills as the
  `thinking-os` plugin, installable in Claude Cowork and Claude Code.
- Validated against the shared-core layout and the Understand 2.1 audited
  stakeholder-question output contract released in Thinking OS v2.1.0.
