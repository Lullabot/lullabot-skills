---
name: tugboat-cli
description: This skill should be used when managing Tugboat preview environments via the tugboat CLI. It applies when creating, listing, rebuilding, refreshing, debugging, or administering Tugboat previews, services, and repositories. Triggers on tugboat commands, preview environment management, .tugboat/config.yml editing, and Tugboat QA workflow questions.
---

# Tugboat CLI

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
tugboat delete <preview-id>      # Delete (add -f to skip confirmation)
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
