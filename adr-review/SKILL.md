---
name: adr-review
description: Review code against its ADRs and Lullabot's. Use when asked for an ADR review.
---

# ADR review

Review the current project against its accepted Architecture Decision Records (ADRs), and against Lullabot's, published at https://architecture.lullabot.com, when the project follows them. Write a report of where the project follows them and where it deviates, with steps to resolve each deviation. Then help record decisions as ADRs, and offer to copy the report into a Google Doc, file issues for the deviations and point agents at the ADRs.

Arguments (optional):

- `project` to review only the project's own ADRs, or `lullabot` to include Lullabot's without asking.
- A path for the report. Default: `docs/adr-review-YYYY-MM-DD.md` in the project root, using today's date.

## 1. Find the project's ADRs

Look for an ADR directory: `docs/adrs/`, `docs/adr/`, `doc/adr/`, `adrs/`, `adr/`, `docs/decisions/` or `architecture/`. Read each ADR's title, date and status from wherever its format keeps them: front matter (`title`, `date`, `status`), a `Date:` line and `## Status` section ([Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)), or `* Status:` and `* Date:` bullets under the title ([MADR](https://adr.github.io/madr/)). Keep only accepted ADRs; skip proposed, deprecated and superseded ones, and templates such as `*.template`.

**No ADRs yet:** before scanning, ask whether to start recording decisions. Suggest the directory the project already names, in `.adr-dir` (adr-tools), `README.md` or `AGENTS.md`. Otherwise suggest `docs/adrs/` if the project has a `docs/` directory, and `adrs/` if it doesn't. If the user agrees, write "Record architecture decisions" there from [assets/record-architecture-decisions.md](assets/record-architecture-decisions.md), as described in step 7. If they decline, review against Lullabot's ADRs only, as below.

Then find the **adoption ADR**: the project ADR whose decision is to follow Lullabot's ADRs, usually titled "Follow Lullabot's architecture decisions". Read the Lullabot ADR IDs in its "Exceptions" list from their URLs. Don't mistake the "Record architecture decisions" ADR for it: that one may link to architecture.lullabot.com for the ADR format, without adopting Lullabot's decisions.

Decide whether to include Lullabot's ADRs:

- `lullabot` or `project` argument: do what it says.
- An adoption ADR exists: include them, minus its exceptions.
- No adoption ADR, but `README.md`, `AGENTS.md` or other docs say the project follows Lullabot's ADRs: include them, minus any exclusions stated there. Before scanning, offer to record that as the adoption ADR, carrying over the exclusions and their reasons as exceptions (ask for any missing reason), and then to replace the original text with a link to the ADR so there's one source of truth. A section that already points to an adoption ADR, such as the one from step 10, doesn't count.
- The project is Lullabot's architecture repository itself (`git remote -v` points at `Lullabot/architecture`): its ADRs are Lullabot's. Review them once, as project ADRs.
- Otherwise: before scanning, ask whether the project will follow Lullabot's ADRs. If it will and it has an ADR directory, write "Follow Lullabot's architecture decisions" from [assets/follow-lullabot-adrs.md](assets/follow-lullabot-adrs.md), with no exceptions yet: step 7 adds them from the review's results. Include Lullabot's ADRs. If the user opts out, review only the project's ADRs.

Show each new ADR before writing it. If the project ends up with no ADRs and doesn't follow Lullabot's, there's nothing to review: say so and stop.

## 2. Get Lullabot's ADRs

Skip this if they aren't included. Use a temporary directory outside the project (`mktemp -d`) for anything you download, and delete it when you're done.

**Public site (default):** `https://architecture.lullabot.com/rss.xml` lists every published ADR with its title, link, context (`description`), tags (`category`) and date. Fetch each ADR's page from its link when you need its full text. Pages of deprecated ADRs say so and link to the ADR that replaces them; skip those.

**Git (faster, if you have access):** Lullabot staff can clone the source instead: `git clone --depth 1 git@github.com:Lullabot/architecture.git <tmp>`. If the clone fails, use the public site without asking. In a clone, read the front matter of each `adrs/*.md` file (`title`, `status`, `tags`, `context`) and keep only `status: accepted`.

Each Lullabot ADR's ID is the last part of its URL, which matches its file name without `.md` (e.g. `20260320-use-phpstan`), and its URL is `https://architecture.lullabot.com/adr/<ID>/`.

Mark the adoption ADR's exceptions **Overridden**, with its reason. List the Lullabot ADRs dated after the adoption ADR last changed (`git log -1 --format=%cs -- <adoption ADR>`) as **new since adoption**: check them like the rest, so the team can follow each one or add it to the exceptions.

## 3. Decide which ADRs apply

Detect the project's stack from cheap signals before reading ADRs in full:

