# Agent Instructions

Conventions for any AI agent (Claude Code, Cursor, Copilot Chat, etc.) editing this repository.

## What this repo is

A bundle of Claude Code skills published to two surfaces:

1. **Direct install:** `git clone https://github.com/Lullabot/lullabot-skills.git .claude/skills` — every skill in this repo immediately becomes available in Claude Code.
2. **Public site:** [Lullabot/prompt_library](https://github.com/Lullabot/prompt_library) consumes this repo as a git submodule and renders each skill as a browsable page at `https://lullabot.github.io/prompt_library/`. Pushes to `main` here trigger an automatic submodule bump there via `repository_dispatch`.

Edits ship to both surfaces as soon as they hit `main`. Treat every commit as a release.

## Skill structure

Each skill folder must contain:

- `SKILL.md` — the Claude Code skill definition. Frontmatter must declare `name` and `description`. Both fields must be on a single line each (multi-line YAML breaks the prompt-library generator).
- `meta.yml` — prompt-library metadata: `title`, `discipline` (one of `development`, `content-strategy`, `design`, `project-management`, `quality-assurance`, `sales-marketing`), `date`, optional `tags`, optional manual `version` / `lastUpdated` / `changelog`.

Companion files (`scripts/`, `references/`, `assets/`, etc.) live alongside `SKILL.md` and are copied to the public site verbatim.

## Required workflow when committing

**Before writing your commit message, run:**

```bash
scripts/propose-changelog.sh
```

This analyzes your staged changes and uses GitHub Models (via `gh models run`) to suggest a `User-Facing-Change:` trailer line per modified skill. Paste the suggestion into the commit message body, edit as needed, or skip entirely for purely internal/cosmetic changes.

**Why:** The prompt-library site auto-builds a per-skill changelog from these trailers (see [its CLAUDE.md](https://github.com/Lullabot/prompt_library/blob/main/CLAUDE.md) for parser details). No trailer = no public changelog entry — which is the right outcome for hygiene commits, but the wrong outcome for substantive changes that users should see in the change history.

**Examples:**

Single-skill commit:
```
Add gollum link reference

User-Facing-Change: Added gollum link syntax reference for handling broken wiki links
```

Multi-skill commit (always scope the trailers):
```
Sync skills from local

User-Facing-Change[github-wiki]: Added gollum link reference
User-Facing-Change[gws-cli]: Reformatted description for clarity
```

Hygiene commit (no trailer):
```
Fix typo in pencil-designer SKILL.md
```

## When to skip the trailer

- Typo fixes
- Formatting / em-dash normalization
- Internal refactors with no observable change
- Dependency bumps with no behavior change
- Documentation tweaks that don't add information

When in doubt, run the helper script — its prompt is calibrated to recognize these cases and respond `SKIP`.

## When the trailer is mandatory

- Adding or removing a skill
- New behavior in a skill (e.g., new commands, new triggers, new output format)
- New companion files (scripts, references) that users will see / use
- Fixed bugs that change observable output
- Renamed commands, flags, or files

## What NOT to do

- **Do not** edit `SKILL.md` and `meta.yml` to bump `lastUpdated` by hand — the prompt-library generator derives it from `git log`. Manual entries are an override, not the default path.
- **Do not** invent a `version` bump unless the change genuinely warrants it. Most changes don't need a version.
- **Do not** include implementation chatter in `User-Facing-Change:` ("refactored the helper", "moved logic to scripts/") — describe the *user-observable* effect, not how the change was made.
- **Do not** commit secrets or personal config to skills. The repo is public.
- **Do not** add skills that are tightly coupled to one developer's local setup. If it only works because of your `~/.config` or your specific time tracker workspace, keep it in `~/.claude/skills/` instead.

## Validating changes locally before pushing

If the prompt_library checkout is available as a sibling directory, you can preview the rendered page:

```bash
cd ../prompt_library
git submodule update --remote _skills-vendor
npm run generate-skills
npm start
# visit http://localhost:8080/<discipline>/skills/<name>/
```

The generator is strict about frontmatter — if `SKILL.md` has multi-line YAML or `meta.yml` is malformed, the build fails fast with a clear error pointing at the offending file.
