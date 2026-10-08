---
id: 3
group: "migrate-remaining-skills"
dependencies: []
status: "completed"
created: 2026-10-08
skills: ["skill-authoring", "policy-review"]
complexity_score: 6
complexity_notes: "Bounded ownership and concrete integration acceptance keep this atomic; security and migration judgment require high effort."
execution_profile: "sol-high"
---
# Migrate remaining skills and review rubric

## Objective
Migrate the other thirteen public skills to requirements, portability and specific policy review boundaries.

## Skills Required
skill-authoring, policy-review. Invoke relevant installed skills; labels alone do not imply installed skill files.

## Acceptance Criteria
- [x] Each assigned skill has substantive Requirements and Safety and review sections and single-line valid metadata.
- [x] Fix SaaS discipline metadata while preserving secondary classifications as tags and flatten content where needed.
- [x] Review disclosure, data eligibility, originality, final human decisions and self-review in applicable writing, design, research and security-evaluation instructions.
- [x] Make reviewing-skills agent-neutral and describe automated advisory judgment without claiming completed human review.
- [x] Run advisory review on assigned skills and record per-skill evidence and unavailable runtime/services honestly.

## Technical Requirements
Follow plan 1 and its approved scope. Ownership: broken-link-report, hemingway-editor, humanizer, idea-crucible, issue-writing, lullabot-saas-security-review, nano-banana-prompt, pencil-designer, pull-request-description, resolve-composer-conflicts, reviewing-skills, seo-expert, slack-markdown-formatter and their companion files only; do not edit shared tooling, package files, dictionaries, workflows or README/AGENTS.

## Input Dependencies
The current repository and approved plan; no task dependencies.

## Output Artifacts
Owned changes above, task status and concrete verification evidence.

## Implementation Notes

<details>
<summary>Execution guidance</summary>

Apply skill-creator and reviewing-skills rubric like task 2. No raw AI policy; use plan summary/phrases. Some prose skills may have no external dependencies; say so explicitly. Public-source research does not authorize sending sensitive data to public models. Humanizer must not promise concealment or bypass appropriate disclosure. Changes need judgement, so this is not a rote Luna task.

Routing rationale: sol-high; required judgement means no task is assigned to the unavailable GPT-5.6 Luna. Each task uses a subagent. Read PRE_TASK_EXECUTION.md and apply meaningful red-green-refactor tests where appropriate. You share the codebase; do not revert others edits. Do not commit or push; orchestrator owns phase commits.

</details>

## Execution record

Started 2026-10-08. Applying skill-creator and the reviewing-skills rubric. This task edits workflow documentation and metadata; prose-mirroring tests would add no meaningful coverage. The workflow audit subsequently found implicit executable dependency installation in the SEO crawler; a behavioral regression test was added for that change with RED → GREEN evidence below.


Completed 2026-10-08. Skill names, version fields, and metadata dates were preserved. Only owned skill files/companions and this task record changed; no commit, push, external mutations, or prerequisite installation was performed. Used the approved public plan policy summary, not raw policy text. SaaS discipline is now the allowed scalar `development`, retaining administration/internal-operation context as tags. Humanizer retains all 28 patterns in a directly linked reference with a contents list, removing agent-specific allowed-tool names and preserving disclosures and supported facts.

### Executed checks

- `node scripts/validate-skills.js`: **pass**, 26 public skills, including scalar SaaS discipline.
- Called exported `checkSkill` for each of the 13 owned directories: **pass**, substantive Requirements / Safety and review and finite portability checks. Section presence does not prove policy compliance.
- Ran `node scripts/review-skill.js <skill-dir>` separately for every owned skill: **0 issues**. Remaining advisory suggestions: Nano Banana reference contents list (1); Pencil reference contents lists (2); Composer description trigger wording (1); SEO companion contents lists (10); Slack contents list and false Windows-path matches on intentional escape syntax (3). These are nonblocking and not claimed as human judgment passes.
- `python3 seo-expert/scripts/test_crawl_prerequisites.py`: **pass**, 1 behavioral test. RED confirmed the original wrapper invoked a stub installer when its virtual environment was missing; GREEN confirmed it now stops without calling installers or creating a venv. The fixture uses no network and stub commands cannot install packages. Normalized wrapper line endings to LF because CRLF otherwise fails Bash parsing before checking prerequisites.
- `python3 seo-expert/scripts/test_analyze_eeat.py`: **pass**, 37 existing tests.
- Python AST inspection: all owned Python companions parse. Bash syntax checks for all four SEO shell wrappers pass. Syntax checks do not execute their workflows.
- Executed five SEO HTML analyzers against synthetic local HTML from a temporary directory outside an agent installation layout: readability, BLUF, headings and meta extraction return 0; E-E-A-T returns the expected low-score advisory exit 1, without traceback. Executed `generate_crawl_report.py` and `compare_crawls.py` on local synthetic JSON: both return 0 and create temporary reports. All artifacts removed with the temporary workspace.
- Owned diff whitespace check: **pass**.

