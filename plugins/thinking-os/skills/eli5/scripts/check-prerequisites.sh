#!/usr/bin/env bash
set -euo pipefail

fail=0

if ! command -v node >/dev/null 2>&1; then
  printf 'Missing prerequisite: Node.js 20 or later is required.\n' >&2
  fail=1
else
  node_major="$(node -p 'Number(process.versions.node.split(".")[0])' 2>/dev/null || printf '0')"
  if [[ ! "$node_major" =~ ^[0-9]+$ ]] || (( node_major < 20 )); then
    printf 'Unsupported Node.js version: found %s; version 20 or later is required.\n' "$(node --version 2>/dev/null || printf 'unknown')" >&2
    fail=1
  fi
fi

if ! command -v npx >/dev/null 2>&1; then
  printf 'Missing prerequisite: npx is required to run the local AnyDoc fallback.\n' >&2
  fail=1
fi

if (( fail != 0 )); then
  exit 69
fi

# Advisory only: the page-preserving PDF path (SKILL.md, step 2 of the reading
# order) uses poppler. Its absence does not fail this check because the AnyDoc
# fallback and host-native readers remain available, but locator quality on
# paginated sources depends on it.
for tool in pdftotext pdftoppm; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    printf 'Note: %s is not installed; page-preserving PDF extraction and page rendering are unavailable. Install poppler (brew install poppler / apt install poppler-utils) for stable page locators.\n' "$tool" >&2
  fi
done

printf 'Document extraction prerequisites are available: Node.js %s and npx %s.\n' "$(node --version)" "$(npx --version)"
