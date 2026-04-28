#!/usr/bin/env python3

"""
Meta Tag Extraction and Schema Validation Script (GEO Enhanced)

Analyzes meta tags and validates GEO-critical structured data (FAQ, HowTo, Article schemas).
Google Gemini leverages structured data for AI citations.

Usage: ./extract_meta.py <html_file_or_url>
"""

import sys
import re
import json
from html.parser import HTMLParser

class MetaTagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.meta_tags = []
        self.in_title = False
        self.in_script = False
        self.script_content = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            self.meta_tags.append(dict(attrs))
        elif tag == 'script':
            attrs_dict = dict(attrs)
            # Capture JSON-LD scripts for schema analysis
            if attrs_dict.get('type') == 'application/ld+json':
                self.in_script = True
                self.script_content = []

    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
        elif self.in_script:
            self.script_content.append(data)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'script' and self.in_script:
            self.scripts.append(''.join(self.script_content))
            self.in_script = False
            self.script_content = []

def analyze_schema_markup(scripts):
    """Analyze Schema.org structured data for GEO optimization."""
    print("GEO: SCHEMA.ORG STRUCTURED DATA (CRITICAL)")
    print("=" * 80)

    if not scripts:
        print("❌ CRITICAL: No JSON-LD structured data found!")
        print()
        print("Recommendations:")
        print("  • Add FAQ Schema for Q&A content (CRITICAL for GEO)")
        print("  • Add HowTo Schema for process/tutorial content")
        print("  • Add Article Schema with author information")
        print()
        print("Why this matters:")
        print("  • 92.36% of AI citations have proper schema markup")
        print("  • Google Gemini confirms it leverages structured data")
        print("  • Schema dramatically improves AI citation rates")
        print()
        return

    schemas_found = []
    faq_schema = None
    howto_schema = None
    article_schema = None

    # Parse each JSON-LD script
    for i, script in enumerate(scripts):
        try:
            data = json.loads(script)

            # Handle single schema or array of schemas
            schemas = data if isinstance(data, list) else [data]

            for schema in schemas:
                schema_type = schema.get('@type', '')

                if schema_type == 'FAQPage':
                    faq_schema = schema
                    schemas_found.append('FAQPage')
                elif schema_type == 'HowTo':
                    howto_schema = schema
                    schemas_found.append('HowTo')
                elif schema_type in ['Article', 'NewsArticle', 'BlogPosting']:
                    article_schema = schema
                    schemas_found.append(schema_type)
                elif schema_type:
                    schemas_found.append(schema_type)

        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Invalid JSON-LD in script {i+1}: {e}")
            continue

    # Summary
    print(f"Schemas found: {len(schemas_found)}")
    if schemas_found:
        for schema_type in set(schemas_found):
            count = schemas_found.count(schema_type)
            print(f"  • {schema_type}" + (f" ({count})" if count > 1 else ""))
    print()

    # Analyze FAQ Schema (CRITICAL for GEO)
    print("FAQ SCHEMA (CRITICAL for GEO)")
    print("-" * 80)
    if faq_schema:
        print("✅ FAQ Schema found!")
        questions = faq_schema.get('mainEntity', [])
        if questions:
            print(f"   Number of Q&A pairs: {len(questions)}")
            print()
            print("   Sample questions:")
            for i, q in enumerate(questions[:3], 1):
                question_text = q.get('name', 'N/A')
                print(f"   {i}. {question_text}")
            if len(questions) > 3:
                print(f"   ... and {len(questions) - 3} more")
        else:
            print("   ⚠️  Warning: FAQ Schema present but no questions found")
    else:
        print("❌ MISSING: No FAQ Schema detected")
        print("   CRITICAL RECOMMENDATION: Add FAQ Schema for Q&A content")
        print("   FAQ Schema drives 3.2x higher AI citation rates (note: Google removed FAQ rich results for most sites in Aug 2023)")
    print()

    # Analyze HowTo Schema
    print("HOWTO SCHEMA")
    print("-" * 80)
    if howto_schema:
        print("✅ HowTo Schema found!")
        steps = howto_schema.get('step', [])
        if steps:
            print(f"   Number of steps: {len(steps)}")
        print("   Perfect for: Process guides, tutorials, instructions")
    else:
        print("⚠️  No HowTo Schema detected")
        print("   Recommendation: Add HowTo Schema for process/tutorial content")
    print()

    # Analyze Article Schema
    print("ARTICLE SCHEMA")
    print("-" * 80)
    if article_schema:
        print("✅ Article Schema found!")
        author = article_schema.get('author', {})
        publisher = article_schema.get('publisher', {})
        date_published = article_schema.get('datePublished', None)
        date_modified = article_schema.get('dateModified', None)

        # Check for author (E-E-A-T signal)
        if author:
            if isinstance(author, dict):
                author_name = author.get('name', 'N/A')
                print(f"   Author: {author_name}")
            else:
                print(f"   Author: {author}")
        else:
            print("   ⚠️  Warning: No author specified (important for E-E-A-T)")

        # Check for dates (freshness signal)
        if date_published:
            print(f"   Published: {date_published}")
        if date_modified:
            print(f"   Modified: {date_modified}")
        elif date_published:
            print("   ⚠️  Recommendation: Add dateModified to show content freshness")

        # Check for publisher
        if not publisher:
            print("   ⚠️  Warning: No publisher specified")
    else:
        print("⚠️  No Article Schema detected")
        print("   Recommendation: Add Article Schema for blog posts/articles")
    print()

    # Overall GEO Schema Score
    print("GEO SCHEMA OPTIMIZATION SCORE")
    print("-" * 80)
    score = 0
    max_score = 3

    if faq_schema:
        score += 1
        print("✅ FAQ Schema: PRESENT (CRITICAL)")
    else:
        print("❌ FAQ Schema: MISSING (CRITICAL)")

    if article_schema and article_schema.get('author'):
        score += 1
        print("✅ Article Schema with Author: PRESENT")
    else:
        print("⚠️  Article Schema with Author: MISSING")

    if howto_schema or len(schemas_found) > 0:
        score += 1
        print("✅ Additional Structured Data: PRESENT")
    else:
        print("⚠️  Additional Structured Data: MISSING")

    print()
    print(f"Overall Score: {score}/{max_score}")

    if score == max_score:
        print("STATUS: ✅ EXCELLENT - Schema optimized for GEO")
    elif score >= 2:
        print("STATUS: ⚠️  GOOD - Add FAQ Schema for optimal GEO")
    else:
        print("STATUS: ❌ NEEDS IMPROVEMENT - Add GEO-critical schemas")

    print()
    print("Schema Implementation Resources:")
    print("  • See references/schema_markup_guide.md for examples")
    print("  • Test with Google's Rich Results Test")
    print("  • FAQ Schema is the highest priority for AI citations")
    print()


