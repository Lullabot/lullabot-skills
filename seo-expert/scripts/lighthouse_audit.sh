#!/bin/bash

# Lighthouse SEO Audit Script
# Usage: ./lighthouse_audit.sh <url>

if [ -z "$1" ]; then
    echo "Usage: $0 <url>"
    echo "Example: $0 https://example.com"
    exit 1
fi

URL="$1"

# Check if Lighthouse CLI is installed
if ! command -v lighthouse &> /dev/null; then
    echo "Error: Lighthouse CLI is not installed."
    echo "Install with: npm install -g lighthouse"
    exit 1
fi

echo "Running Lighthouse audit on: $URL"
echo "This may take 30-60 seconds..."
echo ""

# Run Lighthouse with SEO, performance, and accessibility categories
lighthouse "$URL" \
    --only-categories=performance,seo,accessibility,best-practices \
    --output=json \
    --output-path=stdout \
    --chrome-flags="--headless" \
    --quiet

echo ""
echo "Audit complete!"
