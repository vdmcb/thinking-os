#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$repo_root"

skills_root="plugins/thinking-os/skills"

printf '%s\n' '== Shared core =='
./scripts/sync-core.sh --check

printf '\n%s\n' '== Agent Skills structure =='
npx -y skills-ref@0.1.5 validate "$skills_root/understand"
npx -y skills-ref@0.1.5 validate "$skills_root/eli5"

printf '\n%s\n' '== Skill discovery =='
npx -y skills@1.5.23 add "$repo_root" --list

printf '\n%s\n' '== Plugin marketplace =='
python3 scripts/check-plugin.py
python3 tests/test-check-plugin.py
if command -v claude >/dev/null 2>&1; then
  claude plugin validate . --strict
  claude plugin validate plugins/thinking-os --strict
else
  printf '%s\n' 'SKIP: claude CLI is not installed locally (CI installs it)'
fi

printf '\n%s\n' '== Shell syntax =='
for script in core/scripts/*.sh "$skills_root"/*/scripts/*.sh tests/*.sh scripts/*.sh; do
  bash -n "$script"
  printf 'OK: %s\n' "$script"
done
python3 -m py_compile scripts/check-evals.py scripts/check-eli5-evals.py scripts/check-activation.py scripts/check-plugin.py scripts/audit-run.py tests/generate-document-fixtures.py tests/test-audit-run.py tests/test-check-plugin.py
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
python3 tests/test-audit-run.py

printf '\n%s\n' '== Extraction tests =='
tests/test-extract-document.sh


printf '\nAll validation checks passed.\n'
