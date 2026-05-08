---
name: content-inventory
description: >
  Run Lullabot's content inventory tool to transform Screaming Frog CSV exports
  into client-ready audit spreadsheets (CSV or Excel). Use when the user needs to:
  (1) run a content audit or content inventory from Screaming Frog data,
  (2) understand what Screaming Frog exports are needed for an audit,
  (3) validate input CSVs before running the tool,
  (4) troubleshoot content inventory tool errors,
  (5) understand the output audit spreadsheet columns and format.
  Requires Python 3, pandas, and openpyxl.
allowed-tools: Bash(python *) Bash(pip *)
---

# Content Inventory Tool

Transforms Screaming Frog CSV exports into client-ready audit spreadsheets with two pipelines: pages and files.

## Setup

The tool is bundled with this skill at `${CLAUDE_SKILL_DIR}/scripts/`. Before first run, install dependencies:

```bash
pip install pandas openpyxl
# Only needed if using --follow-redirects:
pip install requests
```

## Quick Start

```bash
python ${CLAUDE_SKILL_DIR}/scripts/run_inventory.py \
  --pages <raw-pages.csv> \
  --orphans <orphan-pages.csv> \
  --files <raw-files.csv> \
  --inlinks <inlinks.csv> \
  --domain example.gov \
  --prefix CLIENT \
  --output-dir output \
  --format xlsx
```

This produces:
- `output/CLIENT-audit-all-pages.xlsx` — pages inventory
- `output/CLIENT-audit-all-files.xlsx` — files inventory

For CSV output, omit `--format` or use `--format csv`.

## Input Files

Four Screaming Frog exports are required. See [screaming-frog-exports.md](references/screaming-frog-exports.md) for detailed SF configuration instructions.

| Flag | SF Export | Columns the tool uses |
|------|-----------|----------------------|
| `--pages` | Internal > HTML (all pages crawl export) | Address, Title 1, Status Code, Flesch Reading Ease Score, GA4 Views, Redirect URL |
| `--orphans` | Crawl Analysis > Orphan Pages | URL (lacks `https://` prefix — this is expected) |
| `--files` | Internal > All (non-HTML resources) | Address, Title 1, Status Code, Size (bytes) |
| `--inlinks` | Bulk Export > All Inlinks | From, To, Anchor Text, Alt Text, Size |

The raw pages CSV contains ~79 columns; the tool extracts only 6. Extra columns are ignored.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--domain` | _(none)_ | Expected domain (e.g., `energy.maryland.gov`). Flags rogue off-domain URLs in output. |
| `--follow-redirects` | off | Follow HTTP redirect chains against the live site. Adds ~0.2s per URL. Requires `requests`. |
| `--format` | `csv` | Output format: `csv` or `xlsx`. |
| `--output-dir` | `.` | Directory for output files. Created if it doesn't exist. |
| `--prefix` | `output` | Filename prefix for output files. |

## What the Tool Does

### Pages pipeline
1. Load raw pages, extract 6 columns, normalize URLs
2. Remove 404 status pages
3. Append orphan pages (separate CSV, URLs already lack `https://`)
4. Deduplicate on normalized URL — first non-empty title/status, MAX for GA views and reading scores
5. Filter out non-page URLs (PDFs, docs, images, etc.)
6. Resolve redirects from Screaming Frog's Redirect URL column (or via HTTP with `--follow-redirects`)
7. Merge redirect duplicates — multiple source URLs become newline-separated in one cell
8. Add redirect target URLs not already in inventory
9. Flag rogue URLs outside `--domain`
10. Convert Flesch reading scores to grade levels (blank stays blank, not "5th grade")

### Files pipeline
1. Load raw files + inlinks, normalize URLs
2. Filter out page URLs (.aspx, .html, .htm, .php, .jsp)
3. Collect unique file URLs from both sources
4. Enrich each file with: title, type (classified by extension), anchor text, source page URLs (newline-separated), alt text, size

## Understanding the Output

Both output files use a two-header-row format:
- **Row 1**: Category headers (e.g., "Page information", "Review criteria", "Decisions & comments")
- **Row 2**: Column descriptions with embedded newlines explaining each field

Pre-filled data columns are followed by empty review columns for auditors. The "Required by law" column defaults to `FALSE`.

For complete column specifications, see [output-columns.md](references/output-columns.md).

## Pre-run Validation

Before running the full tool, validate that input CSVs have the expected columns:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/check_inputs.py \
  --pages <raw-pages.csv> \
  --orphans <orphan-pages.csv> \
  --files <raw-files.csv> \
  --inlinks <inlinks.csv>
```

This catches the most common error: passing the wrong Screaming Frog export to the wrong flag.

## Troubleshooting

Common issues:

- **KeyError on a column name** — Wrong SF export passed to wrong flag. Run `check_inputs.py` to diagnose.
- **ModuleNotFoundError: pandas/openpyxl** — Run `pip install pandas openpyxl`.
- **Output has 0 rows** — All pages were 404, or the wrong file was passed to `--pages`.

For more, see [troubleshooting.md](references/troubleshooting.md).

## Development

```bash
# Run all tests
pytest

# Run a single test
pytest tests/test_normalize.py::test_strips_https
```

Source modules in `content_inventory/`: `cli.py` (arg parsing), `pages.py` (pages pipeline), `files.py` (files pipeline), `output.py` (formatting), `normalize.py` (URL normalization), `redirects.py` (redirect resolution), `filetypes.py` (file classification), `readability.py` (Flesch to grade).
