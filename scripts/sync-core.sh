#!/usr/bin/env bash
# Copy the shared core into every skill package, or check that the copies match.
# Usage: scripts/sync-core.sh [--check]
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$repo_root"

mode="sync"
if [[ "${1:-}" == "--check" ]]; then
  mode="check"
fi

status=0
synced=()
for skill_dir in skills/*/; do
  skill="${skill_dir%/}"
  synced+=("$skill")
  for src in core/references/*.md; do
    dest="$skill/references/core/$(basename "$src")"
    if [[ "$mode" == "check" ]]; then
      if ! cmp -s "$src" "$dest"; then
        printf 'DRIFT: %s differs from %s (run scripts/sync-core.sh)\n' "$dest" "$src" >&2
        status=1
      fi
    else
      mkdir -p "$(dirname "$dest")"
      cp "$src" "$dest"
    fi
  done
  for src in core/scripts/*.sh; do
    dest="$skill/scripts/$(basename "$src")"
    if [[ "$mode" == "check" ]]; then
      if ! cmp -s "$src" "$dest"; then
        printf 'DRIFT: %s differs from %s (run scripts/sync-core.sh)\n' "$dest" "$src" >&2
        status=1
      fi
    else
      mkdir -p "$(dirname "$dest")"
      cp -p "$src" "$dest"
    fi
  done
done

if [[ "$mode" == "check" ]]; then
  if (( status == 0 )); then
    printf 'Core copies are in sync.\n'
  fi
  exit "$status"
fi

printf 'Core synced into %s\n' "${synced[*]}"
