---
name: adr-review
description: Review a codebase against Lullabot's ADRs and report deviations and fixes
---

# ADR review

Review the current project against Lullabot's accepted Architecture Decision Records (ADRs), published at https://architecture.lullabot.com. Write a report of where the project follows them and where it deviates, with steps to resolve each deviation. Then offer to copy the report into a Google Doc and to file issues for the deviations.

Arguments (optional): a path for the report. Default: `docs/adr-review-YYYY-MM-DD.md` in the project root, using today's date.

## 1. Get the ADRs

Use a temporary directory outside the project (`mktemp -d`) for anything you download, and delete it when you're done.

**Public site (default):** `https://architecture.lullabot.com/rss.xml` lists every published ADR with its title, link, context (`description`), tags (`category`) and date. Fetch each ADR's page from its link when you need its full text. Pages of deprecated ADRs say so and link to the ADR that replaces them; skip those.

**Git (faster, if you have access):** Lullabot staff can clone the source instead: `git clone --depth 1 git@github.com:Lullabot/architecture.git <tmp>`. If the clone fails, use the public site without asking. In a clone, read the front matter of each `adrs/*.md` file (`title`, `status`, `tags`, `context`) and keep only `status: accepted`.

Record the source for the report: `Lullabot/architecture@<git rev-parse --short HEAD>`, or `architecture.lullabot.com, <date>`.

Each ADR's ID is the last part of its URL, which matches its file name without `.md` (e.g. `20260320-use-phpstan`), and its URL is `https://architecture.lullabot.com/adr/<ID>/`.

## 2. Find project overrides

Lullabot's ADRs allow a project to override a decision when the client needs it, as long as the project records that in its own ADR. Look for project-level ADRs or decision records (e.g. `docs/adr/`, `docs/adrs/`, `docs/decisions/`, `adr/`, `architecture/`, or ADR sections in `README.md` or `AGENTS.md`). Note each one that overrides, amends or replaces a Lullabot ADR.

## 3. Decide which ADRs apply

Detect the project's stack from cheap signals before reading ADRs in full:

- Drupal: `composer.json` requiring `drupal/core` or `drupal/core-recommended`; note the core version.
- PHP: `composer.json`, `*.php` files.
- Front end: `package.json`, themes (`web/themes/custom`), `*.ts`, `*.css`, `*.twig`.
- Local and CI: `.ddev/`, `.github/workflows/`, `.gitlab-ci.yml`, `.tugboat/`, `Taskfile.yml`, `renovate.json`.

Use each ADR's title, tags and context to mark it **Not applicable** when it clearly doesn't fit the stack (e.g. a Gatsby ADR on a Drupal-only site), with a one-line reason. Don't fetch or read the full text of those.

## 4. Check each applicable ADR

For each remaining ADR, read its Decision section and turn it into concrete checks: a file that should exist, a config value, a dependency, a code pattern to search for, or a sample of the relevant code. Gather evidence as `path:line`.

For large codebases, check the ADRs in groups by tag (e.g. `drupal`, `php`, `front-end`, `ci`), using subagents if your tool supports them.

Give each ADR one verdict:

| Verdict              | Meaning                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Follows**          | The project does what the ADR says.                                                                                                 |
| **Partial**          | Some of the project does, some doesn't (e.g. one theme of two, or new code but not CI).                                             |
| **Deviates**         | The project does something else, or nothing.                                                                                        |
| **Overridden**       | It deviates, but a project ADR documents why.                                                                                       |
| **Not applicable**   | The ADR doesn't fit this project's stack.                                                                                           |
| **Unable to verify** | The ADR is about something outside the code, such as hosting, process or the Drupal UI. Say what a person should check, and where. |

Rules:

- Every verdict needs evidence: a `path:line`, a command and its result, or the reason it doesn't apply. Don't guess. If you're not sure, say so and use **Unable to verify**.
- Cite paths, never quote secrets, credentials or values from `.env` or `settings.local.php` files.
- Existing code in an inherited codebase may predate an ADR. Note that in the deviation, but still report it.

## 5. Write the report

