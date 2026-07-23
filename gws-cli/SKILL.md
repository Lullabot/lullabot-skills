---
name: gws-cli
description: This skill should be used when users need to interact with Google Workspace services (Gmail, Calendar, Drive, Sheets, Docs, Tasks, Chat, etc.) from the command line. Use when users ask to send/read email, check calendar, upload files, read spreadsheets, manage tasks, or perform any Google Workspace operation. Triggers on "check my email", "send email", "calendar", "agenda", "upload to drive", "read spreadsheet", "google workspace", "gws", or any request involving Gmail, Google Calendar, Google Drive, Google Sheets, Google Docs, or Google Tasks.
---

# Google Workspace CLI (gws)

Use the `gws` CLI for ALL Google Workspace operations. Do NOT use MCP tools for Gmail, Calendar, Drive, or Sheets -- always prefer `gws`.

## Command Structure

```
gws <service> <resource> [sub-resource] <method> [flags]
```

Helper commands use `+` prefix for common operations:
```
gws <service> +<helper> [flags]
```

## Services

| Service | Description |
|---------|-------------|
| `gmail` | Send, read, and manage email |
| `calendar` | Manage calendars and events |
| `drive` | Manage files, folders, and shared drives |
| `sheets` | Read and write spreadsheets |
| `docs` | Read and write Google Docs |
| `slides` | Read and write presentations |
| `tasks` | Manage task lists and tasks |
| `chat` | Manage Chat spaces and messages |
| `people` | Manage contacts and profiles |
| `forms` | Read and write Google Forms |
| `keep` | Manage Google Keep notes |
| `meet` | Manage Google Meet conferences |
| `workflow` | Cross-service productivity workflows (alias: `wf`) |

## Global Flags

| Flag | Description |
|------|-------------|
| `--params <JSON>` | URL/Query parameters as JSON |
| `--json <JSON>` | Request body as JSON (POST/PATCH/PUT) |
| `--upload <PATH>` | Local file to upload as media content |
| `--output <PATH>` | Output file path for binary responses |
| `--format <FMT>` | Output format: `json` (default), `table`, `yaml`, `csv` |
| `--page-all` | Auto-paginate (NDJSON output) |
| `--page-limit <N>` | Max pages with --page-all (default: 10) |
| `--dry-run` | Validate without sending to API |

## Gmail

### Helpers (preferred for common tasks)

**Send email:**
```bash
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi Alice!'
gws gmail +send --to alice@example.com --subject 'Report' --body 'See attached' -a report.pdf
gws gmail +send --to alice@example.com --subject 'Hello' --body '<b>Bold</b>' --html
gws gmail +send --to a@ex.com --subject 'Hi' --cc b@ex.com --bcc c@ex.com --body 'Hello'
```

**Save as draft (instead of sending):**
```bash
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi Alice!' --draft
```

**Triage inbox (read-only):**
```bash
gws gmail +triage                              # Unread inbox summary (table)
gws gmail +triage --max 5 --query 'from:boss'  # Filtered
gws gmail +triage --format json                # JSON output
gws gmail +triage --labels                     # Include label names
```

**Read a message:**
```bash
gws gmail +read --id <MESSAGE_ID>
gws gmail +read --id <MESSAGE_ID> --headers    # Include From, To, Subject, Date
gws gmail +read --id <MESSAGE_ID> --format json
```

**Reply to a message:**
```bash
gws gmail +reply --message-id <ID> --body 'Thanks!'
gws gmail +reply --message-id <ID> --body 'Looping in Carol' --cc carol@ex.com
gws gmail +reply --message-id <ID> --body '<b>Bold</b>' --html
```

**Reply-all:**
```bash
gws gmail +reply-all --message-id <ID> --body 'Sounds good!'
```

**Forward a message:**
```bash
gws gmail +forward --message-id <ID> --to dave@example.com
gws gmail +forward --message-id <ID> --to dave@example.com --body 'FYI see below'
```

### Plain-text wrapping gotcha (draft looks unwrapped, sent looks hard-wrapped)

