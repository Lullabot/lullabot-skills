"""Pages workflow pipeline — transforms raw Screaming Frog exports into a deduplicated content inventory."""

import sys

import pandas as pd

from .normalize import normalize_url
from .readability import flesch_to_grade
from .redirects import resolve_redirects_from_csv, resolve_redirects_via_http


# Columns we need from the raw Screaming Frog pages export
RAW_COLUMNS = {
    "Address": "address",
    "Title 1": "page_title",
    "Status Code": "status_code",
    "Flesch Reading Ease Score": "reading_score",
    "GA4 Views": "ga_views",
    "Redirect URL": "redirect_url",
}


def load_raw_pages(filepath: str) -> pd.DataFrame:
    """Load and extract relevant columns from a Screaming Frog pages CSV."""
    df = pd.read_csv(filepath, low_memory=False)
    # Rename only the columns we care about
    rename = {k: v for k, v in RAW_COLUMNS.items() if k in df.columns}
    df = df.rename(columns=rename)
    # Keep only our columns
    keep = [v for v in rename.values()]
    df = df[keep].copy()
    # Add normalized URL
    df["normalized_url"] = df["address"].apply(normalize_url)
    return df


def load_orphan_pages(filepath: str) -> pd.DataFrame:
    """Load orphan pages CSV. These have only URL and Source columns,
    with URLs already lacking the https:// prefix."""
    df = pd.read_csv(filepath, low_memory=False)
    # Map the URL column to our schema
    url_col = "URL" if "URL" in df.columns else df.columns[0]
    df = df.rename(columns={url_col: "address"})
    df["normalized_url"] = df["address"].apply(normalize_url)
    # Add empty columns to match raw pages schema
    for col in ["page_title", "status_code", "reading_score", "ga_views", "redirect_url"]:
        if col not in df.columns:
            df[col] = pd.NA
    keep = ["address", "page_title", "status_code", "reading_score", "ga_views", "redirect_url", "normalized_url"]
    return df[keep].copy()


