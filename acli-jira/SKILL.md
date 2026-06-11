---
name: acli-jira
description: This skill should be used when the user asks to "get Jira issue", "view Jira ticket", "search Jira", "create Jira issue", "update Jira ticket", "transition issue status", "add comment to Jira", or mentions acli, Jira workitems, JQL queries, or Jira sprints. Provides guidance for using the Atlassian CLI (acli) to interact with Jira Cloud.
---

# Atlassian CLI (acli) for Jira

This skill provides guidance for using the `acli` command-line tool to interact with Jira Cloud.

## Overview

The Atlassian CLI (`acli`) enables command-line access to Jira Cloud. Use it to view, search, create, edit, and transition work items without leaving the terminal.

> Jira calls issues **work items**, and so does `acli` (the commands are `acli jira workitem ...`). This skill uses "work item" throughout to match the tool.

## Prerequisites

Before any command below will work, `acli` must be installed and authenticated:

```bash
# Verify acli is installed
acli --version

# Authenticate against your Jira Cloud site (interactive; opens a browser)
acli jira auth login

# Confirm the active session
acli jira auth status
```

If a command fails with an authentication or permission error, re-run `acli jira auth login`. Don't assume the environment is already set up — check `acli jira auth status` first when in doubt.

## Common Operations

### View a Work Item

Retrieve details about a specific work item:

```bash
# Basic view (key, type, summary, status, assignee, description)
acli jira workitem view KEY-123

# View specific fields only
acli jira workitem view KEY-123 --fields summary,status,comment

# View all fields
acli jira workitem view KEY-123 --fields "*all"

# JSON output for parsing
acli jira workitem view KEY-123 --json

# Open in browser
acli jira workitem view KEY-123 --web
```

### Search Work Items

Find work items using JQL (Jira Query Language):

```bash
# Search by project
acli jira workitem search --jql "project = TEAM"

# Search with specific fields
acli jira workitem search --jql "project = TEAM" --fields "key,summary,assignee,status"

# Search assigned to current user
acli jira workitem search --jql "assignee = currentUser() AND status != Done"

# Get count of matching work items
acli jira workitem search --jql "project = TEAM AND status = 'In Progress'" --count

# Paginate through all results
acli jira workitem search --jql "project = TEAM" --paginate

# Limit results
acli jira workitem search --jql "project = TEAM" --limit 20

# CSV output for spreadsheets
acli jira workitem search --jql "project = TEAM" --csv

# JSON output for parsing
acli jira workitem search --jql "project = TEAM" --json
```

### Create Work Items

Create new work items:

```bash
# Basic creation
acli jira workitem create --project "TEAM" --type "Task" --summary "New feature request"

# With description
acli jira workitem create --project "TEAM" --type "Bug" \
  --summary "Login button broken" \
  --description "Users cannot click the login button on mobile"

# With assignee and labels
acli jira workitem create --project "TEAM" --type "Story" \
  --summary "Implement dark mode" \
  --assignee "user@example.com" \
  --label "frontend,ui"

# Self-assign
acli jira workitem create --project "TEAM" --type "Task" \
  --summary "Review PRs" --assignee "@me"

# Open editor for summary and description
acli jira workitem create --project "TEAM" --type "Task" --editor

# Create subtask under parent
acli jira workitem create --project "TEAM" --type "Subtask" \
  --summary "Update tests" --parent "TEAM-123"
```

### Edit Work Items

Modify existing work items:

```bash
# Edit summary
acli jira workitem edit --key "KEY-123" --summary "Updated summary"

# Edit description
acli jira workitem edit --key "KEY-123" --description "New description text"

# Change assignee
acli jira workitem edit --key "KEY-123" --assignee "user@example.com"

# Self-assign
acli jira workitem edit --key "KEY-123" --assignee "@me"

# Remove assignee
acli jira workitem edit --key "KEY-123" --remove-assignee

# Add labels
acli jira workitem edit --key "KEY-123" --labels "urgent,blocker"

# Edit multiple work items
acli jira workitem edit --key "KEY-1,KEY-2,KEY-3" --assignee "@me"

# Bulk edit with JQL (requires confirmation)
acli jira workitem edit --jql "project = TEAM AND status = Open" --assignee "@me" --yes
```

