#!/usr/bin/env bash
set -euo pipefail

BASE_REF="${BASE_REF:-feather-main}"
CURRENT_BRANCH="$(git branch --show-current || true)"

printf '== Feather Quantizer task verification ==\n'
printf 'branch: %s\n' "${CURRENT_BRANCH:-<detached>}"
printf 'base:   %s\n' "$BASE_REF"

printf '\n-- diff hygiene --\n'
git diff --check "$BASE_REF"...HEAD

git diff --stat "$BASE_REF"...HEAD
printf '\nChanged files:\n'
git diff --name-only "$BASE_REF"...HEAD

printf '\n-- protected path check --\n'
mapfile -t CHANGED < <(git diff --name-only "$BASE_REF"...HEAD)
VIOLATIONS=()
for path in "${CHANGED[@]}"; do
  case "$path" in
    keyboards/sekigon/*|lib/*|platforms/*|quantum/*|tmk_core/*|.gitmodules)
      VIOLATIONS+=("$path")
      ;;
  esac
done

if (( ${#VIOLATIONS[@]} > 0 )); then
  printf 'Protected paths changed:\n' >&2
  printf '  %s\n' "${VIOLATIONS[@]}" >&2
  exit 1
fi

printf 'protected shared paths: OK\n'

printf '\n-- non-documentation diff budget --\n'
NON_DOC_LINES=0
while IFS=$'\t' read -r added deleted path; do
  [[ -z "${path:-}" ]] && continue
  case "$path" in
    docs/*|prompts/*) continue ;;
  esac
  [[ "$added" == "-" ]] && added=0
  [[ "$deleted" == "-" ]] && deleted=0
  NON_DOC_LINES=$((NON_DOC_LINES + added + deleted))
done < <(git diff --numstat "$BASE_REF"...HEAD)

printf 'non-documentation changed lines: %d\n' "$NON_DOC_LINES"
if (( NON_DOC_LINES > 1500 )); then
  printf 'ERROR: hard diff threshold exceeded (1500)\n' >&2
  exit 1
fi

printf '\n-- loop state files --\n'
STATE_FILES=()
while IFS= read -r file; do
  [[ -n "$file" ]] && STATE_FILES+=("$file")
done < <(git diff --name-only "$BASE_REF"...HEAD -- 'docs/feather-quantizer/loop/runs/*/state.json')

if [[ "$CURRENT_BRANCH" == loop/* ]]; then
  if (( ${#STATE_FILES[@]} == 0 )); then
    printf 'ERROR: loop branch must change/add a run state.json\n' >&2
    exit 1
  fi
fi

for state in "${STATE_FILES[@]}"; do
  python3 scripts/feather-quantizer/verify-loop-state.py "$state"
  run_dir="$(dirname "$state")"
  if [[ ! -f "$run_dir/iterations.md" ]]; then
    printf 'ERROR: missing iterations.md next to %s\n' "$state" >&2
    exit 1
  fi
done

printf '\n-- working tree --\n'
git status --short

printf '\nverify-task: PASS\n'
