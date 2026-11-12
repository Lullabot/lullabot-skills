# Filing issues

Step 9 of the `adr-review` skill: search the issue tracker it found, then publish the report and its deviations as issues the user approves.

## Search for existing issues

Search the tracker for existing issues about each **Partial** and **Deviates** finding, open or closed, by the ADR's ID (without the `lullabot:` or `project:` prefix) and its title (e.g. `gh issue list --state all --search "<ID> in:title,body"`, `glab issue list --all --search "<ID>"`, or the JQL `text ~ "<ID>"`). Add each match's link under its deviation in the report, and don't file a new issue for it. If a closed issue matches a deviation that's still there, mention it so the user can decide whether to reopen it.

For open issues an earlier review filed (their body starts with `<!-- adr-review:<ID> -->`), offer one short comment each: "Still deviates as of YYYY-MM-DD" or "Looks resolved in the YYYY-MM-DD review", with the evidence. Don't edit their bodies or close them. Issues without the marker are only linked in the report.

Also search for a report issue from an earlier review by its title, `ADR review: <project name>` (e.g. `gh issue list --state all --search "ADR review in:title"`), and confirm its body starts with `<!-- adr-review -->`. Search may not index that marker, and some trackers, such as Jira, may strip it, so match on the title there. Update an open one; if only a closed one exists, link to it from the new issue.

## Ask, then file

Ask which to file, showing the issue titles and the existing issues you found: one issue with the full report (recommend this by default: one place to track the review), one issue per remaining deviation, or both. Create or change nothing without an explicit yes.

Start every issue body and comment you write, after its `<!-- adr-review… -->` marker if it has one, with the AI disclosure note from the report template (step 5). The marker stays first so the next review finds the issue. Only GitHub and GitLab render the `> [!NOTE]` alert; on other trackers, such as Jira, use their own callout (e.g. a Jira info panel) or a plain sentence.

**The report as an issue:**

- Title: `ADR review: <project name>`. Body: the report, starting with `<!-- adr-review -->` so the next review finds it, with each deviation's issue linked if you filed them.
- If an open report issue exists, offer to update it instead of creating another. Replace its body with the new report, keeping ticked checkboxes for steps that are still in it, and add a comment with the "Changes since" summary so watchers are notified. Show the new body and the comment before posting. The tracker keeps the old body in its history.

**One issue per deviation:**

- Title: `ADR deviation: <ADR title>`
- Body: `<!-- adr-review:<ID> -->`, then the deviation's section from the report, a link to the ADR (Lullabot's URL, or the project ADR's path; both contain the ID, so the next review finds the issue), and the report's path (and the Google Doc's link, if you created one). If the `issue-writing` skill is available, follow it for the body.

After creating or updating them, add each issue's link to the report (under its deviation, or at the top for the report issue).
