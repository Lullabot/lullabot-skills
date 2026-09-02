---
name: github-attachments
description: Upload images, screenshots, videos, and other files to GitHub so they render inside an issue, pull request, comment, release note, or wiki page. Use when a GitHub body needs an embedded screenshot or diagram, when asked to "attach this image to the issue", when a bug report needs a visual, or when a PR description should show before/after screenshots. Covers the gh --attach flag, the undocumented user-attachments upload endpoint it falls back to, MIME/size limits, and the markdown to embed the result.
---

# Attaching files to GitHub content

There are two routes, and which one you use depends on the gh version and on what the file has to do.

**`gh --attach`** is the supported route, added in [GitHub CLI 2.99.0](https://github.blog/changelog/2026-09-01-github-cli-media-in-issues-pull-requests-and-comments/) (September 2026). Use it whenever it covers the job: an image or video going onto an issue, a PR, or a comment. It is not available on GitHub Enterprise Server as of that release.

**The direct upload endpoint** is the fallback. GitHub's public API still has no documented attachment endpoint, so the web UI's `uploads.github.com/user-attachments/assets` remains the only way to get an asset URL you can place yourself. Source: [Ben Sheldon, "Programmatically upload attachments to GitHub issues, pull requests, comments"](https://island94.org/2026/08/programmatically-upload-attachments-to-github-issues-pull-requests-comments). Reach for it when:

- `gh --version` is below 2.99.0, or the target is GitHub Enterprise Server.
- The content is a release note or a wiki page, which `--attach` does not support.
- You need `<img width>` sizing or a before/after table. `--attach` rewrites a markdown reference in the body but the help does not document the same for an HTML `<img>` tag, so the endpoint is the safe route when the markup matters.
- The file is not an image or video (PDF, plain text, zip).

Because the endpoint is unofficial, it can change or disappear without notice. If a call starts returning 404 or 422 where it used to work and the troubleshooting below does not explain it, stop. Tell the user the endpoint looks like it has changed and let them decide what to do. Do not spend a session reverse-engineering a replacement.

## Upload with `gh --attach`

Check the version first: `gh --version`. Below 2.99.0, skip to the direct upload below.

`--attach` is repeatable and takes an optional alt string after a `#`. Quote the whole argument. The `#` itself is safe unquoted, since it only opens a comment at the start of a word, but an unquoted alt string with spaces in it splits into separate arguments and gh sees only the first word.

```bash
gh issue comment 123 --repo owner/name \
  --body "Repro on staging." \
  --attach './checkout.png#Checkout form with the ZIP field overlapping the submit button'

gh pr create --title "..." --body-file body.md \
  --attach './before.png#Sidebar before the fix' \
  --attach './after.png#Sidebar after the fix'
```

It works on `gh issue create`, `gh issue edit`, `gh issue comment`, `gh pr create`, `gh pr edit`, and `gh pr comment`. Supported types are PNG, JPEG, GIF, WebP, SVG, MP4, MOV, and WebM. You need write access to the repo, and the token `gh auth login` already gave you. Up to 50 files per command.

**You do control placement.** Reference the local path in the body and gh rewrites that reference to point at the uploaded asset. Anything you attach without referencing it gets appended to the end instead.

```bash
gh issue create --repo owner/name --title "Checkout layout breaks on mobile" \
  --body 'Steps to reproduce are below.

![Checkout form with the ZIP field overlapping the submit button](./checkout.png)

The overlap starts at 375px.' \
  --attach ./checkout.png
```

Alt text comes from whichever source is more specific: a reference already in the body keeps the alt text written there, otherwise the `#` suffix on the flag supplies it, otherwise gh falls back to the filename. Video renders as a player and takes no alt text at all.

If some attachments upload and others fail, gh still creates the issue or comment with the ones that worked, prints the URL to stdout, and exits non-zero. A script that treats a non-zero exit as "nothing happened" will be wrong here.

## Upload directly (fallback)

Use the bundled helper (`<skill-dir>/scripts/gh-upload-attachment.sh`):

```bash
bash <skill-dir>/scripts/gh-upload-attachment.sh screenshot.png --markdown --alt="Checkout form with the ZIP field overlapping the submit button"
# ![Checkout form with the ZIP field overlapping the submit button](https://github.com/user-attachments/assets/1ccd36c3-...)
```

Arguments: the file path, then optionally `owner/repo` (defaults to the current directory's GitHub remote), `--alt="..."`, and one of `--markdown` or `--html`. With no format flag it prints the bare URL. Always pass `--alt`; without it the helper falls back to the filename, which tells a screen reader nothing. The helper URL-encodes the filename and MIME type and HTML-escapes the alt string, so awkward filenames and quotes in the alt text are safe.

The raw call, if you need to do it inline:

```bash
FILE=screenshot.png
REPO=owner/name
curl -sS "https://uploads.github.com/user-attachments/assets?name=$FILE&content_type=image/png&repository_id=$(gh api "repos/$REPO" --jq .id)" \
  -X POST \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/json" \
  --data-binary "@$FILE"
# {"url":"https://github.com/user-attachments/assets/<uuid>"}
```

The response is a single JSON object with a `url` key. A 201 means success.

## Embed a direct upload

The direct upload does not attach the file to anything. It returns a URL, and the file only shows up where you paste that URL.

```bash
BODY="Repro on staging:

![Broken layout](https://github.com/user-attachments/assets/<uuid>)"

gh issue create --repo owner/name --title "..." --body "$BODY"
gh issue comment 123 --repo owner/name --body "$BODY"
gh pr create --body "$BODY"
```

For a body with several images or any shell-hostile characters, write it to a file and use `--body-file` instead of `--body`.

Use HTML when you need to control the size, which is usually the case for full-page screenshots:

```html
<img src="https://github.com/user-attachments/assets/<uuid>" alt="Broken layout on mobile" width="600">
```

Before/after pairs read best in a table:

```markdown
| Before | After |
| --- | --- |
| <img src="URL_A" width="400"> | <img src="URL_B" width="400"> |
```

## Rules

- **Always write real alt text.** The alt text carries the point of the screenshot for anyone using a screen reader, and for anyone reading the issue when the image fails to load. `![screenshot](...)` says nothing. Describe what the image shows: `![Checkout form with the ZIP field overlapping the submit button](...)`.
- **An image supplements the text, it never replaces it.** Error messages, stack traces, and config go in the body as text so they are searchable and copyable. Screenshot the thing a screenshot is actually needed for: layout, rendering, a UI state.
- **Prefer `--attach` when it fits.** It is supported, so it will not break the way an undocumented endpoint can. Fall back to the direct upload for the cases listed at the top, not by habit.
- **The repo scopes the upload, not the placement.** Upload against the repo where the content will live. Do not upload a client's screenshot against an unrelated repo just because it is the current directory.
- **Check what is in the frame before uploading.** Screenshots leak: session tokens in a URL bar, other clients' names in browser tabs, staff email addresses, customer data in a CMS listing. Crop or redact first. In a client repo this also means the cross-client rule applies to pixels, not just prose.
- **Anyone with the URL can view the asset**, including on a private repo. Treat the URL as the access control.
- **The asset persists** once uploaded, whether or not you ever reference it. There is no delete API here.

## Limits and formats

GitHub's own upload limits apply, and they are the same on both routes: 10MB for images and gifs, 10MB for most other files, and 10MB for video on Free plans (100MB on a paid plan). Supported types include PNG, JPEG, GIF, WEBP, SVG, PDF, plain text, MP4, MOV, WebM, and zip; `--attach` takes the image and video types only. Compress or trim before uploading rather than finding out at the request.

Set `content_type` to the file's real MIME type. The helper reads it with `file --mime-type`; if you hand-roll the call, do not guess `image/png` for a `.jpg`.

## Troubleshooting

- **`unknown flag: --attach`** — gh is older than 2.99.0. Upgrade it, or use the direct upload above.
- **401** — `gh auth token` returned nothing or an expired token. Run `gh auth status`. Any source gh recognizes works here, including a `GH_TOKEN` or `GITHUB_TOKEN` exported by a secret manager such as `op run`, since `gh auth token` prints the environment token when one is set.
- **404 on the `repos/` lookup** — wrong `owner/repo`, or the token cannot see a private repo. Confirm with `gh repo view owner/name`.
- **422** — usually a missing or mismatched `content_type`, or a file over the size limit.
- **The URL renders as a link instead of an image** — the markdown is missing the leading `!`, or the content type was uploaded as something other than an image type.
