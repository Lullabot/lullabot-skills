# Troubleshooting

## Missing Columns (KeyError)

**Symptom**: `KeyError: 'Address'` or similar column name error.

**Cause**: Wrong Screaming Frog export passed to the wrong CLI flag. Most common: passing inlinks to `--files` or vice versa.

**Fix**: Run `check_inputs.py` to validate all 4 files have expected columns. Re-export from Screaming Frog if needed.

## ModuleNotFoundError

**Symptom**: `ModuleNotFoundError: No module named 'pandas'` (or `openpyxl`, `requests`).

**Fix**:
```bash
pip install pandas openpyxl
# For --follow-redirects:
pip install requests
```

If using a virtual environment, ensure it's activated first.

## Empty Output (0 Rows)

**Symptom**: Output file has headers but no data rows.

**Possible causes**:
- All pages in the raw CSV have 404 status codes (removed in step 2 of the pipeline)
- Wrong file passed to `--pages` (e.g., the files CSV instead of pages CSV)
- The CSV is empty or has only header rows

**Diagnosis**: Check the raw CSV row count and status code distribution:
```bash
# Count rows
wc -l raw-pages.csv
# Check status codes
cut -d',' -f<status-code-column> raw-pages.csv | sort | uniq -c
```

## Unexpected Row Counts

**Too many rows**: Orphan pages can contribute thousands of URLs. The MEA sample has 22,385 orphan pages vs 258 raw pages. After dedup the count drops significantly, but orphans often dominate.

**Too few rows**: Deduplication merges rows on normalized URL. Multiple URLs that differ only in protocol, www prefix, trailing slashes, query params, or fragments collapse to one row. Redirect merging further reduces count when multiple URLs redirect to the same destination.

## Rogue URL Warnings

**Symptom**: Tool prints warnings about off-domain URLs.

**Cause**: The crawl picked up URLs on a different domain than `--domain`. This happens with cross-domain redirects, embedded content from other sites, or subdomains.

**Fix**: These are warnings only — rogue URLs are flagged in the output but not removed. Review them in the audit sheet. If `--domain` is not set, no rogue URL detection occurs.

## --follow-redirects Timeouts

**Symptom**: Tool hangs or throws connection errors during redirect resolution.

**Causes**:
- Target site is slow or rate-limiting requests
- Network/firewall issues
- DNS resolution failures

**Fix**: The tool adds a 0.2s delay between requests and follows up to 10 redirect hops. For persistent issues:
- Try without `--follow-redirects` (uses CSV-based redirect data from Screaming Frog instead)
- Check network connectivity to the target domain
- Try again later if the site is rate-limiting

## GA4 Views Column Missing from SF Export

**Symptom**: GA4 Views column is empty or absent in the raw pages CSV.

**Fix**: In Screaming Frog, go to Configuration > API Access > Google Analytics. Connect your GA4 property. Then re-crawl the site. GA4 data is fetched during the crawl, not after.

## Reading Score Column Missing from SF Export

**Symptom**: Flesch Reading Ease Score column is empty or absent.

**Fix**: In Screaming Frog, go to Configuration > Content > Readability. Enable "Flesch Reading Ease". Re-crawl the site. Readability analysis must be enabled before the crawl.

## Excel Formatting Issues

**Symptom**: Excel output looks wrong — missing bold headers, no text wrapping, etc.

**Fix**: Ensure `openpyxl` is up to date: `pip install --upgrade openpyxl`. The tool requires openpyxl for Excel output and applies bold fonts, text wrapping, and vertical alignment to headers.
