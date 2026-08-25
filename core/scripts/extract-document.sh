#!/usr/bin/env bash
set -euo pipefail

readonly ANYDOC_VERSION="0.2.3"

usage() {
  printf 'Usage: %s INPUT_FILE OUTPUT_MD\n' "$(basename "$0")" >&2
}

if (( $# != 2 )); then
  usage
  exit 64
fi

input="$1"
output="$2"

if [[ ! -e "$input" ]]; then
  printf 'Input does not exist: %s\n' "$input" >&2
  exit 66
fi

if [[ ! -f "$input" ]]; then
  printf 'Input must be a regular file: %s\n' "$input" >&2
  exit 66
fi

if [[ ! -r "$input" ]]; then
  printf 'Input is not readable with the current permissions: %s\n' "$input" >&2
  exit 66
fi

extension="${input##*.}"
extension="$(printf '%s' "$extension" | tr '[:upper:]' '[:lower:]')"
case "$extension" in
  doc|docx|odt|pdf|ppt|pptx|rtf|epub|xls|xlsx|ods|odp|csv) ;;
  *)
    printf 'Unsupported document extension: .%s\n' "$extension" >&2
    exit 65
    ;;
esac

if [[ -e "$output" ]]; then
  printf 'Refusing to overwrite existing output: %s\n' "$output" >&2
  exit 73
fi

output_dir="$(dirname "$output")"
if [[ ! -d "$output_dir" ]]; then
  printf 'Output directory does not exist: %s\n' "$output_dir" >&2
  exit 73
fi

input_abs="$(cd "$(dirname "$input")" && pwd -P)/$(basename "$input")"
output_abs="$(cd "$output_dir" && pwd -P)/$(basename "$output")"

if [[ "$input_abs" == "$output_abs" ]]; then
  printf 'Output path must differ from the source path.\n' >&2
  exit 73
fi

"$(dirname "$0")/check-prerequisites.sh" >/dev/null

umask 077
temporary="$(mktemp "${output_abs}.tmp.XXXXXX")"
cleanup() {
  rm -f -- "$temporary"
}
trap cleanup EXIT HUP INT TERM

if ! npx -y "@firecrawl/anydoc@${ANYDOC_VERSION}" "$input_abs" -o "$temporary"; then
  printf 'AnyDoc could not convert the source. The file may be corrupt, encrypted, or image-only.\n' >&2
  exit 1
fi

if [[ ! -s "$temporary" ]]; then
  printf 'AnyDoc produced no readable content. The source may require OCR or host-native vision.\n' >&2
  exit 1
fi

if ! ln "$temporary" "$output_abs"; then
  printf 'Refusing to overwrite output created during conversion: %s\n' "$output_abs" >&2
  exit 73
fi
rm -f -- "$temporary"
trap - EXIT HUP INT TERM
printf 'Extracted Markdown: %s\n' "$output_abs" >&2