Write the report to the path from the arguments, or `docs/adr-review-YYYY-MM-DD.md`. Create the directory if needed. Use this structure:

```markdown
# ADR review: <project name>

- Date: YYYY-MM-DD
- Project commit: <git rev-parse --short HEAD>
- ADR source: Lullabot/architecture@<sha> (or architecture.lullabot.com, <date>)
- Results: <n> follow, <n> partial, <n> deviate, <n> overridden, <n> not applicable, <n> unable to verify

## Summary

| ID | ADR | Verdict | Evidence | Effort |
| --- | --- | --- | --- | --- |
| ADR-20260320-use-phpstan | [Use PHPStan …](https://architecture.lullabot.com/adr/20260320-use-phpstan/) | Deviates | `composer.json` has no phpstan | M |

## Deviations

<!-- Partial and Deviates, ordered by impact, then effort (S/M/L). -->

### ADR-<ID>: <ADR title>

- **Verdict:** Deviates
- **The ADR requires:** <one or two sentences>
- **The project does:** <what you found, with `path:line`>
- **Impact:** <why it matters for this project>
- **Effort:** S | M | L

To resolve:

- [ ] <concrete step, naming files and commands>
- [ ] <next step>
- [ ] Or, if this deviation is deliberate, record it in a project ADR explaining why.

## Overridden

- ADR-<ID>: <title>, overridden by `<path to project ADR>`.

## Follows

- ADR-<ID>: <title>, `<evidence>`.

## Not applicable

- ADR-<ID>: <title>, <reason>.

## Unable to verify

- ADR-<ID>: <title>, <what a person should check, and where>.
```

Keep the IDs stable (`ADR-` plus the ADR's ID) so a later review can be compared with this one, and issues can link back to it. If an earlier report exists in the same directory, add a short "Changes since <date>" section listing deviations that were resolved and new ones.

## 6. Summarize in the chat

Print the result counts, the top five deviations (ID, title, one line each), and the report's path. Ask the user to review the report before sharing it: the verdicts are a draft.

## 7. Offer a Google Doc

If you can write to Google Drive, offer to copy the report into a Google Doc for people who don't read Markdown in the repository. You can write to Drive if any of these is true:

- you have a Google Docs or Google Drive tool;
- the `gws` CLI is installed and `gws drive about get --params '{"fields": "user"}'` succeeds (see the `gws-cli` skill if it's available).

If neither is available, skip this step without mentioning it.

Ask before creating it, and say which account it goes to. Then:

- Upload the Markdown report and have Drive convert it: create the file with `"mimeType": "application/vnd.google-apps.document"` and the report as `text/markdown` media. With `gws`: `gws drive files create --json '{"name": "ADR review: <project> (YYYY-MM-DD)", "mimeType": "application/vnd.google-apps.document"}' --upload <report path>`. If your tool can only create a Doc from text, create it from the report's content and keep its headings, table and checklists.
- Leave it private to that account. Don't share it or move it into a shared folder unless the user asks.
- Check that the Doc opens and has the summary table, then give the user its link and add the link to the top of the Markdown report.

The Markdown report stays the source of truth. If the review is run again, create a new Doc rather than editing the old one.

## 8. Offer to file issues

Detect where the project tracks issues:

- **GitHub:** `git remote -v` points at github.com and `gh auth status` succeeds.
- **GitLab:** the remote points at a GitLab host and `glab auth status` succeeds.
- **Jira:** a Jira or Atlassian tool is available to you, or the project uses Jira keys (e.g. `ABC-123` in branch names, recent commit messages or docs). Ask the user for the project key if it isn't clear, and use that tool, or the `jira` or `acli` CLI if installed.

If none is found, say so and point to the report's checklists. Don't ask for one.

If one is found, offer to create issues for the **Partial** and **Deviates** findings. Show the list of issue titles first and ask whether to create one issue per deviation or a single tracking issue with every checklist. Create nothing without an explicit yes.

- Title: `ADR deviation: <ADR title>`
- Body: the deviation's section from the report, a link to the ADR, and the report's path (and the Google Doc's link, if you created one). If the `issue-writing` skill is available, follow it for the body.

After creating them, add each issue's link under its deviation in the report.
