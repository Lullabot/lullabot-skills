#!/usr/bin/env python3

"""
Heading Hierarchy Analyzer with GEO Question-Based Detection

Analyzes heading structure and detects question-based headers for GEO optimization.
Long-tail queries of 8+ words are 7x more likely to trigger AI Overviews.

Usage: ./analyze_headings.py <html_file_or_url>
"""

import sys
import re
from html.parser import HTMLParser

class HeadingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.current_heading = None
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_tag = tag
            self.current_heading = {'tag': tag, 'level': int(tag[1]), 'text': '', 'attrs': dict(attrs)}

    def handle_data(self, data):
        if self.current_heading is not None:
            self.current_heading['text'] += data.strip()

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and self.current_heading:
            if self.current_heading['text']:  # Only add if not empty
                self.headings.append(self.current_heading)
            self.current_heading = None
            self.current_tag = None

def analyze_heading_hierarchy(html_content):
    """Parse and analyze heading hierarchy from HTML content"""
    parser = HeadingParser()
    parser.feed(html_content)

    print("Heading Hierarchy Analysis")
    print("=" * 80)
    print()

    if not parser.headings:
        print("✗ No headings found on the page!")
        print("  Recommendation: Add proper heading structure (H1-H6) for better SEO")
        return

    print(f"Total headings found: {len(parser.headings)}")
    print()

    # Count headings by level
    heading_counts = {}
    for h in parser.headings:
        level = h['level']
        heading_counts[level] = heading_counts.get(level, 0) + 1

    print("HEADING COUNT BY LEVEL")
    print("-" * 80)
    for level in range(1, 7):
        count = heading_counts.get(level, 0)
        symbol = "✓" if count > 0 else " "
        print(f"{symbol} H{level}: {count}")
    print()

    # Check for H1
    h1_headings = [h for h in parser.headings if h['level'] == 1]
    print("H1 TAG ANALYSIS")
    print("-" * 80)
    if not h1_headings:
        print("✗ CRITICAL: No H1 tag found!")
        print("  Recommendation: Every page should have exactly one H1 tag describing the main topic")
    elif len(h1_headings) == 1:
        print(f"✓ Correct: One H1 tag found")
        print(f"  Text: {h1_headings[0]['text']}")
        print(f"  Length: {len(h1_headings[0]['text'])} characters")
    else:
        print(f"⚠ WARNING: Multiple H1 tags found ({len(h1_headings)})")
        print("  Recommendation: Use only one H1 tag per page")
        for i, h1 in enumerate(h1_headings, 1):
            print(f"  {i}. {h1['text']}")
    print()

    # Check hierarchy
    print("HIERARCHY VALIDATION")
    print("-" * 80)
    issues = []
    prev_level = 0

    for i, heading in enumerate(parser.headings):
        level = heading['level']

        # Check for skipped levels
        if level > prev_level + 1:
            issues.append({
                'type': 'skipped_level',
                'position': i + 1,
                'heading': heading,
                'prev_level': prev_level,
                'message': f"Skipped from H{prev_level} to H{level}"
            })

        prev_level = level

    if not issues:
        print("✓ Heading hierarchy is properly structured")
    else:
        print(f"⚠ Found {len(issues)} hierarchy issues:")
        for issue in issues:
            print(f"  • Position {issue['position']}: {issue['message']}")
            print(f"    Text: {issue['heading']['text']}")
    print()

    # Display full hierarchy
    print("COMPLETE HEADING STRUCTURE")
    print("-" * 80)
    for i, heading in enumerate(parser.headings, 1):
        level = heading['level']
        indent = "  " * (level - 1)
        text = heading['text'][:70] + "..." if len(heading['text']) > 70 else heading['text']
        print(f"{indent}H{level}: {text}")
    print()

    # Check for empty headings
    empty_headings = [h for h in parser.headings if not h['text'].strip()]
    if empty_headings:
        print("EMPTY HEADINGS")
        print("-" * 80)
        print(f"⚠ Found {len(empty_headings)} empty heading(s)")
        print("  Recommendation: All headings should contain descriptive text")
        print()

    # GEO: Question-based header analysis
    print("GEO: QUESTION-BASED HEADER ANALYSIS")
    print("-" * 80)

    # Question words and patterns
    question_words = [
        'what', 'why', 'how', 'when', 'where', 'who', 'which', 'whose',
        'can', 'could', 'should', 'would', 'will', 'do', 'does', 'did',
        'is', 'are', 'am', 'was', 'were'
    ]

    question_headings = []
    long_tail_headings = []

    for heading in parser.headings:
        text = heading['text'].strip()
        text_lower = text.lower()
        word_count = len(text.split())

        # Check if it's a question (ends with ? or starts with question word)
        is_question = False

        if text.endswith('?'):
            is_question = True
        else:
            # Check if starts with question word
            first_word = text_lower.split()[0] if text_lower.split() else ''
            if first_word in question_words:
                is_question = True

        if is_question:
            question_headings.append({
                'heading': heading,
                'word_count': word_count,
                'is_long_tail': word_count >= 8
            })

        # Check for long-tail (8+ words)
        if word_count >= 8:
            long_tail_headings.append({
                'heading': heading,
                'word_count': word_count,
                'is_question': is_question
            })

    # H2 and H3 headings (primary targets for GEO)
    h2_h3_headings = [h for h in parser.headings if h['level'] in [2, 3]]
    h2_h3_questions = [q for q in question_headings if q['heading']['level'] in [2, 3]]

    total_h2_h3 = len(h2_h3_headings)
    question_count = len(question_headings)
    h2_h3_question_count = len(h2_h3_questions)

    # Calculate percentages
    if total_h2_h3 > 0:
        question_percentage = (h2_h3_question_count / total_h2_h3) * 100
    else:
        question_percentage = 0

    print(f"Total headings:           {len(parser.headings)}")
    print(f"Question-based headings:  {question_count} ({(question_count/len(parser.headings)*100):.1f}%)")
    print(f"H2/H3 headings:           {total_h2_h3}")
    print(f"H2/H3 questions:          {h2_h3_question_count} ({question_percentage:.1f}%)")
    print(f"Long-tail headings (8+):  {len(long_tail_headings)}")
    print()

    # GEO recommendations
    if question_percentage < 30:
        print("⚠️  RECOMMENDATION: Increase question-based H2/H3 headers")
        print("   Target: 30%+ of H2/H3 headers should be questions")
        print("   AI Overviews favor question-based content structure")
        print()
        print("   Examples of converting headers to questions:")
        non_question_h2h3 = [h for h in h2_h3_headings if h not in [q['heading'] for q in h2_h3_questions]]
        for i, heading in enumerate(non_question_h2h3[:3], 1):
            text = heading['text']
            print(f"   {i}. \"{text}\"")
            # Suggest question format
            if text.lower().startswith(('benefits', 'advantages')):
                print(f"      → \"What are the {text.lower()}?\"")
            elif text.lower().startswith(('features', 'characteristics')):
                print(f"      → \"What {text.lower()} should you know?\"")
            elif text.lower().startswith(('process', 'steps', 'guide')):
                print(f"      → \"How to {text.lower().replace('process', '').strip()}?\"")
            else:
                print(f"      → \"What is {text.lower()}?\" or \"How does {text.lower()} work?\"")
        print()
    else:
        print(f"✓ Good: {question_percentage:.1f}% of H2/H3 headers are questions")
        print()

    # Display question headings
    if question_headings:
        print("Question-based headings found:")
        for q in question_headings:
            h = q['heading']
            marker = "🎯" if q['is_long_tail'] else "  "
            print(f"  {marker} H{h['level']}: {h['text']} ({q['word_count']} words)")
        print()
        if any(q['is_long_tail'] for q in question_headings):
            print("🎯 = Long-tail query (8+ words, 7x more likely to trigger AI Overviews)")
            print()

    # Long-tail analysis
    if long_tail_headings:
        print("Long-tail headings (8+ words, optimal for GEO):")
        for lt in long_tail_headings:
            h = lt['heading']
            marker = "?" if lt['is_question'] else " "
            print(f"  {marker} H{h['level']}: {h['text']} ({lt['word_count']} words)")
        print()

    # Keyword density check (basic)
    print("KEYWORD USAGE")
    print("-" * 80)
    all_text = ' '.join([h['text'].lower() for h in parser.headings])
    words = re.findall(r'\b\w+\b', all_text)

    if words:
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Only count words longer than 3 characters
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top 10 most common words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

        print("Top keywords in headings:")
        for word, count in top_words:
            print(f"  • {word}: {count} occurrence(s)")
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: ./analyze_headings.py <html_file_or_url>")
        print("Example: ./analyze_headings.py page.html")
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

        analyze_heading_hierarchy(html_content)

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
