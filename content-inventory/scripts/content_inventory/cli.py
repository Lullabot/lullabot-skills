"""CLI entry point for content inventory automation."""

import argparse
import os
import sys

from .files import build_file_inventory
from .output import (
    format_files_csv,
    format_files_excel,
    format_pages_csv,
    format_pages_excel,
)
from .pages import process_pages


def main():
    parser = argparse.ArgumentParser(
        description="Generate content inventory audit sheets from Screaming Frog exports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python run_inventory.py \\
    --pages MEA-sf-raw-pages.csv \\
    --orphans MEA-sf-raw-orphan-pages.csv \\
    --files MEA-sf-raw-files.csv \\
    --inlinks MEA-sf-raw-files-inlinks.csv \\
    --domain energy.maryland.gov \\
    --prefix MEA
        """,
    )
    parser.add_argument("--pages", required=True, help="Path to Screaming Frog raw pages CSV")
    parser.add_argument("--orphans", required=True, help="Path to orphan pages CSV")
    parser.add_argument("--files", required=True, help="Path to Screaming Frog raw files CSV")
    parser.add_argument("--inlinks", required=True, help="Path to inlinks CSV")
    parser.add_argument("--domain", default="", help="Expected domain for rogue URL detection (e.g., energy.maryland.gov)")
    parser.add_argument("--follow-redirects", action="store_true", help="Follow HTTP redirect chains (hits live site)")
    parser.add_argument("--format", choices=["csv", "xlsx"], default="csv", help="Output format (default: csv)")
    parser.add_argument("--output-dir", default=".", help="Output directory (default: current directory)")
    parser.add_argument("--prefix", default="output", help="Output filename prefix (default: output)")

    args = parser.parse_args()

    # Validate inputs exist
    for path, label in [(args.pages, "pages"), (args.orphans, "orphans"), (args.files, "files"), (args.inlinks, "inlinks")]:
        if not os.path.exists(path):
            print(f"Error: {label} file not found: {path}", file=sys.stderr)
            sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    ext = args.format

    # Process pages
    print("=== Processing Pages ===", file=sys.stderr)
    pages_df = process_pages(
        raw_pages_path=args.pages,
        orphan_pages_path=args.orphans,
        expected_domain=args.domain,
        follow_redirects_http=args.follow_redirects,
    )

    pages_output = os.path.join(args.output_dir, f"{args.prefix}-audit-all-pages.{ext}")
    if ext == "csv":
        format_pages_csv(pages_df, pages_output)
    else:
        format_pages_excel(pages_df, pages_output)

    # Process files
    print("\n=== Processing Files ===", file=sys.stderr)
    files_df = build_file_inventory(
        raw_files_path=args.files,
        inlinks_path=args.inlinks,
    )

    files_output = os.path.join(args.output_dir, f"{args.prefix}-audit-all-files.{ext}")
    if ext == "csv":
        format_files_csv(files_df, files_output)
    else:
        format_files_excel(files_df, files_output)

    print(f"\nDone. Pages: {len(pages_df)} rows, Files: {len(files_df)} rows", file=sys.stderr)


if __name__ == "__main__":
    main()
