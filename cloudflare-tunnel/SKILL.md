---
name: cloudflare-tunnel
description: "This skill should be used when users need to expose a local development web service to the internet via Cloudflare Tunnel. Use when users say 'expose my local server', 'share my dev server', 'create a tunnel', 'cloudflare tunnel', 'public URL for localhost', 'trycloudflare', or need to share a locally running service with others for testing or preview."
---

# Cloudflare Tunnel

Expose any local web service to the internet instantly using Cloudflare Tunnel (`cloudflared`). Supports two modes: **quick tunnels** (zero config, temporary URL) and **named tunnels** (persistent, reusable).

## Quick Start

For the fastest path to a public URL, run the helper script with the local port:

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh quick <port>
```

This creates a temporary `*.trycloudflare.com` URL with no authentication required.

## Workflow

### 1. Check Prerequisites

Before starting a tunnel, verify `cloudflared` is installed:

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh status
```

If not installed, install it:

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh install
```

On macOS this uses Homebrew. On Linux it detects apt/yum/pacman automatically.

### 2. Choose Tunnel Type

**Quick Tunnel** (recommended for most dev work):
- No Cloudflare account or authentication needed
- Generates a random `*.trycloudflare.com` subdomain
- URL changes each time the tunnel restarts
- Max 200 concurrent in-flight requests
- No Server-Sent Events (SSE) support
- Will not work if a `config.yaml` exists in `~/.cloudflared/`

**Named Tunnel** (for persistent access):
- Requires a Cloudflare account and authentication
- Stable tunnel identity (UUID-based)
- Can be mapped to custom DNS hostnames
- Supports all protocols

### 3. Start the Tunnel

#### Quick Tunnel

To expose a local HTTP service:

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh quick <port>
```

To expose an HTTPS local service:

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh quick <port> https
```

The script outputs a public URL like `https://random-words.trycloudflare.com`. Share this URL for remote access.

#### Named Tunnel

First authenticate (one-time):

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh login
```

Create the tunnel (one-time per project):

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh create my-project
```

Run the tunnel:

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh named my-project <port>
```

### 4. Stop the Tunnel

Press `Ctrl+C` in the terminal, or:

```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh stop
```

## Script Reference

The helper script at `scripts/tunnel.sh` supports these commands:

| Command | Description |
|---|---|
| `quick <port> [protocol]` | Start a quick tunnel (default protocol: http) |
| `named <name> <port>` | Run a named tunnel |
| `create <name>` | Create a new named tunnel |
| `list` | List existing named tunnels |
| `login` | Authenticate with Cloudflare |
| `stop` | Stop any running tunnel |
| `status` | Check installation and auth status |
| `install` | Install cloudflared |

## Common Patterns

**React dev server (port 3000):**
```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh quick 3000
```

**Vite dev server (port 5173):**
```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh quick 5173
```

**Django/Rails/Express (port 8000):**
```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh quick 8000
```

**PHP built-in server (port 8080):**
```bash
~/.claude/skills/cloudflare-tunnel/scripts/tunnel.sh quick 8080
```

## Troubleshooting

- **"config.yaml exists" error with quick tunnels:** Quick tunnels fail if `~/.cloudflared/config.yaml` exists. Temporarily rename or remove it.
- **HTTP 429 errors:** Quick tunnels cap at 200 concurrent in-flight requests. For higher traffic, use a named tunnel.
- **SSE not working:** Quick tunnels do not support Server-Sent Events. Use a named tunnel instead.
- **Tunnel stops when terminal closes:** Run with `nohup` or `screen`/`tmux` to persist across terminal sessions.
