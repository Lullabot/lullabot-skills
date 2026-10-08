# Public skill migration evidence

Verified on 2026-10-08 for all 26 public skills. This record consolidates the
operational and remaining-skill migration task records and final repository
checks. Inspection means an agent read the instructions, metadata and relevant
companions against the approved public requirements and policy summary. It does
not mean a human approved the work, a service ran successfully, or a tool is
approved for actual client data.

Every public skill passes structural validation and substantive Requirements /
Safety and review / finite portability checks. Names, purposes, triggers, metadata
dates and versions were preserved. Required safety/portability behavior was
updated, and the SaaS discipline was corrected. Companion locations are resolved from
the loaded skill independently of the project or agent installation directory.

## Per-skill evidence

The harmless executions below were performed during migration; the selected
companion regression tests also run in the separate read-only CI test job.
Syntax checks establish parsing only. Service-dependent cases were inspected and
are listed as unavailable rather than represented as successful runs.

| Skill | Instructions and companions inspected | Actually exercised | Unavailable or intentionally not executed |
| --- | --- | --- | --- |
| broken-link-report | Complete CSV-to-workbook companion, output paths, manual 403 review and private URL handling | Python syntax | Workbook generation: openpyxl absent; no live crawl |
| cloudflare-tunnel | Bash helper, public exposure, credential/configuration preservation, installation and URL sharing gates | Bash syntax; cloudflared version; helper usage from a temporary neutral installation outside a synthetic project | No login, tunnel creation, installation or public exposure |
| content-inventory | Both pipelines; normalization, readability, file/output/redirect modules; CSV checker; three references | Python syntax; checker help; four valid synthetic CSV exports accepted, invalid pages export rejected | pandas/openpyxl absent; no workbook generation or live redirect retrieval |
| data-dict-extractor | Extractor, YAML inputs, workbook/sheet generation and project-relative outputs | Python syntax | openpyxl absent; no workbook generation or live Drupal access |
| ddev-xhgui-analyze | SQL/export/PHP/report workflow, read-only credentials and confidential profiles | DDEV version | Docker access denied; no project, database/profile export or analysis run |
| drupal-demo-recorder | Overlay JS/config, bootstrap/transcode/frame helpers, check/apply boundaries and verified container paths | Bash/JS syntax; bootstrap help; mock DDEV missing-tool check with no filesystem changes | Docker unavailable; no install, restart, browser recording, ffmpeg or video run |
| drupal-security-review | Methodology, recon/cleanup PHP, UI/CLI references, isolated reproduction and exact-manifest cleanup | PHP lint; four synthetic cleanup tests for preview, exact ID, label mismatch and protected user | No Drupal bootstrap, live recon, exploit or cleanup; Docker unavailable |
| github-attachments | Upload routes/helper, persistent public URLs, redaction, permissions and upload/post gates | Bash syntax; GitHub CLI version | No upload, posting, live authentication or destination-permission verification |
| github-wiki | Wiki workflow/Gollum reference, reviewed staging, remote/branch and publication checks | Git version; command/link inspection | No supplied wiki remote/authentication; no clone, push or live rendering |
| gws-cli | Google mail/calendar/drive/sheets operations, data eligibility, scope/pagination and mutation gates | CLI availability check: gws absent | No authentication, reads, sends, drafts, uploads, scheduling or sharing |
| hemingway-editor | Meaning/facts, editorial decisions, eligible drafts and applicable disclosures | Repository checks | No actual publication or human editorial acceptance |
| htmx-expert | Attribute/event/security/config guidance, extracted server and practical-pattern reference | Helper help; Python syntax; two local tests for loopback content/fragments and invalid directory | No production/backend/deployment verification |
| humanizer | All 28 patterns/examples, factual voice and disclosure preservation | Repository checks | Public highlighter not contacted; no authorship claim or publication |
| idea-crucible | Comparison/selection, deterministic arithmetic and human strategy/domain decisions | Repository checks | No actual budget decision or requested arithmetic deliverable |
| improve-test-quality | Phased workflow, analyzer and both READMEs, installed-tool and local test-edit scope | JS syntax; analyzer invoked by absolute skill path from a temporary synthetic project, expected 50 score | No installed Stryker/project test harness; no mutation run |
| issue-writing | Source reference, filing/uploads, private security channels and review gates | Repository checks | No authenticated tracker write, reproduction environment or upload |
| lullabot-saas-security-review | Report template, vendor-source limits, intake minimization and human security/procurement decisions | Repository checks; discipline changed to valid scalar development with context preserved in tags | No vendor research, private evaluation documents, procurement approval, trial install or production consent |
| nano-banana-prompt | Style reference and image/text transfer, observable style descriptions and designer review | Repository checks | No Gemini account, generation or upload; tool approval not asserted |
| pencil-designer | Format/MCP references and batch/delete/import/export/library scope, final designer/developer review | Repository checks | No editor/MCP, Figma import, image generation, irreversible conversion or code export |
| pull-request-description | Source reference, actual test evidence, inline-comment proposals, uploads and self-review | Repository checks | No PR write, comment posting, attachment upload or target-code runtime |
| refresh | Survey/discard/default-branch/worktree/submodule/failure flow and exact destructive scope | Git version; command semantics inspection | No destructive refresh, remote fetch, checkout, cleanup or submodule update |
| resolve-composer-conflicts | Package replay, merge-side semantics, local preservation and plugin/script risks | Repository checks | No real merge, dependency installation, DDEV project or commit |
| reviewing-skills | Definition, pinned upstream rubric, five advisory categories, catalog and incomplete-coverage limits | Local deterministic advisory checker | No paid API review, credentialed comment, rubric refresh or live model quality assessment |
| seo-expert | Shell/Python dataflow, templates/references, bounded crawls, reviewed prerequisite setup and estimate caveats | Python/Bash syntax; crawler prerequisite guard; 37 E-E-A-T tests; five HTML analyzers and two JSON report/comparison workflows on synthetic inputs | markdown/reportlab/openpyxl absent for PDF flow; no LibreCrawl/tier config, Lighthouse/Chrome/network audit; numerical GEO claims not revalidated |
| slack-markdown-formatter | Full formatting reference, recipient/mention/privacy gates and API link syntax | Repository checks; read-only official Slack documentation retrieval | No credentialed preview, message/file mutation or notification |
| tugboat-cli | Lifecycle/config/reference, grants, shell and extracted upload helper with preview/no-clobber defaults | Python syntax/help; three local tests for quoted binary upload, no-clobber/injection prevention, relative paths and no API call in preview | Tugboat CLI absent; no live token, preview, config or upload |

