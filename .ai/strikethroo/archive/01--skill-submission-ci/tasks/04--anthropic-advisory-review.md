---
id: 4
group: "anthropic-advisory-review"
dependencies: [1]
status: "completed"
created: 2026-10-08
skills: ["nodejs", "api-integration"]
complexity_score: 6
complexity_notes: "Bounded ownership and concrete integration acceptance keep this atomic; security and migration judgment require high effort."
execution_profile: "sol-high"
---
# Implement bounded Anthropic advisory reviewer

## Objective
Implement the small JavaScript advisory reviewer and structured renderer for all five approved categories.

## Skills Required
nodejs, api-integration. Invoke relevant installed skills; labels alone do not imply installed skill files.

## Acceptance Criteria
- [x] Use pinned SDK and one or two small JS modules with JSDoc and runtime validation; expose a CLI and reusable pure helpers.
- [x] Assess duplicate/trigger overlap, safety consistency, requirements completeness, semantic portability and authoring quality using trusted rubric/public policy summary.
- [x] Collect exact supplied commit snapshots and file inventory; compare catalog descriptions then candidate bodies with changed-to-changed coverage; bounds disclose omissions.
- [x] Validate structured finding categories, paths/locations/evidence, render brief advisory report with commit/model, no certification and no execution tools.
- [x] Missing key/API errors/refusals/timeouts/malformed or partial output are explicit advisory failures, not clean reports. Bound input/output/request count/retries/timeouts.
- [x] Run node --test scripts/tests/llm-review.test.js with meaningful mocked responses including invalid location, missing key, injection text as data, and coverage limits.

## Technical Requirements
Follow plan 1 and its approved scope. Ownership: scripts/llm-review.js, scripts/tests/llm-review.test.js, scripts/review-policy.md only; package dependencies and shared discovery belong to task 1; workflows belong to task 6.

## Input Dependencies
Task outputs: 1

## Output Artifacts
Owned changes above, task status and concrete verification evidence.

## Implementation Notes

<details>
<summary>Execution guidance</summary>

Read whole plan advisory section. Default API model explicit via configuration; use supported current model verified against Anthropic official docs. Never import/execute submitted files or use submitted rubric/config; script receives data snapshots. A reviewed PR instruction must not become trusted reviewer instructions. Avoid provider framework or vector DB. Coordinate exports/CLI contract with task 6; service unavailable does not block required CI. Keep public policy rubric concise source-attributed, no verbatim policy. Do not use real secret keys or paid calls without approved supplied configuration.

Routing rationale: sol-high; required judgement means no task is assigned to the unavailable GPT-5.6 Luna. Each task uses a subagent. Read PRE_TASK_EXECUTION.md and apply meaningful red-green-refactor tests where appropriate. You share the codebase; do not revert others edits. Do not commit or push; orchestrator owns phase commits.

</details>

## Noteworthy Events
- [2026-10-08] Implemented one trusted JavaScript module, one mock-test file, and an approved source-attributed public policy summary. Followed PRE_TASK_EXECUTION.md with red-green-refactor increments for catalog selection, omitted-body coverage, credential handling and injection separation, location/evidence validation, transient retries and hung transports, rendering, large-catalog prioritization, and description-only duplication mislabeling. No submitted program was imported or executed.
- [2026-10-08] Exact SHA-addressed input contract: JSON `{baseSha, headSha, changes:[{status,path,previousPath?}], files:[{path,text}], omissions?:[{path,reason}]}` containing resulting-head public files as data. Status values are added, modified, renamed, deleted. Shared public tooling exclusions and companion text extensions are reused. Catalog descriptions rank likely matches deterministically; changed skill definitions are prioritized, all supplied changed companions are considered, changed-to-changed bodies are included, and old rename/deletion identities are removed. Path-level omissions and description-only coverage are recorded.
- [2026-10-08] CLI/API shared with task 6: `node scripts/llm-review.js --snapshot snapshot.json --output report.json`; CLI exits 0 for completed, partial, skipped, and failed advisory outcomes. Exports are buildReviewMaterial, validateFindings, runReview, renderReview, DEFAULT_MODEL, CATEGORIES, LIMITS, and FINDING_SCHEMA. ANTHROPIC_API_KEY is optional at runtime; absence yields explicit skipped status. ANTHROPIC_MODEL defaults to claude-sonnet-5-5, verified by the orchestrator against Anthropic's model overview; installed SDK 0.132.1 types also show this model and output_config.format support.
- [2026-10-08] Bounds: 2 MB snapshot JSON, 180 KB complete serialized model context including trusted instructions, 32 KB per full body, 100 full text files, 100 catalog descriptions (1024 characters each, additionally bounded by a 60 KB catalog budget), six unchanged comparison candidates, 4096 output tokens, 12 findings, at most two API attempts, 45 seconds per attempt, and 90 seconds overall. SDK automatic retries are disabled; only transient transport/server failures retry once. Limits never silently truncate a full reviewed body.
- [2026-10-08] Structured findings independently validate all five categories, priorities, shape, supplied-path membership, integer line bounds, exact quotes at those locations, and body evidence in every compared skill for substantive duplication. Description-only overlap is labeled tentative. Validated quotes are stripped from outward reports, presentation escapes markup/mentions/links, and obvious private literals are omitted. These precautions do not establish absence of private information or correct model judgment. Refusals, truncation, malformed responses, errors, timeouts, and incomplete categories remain explicit advisory outcomes.
- [2026-10-08] Verification: Node 22.23.3 `node --test scripts/tests/llm-review.test.js` passed 16 tests; full Node 22 `npm test` passed all 30 tests. Mocked fixtures cover duplicate vs specialization, changed-to-changed and renamed/deleted skills, invalid evidence, missing key, injected instructions remaining data, context/body omissions, retry ceilings, hung request aborts, refusal/malformed/truncated output, safe rendering, and CLI exit/status behavior. `npm run validate` and `npm run check:skills` still pass 26 skills. Node syntax and owned diff-whitespace checks pass.
- [2026-10-08] No real credential, paid API request, external mutation, commit, or push was used. Mocked transport/schema fixtures validate implementation behavior; they do not evaluate live model quality or provide human policy/code signoff. Organization credential provisioning, service approval/budget, trusted workflow activation, live report usefulness, and human quality assessment remain explicitly deferred.
