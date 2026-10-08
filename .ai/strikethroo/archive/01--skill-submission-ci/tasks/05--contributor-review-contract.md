---
id: 5
group: "contributor-review-contract"
dependencies: [1, 2, 3]
status: "completed"
created: 2026-10-08
skills: ["technical-writing", "github-review"]
complexity_score: 5
execution_profile: "sol-medium"
---
# Document contributor and administrator review contract

## Objective
Publish focused contributor instructions, Markdown PR template, standalone code ownership and deferred administrator handoff.

## Skills Required
technical-writing, github-review. Invoke relevant installed skills; labels alone do not imply installed skill files.

## Acceptance Criteria
- [x] Explain required local commands, automatic/advisory limits, skill location, spelling scope/dictionary and migration conventions while preserving manual changelog instructions from main.
- [x] PR checklist preserves four exact user declarations plus existing companion, test, requirements, policy review prompts; no issue form.
- [x] CODEOWNERS covers actual JS/CJS/Python/PHP/shell companions, workflows and ownership file; ordinary public skill Markdown is not developer-owned.
- [x] Plan @Lullabot/skill-review with all membership, notifications, permissions and merge activation deferred; document fork approval settings, API/model secret and budget provisioning as not configured.
- [x] Explain all five semantic categories and automated submitter feedback, private-policy prohibition, trusted code boundary and vendored-tool permission defaults.
- [x] Manually validate ownership representative coverage and template headings; git diff --check passes.

## Technical Requirements
Follow plan 1 and its approved scope. Ownership: README.md, AGENTS.md, CLAUDE.md if needed, .github/PULL_REQUEST_TEMPLATE.md, .github/CODEOWNERS only.

## Input Dependencies
Task outputs: 1, 2, 3

## Output Artifacts
Owned changes above, task status and concrete verification evidence.

## Implementation Notes

<details>
<summary>Execution guidance</summary>

Review current docs and actual package commands. Keep README focused with concise public policy summary and handoff; no raw AI policy and no private approval records. No admin/API-secret/team writes. Owning team may not yet exist; no live lookup gate. Spell final cleanup is task 7. Coordinate reviewer CLI command spelling with task 4.

Routing rationale: sol-medium; required judgement means no task is assigned to the unavailable GPT-5.6 Luna. Each task uses a subagent. Read PRE_TASK_EXECUTION.md and apply meaningful red-green-refactor tests where appropriate. You share the codebase; do not revert others edits. Do not commit or push; orchestrator owns phase commits.

</details>

## Execution Evidence

- Executed on 2026-10-08 by the delegated GPT-6.1 Sol Medium worker, following
  `st-execute-task` and PRE_TASK_EXECUTION. Technical-writing and github-review
  capability labels had no matching installed skills; focused technical editing
  was performed directly. No new tests were warranted for prose, template, or
  ownership declarations; manual acceptance review was meaningful here.
- Updated README.md and AGENTS.md. CLAUDE.md remains the existing symlink to
  AGENTS.md, preserving one shared instruction source. Created the Markdown PR
  template and standalone CODEOWNERS; no issue form was added.
- Read package.json and the actual submission checker/CSpell scope to document
  `npm ci`, `npm run validate`, `npm run check:skills`, `npm run spellcheck`,
  checker tests and relevant executable companion tests accurately. Preserved
  manual staged-diff changelog instructions and neutral installation paths.
- `node scripts/validate-skills.js`: passed, 26 skills.
- `node scripts/check-submissions.js`: passed, 26 skills.
- Manually reviewed all seven template headings and all eight checklist entries;
  the four user-requested declarations are preserved exactly, with the requested
  punctuation. Companion files, testing limitations, requirements, and applicable
  policy review prompts remain explicit.
- Manually checked extension-only, any-depth CODEOWNERS patterns against
  `drupal-demo-recorder/assets/input-overlay.js`,
  `.agents/skills/st-execute-task/scripts/dispatch-task-execution.cjs`,
  `content-inventory/scripts/content_inventory/cli.py`,
  `drupal-security-review/scripts/recon.php`, and
  `seo-expert/scripts/crawl_site.sh`; each matches @Lullabot/skill-review.
  `.github/workflows/skill-review.yml` and `.github/CODEOWNERS` match their
  anchored patterns. `htmx-expert/SKILL.md` and README.md have no automatic
  code ownership. Pattern ordering has no competing owner. Live team existence
  and GitHub owner validity were intentionally not made local acceptance gates.
- Targeted CSpell review of README.md, AGENTS.md and the PR template found only
  five existing occurrences of browsable/frontmatter; no new prose terms were
  reported. Dictionary cleanup and the full spelling baseline belong to task 7.
- `git diff --check`: passed after documentation and task-evidence changes.
- API CLI, credential/model names, advisory exit behavior and mock-test command
  match task 4's supplied integration contract. Exact request caps remain the
  reviewer implementation's responsibility; docs state bounded coverage and
  disclose omissions. No paid API request or live service verification was made.

## Noteworthy Events

- 2026-10-08: Only the source-attributed public policy summary is published; raw
  policy and private approval records remain excluded. Documented the five
  advisory categories, author self-review and expert-review limits, trusted
  untrusted-data boundary, and local Strikethroo permission review.
- 2026-10-08: Team creation, qualified membership, auto assignment and notifications,
  write access, native merge enforcement, fork approval settings, API secret/model
  approval and budget remain deferred administrator work. Existing private settings
  were unverified, rather than assumed absent. Documented that workflow_run only
  activates once its workflow reaches the default branch. No admin, secret, team,
  commit or push actions were performed.

- 2026-10-08: Aligned the deferred handoff with task 6's fork trust gate: the
  `SKILL_REVIEW_FORK_APPROVAL_VERIFIED=true` repository variable may be set only
  after an administrator verifies the intended outside-contributor approval
  policy. Documented that a completed run alone is insufficient evidence and the
  reporter declines fork advice without the attestation. Named the API secret
  and model variable in the administrator handoff. No settings were changed;
  task 5 remains completed. `git diff --check` passed after this clarification.

- 2026-10-08: Aligned README.md and AGENTS.md with completed task 6's exact required
  status names: Skill structure, Skill disclosure and portability, Skill spelling,
  and Skill tests. Clarified that npm test runs Node.js checker fixtures and that
  structure/disclosure/spelling do not execute companions. Separate synthetic CI
  behavior coverage includes htmx (2), Tugboat (3), Drupal cleanup (4), SEO (37),
  and crawler guard (1), using standard-library Python/PHP without live services
  or skill dependency installation. Contributor prose describes the bounded
  coverage concisely. No new tests are warranted for this wording adjustment;
  `git diff --check` passed. Task 5 remains completed.
