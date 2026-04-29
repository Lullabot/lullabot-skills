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
- **github-wiki** — Read and edit GitHub wikis.
- **gws-cli** — Drive Google Workspace (Gmail, Calendar, Drive, Sheets, Docs) from the CLI.
- **htmx-expert** — htmx patterns, attributes, and hypermedia-driven app guidance.
- **humanizer** — Strip AI-writing tells from text.
- **nano-banana-prompt** — Craft prompts for Gemini Nano Banana image generation.
- **noko-log-time** — Analyze Claude Code sessions and log time entries to Noko.
- **pencil-designer** — Work with Pencil design files via the Pencil MCP tools.
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

## License

MIT — see `LICENSE`.
