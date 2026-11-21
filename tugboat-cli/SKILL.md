---
name: tugboat-cli
description: This skill should be used when managing Tugboat preview environments via the tugboat CLI. It applies when creating, listing, rebuilding, refreshing, debugging, or administering Tugboat previews, services, and repositories. Triggers on tugboat commands, preview environment management, .tugboat/config.yml editing, and Tugboat QA workflow questions.
---

# Tugboat CLI

## Requirements

The `tugboat` CLI, network access, and an API token scoped to the intended project/repository (configured with `~/.tugboat.yml` or `TUGBOAT_API_TOKEN`). A shell and local file access support configuration work. The optional upload companion needs Python 3.9+ locally and Bash plus `base64` in the destination service. It constructs an argv array; it does not require an agent-specific tool or MCP server.

Resolve `SKILL_DIR` to the absolute directory containing the loaded `SKILL.md`, using the skill location supplied by the agent or locating this file. Set it explicitly (for example, `SKILL_DIR="/path/to/installed/tugboat-cli"`); do not derive it from the project working directory. Run project-relative commands from the working project and use `"$SKILL_DIR/..."` for companions.

## Safety and review

Listing is read-only; preview lifecycle actions, config changes, access grants/revocations, key creation, remote shell commands, and uploads can change data or incur builds. A human reviews exact project/repository/service IDs, refs, command argv, affected data, downtime, and costs before each mutation. Use the narrowest token, avoid root/admin and force flags, and keep TLS verification enabled. Verify build lifecycle commands and dependency sources before create/rebuild/refresh. Logs/mail/screenshots may contain personal information or secrets; limit retrieval and use eligible tooling. Uploading into the docroot publishes the file at the preview URL, so use sanitized public content only and review destination/overwrite effects before execution. Human review of reports, screenshots, and audience precedes sharing preview URLs; no CLI token establishes tool approval.

Outside a verified secure sandbox, a human must read and understand unreviewed shell commands and generated code before execution. Always review MCP data-changing operations if an MCP alternative is used. Use least privilege; tool installation requires Security Team review and verification of upstream identity. Personal information requires approved tooling integrated with its source system; confidential information requires specifically approved tools; non-public information requires tools that neither train on nor retain it. Never send sensitive non-public data to public AI models. Stop when eligibility is unknown. An AI check does not replace human self-review before sharing, publishing, or handing work to another reviewer.


## Overview

Tugboat is a preview environment service (tugboatqa.com) that builds fully functional website previews for branches, tags, commits, and pull requests. This skill provides guidance for using the `tugboat` CLI to manage previews, services, repositories, and related resources.

## Prerequisites

