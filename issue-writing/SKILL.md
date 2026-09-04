---
name: issue-writing
description: Draft concise, verified issues, tickets, and bug reports that maintainers can triage and discuss. Use when filing a GitHub issue or Jira ticket, reporting a bug, writing a feature request or task, filling in an ISSUE_TEMPLATE, filing a Drupal.org issue, or grooming vague tickets in a backlog. Covers titles, descriptions, acceptance criteria, reproduction steps, and labeling.
---

# Writing Issues

An issue is a compact request and decision record for someone else, often someone who joins the project months from now. It has to survive without you in the room. State the problem, define the desired outcome, and include enough verified context to triage it and begin the right discussion. Make unresolved questions explicit instead of guessing.

## Own the submission

You are responsible for every issue you submit. Treat AI-generated text as a draft, not as evidence or a substitute for understanding. Verify every factual claim, rewrite the issue in your own words, and make sure you can explain each proposed decision. Never excuse an error or unsupported choice by saying that AI wrote it.

When assisting someone who will submit under their name, present a draft for their review unless they explicitly asked you to file it. Surface unresolved facts and decisions; do not hide them behind polished language.

## Before you file

1. **Read the contribution rules.** Check `CONTRIBUTING`, the repository's AI-use policy, and its security-reporting process before drafting.
2. **Search first.** Open and closed issues, both. Drupal's [issue etiquette](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette) puts this first for a reason: adding to an existing issue beats splitting the discussion across two. Link related issues either way.
3. **Confirm it's current.** Reproduce on the latest release or the current development branch before reporting. Fixed-in-dev is a common outcome.
4. **Use the repo's template.** If `.github/ISSUE_TEMPLATE/` exists, pick the right one and complete every applicable required field. Use `TBD` or explain what is unknown when the project allows it; never invent an answer to complete the form.
5. **One issue per issue.** Two unrelated problems in one ticket means one of them gets forgotten when the other is fixed.

## Titles

