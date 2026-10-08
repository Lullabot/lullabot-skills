---
id: 2
group: "migrate-operational-skills"
dependencies: []
status: "completed"
created: 2026-10-08
skills: ["skill-authoring", "secure-coding"]
complexity_score: 6
complexity_notes: "Bounded ownership and concrete integration acceptance keep this atomic; security and migration judgment require high effort."
execution_profile: "sol-high"
---
# Migrate operational and code-bearing skills

## Objective
Migrate thirteen operational skills for declared prerequisites, portable paths, meaningful review gates and policy safeguards.

## Skills Required
skill-authoring, secure-coding. Invoke relevant installed skills; labels alone do not imply installed skill files.

## Acceptance Criteria
- [x] Each assigned SKILL.md has single-line name/description, substantive Requirements and Safety and review, and complete concrete tool declarations.
- [x] Review all assigned instructions and companions against the public policy mapping; expose pre-execution shell review, external/MCP mutation and sharing gates, least privilege, and data restrictions.
- [x] Replace Claude-only paths/variables/operations with actual skill-location resolution and agent-neutral alternatives; preserve useful commands and intent.
- [x] Move reusable htmx server and Tugboat upload implementations into companion files; retain short illustrative commands and useful teaching snippets.
- [x] Record per-skill inspected and exercised checks with credential/service limitations; run node scripts/review-skill.js for assigned skills and appropriate harmless script checks.

## Technical Requirements
Follow plan 1 and its approved scope. Ownership: cloudflare-tunnel, content-inventory, data-dict-extractor, ddev-xhgui-analyze, drupal-demo-recorder, drupal-security-review, github-attachments, github-wiki, gws-cli, htmx-expert, improve-test-quality, refresh, tugboat-cli and their companion files only; do not edit shared scripts, package files, dictionaries, workflows or README/AGENTS.

## Input Dependencies
The current repository and approved plan; no task dependencies.

## Output Artifacts
Owned changes above, task status and concrete verification evidence.

## Implementation Notes

<details>
<summary>Execution guidance</summary>

Read and apply /home/andrew/.codex/skills/.system/skill-creator/SKILL.md and reviewing-skills/SKILL.md with its rubric. You are not alone; preserve other workers edits. Read whole assigned files and relevant companions; do not append boilerplate hiding unsafe workflow instructions. Understand actual code before changing examples. Do not run external-service mutations, destructive refresh, or install skill dependencies to test documentation. Preserve skill names and metadata dates; no manual versions. Existing tests for changed companions warrant meaningful verification, but do not create tests mirroring prose.

Routing rationale: sol-high; required judgement means no task is assigned to the unavailable GPT-5.6 Luna. Each task uses a subagent. Read PRE_TASK_EXECUTION.md and apply meaningful red-green-refactor tests where appropriate. You share the codebase; do not revert others edits. Do not commit or push; orchestrator owns phase commits.

</details>

## Execution evidence — 2026-10-08

Completed by the operational migration subagent using the selected GPT-6.1 Sol High routing. Read the repository AGENTS.md, `.ai/strikethroo/config/hooks/PRE_TASK_EXECUTION.md`, the complete assigned workflows and meaningful companion code/references, `skill-creator`, `reviewing-skills`, its vendored rubric, and plan 1's policy/portability requirements. No commits, pushes, package installations, external writes, live demonstrations, or destructive repository refresh were performed by this task. Shared tooling and other workers' files were preserved.

All thirteen entrypoints now declare concrete requirements and substantive Safety and review. Loaded-skill paths are explicitly resolved separately from the working project; host/container paths require verified mounts or copying only the needed companion into the project. Removed runtime reliance on Claude variables, installation layouts, command/tool names, and unconditional demonstration execution. Preserved skill names and metadata dates without version overrides.

### Per-skill inspection and actual checks

