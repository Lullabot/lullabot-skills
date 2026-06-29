---
name: drupal-demo-recorder
description: Use when asked to record demo videos or screenshots of a Drupal site (running under DDEV) to share with people — e.g. "make a demo video of <feature>", "record a walkthrough", "capture screenshots of this flow for the team", "show this working". Produces 1080p, narrated, validated, presentable captures driven through the real UI with e0ipso/ddev-playwright-cli. Do NOT use for writing automated/CI Playwright tests (use the playwright-cli skill) or for non-Drupal / non-DDEV recording.
---

# drupal-demo-recorder

Produce **demo-ready-for-a-team-meeting** videos and screenshots of a Drupal site
running under DDEV. This skill is the *methodology + quality bar* layer on top of
the `playwright-cli` skill (which documents the raw CLI: `open`, `goto`, `run-code`,
`video-start/chapter/stop`, `screenshot`, sessions). Read that skill for CLI
mechanics; read this one for **how to make the output good and prove it is**.

The bar: a colleague watching in a meeting immediately understands what is happening,
sees every click/keystroke, sees real content (not empty boxes), and never waits on
dead air. If you would be embarrassed to play it in a meeting, it is not done.

## The one rule that drives everything

**Drive the REAL UI, never shortcuts.** Use `page.mouse.move/down/up`,
`locator.click()`, `locator.dragTo()`, and type with `locator.pressSequentially()` /
`page.keyboard.type()`. Do **not** use `locator.fill()` or `page.evaluate(() => el.click())`
or firing the app's AJAX directly. Two reasons:
1. The visible-input overlay only renders a cursor/keystroke for **real** events — shortcuts show nothing on screen.
2. A demo must show the **genuine workflow** a user would perform. "It works, trust me (via AJAX)" is exactly the kind of unconvincing capture this skill exists to prevent.

If a native interaction seems hard (HTML5 drag-and-drop, a modal in an iframe), **spike it** (see Phase 2) — it is almost always drivable. `page.mouse.down/move/up` fires real `dragstart/dragover/drop`; iframes are reachable via `page.frameLocator(...)`.

## Setup — run first (auto-installs missing tooling)

From the DDEV project root, run the idempotent bootstrap. It installs anything missing
and restarts DDEV once if needed — safe to run before every recording:

```bash
bash <skill-dir>/scripts/ensure-tooling.sh
```

