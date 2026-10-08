#!/usr/bin/env bash
# Inspect the toolchain in THIS DDEV project; default mode never changes it.
# Run from the project root. --apply explicitly permits reviewed setup effects:
# starting/restarting DDEV, installing the add-on, adding ffmpeg, and config copy.
set -euo pipefail

apply=0
case "${1:-}" in
  --apply) apply=1 ;;
  --help|-h) echo "Usage: ensure-tooling.sh [--apply] (default: check only)"; exit 0 ;;
  "") ;;
  *) echo "Unknown option: $1" >&2; exit 2 ;;
esac

if ! command -v ddev >/dev/null 2>&1; then
  echo "ERROR: DDEV is required; no project changes made." >&2
  exit 127
fi

CONFIG_SRC="$(cd "$(dirname "$0")/.." && pwd)/assets/cli.config.example.json"
need_restart=0

if [ ! -d .ddev ]; then
  echo "ERROR: no .ddev/ here. Run this from a DDEV project root." >&2
  exit 1
fi

# Check mode reports availability and exits without starting/installing/writing.
if [ "$apply" != 1 ]; then
  if ! ddev describe >/dev/null 2>&1; then
    echo "DDEV unavailable or stopped. Review setup and start effects before --apply."
    exit 1
  fi
  missing=0
  for tool in playwright-cli ffmpeg ffprobe; do
    if ! ddev exec which "$tool" >/dev/null 2>&1; then
      echo "Missing container tool: $tool"
      missing=1
    fi
  done
  if [ ! -f .playwright/cli.config.json ]; then
    echo "Missing project config: .playwright/cli.config.json"
    missing=1
  fi
  if [ "$missing" = 1 ]; then
    echo "Review package identity, project changes, and restart downtime before --apply."
  else
    echo "Tooling present; no changes made."
  fi
  exit "$missing"
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
  ddev add-on get e0ipso/ddev-playwright-cli
  need_restart=1
fi

# 2) ffmpeg + ffprobe (persistent, via a web-build Dockerfile so it survives rebuilds).
if ddev exec which ffmpeg >/dev/null 2>&1 && ddev exec which ffprobe >/dev/null 2>&1; then
  echo "✓ ffmpeg/ffprobe present"
else
  echo "• Adding ffmpeg to the web image (.ddev/web-build/Dockerfile.ffmpeg)…"
  mkdir -p .ddev/web-build
  if [ -e .ddev/web-build/Dockerfile.ffmpeg ]; then
    echo "ERROR: existing Dockerfile.ffmpeg requires manual review; refusing overwrite." >&2
    exit 1
  fi
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
