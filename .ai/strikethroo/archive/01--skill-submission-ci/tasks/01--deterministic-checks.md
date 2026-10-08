---
id: 1
group: "deterministic-checks"
dependencies: []
status: "completed"
created: 2026-10-08
skills: ["nodejs", "validation"]
complexity_score: 6
complexity_notes: "Bounded ownership and concrete integration acceptance keep this atomic; security and migration judgment require high effort."
execution_profile: "sol-high"
---
# Build deterministic submission checks

## Objective
Strengthen structure, requirements/safety disclosures, portability, and spelling infrastructure without running submitted programs.

## Skills Required
nodejs, validation. Invoke relevant installed skills; labels alone do not imply installed skill files.

## Acceptance Criteria
- [x] Install exact pinned yaml, cspell, and @anthropic-ai/sdk dependencies with lockfile; Node 22 commands: npm test, npm run validate, npm run check:skills, npm run spellcheck.
- [x] Use shared public directory discovery, real YAML parsing, scalar/source single-line validation, valid metadata lists and discipline, and incomplete-directory errors.
- [x] Check substantive Requirements and Safety and review Markdown sections outside code fences; known portability rules with narrow exact-occurrence rationale exemptions.
- [x] Preserve advisory checker behavior and add mechanical missing-reference/XML checks only as advice. Keep exports compatible with its caller.
- [x] Meaningful fixture tests reject malformed metadata, fake sections, dependency dirs and known runtime coupling while allowing legitimate installation/quoted references.
- [x] Spelling infrastructure uses reviewed scope and dictionary; existing spelling failures are expected until task 7.

## Technical Requirements
Follow plan 1 and its approved scope. Ownership: package.json, package-lock.json, cspell.json, cspell-words.txt initial dictionary, .gitignore, scripts/validate-skills.js, scripts/check-submissions.js, scripts/review-skill.js, scripts/tests/validation*.test.js; do not edit skill directories, workflows, or contributor docs.

## Input Dependencies
The current repository and approved plan; no task dependencies.

## Output Artifacts
Owned changes above, task status and concrete verification evidence.

## Implementation Notes

<details>
<summary>Execution guidance</summary>

Use red-green-refactor for validation logic. Shared checker exports must support task 4. Preserve one discipline scalar and multiline descriptions must fail. No broad portability exemptions. Exclude node_modules, .ai, .agents, .claude, .codex, .github, scripts from public discovery. Package dependencies belong only to this task; no concurrent package edits. npm scripts should keep structure and disclosure/portability commands separate. node --test scripts/tests/*.test.js supplies meaningful integration fixtures. All existing migration failures are baseline until tasks 2 and 3 finish.

Routing rationale: sol-high; required judgement means no task is assigned to the unavailable GPT-5.6 Luna. Each task uses a subagent. Read PRE_TASK_EXECUTION.md and apply meaningful red-green-refactor tests where appropriate. You share the codebase; do not revert others edits. Do not commit or push; orchestrator owns phase commits.

</details>

## Noteworthy Events
- [2026-10-08] Delegated implementation followed PRE_TASK_EXECUTION.md and meaningful red-green-refactor increments. Fixture failures first demonstrated discovery ignoring its root, malformed YAML acceptance, multiline/type acceptance, missing disclosure and portability checks, missing advisory XML/reference checks, placeholder-only section bypass, and braced ARGUMENTS coupling. The corresponding fixes passed before refactoring. Fixtures are isolated temporary data, and npm tests do not import or run submitted companion programs.
- [2026-10-08] Added exact pinned dev dependencies yaml 2.9.1, cspell 10.3.6, and @anthropic-ai/sdk 0.132.1 with npm lockfile. Node 22.23.3 reproducible `npm ci --ignore-scripts` completed successfully (115 packages, 0 audit vulnerabilities); package engines require Node >=22.18.0 because of CSpell's supported runtime.
- [2026-10-08] Verification on Node 22.23.3: `npm test` passed 14 tests; `npm run validate` passed all 26 public skills; `npm run check:skills` passed all 26 public skills. The advisory `node scripts/review-skill.js` exited 0 with 3 issues and 22 suggestions, preserving its nonblocking contract. Structural and advisory exports remain compatible, with optional fixture/snapshot root arguments and shared public discovery.
- [2026-10-08] Spelling scope covers public definitions, metadata, first-party companion documentation, repository Markdown, trusted scripts/review-policy.md when present, and .github Markdown templates. It excludes dependency/tooling directories and the exact pinned upstream authoring rubric. The initial dictionary contains reviewed tool/project terms. `npm run spellcheck` correctly exits 1 on the current baseline (349 issues in 51 of 84 files at the final Node 22 run; the shared tree changed during parallel migration); final cleanup is explicitly task 7. A fixture proves an intentional typo fails, reviewed terms pass, and installed tooling is excluded.
- [2026-10-08] Known portability failures are scoped to CLAUDE_SKILL_DIR, supplied ARGUMENTS shell parameters (including defaults and array access), hardcoded Claude companion paths, and the known Claude security-review operation. Exemptions require a recognized rule, one exact matched occurrence on the next source line, and substantive rationale; invalid, ambiguous, and unused exemptions fail. Broader semantic portability and policy judgments remain advisory/human responsibilities.
- [2026-10-08] Owned changes pass `git diff --check`. A repository-wide whitespace check identified a trailing blank line in improve-test-quality/SKILL.md owned by the migration worker; it was reported to the orchestrator without changing another worker's file. Python bytecode and node_modules are ignored as generated artifacts. No commit, push, submitted companion execution, or live external-service workflow was performed.

- [2026-10-08] Phase-3 compatibility follow-up: the orchestrator reproduced an unsupported-tag mismatch between yaml 2.9.1 (TAG_RESOLVE_FAILED warning but no parse error) and prompt-library's js-yaml 4.1.1 loader (rejection). Added a failing fixture for unknown tags in both name/description frontmatter and scalar/nested-list metadata, then rejected only the finite TAG_RESOLVE_FAILED warning code. Standard supported !!str tags remain valid. The fixture now passes; all 26 public skills pass structural validation, all 42 current repository tests pass under Node 22, and owned whitespace checks pass. Task status remains completed; no commit or push performed by this worker.
