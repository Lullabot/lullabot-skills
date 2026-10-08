---
name: cloudflare-tunnel
description: "This skill should be used when users need to expose a local development web service to the internet via Cloudflare Tunnel. Use when users say 'expose my local server', 'share my dev server', 'create a tunnel', 'cloudflare tunnel', 'public URL for localhost', 'trycloudflare', or need to share a locally running service with others for testing or preview."
---

# Cloudflare Tunnel

## Requirements

Bash and `cloudflared`; the helper also uses standard Unix commands (`head`, `cat`, `kill`, `rm`). Quick tunnels need network access but no account; named tunnels need a Cloudflare account and tunnel credentials in `~/.cloudflared/`. Optional installation uses Homebrew, apt with `curl`/`sudo`, yum, or pacman; installation is a separate reviewed setup action.

Resolve `SKILL_DIR` to the absolute directory containing the loaded `SKILL.md`, using the skill location supplied by the agent or locating this file. Set it explicitly (for example, `SKILL_DIR="/path/to/installed/cloudflare-tunnel"`); do not derive it from the project working directory. Run project-relative commands from the working project and use `"$SKILL_DIR/..."` for companions.

## Safety and review

Starting either tunnel exposes the selected local service to the internet. Before starting, a human reviews the port, rendered pages, endpoints, authentication, and whether the data is eligible for public exposure; a random URL is not access control. Prefer a disposable service containing public or synthetic data. Login, tunnel creation, DNS/access changes, and installing packages need review of the exact target and effects. Stop the foreground tunnel with Ctrl+C; use the helper stop command only for a tunnel started by that helper and verify the PID. Review the URL and audience before sharing it. Do not remove existing Cloudflare configuration merely to bypass a quick-tunnel error.

Outside a verified secure sandbox, a human must read and understand unreviewed shell commands and generated code before execution. Always review MCP data-changing operations if an MCP alternative is used. Use least privilege; tool installation requires Security Team review and verification of upstream identity. Personal information requires approved tooling integrated with its source system; confidential information requires specifically approved tools; non-public information requires tools that neither train on nor retain it. Never send sensitive non-public data to public AI models. Stop when eligibility is unknown. An AI check does not replace human self-review before sharing, publishing, or handing work to another reviewer.


Expose any local web service to the internet instantly using Cloudflare Tunnel (`cloudflared`). Supports two modes: **quick tunnels** (zero config, temporary URL) and **named tunnels** (persistent, reusable).

## Quick Start

After the human exposure review in Safety and review, run the helper with the selected local port:

```bash
bash "$SKILL_DIR/scripts/tunnel.sh" quick <port>
```

This creates a temporary `*.trycloudflare.com` URL with no authentication required.

## Workflow

### 1. Check Prerequisites

Before starting a tunnel, verify `cloudflared` is installed:

```bash
bash "$SKILL_DIR/scripts/tunnel.sh" status
```

If missing, review the upstream package and installation effects first. Linux installation modifies host package sources with sudo; perform privileged host setup manually, rather than running it unattended. After authorized setup, the helper supports:

```bash
bash "$SKILL_DIR/scripts/tunnel.sh" install
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
bash "$SKILL_DIR/scripts/tunnel.sh" quick <port>
```

To expose an HTTPS local service:

```bash
bash "$SKILL_DIR/scripts/tunnel.sh" quick <port> https
```

The script outputs a public URL like `https://random-words.trycloudflare.com`. Have a human review the URL and intended audience before sharing.

#### Named Tunnel

First authenticate (one-time):

```bash
bash "$SKILL_DIR/scripts/tunnel.sh" login
```

Create the tunnel (one-time per project):

```bash
bash "$SKILL_DIR/scripts/tunnel.sh" create my-project
```

Run the tunnel:

```bash
bash "$SKILL_DIR/scripts/tunnel.sh" named my-project <port>
```

### 4. Stop the Tunnel

Press `Ctrl+C` in the terminal, or:

```bash
bash "$SKILL_DIR/scripts/tunnel.sh" stop
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
bash "$SKILL_DIR/scripts/tunnel.sh" quick 3000
```

**Vite dev server (port 5173):**
```bash
bash "$SKILL_DIR/scripts/tunnel.sh" quick 5173
```

**Django/Rails/Express (port 8000):**
```bash
bash "$SKILL_DIR/scripts/tunnel.sh" quick 8000
```

**PHP built-in server (port 8080):**
```bash
bash "$SKILL_DIR/scripts/tunnel.sh" quick 8080
```

## Troubleshooting

- **"config.yaml exists" error with quick tunnels:** Quick tunnels fail if `~/.cloudflared/config.yaml` exists. Prefer a named tunnel. Only relocate existing configuration after reviewing its purpose and an explicit restoration plan.
- **HTTP 429 errors:** Quick tunnels cap at 200 concurrent in-flight requests. For higher traffic, use a named tunnel.
- **SSE not working:** Quick tunnels do not support Server-Sent Events. Use a named tunnel instead.
- **Tunnel stops when terminal closes:** Run with `nohup` or `screen`/`tmux` to persist across terminal sessions.
