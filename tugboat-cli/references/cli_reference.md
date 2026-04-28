# Tugboat CLI Command Reference

## Global Options

| Flag | Description |
|------|-------------|
| `-V`, `--version` | Output the version number |
| `-u`, `--api-url <url>` | The URL to the Tugboat API. Default: `https://api.tugboatqa.com` |
| `-p`, `--proxy <url>` | HTTP/HTTPS proxy URL for API connections |
| `-t`, `--api-token <token>` | Access token for the Tugboat API |
| `-k`, `--no-check-certificate` | Skip API certificate verification |
| `-q`, `--quiet` | No output, just return object ID or status code |
| `-v`, `--verbose` | Verbose output (ignored if `--quiet`) |
| `-j`, `--json` | Raw JSON output (ignored if `--quiet` or `--verbose`) |
| `-w`, `--write [path]` | Write output to file (overrides `--quiet`, `--verbose`, `--json`) |
| `--debug` | Debug output (not applied if `--quiet`) |
| `-f`, `--force` | Force an operation to execute |
| `--no-color` | Disable color output |
| `-b`, `--browser [browser]` | Open preview URL in default browser |
| `--tree` | Show output in a tree |

## Commands

### list|ls

List or show details of Tugboat resources.

```bash
tugboat ls <resource-type>           # List all of a resource type
tugboat ls <id>                      # Show details of a specific resource
tugboat ls previews repo=<repo-id>   # Filter previews by repo
tugboat ls services preview=<id>     # List services in a preview
tugboat ls pulls <repo-id>           # List pull requests for a repo
tugboat ls jobs <resource-id>        # List jobs for a resource
tugboat ls branches <repo-id>        # List branches for a repo
tugboat ls keys                      # List API keys
tugboat ls mail                      # List captured mail
tugboat ls projects                  # List all projects
tugboat ls repos                     # List all repositories
```

Listable resource types: `agents`, `keys`, `lighthouse`, `mail`, `previews`, `projects`, `repos`, `screenshots`, `services`, `visualdiffs`

Filter arguments per resource type:
- **previews**: `preview`, `repo`, `project`, `anchor`
- **services**: `service`, `preview`, `repo`, `project`
- **repos**: `repo`, `project`
- **screenshots**: `screenshot`, `service`, `preview`, `repo`, `project`, `data`, `crop`, `scale`
- **visualdiffs**: `visualdiff`, `screenshot`, `service`, `preview`, `repo`, `project`, `data`, `crop`, `scale`
- **pulls**: `state` (GitHub: open/closed/all; GitLab: opened/closed/merged; Bitbucket: OPEN/DECLINED/MERGED/ALL)

### create

Create Tugboat resources.

```bash
# Create a preview
tugboat create preview <ref> repo=<repo-id>
tugboat create preview main repo=<repo-id> anchor=true
tugboat create preview feature-branch repo=<repo-id> base=false
tugboat create preview pr-123 repo=<repo-id> type=pullrequest
tugboat create preview main repo=<repo-id> expires=2024-12-31 name="My Preview"

# Create other resources
tugboat create key <name>
tugboat create lighthouse <service-id> [url=/path] [screen=desktop|mobile]
tugboat create screenshot <service-id> [url=/path] [screen=desktop|tablet|mobile]
tugboat create visualdiff <screenshot-id> base=<base-screenshot-id>
tugboat create repo <name> project=<project-id>
tugboat create registry <repo-id> username=<user> password=<pass>
```

Preview create arguments:
- `repo=<id>` (required) - Repository to build from
- `type=branch|tag|commit|pullrequest|mergerequest` - Ref type disambiguation
- `base=<id>|false` - Base preview to clone from, or `false` to skip
- `name=<string>` - Friendly name
- `config=<path>` - Local YAML config file override
- `expires=<date>` - Auto-delete date (ISO 8601)
- `anchor=true` - Anchor as default base preview
- `anchor_type=repo|preview` - Anchor scope

### update

Update Tugboat resource properties.

```bash
tugboat update <id> anchor=true       # Set as base preview
tugboat update <id> anchor=false      # Remove base preview status
```

### delete|rm

Delete a Tugboat resource.

```bash
tugboat delete <id>
tugboat delete <id> -f                # Force delete without confirmation
```

### Preview Lifecycle Commands

```bash
tugboat rebuild <id>                  # Full rebuild (pulls images, runs init+update+build)
tugboat rebuild <id> base=<new-base>  # Rebuild with different base
tugboat refresh <id>                  # Pull latest code, run update+build (skip init)
tugboat redeploy <id>                 # Redeploy code on a preview
tugboat reset <id>                    # Reset to post-build snapshot
tugboat reset <id> -f                 # Force reset a stuck preview
tugboat start <id>                    # Start a stopped/suspended preview
tugboat stop <id>                     # Stop a running preview
tugboat suspend <id>                  # Suspend a preview (save resources)
tugboat cancel <id>                   # Cancel a currently building preview
tugboat clone <id>                    # Clone a preview
```

