# Review methodology, findings schema, and the demo feedback loop

## Scope

All custom code under the project's custom module and theme dirs (default
`web/modules/custom/`, `web/themes/custom/`). Exclude Drupal core, contrib
modules, and test code — they are out of scope and reviewed upstream.

## Deep multi-agent sweep

Fan out independent reviewers along **two axes**, then verify each candidate
adversarially. If the `Workflow` tool is available, use it (pipeline: find →
adversarially verify each finding); otherwise spawn parallel `Agent` subagents
and a verification pass.

**Axis 1 — by vulnerability class** (the six classes below). Good at applying a
consistent sink taxonomy across the whole codebase.

**Axis 2 — by subsystem** (one agent per custom module, plus a dedicated agent
for *the theme on its own*). Good at exhaustively tracing data-flow and *caller
graphs within a subsystem* — which class-based agents, spread thin across all
modules + theme, tend to skip.

Run **both** axes (hybrid). Neither alone is sufficient: a real review missed an
editor→anonymous stored XSS because a single per-class XSS agent found the shared
`|raw` Twig atom (`button.twig`) but traced only its first, admin-only caller and
never enumerated the ~13 other callers — one of which (`results-teaser.twig` →
`button_content: topic.title`) was editor-reachable. A theme-dedicated agent,
whose natural job is component composition (which template embeds which atom and
what it passes in), surfaces exactly that caller graph. Give the theme its own
agent for this reason. The vulnerability classes (Axis 1):

1. **XSS** — `|raw` / `|safe_join` in Twig, `Markup::create()`, `#markup`,
   `->value` of plain-text/formatted fields rendered without escaping,
   `t()` with unsanitised args, `TrustedCallback`/inline JS with user data.
2. **Access control** — `accessCheck(FALSE)` on entity queries, missing
   `->access()` checks in preprocess/controllers, route `_access: 'TRUE'`,
   `bypass`-style perms, IEF/entity-browser bundle access, unpublished-entity
   leaks.
3. **Injection** — raw `\Drupal::database()->query()` with concatenation,
   `db_query` string building, dynamic `\Drupal::service()` ids, `unserialize`
   of user data, path/file operations with user input.
4. **CSRF / SSRF** — state-changing GET routes without `_csrf_token`, custom
   forms skipping form tokens, `\Drupal::httpClient()` / `file_get_contents` to
   user-controlled URLs.
5. **RCE / secrets** — `eval`/`assert`/`\\Drupal::service` from input,
   `exec`/`shell_exec`/`proc_open`, hardcoded keys/tokens/passwords in code or
   config, debug backdoors.
6. **Data exposure** — verbose errors, secrets in logs/responses, PII in
   render arrays/JSON, overly broad serializer/REST/JSON:API exposure.

Each reviewer cites `file:line` and explains the data flow. Each candidate then
gets **three** adversarial checks: one tracing the code path, one assessing
real-world exploitability **against the recon facts** (who can author the
content? is the surface reachable? is the data already public?), and one
**caller-graph completeness** check (below).

## Complete the sink's source set — grade by the lowest-privilege source

This is mandatory and is the step most likely to be skipped. When you find an
**unescaped or trust-marking sink** — a `|raw` Twig variable (especially in a
shared atom/molecule), `Markup::create()`, `#markup`, `FormattableMarkup`, a
`->value` printed without filtering — **do not stop at the first caller**. The
severity of a shared sink is set by the *lowest-privilege source that can reach
it*, not by the first one you happen to trace.

1. Enumerate **every** source feeding the sink:
   - For a Twig component variable, grep every `include`/`embed`/`{{ ... }}` that
     passes that variable (e.g. `grep -rn 'button_content' …`), across atoms,
     molecules, organisms, *and* node/field/view templates.
   - For a PHP sink, grep every assignment/caller of the variable and every code
     path that reaches it.
2. For each source, identify what controls it (a node title? a link-field title?
   admin-only config? a plain-text vs. format-filtered field?) and which role can
   set it — cross-check against the recon JSON.
3. Assign severity from the **lowest-privilege** reachable source. A sink fed by
   an admin-only config value *and* by an editor-settable node title is an
   **editor→anonymous/admin** finding (Medium+), not the admin-only Low it looks
   like if you only saw the config caller.

The verification pass must explicitly answer: *"Have all callers/sources of this
sink been enumerated? Is there a lower-privilege source than the one analyzed?"*
A "Low — admin only" verdict on a shared sink is not trustworthy until the full
source set is listed.

## Severity rule of thumb

- **High** — exploitable by anonymous or a low-trust authenticated user, or
  leads to RCE / auth bypass / mass data exposure.
- **Medium** — exploitable by a *semi-trusted* user (e.g. an editor) against
  higher-privilege users or other users (stored XSS that fires for admins /
  anonymous visitors = editor→admin or →anon escalation).
- **Low / hardening** — only an `is_admin` administrator can trigger it (admin
  XSS-ing the admin = same trust level), or it leaks already-public data, or the
  vulnerable surface is dormant/unused.

The recon JSON is what tells you which bucket applies. A `|raw` bug whose only
author is the administrator is a hardening note, not an escalation.

## Findings document schema (`security-review-custom-code.md`)

```
# Security Review — Custom Modules & Theme
**Scope:** ...    **Method:** ...    **Result:** <one-paragraph verdict>

## Findings
### Finding N — <title>
* Severity: ...   * Category: ...   * Location: file:line   * Confidence: x/10
**Description.** <code + data flow>
**Exploit scenario.** <who plants it, who it fires for>
**Recommendation.** <fix>
**Reproduction recipe.** <lowest-privilege role; exact UI steps; payload; trigger URL; affected audience>   <-- REQUIRED; drives the demo

## Refuted candidates (investigated, not reported)
| Candidate | Location | Why refuted (tie to recon facts) | Reproduction recipe (attempt + expected barrier) |

## Recommended next steps
```

Every candidate — reported *and* refuted, every severity — **must** carry a
reproduction recipe. It is the script for the Phase-3 video (which is recorded
for **all** candidates, not just confirmed ones) and the input to the Phase-4
reconciliation. A refuted candidate's recipe names the lowest-privilege role and
UI steps to attempt on camera and the access barrier you expect to hit; the
resulting video is the evidence of refutation.

## The demo feedback loop (Phase 4) — record changes in BOTH directions

Every finding **and** every refuted candidate is demonstrated on camera in
Phase 3, regardless of severity and without asking the user — that complete set
of recordings is what makes this loop trustworthy. Demonstrating is adversarial
verification with the real access system in the loop, so it frequently revises
severity:

- **Downgrade** when the demo shows the lowest possible planter is an admin and
  the only audience is admins (admin→admin). Move it toward "Low / hardening" or
  the refuted table, and say why.
- **UPGRADE** when the demo shows a *non-admin* can plant or trigger something
  the review assumed was admin-only, or that anonymous can trigger it with no
  auth. **This is the highest-value outcome — never bury it.**
- **Confirm** when the demo matches the predicted severity.

Add this section to the review and put it near the top of the delivery summary:

```
## Severity changes after demonstration
### ⬆️ Upgrades (read these first)
- Finding X: <old> → <new>. Demo proof: <role/steps that worked>.
### ⬇️ Downgrades
- Finding Y: <old> → <new>. Demo proof: <why not reachable by non-admins>.
### ✔️ Confirmed
- Finding Z: severity unchanged; demo reproduced as predicted.
```

If a finding can't be demonstrated at all (no actor can reach it), that itself
is evidence — still record the on-camera attempt that shows the access system
blocking the actor, and file it as refuted with the access reason from recon.
