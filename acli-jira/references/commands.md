# acli Jira Command Reference

Complete reference for all acli Jira commands.

## Top-Level Structure

```
acli jira
├── auth        # Authentication
├── board       # Board commands
├── dashboard   # Dashboard commands
├── field       # Field commands
├── filter      # Filter commands
├── project     # Project commands
├── sprint      # Sprint commands
└── workitem    # Work item (issue) commands
```

## workitem Commands

### workitem view

Retrieve information about Jira work items.

```bash
acli jira workitem view [key] [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `-f, --fields string` | Comma-separated list of fields to return (default: key,issuetype,summary,status,assignee,description) |
| `--json` | Generate JSON output |
| `-w, --web` | Open in web browser |

**Field Options:**
- `*all` - Returns all fields
- `*navigable` - Returns navigable fields
- Prefix with `-` to exclude (e.g., `-description`)
- Specific fields: `summary`, `comment`, `status`, `assignee`, `priority`, `labels`, `created`, `updated`

### workitem search

Search for work items using JQL or filter.

```bash
acli jira workitem search [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `-j, --jql string` | JQL query to search for work items |
| `--filter string` | Filter ID of work items to search |
| `-f, --fields string` | Fields to display (default: issuetype,key,assignee,priority,status,summary) |
| `-l, --limit int` | Maximum number of work items to fetch |
| `--paginate` | Fetch all results by paginating |
| `--count` | Return count only |
| `--json` | JSON output |
| `--csv` | CSV output |
| `-w, --web` | Open in browser |

### workitem create

Create a new Jira work item.

```bash
acli jira workitem create [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `-p, --project string` | Project key (required) |
| `-t, --type string` | Work item type: Epic, Story, Task, Bug, Subtask |
| `-s, --summary string` | Summary/title |
| `-d, --description string` | Description in plain text or ADF |
| `--description-file string` | Read description from file |
| `-a, --assignee string` | Assignee email, account ID, `@me`, or `default` |
| `-l, --label strings` | Labels (comma-separated) |
| `--parent string` | Parent work item ID (for subtasks) |
| `-e, --editor` | Open editor for summary/description |
| `-f, --from-file string` | Read summary and description from file |
| `--from-json string` | Read work item definition from JSON |
| `--generate-json` | Generate template JSON file |
| `--json` | Output in JSON |

### workitem edit

Edit existing work items.

```bash
acli jira workitem edit [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `-k, --key string` | Work item key(s) to edit (comma-separated) |
| `--jql string` | JQL query for work items to edit |
| `--filter string` | Filter ID of work items to edit |
| `-s, --summary string` | New summary |
| `-d, --description string` | New description |
| `--description-file string` | Read description from file |
| `-a, --assignee string` | New assignee |
| `--remove-assignee` | Remove assignee |
| `-l, --labels string` | New labels |
| `--remove-labels string` | Labels to remove |
| `-t, --type string` | Change work item type |
| `-y, --yes` | Confirm without prompting |
| `--ignore-errors` | Continue on errors |
| `--json` | JSON output |

### workitem transition

Change work item status.

```bash
acli jira workitem transition [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `-k, --key string` | Work item key(s) to transition |
| `--jql string` | JQL query for work items to transition |
| `--filter string` | Filter ID |
| `-s, --status string` | Target status |
| `-y, --yes` | Confirm without prompting |
| `--ignore-errors` | Continue on errors |
| `--json` | JSON output |

### workitem assign

Assign work items to users.

```bash
acli jira workitem assign [flags]
```

**Assignee Values:**
- Email address: `user@example.com`
- Account ID: `5b10ac8d82e05b22cc7d4ef5`
- Self: `@me`
- Default assignee: `default`

### workitem comment

Manage work item comments.

**Subcommands:**
```bash
acli jira workitem comment create --key KEY-123 --body "Comment text"
acli jira workitem comment list --key KEY-123
acli jira workitem comment update --key KEY-123 --comment-id 12345 --body "Updated text"
acli jira workitem comment delete --key KEY-123 --comment-id 12345
```

### workitem attachment

Manage work item attachments.

```bash
acli jira workitem attachment list --key KEY-123
acli jira workitem attachment add --key KEY-123 --file /path/to/file.pdf
acli jira workitem attachment delete --key KEY-123 --attachment-id 12345
```

### workitem link

Link work items together.

```bash
acli jira workitem link create --from KEY-1 --to KEY-2 --type "blocks"
acli jira workitem link list --key KEY-123
acli jira workitem link delete --id 12345
```

### workitem clone

Duplicate a work item.

```bash
acli jira workitem clone --key KEY-123
```

### workitem archive/unarchive

Archive or restore work items.

```bash
acli jira workitem archive --key KEY-123
acli jira workitem unarchive --key KEY-123
```

### workitem delete

Delete work items (use with caution).

```bash
acli jira workitem delete --key KEY-123 --yes
```

## project Commands

### project list

List visible projects.

```bash
acli jira project list
```

### project view

View project details.

```bash
acli jira project view PROJECT_KEY
```

### project create

Create a new project.

```bash
acli jira project create --name "Project Name" --key "PROJ" --type "software"
```

## sprint Commands

### sprint view

View sprint details.

```bash
acli jira sprint view --sprint-id 123
```

### sprint list-workitems

List work items in a sprint.

```bash
acli jira sprint list-workitems --sprint-id 123
```

### sprint create

Create a new sprint.

```bash
acli jira sprint create --board-id 1 --name "Sprint 10" --goal "Complete feature X"
```

### sprint update

Update sprint details.

```bash
acli jira sprint update --sprint-id 123 --name "Sprint 10 (Extended)" --goal "Updated goal"
```

## board Commands

### board list

List Jira boards.

```bash
acli jira board list
```

### board view

View board details.

```bash
acli jira board view --board-id 1
```

## filter Commands

### filter list

List saved filters.

```bash
acli jira filter list
```

### filter view

View filter details.

```bash
acli jira filter view --filter-id 10001
```

## field Commands

### field list

List available fields.

```bash
acli jira field list
```

## JQL Reference

### Operators

| Operator | Example |
|----------|---------|
| `=` | `status = "In Progress"` |
| `!=` | `status != Done` |
| `>`, `>=`, `<`, `<=` | `created >= -7d` |
| `~` | `summary ~ "search text"` (contains) |
| `!~` | `summary !~ "exclude"` (does not contain) |
| `IN` | `status IN ("Open", "In Progress")` |
| `NOT IN` | `status NOT IN (Done, Closed)` |
| `IS` | `assignee IS EMPTY` |
| `IS NOT` | `assignee IS NOT EMPTY` |

### Functions

| Function | Description |
|----------|-------------|
| `currentUser()` | Current authenticated user |
| `now()` | Current timestamp |
| `startOfDay()` | Start of current day |
| `endOfDay()` | End of current day |
| `startOfWeek()` | Start of current week |
| `startOfMonth()` | Start of current month |
| `openSprints()` | Active sprints |
| `closedSprints()` | Completed sprints |
| `futureSprints()` | Upcoming sprints |

### Date Shortcuts

| Shortcut | Meaning |
|----------|---------|
| `-1d` | 1 day ago |
| `-7d` | 7 days ago |
| `-1w` | 1 week ago |
| `-1M` | 1 month ago |

### Common Queries

```jql
# My open issues
assignee = currentUser() AND status != Done

# High priority bugs
project = TEAM AND issuetype = Bug AND priority = High

# Recently updated
updated >= -1d ORDER BY updated DESC

# Unassigned in current sprint
sprint in openSprints() AND assignee IS EMPTY

# Created this week
created >= startOfWeek()

# Blocking issues
issueLinkType = "blocks" AND status != Done

# Epics with incomplete stories
issuetype = Epic AND "Epic Link" IS NOT EMPTY AND status != Done
```

## Error Handling

When using `--ignore-errors` with bulk operations, acli continues processing remaining items if individual operations fail.

Always use `--yes` flag for non-interactive scripts to skip confirmation prompts.

## JSON Output Parsing

Use `--json` flag with `jq` for scripting:

```bash
# Get just the issue key
acli jira workitem view KEY-123 --json | jq -r '.key'

# Get all keys from search
acli jira workitem search --jql "project = TEAM" --json | jq -r '.[].key'

# Get summary and status
acli jira workitem search --jql "assignee = currentUser()" --json | jq '.[] | {key, summary, status: .status.name}'
```
