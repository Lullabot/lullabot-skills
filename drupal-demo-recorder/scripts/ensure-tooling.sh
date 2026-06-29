#!/usr/bin/env bash
# Ensure the demo-recording toolchain exists in THIS DDEV project. Idempotent:
# safe to run before every recording — it no-ops when everything is present, and
# otherwise installs what's missing and restarts DDEV once.
#
# Run from the DDEV project root:  bash <skill-dir>/scripts/ensure-tooling.sh
#
# It will, announcing each project-modifying step:
#   - install the e0ipso/ddev-playwright-cli add-on (the recorder CLI) if missing
#   - add ffmpeg/ffprobe to the web image via .ddev/web-build/Dockerfile.ffmpeg if missing
#   - create .playwright/cli.config.json (1080p) from the bundled example if absent
#   - ddev restart ONCE if the add-on or web image changed (brief container downtime)
set -euo pipefail

CONFIG_SRC="$(cd "$(dirname "$0")/.." && pwd)/assets/cli.config.example.json"
need_restart=0

if [ ! -d .ddev ]; then
  echo "ERROR: no .ddev/ here. Run this from a DDEV project root." >&2
  exit 1
fi

# Make sure the project is up so we can exec into the web container.
if ! ddev describe >/dev/null 2>&1; then
  echo "• DDEV not running — starting it…"
  ddev start
fi

# 1) playwright-cli (DDEV add-on; builds chromium into the web image on restart).
if ddev exec which playwright-cli >/dev/null 2>&1; then
  echo "✓ playwright-cli present"
else
  echo "• Installing the e0ipso/ddev-playwright-cli add-on…"
  ddev add-on get e0ipso/ddev-playwright-cli || ddev get e0ipso/ddev-playwright-cli
  need_restart=1
fi

# 2) ffmpeg + ffprobe (persistent, via a web-build Dockerfile so it survives rebuilds).
if ddev exec which ffmpeg >/dev/null 2>&1 && ddev exec which ffprobe >/dev/null 2>&1; then
  echo "✓ ffmpeg/ffprobe present"
else
  echo "• Adding ffmpeg to the web image (.ddev/web-build/Dockerfile.ffmpeg)…"
  mkdir -p .ddev/web-build
  cat > .ddev/web-build/Dockerfile.ffmpeg <<'EOF'
# Added by the drupal-demo-recorder skill — ffmpeg/ffprobe for slowing &
# transcoding demo recordings and extracting frames for validation.
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
EOF
  need_restart=1
fi

# 3) Apply image/add-on changes once.
if [ "$need_restart" = "1" ]; then
  echo "• Restarting DDEV to apply changes (containers briefly stop)…"
  ddev restart
fi

# 4) Viewport config at the project root.
if [ -f .playwright/cli.config.json ]; then
  echo "✓ .playwright/cli.config.json present"
else
  echo "• Creating .playwright/cli.config.json (1920×1080)…"
  mkdir -p .playwright
  cp "$CONFIG_SRC" .playwright/cli.config.json
fi

# 5) Verify everything is now in place (fails loudly if not).
echo "--- verification ---"
ddev exec which playwright-cli ffmpeg ffprobe
echo "✓ Tooling ready."
