#!/bin/sh
# Tests fetch-lullabot-adrs.sh against local archives, without the network.
# Usage: sh adr-review/scripts/tests/test-fetch-lullabot-adrs.sh

set -eu

script="$(cd "$(dirname "$0")/.." && pwd)/fetch-lullabot-adrs.sh"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

failures=0
check() {
  if [ "$2" = "$3" ]; then
    echo "ok - $1"
  else
    echo "not ok - $1: expected '$3', got '$2'"
    failures=$((failures + 1))
  fi
}

mkdir -p "$work/src/adrs"
printf -- '---\nstatus: accepted\n---\n' > "$work/src/adrs/20260101-example.md"
python3 -I -m zipfile -c "$work/good.zip" "$work/src/adrs" >/dev/null
echo junk > "$work/bad.zip"

# A valid archive is extracted, and the ADR directory is printed.
out=$(ADR_REVIEW_ARCHIVE_URL="file://$work/good.zip" sh "$script" "$work/cache")
check "prints the ADR directory" "$out" "$work/cache/adrs"
check "extracts the ADRs" "$(ls "$work/cache/adrs")" "20260101-example.md"

# A corrupt archive fails and is removed, so the next run downloads it again.
status=0
ADR_REVIEW_ARCHIVE_URL="file://$work/bad.zip" sh "$script" "$work/bad-cache" >/dev/null 2>&1 || status=$?
check "fails on a corrupt archive" "$status" 1
check "removes the corrupt archive" "$(ls -A "$work/bad-cache")" ""

# A failed download falls back to the cached copy.
out=$(ADR_REVIEW_ARCHIVE_URL="file://$work/missing.zip" sh "$script" "$work/cache" 2>/dev/null)
check "uses the cache when the download fails" "$out" "$work/cache/adrs"

# A failed download with nothing cached fails.
status=0
ADR_REVIEW_ARCHIVE_URL="file://$work/missing.zip" sh "$script" "$work/empty" >/dev/null 2>&1 || status=$?
check "fails with nothing cached" "$status" 1

exit "$failures"
