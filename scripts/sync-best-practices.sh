#!/usr/bin/env bash
# sync-best-practices.sh
#
# Keep the vendored skill best-practices rubric current with the upstream doc.
#
# What it does:
#   1. Reports how long ago the rubric was last synced (the `last_synced:`
#      stamp in reviewing-skills/references/skill-best-practices.md).
#   2. Best-effort: checks that the upstream URL is still reachable, so a docs
#      restructure that 404s the page surfaces here rather than silently. (We
#      deliberately don't content-diff: the docs site is client-rendered and
#      serves rotating build hashes, so a text diff is all false positives.)
#      Degrades gracefully when offline or when curl isn't available.
#
# It never edits the rubric itself — the actual re-curation is a judgment step
# done in Claude via the `reviewing-skills` skill's refresh mode (it WebFetches
# the URL, proposes edits, and bumps `last_synced:`). This script is the nudge.
#
# Run it monthly (or whenever review-skill.js flags the rubric as stale).
#
# Usage:
#   scripts/sync-best-practices.sh
#
# Always exits 0 — this is advisory tooling, not a gate.

set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -z "$REPO_ROOT" ] && REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

RUBRIC="reviewing-skills/references/skill-best-practices.md"
STALE_DAYS=30

if [ ! -f "$RUBRIC" ]; then
  echo "Rubric not found at $RUBRIC — nothing to sync."
  exit 0
fi

URL="$(grep -oE 'https?://[^ ]*best-practices' "$RUBRIC" | head -1)"
LAST_SYNCED="$(grep -oE 'last_synced:[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}' "$RUBRIC" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)"

# --- Age report -------------------------------------------------------------
if [ -n "${LAST_SYNCED:-}" ]; then
  # Portable epoch conversion: GNU date (-d) or BSD/macOS date (-j -f).
  synced_epoch="$(date -d "$LAST_SYNCED" +%s 2>/dev/null \
    || date -j -f "%Y-%m-%d" "$LAST_SYNCED" +%s 2>/dev/null \
    || echo "")"
  if [ -n "$synced_epoch" ]; then
    now_epoch="$(date +%s)"
    age_days=$(( (now_epoch - synced_epoch) / 86400 ))
    echo "Rubric last synced: $LAST_SYNCED ($age_days days ago)."
    if [ "$age_days" -gt "$STALE_DAYS" ]; then
      echo "  → Stale (> ${STALE_DAYS} days). Time to refresh."
    fi
  else
    echo "Rubric last_synced: $LAST_SYNCED (could not compute age on this platform)."
  fi
else
  echo "Rubric has no last_synced stamp."
fi

echo "Upstream: ${URL:-<not recorded in rubric>}"
echo

# --- Best-effort reachability check ----------------------------------------
if [ -z "${URL:-}" ]; then
  echo "No upstream URL recorded — skipping reachability check."
elif ! command -v curl >/dev/null 2>&1; then
  echo "curl not available — skipping reachability check."
else
  code="$(curl -fsS -o /dev/null -w '%{http_code}' --max-time 20 "$URL" 2>/dev/null || true)"
  if [ -z "$code" ] || [ "$code" = "000" ]; then
    echo "Could not reach upstream (offline or blocked) — try again when online."
  elif [ "$code" = "200" ]; then
    echo "Upstream URL is reachable (HTTP 200)."
  else
    echo "Upstream URL returned HTTP $code — the docs page may have moved. Check the URL in $RUBRIC."
  fi
fi

echo
echo "----"
echo "To refresh: open Claude in this repo and ask the reviewing-skills skill to"
echo "run its refresh mode — it will WebFetch the doc, propose rubric edits, and"
echo "bump last_synced. This script does not edit the rubric itself."

exit 0
