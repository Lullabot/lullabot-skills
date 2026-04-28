#!/usr/bin/env python3
"""
BLUF (Bottom Line Up Front) Detection for GEO Optimization

Checks if content has a 50-70 word direct answer at the top of the page.
BLUF format is CRITICAL for AI Overview citations.

Usage:
    python3 check_bluf.py <html_file>
    python3 check_bluf.py <html_file> --min-words 50 --max-words 70

References:
    - BLUF format places key information in first 2-3 paragraphs
    - AI prefers content with immediate, direct answers
    - 50-70 words is optimal length for citations
"""

import sys
import re
from html.parser import HTMLParser


class ContentExtractor(HTMLParser):
    """Extract main content paragraphs from HTML."""

    def __init__(self):
        super().__init__()
        self.paragraphs = []
        self.current_paragraph = []
        self.in_content = True
        self.in_skip_tag = False
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'form'}

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.in_skip_tag = True
        elif tag == 'p':
            self.current_paragraph = []

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.in_skip_tag = False
        elif tag == 'p' and self.current_paragraph:
            text = ' '.join(self.current_paragraph).strip()
            if text and len(text.split()) > 5:  # Only keep paragraphs with 5+ words
                self.paragraphs.append(text)
            self.current_paragraph = []

    def handle_data(self, data):
        if not self.in_skip_tag and self.in_content:
            text = data.strip()
            if text:
                self.current_paragraph.append(text)


def extract_paragraphs(html_content):
    """Extract paragraphs from HTML content."""
    parser = ContentExtractor()
    parser.feed(html_content)
    return parser.paragraphs


def count_words(text):
    """Count words in text."""
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text)
    return len(words)


def is_direct_answer(paragraph):
    """
    Check if paragraph appears to be a direct answer.

    Heuristics:
    - Not too short (>20 words) or too long (<150 words)
    - Contains complete sentences
    - Not just a list of links
    """
    word_count = count_words(paragraph)

    if word_count < 20 or word_count > 150:
        return False

    # Check for sentence structure (ends with period, question mark, or exclamation)
    if not re.search(r'[.!?]$', paragraph.strip()):
        return False

    # Reject if mostly links (heuristic: less than 50% actual content)
    text_without_tags = re.sub(r'<[^>]+>', '', paragraph)
    if len(text_without_tags) < len(paragraph) * 0.5:
        return False

    return True


