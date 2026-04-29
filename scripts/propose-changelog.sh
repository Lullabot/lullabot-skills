#!/usr/bin/env bash
# propose-changelog.sh
#
# Suggest one or more `User-Facing-Change:` commit trailer lines for
# the changes you're about to commit (or the most recent commit).
#
# How it works:
#   1. Detect which skill folders have changes.
#   2. For each, show a diff summary and ask GitHub Models (via `gh models`)
#      for a one-line user-facing summary — or "SKIP" for cosmetic-only changes.
#   3. Print the trailer line(s). Paste into your commit message.
#
# Usage:
#   scripts/propose-changelog.sh              # analyze staged changes
#   scripts/propose-changelog.sh --last       # analyze HEAD's changes
#   scripts/propose-changelog.sh --range R    # analyze a custom range (e.g. main..HEAD)
#
# Requirements:
#   - `gh` CLI authenticated (gh auth login)
#   - `gh models` extension (gh extension install github/gh-models)
#
# Falls back gracefully:
#   - No changes detected? Prints a no-op note and exits 0.
#   - `gh models` unavailable? Prints the diff summary and a stub trailer
#     for the author to fill in manually. Exits 0.

set -euo pipefail

MODEL="${PROPOSE_CHANGELOG_MODEL:-gpt-4o-mini}"
MODE="staged"
RANGE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --staged) MODE="staged"; shift ;;
    --last)   MODE="last"; shift ;;
    --range)  MODE="range"; RANGE="${2:-}"; shift 2 ;;
    -h|--help)
      sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

case "$MODE" in
  staged)
    DIFF_CMD=(git diff --cached)
    NAME_CMD=(git diff --cached --name-only)
    LABEL="staged changes"
    ;;
  last)
    DIFF_CMD=(git show HEAD)
    NAME_CMD=(git show HEAD --name-only --format=)
    LABEL="HEAD ($(git log -1 --pretty=format:%h))"
    ;;
  range)
    if [ -z "$RANGE" ]; then echo "--range requires an argument" >&2; exit 2; fi
    DIFF_CMD=(git diff "$RANGE")
    NAME_CMD=(git diff "$RANGE" --name-only)
    LABEL="range $RANGE"
    ;;
esac

# Detect skill folders that changed (top-level dir of changed paths,
# filtered to those that actually look like skills).
mapfile -t CHANGED_FILES < <("${NAME_CMD[@]}")
declare -A SKILLS_TOUCHED=()
for f in "${CHANGED_FILES[@]}"; do
  [ -z "$f" ] && continue
  top="${f%%/*}"
  case "$top" in
    .|..|"") continue ;;
    .github|scripts|node_modules|_*) continue ;;
  esac
  if [ -f "$top/SKILL.md" ]; then
    SKILLS_TOUCHED["$top"]=1
  fi
done

if [ "${#SKILLS_TOUCHED[@]}" -eq 0 ]; then
  echo "No skill folders changed in $LABEL — no trailer needed."
  exit 0
fi

echo "Skill folders changed in $LABEL:"
for s in "${!SKILLS_TOUCHED[@]}"; do echo "  - $s"; done
echo

# Detect whether `gh models` is available
HAS_GH_MODELS=0
if command -v gh >/dev/null 2>&1 && gh models --help >/dev/null 2>&1; then
  HAS_GH_MODELS=1
fi

PROMPT_TEMPLATE='You are summarizing a change to a Claude Code skill bundle for end users browsing a public prompt library.

A "user-facing change" is anything visible to people who install or read the skill: new sections, behavior changes, new helper scripts, new dependencies, fixed bugs that affect output.

NOT user-facing: typo fixes, formatting tweaks, dependency bumps with no behavior change, internal refactors, doc improvements that do not add information.

Skill folder: SKILL_NAME

Diff:
DIFF_BODY

Respond in EXACTLY ONE LINE. Either:
- A single sentence summary, around 10-15 words, in past tense ("Added X", "Renamed Y").
- The literal word SKIP if there is no user-facing change worth listing.

Examples:
- Added gollum link syntax reference for handling broken wiki links
- Added analyze-eeat.py helper for E-E-A-T signal scoring
- Renamed install command to setup for consistency with other skills
- SKIP

Respond with only the line, no quotes, no markdown.'

multi_skill="false"
[ "${#SKILLS_TOUCHED[@]}" -gt 1 ] && multi_skill="true"

for skill in "${!SKILLS_TOUCHED[@]}"; do
  echo "—— $skill ——"
  diff_body="$(git diff $([ "$MODE" = "staged" ] && echo --cached || true) \
                $([ "$MODE" = "last" ]   && echo HEAD~1 HEAD       || true) \
                $([ "$MODE" = "range" ]  && echo "$RANGE"          || true) \
                -- "$skill/" 2>/dev/null || true)"

  if [ -z "$diff_body" ]; then
    echo "  (no diff for $skill — skipping)"
    continue
  fi

  if [ "$HAS_GH_MODELS" -eq 1 ]; then
    prompt="${PROMPT_TEMPLATE//SKILL_NAME/$skill}"
    prompt="${prompt//DIFF_BODY/$diff_body}"
    summary="$(printf '%s' "$prompt" | gh models run "$MODEL" 2>/dev/null | head -1 | tr -d '\r')"
    summary="${summary#"${summary%%[![:space:]]*}"}"
    summary="${summary%"${summary##*[![:space:]]}"}"
  else
    summary=""
  fi

  if [ -z "$summary" ] || [ "$summary" = "SKIP" ]; then
    if [ "$summary" = "SKIP" ]; then
      echo "  Model says: no user-facing change worth listing. (No trailer.)"
      continue
    fi
    summary="<your one-line user-facing summary here>"
  fi

  if [ "$multi_skill" = "true" ]; then
    echo "User-Facing-Change[$skill]: $summary"
  else
    echo "User-Facing-Change: $summary"
  fi
done

cat <<'EOF'

----
Paste the lines above into your commit message body, edit as needed,
or remove them entirely if the change is purely cosmetic / internal.

If `gh models` is not installed, the script falls back to a stub
("<your one-line user-facing summary here>") that you fill in by hand.
Install with: gh extension install github/gh-models
EOF
