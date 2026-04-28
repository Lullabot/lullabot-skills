#!/bin/bash
#
# crawl_site.sh - Wrapper script for LibreCrawl integration with seo-expert skill
#
# Usage:
#   ./scripts/crawl_site.sh <url> [config] [output]
#
# Arguments:
#   url     - Website URL to crawl (required)
#   config  - Config name: tier1, tier2, tier3, or path to custom JSON (default: tier1)
#   output  - Output file path (default: crawl-results-TIMESTAMP.json)
#
# Examples:
#   ./scripts/crawl_site.sh https://example.com
#   ./scripts/crawl_site.sh https://example.com tier2
#   ./scripts/crawl_site.sh https://example.com tier3 monthly-audit.json
#   ./scripts/crawl_site.sh https://example.com /path/to/custom-config.json
#

set -e  # Exit on error

# Get script directory (works even when called from elsewhere)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CRAWLER_DIR="$SKILL_DIR/tools/LibreCrawl"
VENV_DIR="$CRAWLER_DIR/venv"

# Parse arguments
URL="$1"
CONFIG="${2:-tier1}"
OUTPUT="${3:-crawl-results-$(date +%Y%m%d-%H%M%S).json}"

# Validation
if [ -z "$URL" ]; then
    echo "Error: URL is required"
    echo ""
    echo "Usage: $0 <url> [config] [output]"
    echo ""
    echo "Arguments:"
    echo "  url     - Website URL to crawl (required)"
    echo "  config  - tier1, tier2, tier3, or path to custom JSON (default: tier1)"
    echo "  output  - Output file path (default: crawl-results-TIMESTAMP.json)"
    echo ""
    echo "Examples:"
    echo "  $0 https://example.com"
    echo "  $0 https://example.com tier2"
    echo "  $0 https://example.com tier3 monthly-audit.json"
    exit 1
fi

# Check if LibreCrawl submodule exists
if [ ! -d "$CRAWLER_DIR" ]; then
    echo "Error: LibreCrawl not found at $CRAWLER_DIR"
    echo ""
    echo "Please initialize the submodule:"
    echo "  cd $SKILL_DIR"
    echo "  git submodule update --init --recursive"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "$VENV_DIR" ]; then
    echo "Setting up LibreCrawl virtual environment..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -q -r "$CRAWLER_DIR/requirements.txt"
    echo "✓ Virtual environment created"
else
    source "$VENV_DIR/bin/activate"
fi

# Determine config file path
if [ -f "$CONFIG" ]; then
    # Custom config file path provided
    CONFIG_FILE="$CONFIG"
elif [ -f "$SKILL_DIR/templates/${CONFIG}-crawl-config.json" ]; then
    # Tier config (tier1, tier2, tier3)
    CONFIG_FILE="$SKILL_DIR/templates/${CONFIG}-crawl-config.json"
else
    echo "Error: Config not found: $CONFIG"
    echo ""
    echo "Available tier configs:"
    ls -1 "$SKILL_DIR/templates/"*-crawl-config.json 2>/dev/null || echo "  (none found - run setup first)"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 SEO Expert - Full Site Crawl"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "URL:       $URL"
echo "Config:    $(basename "$CONFIG_FILE")"
echo "Output:    $OUTPUT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create a temporary Python script that uses LibreCrawl's crawler directly
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << 'PYTHON_SCRIPT'
import sys
import json
import time
sys.path.insert(0, sys.argv[1])  # Add LibreCrawl to path

from src.crawler import WebCrawler

def crawl_site(url, config_file, output_file):
    """Run LibreCrawl with provided config"""

    # Load config
    with open(config_file, 'r') as f:
        config = json.load(f)

    print(f"Starting crawl of {url}")
    print(f"Max depth: {config.get('max_depth', 3)}, Max URLs: {config.get('max_urls', 100)}")
    print("-" * 60)

    # Create crawler
    crawler = WebCrawler()
    crawler.update_config(config)

    # Start crawl
    crawler.start_crawl(url)

    # Monitor progress
    last_status = None
    while crawler.is_running:
        status = crawler.get_status()
        stats = status.get('stats', {})

        if stats != last_status:
            crawled = stats.get('crawled', 0)
            discovered = stats.get('discovered', 0)
            depth = stats.get('depth', 0)
            speed = stats.get('speed', 0)
            print(f"Progress: {crawled}/{discovered} URLs crawled (depth: {depth}, speed: {speed:.2f} URLs/sec)")
            last_status = stats

        time.sleep(1)

    # Get final results
    final_status = crawler.get_status()
    results = final_status.get('urls', [])
    stats = final_status.get('stats', {})
    issues = final_status.get('issues', [])

    print("\n" + "=" * 60)
    print("CRAWL COMPLETE")
    print("=" * 60)
    print(f"URLs discovered: {stats.get('discovered', 0)}")
    print(f"URLs crawled: {stats.get('crawled', 0)}")
    print(f"Max depth: {stats.get('depth', 0)}")
    print(f"Avg speed: {stats.get('speed', 0):.2f} URLs/sec")
    print(f"SEO issues: {len(issues)}")

    # Save results
    output_data = {
        'crawl_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'url': url,
        'config': config,
        'stats': stats,
        'results': results,
        'issues': issues
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n✓ Results saved to: {output_file}")

    return len(issues)

if __name__ == '__main__':
    crawler_dir = sys.argv[1]
    url = sys.argv[2]
    config_file = sys.argv[3]
    output_file = sys.argv[4]

    issue_count = crawl_site(url, config_file, output_file)

    # Exit code = number of issues (capped at 125 for shell compatibility)
    sys.exit(min(issue_count, 125))
PYTHON_SCRIPT

# Run the crawl
python3 "$TEMP_SCRIPT" "$CRAWLER_DIR" "$URL" "$CONFIG_FILE" "$OUTPUT"
CRAWL_EXIT_CODE=$?

# Cleanup
rm "$TEMP_SCRIPT"
deactivate

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $CRAWL_EXIT_CODE -eq 0 ]; then
    echo "✓ Crawl completed successfully - No issues found!"
else
    echo "✓ Crawl completed - $CRAWL_EXIT_CODE issues detected"
fi

echo ""
echo "Next steps:"
echo "  1. Generate report:   ./scripts/generate_crawl_report.py $OUTPUT"
echo "  2. Compare to previous: ./scripts/compare_crawls.py $OUTPUT previous.json"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit 0
