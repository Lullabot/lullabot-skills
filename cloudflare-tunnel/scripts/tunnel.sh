#!/usr/bin/env bash
# tunnel.sh — Helper script for managing Cloudflare Tunnels
# Part of the Cloudflare Tunnel skill for Claude Code
#
# Usage:
#   tunnel.sh <command> [args]
#
# Commands:
#   quick <port> [protocol]   Start a quick tunnel (default protocol: http)
#   named <name> <port>       Run a named tunnel
#   create <name>             Create a new named tunnel
#   list                      List existing named tunnels
#   login                     Authenticate with Cloudflare
#   stop                      Stop any running tunnel
#   status                    Check installation and auth status
#   install                   Install cloudflared

set -euo pipefail

CLOUDFLARED="cloudflared"
PID_FILE="/tmp/cloudflared-tunnel.pid"

command_exists() {
  command -v "$1" &>/dev/null
}

check_installed() {
  if ! command_exists "$CLOUDFLARED"; then
    echo "Error: cloudflared is not installed."
    echo "Run: $0 install"
    return 1
  fi
}

cmd_install() {
  if command_exists "$CLOUDFLARED"; then
    echo "cloudflared is already installed: $($CLOUDFLARED --version)"
    return 0
  fi

  if [[ "$OSTYPE" == darwin* ]]; then
    if command_exists brew; then
      brew install cloudflared
    else
      echo "Error: Homebrew is required on macOS. Install from https://brew.sh"
      return 1
    fi
  elif [[ "$OSTYPE" == linux* ]]; then
    if command_exists apt-get; then
      local codename=""
      if command_exists lsb_release; then
        codename="$(lsb_release -cs)"
      elif [[ -f /etc/os-release ]]; then
        # shellcheck disable=SC1091
        . /etc/os-release
        codename="${VERSION_CODENAME:-}"
      fi
      if [[ -z "$codename" ]]; then
        echo "Error: Could not determine Debian/Ubuntu codename. Install lsb-release or provide /etc/os-release with VERSION_CODENAME."
        return 1
      fi
      curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
      echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $codename main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
      sudo apt-get update && sudo apt-get install -y cloudflared
    elif command_exists yum; then
      sudo yum install -y cloudflared
    elif command_exists pacman; then
      sudo pacman -S --noconfirm cloudflared
    else
      echo "Error: No supported package manager found (apt, yum, pacman)."
      return 1
    fi
  else
    echo "Error: Unsupported OS: $OSTYPE"
    return 1
  fi

  echo "Installed: $($CLOUDFLARED --version)"
}

cmd_status() {
  echo "=== Cloudflare Tunnel Status ==="

  if command_exists "$CLOUDFLARED"; then
    echo "cloudflared: installed ($($CLOUDFLARED --version 2>&1 | head -1))"
  else
    echo "cloudflared: NOT installed"
    return 0
  fi

  if [[ -f "$HOME/.cloudflared/cert.pem" ]]; then
    echo "Authentication: configured"
  else
    echo "Authentication: not configured (run: $0 login)"
  fi

  if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Tunnel: running (PID $(cat "$PID_FILE"))"
  else
    echo "Tunnel: not running"
    rm -f "$PID_FILE"
  fi
}

cmd_login() {
  check_installed || return 1
  echo "Opening browser for Cloudflare authentication..."
  $CLOUDFLARED tunnel login
}

cmd_quick() {
  check_installed || return 1
  local port="${1:?Usage: $0 quick <port> [protocol]}"
  local protocol="${2:-http}"

  if [[ -f "$HOME/.cloudflared/config.yaml" ]] || [[ -f "$HOME/.cloudflared/config.yml" ]]; then
    echo "Warning: ~/.cloudflared/config.yaml exists. Quick tunnels may fail."
    echo "Rename or remove it, or use a named tunnel instead."
  fi

  echo "Starting quick tunnel to ${protocol}://localhost:${port}..."
  echo "Press Ctrl+C to stop."
  $CLOUDFLARED tunnel --url "${protocol}://localhost:${port}" &
  local pid=$!
  echo "$pid" > "$PID_FILE"
  wait "$pid"
  rm -f "$PID_FILE"
}

cmd_named() {
  check_installed || return 1
  local name="${1:?Usage: $0 named <name> <port>}"
  local port="${2:?Usage: $0 named <name> <port>}"

  if [[ ! -f "$HOME/.cloudflared/cert.pem" ]]; then
    echo "Error: Not authenticated. Run: $0 login"
    return 1
  fi

  echo "Starting named tunnel '${name}' to http://localhost:${port}..."
  echo "Press Ctrl+C to stop."
  $CLOUDFLARED tunnel run --url "http://localhost:${port}" "$name" &
  local pid=$!
  echo "$pid" > "$PID_FILE"
  wait "$pid"
  rm -f "$PID_FILE"
}

cmd_create() {
  check_installed || return 1
  local name="${1:?Usage: $0 create <name>}"

  if [[ ! -f "$HOME/.cloudflared/cert.pem" ]]; then
    echo "Error: Not authenticated. Run: $0 login"
    return 1
  fi

  $CLOUDFLARED tunnel create "$name"
  echo "Tunnel '${name}' created. Run it with: $0 named ${name} <port>"
}

cmd_list() {
  check_installed || return 1
  $CLOUDFLARED tunnel list
}

cmd_stop() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid"
      echo "Tunnel stopped (PID ${pid})."
    else
      echo "No running tunnel found (stale PID file)."
    fi
    rm -f "$PID_FILE"
  else
    echo "No running tunnel found."
  fi
}

# Main dispatcher
case "${1:-}" in
  install) cmd_install ;;
  status)  cmd_status ;;
  login)   cmd_login ;;
  quick)   shift; cmd_quick "$@" ;;
  named)   shift; cmd_named "$@" ;;
  create)  shift; cmd_create "$@" ;;
  list)    cmd_list ;;
  stop)    cmd_stop ;;
  *)
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  quick <port> [protocol]   Start a quick tunnel (default: http)"
    echo "  named <name> <port>       Run a named tunnel"
    echo "  create <name>             Create a new named tunnel"
    echo "  list                      List existing named tunnels"
    echo "  login                     Authenticate with Cloudflare"
    echo "  stop                      Stop any running tunnel"
    echo "  status                    Check installation and auth status"
    echo "  install                   Install cloudflared"
    exit 1
    ;;
esac
