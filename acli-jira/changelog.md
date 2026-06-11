# Changelog — acli-jira skill

Notable changes to the **Atlassian CLI (acli) for Jira** skill. Reviewed against
Anthropic's [Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

## 2026-06-11 — Best-practices review pass

A structural and content review of the initial skill. No commands were removed;
existing examples still work. Highlights for the team:

### Fixed
- **Added the missing `meta.yml`.** The skill was failing the repo's
  `scripts/validate-skills.js` check and would not have rendered on the
  prompt-library site. Set `discipline: project-management` with Jira tags.
- **Moved `version` out of `SKILL.md` frontmatter** so it only declares `name`
  and `description`, matching the convention used by the other skills in this repo.

### Added
- **Prerequisites section.** The skill now states up front that `acli` must be
  installed and authenticated (`acli jira auth login`) and how to check
  `acli jira auth status`. Previously it assumed a configured environment —
  the official guidance explicitly warns against assuming tools are installed.
- **Guidance on discovering valid transitions.** Jira statuses and transitions
  are defined per-project, so the skill now tells Claude to inspect the work
  item's current status and run `transition --list` *before* transitioning,
  instead of guessing `"Done"` / `"In Progress"` (which may not exist in a given
  project's workflow).
- **"Bulk and Destructive Operations" section.** Adds a preview-the-scope-first
  workflow for any `--yes` / `--jql` bulk edit, transition, or delete, and
  recommends `archive` (reversible) over `delete` (permanent) where appropriate.
- **Table of contents in `references/commands.md`.** The reference file is ~400
  lines; a contents list lets Claude see the full scope even when previewing the
  file with a partial read.

### Changed
- **Consistent terminology.** Normalized "issue" → "work item" throughout the body
  to match the `acli jira workitem ...` command name, with a one-line note that
  Jira calls these "issues." (Trigger phrases in the `description` still mention
  "issue" so the skill activates on natural phrasing.)

### Notes / not changed
- **Skill name (`acli-jira`) kept as-is.** Best practices prefer gerund names
  (e.g., `managing-jira-issues`) but accept noun phrases; mirroring the CLI name
  aids discovery.
- **`--label` vs `--labels` discrepancy** between `create` and `edit` is left
  unchanged pending verification against the real CLI — confirm with
  `acli jira workitem create --help` / `edit --help` before "fixing" either.
- **Description triggering not yet optimized.** Running the `skill-creator`
  description optimizer is a possible future step to tune activation accuracy.
