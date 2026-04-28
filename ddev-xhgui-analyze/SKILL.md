---
name: ddev-xhgui-analyze
description: Analyze an xhgui/xhprof profile run from a DDEV environment. Provide one run ID for standalone analysis, or two for before/after comparison.
argument-hint: "<run_id> [compare_run_id]"
disable-model-invocation: true
---
# Analyze xhgui Profile Run

You are a performance analysis specialist. Your job is to fetch xhprof profile data from the xhgui service in a DDEV environment, analyze it, and present a clear summary of where time is being spent.

## Prerequisites

This skill requires:

1. **DDEV** — You must be working inside a DDEV project (a directory with a `.ddev/` config). All commands below use `ddev exec`.
2. **The xhgui add-on** — xhgui must already be installed and configured. See [DDEV xhprof/xhgui docs](https://docs.ddev.com/en/stable/users/debugging-profiling/xhprof-profiling/) for setup instructions.
3. **At least one captured profile run** — You need a run ID from xhgui. You can find run IDs by browsing the xhgui UI (typically at `https://<project>.ddev.site:8143`) or by querying the database directly:
   ```bash
   ddev exec mysql -u db -pdb xhgui -e "SELECT id, url, request_ts FROM results ORDER BY request_ts DESC LIMIT 10"
   ```

If any prerequisite is not met, inform the user and point them to the DDEV docs linked above.

## Arguments

The user provides: $ARGUMENTS

Parse the arguments:
- If one ID is provided: perform a **standalone analysis** of that run.
- If two IDs are provided: the first is the **baseline** run, the second is the **after** run. Perform a **comparison analysis**.

## Step 1: Fetch run metadata

Query the xhgui MySQL database for run-level summary data. The xhgui DDEV add-on stores profiling data in the `xhgui` database on the `db` service using PDO/MySQL.

```bash
ddev exec mysql -u db -pdb xhgui -e "SELECT id, url, simple_url, request_ts, main_wt, main_ct, main_cpu, main_mu, main_pmu FROM results WHERE id = '<run_id>'"
```

Do this for each run ID provided. Verify the run exists before proceeding.

## Step 2: Export profile data

Export the full profile JSON (stored as `longtext` in the `profile` column) to `/tmp` inside the container:

```bash
ddev exec bash << 'EOF'
mysql -u db -pdb xhgui -N -e "SELECT profile FROM results WHERE id = '<run_id>'" > /tmp/xhgui_profile_<run_id>.json
EOF
```

## Step 3: Analyze the profile

Pipe a PHP script into the container via `ddev exec php` using a heredoc. The script reads the exported JSON from the container's `/tmp`. PHP is always available in DDEV containers.

```bash
ddev exec php << 'PHPEOF'
<?php
$profile = json_decode(file_get_contents('/tmp/xhgui_profile_<run_id>.json'), true);
// ... analysis code ...
PHPEOF
```

The analysis should produce:

### 3a. Top 30 functions by inclusive wall time
The profile is a dictionary keyed by `"caller==>callee"` with values `{wt, ct, cpu, mu, pmu}`. Aggregate inclusive wall time per callee across all callers.

### 3b. HTTP / external call breakdown
Filter for functions containing: `guzzle`, `curl`, `http`, `stream_`. Show the top entries by wall time.

### 3c. Application-specific hotspots
Look for functions that belong to the project's own codebase (non-vendor, non-core). Identify custom modules, services, or controllers that appear in the top functions by wall time. Cross-reference with the project directory structure to categorize them.

Also look for hotspots in these common areas:
- AI/ML providers
- External API calls
- Database operations
- Queue/batch processing

### 3d. Call chain analysis
For the top time-consuming leaf functions (functions where most time is actually spent, not just passed through), trace the caller chain by examining `caller==>callee` keys.

## Step 4: Cross-reference with codebase

For the most expensive custom (non-vendor) functions found in the profile, use Grep/Glob to find them in the codebase and understand what the code is actually doing. This provides context for the recommendations.

## Step 5: Report

Present a structured summary:

### For standalone analysis:
1. **Run overview**: URL, total wall time, memory, date
2. **Time breakdown table**: Top components by wall time (as a markdown table)
3. **HTTP call analysis**: How many external calls, to where, total time
4. **Hotspots**: The most expensive functions with codebase context
5. **Recommendations**: Actionable suggestions ranked by estimated impact

### For comparison analysis:
Include everything above for the "after" run, plus:
1. **Before vs After table**: Side-by-side metrics for key functions
2. **What improved**: Functions that got faster or were called fewer times
3. **What didn't change**: Remaining bottlenecks
4. **What regressed**: Anything that got slower (if applicable)
5. **Next steps**: What to optimize next

## Notes

- Wall time (`wt`) is in **microseconds** in the profile data. Convert to milliseconds or seconds for display.
- Call count (`ct`) indicates how many times a function was invoked.
- `main_wt` in the results table is also in microseconds.
- `request_ts` is a Unix timestamp.
- The profile keys use `==>` as the caller/callee separator.
- Memory values (`mu`, `pmu`) are in bytes.
