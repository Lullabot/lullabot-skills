#!/usr/bin/env bash
# Extract evenly-spaced frames from a video for VISUAL validation.
# This script only PRODUCES the frames — you MUST then open/Read each PNG and
# check it against the validation checklist in SKILL.md. Do not trust a recording
# you have not looked at.
#
# Usage: extract-frames.sh <video.(mp4|webm)> <out-dir> [count]
#   <video>    path relative to the DDEV project root
#   <out-dir>  output dir, relative to the DDEV project root (created if missing)
#   [count]    number of evenly-spaced frames (default 8)
#
# Also grab specific moments by hand when needed, e.g. a drag mid-motion or a
# modal — the even spacing can miss the exact instant that matters:
#   ddev exec ffmpeg -y -ss <seconds> -i /var/www/html/<video> -frames:v 1 /var/www/html/<dir>/moment.png
set -euo pipefail
VID="${1:?usage: extract-frames.sh <video> <out-dir> [count]}"
DIR="${2:?missing out-dir}"
N="${3:-8}"

DUR=$(ddev exec ffprobe -v error -show_entries format=duration -of csv=p=0 "/var/www/html/${VID}" | cut -d. -f1)
mkdir -p "${DIR}"
for i in $(seq 1 "${N}"); do
  T=$(( DUR * i / (N + 1) ))
  ddev exec ffmpeg -y -ss "${T}" -i "/var/www/html/${VID}" -frames:v 1 "/var/www/html/${DIR}/frame-${T}s.png" >/dev/null 2>&1
done
echo "Extracted ${N} frames (of a ${DUR}s video) to ${DIR}/"
echo "NOW OPEN EACH FRAME and verify: single cursor, key badges while typing, real"
echo "content rendered, relevant element scrolled into view, no dead-air, clean layout."