By default (any body you don't send with `--html`), `gws` builds email bodies as `Content-Type: text/plain` and stores each paragraph as a single logical line, wrapped only with quoted-printable *soft* breaks (a `=` at end of line, which every client strips and reflows). So a gws-created draft renders unwrapped everywhere gws touches it, and gws's own `+send` and `+reply` put it on the wire the same way -- unwrapped. gws does NOT insert real newlines into your paragraphs.

The hard wrapping people see comes from **Gmail's web compose, not gws**. A `text/plain` message opens in Gmail's plain-text compose mode, and Gmail hard-wraps outgoing plain text at ~70 columns *at send time*. So the common pattern is: draft with `gws ... --draft`, open it in the Gmail web UI to review or add Cc, then hit Send -- and Gmail rewrites `Count me in` into `Count` + newline + `me in` with genuine newlines. The draft never changed; the Gmail Send step rewraps it.

You can verify this by comparing raw MIME:

```bash
gws gmail users messages get --params '{"userId": "me", "id": "<ID>", "format": "raw"}'
```

A gws draft and a gws direct-send both show soft breaks (`much lon=` then `ger` on the next line), while a message sent through the Gmail UI shows hard breaks (`Count` then `me in`, with no trailing `=`).

Two ways to avoid the wrap:

- **Send straight from gws** (`gws gmail +send` / `+reply` with `--cc`/`--to`/`--bcc`), skipping the Gmail Send button entirely. gws transmits the body unwrapped. You lose the in-Gmail review step.
- **Build the draft as HTML** (`--html`, using real `<p>...</p>`/`<br>` tags, NOT markdown). An HTML message opens in Gmail's rich-text mode, which doesn't do the plain-text column wrap, so you keep the "review and add Cc in Gmail before sending" workflow without the hard wrap.

There is no clean way to keep composing plain text in Gmail *and* avoid the wrap: the wrap is Gmail's behavior, not gws's.

### Raw API

**Search/list messages:**
```bash
gws gmail users messages list --params '{"userId": "me", "q": "subject:invoice after:2026/01/01"}'
gws gmail users messages list --params '{"userId": "me", "labelIds": ["INBOX"], "maxResults": 10}'
```

**Get message details:**
```bash
gws gmail users messages get --params '{"userId": "me", "id": "<MESSAGE_ID>"}'
```

**Manage labels:**
```bash
gws gmail users labels list --params '{"userId": "me"}'
gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "MyLabel"}'
```

**Modify message labels:**
```bash
gws gmail users messages modify --params '{"userId": "me", "id": "<ID>"}' \
  --json '{"addLabelIds": ["STARRED"], "removeLabelIds": ["UNREAD"]}'
```

**Trash/untrash:**
```bash
gws gmail users messages trash --params '{"userId": "me", "id": "<ID>"}'
gws gmail users messages untrash --params '{"userId": "me", "id": "<ID>"}'
```

## Calendar

### Helpers

**View agenda:**
```bash
gws calendar +agenda                           # Upcoming events
gws calendar +agenda --today                   # Today only
gws calendar +agenda --tomorrow                # Tomorrow
gws calendar +agenda --week --format table     # This week as table
gws calendar +agenda --days 3 --calendar 'Work'
gws calendar +agenda --today --timezone America/New_York
```

**Create event:**
```bash
gws calendar +insert --summary 'Standup' \
  --start '2026-06-17T09:00:00-07:00' \
  --end '2026-06-17T09:30:00-07:00'

gws calendar +insert --summary 'Review' \
  --start '2026-06-17T14:00:00-07:00' \
  --end '2026-06-17T15:00:00-07:00' \
  --attendee alice@example.com --meet
```

### Raw API

**List events:**
```bash
gws calendar events list --params '{"calendarId": "primary", "timeMin": "2026-03-01T00:00:00Z", "timeMax": "2026-03-31T23:59:59Z", "singleEvents": true, "orderBy": "startTime"}'
```

**Update event:**
```bash
gws calendar events patch --params '{"calendarId": "primary", "eventId": "<EVENT_ID>"}' \
  --json '{"summary": "Updated Title"}'
```

**Delete event:**
```bash
gws calendar events delete --params '{"calendarId": "primary", "eventId": "<EVENT_ID>"}'
```

**Check free/busy:**
```bash
gws calendar freebusy query --json '{
  "timeMin": "2026-03-23T00:00:00Z",
  "timeMax": "2026-03-23T23:59:59Z",
  "items": [{"id": "primary"}]
}'
```

## Drive

### Helpers

**Upload a file:**
```bash
gws drive +upload ./report.pdf
gws drive +upload ./report.pdf --parent FOLDER_ID
gws drive +upload ./data.csv --name 'Sales Data.csv'
```

### Raw API

**List files:**
```bash
gws drive files list --params '{"pageSize": 10}'
gws drive files list --params '{"q": "mimeType=\"application/pdf\"", "pageSize": 20}'
gws drive files list --params '{"q": "name contains \"report\"", "fields": "files(id,name,modifiedTime)"}'
```

**Get file metadata:**
```bash
gws drive files get --params '{"fileId": "<FILE_ID>", "fields": "id,name,mimeType,size,webViewLink"}'
```

**Download file:**
```bash
gws drive files get --params '{"fileId": "<FILE_ID>", "alt": "media"}' --output ./downloaded-file.pdf
```

**Create folder:**
```bash
gws drive files create --json '{"name": "My Folder", "mimeType": "application/vnd.google-apps.folder"}'
```

**Move file to folder:**
```bash
gws drive files update --params '{"fileId": "<FILE_ID>", "addParents": "<FOLDER_ID>", "removeParents": "<OLD_PARENT_ID>"}'
```

**Share file:**
```bash
gws drive permissions create --params '{"fileId": "<FILE_ID>"}' \
  --json '{"role": "reader", "type": "user", "emailAddress": "alice@example.com"}'
```

## Sheets

### Helpers

**Read spreadsheet:**
```bash
gws sheets +read --spreadsheet <ID> --range "Sheet1!A1:D10"
gws sheets +read --spreadsheet <ID> --range "Sheet1" --format table
```

**Append rows:**
```bash
gws sheets +append --spreadsheet <ID> --values 'Alice,100,true'
gws sheets +append --spreadsheet <ID> --json-values '[["a","b"],["c","d"]]'
```

### Raw API

**Get spreadsheet metadata:**
```bash
gws sheets spreadsheets get --params '{"spreadsheetId": "<ID>"}'
```

**Update cell values:**
```bash
gws sheets spreadsheets values update \
  --params '{"spreadsheetId": "<ID>", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["Hello", "World"]]}'
```

## Workflows (Cross-Service)

**Standup report** (today's meetings + open tasks):
```bash
gws workflow +standup-report
```

**Meeting prep** (agenda, attendees, linked docs):
```bash
gws workflow +meeting-prep
```

**Email to task** (convert Gmail message to Google Tasks):
```bash
gws workflow +email-to-task
```

**Weekly digest** (meetings + unread count):
```bash
gws workflow +weekly-digest
```

**Announce Drive file in Chat:**
```bash
gws workflow +file-announce
```

## Schema Discovery

Explore any API method's parameters:
```bash
gws schema gmail.users.messages.list
gws schema drive.files.list --resolve-refs
gws schema calendar.events.insert
```

## Output Formats

- `--format json` (default) -- JSON output, pipe to `jq` for filtering
- `--format table` -- Human-readable table
- `--format yaml` -- YAML output
- `--format csv` -- CSV output

## Pagination

For large result sets:
```bash
gws gmail users messages list --params '{"userId": "me"}' --page-all --page-limit 5
```

## Important Notes

1. **Always use `gws` over MCP tools** for Google Workspace operations
2. **userId is always "me"** for Gmail operations on the authenticated user
3. **Use helpers (`+command`) for common tasks** -- they handle encoding, threading, MIME, etc.
4. **Use raw API for advanced operations** not covered by helpers
5. **Use `--dry-run`** to validate commands before executing destructive operations
6. **Use `--format table`** when output is for human reading
7. **Pipe JSON to `jq`** for filtering: `gws gmail +triage --format json | jq '.[].subject'`
8. **Times must be RFC 3339/ISO 8601** for calendar operations (e.g., `2026-06-17T09:00:00-07:00`)
9. **Gmail plain-text bodies get hard-wrapped by Gmail's web Send**, not by gws (see "Plain-text wrapping gotcha"). To keep paragraphs unwrapped, either send directly with `gws gmail +send`/`+reply` or draft as `--html`.
