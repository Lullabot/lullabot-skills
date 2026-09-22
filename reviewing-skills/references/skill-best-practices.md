<!-- source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices -->
<!-- last_synced: 2026-09-22 -->

# Skill authoring best practices (rubric)

A curated checklist distilled from Anthropic's skill-authoring best practices, scoped to
this repo's review workflow. The canonical, always-current source is the URL in the comment
above. Refresh this file with `scripts/sync-best-practices.sh` (see the `reviewing-skills`
refresh mode) and bump `last_synced`.

## Contents

- [Frontmatter rules](#frontmatter-rules)
- [Conciseness](#conciseness)
- [Structure and progressive disclosure](#structure-and-progressive-disclosure)
- [Naming](#naming)
- [Workflows and feedback loops](#workflows-and-feedback-loops)
- [Content guidelines](#content-guidelines)
- [Scripts and executable code](#scripts-and-executable-code)
- [Evaluation and iteration](#evaluation-and-iteration)
- [Quick checklist](#quick-checklist)

## Frontmatter rules

- **`name`** — max 64 characters; lowercase letters, numbers, and hyphens only; no XML tags;
  must not contain the reserved words `anthropic` or `claude`; should match the skill's
  directory name (this repo's `validate-skills.js` enforces the match).
- **`description`** — non-empty; max 1024 characters; no XML tags. Must state **both what the
  skill does and when to use it**, because Claude picks among many skills using this field
  alone.
- **Third person, always.** The description is injected into the system prompt; first/second
  person ("I can help…", "You can use this…") causes discovery problems. Write "Processes
  Excel files and generates reports."
- **Be specific, include trigger terms.** Avoid vague descriptions ("Helps with documents",
  "Processes data", "Does stuff with files"). Name the file types, tasks, and contexts that
  should trigger it.
- Both `name` and `description` must be a **single line each** — multi-line YAML breaks this
  repo's prompt-library generator.

## Conciseness

- **Default assumption: Claude is already smart.** Only add context Claude doesn't already
  have. Challenge each paragraph: "Does Claude really need this? Can I assume it's known?
  Does this justify its token cost?"
- Don't explain general concepts (what a PDF is, how libraries work). Show the specific,
  non-obvious thing.
- **Set degrees of freedom to match the task.** High freedom (prose steps) when many
  approaches work; medium (parameterized scripts) when a preferred pattern exists; low
  (exact commands, "do not modify") when operations are fragile and order matters.

## Structure and progressive disclosure

- **Keep the SKILL.md body under 500 lines.** Split into separate files as you approach it.
- **SKILL.md is a table of contents.** Put the overview + quick start inline; link to
  detail files (`FORMS.md`, `reference/finance.md`, `examples.md`) that load only when
  needed. Organize multi-domain skills by domain so unrelated context isn't loaded.
- **Keep references one level deep from SKILL.md.** Claude may only partially read files
  reached through a chain of references. Every detail file should link directly from
  SKILL.md, not from another detail file.
- **Reference files longer than 100 lines need a table of contents** at the top, so a
  partial read still reveals the full scope.
- **Name files descriptively** (`form_validation_rules.md`, not `doc2.md`) and use
  **forward slashes** in every path, even on Windows.

## Naming

- Prefer **gerund form** (verb + -ing): `processing-pdfs`, `analyzing-spreadsheets`,
  `reviewing-skills`. Acceptable alternatives: noun phrases (`pdf-processing`) or
  action-oriented (`process-pdfs`).
- Avoid vague (`helper`, `utils`, `tools`), overly generic (`documents`, `data`), and
  reserved-word names. Keep the pattern consistent across the skill collection.

## Workflows and feedback loops

- Break complex operations into **clear, sequential steps**. For long ones, provide a
  checklist Claude can copy into its response and check off.
- **Implement feedback loops**: run validator → fix → repeat. The "validator" can be a
  script or a reference doc Claude reads and compares against.
- For open-ended, error-prone batch work, use **plan → validate → execute**: have Claude
  write a structured plan file, validate it with a script, then execute.
- **Match template strictness to the output.** Say "ALWAYS use this exact structure" for data formats and API responses; offer "a sensible default, adapt as needed" when judgment helps.
- **Route decision points explicitly** ("Creating new content? Follow the creation workflow. Editing? Follow the editing workflow."). When a workflow grows large, move it into its own file and tell Claude which file to read for which task.

## Content guidelines

- **No time-sensitive information.** Don't write "before August 2025, use the old API."
  Keep current guidance in the main body and move deprecated material into a collapsed
  "Old patterns" section.
- **Use consistent terminology.** Pick one term per concept ("field", "extract", "API
  endpoint") and use it throughout. Mixing synonyms confuses the model.
- **Examples should be concrete, not abstract.** When output quality depends on style,
  provide input/output pairs, as in regular prompting.
- **Provide one default, with an escape hatch** — not a menu of options. "Use pdfplumber.
  For scanned PDFs needing OCR, use pdf2image instead" beats listing five libraries.

## Scripts and executable code

- **Solve, don't punt.** Scripts should handle their own error conditions rather than
  failing and leaving Claude to figure it out.
- **No voodoo constants.** Justify and document every configuration value. If you don't
  know the right value, Claude won't either.
- **Make execution intent explicit**: "Run `analyze_form.py` to extract fields" (execute)
  vs. "See `analyze_form.py` for the algorithm" (read as reference). Prefer execution for
  deterministic operations.
- **Declare dependencies.** Don't assume packages are installed; list required packages and
  the install command. claude.ai can install from npm and PyPI at runtime; the Claude API
  runtime has no network access and no runtime package installation.
- **Make validation output specific.** A validator that says "Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed" lets Claude fix the problem; "invalid input" doesn't.
- **Prefer bundled utility scripts** for deterministic operations. They're more reliable than generated code, and only their output costs context.
- Use **fully qualified MCP tool names** (`ServerName:tool_name`) to avoid "tool not found".

## Evaluation and iteration

- **Build evaluations before writing extensive docs.** Run Claude on representative tasks without the skill, note where it fails, write at least three scenarios that cover those gaps, and measure a baseline. Then write only enough instruction to pass them.
- **Test with every model you plan to use.** Haiku may need more guidance than Opus; Opus may find the same text over-explained.
- **Iterate from observed use.** Give the skill to a fresh Claude instance on real tasks and watch where it struggles. Take specifics back to the authoring session.
- **Watch how Claude navigates the skill.** Unexpected read order, missed links, one file read over and over (maybe it belongs in SKILL.md), or a bundled file never opened (maybe unnecessary or poorly signaled) all point at structure problems.

## Quick checklist

- [ ] Description is specific, third-person, includes what + when, ≤1024 chars.
- [ ] `name` is gerund-ish, ≤64 chars, lowercase/hyphen, no reserved words, matches dir.
- [ ] SKILL.md body < 500 lines; details split into separate files.
- [ ] References are one level deep; reference files >100 lines have a ToC.
- [ ] Forward-slash paths only.
- [ ] No time-sensitive info (or in an "Old patterns" section).
- [ ] Consistent terminology; examples are concrete.
- [ ] Workflows have clear steps; quality-critical tasks have a feedback loop.
- [ ] Scripts handle errors, document constants, declare dependencies.
- [ ] Critical operations have validation/verification steps.
- [ ] At least three evaluations exist; tested with each target model and on real usage.
