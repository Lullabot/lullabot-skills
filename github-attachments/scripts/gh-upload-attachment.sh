#!/usr/bin/env bash
# Upload a file to GitHub's user-attachments store and print the asset URL.
#
# Usage: gh-upload-attachment.sh <file> [owner/repo] [--alt="text"] [--markdown|--html]
#
# The repo defaults to the current directory's GitHub remote. The repo only
# scopes the upload; it does not attach the file to anything. Paste the printed
# URL into an issue, PR, or comment body to render it.
set -euo pipefail

for dep in gh jq curl file; do
  command -v "$dep" >/dev/null 2>&1 || {
    echo "missing required command: $dep" >&2
    exit 127
  }
done

file="${1:-}"
[ -n "$file" ] || { echo "usage: $0 <file> [owner/repo] [--alt=\"text\"] [--markdown|--html]" >&2; exit 2; }
[ -f "$file" ] || { echo "no such file: $file" >&2; exit 2; }

repo=""
format="url"
alt=""
shift
for arg in "$@"; do
  case "$arg" in
    --markdown) format="markdown" ;;
    --html) format="html" ;;
    --alt=*) alt="${arg#--alt=}" ;;
    *) repo="$arg" ;;
  esac
done

if [ -z "$repo" ]; then
  repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
fi

urlencode() { jq -rn --arg v "$1" '$v|@uri'; }
htmlescape() { jq -rn --arg v "$1" '$v|@html'; }

name=$(basename "$file")
mime=$(file --brief --mime-type "$file")
repo_id=$(gh api "repos/$repo" --jq .id)
[ -n "$alt" ] || alt="$name"

resp=$(curl -sS --fail-with-body \
  "https://uploads.github.com/user-attachments/assets?name=$(urlencode "$name")&content_type=$(urlencode "$mime")&repository_id=$repo_id" \
  -X POST \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/json" \
  --data-binary "@$file")

url=$(printf %s "$resp" | jq -r .url)
[ "$url" != "null" ] && [ -n "$url" ] || { echo "upload failed: $resp" >&2; exit 1; }

case "$format" in
  markdown) printf '![%s](%s)\n' "$alt" "$url" ;;
  html)     printf '<img src="%s" alt="%s" width="600">\n' "$url" "$(htmlescape "$alt")" ;;
  *)        printf '%s\n' "$url" ;;
esac
