#!/bin/bash

# Sitemap Checker Script
# Usage: ./check_sitemap.sh <url>

if [ -z "$1" ]; then
    echo "Usage: $0 <url>"
    echo "Example: $0 https://example.com"
    exit 1
fi

URL="$1"

# Remove trailing slash if present
URL="${URL%/}"

# Construct sitemap URL
SITEMAP_URL="${URL}/sitemap.xml"

echo "Checking sitemap at: $SITEMAP_URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Fetch sitemap with HTTP status
HTTP_STATUS=$(curl -s -o /tmp/sitemap.xml -w "%{http_code}" "$SITEMAP_URL")

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "✓ sitemap.xml found (HTTP $HTTP_STATUS)"
    echo ""

    # Check if it's a valid XML file
    if ! command -v xmllint &> /dev/null; then
        echo "⚠ xmllint not available for validation (install libxml2)"
        echo ""
    else
        if xmllint --noout /tmp/sitemap.xml 2>/dev/null; then
            echo "✓ Valid XML structure"
        else
            echo "✗ Invalid XML structure detected"
        fi
        echo ""
    fi

    # Count URLs
    URL_COUNT=$(grep -c "<loc>" /tmp/sitemap.xml)
    echo "📋 Contains $URL_COUNT URLs"

    # Check for sitemap index (nested sitemaps)
    if grep -q "<sitemapindex" /tmp/sitemap.xml; then
        echo "📂 This is a sitemap index (contains nested sitemaps)"
        SITEMAP_COUNT=$(grep -c "<sitemap>" /tmp/sitemap.xml)
        echo "   Contains $SITEMAP_COUNT child sitemaps"
    fi

    # Check for lastmod dates
    LASTMOD_COUNT=$(grep -c "<lastmod>" /tmp/sitemap.xml)
    if [ "$LASTMOD_COUNT" -gt 0 ]; then
        echo "✓ Includes lastmod dates ($LASTMOD_COUNT entries)"
    else
        echo "⚠ No lastmod dates found (recommended for better crawl efficiency)"
    fi

    # Check for priority and changefreq
    PRIORITY_COUNT=$(grep -c "<priority>" /tmp/sitemap.xml)
    CHANGEFREQ_COUNT=$(grep -c "<changefreq>" /tmp/sitemap.xml)

    if [ "$PRIORITY_COUNT" -gt 0 ]; then
        echo "📊 Includes priority hints ($PRIORITY_COUNT entries)"
    fi

    if [ "$CHANGEFREQ_COUNT" -gt 0 ]; then
        echo "📊 Includes changefreq hints ($CHANGEFREQ_COUNT entries)"
    fi

    # File size check
    FILE_SIZE=$(wc -c < /tmp/sitemap.xml | tr -d ' ')
    FILE_SIZE_MB=$(echo "scale=2; $FILE_SIZE / 1048576" | bc)
    echo ""
    echo "📦 Sitemap size: $FILE_SIZE_MB MB"

    if [ "$FILE_SIZE" -gt 52428800 ]; then
        echo "⚠ WARNING: Sitemap exceeds 50MB limit!"
    fi

    if [ "$URL_COUNT" -gt 50000 ]; then
        echo "⚠ WARNING: Sitemap exceeds 50,000 URL limit!"
        echo "   Consider splitting into multiple sitemaps with a sitemap index"
    fi

elif [ "$HTTP_STATUS" -eq 404 ]; then
    echo "✗ sitemap.xml not found (HTTP $HTTP_STATUS)"
    echo ""
    echo "Recommendation: Create an XML sitemap to help search engines discover content."
    echo ""
    echo "Also check for sitemap_index.xml or alternative locations:"
    echo "- ${URL}/sitemap_index.xml"
    echo "- ${URL}/sitemap-index.xml"
    echo "- Check robots.txt for sitemap location"
else
    echo "⚠ Unexpected HTTP status: $HTTP_STATUS"
fi

# Cleanup
rm -f /tmp/sitemap.xml
