# Screaming Frog Export Configuration

How to produce each of the 4 required input files from Screaming Frog SEO Spider.

## Prerequisites

Before crawling, enable these in Screaming Frog:

- **GA4 integration**: Configuration > API Access > Google Analytics > connect GA4 property. Required for the GA4 Views column in the pages export.
- **Readability analysis**: Configuration > Content > Readability > enable "Flesch Reading Ease". Required for the reading score column.

## 1. Raw Pages CSV (`--pages`)

**How to export**: After crawling, go to Internal tab > filter to HTML. Export via File > Export or Bulk Export > All HTML.

**Required columns** (tool extracts these 6 from ~79 total):

| Column | Required | Notes |
|--------|----------|-------|
| Address | Yes | Full URL including protocol |
| Title 1 | Yes | Page `<title>` tag |
| Status Code | Yes | HTTP status (200, 301, 302, 404) |
| Flesch Reading Ease Score | Yes | Requires readability analysis enabled |
| GA4 Views | Yes | Requires GA4 API integration |
| Redirect URL | Yes | Populated for 301/302 status codes |

If GA4 Views or Flesch Reading Ease Score columns are missing, see the prerequisites above.

## 2. Orphan Pages CSV (`--orphans`)

**How to export**: After crawling, run Crawl Analysis (Crawl Analysis > Start). Go to Crawl Analysis > Orphan Pages. Export.

**Required columns**:

| Column | Required | Notes |
|--------|----------|-------|
| URL | Yes | URLs lack `https://` prefix — this is expected and handled by the tool |

The orphan URLs are already partially normalized (no protocol). The tool's URL normalization is idempotent, so this works correctly.

## 3. Raw Files CSV (`--files`)

**How to export**: After crawling, go to Internal tab. Filter to non-HTML content types (Images, JavaScript, CSS, PDF, etc.) or use Bulk Export > All Internal to get everything (the tool filters out page URLs automatically).

**Required columns**:

| Column | Required | Notes |
|--------|----------|-------|
| Address | Yes | Full URL of the file |
| Title 1 | No | Document title if available |
| Status Code | No | HTTP status code |
| Size (bytes) | No | File size |

The tool filters out page-like URLs (.aspx, .html, .htm, .php, .jsp) from this export automatically.

## 4. Inlinks CSV (`--inlinks`)

**How to export**: Use Bulk Export > All Inlinks. Alternatively, select specific resources and right-click > Export Inlinks.

**Required columns**:

| Column | Required | Notes |
|--------|----------|-------|
| From | Yes | Source page URL (the page containing the link) |
| To | Yes | Target file URL (the linked resource) |
| Anchor Text | No | Link text used in the `<a>` tag |
| Alt Text | No | Image alt attribute |
| Size | No | File size from inlinks data |

## Common Mistakes

- **Swapped files**: Passing the inlinks CSV to `--files` or vice versa. Use `check_inputs.py` to validate.
- **Missing GA4 column**: Forgot to connect GA4 API before crawling. Re-crawl with GA4 enabled.
- **Missing readability column**: Forgot to enable Flesch analysis. Re-crawl with readability enabled.
- **Wrong filter on pages export**: Exporting "All" instead of "HTML" gives you files mixed in with pages. The tool handles this (filters non-page URLs), but it's cleaner to export HTML-only.