def analyze_meta_tags(html_content):
    """Parse and analyze meta tags from HTML content"""
    parser = MetaTagParser()
    parser.feed(html_content)

    print("SEO Meta Tag Analysis")
    print("=" * 80)
    print()

    # Title Tag
    print("TITLE TAG")
    print("-" * 80)
    if parser.title:
        title_length = len(parser.title)
        status = "✓" if 50 <= title_length <= 60 else "⚠"
        print(f"{status} Title: {parser.title}")
        print(f"  Length: {title_length} characters")
        if title_length < 50:
            print(f"  Warning: Title is too short (recommended: 50-60 characters)")
        elif title_length > 60:
            print(f"  Warning: Title may be truncated in search results (recommended: 50-60 characters)")
    else:
        print("✗ No title tag found!")
    print()

    # Meta Description
    print("META DESCRIPTION")
    print("-" * 80)
    description = None
    for meta in parser.meta_tags:
        if meta.get('name', '').lower() == 'description':
            description = meta.get('content', '')
            break

    if description:
        desc_length = len(description)
        status = "✓" if 150 <= desc_length <= 160 else "⚠"
        print(f"{status} Description: {description}")
        print(f"  Length: {desc_length} characters")
        if desc_length < 150:
            print(f"  Warning: Description is too short (recommended: 150-160 characters)")
        elif desc_length > 160:
            print(f"  Warning: Description may be truncated in search results (recommended: 150-160 characters)")
    else:
        print("✗ No meta description found!")
    print()

    # Robots Tag
    print("META ROBOTS")
    print("-" * 80)
    robots = None
    for meta in parser.meta_tags:
        if meta.get('name', '').lower() == 'robots':
            robots = meta.get('content', '')
            break

    if robots:
        print(f"✓ Robots: {robots}")
        if 'noindex' in robots.lower():
            print(f"  ⚠ WARNING: Page is set to noindex!")
        if 'nofollow' in robots.lower():
            print(f"  ⚠ WARNING: Links are set to nofollow!")
    else:
        print("  No robots meta tag (default: index, follow)")
    print()

    # Canonical URL
    print("CANONICAL URL")
    print("-" * 80)
    canonical = None
    for meta in parser.meta_tags:
        if meta.get('rel', '') == 'canonical':
            canonical = meta.get('href', '')
            break

    if canonical:
        print(f"✓ Canonical: {canonical}")
    else:
        print("⚠ No canonical URL specified")
        print("  Recommendation: Add <link rel='canonical' href='...'> to prevent duplicate content issues")
    print()

    # Open Graph Tags
    print("OPEN GRAPH (Social Media)")
    print("-" * 80)
    og_tags = {meta.get('property', ''): meta.get('content', '')
               for meta in parser.meta_tags
               if meta.get('property', '').startswith('og:')}

    if og_tags:
        for prop, content in og_tags.items():
            print(f"✓ {prop}: {content}")
    else:
        print("⚠ No Open Graph tags found")
        print("  Recommendation: Add OG tags for better social media sharing")
    print()

    # Twitter Card Tags
    print("TWITTER CARD")
    print("-" * 80)
    twitter_tags = {meta.get('name', ''): meta.get('content', '')
                    for meta in parser.meta_tags
                    if meta.get('name', '').startswith('twitter:')}

    if twitter_tags:
        for name, content in twitter_tags.items():
            print(f"✓ {name}: {content}")
    else:
        print("⚠ No Twitter Card tags found")
        print("  Recommendation: Add Twitter Card tags for better Twitter sharing")
    print()

    # Viewport (Mobile)
    print("VIEWPORT (Mobile)")
    print("-" * 80)
    viewport = None
    for meta in parser.meta_tags:
        if meta.get('name', '').lower() == 'viewport':
            viewport = meta.get('content', '')
            break

    if viewport:
        print(f"✓ Viewport: {viewport}")
        if 'width=device-width' not in viewport.lower():
            print(f"  ⚠ Warning: Viewport should include 'width=device-width' for mobile optimization")
    else:
        print("✗ No viewport meta tag found!")
        print("  Recommendation: Add <meta name='viewport' content='width=device-width, initial-scale=1'>")
    print()

    # GEO: Schema.org Structured Data Analysis
    analyze_schema_markup(parser.scripts)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./extract_meta.py <html_file_or_url>")
        print("Example: ./extract_meta.py page.html")
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        if input_path.startswith('http://') or input_path.startswith('https://'):
            import urllib.request
            with urllib.request.urlopen(input_path) as response:
                html_content = response.read().decode('utf-8')
        else:
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

        analyze_meta_tags(html_content)

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
