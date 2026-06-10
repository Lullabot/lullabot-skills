---
name: drupal-security-review
description: Deep security review of a Drupal site's CUSTOM code (modules + theme) running under DDEV, followed by recorded exploit-demonstration videos produced with the Playwright Agent CLI (playwright-cli) via the e0ipso/ddev-playwright-cli add-on. Use when the user wants to audit a DDEV Drupal codebase for vulnerabilities AND get reproducible video proofs-of-concept, especially on projects that do NOT already have a Playwright test harness. Not for diff-only PR review (use the built-in /security-review for that).
---

# drupal-security-review

Run a thorough security review of a Drupal project's custom code, then *prove*
each finding by driving a real browser with `playwright-cli` and recording a
video. Recording the exploit is treated as adversarial verification: it
routinely changes a finding's severity — usually **down** (the payload turns
out to be plantable only by an administrator), occasionally **up** (something
believed admin-only is reachable by a semi-trusted user). Surface every change,
and call out **upgrades loudly**.

**Always record every finding, regardless of severity — and never ask first.**
The video and reproduction scenario are how we validate findings and detect
severity changes, so they are produced for *all* findings (High, Medium, Low,
hardening) **and** for the refuted candidates — a recording that demonstrates a
candidate is genuinely unreachable is itself the evidence of refutation. Do
**not** ask the user whether to record a given finding, skip low-severity ones,
or seek confirmation before producing the videos: just create all of them.

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
- `scripts/cleanup.php` — deletes everything this skill planted (content/blocks
  whose title/label contains the marker, and the throwaway test users).

Copy a helper into the project root before running it, because `ddev drush
php:script` resolves paths inside the web container:
`cp ~/.claude/skills/drupal-security-review/scripts/recon.php ./.sec_recon.php && ddev drush php:script .sec_recon.php`

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

### Phase 1 — Deep multi-agent review
Follow `references/review-methodology.md`. Fan out along **two axes** (hybrid):
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

### Phase 2 — Prepare the demo environment
1. Ensure the add-on: if `ddev exec playwright-cli --version` fails, install it
   with `ddev add-on get e0ipso/ddev-playwright-cli && ddev restart`.
2. Create the throwaway test users the demos need — one per distinct role that
   appears in a reproduction recipe (e.g. an editor-role user). Use a clear
   marker in the name (e.g. `secdemo_<role>`). See the UI-automation reference
   for login.
3. Heed the DB-reset caveat in the UI-automation reference: do **not** run the
   project's own own test suite during the demos.

### Phase 3 — Demonstrate every finding (full path) with video
Demo **every finding, full creation→trigger path — regardless of severity and
without asking the user.** This includes High/Medium findings, Low/hardening
findings, *and* the refuted candidates: record one video per candidate so each is
independently validated on camera. For a finding you expect to be unreachable,
still record the attempt — the video that shows the access system blocking the
actor is the proof of refutation and may instead reveal a path you missed. Never
gate a recording on severity, and never pause to ask whether to make it. For
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
1. Deliver: the updated `security-review-custom-code.md`, the videos (send mp4s
   with `SendUserFile`), and the severity-change summary.
2. Run `scripts/cleanup.php` to remove planted content and test users; scrub any
   one-time login tokens from working files.
3. Ask before deleting the review doc, videos, or any recording harness — these
   are the deliverables.

## Guardrails
- Record everything, never ask: produce a video and reproduction scenario for
  every finding and every refuted candidate at all severities, without pausing to
  ask the user whether to record any of them. The only "ask" in this skill is the
  Phase-5 confirmation before *deleting* the finished deliverables.
- Authorized review only. This runs against the user's own local DDEV site.
- Use a visibly-defacing but non-destructive payload (overlay/`document.title`),
  never anything that exfiltrates or persists beyond the planted node/block.
- Generic first: derive roles, content types, login, and quirks from recon and
  the live forms — never assume another project matches this one.
