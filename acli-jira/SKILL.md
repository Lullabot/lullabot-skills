---
name: acli-jira
description: This skill should be used when the user asks to "get Jira issue", "view Jira ticket", "search Jira", "create Jira issue", "update Jira ticket", "transition issue status", "add comment to Jira", or mentions acli, Jira workitems, JQL queries, or Jira sprints. Provides guidance for using the Atlassian CLI (acli) to interact with Jira Cloud.
version: 1.0.0
---

# Atlassian CLI (acli) for Jira

This skill provides guidance for using the `acli` command-line tool to interact with Jira Cloud.

## Overview

The Atlassian CLI (`acli`) enables command-line access to Jira Cloud. Use it to view, search, create, edit, and transition work items (issues) without leaving the terminal.

## Common Operations

### View a Work Item

Retrieve details about a specific issue:

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

Find issues using JQL (Jira Query Language):

```bash
# Search by project
acli jira workitem search --jql "project = TEAM"

# Search with specific fields
acli jira workitem search --jql "project = TEAM" --fields "key,summary,assignee,status"

# Search assigned to current user
acli jira workitem search --jql "assignee = currentUser() AND status != Done"

# Get count of matching issues
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

Create new issues:

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

Modify existing issues:

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

# Edit multiple issues
acli jira workitem edit --key "KEY-1,KEY-2,KEY-3" --assignee "@me"

# Bulk edit with JQL (requires confirmation)
acli jira workitem edit --jql "project = TEAM AND status = Open" --assignee "@me" --yes
```

### Transition Work Items

Change issue status:

```bash
# Transition single issue
acli jira workitem transition --key "KEY-123" --status "In Progress"

# Transition to Done
acli jira workitem transition --key "KEY-123" --status "Done"

# Transition multiple issues
acli jira workitem transition --key "KEY-1,KEY-2" --status "In Review" --yes

# Bulk transition with JQL
acli jira workitem transition --jql "project = TEAM AND assignee = currentUser()" \
  --status "Done" --yes
```

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

## JQL Quick Reference

Common JQL patterns for searching:

| Query | Description |
|-------|-------------|
| `project = TEAM` | Issues in project TEAM |
| `assignee = currentUser()` | Assigned to me |
| `status = "In Progress"` | Issues in progress |
| `status != Done` | Not completed |
| `created >= -7d` | Created in last 7 days |
| `updated >= -1d` | Updated in last day |
| `priority = High` | High priority issues |
| `labels = bug` | Issues with bug label |
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
