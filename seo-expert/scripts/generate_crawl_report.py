#!/usr/bin/env python3
"""
generate_crawl_report.py - Generate SEO audit report from LibreCrawl results

Usage:
    ./scripts/generate_crawl_report.py <crawl-results.json> [output.md]

Arguments:
    crawl-results - LibreCrawl JSON output file
    output        - Optional output file for markdown report (default: stdout)

Example:
    ./scripts/generate_crawl_report.py crawl-results.json audit-report.md
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

def priority_emoji(issue_type):
    """Get priority emoji based on issue type"""
    if issue_type == 'error':
        return '🔴'
    elif issue_type == 'warning':
        return '🟡'
    else:
        return '🟢'

def estimate_effort(issue_count):
    """Estimate effort hours based on issue count and type"""
    if issue_count <= 5:
        return "1-2 hours"
    elif issue_count <= 15:
        return "2-4 hours"
    elif issue_count <= 30:
        return "4-8 hours"
    else:
        return "8-12 hours"

def calculate_roi(category):
    """Estimate ROI based on issue category"""
    high_roi = ['SEO', 'Technical', 'Mobile']
    medium_roi = ['Social', 'Structured Data', 'Performance']

    if category in high_roi:
        return '🔴 High'
    elif category in medium_roi:
        return '🟡 Medium'
    else:
        return '🟢 Low'

def generate_report(data):
    """Generate SEO audit report from crawl data"""

    stats = data.get('stats', {})
    issues = data.get('issues', [])
    results = data.get('results', [])
    url = data.get('url', 'Unknown')
    crawl_date = data.get('crawl_date', 'Unknown')

    report = []

    # Header
    report.append("# SEO Health Check Report")
    site_name = url.replace('https://', '').replace('http://', '').split('/')[0]
    report.append(f"## {site_name}")
    report.append("")
    report.append(f"**Report Date:** {datetime.now().strftime('%B %d, %Y')}")
    report.append(f"**Crawl Date:** {crawl_date}")
    report.append(f"**Pages Analyzed:** {stats.get('crawled', 0)}")
    report.append(f"**Service Tier:** Foundation (Example)")
    report.append("")
    report.append("---")
    report.append("")

    # Executive Summary
    report.append("## Executive Summary")
    report.append("")

    total_issues = len(issues)
    errors = len([i for i in issues if i.get('type') == 'error'])
    warnings = len([i for i in issues if i.get('type') == 'warning'])

    if total_issues == 0:
        report.append("### Overall Score: 🟢 Excellent")
        report.append("")
        report.append("Your site has no detected SEO issues. Great work!")
    elif errors == 0 and warnings < 20:
        report.append("### Overall Score: 🟡 Good")
        report.append("")
        report.append(f"Found {total_issues} minor optimization opportunities. Site is in good shape with room for improvement.")
    elif errors < 10:
        report.append("### Overall Score: 🟡 Fair (Needs Improvement)")
        report.append("")
        report.append(f"Identified {total_issues} optimization opportunities across {stats.get('crawled', 0)} pages. Priority issues should be addressed soon.")
    else:
        report.append("### Overall Score: 🔴 Needs Attention")
        report.append("")
        report.append(f"Found {total_issues} issues including {errors} critical errors. Immediate action recommended.")

    report.append("")

    # What's Working
    pages_with_meta = len([p for p in results if p.get('meta_description')])
    pages_with_title = len([p for p in results if p.get('title')])
    pages_with_h1 = len([p for p in results if p.get('h1')])
    pages_200 = len([p for p in results if p.get('status_code') == 200])

    report.append("**What's Working:**")
    if pages_200 == stats.get('crawled', 0):
        report.append("- ✅ All pages load successfully (200 status)")
    if pages_with_h1 > stats.get('crawled', 0) * 0.8:
        report.append(f"- ✅ Most pages have H1 tags ({pages_with_h1}/{stats.get('crawled', 0)})")
    if pages_with_title == stats.get('crawled', 0):
        report.append("- ✅ All pages have title tags")

    avg_internal_links = sum(p.get('internal_links', 0) for p in results) / max(len(results), 1)
    if avg_internal_links > 10:
        report.append(f"- ✅ Good internal linking (avg {avg_internal_links:.0f} links/page)")

    report.append("")

    # Priority Issues
    report.append("**Priority Issues:**")
    if errors > 0:
        report.append(f"- ❌ {errors} critical errors require immediate attention")
    if warnings > 0:
        report.append(f"- ⚠️ {warnings} warnings should be addressed")

    missing_meta = len([i for i in issues if 'Meta Description' in i.get('issue', '')])
    if missing_meta > 0:
        report.append(f"- ❌ {missing_meta} pages missing meta descriptions")

    missing_social = len([i for i in issues if 'OpenGraph' in i.get('issue', '') or 'Twitter' in i.get('issue', '')])
    if missing_social > 0:
        report.append(f"- ❌ Social media tags missing site-wide")

    missing_schema = len([i for i in issues if 'Structured Data' in i.get('issue', '')])
    if missing_schema > 0:
        report.append(f"- ❌ {missing_schema} pages missing structured data")

    report.append("")
    report.append("---")
    report.append("")

    # Issue Breakdown
    report.append("## Issue Breakdown")
    report.append("")

    categories = Counter(i.get('category', 'Unknown') for i in issues)

    report.append("### By Category")
    report.append("")
    report.append("| Category | Count | Priority | Est. Effort | ROI |")
    report.append("|----------|-------|----------|-------------|-----|")

    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        priority = priority_emoji('error' if count > 10 else 'warning')
        effort = estimate_effort(count)
        roi = calculate_roi(category)
        report.append(f"| {category} | {count} | {priority} | {effort} | {roi} |")

    report.append("")

    # Top Issues
    report.append("### Top 5 Most Impactful Issues")
    report.append("")

    issue_types = Counter(i.get('issue', 'Unknown') for i in issues)

    for rank, (issue_type, count) in enumerate(issue_types.most_common(5), 1):
        # Get category for this issue type
        category = next((i.get('category', 'Unknown') for i in issues if i.get('issue') == issue_type), 'Unknown')
        sample_issue = next(i for i in issues if i.get('issue') == issue_type)
        severity = sample_issue.get('type', 'warning')

        report.append(f"**{rank}. {issue_type}** ({count} pages)")
        report.append(f"   - **Impact:** {calculate_roi(category)}")
        report.append(f"   - **Effort:** {estimate_effort(count)}")
        report.append(f"   - **Category:** {category}")

        # Add specific recommendation
        if 'Meta Description' in issue_type:
            report.append(f"   - **Fix:** Write compelling 150-160 character meta descriptions")
        elif 'OpenGraph' in issue_type or 'Twitter' in issue_type:
            report.append(f"   - **Fix:** Add social media tags to site template")
        elif 'Structured Data' in issue_type:
            report.append(f"   - **Fix:** Implement JSON-LD schema markup")
        elif 'Title' in issue_type and 'Short' in issue_type:
            report.append(f"   - **Fix:** Lengthen titles to 30-60 characters")
        elif 'Thin Content' in issue_type:
            report.append(f"   - **Fix:** Expand content to 400+ words")

        report.append("")

    report.append("---")
    report.append("")

    # Detailed Findings
    report.append("## Detailed Findings")
    report.append("")

    # Group issues by category
    for category in sorted(set(i.get('category') for i in issues)):
        category_issues = [i for i in issues if i.get('category') == category]
        if not category_issues:
            continue

        report.append(f"### {category} ({len(category_issues)} issues)")
        report.append("")

        # Group by issue type within category
        issue_groups = {}
        for issue in category_issues:
            issue_type = issue.get('issue', 'Unknown')
            if issue_type not in issue_groups:
                issue_groups[issue_type] = []
            issue_groups[issue_type].append(issue)

        for issue_type, group in sorted(issue_groups.items(), key=lambda x: len(x[1]), reverse=True):
            severity = group[0].get('type', 'warning')
            emoji = priority_emoji(severity)

            report.append(f"**{emoji} {issue_type}** ({len(group)} pages)")
            report.append("")
            report.append(f"*{group[0].get('details', 'No details available')}*")
            report.append("")

            # Show up to 5 affected URLs
            report.append("**Affected pages:**")
            for issue in group[:5]:
                url_path = issue.get('url', 'Unknown').replace(url, '')
                if not url_path:
                    url_path = '/'
                report.append(f"- {url_path}")

            if len(group) > 5:
                report.append(f"- ... and {len(group) - 5} more pages")

            report.append("")

    report.append("---")
    report.append("")

    # Page-by-Page Summary
    report.append("## Page-by-Page Summary")
    report.append("")
    report.append("| Page | Status | Word Count | Has Meta? | Issues |")
    report.append("|------|--------|------------|-----------|--------|")

    for page in results[:20]:  # Show first 20 pages
        url_path = page.get('url', '').replace(url, '')
        if not url_path:
            url_path = '/'
        status = page.get('status_code', 'N/A')
        word_count = page.get('word_count', 0)
        has_meta = '✓' if page.get('meta_description') else '✗'

        # Count issues for this page
        page_issues = [i for i in issues if i.get('url') == page.get('url')]
        issue_count = len(page_issues)

        status_emoji = '✅' if status == 200 else '❌'
        report.append(f"| {url_path[:50]} | {status_emoji} {status} | {word_count} | {has_meta} | {issue_count} |")

    if len(results) > 20:
        report.append(f"| *... and {len(results) - 20} more pages* | | | | |")

    report.append("")
    report.append("---")
    report.append("")

    # Recommended Action Plan
    report.append("## Recommended Action Plan")
    report.append("")

    # Calculate quick wins
    quick_win_issues = []
    if missing_meta > 0:
        quick_win_issues.append(f"Add meta descriptions to {missing_meta} pages")
    if missing_social > 0:
        quick_win_issues.append("Add social media tags site-wide")

    short_titles = len([i for i in issues if 'Title Too Short' in i.get('issue', '')])
    if short_titles > 0:
        quick_win_issues.append(f"Optimize {short_titles} short title tags")

    report.append("### 🚀 Quick Wins (Week 1-2) - 8-10 hours")
    report.append("")
    for idx, task in enumerate(quick_win_issues, 1):
        report.append(f"{idx}. {task}")

    report.append("")
    report.append("**Expected Impact:**")
    report.append("- 📈 15-25% improvement in search click-through rate")
    report.append("- 📈 Professional social media sharing")
    report.append("- 📈 Better search result presentation")
    report.append("")

    # Month 2 recommendations
    report.append("### 📊 Month 2: Technical SEO (6-8 hours)")
    report.append("")

    if missing_schema > 0:
        report.append("- Add structured data (Organization, Service, BreadcrumbList schemas)")

    canonical_issues = len([i for i in issues if 'Canonical' in i.get('issue', '')])
    if canonical_issues > 0:
        report.append("- Fix canonical URL issues")

    if len([i for i in issues if i.get('category') == 'Performance']) > 0:
        report.append("- Address performance optimizations")

    report.append("")
    report.append("**Expected Impact:**")
    report.append("- 📈 Eligibility for rich search results")
    report.append("- 📈 Improved crawl efficiency")
    report.append("- 📈 Better mobile experience")
    report.append("")

    # Month 3 recommendations
    thin_content = len([i for i in issues if 'Thin Content' in i.get('issue', '')])
    if thin_content > 0:
        report.append("### 🎯 Month 3: Content Enhancement (8-10 hours)")
        report.append("")
        report.append(f"- Expand {thin_content} pages with thin content (250 → 400+ words)")
        report.append("- Add FAQ sections where appropriate")
        report.append("- Optimize content structure for readability")
        report.append("")
        report.append("**Expected Impact:**")
        report.append("- 📈 Improved page quality scores")
        report.append("- 📈 Better user engagement")
        report.append("- 📈 Higher search rankings")
        report.append("")

    report.append("---")
    report.append("")

    # Next Steps
    report.append("## Next Steps")
    report.append("")
    report.append("1. **Review this report** and prioritize which issues to address first")
    report.append("2. **Schedule a strategy call** to discuss implementation timeline")
    report.append("3. **Approve Quick Wins action plan** for immediate improvements")
    report.append("4. **Schedule monthly re-crawl** to track progress")
    report.append("")
    report.append("---")
    report.append("")

    # Footer
    report.append("## Questions?")
    report.append("")
    report.append("Contact your SEO specialist to discuss any findings or prioritization questions.")
    report.append("")
    report.append(f"**This report generated by:** LibreCrawl + SEO Expert Skill")
    report.append(f"**Analysis depth:** {stats.get('depth', 0)} levels, {stats.get('crawled', 0)} pages")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(report)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    crawl_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Load data
    data = load_crawl(crawl_file)

    # Generate report
    report = generate_report(data)

    # Output
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)
        print(f"✓ SEO audit report saved to: {output_file}")
    else:
        print(report)

if __name__ == '__main__':
    main()
