# Lullabot Skills

A bundle of [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) maintained by Lullabot for use across client and internal projects. Each skill is also browsable individually in the [Lullabot Prompt Library](https://github.com/Lullabot/prompt_library); this repo exists to make installing all of them at once a one-liner.

## Install

From the root of any project:

```bash
git clone https://github.com/Lullabot/lullabot-skills.git .claude/skills
```

Or, to update an existing install:

```bash
cd .claude/skills && git pull
```

Claude Code will pick up every skill automatically on the next session.

> **Tip:** add `.claude/skills` to your project's `.gitignore` so each developer pulls their own copy.

## Skills included

<!-- skills-start -->
- **cloudflare-tunnel** — Expose a local dev server via Cloudflare Tunnel.
- **ddev-xhgui-analyze** — Analyze xhprof/xhgui profile runs from a DDEV environment.
- **github-attachments** — Upload screenshots and files to GitHub so they render in issues, PRs, and comments.
- **github-wiki** — Read and edit GitHub wikis.
- **gws-cli** — Drive Google Workspace (Gmail, Calendar, Drive, Sheets, Docs) from the CLI.
- **hemingway-editor** — Apply editing principles to make writing clear, direct, and powerful.
- **htmx-expert** — htmx patterns, attributes, and hypermedia-driven app guidance.
- **humanizer** — Strip AI-writing tells from text.
- **improve-test-quality** — Improve test quality with mutation testing analysis.
- **issue-writing** — Write issues, tickets, and bug reports someone else can act on.
- **nano-banana-prompt** — Craft prompts for Gemini Nano Banana image generation.
- **pencil-designer** — Work with Pencil design files via the Pencil MCP tools.
- **pull-request-description** — Write PR/MR descriptions and titles a reviewer can act on.
- **refresh** — Reset a repo to a clean, up-to-date default branch, halting if it finds unsaved work.
- **resolve-composer-conflicts** — Resolve `composer.lock` merge conflicts cleanly.
- **seo-expert** — SEO audits and prioritized recommendations.
- **slack-markdown-formatter** — Format messages for Slack's mrkdwn dialect.
- **tugboat-cli** — Manage Tugboat preview environments via the `tugboat` CLI.
<!-- skills-end -->

## Skill structure

Each skill lives in its own folder with two required files:

```text
<skill-name>/
  SKILL.md      # Claude Code skill definition (name + description frontmatter, then markdown body)
  meta.yml      # Lullabot prompt-library metadata
  …             # optional: scripts/, references/, assets/, etc.
```

`meta.yml` carries the metadata the [prompt library](https://github.com/Lullabot/prompt_library) site needs to categorize and render the skill — Claude Code ignores it at runtime.

```yaml
title: "Cloudflare Tunnel"
discipline: development          # one of: development, content-strategy, design,
                                 # project-management, quality-assurance, sales-marketing
date: "2025-01-22"               # original publication date
tags: [cloudflare, tunnels, networking]
# Optional version tracking:
version: "1.1.0"
lastUpdated: "2026-04-14"
changelog:
  - version: "1.1.0"
    date: "2026-04-14"
    summary: "What changed"
```

## Contributing

This repo is the source of truth for skill content. Edits made here flow downstream to the prompt library site automatically on push to `main`. Open PRs directly against this repo.

Before opening a PR, validate skill structure:

```bash
node scripts/validate-skills.js
```

**Before committing, review your staged changes and write a `User-Facing-Change:` trailer for substantive skill changes.** Describe the user-observable effect in plain language; the public site renders these trailers as per-skill changelog entries. Cosmetic / internal commits skip the trailer. See `AGENTS.md` for the full convention.

## Planning repository changes

[Strikethroo](https://strikethroo.canpicasoft.com/) is installed for development
of this repository, with a shared workspace in `.ai/strikethroo/` and seven
workflow skills in `.agents/skills/`. Claude Code discovers the same skills
through links in `.claude/skills/`. These hidden tooling directories are separate
from the public skill bundle.

Use `st-create-plan` with a work order to prepare a plan. The skill confirms
scope and compatibility requirements before writing the plan. Review the plan
before using `st-execute-blueprint` to implement it.

Node.js 22 or later is required. After cloning this repository, initialize the
ignored local configuration using the installed workspace version:

```bash
npx strikethroo@4.1.1 init
```

This uses the saved Codex and Claude harness selection and creates the local
configuration that is intentionally excluded from version control. Then validate
the workspace with:

```bash
npx strikethroo validate
```

To refresh the workspace, run `npx strikethroo@latest init` (it remembers the
Codex and Claude harness selection). Reinstall the workflow skills from
`e0ipso/strikethroo` into `.agents/skills/` using your skill installer; preserve
the Claude links when updating.

## License

MIT — see `LICENSE`.