- The `tugboat` CLI must be installed (`brew install tugboatqa/tugboat/tugboat-cli` on macOS)
- An API access token must be configured (generated at https://dashboard.tugboatqa.com/access-tokens)
- Token is stored in `~/.tugboat.yml` after first use, or passed via `-t` flag or `TUGBOAT_API_TOKEN` env var

## Quick Start

To list available projects and repos:
```bash
tugboat ls projects
tugboat ls repos
```

To create a preview from a branch:
```bash
tugboat ls repos                                    # Find the repo ID
tugboat create preview <branch> repo=<repo-id>      # Create preview
```

To check preview status and open it:
```bash
tugboat ls previews repo=<repo-id>
tugboat ls <preview-id> -b                          # Open in browser
```

## Common Workflows

### Creating and Managing Previews

```bash
# Create a preview from a branch or PR
tugboat create preview <ref> repo=<repo-id>
tugboat create preview <ref> repo=<repo-id> type=pullrequest
tugboat create preview <ref> repo=<repo-id> base=false    # Skip base preview

# Preview lifecycle
tugboat refresh <preview-id>     # Pull latest code, run update+build
tugboat rebuild <preview-id>     # Full rebuild from scratch
tugboat reset <preview-id>       # Revert to post-build snapshot
tugboat redeploy <preview-id>    # Redeploy code

# State management
tugboat start <preview-id>
tugboat stop <preview-id>
tugboat suspend <preview-id>     # Save resources
tugboat cancel <preview-id>      # Cancel active build
tugboat delete <preview-id>      # Delete exact reviewed preview; retain confirmation
```

### Base Previews (Speed Up Builds)

Base previews are snapshots that child previews clone from instead of building from scratch.

```bash
# Create and anchor a base preview
tugboat create preview main repo=<repo-id> anchor=true

# Or anchor an existing preview
tugboat update <preview-id> anchor=true

# List base previews
tugboat ls previews repo=<repo-id> anchor=true

# Rebuild base to keep it fresh
tugboat rebuild <base-preview-id>
```

### Debugging Previews

```bash
# Check build logs
tugboat log <preview-id>
tugboat log <preview-id> -a              # Attach and follow

# List services to find service IDs
tugboat ls services preview=<preview-id>

# Shell into a preview or service
tugboat shell <preview-id>               # Default service
tugboat shell <service-id>               # Specific service
tugboat shell <id> command="drush status"  # Run a command

# View service output
tugboat output <service-id>
```

### Uploading a File Into a Preview (e.g. an HTML report)

There is **no `tugboat cp`/upload command**, and two non-obvious traps make naive
approaches fail silently:

1. **`tugboat shell ... command=` does NOT forward stdin.** `cat localfile | tugboat shell <id> command="cat > dest"` produces an *empty* file — the pipe is ignored.
2. **A plain string `command=` is split on whitespace and exec'd directly — it is NOT run through a shell.** So `command="echo hi > /tmp/x"` passes `>` and `/tmp/x` as literal args to `echo`; redirects and pipes never happen.

**The working pattern: pass `command=` a JSON array of argv** (`["bash","-c","<script>"]`).
A JSON array is honored verbatim, so the script string runs through a real shell with
pipes/redirects intact. Carry the file content as base64 inside that script:

Confirm the exact service ID and docroot with read-only commands first (`tugboat ls services preview=<preview-id>` and a reviewed `ls` command). Then use the bundled companion:

```bash
# Preview only: does not contact Tugboat or write a command file.
python3 "$SKILL_DIR/scripts/upload_file.py" report.html \
  --service <service-id> --destination /var/lib/tugboat/web/report.html
# After human review of file contents, target path, and URL exposure, repeat with --execute.
```

The companion constructs the JSON argv and quotes the destination for the remote Bash script. It defaults to preserving existing files; `--overwrite` is an explicit additional reviewed effect. File bytes are carried in the command arguments, so use sanitized public data only. Large files may exceed local/remote argv limits; stop on that error instead of silently splitting the upload. Read [scripts/upload_file.py](scripts/upload_file.py) when adapting it, and verify local payload behavior with `python3 -m unittest discover -s "$SKILL_DIR/tests"`.

**Re-uploading:** preview files placed this way live outside git, so a `tugboat rebuild`
(or a fresh build) wipes them — just re-run the steps above to restore the file. Use
`printf %s` (not `echo`) so no trailing newline corrupts binary payloads.

### Listing and Filtering Resources

```bash
# Projects, repos, previews
tugboat ls projects
tugboat ls repos
tugboat ls previews repo=<repo-id>

# Services, screenshots, visual diffs
tugboat ls services preview=<preview-id>
tugboat ls screenshots service=<service-id>
tugboat ls visualdiffs preview=<preview-id>

# Git info from repos
tugboat ls branches <repo-id>
tugboat ls pulls <repo-id>
tugboat ls pulls <repo-id> state=all     # Include closed PRs
tugboat ls tags <repo-id>
```

### JSON Output for Scripting

Append `-j` or `--json` to any command for JSON output. Combine with `-q` for just IDs.

```bash
tugboat ls previews repo=<repo-id> -j
tugboat create preview main repo=<repo-id> -q    # Returns just the preview ID
```

### Config Validation

Validate a `.tugboat/config.yml` before committing:
```bash
tugboat validate .tugboat/config.yml
tugboat validate <repo-id>              # Validate against a repo
tugboat validate <repo-id> <git-ref>    # Validate a specific ref
```

## Config File (.tugboat/config.yml)

The `.tugboat/config.yml` file in a repository defines the Docker services and lifecycle commands for previews. For the full configuration schema including service properties, lifecycle phases (init, update, build, ready, online, start, clone), and environment variables, read `references/cli_reference.md`.

Key concepts:
- **Services** are Docker containers (e.g., apache, mysql, redis)
- The `default: true` service receives the preview URL
- The `checkout: true` service gets the git clone
- **Lifecycle phases** run commands at different stages (init for fresh builds, update for data imports, build for every build)
- Services can depend on each other via `depends`

## Reference

For the complete command reference, configuration schema, environment variables, and API details, load `references/cli_reference.md`.
