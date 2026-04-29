---
name: noko-log-time
description: This skill should be used when the user wants to log time to Noko from Claude Code sessions. It analyzes session logs, clusters active work segments per project, and posts time entries to the Noko API. Triggers on "log time", "noko", "track time", or at end-of-day workflows.
allowed-tools: Read, Bash, Glob, Grep, Agent, AskUserQuestion
---

Log time spent in Claude Code sessions to Noko. Arguments: $ARGUMENTS

## Overview

Analyze Claude Code session logs to calculate active time per project, then log
entries to Noko. A companion script at `~/.claude/skills/noko-log-time/scripts/session-summary.py`
handles all JSONL parsing (zero token cost); this skill handles presentation,
user confirmation, and API calls.

## Step 1: Run Session Summary Script

Execute the session summary script to extract and cluster session data:

```bash
python3 ~/.claude/skills/noko-log-time/scripts/session-summary.py [DATE]
```

- If the user provides a date argument, pass it (YYYY-MM-DD format).
- If no date argument, omit it (defaults to today).
- If the user specifies a project name only (e.g., "SDSU"), still run for the full day
  and filter to that project in the presentation step.

The script outputs JSON with per-project active minutes, segments, and prompt summaries.
It uses a 5-minute gap threshold between user messages to separate active segments,
and converts all timestamps to Pacific time.

**Project keys in output:**

- `CATIC`, `SDSU`, `ElkGrove`, `VINCI`, `ManhattanU`, `LSM` — billable client projects
- `Internal` — Lullabot internal (non-client) work (Noko project ID 17045)
- `_INTERNAL` — Hivemind dashboard/automation work; default to LSM unless user says otherwise
- `UNKNOWN` — sessions that couldn't be mapped (ask user)

## Step 2: Present Timeline

Show the user a concise timeline. Format:

```
Session Activity for [DATE]:

PROJECT (Xh Ym):
  HH:MM-HH:MM (Xm) — [first prompt summary]
  HH:MM-HH:MM (Xm) — [first prompt summary]

PROJECT (Xh Ym):
  ...

Total tracked: Xh Ym
```

For `_INTERNAL` time, ask:
> "Internal/Hivemind work detected (Xh Ym). Attribute to LSM, split across projects, or skip?"

For `UNKNOWN` time, ask which project it belongs to.

## Step 3: Adjustments

Ask:
> "Any adjustments? Examples: +1h SDSU call, +30m VINCI meeting, -15m SDSU (overcounted)"

Parse adjustment expressions:

- `+Xh PROJECT description` or `+Xm PROJECT description`
- `-Xh PROJECT` or `-Xm PROJECT`
- Multiple adjustments separated by commas or newlines

Add/subtract from project totals. Re-round each project to nearest 15 minutes (minimum 15m).

## Step 4: Categorize (Maintenance vs Professional)

For each project with time to log, determine the category.

Read env file at `~/repos/Hivemind/automation/scripts/.env` to get:

- `NOKO_API_TOKEN`
- `NOKO_USER_ID`
- `{PROJECT}_PROJECT_ID`
- `{PROJECT}_GITHUB_REPO`

**Auto-categorization from session prompts:**

- Prompts mentioning bugs, fixes, dependency updates, renovate, security, infrastructure → **maintenance**
- Prompts mentioning features, enhancements, design, content, strategy, new functionality → **professional**
- PR reviews: check the PR labels if a GitHub URL is in the prompts

**If unclear**, present each project and ask:
> "SDSU (30m): maintenance or professional? (or split, e.g., '15m maintenance, 15m professional')"

**Noko tag IDs:**

- `maintenance` → `1287532`
- `professional` → `1444878`

## Step 5: Generate Descriptions

For each entry, write a concise 1-2 sentence description suitable for client-facing time logs.
Use the prompt summaries from the script output to understand what was done.

- Include GitHub issue/PR numbers with `#` prefix when visible in prompts
- Use professional language (not "fixed a bug for the customer" but "Resolved contact form display issue #1121")
- Include the hashtag in the description (Noko convention): `#maintenance` or `#professional`

Show all entries to the user for review before logging:

```
Ready to log:
1. SDSU | 30m | #professional | Investigated contact form issues, created #1121
2. VINCI | 15m | #maintenance | PR #494 security review, generated high-res map asset
3. LSM | 30m | #maintenance | Fixed email template rendering in noko-lsm PR #975
```

> "Look good? Edit any entry by number, or 'go' to log all."

## Step 6: Log to Noko

For each confirmed entry, POST to the Noko API:

```bash
curl -s -X POST "https://api.nokotime.com/v2/entries" \
  -H "X-NokoToken: {NOKO_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "{YYYY-MM-DD}",
    "minutes": {minutes},
    "description": "{summary} #{tag_name}",
    "project_id": {project_id},
    "tag_ids": [{tag_id}]
  }'
```

- Use the date from the script output (not necessarily today if logging a past day)
- HTTP 201 = success. Show entry ID and confirmation.
- If a project has no `noko_project_id` (like `_INTERNAL`), skip it or ask which Noko project to use.

## Step 7: Summary

Show final confirmation:

```
Logged to Noko:
- 2026-04-20 | SDSU     | 30m | #professional | Investigated contact form issues
- 2026-04-20 | VINCI    | 15m | #maintenance  | PR review + map generation
- 2026-04-20 | LSM      | 30m | #maintenance  | Email template fix PR #975
Total: 1h 15m
```

## Practice Tips (for accuracy)

To help the script produce more accurate time tracking:

1. Use `/exit` when switching between projects (creates clean session boundaries)
2. Use `/clear` before starting a new task in the same project
3. Keep sessions focused on one project at a time when possible
4. The script handles overlapping sessions and idle gaps automatically
