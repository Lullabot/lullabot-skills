# Sources

Guides behind the `pull-request-description` skill, and what each contributes.

## Lullabot

- [A Quick Guide for Code Reviews](https://www.lullabot.com/articles/a-quick-guide-for-code-reviews) — a pull request is the atomic unit describing why the change was made, what changed, and how to verify it worked. Also the reviewer checklist a good description anticipates: correct system layer, security (SQL injection, XSS, CSRF, access control), API-first reusability, docs and tests alongside the code.
- [The Peer Review How-To Guide](https://www.lullabot.com/articles/the-peer-review-howto-guide) — put testing instructions at the top of the PR. The author's prep list: code is clear and meets standards, comments are adequate, commit messages match the changes, testing guidance is present. Long review discussions become follow-up tickets rather than blocking the merge.
- [Guidelines for Writing Proper Tickets and Commits](https://www.lullabot.com/articles/guidelines-for-writing-proper-tickets-and-commits) — action-oriented titles prefixed with the issue ID (`[PROJ-1234] Prevent Nav Bar From Bouncing on Scroll`, not `Navbar Issues`). Commits prefixed with the issue ID; if one sentence can't describe a commit, split it. **Caveat:** its branch format (`owner/issue-id/short-description`) predates and is superseded by the branch-naming ADR below.
- [ADR: Branch naming convention](https://architecture.lullabot.com/adr/20220920-git-branch-naming/) — `[ticket-id]--[short-description]`. No forward slashes; they break prefix-sharing branch operations. With no ticket, the ADR substitutes `NOTICKET`, `0`, or `HOTFIX` into the ticket-id slot and keeps the separator: `NOTICKET--fix-jumping-nav`, `0--fix-jumping-nav`, `HOTFIX--remove-has-krumo`.
- [ADR: Main branch always deployable](https://architecture.lullabot.com/adr/20251125-main-deployable/) — no long-lived dev or sprint branches, so every PR has to stand on its own.
- [How Automated Code Review Tools Reduce Pull Request Bottlenecks](https://www.lullabot.com/articles/how-automated-code-review-tools-reduce-pull-request-bottlenecks) — context on automated review passes running alongside human review.

## Drupal

- [Creating merge requests](https://www.drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/creating-merge-requests) — title format `Issue #3467675: Make URL field required by default`. The default body is only `Closes #issue_number`; expand it with the problem summary, key changes, and known limitations or follow-up work.
- [Merge request guidelines](https://www.drupal.org/docs/develop/git/using-git-to-contribute-to-drupal/merge-request-guidelines) — one change type per issue and merge request. Follow coding standards, run checks locally, target the current development version. Merge requests with automated tests are likelier to be accepted.
- [Issue summary field](https://www.drupal.org/docs/develop/issues/fields-and-other-parts-of-an-issue/issue-summary-field) — the canonical record for a Drupal issue: problem, proposed resolution, approaches tried and ruled out with pros and cons, links to relevant API docs, known workarounds, and a link to the current merge request.
- [Issue etiquette](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette) and [Issue scope guidelines for core](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/core-scope) — how scope creep is handled in core issues.

## Open source and industry

- [GitHub: How to write the perfect pull request](https://github.blog/developer-skills/github/how-to-write-the-perfect-pull-request/) — open with the purpose ("This is a spike to explore…", "This fixes handling of…"). Provide context without assuming shared history. Say what kind of feedback you want. Prefix `[WIP]`. Assume anyone might read it later.
- [Google eng-practices: Writing good CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) — first line is a complete sentence in the imperative, then a blank line, then context: why this approach, what its shortcomings are, links to bugs and benchmarks. Named bad first lines: "Fix bug", "Fix build", "Phase 1", "Moving code from A to B."
- [Graphite: GitHub PR description best practices](https://graphite.com/guides/github-pr-description-best-practices) — 200 to 400 words. Keep `PULL_REQUEST_TEMPLATE.md` short; a fifteen-checkbox template gets ignored or rubber-stamped.
- [freeCodeCamp: How to write a good pull request description](https://www.freecodecamp.org/news/how-to-write-a-pull-request-description/) — the what, why, how framing for contributors new to the practice.

## Where these disagree

- **Title format.** Lullabot uses `[TICKET-ID] Description`, Drupal.org uses `Issue #NNNNNNN: Description`, and many open source projects use a bare imperative or Conventional Commits. Match the repo you're in.
- **Where the reasoning lives.** Drupal.org keeps it in the issue summary and treats the merge request body as secondary. GitHub-centric guidance puts it in the PR body. Follow the tracker's convention, and don't split the reasoning across both.