### log

View logs for a preview or service.

```bash
tugboat log <id>                      # View build logs
tugboat log <id> -a                   # Attach and watch for new entries
tugboat log <id> --attach             # Same as -a
```

### shell

Open a shell session in a preview or service.

```bash
tugboat shell <id>                    # Interactive shell on default service
tugboat shell <service-id>            # Shell into specific service
tugboat shell <id> command="cmd"      # Execute a command
tugboat shell <id> command='["script.sh", "--opt", "arg"]'  # Array form
```

### Other Commands

```bash
tugboat find <id>                     # Find a resource by ID
tugboat grant <id> <args>             # Grant access to a resource
tugboat revoke <id> <args>            # Revoke access from a resource
tugboat rekey <id>                    # Rekey a preview
tugboat validate <id|filename> [ref]  # Validate a config.yml
tugboat version                       # Show client/server versions
tugboat output <service-id>           # View output of a service
tugboat statistics <id> <item>        # Get historical statistics
```

## Configuration File (.tugboat/config.yml)

The repository config file defines preview infrastructure.

### Service Properties

```yaml
services:
  service-name:
    image: tugboatqa/httpd:2.4       # Docker image
    default: true                     # Default service (gets preview URL)
    checkout: true                    # Clone git repo into this service
    checkout_path: /var/lib/tugboat   # Where to clone
    expose: 80                        # Port exposed to Tugboat proxy
    http: false                       # Allow HTTP
    https: true                       # Allow HTTPS
    depends:
      - mysql                         # Service dependencies
    aliases:
      - foo
      - bar.example.com
    alias_type: default|domain
    subpath: false
    domain: tugboatqa.com
    urls:
      - /
      - /about
    screenshot:
      enabled: true
      fullPage: true
      timeout: 30
    visualdiff:
      enabled: true
      threshold: 0
    lighthouse:
      enabled: true
      screen:
        - desktop
        - mobile
    environment:
      VAR_NAME: value
    commands:
      init: []      # Fresh builds only - install packages
      update: []    # Fresh builds + refreshes - import data
      build: []     # Every build/refresh/rebuild - compile, clear caches
      ready: []     # After build - health checks
      online: []    # After preview is live - one-time tasks
      start: []     # Every time preview starts - start daemons
      clone: []     # When cloning from base - adjust settings
```

### Lifecycle Phases

| Phase | Runs when | Purpose |
|-------|-----------|---------|
| `init` | Fresh builds only | Install packages, configure infrastructure |
| `update` | Fresh builds + refreshes | Import databases, assets |
| `build` | Every build/refresh/rebuild | Compile code, run DB updates, clear caches |
| `ready` | After build completes | Health checks (e.g., wait for TCP port) |
| `online` | After preview is live | One-time post-launch tasks |
| `start` | Every time preview starts | Start daemons, background processes |
| `clone` | Cloning from base preview | Adjust cloned preview settings |

## Environment Variables (Inside Preview Containers)

| Variable | Description |
|----------|-------------|
| `$TUGBOAT_PREVIEW_ID` | Current preview ID |
| `$TUGBOAT_PREVIEW` | Preview ref name (e.g., `pr381`) |
| `$TUGBOAT_PREVIEW_SHA` | Git SHA used for the build |
| `$TUGBOAT_REPO` | Repository name |
| `$TUGBOAT_REPO_ID` | Repository ID |
| `$TUGBOAT_SERVICE` | Current service name |
| `$TUGBOAT_SERVICE_ID` | Current service ID |
| `$TUGBOAT_ROOT` | Git clone location (`/var/lib/tugboat`) |
| `$TUGBOAT_DEFAULT_SERVICE_URL` | Full URL of default service |
| `$TUGBOAT_DEFAULT_SERVICE_URL_HOST` | Hostname of default service |
| `$TUGBOAT_DEFAULT_SERVICE_URL_PROTOCOL` | Protocol (http/https) |
| `$TUGBOAT_DEFAULT_SERVICE_TOKEN` | Auth token for service |
| `$TUGBOAT_SMTP` | SMTP server for email capture |
| `$TUGBOAT_PROJECT_ID` | Project ID |
| `$TUGBOAT_GITHUB_OWNER` | GitHub repo owner |
| `$TUGBOAT_GITHUB_REPO` | GitHub repo name |
| `$TUGBOAT_GITHUB_PR` | GitHub PR number |
| `$DOCROOT` | Web document root path |

## Authentication

### Access Token Setup
1. Generate at https://dashboard.tugboatqa.com/access-tokens
2. Configure via: first run prompt, `~/.tugboat.yml`, `-t` flag, or `TUGBOAT_API_TOKEN` env var

### Config File (~/.tugboat.yml)
Stores the API token after first configuration.

## API Reference
Full API docs: https://api.tugboatqa.com/v3