## Final local checks and compatibility

- `npm test`: 44 Node.js tests passed on Node 24.21.0. These test structure,
  disclosure, portability, spelling behavior, advisory response handling, trusted
  provenance, bounded input, stale suppression and sticky-comment handling using
  fixtures and mocks. GitHub Actions also passed all 44 Node tests and 47 selected companion tests on
  Node 22.23.3 in PR #45. The repository requires Node 22.18 or later.
- `npm run validate`: 26 public skills passed.
- `npm run check:skills`: 26 public skills passed.
- `npm run spellcheck`: the full configured scope passes. Code fences remain
  checked. Dictionary additions were reviewed in source context and grouped by
  rationale; the actual spelling correction and intentionally invalid Slack
  example were edited directly.
- The orchestrator and CI task verified 47 selected offline Python/PHP companion
  tests: htmx 2, Tugboat 3, Drupal cleanup 4, SEO E-E-A-T 37 and crawler guard 1.
  No live services or skill dependency installation were needed. Migration task 3
  separately recorded its 38 SEO tests and seven synthetic CLI workflows.
- The final advisory authoring run reported zero issues and 17 advisory
  suggestions. Reference contents lists, description wording and intentional
  Slack escape syntax remain advisory; this is not a human quality pass.
- The CI task verified workflow YAML and actionlint. The orchestrator verified
  reproducible lockfile installation with npm ci --ignore-scripts on Node 22.
- The orchestrator loaded and rendered all 26 current skills using the sibling
  prompt-library generator's readSkill/buildPageContent functions in an isolated
  copy with trusted js-yaml 4.1.1 and gray-matter 4.0.3. This checks parser/page
  compatibility. No sibling files were edited; a full site build or deployment
  was not performed.
- `git diff --check` passes. No new wording-matching tests were added for spelling
  cleanup or this evidence document; existing checker tests cover real spelling
  rejection and approved-term acceptance.

## Deliberate scope and limits

CSpell covers public skill Markdown/metadata, first-party companion documentation,
contributor Markdown and text, including code examples. Its extension scope omits
binary/code outputs; ignored generated output remains ignored. The dependency
folder, Git internals, hidden installed development tooling and the pinned external
upstream rubric are explicitly excluded in cspell.json. No whole first-party
skill or code-fence exemption was added. Literal codec, API, schema, flag, example
identifier and proper-name spellings are accepted as exact reviewed terms; this
acceptance does not verify factual assertions in examples.

All five model categories and failure/provenance paths were checked with mocks.
No paid Anthropic call or live model quality assessment was performed. GitHub
secret and fork-policy inspection was unavailable because the read-only attempt
was denied; private settings are unverified rather than assumed absent.

The trusted workflow_run reporter starts only after its workflow reaches the
default branch. Actual service activation, PR-template UI presentation, fork events,
team membership/access/notifications, required statuses and native code-owner
approval need post-merge administrator verification. Fork advisory review also
requires the administrator's SKILL_REVIEW_FORK_APPROVAL_VERIFIED attestation.
Live provisioning, approval and budget are deferred. Passing these checks does
not establish actual human author review, qualified code/domain approval, privacy,
tool approval, client consent, appropriate disclosure or policy compliance.

## PR and execution evidence

The implementation at `5cedbdd` passed all five reported PR checks: Skill structure,
Skill disclosure and portability, Skill spelling, Skill tests, and Advisory
mechanical authoring review. The source run is [Skill validation](https://github.com/Lullabot/lullabot-skills/actions/runs/37831052929).

Strikethroo attempted its independent review gate once. The configured read-only
Claude harness could not write the temporary readiness file, and the other
external harnesses were unavailable. The gate returned `action: continue`, with a
failed review result and no certified findings. This is not a clean independent
review. The complete result is recorded in the archived plan execution summary.
