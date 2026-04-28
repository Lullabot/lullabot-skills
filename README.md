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
- **github-wiki** — Read and edit GitHub wikis.
- **gws-cli** — Drive Google Workspace (Gmail, Calendar, Drive, Sheets, Docs) from the CLI.
- **htmx-expert** — htmx patterns, attributes, and hypermedia-driven app guidance.
- **humanizer** — Strip AI-writing tells from text.
- **nano-banana-prompt** — Craft prompts for Gemini Nano Banana image generation.
- **resolve-composer-conflicts** — Resolve `composer.lock` merge conflicts cleanly.
- **seo-expert** — SEO audits and prioritized recommendations.
- **slack-markdown-formatter** — Format messages for Slack's mrkdwn dialect.
- **tugboat-cli** — Manage Tugboat preview environments via the `tugboat` CLI.
<!-- skills-end -->

## Contributing

Skills are authored and reviewed in the [prompt_library](https://github.com/Lullabot/prompt_library) repo, then synced here. Open issues and PRs against the prompt library — changes flow downstream to this repo.

## License

See `LICENSE`.
