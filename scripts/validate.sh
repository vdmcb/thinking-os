#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$repo_root"

printf '%s\n' '== Shared core =='
./scripts/sync-core.sh --check

printf '\n%s\n' '== Agent Skills structure =='
npx -y skills-ref@0.1.5 validate skills/understand
npx -y skills-ref@0.1.5 validate skills/eli5

printf '\n%s\n' '== Skill discovery =='
npx -y skills@1.5.23 add "$repo_root" --list

printf '\n%s\n' '== Plugin marketplace =='
python3 scripts/check-plugin.py
python3 tests/test-check-plugin.py
if command -v claude >/dev/null 2>&1; then
  claude plugin validate . --strict
  # The repo root doubles as the plugin root, so the CLI warns that CLAUDE.md is
  # not shipped as plugin context. That is intended: CLAUDE.md governs repository
  # contributions, not plugin behavior. Accept exactly that warning; fail on any
  # other warning or on errors.
  if ! plugin_report="$(claude plugin validate .claude-plugin/plugin.json 2>&1)"; then
    printf '%s\n' "$plugin_report"
    exit 1
  fi
  printf '%s\n' "$plugin_report"
  warning_count="$(printf '%s\n' "$plugin_report" | sed -n 's/.*Found \([0-9][0-9]*\) warning.*/\1/p' | head -n 1)"
  warning_count="${warning_count:-0}"
  if [ "$warning_count" -ne 0 ] && \
     ! { [ "$warning_count" -eq 1 ] && printf '%s' "$plugin_report" | grep -q 'CLAUDE.md at the plugin root'; }; then
    printf '%s\n' 'Unexpected plugin validation warnings (only the CLAUDE.md-at-plugin-root warning is accepted)'
    exit 1
  fi
else
  printf '%s\n' 'SKIP: claude CLI is not installed locally (CI installs it)'
fi

printf '\n%s\n' '== Shell syntax =='
for script in core/scripts/*.sh skills/*/scripts/*.sh tests/*.sh scripts/*.sh; do
  bash -n "$script"
  printf 'OK: %s\n' "$script"
done
python3 -m py_compile scripts/check-evals.py scripts/check-eli5-evals.py scripts/check-activation.py scripts/check-plugin.py scripts/audit-run.py tests/generate-document-fixtures.py tests/test-check-plugin.py
printf 'OK: Python syntax\n'

if command -v shellcheck >/dev/null 2>&1; then
  printf '\n%s\n' '== ShellCheck =='
  shellcheck core/scripts/*.sh tests/*.sh scripts/*.sh
else
  printf '\n%s\n' 'SKIP: shellcheck is not installed locally'
fi

printf '\n%s\n' '== Deterministic eval checks =='
python3 scripts/check-evals.py
python3 scripts/check-eli5-evals.py
python3 scripts/check-activation.py

printf '\n%s\n' '== Extraction tests =='
tests/test-extract-document.sh


printf '\nAll validation checks passed.\n'
