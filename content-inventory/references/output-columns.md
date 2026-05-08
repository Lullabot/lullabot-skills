# Output Column Specifications

Both output files use a two-header-row format. Row 1 contains category headers spanning multiple columns. Row 2 contains individual column descriptions (with embedded newlines in Excel).

## Pages Audit Sheet

**Sheet name (Excel)**: "Inventory All Pages"

### Category headers (Row 1)

| Columns | Category |
|---------|----------|
| 1-6 | Page information (pulled and provided) |
| 7-11 | Review criteria |
| 12-14 | Decisions & comments |
| 15-16 | Responsibilities |
| 17 | For Lullabot |

### Column details (Row 2)

| # | Header | Description | Data source |
|---|--------|-------------|-------------|
| 1 | Page title | The title of this page. | `<title>` tag from Screaming Frog |
| 2 | Page URL | The URL to this page. | Normalized URL (no protocol, www, trailing slashes) |
| 3 | Redirect, Plaintext | Convert this to the main page column for agency once cleanup is done | Redirect URL if redirected, otherwise `https://{normalized_url}` |
| 4 | GA page views | Google Analytics data (1 year prior to scan). | GA4 Views from Screaming Frog |
| 5 | Reading level: Score | _(no description)_ | Flesch Reading Ease Score |
| 6 | Reading level: Grade | Aim for Normal or easier (Normal equals 8th Grade). | Converted from score. Blank input stays blank. |
| 7 | Audience | Who is this content for and how will it serve them? | _Empty — for auditor_ |
| 8 | Up to date | Content is current and up-to-date. | _Empty — for auditor_ |
| 9 | Accuracy | Content should be accurate, free of errors. | _Empty — for auditor_ |
| 10 | Uniqueness | Content should be unique. | _Empty — for auditor_ |
| 11 | High quality | Grade 1-5 (1 = low, 5 = high). | _Empty — for auditor_ |
| 12 | Keep, edit, delete or consolidate? | If consolidating, note what page to combine it with. | _Empty — for auditor_ |
| 13 | Required by law | This content is required to be on the website. | Pre-filled: `FALSE` |
| 14 | Notes, questions, comments | Leave any notes, gut reactions, thoughts. | _Empty — for auditor_ |
| 15 | Reviewed by | | _Empty — for auditor_ |
| 16 | Stakeholder (if applicable) | | _Empty — for auditor_ |
| 17 | Notes | | _Empty — for Lullabot_ |

### Data behaviors — pages

- **Page URL** (col 2): When multiple URLs redirect to the same destination, they're merged into a single row with source URLs joined by `\n` (newline) in this cell.
- **Redirect, Plaintext** (col 3): If the page has no redirect, this reconstructs the full URL as `https://{normalized_url}`. If it does redirect, shows the redirect target.
- **Reading level: Grade** (col 6): Blank/NaN scores produce empty string (not "5th grade"). This is an intentional bug fix from the old Google Sheets workflow.

## Files Audit Sheet

**Sheet name (Excel)**: "All Files"

### Category headers (Row 1)

| Columns | Category |
|---------|----------|
| 1-8 | File information (pulled and provided) |
| 9-13 | Review criteria |
| 14-16 | Decisions & comments |
| 17-18 | Responsibilities |
| 19 | For Lullabot |

### Column details (Row 2)

| # | Header | Description | Data source |
|---|--------|-------------|-------------|
| 1 | File title | The title of this file. | Title 1 from SF, fallback to inlinks Anchor Text |
| 2 | File URL | The URL to this file. | Full file URL |
| 3 | File URL without formatting | (http(s), www. & trailing slashes) | Normalized URL |
| 4 | File type | The type of file. | Classified by extension: PDF, Image, GIF, Word document, Spreadsheet, PPT, Video, Archive, CSV, Text, or uppercase extension |
| 5 | Anchor text | The text of the link to this file. | First non-empty anchor text from inlinks |
| 6 | Source | The page that has or links to this file. | All unique source page URLs, newline-separated |
| 7 | Alt text | The image alt text. | First non-empty alt text from inlinks |
| 8 | Size | Size of this file (bytes). | From raw files or inlinks |
| 9 | Audience | Who is this content for? | _Empty — for auditor_ |
| 10 | Up to date | Content is current and up-to-date. | _Empty — for auditor_ |
| 11 | Accuracy | Content should be accurate, free of errors. | _Empty — for auditor_ |
| 12 | Uniqueness | Content should be unique. | _Empty — for auditor_ |
| 13 | High quality | Grade 1-5 (1 = low, 5 = high). | _Empty — for auditor_ |
| 14 | Keep, edit, delete or consolidate? | If consolidating, note what page to combine it with. | _Empty — for auditor_ |
| 15 | Required by law | This content is required to be on the website. | Pre-filled: `FALSE` |
| 16 | Notes, questions, comments | Leave any notes, gut reactions, thoughts. | _Empty — for auditor_ |
| 17 | Reviewed by | | _Empty — for auditor_ |
| 18 | Stakeholder (if applicable) | | _Empty — for auditor_ |
| 19 | Notes | | _Empty — for Lullabot_ |

### Data behaviors — files

- **Source** (col 6): Multiple source pages are joined by `\n` (newline) in a single cell. In Excel, cells with newlines have wrap_text enabled.
- **File type** (col 4): Classified from URL extension. Supported types: PDF, Image (png/jpg/jpeg/jfif/svg), GIF, Word document (doc/docx), Spreadsheet (xls/xlsx), XLSM, PPT (ppt/pptx), Video (mp4/avi/mov/wmv), Archive (zip), CSV, Text (txt). Unknown extensions shown as uppercase.
