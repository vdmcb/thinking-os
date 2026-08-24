#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$repo_root"

printf '%s\n' '== Agent Skills structure =='
npx -y skills-ref@0.1.5 validate skills/understand

printf '\n%s\n' '== Skill discovery =='
npx -y skills@1.5.23 add "$repo_root" --list

printf '\n%s\n' '== Shell syntax =='
for script in skills/understand/scripts/*.sh tests/*.sh scripts/*.sh; do
  bash -n "$script"
  printf 'OK: %s\n' "$script"
done
python3 -m py_compile scripts/check-evals.py tests/generate-document-fixtures.py
printf 'OK: Python syntax\n'

if command -v shellcheck >/dev/null 2>&1; then
  printf '\n%s\n' '== ShellCheck =='
  shellcheck skills/understand/scripts/*.sh tests/*.sh scripts/*.sh
else
  printf '\n%s\n' 'SKIP: shellcheck is not installed locally'
fi

printf '\n%s\n' '== Deterministic eval checks =='
python3 scripts/check-evals.py

printf '\n%s\n' '== Extraction tests =='
tests/test-extract-document.sh


printf '\nAll validation checks passed.\n'
