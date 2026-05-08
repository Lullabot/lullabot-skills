"""Files workflow pipeline — transforms raw Screaming Frog file exports + inlinks into a file inventory."""

import sys

import pandas as pd

from .filetypes import classify_file_type
from .normalize import normalize_url


def load_raw_files(filepath: str) -> pd.DataFrame:
    """Load relevant columns from a Screaming Frog files CSV."""
    df = pd.read_csv(filepath, low_memory=False)
    keep = {
        "Address": "file_url",
        "Title 1": "file_title",
        "Status Code": "status_code",
        "Size (bytes)": "size",
    }
    rename = {k: v for k, v in keep.items() if k in df.columns}
    df = df.rename(columns=rename)
    df = df[[v for v in rename.values()]].copy()
    df["normalized_url"] = df["file_url"].apply(normalize_url)
    return df


def load_inlinks(filepath: str) -> pd.DataFrame:
    """Load the inlinks reference CSV."""
    df = pd.read_csv(filepath, low_memory=False)
    # Normalize the target file URL (To column)
    df["normalized_url"] = df["To"].apply(normalize_url)
    # Normalize the source page URL (From column)
    df["source_url"] = df["From"]
    return df


def build_file_inventory(
    raw_files_path: str,
    inlinks_path: str,
) -> pd.DataFrame:
    """Build a deduplicated file inventory with lookups from the inlinks reference.

    Returns a DataFrame ready for output formatting.
    """
    raw = load_raw_files(raw_files_path)
    inlinks = load_inlinks(inlinks_path)
    print(f"Loaded {len(raw)} raw file rows, {len(inlinks)} inlinks rows", file=sys.stderr)

    # Filter out page URLs (.aspx, .html, .htm) from raw files
    page_extensions = r"\.(?:aspx|html|htm|php|jsp)(?:\?|$|#)"
    raw = raw[~raw["file_url"].str.lower().str.contains(page_extensions, na=False, regex=True)].copy()

    # Also filter inlinks To column similarly
    inlinks_files = inlinks[~inlinks["To"].str.lower().str.contains(page_extensions, na=False, regex=True)].copy()

    # Get unique normalized file URLs from both sources
    raw_urls = set(raw["normalized_url"].dropna().unique())
    inlink_urls = set(inlinks_files["normalized_url"].dropna().unique())
    all_urls = raw_urls | inlink_urls
    # Remove empty strings
    all_urls.discard("")
    print(f"Unique file URLs: {len(all_urls)}", file=sys.stderr)

    rows = []
    for norm_url in sorted(all_urls):
        # Look up file title from raw files first
        raw_match = raw[raw["normalized_url"] == norm_url]
        inlink_match = inlinks_files[inlinks_files["normalized_url"] == norm_url]

        # File title: prefer raw files Title 1, fall back to inlinks Anchor Text
        file_title = ""
        if not raw_match.empty:
            titles = raw_match["file_title"].dropna()
            if not titles.empty:
                file_title = str(titles.iloc[0]).strip()
        if not file_title and not inlink_match.empty:
            anchors = inlink_match["Anchor Text"].dropna()
            anchors = anchors[anchors.str.strip() != ""]
            if not anchors.empty:
                file_title = str(anchors.iloc[0]).strip()

        # File type: classify by URL extension
        file_type = classify_file_type(norm_url)

        # Anchor text: first non-empty from inlinks
        anchor_text = ""
        if not inlink_match.empty:
            anchors = inlink_match["Anchor Text"].dropna()
            anchors = anchors[anchors.str.strip() != ""]
            if not anchors.empty:
                anchor_text = str(anchors.iloc[0]).strip()

        # Source URLs: all unique From URLs, newline-separated
        source_urls = ""
        if not inlink_match.empty:
            sources = inlink_match["source_url"].dropna().unique()
            source_urls = "\n".join(sorted(set(str(s) for s in sources if str(s).strip())))

        # Alt text: first non-empty from inlinks
        alt_text = ""
        if not inlink_match.empty:
            alts = inlink_match["Alt Text"].dropna()
            alts = alts[alts.str.strip() != ""]
            if not alts.empty:
                alt_text = str(alts.iloc[0]).strip()

        # Size: from raw files or inlinks
        size = ""
        if not raw_match.empty:
            sizes = raw_match["size"].dropna()
            if not sizes.empty:
                size = sizes.iloc[0]
        if not size and not inlink_match.empty:
            sizes = inlink_match["Size"].dropna()
            sizes = sizes[sizes != 0]
            if not sizes.empty:
                size = sizes.iloc[0]

        rows.append({
            "file_title": file_title,
            "file_url": norm_url,
            "normalized_url": norm_url,
            "file_type": file_type,
            "anchor_text": anchor_text,
            "source_urls": source_urls,
            "alt_text": alt_text,
            "size": size,
        })

    result = pd.DataFrame(rows)
    print(f"Final file inventory: {len(result)} rows", file=sys.stderr)
    return result