def remove_404s(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with 404 status codes."""
    df["status_code"] = pd.to_numeric(df["status_code"], errors="coerce")
    return df[df["status_code"] != 404].copy()


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate on normalized URL with conflict resolution:
    - page_title: first non-empty
    - status_code: first non-empty
    - ga_views: max
    - reading_score: max
    - redirect_url: first non-empty
    """
    df["ga_views"] = pd.to_numeric(df["ga_views"], errors="coerce")
    df["reading_score"] = pd.to_numeric(df["reading_score"], errors="coerce")

    def first_non_empty(series):
        """Return first non-null, non-empty value."""
        for val in series:
            if pd.notna(val) and str(val).strip():
                return val
        return pd.NA

    agg = df.groupby("normalized_url", sort=False).agg(
        page_title=("page_title", first_non_empty),
        status_code=("status_code", first_non_empty),
        ga_views=("ga_views", "max"),
        reading_score=("reading_score", "max"),
        redirect_url=("redirect_url", first_non_empty),
    ).reset_index()

    return agg


def merge_redirect_duplicates(df: pd.DataFrame, redirects: dict) -> pd.DataFrame:
    """When multiple normalized URLs redirect to the same final destination,
    merge them into a single row with all source URLs preserved."""
    if not redirects:
        return df

    # Add redirect target column
    df["redirect_target"] = df["normalized_url"].map(
        lambda u: normalize_url(redirects.get(u, ""))
    )
    df["redirect_full_url"] = df["normalized_url"].map(
        lambda u: redirects.get(u, "")
    )

    # Separate redirecting and non-redirecting rows
    has_redirect = df["redirect_target"].astype(bool)
    non_redirect = df[~has_redirect].copy()
    redirecting = df[has_redirect].copy()

    if redirecting.empty:
        df.drop(columns=["redirect_target", "redirect_full_url"], inplace=True)
        return df

    # Group redirecting rows by their target
    def merge_group(group):
        urls = list(group["normalized_url"])
        return pd.Series({
            "normalized_url": "\n".join(urls),
            "page_title": group["page_title"].dropna().iloc[0] if not group["page_title"].dropna().empty else pd.NA,
            "status_code": group["status_code"].dropna().iloc[0] if not group["status_code"].dropna().empty else pd.NA,
            "ga_views": group["ga_views"].max(),
            "reading_score": group["reading_score"].max(),
            "redirect_url": group["redirect_full_url"].iloc[0],
        })

    merged = redirecting.groupby("redirect_target", sort=False).apply(merge_group, include_groups=False).reset_index()

    # Check if any redirect targets match existing non-redirect rows
    # If so, merge the URL lists
    for idx, row in merged.iterrows():
        target = row["redirect_target"]
        match = non_redirect[non_redirect["normalized_url"] == target]
        if not match.empty:
            match_idx = match.index[0]
            # Append redirect source URLs to the target row
            existing_urls = non_redirect.at[match_idx, "normalized_url"]
            new_urls = row["normalized_url"]
            non_redirect.at[match_idx, "normalized_url"] = f"{existing_urls}\n{new_urls}"
            non_redirect.at[match_idx, "redirect_url"] = row["redirect_url"]
            # Take max GA views and reading score
            if pd.notna(row["ga_views"]):
                existing = non_redirect.at[match_idx, "ga_views"]
                non_redirect.at[match_idx, "ga_views"] = max(existing, row["ga_views"]) if pd.notna(existing) else row["ga_views"]
            merged.drop(idx, inplace=True)

    # Combine
    merged = merged.drop(columns=["redirect_target"])
    non_redirect = non_redirect.drop(columns=["redirect_target", "redirect_full_url"], errors="ignore")
    result = pd.concat([non_redirect, merged], ignore_index=True)
    return result


def filter_non_page_urls(df: pd.DataFrame) -> pd.DataFrame:
    """Remove document/file URLs (PDFs, images, etc.) that don't belong in the pages inventory,
    and remove custom error pages (e.g., pagenotfound.aspx)."""
    file_extensions = r"\.(?:pdf|doc|docx|xls|xlsx|xlsm|ppt|pptx|csv|zip|png|jpg|jpeg|gif|svg|mp4|avi|mov|wmv|txt)(?:\?|$|#)"
    is_file = df["normalized_url"].str.lower().str.contains(file_extensions, na=False, regex=True)

    return df[~is_file].copy()


def flag_rogue_urls(df: pd.DataFrame, expected_domain: str) -> list[str]:
    """Identify URLs that don't belong to the expected domain.
    Returns list of rogue URLs for reporting."""
    rogue = []
    for url in df["normalized_url"]:
        for u in str(url).split("\n"):
            u = u.strip()
            if u and not u.startswith(expected_domain.lower()):
                rogue.append(u)
    return rogue


def process_pages(
    raw_pages_path: str,
    orphan_pages_path: str,
    expected_domain: str = "",
    follow_redirects_http: bool = False,
) -> pd.DataFrame:
    """Run the full pages pipeline. Returns a DataFrame ready for output formatting."""
    # Step 1: Load raw pages
    raw = load_raw_pages(raw_pages_path)
    print(f"Loaded {len(raw)} raw page rows", file=sys.stderr)

    # Step 2: Remove 404s
    raw = remove_404s(raw)
    print(f"After removing 404s: {len(raw)} rows", file=sys.stderr)

    # Step 3: Load and append orphan pages
    orphans = load_orphan_pages(orphan_pages_path)
    print(f"Loaded {len(orphans)} orphan page rows", file=sys.stderr)
    combined = pd.concat([raw, orphans], ignore_index=True)
    print(f"Combined: {len(combined)} rows", file=sys.stderr)

    # Step 4: Deduplicate
    deduped = deduplicate(combined)
    print(f"After deduplication: {len(deduped)} rows", file=sys.stderr)

    # Step 4b: Filter out non-page URLs (documents, error pages)
    deduped = filter_non_page_urls(deduped)
    print(f"After filtering non-page URLs: {len(deduped)} rows", file=sys.stderr)

    # Step 5: Resolve redirects
    redirects = resolve_redirects_from_csv(raw)
    verified_urls = {}  # Maps normalized URL -> verified final URL (for redirect column)
    if follow_redirects_http:
        # Probe all URLs via HTTP to discover redirects (mirrors getFinalUrl behavior)
        all_urls = list(deduped["normalized_url"])
        print(f"Following redirects for {len(all_urls)} URLs via HTTP...", file=sys.stderr)
        http_results = resolve_redirects_via_http(all_urls)
        for source_url, final_url in http_results.items():
            verified_urls[source_url] = final_url
            source_norm = normalize_url(source_url)
            final_norm = normalize_url(final_url)
            if final_norm and final_norm != source_norm and not final_url.startswith("Error"):
                redirects[source_url] = final_url
    print(f"Found {len(redirects)} actual redirects", file=sys.stderr)

    # Step 6: Merge redirect duplicates
    result = merge_redirect_duplicates(deduped, redirects)
    print(f"After merging redirects: {len(result)} rows", file=sys.stderr)

    # Step 6b: Add redirect targets not already in inventory
    if redirects:
        existing_urls = set()
        for url_cell in result["normalized_url"]:
            for u in str(url_cell).split("\n"):
                u = u.strip()
                if u:
                    existing_urls.add(u)

        new_targets = []
        for source_url, target_full_url in redirects.items():
            target_norm = normalize_url(target_full_url)
            if target_norm and target_norm not in existing_urls and not target_full_url.startswith("Error"):
                existing_urls.add(target_norm)  # avoid adding duplicates
                new_targets.append({
                    "normalized_url": target_norm,
                    "page_title": pd.NA,
                    "status_code": pd.NA,
                    "ga_views": pd.NA,
                    "reading_score": pd.NA,
                    "redirect_url": target_full_url,
                })

        if new_targets:
            new_df = pd.DataFrame(new_targets)
            result = pd.concat([result, new_df], ignore_index=True)
            print(f"Added {len(new_targets)} redirect target URLs not in crawl data", file=sys.stderr)

    # Step 7: Flag rogue URLs
    if expected_domain:
        rogue = flag_rogue_urls(result, expected_domain)
        if rogue:
            print(f"Warning: {len(rogue)} rogue URLs found outside {expected_domain}:", file=sys.stderr)
            for u in rogue[:10]:
                print(f"  {u}", file=sys.stderr)
            if len(rogue) > 10:
                print(f"  ... and {len(rogue) - 10} more", file=sys.stderr)

    # Step 8: Populate redirect column with verified URLs
    if verified_urls:
        # Probe any new rows (redirect targets) that weren't in the original batch
        unprobed = [u for u in result["normalized_url"] if u not in verified_urls and "\n" not in str(u)]
        if unprobed:
            print(f"Verifying {len(unprobed)} newly-discovered URLs via HTTP...", file=sys.stderr)
            new_verified = resolve_redirects_via_http(unprobed)
            verified_urls.update(new_verified)

        def get_verified_url(row):
            # Keep existing redirect_url if already set (e.g. from redirect target addition)
            existing = row.get("redirect_url", "")
            if pd.notna(existing) and str(existing).strip():
                return existing
            primary = str(row["normalized_url"]).split("\n")[0].strip()
            return verified_urls.get(primary, "")
        result["redirect_url"] = result.apply(get_verified_url, axis=1)

    # Step 9: Convert reading scores to grade levels
    result["reading_grade"] = result["reading_score"].apply(flesch_to_grade)

    return result
