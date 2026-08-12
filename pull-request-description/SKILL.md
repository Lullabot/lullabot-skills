---
name: pull-request-description
description: Write or improve a pull request or merge request description so a reviewer can act on it without reconstructing your reasoning from the diff. Use when opening a PR/MR, when asked to draft or rewrite a PR description or title, when filling in a PULL_REQUEST_TEMPLATE, or when a reviewer says a PR lacks context. Covers client-repo PRs, Drupal.org merge requests, and open source contributions.
---

# Pull Request Descriptions

A reviewer opening your PR has the diff. What they don't have is why the change exists, what you decided along the way, and how to confirm it works. Supplying those three things is the entire job.

## Answer three questions

Every description, however short, answers:

1. **Why** — the problem, and the link to the ticket or issue.
2. **What** — what changed, in reviewer-facing terms rather than a file listing.
3. **How to verify** — the steps someone else follows to see it working.

Lullabot's [A Quick Guide for Code Reviews](https://www.lullabot.com/articles/a-quick-guide-for-code-reviews) frames a pull request as the atomic unit that carries those three. [The Peer Review How-To Guide](https://www.lullabot.com/articles/the-peer-review-howto-guide) adds the reason to bother: the easier you make it for the reviewer, the faster it merges.

## Workflow

1. **Read the actual change.** `git diff <base>...HEAD --stat`, then the diff itself. Describe what the code does now, not what the ticket asked for. Those drift apart.
2. **Find the ticket.** Pull the issue number from the branch name, the commits, or ask. Every title and description links back to it.
3. **Check for a template.** If `.github/PULL_REQUEST_TEMPLATE.md` (or `.gitlab/merge_request_templates/`) exists, fill that structure instead of imposing your own. Never delete a template's sections to make room for prose.
4. **Match the house style.** Skim two or three recently merged PRs in the repo. A repo with terse three-line descriptions does not want an essay.
5. **Draft, then cut.** Aim for roughly 200 to 400 words in the body. Longer descriptions get skimmed, which defeats the point.
6. **Self-review the diff as if you were the reviewer.** Leave inline comments on anything surprising: a workaround, a decision that looks wrong without context, a deliberately out-of-scope chunk.

## Template

Adapt freely. The headings matter less than the questions being answered.

```markdown
## Why

<Problem in one or two sentences.> Closes #123.

## What changed

- <Change a reviewer needs to know about, in behavior terms.>
- <Another one.>
- Out of scope: <anything deliberately left alone, with the follow-up ticket.>

## How to verify

1. <Setup: branch, environment, URL, test user.>
2. <Action.>
3. Expected: <observable result.>

## Notes for the reviewer

<Approaches ruled out, known limitations, where you want the closest attention.>
```

Drop sections that would be empty. A one-line CSS fix needs Why and How to verify, and nothing else.

## Titles

The title is the part that shows up in changelogs, release notes, and six months of `git log`. Write it as an action.

| Context | Format | Example |
| --- | --- | --- |
| Client / internal repo | `[TICKET-ID] Imperative description` | `[PROJ-1234] Prevent nav bar from bouncing on scroll` |
| Drupal.org merge request | `Issue #NNNNNNN: Brief description` | `Issue #3467675: Make URL field required by default` |
| Open source, no tracker | Imperative summary | `Cache the taxonomy term lookup in the menu builder` |

Rules that hold everywhere:

- Start with a verb, in the imperative. "Delete the RPC", not "Deleting the RPC" and not "Deleted the RPC."
- Be specific enough to stand alone. Google's [CL description guidance](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) names the failures: "Fix bug", "Fix build", "Phase 1", "Moving code from A to B."
- Describe the change, not the symptom. "Prevent nav bar from bouncing on scroll" beats "Navigation is wonky."
- Prefix `[WIP]` or open as a draft when it isn't ready for review, and say what feedback you want.

Branch names follow the Lullabot ADR [`[ticket-id]--[short-description]`](https://architecture.lullabot.com/adr/20220920-git-branch-naming/) — double dash, no forward slashes. When no ticket exists the ADR substitutes a prefix in the ticket-id slot, keeping the separator: `NOTICKET--fix-jumping-nav`, `0--fix-jumping-nav`, or `HOTFIX--remove-has-krumo` for urgent fixes.

## Scope

Description quality is downstream of PR scope. A PR that does three unrelated things cannot be described well.

- **One change type per PR.** Drupal's [merge request guidelines](https://www.drupal.org/docs/develop/git/using-git-to-contribute-to-drupal/merge-request-guidelines) put bug fixes, performance work, and code style fixes in separate merge requests. The same discipline helps in client repos.
- **Split, don't apologize.** If the description needs "also, unrelated:", that's a second PR.
- **Keep main deployable.** Lullabot's [main-branch ADR](https://architecture.lullabot.com/adr/20251125-main-deployable/) rules out long-lived integration branches, so each PR merges on its own merit and its description has to stand on its own.
- **Follow-ups over stalling.** When review discussion outgrows the change, file a follow-up ticket, link it in the description, and merge.

## Drupal.org contributions

Drupal.org inverts the usual weighting: the **issue summary** is the canonical record, not the merge request body.

- Keep the [issue summary](https://www.drupal.org/docs/develop/issues/fields-and-other-parts-of-an-issue/issue-summary-field) current: problem, proposed resolution, remaining tasks, user interface changes, API changes. Reviewers and committers read this first.
- Record **approaches tried and ruled out**, with the reasoning. This is the section other contributors most often need and most often lack.
- The MR description defaults to `Closes #issue_number`. Expand it with the problem summary, the key changes, and any known limitations or follow-up work, per [Creating merge requests](https://www.drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/creating-merge-requests).
- Note automated test coverage explicitly. Merge requests with tests are likelier to be accepted.

## Open source contributions

- Read `CONTRIBUTING.md` before writing anything. It outranks this skill.
- Assume the reader has no history with your work. GitHub's [how to write the perfect pull request](https://github.blog/developer-skills/github/how-to-write-the-perfect-pull-request/) makes the point that anyone might read this, at any point in the future.
- Say what kind of feedback you want: architecture, correctness, wording, or a sanity check on an approach before you go further.
- Link the issue you're fixing and confirm a maintainer wanted it fixed. Unsolicited large PRs get closed.
- Screenshots or a short recording for anything visual. Before and after, in the same viewport.

## Anti-patterns

- **A file-by-file narration of the diff.** The reviewer has the diff. Tell them what it means.
- **A description written from the ticket rather than the code.** They diverge, and the reviewer trusts the description.
- **"See ticket."** The ticket describes the problem. Only the PR describes the solution.
- **Silent scope expansion.** An unmentioned refactor buried in a bug fix is the fastest way to lose a reviewer's trust.
- **A checked template with empty answers.** "Tested: yes" tells a reviewer nothing they can repeat.
- **Fifteen-checkbox templates.** They get rubber-stamped. Keep repo templates short enough that people fill them in honestly.

## Before you post

- Title starts with a verb and carries the ticket reference.
- Ticket linked with a closing keyword (`Closes #123`) where the tracker supports it.
- Verification steps are numbered and specific enough for someone else's machine.
- Anything out of scope is named, with a follow-up link.
- Screenshots for visual changes.
- No credentials, internal URLs, or customer data in the body or screenshots.
- In a client repo: no other client's name anywhere in the description, commits, or screenshots.
- No invented time estimates. Describe the work, not how long you imagine review will take.
- Run the `humanizer` skill over the text if it will be read by a client. Then grep for `—` and `–`; a hit means the pass isn't finished.

## Sources

`references/sources.md` collects the guides this skill draws on, with what each one contributes.
