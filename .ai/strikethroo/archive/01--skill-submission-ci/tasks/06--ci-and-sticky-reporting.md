---
id: 6
group: "ci-and-sticky-reporting"
dependencies: [1, 4, 5]
status: "completed"
created: 2026-10-08
skills: ["github-actions", "secure-coding"]
complexity_score: 7
complexity_notes: "Bounded ownership and concrete integration acceptance keep this atomic; security and migration judgment require high effort."
execution_profile: "sol-high"
---
# Integrate required CI and trusted sticky reporting

## Objective
Wire deterministic full-bundle CI and trusted Anthropic reporting, keeping forks unprivileged and model failure advisory.

## Skills Required
github-actions, secure-coding. Invoke relevant installed skills; labels alone do not imply installed skill files.

## Acceptance Criteria
- [x] Required stable structure, disclosure/portability, spelling and meaningful test jobs run on all PRs with read-only permissions and no model secrets.
- [x] Trusted workflow_run reporter executes base/default-branch code and validates originating workflow identity, repo, PR, source run, exact snapshot and eligibility before using key/write token.
- [x] Never execute/install/import PR code or trust fork artifacts as provenance; fetch contents as bounded data. Do not use pull_request_target.
- [x] Combine mechanical and all five model findings into one sticky comment, bot-owned marker verification, head/base/model and clear unavailable/coverage status.
- [x] Suppress stale reports and coordinate races with one reporting authority; forks require configured maintainer approval, key never enters fork jobs.
- [x] node --test scripts/tests/pr-review-report.test.js proves rejection of forged run association/stale snapshots and update behavior; parse workflow YAML and ensure fixture/service failures do not gate merges.

## Technical Requirements
Follow plan 1 and its approved scope. Ownership: .github/workflows/skill-validation.yml, .github/workflows/skill-review.yml, .github/workflows/skill-review-report.yml, scripts/pr-review-report.js, scripts/tests/pr-review-report.test.js; coordinate exact workflow names and CLI with task 4.

## Input Dependencies
Task outputs: 1, 4, 5

## Output Artifacts
Owned changes above, task status and concrete verification evidence.

## Implementation Notes

<details>
<summary>Execution guidance</summary>

Score 7 retained because provenance, runner trust and reporting are one security boundary; splitting provenance from its publisher would hide critical acceptance tests. Use red-green-refactor for provenance and stale-report logic. Trusted workflows only run after landing on default branch; report this activation limit honestly on PR45 and validate statically/mocked now. Manual maintainer dispatch on default branch may be available later but do not falsely claim this PR ran new workflow_run service. No secrets needed by required jobs. Keep release dispatch unchanged. Data-only GitHub API snapshots use trusted base code; never checkout PR then npm ci with secrets. Expect tests to simulate GitHub API and report posting without real mutations.

Routing rationale: sol-high; required judgement means no task is assigned to the unavailable GPT-5.6 Luna. Each task uses a subagent. Read PRE_TASK_EXECUTION.md and apply meaningful red-green-refactor tests where appropriate. You share the codebase; do not revert others edits. Do not commit or push; orchestrator owns phase commits.

</details>

## Execution evidence — 2026-10-08

Implemented `Skill validation` with four stable required job names: `Skill structure`, `Skill disclosure and portability`, `Skill spelling`, and `Skill tests`. Every PR runs these jobs without path filtering, model credentials, or write permissions. Node 22 and the pinned repository lockfile are used with `npm ci --ignore-scripts`. The separate mechanical authoring job remains advisory and read-only. The existing release notification workflow was not edited.

The privileged reporter checks out the trusted default-branch workflow event commit (`github.sha`) and installs only that commit's lockfile. It receives no PR artifact, dependency cache, checkout, executable import, or submitted program. It re-fetches canonical workflow identity and the live source run, verifies repository IDs/names, workflow ID/path/name, pull-request event, completed success/failure, attempt, exact head/base, public-data eligibility, and latest run before publishing. Immutable commit/tree/blob API responses supply bounded inert data. GitHub `removed` changes map to `deleted`; symlinks are omitted rather than followed. Empty genuine-fork associations recover through the exact-head commit-associated PR API and require one unambiguous matching repository/head association.

One serialized reporting authority combines trusted mechanical findings and all five model areas in the legacy sticky marker. Both marker and exact Actions-bot identity are required before editing a comment. Head/base/run freshness is rechecked before writes, with newer sticky metadata suppressing older reports. GitHub does not provide an atomic PR-head-and-comment conditional write; serialization and final live checks reduce that residual race without claiming transactional guarantees. Missing credentials, API/snapshot/model/rendering errors remain explicit advisory states. Unexpected model or rendering failures preserve already-computed mechanical findings; public rendering redacts obvious private assignments and does not reproduce submitted source bodies or provider error details.

Administrator activation is deferred: repository variable `SKILL_REVIEW_FORK_APPROVAL_VERIFIED=true` must attest that an administrator verified the configured fork-workflow approval policy covers the intended outside contributors. It is not evidence of an individual run's human approval. Without this flag, privileged fork review fails closed, even for a completed successful run. No administrator settings, secrets, real model calls, or GitHub comment mutations were performed. The new `workflow_run` workflow cannot run until it reaches the default branch; actual post-merge activation, model access, fork-policy configuration, and real fork events remain unverified here. The parent inspected a read-only existing source-run response to establish nested association repository IDs (which lack `full_name`); this task tests that shape and the empty-fork fallback with mocks.

Red/green evidence: the reporter test initially failed for the missing implementation; later a regression test demonstrated that a thrown model request discarded valid mechanical findings. After separation of collection/mechanical and model failure handling, all 13 reporter tests pass. Cases cover missing API credentials; canonical workflow and nested repository IDs; empty fork fallback and missing approval-policy attestation; forged repository/workflow/path/event/status/head/base/private eligibility; ambiguous or unrelated associations; stale head/base/rerun/newer-run suppression; foreign/human marker protection; legacy bot comment updates and newer sticky ownership; all five areas in one comment; symlink/oversized-body omissions; model/render failure preservation and private-value redaction; and request-count/byte/status limits without response leakage.

Actual local checks:

- `node --test scripts/tests/pr-review-report.test.js`: 13 passed, no network/model writes.
- `npm test`: all 44 repository Node tests passed on local Node 24.21.0; Node 22 is specified for CI but was not separately executed locally.
- `npm run validate` and `npm run check:skills`: all 26 skills passed.
- The exact CI-selected Python commands passed 47 tests: htmx 2, Tugboat 3, Drupal cleanup 4 with installed PHP, E-E-A-T 37, crawler prerequisite guard 1. Tests use synthetic local inputs, do not contact live services, and do not install skill dependencies. Explicit SEO discovery patterns avoid unavailable PDF dependencies.
- Trusted YAML parser accepted all three owned workflows; `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.12` on those workflows exited 0.
- `npm run spellcheck` ran and reported 350 terminology issues across 52 files. Dictionary cleanup belongs to task 7; no spelling success is claimed at this task's completion. The required spelling job is wired and will fail until that separate cleanup lands.

Primary API/event contracts consulted: [commit-associated pull requests](https://docs.github.com/en/rest/commits/commits#list-pull-requests-associated-with-a-commit), [workflow_run](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run), [get workflow run](https://docs.github.com/en/rest/actions/workflow-runs#get-a-workflow-run), and [Git trees](https://docs.github.com/en/rest/git/trees#get-a-tree). No claims rely on environment/deployment approval history as proof of fork-run approval.
