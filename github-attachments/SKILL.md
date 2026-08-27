---
name: github-attachments
description: Upload images, screenshots, videos, and other files to GitHub so they render inside an issue, pull request, comment, release note, or wiki page. Use when a GitHub body needs an embedded screenshot or diagram, when asked to "attach this image to the issue", when a bug report needs a visual, or when a PR description should show before/after screenshots. Covers the undocumented user-attachments upload endpoint, MIME/size limits, and the markdown to embed the result.
---

# Attaching files to GitHub content

GitHub's public API has no endpoint for issue or PR attachments. The web UI uploads through `uploads.github.com/user-attachments/assets`, which is undocumented but works with a normal `gh auth token`. Source: [Ben Sheldon, "Programmatically upload attachments to GitHub issues, pull requests, comments"](https://island94.org/2026/08/programmatically-upload-attachments-to-github-issues-pull-requests-comments).

Because it is unofficial, it can change or disappear without notice. If a call starts returning 404 or 422 where it used to work and the troubleshooting below does not explain it, stop. Tell the user the endpoint looks like it has changed and let them decide what to do. Do not spend a session reverse-engineering a replacement.

## Upload

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

## Embed

The upload does not attach the file to anything. It returns a URL, and the file only shows up where you paste that URL.

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
- **The repo scopes the upload, not the placement.** Upload against the repo where the content will live. Do not upload a client's screenshot against an unrelated repo just because it is the current directory.
- **Check what is in the frame before uploading.** Screenshots leak: session tokens in a URL bar, other clients' names in browser tabs, staff email addresses, customer data in a CMS listing. Crop or redact first. In a client repo this also means the cross-client rule applies to pixels, not just prose.
- **Anyone with the URL can view the asset**, including on a private repo. Treat the URL as the access control.
- **The asset persists** once uploaded, whether or not you ever reference it. There is no delete API here.

## Limits and formats

GitHub's own upload limits apply: 10MB for images and gifs, 10MB for most other files, 25MB for videos (100MB for accounts on a paid plan). Supported types include PNG, JPEG, GIF, WEBP, SVG, PDF, plain text, MP4, MOV, and zip. Compress or trim before uploading rather than finding out at the request.

Set `content_type` to the file's real MIME type. The helper reads it with `file --mime-type`; if you hand-roll the call, do not guess `image/png` for a `.jpg`.

## Troubleshooting

- **401** — `gh auth token` returned nothing or an expired token. Run `gh auth status`. Any source gh recognizes works here, including a `GH_TOKEN` or `GITHUB_TOKEN` exported by a secret manager such as `op run`, since `gh auth token` prints the environment token when one is set.
- **404 on the `repos/` lookup** — wrong `owner/repo`, or the token cannot see a private repo. Confirm with `gh repo view owner/name`.
- **422** — usually a missing or mismatched `content_type`, or a file over the size limit.
- **The URL renders as a link instead of an image** — the markdown is missing the leading `!`, or the content type was uploaded as something other than an image type.
