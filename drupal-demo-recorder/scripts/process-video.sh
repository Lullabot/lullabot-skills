#!/usr/bin/env bash
# Slow a raw screen recording for natural pacing and transcode to a shareable mp4.
#
# Usage: process-video.sh <input.webm> <output-basename> [speed-factor]
#   <input.webm>       raw recording, path relative to the DDEV project root
#   <output-basename>  output path (no extension), relative to the DDEV project root
#   [speed-factor]     PTS multiplier; 1.5 = 1.5x slower (default). Higher = slower.
#                      Pass 1.0 for transcode-only (no slowdown) when you already
#                      paced the run at record time (the preferred approach).
#
# Produces <output-basename>.webm (slowed, silent) and <output-basename>.mp4 (H.264).
# ffmpeg runs inside the DDEV web container; the repo is mounted at /var/www/html.
# Do NOT add a scale filter — record at the final resolution (see cli.config.example.json).
set -euo pipefail
IN="${1:?usage: process-video.sh <input.webm> <output-basename> [speed-factor]}"
OUT="${2:?missing output basename}"
SPEED="${3:-1.5}"

ddev exec ffmpeg -y -i "/var/www/html/${IN}" -filter:v "setpts=${SPEED}*PTS" -an "/var/www/html/${OUT}.webm"
ddev exec ffmpeg -y -i "/var/www/html/${OUT}.webm" -c:v libx264 -pix_fmt yuv420p -movflags +faststart "/var/www/html/${OUT}.mp4"

DUR=$(ddev exec ffprobe -v error -show_entries format=duration -of csv=p=0 "/var/www/html/${OUT}.mp4" 2>/dev/null || echo '?')
RES=$(ddev exec ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "/var/www/html/${OUT}.mp4" 2>/dev/null || echo '?')
echo "Wrote ${OUT}.webm and ${OUT}.mp4  (duration=${DUR}s, ${RES})"
echo "NEXT: validate with extract-frames.sh and OPEN the frames."
