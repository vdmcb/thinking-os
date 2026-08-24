#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
extractor="$repo_root/core/scripts/extract-document.sh"
prereqs="$repo_root/core/scripts/check-prerequisites.sh"
temporary="$(mktemp -d "${TMPDIR:-/tmp}/thinking-os-test.XXXXXX")"
cleanup() { rm -rf -- "$temporary"; }
trap cleanup EXIT HUP INT TERM

pass=0
fail=0

expect_success() {
  local name="$1"
  shift
  if "$@" >/dev/null 2>"$temporary/stderr"; then
    printf 'PASS: %s\n' "$name"
    pass=$((pass + 1))
  else
    printf 'FAIL: %s\n' "$name" >&2
    sed 's/^/  /' "$temporary/stderr" >&2
    fail=$((fail + 1))
  fi
}

expect_failure() {
  local name="$1"
  shift
  if "$@" >/dev/null 2>"$temporary/stderr"; then
    printf 'FAIL: %s unexpectedly succeeded\n' "$name" >&2
    fail=$((fail + 1))
  else
    printf 'PASS: %s\n' "$name"
    pass=$((pass + 1))
  fi
}

expect_failure "missing arguments" "$extractor"
expect_failure "missing input" "$extractor" "$temporary/missing.pdf" "$temporary/out.md"
expect_failure "directory input" "$extractor" "$temporary" "$temporary/out.md"
printf 'not a document\n' > "$temporary/input.exe"
expect_failure "unsupported extension" "$extractor" "$temporary/input.exe" "$temporary/out.md"
printf 'existing\n' > "$temporary/existing.md"
printf 'name,value\nalpha,42\n' > "$temporary/input.csv"
expect_failure "existing output protection" "$extractor" "$temporary/input.csv" "$temporary/existing.md"
expect_failure "source and output path collision" "$extractor" "$temporary/input.csv" "$temporary/input.csv"

mkdir -p "$temporary/path with spaces"
printf 'name,value\nalpha,42\n' > "$temporary/path with spaces/ünicode source.csv"
expect_success "spaces and Unicode paths" "$extractor" "$temporary/path with spaces/ünicode source.csv" "$temporary/path with spaces/result.md"
if grep -q '42' "$temporary/path with spaces/result.md"; then
  printf 'PASS: converted content preserved\n'
  pass=$((pass + 1))
else
  printf 'FAIL: converted content missing expected value\n' >&2
  fail=$((fail + 1))
fi

printf 'name,value\nbeta,73\n' > "$temporary/-leading.csv"
expect_success "leading-hyphen filename" "$extractor" "$temporary/-leading.csv" "$temporary/leading.md"

python3 "$repo_root/tests/generate-document-fixtures.py" "$temporary/formats"
for specification in \
  'docx:sample.docx:DOCX_MARKER_41' \
  'pptx:sample.pptx:PPTX_MARKER_42' \
  'xlsx:sample.xlsx:XLSX_MARKER_43' \
  'pdf:sample.pdf:PDF_MARKER_44'; do
  IFS=: read -r label filename marker <<< "$specification"
  output="$temporary/formats/$label.md"
  expect_success "$label conversion" "$extractor" "$temporary/formats/$filename" "$output"
  if grep -q "$marker" "$output"; then
    printf 'PASS: %s content preserved\n' "$label"
    pass=$((pass + 1))
  else
    printf 'FAIL: %s output missing %s\n' "$label" "$marker" >&2
    fail=$((fail + 1))
  fi
done

printf 'not really a PDF\n' > "$temporary/malformed.pdf"
expect_failure "malformed PDF" "$extractor" "$temporary/malformed.pdf" "$temporary/malformed.md"
printf 'name,value\ngamma,99\n' > "$temporary/misleading.docx"
expect_failure "misleading DOCX extension" "$extractor" "$temporary/misleading.docx" "$temporary/misleading.md"

printf 'secret\n' > "$temporary/unreadable.csv"
chmod 000 "$temporary/unreadable.csv"
if [[ -r "$temporary/unreadable.csv" ]]; then
  printf 'SKIP: permission-denied input check (current user can still read mode 000)\n'
else
  expect_failure "permission-denied input" "$extractor" "$temporary/unreadable.csv" "$temporary/unreadable.md"
fi
chmod 600 "$temporary/unreadable.csv"

if PATH="/usr/bin:/bin" "$prereqs" >/dev/null 2>"$temporary/missing-prereq"; then
  printf 'SKIP: missing-prerequisite diagnostic (Node.js is in the base PATH)\n'
elif grep -Eq 'Node.js|npx' "$temporary/missing-prereq"; then
  printf 'PASS: missing-prerequisite diagnostic\n'
  pass=$((pass + 1))
else
  printf 'FAIL: missing-prerequisite diagnostic was not readable\n' >&2
  fail=$((fail + 1))
fi

printf '\n%d passed, %d failed\n' "$pass" "$fail"
(( fail == 0 ))
