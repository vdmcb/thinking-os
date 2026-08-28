# Changelog

Plugin releases follow semantic versioning. The version lives in
`.claude-plugin/plugin.json` and the matching marketplace entry in
`.claude-plugin/marketplace.json`; the two must move together
(`scripts/check-plugin.py` enforces this). Cowork organization
marketplaces with "Sync automatically" enabled re-sync when a pull
request containing a version bump merges to `main`, so every release
is a PR that bumps both files and adds an entry here.

## [0.1.0] - 2026-08-28

- Initial plugin marketplace release.
- Packages the `understand` (2.1.0) and `eli5` (0.3.0) skills as the
  `thinking-os` plugin, installable in Claude Cowork and Claude Code.
- Validated against the shared-core layout and the Understand 2.1 audited
  stakeholder-question output contract released in Thinking OS v2.1.0.
