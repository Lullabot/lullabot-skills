# Driving Drupal's admin UI for exploit demos

These are the things that break naive form automation on a real Drupal site.
All were learned the hard way; check each against the live site via `recon.php`
and `snapshot`.

## Logging in — don't fight the login form

Many sites front-end authentication with **OpenID Connect / SAML / CAS SSO**,
and protect forms with **antibot** (JS-injected token) or **honeypot**
(time-trap / hidden field). The standard `user/login` form may be absent or
unsubmittable. The login mechanism is *not* the security-relevant part of the
demo, so establish the session with a one-time login link instead:

```bash
# host side: mint a one-time login URL for a specific user
ddev drush uli --name=secdemo_editor --uri=$(ddev describe -j | jq -r '.raw.primary_url')
```

Then in the recording: `playwright-cli goto "<that URL>"`. It logs the user in
and lands on their account page. The link is single-use — mint a fresh one per
recording, and never commit it.

Create the throwaway users first:

```bash
ddev drush user:create secdemo_editor --mail=secdemo_editor@example.com --password='SecDemoPass123!'
ddev drush user:role:add editor secdemo_editor
```

`recon.php` reports which login-related modules are enabled and which forms
honeypot/antibot actually protect (node forms are often *un*protected even when
the modules are on).

## The standard XSS demo payload

Use a payload that **visibly defaces** the page (so the video is unambiguous)
but does nothing destructive. It must fit the field's `varchar(255)` limit — a
node title and a block `info` label are both 255. This overlay payload is 234
chars; swap the marker number per finding:

```
<img src=x onerror="e=document.createElement('div');e.textContent='XSS FINDING 1 FIRED';e.style.cssText='position:fixed;inset:0;z-index:99999;background:red;color:#fff;font:bold 40px sans-serif;padding:40px';document.body.append(e)">1
```

Assert success by waiting for the exact text (`XSS FINDING N FIRED`) — but note
the *escaped* copy of the field may also contain that substring, so match the
injected `<div>` exactly (the overlay element's textContent), not a substring of
the whole page. No `Content-Security-Policy` header → an unescaped inline
`<img onerror>` executes on render; confirm with `curl -I` that no CSP is sent.

## Node/block form gotchas

- **Stable selectors:** title = `[data-drupal-selector="edit-title-0-value"]`;
  block label = `[data-drupal-selector="edit-info-0-value"]`; primary submit =
  `[data-drupal-selector="edit-submit"]`.
- **Gin admin theme duplicates the submit button** into a sticky bar, so
  `edit-submit` matches **two** elements. Click `.last()` (the in-form one), or
  scope to the form, to avoid a strict-mode failure / clicking a non-functional
  clone.
- **Required-on-publish fields:** Drupal lets you save *unpublished* without
  required fields, but publishing enforces them ("X is required when
  publishing"). `recon.php` lists these per content type. **In a demo video, fill
  them on camera and publish through the real form** — tick the Published
  checkbox explicitly (`[data-drupal-selector="edit-status-value"]`) — because
  the point of the recording is to prove the acting role can author this content
  through the UI. Do **not** edit a pre-existing published node or seed it via
  `drush ::save()` to dodge the required fields *when the entity is the exploit
  vector*: that bypasses form validation and the access question the demo exists
  to answer. (Programmatic `drush` seeding is fine only for setup the actor
  doesn't control and that isn't the vector — e.g. a referenced parent node —
  and should be narrated as pre-seeded.) If a required field genuinely blocks the
  role from publishing through the UI, that constrained reachability is a Phase-4
  finding, not something to engineer around.
- **Invalid default references block save:** a field (e.g. `field_parent`) may
  pre-fill a default that the acting role can't reference (an unpublished node →
  "This entity (node: N) cannot be referenced"). Clear it before saving.
- **Tagify autocomplete** (entity reference): the pre-filled tag has a remove
  button `.tagify__tag__removeBtn` (force-click it). To set a value, click
  `.tagify__input`, type, wait for `.tagify__dropdown__item`, click the match.
- **options_buttons** (checkbox/radio entity reference, e.g. `field_topics`):
  the option label is the (escaped) entity title — match the checkbox by its
  accessible name, or by the input `value="<target nid>"`.
- **Published-by-default** varies by content type; recon reports it. The teaser
  that renders an XSS chip only shows for **published** referencing content.

## Who can actually plant the payload (the severity question)

Editors frequently **cannot** do what a finding assumes:
- Block creation needs a block-create permission editors usually lack. The CTA
  entity browser shows non-creators only a "select existing" tab — no "Create"
  tab. `block_content` create access is `createAccess('<bundle>')`.
- Layout Builder is often enabled on only one bundle and gated behind layout
  permissions no editor holds (`layout_builder.overrides.node.*` denied), so the
  block browsers there are unreachable by editors.
- Some bundles (e.g. an "other_bio") have no non-admin create permission at all.

`recon.php` answers all of these per role. If only `administrator` (an
`is_admin` role that bypasses everything) can plant it **and** only admins see
the trigger surface, the finding is admin→admin — not a privilege escalation.

## DB-reset caveat

If the project has its own test suite, its global setup may
**reimport/reset the database** on start (e.g. `@lullabot/playwright-drupal`
installs a throwaway SQLite DB). Running that suite mid-demo deletes planted
content. `playwright-cli` drives the live site directly and does **not** trigger
that setup — so just don't run the project's test suite while demonstrating.