- Drupal: `composer.json` requiring `drupal/core` or `drupal/core-recommended`; note the core version.
- PHP: `composer.json`, `*.php` files.
- Front end: `package.json`, themes (`web/themes/custom`), `*.ts`, `*.css`, `*.twig`.
- Local and CI: `.ddev/`, `.github/workflows/`, `.gitlab-ci.yml`, `.tugboat/`, `Taskfile.yml`, `renovate.json`.

Use each Lullabot ADR's title, tags and context to mark it **Not applicable** when it clearly doesn't fit the stack (e.g. a Gatsby ADR on a Drupal-only site), with a one-line reason. Don't fetch or read the full text of those. The project's own ADRs apply unless they say otherwise. ADRs about recording decisions themselves, such as "Record architecture decisions" or "Use Markdown Architecture Decision Records", are **Follows** when the ADR directory exists and its ADRs use the format they name.

## 4. Check each applicable ADR

For each remaining ADR, read its Decision section ("Decision Outcome" in MADR) and turn it into concrete checks: a file that should exist, a config value, a dependency, a code pattern to search for, or a sample of the relevant code. Gather evidence as `path:line`. When a project ADR and a Lullabot ADR cover the same thing, the project's wins: mark the Lullabot ADR **Overridden** by it.

For large codebases, check the ADRs in groups by tag (e.g. `drupal`, `php`, `front-end`, `ci`), using subagents if your tool supports them.

Give each ADR one verdict:

| Verdict              | Meaning                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Follows**          | The project does what the ADR says.                                                                                                 |
| **Partial**          | Some of the project does, some doesn't (e.g. one theme of two, or new code but not CI).                                             |
| **Deviates**         | The project does something else, or nothing.                                                                                       |
| **Overridden**       | A Lullabot ADR the project doesn't follow, documented by a project ADR or the adoption ADR's exceptions.                           |
| **Not applicable**   | The ADR doesn't fit this project's stack.                                                                                           |
| **Unable to verify** | The ADR is about something outside the code, such as hosting, process or the Drupal UI. Say what a person should check, and where. |

Rules:

- Every verdict needs evidence: a `path:line`, a command and its result, or the reason it doesn't apply. Don't guess. If you're not sure, say so and use **Unable to verify**.
- Cite paths, never quote secrets, credentials or values from `.env` or `settings.local.php` files.
- Existing code in an inherited codebase may predate an ADR. Note that in the deviation, but still report it.

## 5. Write the report

Write the report to the path from the arguments, or `docs/adr-review-YYYY-MM-DD.md`. Create the directory if needed. Give each ADR a stable ID: `lullabot:<ID>` for Lullabot's, `project:<file name without .md>` for the project's. Use this structure:

```markdown
# ADR review: <project name>

- Date: YYYY-MM-DD
- Project commit: <git rev-parse --short HEAD>
- Project ADRs: `<ADR directory>` (<n> accepted), adoption ADR: `<path>` (or none)
- Lullabot ADRs: Lullabot/architecture@<sha> (or architecture.lullabot.com, <date>, or not included)
- Results: <n> follow, <n> partial, <n> deviate, <n> overridden, <n> not applicable, <n> unable to verify

## Summary

| ID | ADR | Verdict | Evidence | Effort |
| --- | --- | --- | --- | --- |
| lullabot:20260320-use-phpstan | [Use PHPStan …](https://architecture.lullabot.com/adr/20260320-use-phpstan/) | Deviates | `composer.json` has no phpstan | M |

## New since adoption

<!-- Lullabot ADRs dated after the adoption ADR last changed. Leave out if none. -->

- lullabot:<ID>: <title>, <verdict>. Follow it, or add it to the adoption ADR's exceptions.

## Deviations

<!-- Partial and Deviates, ordered by impact, then effort (S/M/L). -->

### <ID>: <ADR title>

- **Verdict:** Deviates
- **The ADR requires:** <one or two sentences>
- **The project does:** <what you found, with `path:line`>
- **Impact:** <why it matters for this project>
- **Effort:** S | M | L

To resolve:

- [ ] <concrete step, naming files and commands>
- [ ] <next step>
- [ ] Or, if this deviation is deliberate, record why: add it to the adoption ADR's exceptions, or write a project ADR.

## Overridden

- <ID>: <title>, <reason>, see `<path to project ADR>`.

## Follows

- <ID>: <title>, `<evidence>`.

## Not applicable

- <ID>: <title>, <reason>.

## Unable to verify

- <ID>: <title>, <what a person should check, and where>.
```

Keep the IDs stable so a later review can be compared with this one, and issues can link back to it. If an earlier report exists in the same directory, add a short "Changes since <date>" section listing deviations that were resolved and new ones.

## 6. Summarize in the chat

Print the result counts, the top five deviations (ID, title, one line each), the Lullabot ADRs new since adoption, and the report's path. Ask the user to review the report before sharing it: the verdicts are a draft.

## 7. Help record decisions

