# Lullabot Skills

A bundle of agent-neutral skills maintained by Lullabot for use across client and internal projects. Skills work with any capable agent using their declared tools; [Claude Code](https://docs.claude.com/en/docs/claude-code/skills) is one supported installation example. Each skill is also browsable individually in the [Lullabot Prompt Library](https://github.com/Lullabot/prompt_library); this repo exists to make installing all of them at once a one-liner.

## Install

For Claude Code, from the root of any project:

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

Each public skill lives in its own top-level folder with two required files. Hidden
development tooling (`.agents/`, `.claude/`, `.ai/`) and `node_modules/` are not
public skills:

```text
<skill-name>/
  SKILL.md      # Agent-neutral skill definition (name + description frontmatter, then markdown body)
  meta.yml      # Lullabot prompt-library metadata
  …             # optional: scripts/, references/, assets/, etc.
```

`meta.yml` carries the metadata the [prompt library](https://github.com/Lullabot/prompt_library) site needs to categorize and render the skill — agents do not need it at runtime.

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

Use Node.js 22.18 or later and the pinned development dependencies. Before opening
a PR, run the same deterministic checks as CI:

```bash
npm ci
npm run validate
npm run check:skills
npm run spellcheck
```

Run `npm test` for the Node.js checker fixtures, plus meaningful companion
behavior tests for executable changes. Structure, disclosure/portability, and
spelling checks do not execute companion programs. A separate read-only CI test
job exercises selected companion behavior with synthetic inputs and standard
Python/PHP tooling, without live services or installing skill dependencies. It
covers the htmx server, Tugboat uploader, Drupal cleanup, SEO helpers, and crawler
guards; it does not establish complete end-to-end workflow correctness. CI checks
the whole public bundle, including existing skills; migration has no exceptions
for older submissions. The checks can fail a CI job. Requiring those statuses for
merging is separate, deferred administrator setup.

Every `SKILL.md` needs substantive `## Requirements` and `## Safety and review`
sections. Declare tools, packages, services, authentication, permissions, and any
optional dependencies; state explicitly when none are needed. Preserve the skill's
name, purpose, and triggers. Keep `name` and `description` on single YAML lines,
and use one allowed `discipline`. Do not manually bump dates or versions during
migration.

Resolve companion files relative to the loaded skill's location, independent of
the agent or installation directory. Describe how user input is read from the
request. Blocking portability checks cover known agent-only variables,
Claude-specific companion execution paths, and the built-in security review
command. Product mentions and installation instructions can remain. Broader
portability needs human review. The rare quoted or optional occurrence exemption
is narrowly scoped: see `checkPortability` in
[scripts/check-submissions.js](scripts/check-submissions.js); exemptions identify
one exact occurrence on the next line and explain its purpose. They do not waive
requirements or human review.

CSpell checks public definitions, metadata, first-party companion documentation,
and contributor Markdown, including code fences. Its scope and narrow exclusions
are in [cspell.json](cspell.json): installed tooling and the pinned upstream rubric
are excluded. Correct real mistakes; propose reviewed project names, command
names, and technical terms in [cspell-words.txt](cspell-words.txt). Explain unusual
additions in the PR rather than adding broad exclusions or accepting misspellings.

**Before committing, review your staged changes and write a `User-Facing-Change:`
trailer for substantive skill changes.** Describe the user-observable effect in
plain language; the public site renders these trailers as per-skill changelog
entries. Use scoped trailers for multiple skills and skip cosmetic or internal
changes. See [AGENTS.md](AGENTS.md) for examples. This is a manual staged-diff
review; no changelog proposal service is required.

### Human review and AI use

Read the complete skill and all companion files before requesting another
person's review. Use the [PR template](.github/PULL_REQUEST_TEMPLATE.md) to record
purpose and triggers, requirements, tested results, untested limitations, and
review evidence. A checked declaration or passing scan does not establish
correctness, absence of private information, tool approval, or policy compliance.

The public policy summary below reflects Lullabot's AI Usage Policy, last reviewed
January 2026. Keep the raw policy, private approval records, credentials, personal
information, client or company confidential material, and identifying examples out
of this public repository, including assets and hidden metadata.

- Humans review AI-assisted work before handing it to another human or sharing it
  externally. Automatic advisory comments below are approved feedback for the
  submitter; they do not replace author self-review or human approval.
- Humans review commands and code before execution outside a secure sandbox, and
  review MCP operations that change data before those operations run. A sandbox
  exception does not waive data protection or later review transitions.
- Classify input data and verify that the destination and tool are eligible for
  that data. Use approved tooling where required; stop when eligibility or needed
  approval is unknown. Personal data requires specifically approved tools integrated
  with the system holding it; confidential data requires approved tools, and
  non-public data requires verified retention and training restrictions. Merely
  listing a tool here does not approve its use. New tools need Security Team review;
  training on company data needs explicit prior approval.
- Qualified reviewers assess code, and domain experts evaluate workflows built by
  non-experts. Identify approval evidence and outstanding exceptions. Apply the
  relevant editorial, brand, accessibility, originality, and AI disclosure rules;
  sales and marketing material and proposals must not be substantially AI-created
  except in rare cases with full disclosure. Respect client AI preferences, avoid
  copying protected work or named artists' styles, and keep final decisions with
  humans. Use deterministic code for calculations; humans own strategic, budget,
  and client communication decisions.

The prepared [CODEOWNERS](.github/CODEOWNERS) patterns request qualified review for
separate executable files, workflow definitions, and the ownership file. They do
not assign ordinary skill Markdown to developers. Authors must understand embedded
commands and examples and keep code beyond simple examples in separate files. Simple examples are short
invocations or illustrative fragments; reusable programs and implementation logic
belong in companions.
Qualified human review remains necessary while native enforcement is deferred.

### Automated advisory feedback

Run the mechanical authoring checker locally before changing a skill:

```bash
node scripts/review-skill.js <skill-dir>
```

Omit the argument to review every public skill. It always exits zero; its findings
and the [reviewing-skills rubric](reviewing-skills/references/skill-best-practices.md)
are advisory. For deeper local judgment, invoke `reviewing-skills` in a capable
agent. The rubric's `last_synced` date and `scripts/sync-best-practices.sh` support
periodic upstream review.

PR feedback combines mechanical findings and an optional Anthropic API review in
one sticky comment, updated for the reviewed commit. The model assesses:

- Duplicate purpose and trigger overlap, comparing changed skills with the public
  catalog and one another. Humans decide whether overlap warrants consolidation.
- Safety consistency between the declared review boundaries and actual workflow.
- Requirements completeness, including implicit tools and permissions.
- Semantic portability beyond the finite blocking patterns.
- Authoring quality, using the existing rubric for clarity, examples, and useful
  progressive disclosure.

Reports are labeled automated and advisory and identify their commit, model,
located evidence, and incomplete coverage. Missing credentials, unavailable APIs,
invalid responses, and bounded-input omissions are explicit limitations rather
than a clean review. Model conclusions never determine the blocking CI result.

The small JavaScript reviewer uses the pinned Anthropic SDK. Its CLI accepts a
verified JSON snapshot and writes a structured advisory report:

```bash
node scripts/llm-review.js --snapshot <snapshot.json> --output <review.json>
```

`ANTHROPIC_API_KEY` is the API credential; `ANTHROPIC_MODEL` selects the model
(default: `claude-sonnet-5-5`). Configure them in trusted reporting only. The CLI
exits zero for advisory failures as well as findings. Run
`node --test scripts/tests/llm-review.test.js` for mock-based validation without a
credential or paid request. Actual service quality, approval, and budget remain
administrator work.

The trusted reporter reads the exact submitted snapshot as untrusted data. It uses
reviewer code, prompts, rubric, and pinned dependencies from the trusted default
branch, never submitted programs or a PR-modified review policy. The model gets
bounded public review material (catalog descriptions and selected skill bodies
and companions), has no execution tools, and cannot write repository files. Review
material is sent to Anthropic; confidential material must not be submitted.

Fork CI runs without model credentials or write permissions after any approval
required by the repository's configured fork policy. A separate `workflow_run`
reporter verifies the source run, PR, and current commit before using credentials
and posting feedback; stale results are suppressed. This reporter only activates
once its workflow exists on the default branch. Maintainer approval of fork CI
does not expose secrets to that fork workflow. Fork advisory reporting also requires
`SKILL_REVIEW_FORK_APPROVAL_VERIFIED=true`, a repository variable set only after an
administrator verifies the intended approval policy. A completed CI run alone
cannot prove those settings; the reporter declines fork advisory review when this
attestation is absent.

### Deferred administrator handoff

The repository change prepares configuration. The following administrator work
remains **deferred and unverified**; existing private settings could not be
inspected, so this is not a claim that no configuration already exists:

- Create or verify `@Lullabot/skill-review`, its organization visibility and explicit
  repository write access. Include eligible developers and explicitly approved
  additional qualified reviewers; leave the existing developers team unchanged.
- Choose a smaller active auto-assignment pool and exclusions, with **Only notify
  requested team members**. Verify notification behavior and that eligible
  unassigned members can still approve; assignment exclusions do not remove
  code-owner eligibility.
- Inspect GitHub's ownership error report, then require the exact statuses
  **Skill structure**, **Skill disclosure and portability**, **Skill spelling**,
  and **Skill tests**, plus code-owner approval through branch protection or a
  ruleset. Check
  representative PRs, unavailable-reviewer fallback, and actual merge enforcement
  before describing qualified approval as enforced.
- Verify fork workflow approval settings for the intended contributor population;
  do not assume every fork requires approval. After verifying coverage for the
  intended outside contributors, set the repository variable
  `SKILL_REVIEW_FORK_APPROVAL_VERIFIED=true`. Leave it unset until verified; a
  completed CI run is insufficient evidence of the approval policy. Activate and
  test trusted reporting after it reaches the default branch.
- Provision an approved Anthropic service account and API secret, explicit model
  configuration, request limits and budget. Use the `ANTHROPIC_API_KEY` secret and
  `ANTHROPIC_MODEL` repository variable (default: `claude-sonnet-5-5`). Check the
  eligible public review data
  and actual live report quality. Mocked tests do not verify a live service.

No team membership, notifications, secrets, repository permissions, or merge
settings are changed as part of this repository implementation.

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
configuration that is intentionally excluded from version control. Before any
host execution, review that local configuration and the installed workflow skills
for permission-bypass modes, sandbox assumptions, and execution targets. Vendored
defaults are not policy approval; do not enable unattended privileged host
execution. The public-bundle exclusion does not exempt this tooling from human
review or data-handling requirements. Then validate
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