### Per-skill inspection and execution evidence

All rows include an end-to-end read of the skill definition, metadata inspection, and executed structural/disclosure/portability/advisory checks described above. Agent inspection is not human author self-review or domain approval.

| Skill | Inspected workflow and applicable safeguards | Actually executed / unavailable |
| --- | --- | --- |
| broken-link-report | Complete Python companion; local CSV→workbook flow, overwrite path, 403 manual verification, dependency install guidance, private URLs/tokens and output sharing | Python syntax only. `openpyxl` is absent; workbook generation not executed. No Screaming Frog crawl performed. |
| hemingway-editor | Prose-only editing, meaning/fact preservation, human editorial decisions, eligible draft environment and sales/marketing disclosures | Repository checks only; no external tool required. No actual publication or human editorial acceptance claimed. |
| humanizer | Complete pattern catalog and examples; disclosure preservation, supported facts/personal voice, optional public cliché highlighter | Repository checks only. Public highlighter not contacted; no authorship/detector claim or real deliverable publication. |
| idea-crucible | Full comparison/selection workflow, deterministic arithmetic for scores/budgets, human strategy/KPI decisions and domain review | Repository checks only; no external tool required. No real budget decision or arithmetic deliverable was requested. |
| issue-writing | Full workflow and source companion; issue labels/filing/uploads, private security channels, evidence sanitation and human self-review before submission | Repository checks only. No authenticated tracker write, reproduction environment, or attachment upload exercised. |
| lullabot-saas-security-review | Full report workflow/template; removed unverified blanket certification policy assertion, current source limits, intake minimization, honest AI marker and human Security Team decision | Repository checks only. Vendor research, linked internal evaluation guidance, procurement approval, trial installs and production consent not exercised or claimed verified. |
| nano-banana-prompt | Full workflow and style reference; replaced artist/studio/franchise imitation instructions with observable styles; human designer checks, eligible image/text transfers | Repository checks only. Gemini account/service generation or reference upload not exercised; service approval not asserted. |
| pencil-designer | Full workflow and both format/MCP companions; reconciled encrypted-file assertion with format docs, human scope review of batches/deletes/import/export/library conversion, designer/developer final review | Repository checks only. Pencil MCP/editor, Figma import, image generation, irreversible conversion and code export not exercised. |
| pull-request-description | Full workflow and source companion; actual code/test evidence, human author self-review before review request, proposed inline comments vs posting, uploads and disclosure | Repository checks only. No PR write, inline comment, attachment upload or target code runtime exercised. |
| resolve-composer-conflicts | Full merge/package-replay workflow; normal-merge `--theirs` boundary, local change preservation, plugin/script risk, validation and human result review before authorized commit | Repository checks only. No DDEV project/Composer package installation or real merge/commit exercised. |
| reviewing-skills | Full definition and source-pinned rubric; agent-neutral entrypoint, five approved API advisory areas, catalog comparison, incomplete coverage and human review distinction | Local deterministic checker executed. No Anthropic API/credentialed comment, rubric refresh or live model quality evaluation performed. |
| seo-expert | Full definition, shell wrappers, Python dependency/import/dataflow, report/template/ROI flow and relevant GEO references; bounded crawls, no implicit install, neutral report default/attribution, factual heuristic caveats and human strategy review | Behavioral test + 37 existing E-E-A-T tests + seven local synthetic CLI workflows executed. `markdown`, `reportlab`, and `openpyxl` absent; PDF rendering not executed. LibreCrawl checkout/tier configs absent; live crawler, Lighthouse/Chrome/network audits not exercised. Numerical GEO claims were not revalidated and must not be presented as current evidence. |
| slack-markdown-formatter | Full definition/reference; human recipient/mention/test-message review, private preview eligibility, reconciled API link syntax with official Slack formatting documentation (public read only) | Repository checks and read-only official documentation retrieval. No Slack credentialed preview/message/file mutation or notification performed. |

### Review limits

No automated result certifies actual human review, absence of private information, vendor/tool approval, current numerical SEO claims, or live service correctness. Qualified human code/domain/policy review and applicable client disclosure decisions remain outstanding responsibilities. External execution is unnecessary for this bounded migration and was not simulated as completed. Root verification covers final phase acceptance and commits.