If the project follows Lullabot's ADRs, offer to update the adoption ADR's exceptions from the review, showing the change before writing it. Draft them from **Not applicable** Lullabot ADRs with their reasons, each **Partial** or **Deviates** one the user confirms is deliberate, and each new-since-adoption ADR they decide not to follow. Ask the user for the reason behind each deliberate deviation; don't invent one. Deviations they want to fix stay out of the list. If there are no exceptions, keep the section and say "None."

Update the report's verdicts to match, e.g. deviations now listed as exceptions become **Overridden**.

When writing any ADR, here or in step 1:

- Follow the project's existing ADRs for file names (e.g. `0002-follow-lullabot-adrs.md` or `20261111-follow-lullabot-adrs.md`). In a new directory, use `0001-record-architecture-decisions.md` and `0002-follow-lullabot-adrs.md`.
- Follow their format too. The templates use Nygard's; rewrite them in the project's. For MADR, that's `* Status:` and `* Date:` bullets, "Context and Problem Statement", "Decision Outcome" holding the decision and exceptions, and "Positive Consequences" and "Negative Consequences". Fill in `Deciders` only with names the user gives you.
- Use today's date, and set the status to Proposed: the team accepts it, not you. A proposed adoption ADR still counts in step 1, so the review includes Lullabot's ADRs; note in the report that it's awaiting acceptance.

## 8. Offer a Google Doc

If you can write to Google Drive, offer to copy the report into a Google Doc for people who don't read Markdown in the repository. You can write to Drive if any of these is true:

- you have a Google Docs or Google Drive tool;
- the `gws` CLI is installed and `gws drive about get --params '{"fields": "user"}'` succeeds (see the `gws-cli` skill if it's available).

If neither is available, skip this step without mentioning it.

Ask before creating it, and say which account it goes to. Then:

- Upload the Markdown report and have Drive convert it: create the file with `"mimeType": "application/vnd.google-apps.document"` and the report as `text/markdown` media. With `gws`: `gws drive files create --json '{"name": "ADR review: <project> (YYYY-MM-DD)", "mimeType": "application/vnd.google-apps.document"}' --upload <report path>`. If your tool can only create a Doc from text, create it from the report's content and keep its headings, table and checklists.
- Leave it private to that account. Don't share it or move it into a shared folder unless the user asks.
- Check that the Doc opens and has the summary table, then give the user its link and add the link to the top of the Markdown report.

The Markdown report stays the source of truth. If the review is run again, create a new Doc rather than editing the old one.

## 9. Offer to file issues

Detect where the project tracks issues:

- **GitHub:** `git remote -v` points at github.com and `gh auth status` succeeds.
- **GitLab:** the remote points at a GitLab host and `glab auth status` succeeds.
- **Jira:** a Jira or Atlassian tool is available to you, or the project uses Jira keys (e.g. `ABC-123` in branch names, recent commit messages or docs). Ask the user for the project key if it isn't clear, and use that tool, or the `jira` or `acli` CLI if installed.

If none is found, say so and point to the report's checklists. Don't ask for one.

If one is found, first search it for existing issues about each **Partial** and **Deviates** finding, open or closed, by the ADR's ID (without the `lullabot:` or `project:` prefix) and its title (e.g. `gh issue list --state all --search "<ID> in:title,body"`, `glab issue list --all --search "<ID>"`, or the JQL `text ~ "<ID>"`). Add each match's link under its deviation in the report, and don't file a new issue for it. If a closed issue matches a deviation that's still there, mention it so the user can decide whether to reopen it.

Then offer to create issues for the remaining findings. Show the list of issue titles first, along with the existing issues you found, and ask whether to create one issue per deviation or a single tracking issue with every checklist. Create nothing without an explicit yes.

- Title: `ADR deviation: <ADR title>`
- Body: the deviation's section from the report, a link to the ADR (Lullabot's URL, or the project ADR's path; both contain the ID, so the next review finds the issue), and the report's path (and the Google Doc's link, if you created one). If the `issue-writing` skill is available, follow it for the body.

After creating them, add each issue's link under its deviation in the report.

## 10. Offer an AGENTS.md section

Offer to add a short section to the project's root `AGENTS.md`, so agents check new code and code reviews against the ADRs. Use `CLAUDE.md` if the project has no `AGENTS.md`. If the section already exists, offer to update it from this review instead. Show the section and ask before writing it.

The ADRs themselves stay the source of truth. List the Lullabot ADRs marked **Follows**, **Partial** or **Deviates** so agents don't have to fetch them all, and link to them rather than copying their text: the file loads into every session. Leave out the Lullabot part if they aren't included.

```markdown
## Architecture decisions

This project records its architecture decisions in `<ADR directory>`. When writing or reviewing code, check changes against its accepted ADRs, and flag any deviation from them.

The project also follows Lullabot's [ADRs](https://architecture.lullabot.com), except those listed in `<path to adoption ADR>`. These apply:

- [<ADR title>](https://architecture.lullabot.com/adr/<ID>/)

Last reviewed: YYYY-MM-DD (`<report path>`). Run the `adr-review` skill again to refresh this list.
```