| Skill | Inspected workflow/companions and substantive changes | Actually exercised; limits |
| --- | --- | --- |
| cloudflare-tunnel | Full tunnel workflow and Bash helper; reviewed public exposure, credentials, package installation, stop scope, configuration preservation, and URL-sharing boundaries. Portable quoted companion invocation. | `bash -n` passed; `cloudflared --version` reported 2026.10.0. Copied helper into a temporary neutral installation outside a synthetic project and ran usage (expected exit 1, command list present). No login, creation, tunnel, installation, or live exposure test. |
| content-inventory | Full workflow, both pipelines, CLI, all normalization/readability/file/output/redirect modules, CSV checker, and all three references. Declared pandas 2.2+ and optional requests; bounded optional HTTP against trusted public inputs, local output overwrite/formula review, and human legal/content decisions. Corrected the visible Responsibilities header typo and removed nonexistent bundled pytest instructions. | Python AST parsing passed for every module; checker `--help` passed. Real checker accepted four synthetic public CSV exports (exit 0) and rejected a wrong pages export with missing Address (exit 1). pandas/openpyxl are absent, so generation/Excel and redirect processing were not executed; no dependencies installed. |
| data-dict-extractor | Full extractor, workbook/sheet generation, YAML loading, command defaults, and project-relative outputs. Explicit local config eligibility and filename/output review. | Python AST parsing passed. PyYAML is available but openpyxl is absent; workbook generation and helper `--help` are therefore untested. No dependency install or live Drupal access. |
| ddev-xhgui-analyze | Full SQL/export/PHP analysis and report workflow. Read-only credentials, validated run IDs before SQL/path interpolation, confidential profile handling, deterministic metric conversion, and review before sharing. | `ddev version` ran and reported 1.25.4, but Docker API access was permission denied. No DDEV project/profile/database supplied; SQL, export, and analysis were inspected, not executed. |
| drupal-demo-recorder | Full recording workflow, overlay JS, JSON config, bootstrap, transcode, and frame helpers. Bootstrap defaults to non-mutating check mode; `--apply` gates reviewed setup/start/restart effects and existing ffmpeg Dockerfile is preserved. Copied overlay path is verified in the project mount; login occurs before recording. | All Bash syntax checks, JS syntax check, and bootstrap `--help` passed. A mock DDEV synthetic project returned missing-tool exit 1 with only describe/which calls and zero filesystem changes. Docker unavailable; no add-on install, start/restart, browser, ffmpeg, or actual video test. |
| drupal-security-review | Full security methodology, recon/cleanup PHP and UI/CLI references. Human-reviewed isolated reproduction scope precedes all mutation; unsafe/unavailable demos remain unverified. Replaced broad title/user-prefix deletion with exact ID/label manifest preview and explicit apply. Neutral artifact delivery and sequential fallback for unavailable delegation. | Both PHP files linted. Four synthetic-storage tests passed: preview never deletes; apply deletes only the exact ID; label mismatch prevents all deletion; user ID 1 is protected. Tests failed against old cleanup before replacement and passed after it. No Drupal bootstrap/recon or live exploit/cleanup execution; Docker unavailable. |
| github-attachments | Full supported and fallback upload workflows plus Bash helper. Separate upload/post review, publicly accessible persistent asset URL, repository scope, image/metadata redaction, credential limits, and partial-success retry handling. | Bash syntax passed; `gh --version` reported 2.102.0. No upload or GitHub content mutation; live authentication/destination permissions were not tested. |
| github-wiki | Full workflow and Gollum reference; removed unused API placeholder. Stage only reviewed files, verify wiki remote/default branch, human self-review before immediate publication, and image/private-data checks. | `git --version` reported 2.47.3. Command examples and links were inspected; no wiki remote/auth supplied and no clone, push, or live rendering test. |
| gws-cli | Full Gmail/Calendar/Drive/Sheets/cross-service reference. Data eligibility before retrieval, narrow scopes/pagination, account/recipient/body review before all mutations including drafts, dry-run limits, and preservation of user-selected approved tooling. Direct send does not bypass human review. | CLI availability checked: `gws` absent. No Google authentication, reads, sends, drafts, uploads, scheduling, or sharing tested. |
| htmx-expert | Full attribute/event/security/config and prototype workflows. Extracted Python server into a linked companion; kept short invocation and teaching fragments; moved optional practical patterns into a linked reference. Safer script/origin/evaluation defaults, loopback-only prototype, dedicated public/synthetic directory. | New helper `--help` and Python syntax passed. Two local tests passed for loopback binding/static content/HTML fragment and missing-directory rejection. Tests first failed while the companion was absent, then passed. No production/backend/deployment test. |
| improve-test-quality | Full phased workflow, JS analyzer and both READMEs. Absolute companion path with report resolution from working project; installed Stryker binary prevents opportunistic npx downloads. Auto mode is scoped to local test edits and retains command/data/share review. Moved long output/error examples into direct references. | JS syntax passed. Analyzer executed from a separate temporary synthetic project using an absolute loaded-skill path; summary produced the expected score 50 for one killed/one surviving mutant. No project-installed Stryker/test harness supplied, so actual mutation runs untested. |
| refresh | Full survey, discard classification, default-branch discovery, reset/clean, worktree/submodule, and failure workflow. Generated/lockfile names no longer imply disposability. Inspect target local default commits/worktree before discarding, use the chosen remote consistently, clean only approved paths, preserve uncertain/submodule work, and review exact destructive scope. | Git version checked and command semantics inspected; no destructive refresh, remote fetch, cleanup, checkout, or submodule update executed. Prose-only changes warrant no tests matching wording. |
| tugboat-cli | Full CLI workflow/reference including lifecycle, credentials, grants, shell, config, and upload pitfalls. Extracted Python upload helper with JSON argv and proper shell quoting, default preview without contacting service, no-clobber default, explicit execute/overwrite, and public-docroot review. | Python syntax and helper `--help` passed. Three tests passed: binary bytes round-trip through a local Bash command with quoted destination; default no-clobber and injection prevention; relative path rejection; preview makes no subprocess/API call. Tests first failed while the companion was absent, then passed. `tugboat` absent; no live preview/token/config/upload test. |

### Repository and authoring verification

- Ran `node scripts/review-skill.js <skill>` separately for each of the thirteen assigned skills after fixes: no issues or suggestions for any assigned skill. Descriptions/triggers, freedom appropriate to fragile mutations, direct references, executable intent, and policy consistency received an additional manual agent review. This is not human policy sign-off.
- `node scripts/validate-skills.js`: passed, 26 public skills.
- `npm run check:skills`: passed, Requirements/Safety and review/portability for 26 public skills.
- `git diff --check`: passed after removing an extra EOF blank line.
- New meaningful code tests cover behavior and safety boundaries; no wording-matching tests were added for documentation. The PRE_TASK_EXECUTION red/green cycle was exercised for the two new companions and cleanup's new manifest interface; after cleanup/quoting refinements, all nine companion tests passed again.
- No claims are made that tools are approved, human review is complete, real client inputs are eligible, live accounts are authorized, or the service-dependent workflows ran successfully. Those checks remain with the user/qualified reviewer in an appropriate environment.
