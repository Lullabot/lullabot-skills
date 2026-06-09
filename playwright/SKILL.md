# Playwright

Open a browser session with playwright-cli to help debug issues or work with testing instructions.

## Usage

```
/playwright <url>
```

## Instructions

When invoked with a URL:

1. **Open the browser session**
   ```
   playwright-cli open <URL> --headed
   ```

2. **Ask the user what they need help with**
   - Debugging an issue they're seeing in the browser
   - Authoring testing instructions (manual QA steps)
   - Following existing testing instructions

3. **Based on their goal, assist by:**

   **For debugging:**
   - Take screenshots to see the current state
   - Check console logs for errors
   - Inspect network requests if relevant
   - Help identify the root cause of visual or functional issues

   **For authoring testing instructions:**
   - Explore the page to understand the feature/flow
   - Write clear, step-by-step instructions a human tester can follow
   - Include expected results for each step
   - Note any edge cases or variations to test

   **For following testing instructions:**
   - Execute each step as described
   - Report what you observe at each step
   - Take screenshots as evidence
   - Flag any discrepancies from expected behavior

4. **Keep the session interactive** - wait for user direction between actions rather than assuming what to do next.

## Command reference

Run commands directly as `playwright-cli <command>` (NOT `npx playwright-cli`).

### Key commands

| Command | Description |
|---------|-------------|
| `playwright-cli open <URL> --headed` | Open browser session |
| `playwright-cli snapshot` | Capture accessibility snapshot (returns element refs) |
| `playwright-cli screenshot` | Screenshot viewport (no arguments) |
| `playwright-cli fill <ref> <text>` | Fill a form field |
| `playwright-cli click <ref>` | Click an element |
| `playwright-cli type <text>` | Type text into focused element |
| `playwright-cli press <key>` | Press a key (e.g., `Enter`) |
| `playwright-cli eval <func> [ref]` | Evaluate JS on page or element |
| `playwright-cli console` | List console messages |
| `playwright-cli goto <url>` | Navigate to URL |
| `playwright-cli reload` | Reload page |

Run `playwright-cli --help` for the full list.

### Element refs

All interaction commands (`fill`, `click`, etc.) use **ref identifiers** (e.g., `e42`) from snapshots — NOT CSS selectors or IDs.

**Workflow:**
1. Run `playwright-cli snapshot` to get the current page tree with refs
2. Find the ref for the element you need (e.g., `searchbox "Search" [ref=e42]`)
3. Use that ref: `playwright-cli fill e42 "my text"`

### Important rules

- **Always snapshot first** before interacting with elements.
- **Refs go stale** after any page change (navigation, dialog open/close, content update). Take a new snapshot after state changes.
- **Snapshot/screenshot files** are saved under the skill base directory: `~/.claude/skills/playwright/.playwright-cli/`. Use absolute paths from there when reading files.
- **`screenshot` takes no arguments** — it saves to an auto-generated path and returns the file location.
- **Dialogs block interaction** with elements behind them. Close the dialog before interacting with the underlying page.

## Notes

- The browser runs in headed mode so the user can see what's happening
- Take screenshots when visual context would be helpful
