#!/bin/sh
# Downloads Lullabot's published ADRs and prints the directory holding them.
#
# Usage: fetch-lullabot-adrs.sh [cache-dir]
#
# The cache directory defaults to ${XDG_CACHE_HOME:-$HOME/.cache}/adr-review.
# The archive is downloaded again only when its ETag changes. On success, the
# path of the extracted ADRs (<cache-dir>/adrs) is the only line on stdout. If
# the download fails but an earlier copy is cached, that copy is used, with a
# warning on stderr. Otherwise the script exits non-zero with a message.

set -eu

# Tests point ADR_REVIEW_ARCHIVE_URL at a local file:// archive.
url="${ADR_REVIEW_ARCHIVE_URL:-https://architecture.lullabot.com/files/all-md.zip}"
cache="${1:-${XDG_CACHE_HOME:-$HOME/.cache}/adr-review}"

fail() {
  echo "fetch-lullabot-adrs: $*" >&2
  exit 1
}

command -v curl >/dev/null 2>&1 || fail "curl is required"

mkdir -p "$cache" || fail "can't create $cache"

# Without the archive, a saved ETag would make curl skip the download.
[ -f "$cache/all-md.zip" ] || rm -f "$cache/etag"

if ! code=$(curl -sSfL --etag-compare "$cache/etag" --etag-save "$cache/etag" \
  -o "$cache/all-md.zip" -w '%{http_code}' "$url"); then
  if [ -d "$cache/adrs" ]; then
    echo "fetch-lullabot-adrs: download failed, using the cached copy" >&2
    echo "$cache/adrs"
    exit 0
  fi
  rm -f "$cache/all-md.zip" "$cache/etag"
  fail "can't download $url"
fi

if [ "$code" = 304 ] && [ -d "$cache/adrs" ]; then
  echo "$cache/adrs"
  exit 0
fi

# Extract into a new directory first, so a failure leaves no partial copy.
# unzip and Python's zipfile both keep absolute and ".." entry paths inside
# the target directory; don't add options that change that (e.g. unzip -:).
tmp=$(mktemp -d "$cache/extract.XXXXXX") || fail "can't create a temporary directory in $cache"
if command -v unzip >/dev/null 2>&1; then
  unzip -q "$cache/all-md.zip" -d "$tmp" >&2 || extracted=no
elif command -v python3 >/dev/null 2>&1; then
  python3 -I -m zipfile -e "$cache/all-md.zip" "$tmp" >&2 || extracted=no
else
  rm -rf "$tmp"
  fail "unzip or python3 is required"
fi

if [ "${extracted:-yes}" = no ] || [ ! -d "$tmp/adrs" ]; then
  rm -rf "$tmp"
  rm -f "$cache/all-md.zip" "$cache/etag"
  fail "can't extract the archive; it will be downloaded again next time"
fi

rm -rf "$cache/adrs"
mv "$tmp/adrs" "$cache/adrs"
rm -rf "$tmp"
echo "$cache/adrs"
