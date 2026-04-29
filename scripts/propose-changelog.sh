#!/usr/bin/env bash
# propose-changelog.sh
#
# Suggest one or more `User-Facing-Change:` commit trailer lines for
# the changes you're about to commit (or the most recent commit).
#
# How it works:
#   1. Detect which skill folders have changes (including deletes/renames).
#   2. For each, ask GitHub Models (via `gh models`) for a one-line
#      user-facing summary — or "SKIP" for cosmetic-only changes.
#   3. Print the trailer line(s). Paste into your commit message.
#
# Usage:
#   scripts/propose-changelog.sh              # analyze staged changes
#   scripts/propose-changelog.sh --last       # analyze HEAD's changes
#   scripts/propose-changelog.sh --range R    # analyze a custom range (e.g. main..HEAD)
#
# Requirements:
#   - Bash 4+ (macOS ships 3.2 by default — `brew install bash`)
#   - `gh` CLI authenticated (gh auth login)
#   - `gh models` extension (gh extension install github/gh-models)
#
# Falls back gracefully:
#   - No changes detected? Prints a no-op note and exits 0.
#   - `gh models` unavailable? Prints a stub trailer line for the
#     author to fill in manually. Exits 0.

set -euo pipefail

# Bash 4+ required (mapfile, declare -A). macOS ships 3.2 — bail early.
if [ "${BASH_VERSINFO[0]:-0}" -lt 4 ]; then
  echo "propose-changelog.sh requires Bash 4+ (you have ${BASH_VERSION})." >&2
  echo "On macOS:  brew install bash  &&  /opt/homebrew/bin/bash $0 \"\$@\"" >&2
  exit 1
fi

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

# Diff-derived path lists. --name-status carries a status code so we can
# pick up deletes (D) and renames (R) — important so a commit that
# removes a skill still triggers a trailer-prompt.
case "$MODE" in
  staged)
    STATUS_CMD=(git diff --cached --name-status --find-renames)
    DIFF_BASE=(git diff --cached)
    LABEL="staged changes"
    ;;
  last)
    STATUS_CMD=(git show HEAD --name-status --format= --find-renames)
    DIFF_BASE=(git diff HEAD~1 HEAD)
    LABEL="HEAD ($(git log -1 --pretty=format:%h))"
    ;;
  range)
    if [ -z "$RANGE" ]; then echo "--range requires an argument" >&2; exit 2; fi
    STATUS_CMD=(git diff "$RANGE" --name-status --find-renames)
    DIFF_BASE=(git diff "$RANGE")
    LABEL="range $RANGE"
    ;;
esac

# Detect skill folders that changed.
# A folder counts as a skill if either:
#   (a) it currently contains a SKILL.md, OR
#   (b) the change deletes/renames it (so SKILL.md is gone in the working tree)
mapfile -t CHANGED_ENTRIES < <("${STATUS_CMD[@]}")
declare -A SKILLS_TOUCHED=()
for entry in "${CHANGED_ENTRIES[@]}"; do
  [ -z "$entry" ] && continue
  IFS=$'\t' read -r status path1 path2 <<< "$entry"
  [ -z "${status:-}" ] && continue

  paths=()
  [ -n "${path1:-}" ] && paths+=("$path1")
  case "$status" in
    R*|C*) [ -n "${path2:-}" ] && paths+=("$path2") ;;
  esac

  for f in "${paths[@]}"; do
    [ -z "$f" ] && continue
    top="${f%%/*}"
    case "$top" in
      .|..|"") continue ;;
      .github|scripts|node_modules|_*) continue ;;
    esac
    # Either the skill is on disk now, OR this change removed/renamed it.
    if [ -f "$top/SKILL.md" ]; then
      SKILLS_TOUCHED["$top"]=1
    else
      case "$status" in
        D|R*) SKILLS_TOUCHED["$top"]=1 ;;
      esac
    fi
  done
done

if [ "${#SKILLS_TOUCHED[@]}" -eq 0 ]; then
  echo "No skill folders changed in $LABEL — no trailer needed."
  exit 0
fi

# Sorted, stable iteration order so output is reproducible across shells.
mapfile -t SORTED_SKILLS < <(printf '%s\n' "${!SKILLS_TOUCHED[@]}" | sort)

echo "Skill folders changed in $LABEL:"
for s in "${SORTED_SKILLS[@]}"; do echo "  - $s"; done
echo

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
[ "${#SORTED_SKILLS[@]}" -gt 1 ] && multi_skill="true"

for skill in "${SORTED_SKILLS[@]}"; do
  echo "—— $skill ——"
  diff_body="$("${DIFF_BASE[@]}" -- "$skill/" 2>/dev/null || true)"

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

  if [ "$summary" = "SKIP" ]; then
    echo "  Model says: no user-facing change worth listing. (No trailer.)"
    continue
  fi
  if [ -z "$summary" ]; then
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
