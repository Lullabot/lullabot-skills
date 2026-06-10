# Driving and video-recording with `playwright-cli`

`playwright-cli` is Microsoft's Playwright **Agent CLI** — a stateful,
token-efficient browser driver for agents. The `e0ipso/ddev-playwright-cli`
add-on installs it in the DDEV web container. No Playwright *test* project is
required, which is why this works on codebases that have never set up Playwright.

## Install / verify

```bash
ddev exec playwright-cli --version        # is it available?
# if not:
ddev add-on get e0ipso/ddev-playwright-cli
ddev restart
```

The add-on ships `.ddev/playwright-cli/cli.config.json` (chromium, headless,
`ignoreHTTPSErrors: true`) and auto-installs its own Claude skills on start.

## State model

The browser/page persists **across** `ddev exec playwright-cli ...` invocations,
so you build a session one command at a time. `snapshot` returns an
accessibility tree whose nodes have short refs (e.g. `e5`) that you pass to
`click`/`fill`. Always `snapshot` after a navigation to learn the current refs —
they are not stable across page loads.

## Core commands

```bash
ddev exec playwright-cli goto <url>                 # navigate
ddev exec playwright-cli snapshot                   # a11y tree + element refs
ddev exec playwright-cli click <ref>                # click by ref from snapshot
ddev exec playwright-cli click --selector "text=Save"   # or by selector
ddev exec playwright-cli fill <ref> "value"         # fill an input
ddev exec playwright-cli fill --selector '[data-drupal-selector="edit-title-0-value"]' "value"
ddev exec playwright-cli press <ref> Enter
ddev exec playwright-cli screenshot out.png
```

Prefer role/text/label selectors (`text=`, `role=`, `[data-drupal-selector=...]`)
over brittle CSS. Drupal's stable hooks are the `data-drupal-selector`
attributes (e.g. `edit-title-0-value`, `edit-submit`).

## Video recording (the deliverable)

```bash
ddev exec playwright-cli video-start finding-1.webm --size=1280x720
ddev exec playwright-cli video-chapter "Step 1: Log in as editor" --duration=2000
#   ... establish the session via one-time login link ...
ddev exec playwright-cli video-chapter "Step 2: Author the block via the editorial UI"
#   ... open the real add form, fill required fields, enter the payload, save ...
#   ... add a chapter per form if the path spans several (create block -> place it) ...
ddev exec playwright-cli video-chapter "Step 3: Trigger as anonymous visitor"
#   ... visit trigger URL ...
ddev exec playwright-cli video-stop
```

- Output: **WebM (VP8/VP9)** under `.playwright-cli/` in the project root —
  e.g. `.playwright-cli/finding-1.webm`. Copy it out and transcode if you want
  mp4 (broad compatibility):
  ```bash
  ffmpeg -y -i .playwright-cli/finding-1.webm -c:v libx264 -pix_fmt yuv420p \
    -movflags +faststart -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" finding-1.mp4
  ```
- Chapter markers render as full-screen cards — use them to narrate the exploit
  steps (login → plant → trigger). `--description=` and `--duration=`(ms) are
  optional.

## Richer annotations (optional) — `run-code`

For overlays/highlights beyond chapters, run a JS snippet with the screencast
API:

```bash
ddev exec playwright-cli run-code --filename script.js
```

```js
// script.js — runs with `page` in scope
const a = await page.screencast.showOverlay(`<div style="position:fixed;top:0;left:0;right:0;padding:16px;background:#c00;color:#fff;font:bold 22px sans-serif;text-align:center">Stored XSS fires here</div>`);
// ... overlays are pointer-events:none, they don't block interaction ...
await a.dispose();
```

## Tips for reliable runs

- Establish auth by navigating to a one-time login link (see the UI-automation
  reference) rather than fighting a login form.
- Insert short waits implicitly by `snapshot`-ing between actions; the CLI waits
  for actionability on `click`/`fill`.
- Keep each finding's recording short and chaptered: login → plant → trigger.