It ensures (announcing each project-modifying step):
- **`e0ipso/ddev-playwright-cli`** — the recorder CLI (also provides the `playwright-cli` skill this builds on). Installed via `ddev add-on get`; chromium is built into the web image on restart.
- **`ffmpeg`/`ffprobe`** — added persistently via `.ddev/web-build/Dockerfile.ffmpeg`.
- **`.playwright/cli.config.json`** — copied from `assets/cli.config.example.json` (1920×1080 + `ignoreHTTPSErrors` for DDEV's self-signed cert) if absent.

> It modifies `.ddev/` and triggers one `ddev restart` (brief downtime) only when the add-on
> or ffmpeg are missing; on an already-equipped project it is a no-op. If you'd rather not
> touch `.ddev/`, run the steps printed by the script by hand instead.

Then you still need to know / decide:
- **Which user/role** to record as. Log in with a one-time link: `LOGIN=$(ddev drush --uri=<site-url> uli --name=<user>)`, then `goto` it. The link is single-use — **regenerate it every recording run**.
- The overlay's container path for `addInitScript`. ddev-playwright-cli runs **inside the container** (repo mounted at `/var/www/html`), so reference this skill's overlay by its container path, e.g. `/var/www/html/.claude/skills/drupal-demo-recorder/assets/input-overlay.js`.

## Non-negotiable quality requirements

| Requirement | How |
| --- | --- |
| **1080p desktop frame** | `cli.config.json` viewport 1920×1080; also `await page.setViewportSize({width:1920,height:1080})` at the top of each script. |
| **Visible mouse + keyboard** | `await page.addInitScript({ path: '<container path>/assets/input-overlay.js' })` BEFORE the first `goto`. Drive via real events (the one rule). Move the mouse in steps between targets (`page.mouse.move(x,y,{steps:8})`) so the cursor visibly travels; nudge it once after entering a view so it is on-screen. |
| **Step narration** | Show a chapter title card per step: `await page.evaluate((t)=>window.__demoTitle(t,2600), 'Add a component')`. Also add `video-chapter "..."` markers. |
| **Scroll the subject into view** | Before acting on / capturing an element: `await locator.scrollIntoViewIfNeeded()` or `window.scrollTo({top,behavior:'smooth'})`, then a short pause. Never act on or screenshot something off-screen. |
| **Real content** | Show genuine content that renders (real images, real text), not empty placeholders or Lorem. Decide its source in Phase 0. If a component renders blank, STOP and find out why before recording (commonly a broken text format, a missing field value, or an empty reference). |
| **Natural, even pacing** | Control pacing AT RECORD TIME (see *Pacing* below): dwell after each change, type with a per-key delay, move the mouse in steps. A light post-process slow is optional polish — not the primary lever, and never `slowMo`. |
| **No dead air** | A click that triggers a navigation/heavy re-render makes Playwright auto-wait; the frame freezes. After such a click wait only ~2s then `video-stop`, and/or trim the tail. Never ship >3s of a static screen. |
| **Screenshots = viewport, scrolled** | Capture the viewport with the relevant part scrolled in — NOT `--full-page` (full-page captures overlap fixed toolbars/palettes and look broken). 1080p stills pulled from the finished video are ideal. |

## Pacing — make it readable without making it sluggish

In order of preference:

1. **Record-time pacing (primary).** Make each step readable as it happens:
   - `await page.waitForTimeout(800–1500)` after each meaningful change (the "let it land" beat).
   - Type at human cadence: `locator.pressSequentially(text, { delay: 70 })` (never `fill()`).
   - Move the mouse in visible steps: `page.mouse.move(x, y, { steps: 10 })`; for drags, many small steps with brief pauses so the motion is followable.
   This produces natural, intentional pacing and needs no post-processing.
2. **Light global slow in post (optional polish).** `scripts/process-video.sh ... 1.5`
   (ffmpeg `setpts`) uniformly slows the finished video — handy to ease fast bits like AJAX
   swaps. Caveat: it ALSO stretches unavoidable reload/auto-wait pauses into dead air, so
   keep it modest (≤1.5×) and short-wait-then-stop / trim the tail. Pass `1.0` for
   transcode-only when you already paced at record time.
3. **`slowMo` — avoid for final output.** Playwright's `slowMo` only inserts a fixed delay
   *before each action* → uneven snap-pause-snap motion; it does NOT slow page animations/AJAX
   or the cursor overlay, and it lengthens the live run (more timeout/flake risk). Debugging
   aid only.

## Workflow

Run **Setup** (above) first so the toolchain is present, then work the phases in order.

### Phase 0 — Content: use existing, or create? (ask the user first)

Demos live or die on showing *real* content. Before storyboarding, **ask the user**
(use AskUserQuestion):

1. **"Does the site already have content we should demo with, or should I create demo content?"**
   - *Use existing* → ask which specific items/pages, then resolve their concrete IDs / URLs /
     titles with drush and use those. Confirm they render with real text + images.
   - *Create it* → continue to Q2.
2. If content must be created, ask **"Should I model the demo content on the site's existing
   content, or build it around a theme you give me?"**
   - *Model on existing* → inspect real examples of the relevant content type(s) — fields,
     structure, length, tone, which images/references they use — and create content that
     mirrors them so it looks authentic and on-brand.
   - *Provide a theme* → ask for the theme/topic (plus any tone/brand notes) and generate
     fitting content for it.
3. Either way: after choosing/creating content, **render it and confirm it actually displays**
   (real text + images, no empty placeholders, no broken-format blanks) BEFORE recording.
   Created demo content is disposable — note it in the README and clean it up if the
   environment is not throwaway.

### Phase 1 — Storyboard
Write the ordered list of steps and the chapter title for each, the exact node/page/URL,
the user/role, and the *specific real content* to use (sourced in Phase 0; resolve concrete
IDs/titles with drush). Decide endings (Save vs Discard — Discard keeps a live page pristine
while still demonstrating the edit).

### Phase 2 — Spike risky interactions FIRST
Before recording a full take, prove each non-obvious interaction in isolation and
**screenshot + look at the result**: native drag-and-drop, modal/iframe flows, anything
that re-renders. Capture the working selectors and the exact event sequence. This is what
prevents recording a 90-second take that fails at second 70. (Drag pattern: `mouse.move`
to the handle → `mouse.down()` → small `mouse.move` to start the native drag → read the
drop target's rect → `mouse.move` over it and PAUSE so `dragover` fires → `mouse.up()`.)

### Phase 3 — Record
One continuous `run-code` session per video (named session, e.g. `-s=rec`). Inject the
overlay, set viewport, log in, navigate (`{waitUntil:'domcontentloaded'}` — NEVER `'load'`
on heavy/edit pages, it can hang), then perform the storyboard with real input + title
cards + scrolling. Save the raw `.webm` to the project root.

### Phase 4 — Process
Transcode to a shareable H.264 mp4: `scripts/process-video.sh <raw>.webm demos/.../<name> [speed]`.
If you paced at record time, pass `1.0` (transcode only); use `1.5` only for the optional light
slow (see *Pacing*). Never add a scale filter (you recorded at final resolution).

### Phase 5 — VALIDATE (mandatory — see below). Iterate until it passes.

## Validation loop — you MUST look at the actual output

A recording you have not watched is not done. Reports of success are not evidence.

1. `scripts/extract-frames.sh demos/.../<name>.mp4 <tmp-dir> 8` to dump evenly-spaced frames, **and** hand-grab the key moments (mid-drag, modal open, the embed/result, a keystroke instant): `ddev exec ffmpeg -ss <t> -i /var/www/html/<video> -frames:v 1 /var/www/html/<dir>/m.png`.
2. **Open every frame** (Read the PNG) and check each item:
   - [ ] Exactly **one** cursor visible (watch modals/iframes — a stray second cursor is the classic bug).
   - [ ] **Key badges** appear while typing (proves real keyboard input, not `fill()`).
   - [ ] The **subject is in view** for each step (nothing important off-screen / cut off).
   - [ ] **Real content rendered** — images load, text is genuine, no empty/placeholder boxes, no error/"Status:" noise.
   - [ ] **No dead-air** tail or >3s static stretch (AJAX re-renders that keep content on screen are fine).
   - [ ] Title card present and readable for each step.
   - [ ] Clean **1080p** layout — no overlapping chrome, no clipping, correct resolution (`ffprobe`).
3. Confirm **duration and resolution** with `ffprobe`.
4. **Re-record anything that fails.** Then re-validate. Do not hand off until every box is checked on the final files.
5. Verify the environment is left clean (any temporary config like a front-page swap, draft node, or test content is reverted; the live site still responds 200).

## Common failure modes (seen repeatedly — design them out)

- **Empty / placeholder / Lorem content** → looks broken. Use real content; verify it renders BEFORE recording. Blank field output is often a broken text format (a CKEditor format with no working filter renders empty) or an unselected entity reference.
- **Too fast** → pace at record time (dwells + keystroke `delay` + mouse `steps`); optional light ≤1.5× post-slow. Not `slowMo` (uneven snap-pause).
- **Didn't scroll** → `scrollIntoViewIfNeeded` before each action and capture.
- **Full-page screenshots** → use viewport stills scrolled to the subject (or frames from the video).
- **Dead air at the end** → the Save/submit click auto-waits for a heavy reload; short-wait then stop, or trim.
- **Invisible mouse/keyboard** → you used `fill()`/AJAX instead of real events. Drive the real UI.
- **Two cursors** → the overlay was injected into an iframe without single-cursor forwarding; use the bundled `input-overlay.js` (it forwards child-frame events to one top-frame cursor).
- **Page hangs on load / Edit surface won't open** → don't use `waitUntil:'load'`; use `domcontentloaded` and `waitForFunction` on a real readiness signal. Heavy/content-rich pages may be slow or hit limits — profile and fix, or pick a lighter representative page, but say so.
- **Recorded as the wrong user** → log in (drush uli) as the intended role; permissions change what's visible.
- **Edited PHP/templates and nothing changed** → reload the workers: `ddev exec bash -c "killall -USR2 php-fpm"`.

## Deliverables & housekeeping
- Put videos/screenshots under a `demos/<feature>/` dir with a short README: what each file shows, the demo node/URL/user, and any environment caveats.
- Keep `.mp4` (shareable) alongside `.webm`.
- Note in the README anything non-default you set up to make it work, and whether it was reverted.

## Optional — subagent orchestration for big jobs
For multi-video jobs you can delegate to subagents, but: the DDEV browser is a shared,
serial resource — **do not run two browser-driving subagents at once** (concurrent edit
renders go flaky). Spike in one agent, record serially, and always do an **independent**
validation pass yourself (open the frames) rather than trusting a subagent's self-report.
