---
name: github-wiki
description: This skill should be used when creating, editing, or managing GitHub wiki pages. Use when writing wiki content, creating internal links between wiki pages, adding images, updating sidebar navigation, or working with .wiki.git repositories. Triggers on "wiki", "wiki page", "update the wiki", "add to wiki", or when working in a *.wiki directory or *.wiki.git repository.
---

# GitHub Wiki

## Overview

GitHub wikis are powered by [Gollum](https://github.com/gollum/gollum),
a git-backed wiki engine. Wiki content lives in a separate `.wiki.git`
repository alongside the main code repository. Understanding Gollum's
link syntax and page resolution is essential — it differs from both
standard Markdown and MediaWiki in ways that cause subtle, hard-to-debug
broken links.

## Critical: Link Syntax

**The most common mistake when working with GitHub wikis is getting the
pipe syntax backwards.** Gollum uses the opposite order from MediaWiki:

```
CORRECT:  [[Display Text|page-name]]
WRONG:    [[page-name|Display Text]]
```

- Left of pipe = what the reader sees
- Right of pipe = the page to link to (filename without `.md`)

When the order is reversed, links silently resolve to non-existent pages
and render as red/broken links with no error message.

For the full link syntax reference including resolution rules, image
handling, and special pages, read `references/gollum-link-syntax.md`.

## Working with Wiki Repositories

### Locating the Wiki Repo

Wiki repositories are cloned separately from the main repo:

```bash
git clone https://github.com/OWNER/REPO.wiki.git
```

Within a project, the wiki repo is typically at a path like
`code/REPO.wiki/` or similar. Check the project's CLAUDE.md or
memory files for the exact location.

### Pushing Changes

Wiki changes are pushed with standard git commands. Changes appear
on GitHub immediately after push — there is no build step or CI.

```bash
cd path/to/repo.wiki
git add -A
git commit -m "Description of changes"
git push origin master
```

Note: Wiki repos typically use `master` as the default branch, not `main`.

## Creating Wiki Pages

### Page Files

Each wiki page is a Markdown file at the root of the wiki repository.

- **Filename** = URL slug and link target (e.g., `my-page.md` → `/wiki/my-page`)
- **H1 heading** = Page title displayed at the top
- Use **kebab-case** for filenames: `setup-guide.md`, not `Setup Guide.md`
- Capitalize proper nouns: `Banner.md`, `Home.md`

### Naming for Grouping

Prefix related pages to keep them organized:

```
its-training-session-1-pantheon.md
its-training-session-2-git.md
its-training-session-3-drupal.md
```

### Internal Links

Always use wiki-style `[[links]]` for internal pages:

```markdown
See [[Setup Guide|setup-guide]] for details.
```

Never use markdown-style `[text](page)` for internal wiki links — they
will not resolve.

### Cross-Page Navigation

Add prev/next navigation at the bottom of sequential pages:

```markdown
**Previous:** [[Session 1|training-session-1]] | **Next:** [[Session 3|training-session-3]]
```

## Special Pages

| File | Purpose |
|---|---|
| `Home.md` | Landing page, always exists |
| `_Sidebar.md` | Navigation sidebar, rendered on every page |
| `_Footer.md` | Footer rendered on every page (optional) |
| `_Header.md` | Header rendered on every page (optional, rare) |

### Sidebar Best Practices

Keep the sidebar organized with sections and wiki-style links:

```markdown
# Project Wiki

[[Home]]

---

### Section Name

- [[Page One|page-one]]
- [[Page Two|page-two]]

---

### External Links

- [GitHub Issues](https://github.com/OWNER/REPO/issues)
```

## Images

Store images in an `images/` directory at the wiki repo root.
Reference with standard markdown or wiki syntax:

```markdown
![Alt text](images/screenshot.png)
```

GitHub wiki does not support image sizing in markdown. Use HTML for
controlled dimensions:

```html
<img src="images/screenshot.png" alt="Alt text" width="600">
```

## Workflow: Adding a New Wiki Section

1. **Create the page files** at the wiki repo root with kebab-case names
2. **Add internal links** using `[[Display Text|page-name]]` syntax
3. **Update `_Sidebar.md`** to add navigation links to the new pages
4. **Update `Home.md`** if the new section should be listed on the landing page
5. **Commit and push** to make changes live immediately
6. **Verify links** — broken links render as red text with class `internal absent`

## Troubleshooting

### Links Show as Red / "absent"

- Check pipe order: must be `[[Display|target]]` not `[[target|Display]]`
- Verify the target filename exists (without `.md` extension) at repo root
- Check for typos — resolution is case-insensitive but must otherwise match

### Images Not Rendering

- Verify the image file is committed and pushed to the wiki repo
- Check the relative path from the wiki root (e.g., `images/file.png`)
- Ensure the image filename has no spaces

### Page Not Appearing in Wiki

- Verify the `.md` file is at the repository root (not in a subdirectory
  unless using Gollum subdirectory support)
- Verify the file was pushed to the remote (`git push origin master`)
- Check that the file has a `.md` extension
