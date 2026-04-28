#!/bin/bash

# Robots.txt Checker Script
# Usage: ./check_robots.sh <url>

if [ -z "$1" ]; then
    echo "Usage: $0 <url>"
    echo "Example: $0 https://example.com"
    exit 1
fi

URL="$1"

# Remove trailing slash if present
URL="${URL%/}"

# Construct robots.txt URL
ROBOTS_URL="${URL}/robots.txt"

echo "Checking robots.txt at: $ROBOTS_URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Fetch robots.txt with HTTP status
HTTP_STATUS=$(curl -s -o /tmp/robots.txt -w "%{http_code}" "$ROBOTS_URL")

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "✓ robots.txt found (HTTP $HTTP_STATUS)"
    echo ""
    echo "Content:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cat /tmp/robots.txt
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Check for sitemap references
    echo ""
    SITEMAPS=$(grep -i "^Sitemap:" /tmp/robots.txt)
    if [ -n "$SITEMAPS" ]; then
        echo "✓ Sitemap references found:"
        echo "$SITEMAPS"
    else
        echo "⚠ No sitemap references found in robots.txt"
    fi

    # Check for disallow rules
    echo ""
    DISALLOWS=$(grep -i "^Disallow:" /tmp/robots.txt | wc -l | tr -d ' ')
    echo "📋 Found $DISALLOWS Disallow directives"

elif [ "$HTTP_STATUS" -eq 404 ]; then
    echo "✗ robots.txt not found (HTTP $HTTP_STATUS)"
    echo ""
    echo "Recommendation: Create a robots.txt file to guide search engine crawlers."
    echo "Minimum recommended content:"
    echo ""
    echo "User-agent: *"
    echo "Allow: /"
    echo "Sitemap: ${URL}/sitemap.xml"
else
    echo "⚠ Unexpected HTTP status: $HTTP_STATUS"
fi

# Cleanup
rm -f /tmp/robots.txt
