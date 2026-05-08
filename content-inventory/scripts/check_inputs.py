#!/usr/bin/env python3
"""Validate Screaming Frog CSV inputs before running the content inventory tool.

Checks that each input file has the expected column headers. Catches the most
common error: passing the wrong SF export to the wrong CLI flag.
"""

import argparse
import csv
import sys


EXPECTED = {
    "pages": {
        "required": ["Address", "Status Code"],
        "recommended": ["Title 1", "Flesch Reading Ease Score", "GA4 Views", "Redirect URL"],
    },
    "orphans": {
        "required": ["URL"],
        "recommended": [],
    },
    "files": {
        "required": ["Address"],
        "recommended": ["Title 1", "Status Code", "Size (bytes)"],
    },
    "inlinks": {
        "required": ["From", "To"],
        "recommended": ["Anchor Text", "Alt Text", "Size"],
    },
}


def read_headers(filepath):
    """Read only the first row of a CSV to get column headers."""
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        return next(reader, [])


def check_file(label, filepath):
    """Check a single file against expected columns. Returns (errors, warnings)."""
    errors = []
    warnings = []

    try:
        headers = read_headers(filepath)
    except FileNotFoundError:
        return [f"File not found: {filepath}"], []
    except Exception as e:
        return [f"Could not read {filepath}: {e}"], []

    if not headers:
        return [f"{filepath} appears empty (no header row)"], []

    header_set = set(headers)
    spec = EXPECTED[label]

    for col in spec["required"]:
        if col not in header_set:
            errors.append(f"Missing required column '{col}'")

    for col in spec["recommended"]:
        if col not in header_set:
            warnings.append(f"Missing recommended column '{col}'")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validate Screaming Frog CSV inputs for the content inventory tool."
    )
    parser.add_argument("--pages", required=True, help="Path to raw pages CSV")
    parser.add_argument("--orphans", required=True, help="Path to orphan pages CSV")
    parser.add_argument("--files", required=True, help="Path to raw files CSV")
    parser.add_argument("--inlinks", required=True, help="Path to inlinks CSV")
    args = parser.parse_args()

    all_ok = True
    inputs = [
        ("pages", args.pages),
        ("orphans", args.orphans),
        ("files", args.files),
        ("inlinks", args.inlinks),
    ]

    for label, filepath in inputs:
        errors, warnings = check_file(label, filepath)
        if errors or warnings:
            print(f"\n  --{label} ({filepath}):")
            for e in errors:
                print(f"    ERROR: {e}")
                all_ok = False
            for w in warnings:
                print(f"    WARNING: {w}")
        else:
            print(f"  --{label}: OK ({filepath})")

    if all_ok:
        print("\nAll input files look good.")
        sys.exit(0)
    else:
        print("\nFix the errors above before running the content inventory tool.")
        sys.exit(1)


if __name__ == "__main__":
    main()
