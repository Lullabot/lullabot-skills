# Gollum Link Syntax Reference

GitHub wikis are powered by Gollum. This reference covers link
resolution, page naming, and image handling.

## Link Formats

### Wiki-Style Links (Preferred for Internal Pages)

```
[[page-name]]                       → links to page-name.md, displays page title
[[Display Text|page-name]]          → links to page-name.md, displays "Display Text"
```

**Critical:** The pipe syntax is `[[display|target]]` — display text BEFORE
the pipe, link target AFTER. This is the opposite of MediaWiki syntax.

### Standard Markdown Links (for External URLs)

```markdown
[Display Text](https://example.com)
```

Use standard markdown links only for external URLs. Do not use
`[text](wiki-page)` for internal wiki pages — it will not resolve.

## Link Resolution Rules

1. Links resolve **case-insensitively**.
2. **Hyphens and spaces are interchangeable**: `my-page` matches `my page`
   matches `My Page` matches `my-Page`.
3. The link target matches against the **filename** (without `.md` extension).
4. Resolution searches the **same directory first**, then the repository root.
5. Absolute paths use a leading slash: `[[/root-level-page]]`.
6. Anchor links to headings within a page are **not supported** in wiki-style
   links. Use standard markdown links for same-page anchors.

## Pipe Syntax Details

The `|` character separates display text from the link target:

```
[[Display Text|link-target]]
```

- **Left of pipe:** What the user sees (rendered text)
- **Right of pipe:** The page to link to (filename without extension)

### Why This Matters

If you write `[[page-name|Pretty Title]]` (target first, display second),
Gollum interprets "page-name" as the display text and "Pretty Title" as
the link target. It will look for a page named `Pretty-Title.md` and
display the text "page-name" — the exact opposite of what was intended.

### Correct Examples

| Syntax | Displays | Links To |
|---|---|---|
| `[[project-brief]]` | "project brief" | project-brief.md |
| `[[Project Brief\|project-brief]]` | "Project Brief" | project-brief.md |
| `[[Home]]` | "Home" | Home.md |
| `[[Back to Home\|Home]]` | "Back to Home" | Home.md |
| `[[1. Setup Guide\|setup-guide]]` | "1. Setup Guide" | setup-guide.md |

### Incorrect Examples (Common Mistakes)

| Syntax | Problem |
|---|---|
| `[[project-brief\|Project Brief]]` | Links to `Project-Brief.md`, displays "project-brief" |
| `[Setup Guide](setup-guide)` | Markdown link syntax does not resolve internal wiki pages |
| `[[setup-guide#section]]` | Anchor links not supported in wiki-style links |

## Page Naming Conventions

### Filename to URL Mapping

The filename (without `.md`) becomes the URL slug:

- `my-page.md` → `/wiki/my-page`
- `Home.md` → `/wiki/Home`
- `Banner.md` → `/wiki/Banner`

### Recommended Naming

- Use **kebab-case** for filenames: `my-page-title.md`
- Capitalize proper nouns: `Banner.md`, `Home.md`
- Prefix related pages for grouping:
  `its-training-session-1-setup.md`,
  `its-training-session-2-workflow.md`

### Page Title Display

When using bare `[[page-name]]` links (no pipe), Gollum displays the
page title by converting the filename:

- Hyphens become spaces
- First letter of each word is capitalized
- `my-page-title` displays as "My Page Title"

To override the display text, use the pipe syntax:
`[[Custom Title|my-page-title]]`.

## Images

### Storing Images

Store images in the wiki repository (e.g., an `images/` directory at the
root of the wiki repo).

### Referencing Images

Use standard markdown image syntax with relative paths:

```markdown
![Alt text](images/screenshot.png)
```

Wiki-style image embeds also work:

```
[[images/screenshot.png]]
[[Alt text|images/screenshot.png]]
```

### Image Sizing

GitHub wiki does not support image sizing in markdown. To control image
dimensions, use raw HTML:

```html
<img src="images/screenshot.png" alt="Alt text" width="600">
```

## Special Pages

- **Home.md** — The wiki landing page. Always exists.
- **_Sidebar.md** — Rendered as the sidebar on every page. Use wiki-style
  links here for navigation.
- **_Footer.md** — Rendered as footer on every page (optional).
- **_Header.md** — Rendered as header on every page (optional, rare).

## Wiki Repository Structure

GitHub wiki content lives in a separate git repository:

```
<repo-name>.wiki.git
├── Home.md
├── _Sidebar.md
├── _Footer.md (optional)
├── page-one.md
├── page-two.md
└── images/
    ├── screenshot-1.png
    └── diagram.png
```

Clone with: `git clone https://github.com/OWNER/REPO.wiki.git`

Push changes with standard git commands. Changes appear on the wiki
immediately after push.
