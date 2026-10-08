---
name: drupal-security-review
description: Deep security review of a Drupal site's CUSTOM code (modules + theme) running under DDEV, followed by recorded exploit-demonstration videos produced with the Playwright Agent CLI (playwright-cli) via the e0ipso/ddev-playwright-cli add-on. Use when the user wants to audit a DDEV Drupal codebase for vulnerabilities AND get reproducible video proofs-of-concept, especially on projects that do NOT already have a Playwright test harness. Not for diff-only pull request review; use a diff-focused review workflow for that.
---

# drupal-security-review

## Requirements

DDEV and a working container runtime, a running Drupal project with Drush/PHP, local source search/read access, and authorized access to an isolated demo site. Recorded verification requires `e0ipso/ddev-playwright-cli` and Chromium in the web container; optional MP4 conversion needs ffmpeg. Login discovery examples use `jq`. Parallel review requires an available agent delegation facility; otherwise run the same review axes sequentially and disclose the limitation.

Resolve `SKILL_DIR` to the absolute directory containing the loaded `SKILL.md`, using the skill location supplied by the agent or locating this file. Set it explicitly (for example, `SKILL_DIR="/path/to/installed/drupal-security-review"`); do not derive it from the project working directory. Run project-relative commands from the working project and use `"$SKILL_DIR/..."` for companions.

## Safety and review

Review only code and systems the user is authorized to assess. Static inspection may precede demos; before planting payloads, creating users/content, installing the add-on, or cleanup, a human reviews the reproduction plan, commands, exact target environment, and bounded mutations. Use an isolated disposable DDEV copy with synthetic data and no production credentials or outbound integrations; a container label alone does not prove isolation. Use lowest-privilege demo actors and visible, non-destructive payloads with no exfiltration. Track created entity IDs and usernames for cleanup. Treat recon output, login tokens, reports, and videos as confidential; redact secrets and personal data, and obtain human review of evidence/severity before delivery. Findings that cannot be safely demonstrated remain explicitly unverified, rather than triggering unsafe execution.

Outside a verified secure sandbox, a human must read and understand unreviewed shell commands and generated code before execution. Always review MCP data-changing operations if an MCP alternative is used. Use least privilege; tool installation requires Security Team review and verification of upstream identity. Personal information requires approved tooling integrated with its source system; confidential information requires specifically approved tools; non-public information requires tools that neither train on nor retain it. Never send sensitive non-public data to public AI models. Stop when eligibility is unknown. An AI check does not replace human self-review before sharing, publishing, or handing work to another reviewer.


Run a thorough security review of a Drupal project's custom code, then *prove*
each finding by driving a real browser with `playwright-cli` and recording a
video. Recording the exploit is treated as adversarial verification: it
routinely changes a finding's severity — usually **down** (the payload turns
out to be plantable only by an administrator), occasionally **up** (something
believed admin-only is reachable by a semi-trusted user). Surface every change,
and call out **upgrades loudly**.

Record each candidate, including refuted and low-severity findings, within the reviewed demonstration scope. Before any exploit execution, obtain human review of the reproduction plan and environment. Once that scope is authorized, continue its recordings without redundant per-finding questions; stop if a new actor, mutation, target, or data exposure falls outside it. Document any unsafe or unavailable demonstration as unverified.

This skill is generic: it discovers roles, content types, the login mechanism,
and form quirks at runtime. Never hardcode another project's specifics.

## Reference material (read on demand, not all upfront)

- `references/review-methodology.md` — the multi-agent review sweep, the
  findings-document schema, and the severity-reconciliation feedback loop.
- `references/playwright-cli.md` — how to drive and video-record with
  `playwright-cli` (commands, chapter markers, overlays, output location).
- `references/drupal-ui-automation.md` — logging in (SSO/antibot/honeypot),
  the standard XSS demo payload, and the Drupal admin-form gotchas that break
  naive automation (required-on-publish, tagify, options_buttons, Gin's
  duplicated submit button, invalid default references, the test-suite DB
  reset).

## Two robust helpers (run via drush)