Write the title as the action to take, so it completes the sentence "This ticket will…" ([Guidelines for Writing Proper Tickets and Commits](https://www.lullabot.com/articles/guidelines-for-writing-proper-tickets-and-commits)).

| Type | Pattern | Good | Weak |
| --- | --- | --- | --- |
| Task | Verb the noun | `Build location content type` | `Location stuff` |
| Bug | What breaks, where, under what conditions | `Links in related documents do not trigger a download` | `Navigation is wonky` |
| Drupal.org | Plain descriptive statement of the problem | `Views UI preview fails when a contextual filter has no default` | `Views broken` |

- Enough context to triage from the list view, without opening it.
- One prefix at most for grouping (`Blog: Build post content type`). Lullabot's [Art of Jira](https://www.lullabot.com/articles/art-jira-ticketing-best-practices-and-issue-schema) calls out `[Blog] [Content Type] [Build] Blog post content type` as the failure mode: over-tagged titles stop being scannable.
- No severity theater. "URGENT!!!" belongs in the priority field.

## Description structure

The Art of Jira framework, which travels well to GitHub:

```markdown
## Problem

<The observed behavior and why it matters, in one or two sentences.>

## Desired outcome

<The observable result, without prescribing implementation unnecessarily.>

## Request

<Optional. Include only when investigated or discussed. Explain the reasoning,
constraints, and important tradeoffs. Mark unresolved decisions clearly.>

## Acceptance criteria

- [ ] <Observable condition someone else can check.>
- [ ] <Another.>

## Resources

<Links to designs, docs, related issues. Minimize hops; screenshot the thing
rather than linking to a doc that links to a doc.>
```

For bugs, replace Request with:

```markdown
## Steps to reproduce

1. <Start from a clean state. Include the obvious steps.>
2. <Action.>

**Expected:** <what should happen>
**Actual:** <what happens instead>

## Environment

<Site/environment, URL, version, browser and OS, user role, date and time
if it's intermittent.>
```

Attach the evidence: screenshot, screen recording, error message, relevant log extract. To embed an image programmatically, use the `github-attachments` skill — it uploads the file and gives you the markdown to paste into the body. Apache's [bug writing guide](https://infra.apache.org/bug-writing-guide.html) reduces a useful report to two properties, reproducible and specific. Everything above serves one of those two.

Separate observed facts, inferences, proposals, and unresolved questions. Verify package, API, version, configuration, and dependency claims against authoritative project sources. If proposing a dependency, confirm that it exists, is maintained, and fits the project. Consider security and privacy implications before recommending an approach. Never present generated or inferred details as observations.

Keep the register plain throughout. Write for the maintainer's first read: include only what helps them understand, reproduce, triage, or decide the issue. Avoid scene-setting about why the area matters, paragraphs that restate the title, speculative implementation detail, and adjectives standing in for evidence. "Significantly degraded user experience" tells a developer nothing; "the submit button is unreachable by keyboard" tells them where to start.

When lengthy material is genuinely useful, summarize its relevant conclusion in the issue and attach the full logs, generated analysis, or other artifact. Sanitize attachments for secrets and personal or customer data. Do not paste a full AI response into the issue merely because it is available.

## Acceptance criteria

This is the part most often missing and the part that decides whether the issue can be closed.

- Write conditions someone other than the author can verify. "Menu works correctly" is not a criterion. "Sub-menu items are reachable by keyboard and announce their expanded state" is.
- Cover non-obvious dimensions that the request actually implies or the stakeholders confirmed: responsive behavior, accessibility, permissions and roles, empty and error states, migration of existing content. Do not silently expand scope.
- Say what's out of scope when a reader could reasonably assume it's included.
- No time estimates. Estimating belongs to whoever does the work, not to whoever writes the ticket.

## Issue types

From the [Art of Jira](https://www.lullabot.com/articles/art-jira-ticketing-best-practices-and-issue-schema) schema. The names differ across trackers; the distinctions hold.

- **Epic** — a body of work that groups related issues. A chapter, not a task. Done when its children are done.
- **Story** — user-facing value, phrased from the user's side.
- **Task** — necessary work with no direct user-visible outcome. Build pipelines, refactors, content model changes.
- **Bug** — existing behavior is wrong. Requires reproduction steps, and gets triaged by severity.

Note that issue type and any billing or contract classification are separate axes. On maintenance retainers where work is split into buckets, a Bug can fall in either one depending on how it arrived. Apply both, and don't let the type drive the classification.

## Labels and fields

- **Label at creation.** A label added later is a label nobody filtered on.
- **Keep the taxonomy small.** [Project Management with GitHub](https://www.lullabot.com/articles/project-management-with-github-v2) warns that too many labels become useless: teams abandon label hygiene once the system is overwhelming or duplicative.
- **Check the repo's actual labels** before applying (`gh label list --repo OWNER/REPO`). Names and casing vary, and inventing a near-duplicate is worse than leaving it unlabeled.
- Some repos use GitHub's native **issue types** or **issue fields** rather than labels for Bug/Feature/Task and Priority. These are GraphQL-only and won't appear in `gh issue view --json`. Check which system a repo uses before reaching for `--add-label`.
- An issue with no project or milestone sits in the backlog and is not ready for work. That's a valid state; just don't mistake it for scheduled.

## Drupal.org issues

Drupal puts the weight in the **issue summary**, which is the canonical record for the whole issue and is expected to stay current as the work evolves. The [template](https://www.drupal.org/docs/develop/issues/fields-and-other-parts-of-an-issue/issue-summary-field) sections:

- **Problem/Motivation** — why the issue exists, with reproduction steps.
- **Steps to reproduce** — exact versions, paths, and actions.
- **Proposed resolution** — the solution and the reasoning, plus workarounds for people who can't apply the patch.
- **Remaining tasks** — reviews needed, tests to write, docs to write.
- **User interface changes** — new or changed features, added or removed modules, changed URLs or interface text.
- **API changes** — anything affecting module, profile, or theme developers.
- **Data model changes** — database or config changes that break existing sites.
- **Release notes snippet** — for major and critical issues.

Also: file in the correct project and component, set version to the current development branch, mark unknown sections `TBD` rather than deleting them, and update the summary as consensus shifts. Maintainers set issues to "Needs work" when the summary goes stale. Never file a security vulnerability in the public queue; use the [security team's process](https://www.drupal.org/drupal-security-team/security-team-procedures/how-to-report-a-security-issue).

## Open source issues

- **Show your work.** [opensource.guide](https://opensource.guide/how-to-contribute/) puts it as: it's fine not to know things, but show that you tried. "I'm not sure how to implement X, I checked the docs and didn't find a mention" gets help. "How do I X?" often doesn't.
- **Context beats urgency.** "X doesn't happen when I do Y" is actionable. "X is broken! Please fix it" is not.
- **Keep it short.** Maintainers are volunteers with more requests than time.
- **Agree before large feature work.** Reach agreement on the problem and approach before writing substantial code.
- **Skip the editorializing.** Apache's guide names this directly: commentary on how the software got shipped this way costs you the reader you were trying to recruit.

## Anti-patterns

- **A title that names a feeling instead of a behavior.** "Navigation is wonky."
- **A bug report with no reproduction path.** If a developer can't see it, it gets closed as "cannot reproduce" and you file it again in three months.
- **Requirements that live only in comments.** Decisions reached in a thread belong in the description. Comments are where reasoning happens; the description is what people read.
- **Rewriting an in-progress ticket.** A substantial requirements change is a new ticket, not an edit to one that's already being worked.
- **Screenshots of text.** Paste the error, so it's searchable.
- **Padding.** A preamble about the importance of the area, or a closing line summarizing what the reader just read. Both cost triage time and add nothing.
- **Copying a client's words verbatim without translating them.** "It's broken" needs to become a described behavior before it's fileable.
- **Submitting generated prose verbatim.** A polished draft can still contain false claims, excess detail, or decisions the submitter does not understand.
- **Unverified implementation advice.** Do not propose a package, API, refactor, or security-sensitive approach because generated text made it sound plausible.

## Before you submit

- Title starts with a verb, or names the broken behavior, and reads clearly in a list.
- Someone unfamiliar with the conversation could act on it.
- Acceptance criteria are observable and checkable.
- Bugs carry steps, expected, actual, environment, and evidence.
- Type, labels, and priority set per this repo's conventions.
- Related issues linked, duplicates searched.
- I rewrote the draft in my own words and can explain every claim, criterion, and proposed decision.
- Observations, inferences, proposals, and unresolved questions are clearly distinguished.
- Dependencies, versions, APIs, and security implications mentioned here were verified.
- No credentials, personal data, or customer records in the body or the screenshots.
- In a client repo: no other client named anywhere in the issue.
- Every sentence helps the maintainer understand, reproduce, triage, or decide the issue.
- Supporting detail is attached only when it materially helps.
- Read the final draft yourself. Remove anything you have not verified and confirm that you can defend what remains.

## Sources

`references/sources.md` collects the guides behind this skill, with what each contributes.
