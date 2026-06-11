---
name: broken-link-report
description: "Turn a Screaming Frog 'All Outlinks' CSV export into a clean broken-links report (Excel workbook). Use whenever the user has a Screaming Frog outlinks export and wants to find, triage, report on, or clean up broken links — including phrasings like 'broken link report', 'dead links', 'find the 404s', 'clean up this outlinks export', 'which links are broken', or 'report on bad links from this crawl'. Trigger even if the user hands over a CSV with From/To/Status Code columns and asks what's broken."
---

# Broken Link Report

## What this does

A Screaming Frog outlinks export is mostly noise for broken-link triage —
typically 90%+ of rows are successful (200) or redirects (301/302). This skill
filters an export down to the links that are actually broken and writes a
formatted Excel workbook with two views: a deduplicated **Summary** (one row per
broken URL, ranked by how many pages link to it) and a full **Detail** sheet (one
row per broken link, so each break can be traced to its source page).

## When to use it

Use it whenever someone has a Screaming Frog "All Outlinks" CSV (columns like
`Type, From, To, Anchor Text, Status Code, Status, ...`) and wants to know what's
broken. The input is usually named something like `all-pages-outlinks.csv` or
`*_all_outlinks.csv`.

## How to run it

The work is done by a single script. Run it on the input CSV:

```bash
python3 scripts/clean_broken_links.py <path-to-outlinks.csv> [output.xlsx]
```

If no output path is given, it writes `<YYYY-MM-DD>-broken-links.xlsx` next to the
input file. The script depends on `openpyxl` (install with
`pip install openpyxl --break-system-packages` if it's missing).

After it runs, present the workbook to the user and call out the highest-impact
findings — especially any URL with a high "Times Linked" count, which usually
means a broken link in a shared header/footer/nav that a single fix will clear
everywhere.

## What counts as "broken" (the filtering logic)

The point of the skill is judgment about what's signal vs. noise. The rules are
host-agnostic so they work on any site's export:

- **Dropped — not broken:** `200 OK`, and all redirects (`301`, `302`, `303`,
  `307`, `308`). A redirect resolves somewhere, so it isn't a dead link.
- **Dropped — uncrawlable, not broken:** status code `0` with status text
  "Blocked by robots.txt". The crawler was told to stay out; that's not the same
  as the link being dead.
- **Dropped — not a real link:** any `To` URL containing
  `/cdn-cgi/l/email-protection`. This is Cloudflare's email-obfuscation/spam
  protection. Screaming Frog reports it as a 404, but Cloudflare rewrites it at
  render time, so it's a false positive. This fragment is the same on every
  Cloudflare-fronted site, which is why it's matched by path, not by host.
- **Kept — genuinely broken:** `404`, `403`, other `4xx`, all `5xx`, and status
  code `0` for real connection failures (DNS lookup failed, connection refused,
  timeout).

A note on `403 Forbidden`: many 403s are external sites bot-blocking the crawler
rather than truly broken resources. They're kept in the broken list per the
report's design, but each 403 row is tagged in a `Flag` column reading
"Likely bot-blocked - verify manually" and tinted amber, so a human can tell at a
glance which "breaks" need a manual check before being treated as dead. The
Summary sheet also naturally tames them — a domain that blocks the crawler
collapses into a single row (e.g. one `Times Linked: 681` entry) instead of
flooding the report. When presenting results, call out high-count flagged hosts
as needing verification rather than as confirmed dead links.

## Adapting the rules

If a particular export has its own noise pattern (a different obfuscation scheme,
an internal hostname that should be ignored, a status code the user wants
treated differently), edit the rule constants at the top of
`scripts/clean_broken_links.py` — `NON_BROKEN_CODES`, `EMAIL_PROTECTION_FRAGMENT`,
and the `is_noise()` function are written to be easy to adjust. Keep the changes
host-agnostic where possible so the skill stays reusable across crawls.

## Output reference

**Summary sheet** (start here): `To`, `Host`, `Status Code`, `Status`,
`Times Linked` (how many links point at this URL), `Source Pages` (how many
distinct pages contain those links), `Flag` (advisory — set for 403s). Sorted
most-linked first.

**Detail sheet**: `From`, `To`, `Anchor Text`, `Status Code`, `Status`, `Type`,
`Link Position`, `Flag`. One row per broken link, sorted by status code then
target URL, so you can find every page that needs editing.

Rows carrying a `Flag` value (currently the 403 bot-block advisory) are tinted
amber on both sheets for quick scanning.