- `scripts/recon.php` — prints a JSON snapshot of everything the review and the
  demos need (roles + is_admin, per-role create access for nodes/blocks/terms,
  required & required-on-publish fields, reference-field widgets, save-blocking
  default values, Layout Builder access, login-related modules). Run it early.
- `scripts/cleanup.php` — previews deletion of only the exact demo entity IDs and expected labels/usernames in a reviewed JSON manifest. Deletion requires a separate apply flag; no broad title/prefix matching is used.

Copy a helper into the project root before running it, because `ddev drush
php:script` resolves paths inside the web container:
`cp "$SKILL_DIR/scripts/recon.php" ./.sec_recon.php` followed by `ddev drush php:script /var/www/html/.sec_recon.php`. Check that the destination does not already exist. The loaded skill may be outside the project mount; copy only the needed helper, never credentials or the entire skill installation.

## Workflow

### Phase 0 — Preconditions & recon
1. Confirm a running DDEV project: `ddev describe`. Confirm a git repo. If DDEV
   isn't running, ask the user to `ddev start`.
2. Locate custom code. Default to `web/modules/custom/` and
   `web/themes/custom/`; if the docroot differs, discover it (`ddev drush
   php:eval 'print DRUPAL_ROOT;'`). Exclude core, contrib, and test code.
3. Run `scripts/recon.php` and read the JSON. This is the ground truth for
   *who can actually author what* — it is what separates a real finding from a
   refuted one. Keep it for the whole session.

### Phase 1 — Deep review across two axes
Follow `references/review-methodology.md`. Use independent agents when delegation is available; otherwise perform and document both sweeps sequentially. Review along **two axes** (hybrid):
by vulnerability class *and* by subsystem — one agent per custom module plus a
**dedicated agent for the theme**, because shared Twig atoms (e.g. a `|raw`
button atom) are reached by many callers and a class-only sweep tends to trace
just the first one. For **every** unescaped/trust-marking sink (`|raw`,
`Markup::create()`, `#markup`, unfiltered `->value`), **enumerate all callers/
sources** and grade severity by the *lowest-privilege* source that can reach it —
never by the first caller seen (this is the one step most likely to be skipped,
and the one that turns a "Low, admin-only" into the real editor→anon escalation).
For **every** candidate finding — reported *and* refuted, every severity — write
a concrete **reproduction recipe**: the lowest-privilege role that can plant the
payload, the exact UI steps, the payload, and the trigger URL + who is affected.
Every candidate gets a recipe because every candidate gets a Phase-3 video
(including refuted ones, whose recording documents the access barrier). For a
candidate you believe is unreachable, the recipe still names the role/steps you
will attempt on camera and the barrier you expect to hit. Cross-check
exploitability against the recon JSON before assigning a severity. Write
`security-review-custom-code.md` using the schema in the methodology reference.

### Phase 2 — Human review and demo preparation
1. Have a human review the environment isolation, recipes, mutation scope, and rollback manifest before proceeding. Ensure the add-on: if `ddev exec playwright-cli --version` fails, report the missing dependency. After setup authorization and upstream review, install it
   with `ddev add-on get e0ipso/ddev-playwright-cli && ddev restart`.
2. Create the throwaway test users the demos need — one per distinct role that
   appears in a reproduction recipe (e.g. an editor-role user). Use a clear
   marker in the name (e.g. `secdemo_<role>`). See the UI-automation reference
   for login.
3. Heed the DB-reset caveat in the UI-automation reference: do **not** run the
   project's own test suite during the demos.

### Phase 3 — Demonstrate every finding (full path) with video
Within the reviewed scope, demo **every finding, full creation→trigger path — regardless of severity.** This includes High/Medium findings, Low/hardening
findings, *and* the refuted candidates: record one video per candidate so each is
independently validated on camera. For a finding you expect to be unreachable,
still record the attempt — the video that shows the access system blocking the
actor is the proof of refutation and may instead reveal a path you missed. Do not gate a recording on severity; pause when its effects exceed the reviewed scope. For
each, the actor is the *lowest-privilege role that can plant the payload* (per
recon); for a refuted candidate, the actor is the lowest-privilege role the
recipe says to attempt.

