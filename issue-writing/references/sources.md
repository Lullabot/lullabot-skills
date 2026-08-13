# Sources

Guides behind the `issue-writing` skill, and what each contributes.

## Lullabot

- [The Art of Jira: Ticketing Best Practices and the Issue Schema](https://www.lullabot.com/articles/art-jira-ticketing-best-practices-and-issue-schema) — the Overview / Request / Acceptance Criteria / Resources / Steps to Reproduce description framework. Titles start with action verbs; bugs name who, what, where, and how. The Epic / Story / Task / Bug schema. Warns against over-tagged titles (`[Blog] [Content Type] [Build] Blog post content type`), against descriptions with no acceptance criteria, and against moving substantial requirements changes into a ticket already in progress. Decisions reached in comments get added back to the description.
- [Guidelines for Writing Proper Tickets and Commits](https://www.lullabot.com/articles/guidelines-for-writing-proper-tickets-and-commits) — ticket titles describe the action to fulfill and complete the phrase "This ticket will…". `Prevent Nav Bar From Bouncing on Scroll`, not `Navigation is Wonky`. Bug descriptions carry steps to reproduce, environment details, and the desired result; task descriptions reference design comps and eliminate assumptions about the goal.
- [Project Management with GitHub: v2](https://www.lullabot.com/articles/project-management-with-github-v2) — issues are the unit of both describing and discussing work. Label taxonomy (Epic, epic name, phase, bug, blocked, front-end) with the warning that too many labels become useless and teams stop maintaining them. Milestones group by release; issues with no project assignment sit in the backlog and are not ready for work.
- [Managing Projects with GitHub](https://www.lullabot.com/articles/managing-projects-with-github) — the earlier version, useful for the workflow-board conventions.

## Drupal

- [Issue summary field](https://www.drupal.org/docs/develop/issues/fields-and-other-parts-of-an-issue/issue-summary-field) — the canonical template: Problem/Motivation, Steps to reproduce, Proposed resolution, Remaining tasks, User interface changes, Introduced terminology, API changes, Data model changes, Release notes snippet. The summary is the key source of information for developers, reviewers, and users, and must stay complete, accurate, and current; maintainers set issues to "Needs work" when it goes stale. Unknown sections are marked TBD rather than removed.
- [Issue etiquette](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette) — search open and closed issues first and add to an existing one rather than filing a duplicate. Verify against the latest stable and the development version. Descriptive human-readable titles. File in the correct project and component. Never report security vulnerabilities through the public queue. Report back when something works, for the next person.
- [Issue scope guidelines for core issues](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/core-scope) — how scope creep is handled once an issue is open.

## Open source and industry

- [opensource.guide: How to Contribute](https://opensource.guide/how-to-contribute/) — do your homework and show that you did. Give context ("X doesn't happen when I do Y") rather than urgency ("X is broken! Please fix it"). Keep requests short, since projects get more requests than they have help for. Keep communication public, assume good intent, and remember maintainers are usually volunteers.
- [Apache Infrastructure: Writing a good bug report](https://infra.apache.org/bug-writing-guide.html) — a useful report is reproducible and specific. Four components: what you intended, what you did, what you expected, what happened instead. Titles identify the problem and its context (`PCMCIA install fails on Tosh Tecra 780DVD w/ 3c589`, not `Install problem`). One issue per report. No editorializing about the software or its authors. Sensitive details go through a private channel.
- [GitHub Docs: Configuring issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository) — templates and issue forms live in `.github/ISSUE_TEMPLATE/`. Forms use a YAML schema with typed fields (text, dropdown, checkbox, file upload) and enforce structure better than markdown templates. `config.yml` controls `blank_issues_enabled` and `contact_links`; numeric filename prefixes control chooser order.
- [BrowserStack: How to write an effective bug report](https://www.browserstack.com/guide/how-to-write-a-bug-report) — the standard evidence checklist: description, steps, expected, actual, screenshots or video, software version, OS and browser.

## Where these disagree

- **Where the requirements live.** Jira and GitHub practice puts them in the issue description and treats comments as conversation. Drupal.org puts them in the issue summary and expects it to be rewritten as consensus changes, so the summary is a living document rather than an original statement of intent.
- **How much process to impose.** Structured issue forms raise report quality and lower the number of reports filed. Open source projects with few maintainers usually want the structure; internal team backlogs often move faster with a lighter template. Match the repo.
