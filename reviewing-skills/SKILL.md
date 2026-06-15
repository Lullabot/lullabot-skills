---
name: reviewing-skills
description: Reviews a Claude Code skill against skill-authoring best practices and produces a prioritized, non-blocking report. Use when creating, editing, or reviewing a SKILL.md, a skill's meta.yml, or a skill directory, or when asked whether a skill follows best practices.
---

# Reviewing Skills

Review a skill against Anthropic's skill-authoring best practices and report what could be
improved. This is **advisory**: produce recommendations, never edit the skill unless the
user explicitly asks. Nothing here blocks a commit.

The rubric you score against lives at
[references/skill-best-practices.md](references/skill-best-practices.md) — a vendored,
version-pinned copy of the upstream guidance. Read it before reviewing.

## When to run this

- The user is creating or editing a `SKILL.md`, `meta.yml`, or a skill directory.
- The user asks "does this skill follow best practices?", "review my skill", or similar.
- Proactively, when you notice you're helping author a skill — offer a quick review.

Keep it lightweight and opt-in. Offer the review; don't force it, and don't gate the user's
work on it.

## Review workflow

1. **Identify the target skill directory** (the folder containing `SKILL.md`). If the user
   didn't name one, ask or infer from the file being edited.

2. **Run the deterministic checks** and capture the output:

   ```bash
   node scripts/review-skill.js <skill-dir>
   ```

   This reports the mechanical findings (body length, `name`/`description` rules,
   Windows-style paths, nested references, missing table-of-contents, rubric staleness). It
   is advisory and always exits 0. Fold its findings into your report rather than repeating
   the work by hand.

3. **Read the rubric**: [references/skill-best-practices.md](references/skill-best-practices.md).

4. **Assess the judgment calls** the script can't — these are where you add value:
   - Is the `description` genuinely specific, or just superficially detailed? Would a
     different skill trigger instead?
   - Is the body **concise**, or does it explain things Claude already knows?
   - Is the **degree of freedom** right (prose vs. exact commands) for how fragile the task
     is?
   - Is **progressive disclosure** used well — overview inline, detail in linked files?
   - Are **examples concrete** (input/output pairs) where output style matters?
   - Is **terminology consistent**? Any **time-sensitive** content that will rot?
   - For skills with scripts: do they solve rather than punt, avoid magic constants, declare
     dependencies, and make execute-vs-read intent clear?
   - Is the **naming** clear (gerund form preferred, but noun-phrase and action-oriented are
     fine)? Only flag a name that is vague or genuinely confusing.

5. **Emit the report** using the template below.

## Report template

Group findings by rubric area. Tag each as **Pass**, **Suggestion**, or **Issue**, and give
a one-line concrete fix. End with a short, prioritized list. Keep it scannable.

```
# Skill review: <skill-name>

## Frontmatter
- [Issue] description is first-person — rewrite in third person: "Generates …".
- [Pass] name is valid and matches the directory.

## Conciseness & structure
- [Suggestion] SKILL.md body is 540 lines — move the API table into reference/api.md.

## Progressive disclosure
- [Pass] Detail files are linked one level deep from SKILL.md.

## Content & examples
- [Suggestion] The commit-message section would benefit from input/output example pairs.

## Scripts (if any)
- [Issue] scripts/run.py uses TIMEOUT = 47 with no rationale — document or derive it.

## Top recommendations
1. Rewrite the description in third person with explicit triggers.
2. Split the SKILL.md body below 500 lines.
3. Add two concrete examples to the commit-message section.
```

If there are no findings, say so plainly and note anything the skill does well.

## Refresh mode

The vendored rubric carries a `last_synced:` date. When it's stale (the deterministic check
flags it after 30 days), or when the user asks to update the best practices:

1. `WebFetch` the canonical URL recorded at the top of
   [references/skill-best-practices.md](references/skill-best-practices.md).
2. Compare the fetched guidance against the vendored rubric and the checks in
   `scripts/review-skill.js`.
3. Propose edits to the rubric (and, if a *mechanical* rule changed, to `review-skill.js`)
   for the user to approve.
4. Update the `last_synced:` date in the rubric header.

Don't refresh silently — show the diff and let the user accept it.

## Boundaries

- **Advisory only.** Do not edit the reviewed skill unless the user asks you to apply a fix.
- This skill complements, and never replaces, the blocking structural gate in
  `scripts/validate-skills.js`.