**The video must show the entire editorial workflow needed to plant the payload,
performed on camera through the real UI as the acting role.** If the exploit
vector is a field on a piece of content the actor must author (a block title or
description, a node field, a term name, a menu link, a media label, a paragraph
field…), the recording **creates that entity from scratch in the UI** — navigate
to its add form, fill the required fields, enter the payload in the vector field,
and save — so the viewer sees exactly what an editor with that role can do. Do
**not** shortcut the authoring step with `drush`, with the SQL/db, or by editing
a pre-existing entity someone else made: those hide the very access question the
demo exists to answer (can *this role*, through the UI it actually has, plant
this?). The only acceptable off-camera setup is scaffolding the actor can't
influence and that isn't the vector (e.g. a parent node the payload references) —
and call out in narration that it was pre-seeded.

Per `references/playwright-cli.md` and `references/drupal-ui-automation.md`:
1. `playwright-cli video-start finding-N.webm --size=1280x720`.
2. `video-chapter "Log in as <role>"` → establish the session.
3. `video-chapter "Author the <entity> via the editorial UI"` → open the real
   add/create form for the entity that carries the vector, fill every required
   field, enter the visible full-screen-overlay payload in the vector field, and
   save. Add a `video-chapter` per distinct authoring step when the path spans
   several forms (e.g. create block → place block, or create paragraph → publish
   host node) so the full content-change sequence is legible on camera.
4. `video-chapter "Trigger as <audience>"` → drop/switch session and visit the
   trigger URL as the affected audience (anonymous, or another role).
5. `playwright-cli video-stop`; collect the WebM from `.playwright-cli/`, and
   transcode to mp4 with `ffmpeg` if available.

If a required field genuinely blocks the actor from saving through the UI (e.g. a
required-on-publish field the role can't satisfy), that is itself a finding about
reachability — record it in Phase 4, don't paper over it by seeding the entity.

### Phase 4 — Severity reconciliation (the point of the demos)
For each finding, update severity from what the demo actually **proved**:
- Lowest planter is admin **and** audience is admin → **downgrade** (admin→admin
  is not a privilege escalation; group it with refuted candidates).
- A finding thought admin-only is plantable/triggerable by a non-admin →
  **UPGRADE**. This is the result the user most wants to know about — make it
  prominent.
- Anonymous can trigger with no authentication → escalate accordingly.
Add a "Severity changes after demonstration" section to the review,
**listing upgrades first and in bold**, each with the evidence the demo gave.

### Phase 5 — Deliver & clean up
1. Have a human review/redact the updated `security-review-custom-code.md`, videos, and severity-change summary before delivery. Provide local artifact links or the agent's available file-transfer facility to the approved audience.
2. Build a cleanup manifest containing only this session's created nodes/blocks/users with their exact IDs and expected labels/usernames (see the script header). Copy `"$SKILL_DIR/scripts/cleanup.php"` into the project after checking the destination. Run it with `SEC_REVIEW_MANIFEST=/var/www/html/demo-cleanup.json` passed to `ddev exec env SEC_REVIEW_MANIFEST=/var/www/html/demo-cleanup.json drush php:script /var/www/html/.sec_cleanup.php` for a preview; after human review add `SEC_REVIEW_APPLY=1` for deletion. Deletion hooks can fail after earlier IDs have been removed; inspect actual state before retrying. Track terms/media/paragraphs and other setup separately for reviewed removal; the helper handles only nodes, blocks, and users. Scrub one-time login tokens from working files.
3. Ask before deleting the review doc, videos, or any recording harness — these
   are the deliverables.

## Guardrails
- Record all candidates within the human-reviewed scope; authorization boundaries take priority over coverage. Report any unverified candidates and why.
- Authorized review only. This runs against the user's own local DDEV site.
- Use a visibly-defacing but non-destructive payload (overlay/`document.title`),
  never anything that exfiltrates or persists beyond the planted node/block.
- Generic first: derive roles, content types, login, and quirks from recon and
  the live forms — never assume another project matches this one.