def analyze_bluf(paragraphs, min_words=50, max_words=70):
    """
    Analyze content for BLUF format.

    Returns:
        dict with analysis results
    """
    if not paragraphs:
        return {
            'has_bluf': False,
            'first_para_words': 0,
            'issue': 'No paragraphs found',
            'recommendation': 'Add content paragraphs to the page'
        }

    # Analyze first 3 paragraphs
    first_para = paragraphs[0] if len(paragraphs) > 0 else ''
    second_para = paragraphs[1] if len(paragraphs) > 1 else ''
    third_para = paragraphs[2] if len(paragraphs) > 2 else ''

    first_para_words = count_words(first_para)
    second_para_words = count_words(second_para)
    third_para_words = count_words(third_para)

    result = {
        'total_paragraphs': len(paragraphs),
        'first_para': first_para,
        'first_para_words': first_para_words,
        'second_para_words': second_para_words,
        'third_para_words': third_para_words,
        'has_bluf': False,
        'bluf_quality': 'none',
        'recommendation': []
    }

    # Check first paragraph for BLUF
    if first_para_words >= min_words and first_para_words <= max_words:
        if is_direct_answer(first_para):
            result['has_bluf'] = True
            result['bluf_quality'] = 'excellent'
            result['bluf_location'] = 'first_paragraph'
            return result

    # Check if BLUF is in first 2 paragraphs combined
    combined_first_two = first_para_words + second_para_words
    if combined_first_two >= min_words and combined_first_two <= 100:
        result['bluf_quality'] = 'acceptable'
        result['bluf_location'] = 'first_two_paragraphs'
        result['recommendation'].append(
            "Consider consolidating first two paragraphs into a single 50-70 word BLUF"
        )
        return result

    # Analyze issues
    if first_para_words == 0:
        result['issue'] = 'No first paragraph found'
        result['recommendation'].append('Add an opening paragraph with a direct answer')
    elif first_para_words < min_words:
        result['issue'] = f'First paragraph too short ({first_para_words} words, target: {min_words}-{max_words})'
        result['recommendation'].append(
            f'Expand first paragraph to {min_words}-{max_words} words with a direct, complete answer'
        )
    elif first_para_words > max_words:
        result['issue'] = f'First paragraph too long ({first_para_words} words, target: {min_words}-{max_words})'
        result['recommendation'].append(
            f'Shorten first paragraph to {min_words}-{max_words} words, focusing on the key answer'
        )
    else:
        result['issue'] = 'First paragraph does not appear to be a direct answer'
        result['recommendation'].append(
            'Rewrite first paragraph as a direct, concise answer to the main question'
        )

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_bluf.py <html_file> [--min-words N] [--max-words N]")
        sys.exit(1)

    html_file = sys.argv[1]
    min_words = 50
    max_words = 70

    # Parse optional parameters
    if '--min-words' in sys.argv:
        idx = sys.argv.index('--min-words')
        if idx + 1 < len(sys.argv):
            min_words = int(sys.argv[idx + 1])

    if '--max-words' in sys.argv:
        idx = sys.argv.index('--max-words')
        if idx + 1 < len(sys.argv):
            max_words = int(sys.argv[idx + 1])

    # Read HTML file
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{html_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Extract paragraphs
    paragraphs = extract_paragraphs(html_content)

    # Analyze BLUF
    analysis = analyze_bluf(paragraphs, min_words, max_words)

    # Display results
    print("=" * 70)
    print("BLUF (Bottom Line Up Front) Analysis")
    print("=" * 70)
    print()
    print(f"Total paragraphs found: {analysis['total_paragraphs']}")
    print(f"Target BLUF length:     {min_words}-{max_words} words")
    print()

    if analysis['total_paragraphs'] == 0:
        print("❌ CRITICAL: No content paragraphs found")
        print()
        print("Recommendation:")
        print("  • Add main content with clear paragraphs")
        print("  • Start with a 50-70 word direct answer")
        sys.exit(1)

    print("First Paragraph Analysis:")
    print("-" * 70)
    print(f"Word count: {analysis['first_para_words']}")
    print()

    if analysis['first_para_words'] > 0:
        # Show first paragraph (truncated if too long)
        first_para_display = analysis['first_para']
        if len(first_para_display) > 300:
            first_para_display = first_para_display[:300] + "..."

        print(f"Content preview:")
        print(f'  "{first_para_display}"')
        print()

    # BLUF status
    print("BLUF Status:")
    print("-" * 70)

    if analysis['has_bluf']:
        print("✅ EXCELLENT: First paragraph follows BLUF format")
        print(f"   {analysis['first_para_words']} words - optimal for AI citations")
        print()
        print("Why this matters:")
        print("  • AI extracts and cites direct, concise answers")
        print("  • 50-70 word answers are optimal for AI Overviews")
        print("  • BLUF format improves user experience and engagement")
        print()
        sys.exit(0)

    elif analysis.get('bluf_quality') == 'acceptable':
        print("⚠️  ACCEPTABLE: BLUF present but split across paragraphs")
        print(f"   First paragraph: {analysis['first_para_words']} words")
        print(f"   Second paragraph: {analysis['second_para_words']} words")
        print()
    else:
        print("❌ MISSING: No BLUF format detected")
        print()
        if 'issue' in analysis:
            print(f"Issue: {analysis['issue']}")
            print()

    # Recommendations
    if analysis['recommendation']:
        print("Recommendations:")
        for i, rec in enumerate(analysis['recommendation'], 1):
            print(f"  {i}. {rec}")
        print()

    print("BLUF Best Practices:")
    print("  • Start with a 50-70 word paragraph that directly answers the main query")
    print("  • Make it conversational and easy to understand")
    print("  • Include the key information someone needs to know")
    print("  • Think 'What would I want to see in an AI Overview?'")
    print()

    # Example
    print("Example BLUF format:")
    print('  "SEO (Search Engine Optimization) is the practice of improving')
    print('   website visibility in search engine results. It involves optimizing')
    print('   content, technical elements, and building authority through links.')
    print('   Good SEO increases organic traffic and helps potential customers')
    print('   find your business online."')
    print()

    # Exit code based on status
    if analysis.get('bluf_quality') == 'acceptable':
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
