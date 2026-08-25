# Core

The shared part of every Thinking OS skill: how to read a source faithfully, how to write for a human reader, and what the visible run looks like. Skills are lenses on top of this core; they should contain only what differs between them.

`core/` is the source of truth. Skills must stay self-contained so that `npx skills add` and a plain copy both work, so the core is copied into each skill package:

- `core/references/*.md` → `skills/<name>/references/core/`
- `core/scripts/*.sh` → `skills/<name>/scripts/`

Run `./scripts/sync-core.sh` after editing anything under `core/`. `./scripts/validate.sh` fails when a packaged copy differs from the source.

Never edit a file under `skills/<name>/references/core/` or `skills/<name>/scripts/` directly.