### Transition Work Items

Change work item status.

**Status names are not universal.** Each Jira project defines its own workflow, so the valid statuses and the transitions available from the *current* status vary by project (and by the work item's current state). Don't assume `"In Progress"` or `"Done"` exist — discover the valid options for the specific work item first:

```bash
# See the current status and the transitions available from it
acli jira workitem view KEY-123 --fields status
acli jira workitem transition --key "KEY-123" --list
```

Then transition using a status name that the `--list` output actually offers:

```bash
# Transition single work item
acli jira workitem transition --key "KEY-123" --status "In Progress"

# Transition multiple work items
acli jira workitem transition --key "KEY-1,KEY-2" --status "In Review" --yes

# Bulk transition with JQL
acli jira workitem transition --jql "project = TEAM AND assignee = currentUser()" \
  --status "Done" --yes
```

If a transition is rejected, it usually means that status isn't reachable from the work item's current state — re-check `--list`.

### Comments

Manage work item comments:

```bash
# Add comment
acli jira workitem comment create --key "KEY-123" --body "Working on this now"

# List comments
acli jira workitem comment list --key "KEY-123"

# Update comment
acli jira workitem comment update --key "KEY-123" --comment-id "12345" --body "Updated comment"

# Delete comment
acli jira workitem comment delete --key "KEY-123" --comment-id "12345"
```

### Assign Work Items

```bash
# Assign to user
acli jira workitem assign --key "KEY-123" --assignee "user@example.com"

# Self-assign
acli jira workitem assign --key "KEY-123" --assignee "@me"

# Assign multiple
acli jira workitem assign --key "KEY-1,KEY-2" --assignee "@me"
```

## Bulk and Destructive Operations

`--yes` skips the confirmation prompt, and a `--jql` selector can match far more work items than expected. Deletes are irreversible. Before running any bulk edit, transition, or delete:

1. **Preview the scope first.** Run the same JQL through `search --count` (or `search` itself) to see exactly how many work items — and which ones — will be affected:

   ```bash
   acli jira workitem search --jql "project = TEAM AND status = Open" --count
   ```

2. **Confirm the count is what you expect** before re-running the command with `--yes`. If the number is surprising, tighten the JQL.

3. **For deletes, confirm with the user** and prefer `archive` over `delete` when the goal is just to get work items out of the way:

   ```bash
   acli jira workitem archive --key "KEY-123"   # reversible
   acli jira workitem delete --key "KEY-123" --yes   # permanent
   ```

Use `--ignore-errors` on bulk runs only when partial completion is acceptable; otherwise let the command stop on the first failure so problems surface immediately.

## JQL Quick Reference

Common JQL patterns for searching:

| Query | Description |
|-------|-------------|
| `project = TEAM` | Work items in project TEAM |
| `assignee = currentUser()` | Assigned to me |
| `status = "In Progress"` | Work items in progress |
| `status != Done` | Not completed |
| `created >= -7d` | Created in last 7 days |
| `updated >= -1d` | Updated in last day |
| `priority = High` | High priority work items |
| `labels = bug` | Work items with bug label |
| `sprint in openSprints()` | In current sprint |
| `ORDER BY created DESC` | Sort by newest first |

Combine with AND/OR:
```
project = TEAM AND status = "In Progress" AND assignee = currentUser()
```

## Projects and Sprints

### List Projects

```bash
acli jira project list
acli jira project view TEAM
```

### View Sprint Details

```bash
# List work items in a sprint
acli jira sprint list-workitems --sprint-id 123

# View sprint details
acli jira sprint view --sprint-id 123
```

## Output Formats

- Default: Human-readable table
- `--json`: JSON for parsing/scripting
- `--csv`: CSV for spreadsheets
- `--web`: Open in browser

## Additional Resources

For detailed command options, consult:
- **`references/commands.md`** - Complete command reference with all flags
