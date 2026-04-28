#!/usr/bin/env python3
"""
compare_crawls.py - Compare two LibreCrawl results for month-over-month analysis

Usage:
    ./scripts/compare_crawls.py <current.json> <previous.json> [output.md]

Arguments:
    current  - Current month's crawl results (JSON)
    previous - Previous month's crawl results (JSON)
    output   - Optional output file for markdown report (default: stdout)

Example:
    ./scripts/compare_crawls.py month2.json month1.json comparison-report.md
"""

import sys
import json
from collections import Counter
from datetime import datetime

def load_crawl(file_path):
    """Load crawl results from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in: {file_path}", file=sys.stderr)
        sys.exit(1)

def calculate_change(current, previous):
    """Calculate change and percentage"""
    change = current - previous
    if previous == 0:
        pct = 100 if current > 0 else 0
    else:
        pct = (change / previous) * 100
    return change, pct

def format_change(change, pct, inverse=False):
    """Format change with emoji indicator"""
    # inverse=True means lower is better (like issue count)
    if change == 0:
        return f"→ {change:+d} (0%)"

    if inverse:
        emoji = "⬇️" if change < 0 else "⬆️"
        sign = "✓" if change < 0 else "⚠️"
    else:
        emoji = "⬆️" if change > 0 else "⬇️"
        sign = "✓" if change > 0 else "⚠️"

    return f"{emoji} {change:+d} ({pct:+.1f}%) {sign}"

def compare_crawls(current_data, previous_data):
    """Generate comparison report"""

    current_stats = current_data.get('stats', {})
    previous_stats = previous_data.get('stats', {})

    current_issues = current_data.get('issues', [])
    previous_issues = previous_data.get('issues', [])

    current_results = current_data.get('results', [])
    previous_results = previous_data.get('results', [])

    report = []

    # Header
    report.append("# SEO Crawl Comparison Report")
    report.append("")
    report.append(f"**Current Crawl:** {current_data.get('crawl_date', 'Unknown')}")
    report.append(f"**Previous Crawl:** {previous_data.get('crawl_date', 'Unknown')}")
    report.append(f"**Site:** {current_data.get('url', 'Unknown')}")
    report.append("")
    report.append("---")
    report.append("")

    # Executive Summary
    report.append("## Executive Summary")
    report.append("")

    total_issues_curr = len(current_issues)
    total_issues_prev = len(previous_issues)
    issues_change, issues_pct = calculate_change(total_issues_curr, total_issues_prev)

    report.append(f"**Total Issues:** {total_issues_prev} → {total_issues_curr} {format_change(issues_change, issues_pct, inverse=True)}")
    report.append("")

    # Issue breakdown by severity
    curr_errors = len([i for i in current_issues if i.get('type') == 'error'])
    prev_errors = len([i for i in previous_issues if i.get('type') == 'error'])
    errors_change, errors_pct = calculate_change(curr_errors, prev_errors)

    curr_warnings = len([i for i in current_issues if i.get('type') == 'warning'])
    prev_warnings = len([i for i in previous_issues if i.get('type') == 'warning'])
    warnings_change, warnings_pct = calculate_change(curr_warnings, prev_warnings)

    report.append(f"**Critical Errors:** {prev_errors} → {curr_errors} {format_change(errors_change, errors_pct, inverse=True)}")
    report.append(f"**Warnings:** {prev_warnings} → {curr_warnings} {format_change(warnings_change, warnings_pct, inverse=True)}")
    report.append("")

    # Pages crawled
    pages_curr = current_stats.get('crawled', 0)
    pages_prev = previous_stats.get('crawled', 0)
    pages_change, pages_pct = calculate_change(pages_curr, pages_prev)

    report.append(f"**Pages Crawled:** {pages_prev} → {pages_curr} {format_change(pages_change, pages_pct)}")
    report.append("")

    # Overall assessment
    if issues_change < 0:
        report.append("### 🎉 Overall Progress: Improving")
        report.append(f"Issue count reduced by {abs(issues_change)} ({abs(issues_pct):.1f}%). Good progress!")
    elif issues_change == 0:
        report.append("### ➡️ Overall Progress: Stable")
        report.append("Issue count unchanged. Consider implementing new optimizations.")
    else:
        report.append("### ⚠️ Overall Progress: Issues Increased")
        report.append(f"Issue count increased by {issues_change} ({issues_pct:.1f}%). Review recent changes.")

    report.append("")
    report.append("---")
    report.append("")

    # Detailed Metrics Comparison
    report.append("## Detailed Metrics")
    report.append("")
    report.append("| Metric | Previous | Current | Change |")
    report.append("|--------|----------|---------|--------|")

    metrics = [
        ('Pages Discovered', 'discovered'),
        ('Pages Crawled', 'crawled'),
        ('Max Depth', 'depth'),
        ('Avg Speed (URLs/sec)', 'speed'),
    ]

    for label, key in metrics:
        curr_val = current_stats.get(key, 0)
        prev_val = previous_stats.get(key, 0)
        change, pct = calculate_change(curr_val, prev_val)

        if isinstance(curr_val, float):
            report.append(f"| {label} | {prev_val:.2f} | {curr_val:.2f} | {change:+.2f} ({pct:+.1f}%) |")
        else:
            report.append(f"| {label} | {prev_val} | {curr_val} | {change:+d} ({pct:+.1f}%) |")

    report.append("")
    report.append("---")
    report.append("")

    # Issue Breakdown by Category
    report.append("## Issues by Category")
    report.append("")

    curr_categories = Counter(i.get('category', 'Unknown') for i in current_issues)
    prev_categories = Counter(i.get('category', 'Unknown') for i in previous_issues)

    all_categories = set(curr_categories.keys()) | set(prev_categories.keys())

    report.append("| Category | Previous | Current | Change |")
    report.append("|----------|----------|---------|--------|")

    for category in sorted(all_categories):
        prev_count = prev_categories.get(category, 0)
        curr_count = curr_categories.get(category, 0)
        change, pct = calculate_change(curr_count, prev_count)
        change_str = format_change(change, pct, inverse=True) if change != 0 else "→ 0"
        report.append(f"| {category} | {prev_count} | {curr_count} | {change_str} |")

    report.append("")
    report.append("---")
    report.append("")

    # Top Issue Types
    report.append("## Top Issue Types")
    report.append("")

    curr_issue_types = Counter(i.get('issue', 'Unknown') for i in current_issues)
    prev_issue_types = Counter(i.get('issue', 'Unknown') for i in previous_issues)

    report.append("### Current Top 10")
    report.append("")
    for issue_type, count in curr_issue_types.most_common(10):
        prev_count = prev_issue_types.get(issue_type, 0)
        change = count - prev_count
        if change != 0:
            report.append(f"- **{issue_type}**: {count} occurrences ({change:+d} from previous)")
        else:
            report.append(f"- **{issue_type}**: {count} occurrences")

    report.append("")

    # Resolved Issues
    resolved_issue_types = set(prev_issue_types.keys()) - set(curr_issue_types.keys())
    if resolved_issue_types:
        report.append("### ✅ Resolved Issue Types")
        report.append("")
        for issue_type in sorted(resolved_issue_types):
            count = prev_issue_types[issue_type]
            report.append(f"- **{issue_type}**: {count} instances resolved!")
        report.append("")

    # New Issues
    new_issue_types = set(curr_issue_types.keys()) - set(prev_issue_types.keys())
    if new_issue_types:
        report.append("### 🆕 New Issue Types")
        report.append("")
        for issue_type in sorted(new_issue_types):
            count = curr_issue_types[issue_type]
            report.append(f"- **{issue_type}**: {count} new instances")
        report.append("")

    report.append("---")
    report.append("")

    # Page-Level Changes
    report.append("## Page-Level Analysis")
    report.append("")

    # Build URL sets
    prev_urls = {p['url'] for p in previous_results if 'url' in p}
    curr_urls = {p['url'] for p in current_results if 'url' in p}

    new_pages = curr_urls - prev_urls
    removed_pages = prev_urls - curr_urls

    if new_pages:
        report.append(f"### 🆕 New Pages Discovered ({len(new_pages)})")
        report.append("")
        for url in sorted(list(new_pages)[:10]):  # Show first 10
            report.append(f"- {url}")
        if len(new_pages) > 10:
            report.append(f"- ... and {len(new_pages) - 10} more")
        report.append("")

    if removed_pages:
        report.append(f"### 🗑️ Pages No Longer Found ({len(removed_pages)})")
        report.append("")
        for url in sorted(list(removed_pages)[:10]):  # Show first 10
            report.append(f"- {url}")
        if len(removed_pages) > 10:
            report.append(f"- ... and {len(removed_pages) - 10} more")
        report.append("")

    # Recommendations
    report.append("---")
    report.append("")
    report.append("## Recommendations")
    report.append("")

    if issues_change < 0:
        report.append("✅ **Good Progress!** Continue current optimization efforts.")
        report.append("")
        if curr_errors > 0:
            report.append(f"- Focus next: Resolve remaining {curr_errors} critical errors")
        if curr_warnings > 10:
            report.append(f"- Address high-priority warnings (currently {curr_warnings})")
    elif issues_change == 0:
        report.append("⚠️ **Plateau Detected** - Time for new optimizations:")
        report.append("")
        report.append("- Review and implement advanced SEO techniques")
        report.append("- Consider content expansion on thin pages")
        report.append("- Add structured data where missing")
    else:
        report.append("🔴 **Issues Increased** - Investigate recent changes:")
        report.append("")
        if new_issue_types:
            report.append(f"- {len(new_issue_types)} new issue types introduced")
        if new_pages:
            report.append(f"- {len(new_pages)} new pages may need optimization")
        report.append("- Review recent content or template changes")

    report.append("")
    report.append("---")
    report.append("")
    report.append(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    return "\n".join(report)

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    current_file = sys.argv[1]
    previous_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    # Load data
    current_data = load_crawl(current_file)
    previous_data = load_crawl(previous_file)

    # Generate report
    report = compare_crawls(current_data, previous_data)

    # Output
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)
        print(f"✓ Comparison report saved to: {output_file}")
    else:
        print(report)

if __name__ == '__main__':
    main()
