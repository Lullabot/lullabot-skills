---
name: content-inventory
description: Transform Screaming Frog CSV exports into content audit spreadsheets (CSV or Excel). Use when asked to validate exports, generate page/file inventories, troubleshoot processing, or explain audit columns.
---

# Content Inventory Tool

## Requirements

Python 3.10+ with pandas 2.2+ (the redirect merge uses `include_groups`), openpyxl for Excel, and requests only for `--follow-redirects`. A shell and local filesystem access are needed to run the helpers. Input is four Screaming Frog CSV exports; Screaming Frog and authorized GA4 access are needed only to produce those exports. No service authentication is needed for local processing.

Resolve `SKILL_DIR` to the absolute directory containing the loaded `SKILL.md`, using the skill location supplied by the agent or locating this file. Set it explicitly (for example, `SKILL_DIR="/path/to/installed/content-inventory"`); do not derive it from the project working directory. Run project-relative commands from the working project and use `"$SKILL_DIR/..."` for companions.

## Safety and review

CSV exports and spreadsheets can contain private URLs, page text, analytics, and personal information. Keep processing local by default. Before enabling `--follow-redirects`, a human reviews the full URL set and possible redirect destinations: the helper sends requests to input URLs and redirect targets without an allowlist, so use only trusted public-site exports in an isolated network environment. `--domain` is a reporting flag, not a network boundary. Choose an output directory/prefix that will not overwrite needed files. A human checks row counts, redirect merging, formulas or external links in spreadsheet inputs, and the default FALSE legal-required column before sharing; that default is not a legal determination. Content decisions and client delivery remain with the human auditor.

Outside a verified secure sandbox, a human must read and understand unreviewed shell commands and generated code before execution. Always review MCP data-changing operations if an MCP alternative is used. Use least privilege; tool installation requires Security Team review and verification of upstream identity. Personal information requires approved tooling integrated with its source system; confidential information requires specifically approved tools; non-public information requires tools that neither train on nor retain it. Never send sensitive non-public data to public AI models. Stop when eligibility is unknown. An AI check does not replace human self-review before sharing, publishing, or handing work to another reviewer.


Transforms Screaming Frog CSV exports into client-ready audit spreadsheets with two pipelines: pages and files.

## Setup

The tool is bundled with this skill at `"$SKILL_DIR/scripts/"`. Before first run, check existing packages; if setup is authorized, install reviewed packages in a project virtual environment:

```bash
python3 -m pip install pandas openpyxl
# Only needed if using --follow-redirects:
python3 -m pip install requests
```

## Quick Start

```bash
python3 "$SKILL_DIR/scripts/run_inventory.py" \
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
python3 "$SKILL_DIR/scripts/check_inputs.py" \
  --pages <raw-pages.csv> \
  --orphans <orphan-pages.csv> \
  --files <raw-files.csv> \
  --inlinks <inlinks.csv>
```

This catches the most common error: passing the wrong Screaming Frog export to the wrong flag.

## Troubleshooting

Common issues:

- **KeyError on a column name** — Wrong SF export passed to wrong flag. Run `check_inputs.py` to diagnose.
- **ModuleNotFoundError: pandas/openpyxl** — Run `python3 -m pip install pandas openpyxl`.
- **Output has 0 rows** — All pages were 404, or the wrong file was passed to `--pages`.

For more, see [troubleshooting.md](references/troubleshooting.md).

## Development

No test suite is bundled here. Validate representative sanitized CSV fixtures and inspect generated rows before client delivery.

Source modules in `scripts/content_inventory/`: `cli.py` (arg parsing), `pages.py` (pages pipeline), `files.py` (files pipeline), `output.py` (formatting), `normalize.py` (URL normalization), `redirects.py` (redirect resolution), `filetypes.py` (file classification), `readability.py` (Flesch to grade).
