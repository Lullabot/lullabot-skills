#!/usr/bin/env python3
"""
Readability Checker for GEO Optimization

Implements Flesch-Kincaid Grade Level and Flesch Reading Ease algorithms
to ensure content meets GEO best practices (target: 8th grade or below).

Usage:
    python3 check_readability.py <html_file>
    python3 check_readability.py <html_file> --target-grade 8

References:
    - Flesch-Kincaid Grade Level: 0.39 * (total words / total sentences) + 11.8 * (total syllables / total words) - 15.59
    - Flesch Reading Ease: 206.835 - 1.015 * (total words / total sentences) - 84.6 * (total syllables / total words)
    - AI prefers content with conversational, 8th-grade readability
"""

import sys
import re
from html.parser import HTMLParser
from pathlib import Path


class TextExtractor(HTMLParser):
    """Extract text content from HTML, excluding script/style tags."""

    def __init__(self):
        super().__init__()
        self.text = []
        self.in_script_style = False

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            self.in_script_style = True

    def handle_endtag(self, tag):
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            self.in_script_style = False

    def handle_data(self, data):
        if not self.in_script_style:
            self.text.append(data)

    def get_text(self):
        return ' '.join(self.text)


def count_syllables(word):
    """
    Count syllables in a word using a simple heuristic.

    Rules:
    - Count vowel groups (consecutive vowels = 1 syllable)
    - Silent 'e' at end doesn't count
    - Minimum 1 syllable per word
    """
    word = word.lower().strip(".,!?;:")

    if len(word) <= 3:
        return 1

    # Remove silent e
    if word.endswith('e'):
        word = word[:-1]

    # Count vowel groups
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel

    # Ensure at least 1 syllable
    return max(1, syllable_count)


def extract_text_from_html(html_content):
    """Extract readable text content from HTML."""
    parser = TextExtractor()
    parser.feed(html_content)
    return parser.get_text()


def calculate_readability(text):
    """
    Calculate readability metrics for the given text.

    Returns:
        dict: {
            'total_words': int,
            'total_sentences': int,
            'total_syllables': int,
            'flesch_kincaid_grade': float,
            'flesch_reading_ease': float,
            'avg_words_per_sentence': float,
            'avg_syllables_per_word': float
        }
    """
    # Split into sentences (basic sentence detection)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    total_sentences = len(sentences)

    if total_sentences == 0:
        return None

    # Split into words
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    total_words = len(words)

    if total_words == 0:
        return None

    # Count syllables
    total_syllables = sum(count_syllables(word) for word in words)

    # Calculate metrics
    avg_words_per_sentence = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words

    # Flesch-Kincaid Grade Level
    fk_grade = (0.39 * avg_words_per_sentence) + (11.8 * avg_syllables_per_word) - 15.59

    # Flesch Reading Ease
    fre_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)

    return {
        'total_words': total_words,
        'total_sentences': total_sentences,
        'total_syllables': total_syllables,
        'flesch_kincaid_grade': round(fk_grade, 1),
        'flesch_reading_ease': round(fre_score, 1),
        'avg_words_per_sentence': round(avg_words_per_sentence, 1),
        'avg_syllables_per_word': round(avg_syllables_per_word, 2)
    }


def interpret_fre_score(score):
    """Interpret Flesch Reading Ease score."""
    if score >= 90:
        return "Very Easy (5th grade)"
    elif score >= 80:
        return "Easy (6th grade)"
    elif score >= 70:
        return "Fairly Easy (7th grade)"
    elif score >= 60:
        return "Standard (8th-9th grade)"
    elif score >= 50:
        return "Fairly Difficult (10th-12th grade)"
    elif score >= 30:
        return "Difficult (College level)"
    else:
        return "Very Difficult (College graduate)"


def get_recommendations(metrics, target_grade=8):
    """Generate recommendations based on readability metrics."""
    recommendations = []

    grade = metrics['flesch_kincaid_grade']

    if grade > target_grade:
        recommendations.append(f"⚠️  Content is at grade {grade} level, target is grade {target_grade} or below")

        if metrics['avg_words_per_sentence'] > 20:
            recommendations.append(
                f"• Shorten sentences: Average {metrics['avg_words_per_sentence']} words per sentence "
                f"(target: 15-20 words)"
            )

        if metrics['avg_syllables_per_word'] > 1.6:
            recommendations.append(
                f"• Use simpler words: Average {metrics['avg_syllables_per_word']} syllables per word "
                f"(target: 1.5 or below)"
            )

        recommendations.append("• Use conversational language and avoid jargon")
        recommendations.append("• Break complex ideas into multiple sentences")
        recommendations.append("• Replace complex words with simpler alternatives")
    else:
        recommendations.append(f"✅ Content meets target grade level ({grade} ≤ {target_grade})")

    return recommendations


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_readability.py <html_file> [--target-grade N]")
        sys.exit(1)

    html_file = sys.argv[1]
    target_grade = 8  # Default target for GEO

    # Parse optional target grade
    if '--target-grade' in sys.argv:
        idx = sys.argv.index('--target-grade')
        if idx + 1 < len(sys.argv):
            target_grade = int(sys.argv[idx + 1])

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

    # Extract text
    text = extract_text_from_html(html_content)

    if not text.strip():
        print("Error: No readable text found in HTML")
        sys.exit(1)

    # Calculate readability
    metrics = calculate_readability(text)

    if not metrics:
        print("Error: Unable to calculate readability metrics")
        sys.exit(1)

    # Display results
    print("=" * 60)
    print("READABILITY ANALYSIS (GEO Optimization)")
    print("=" * 60)
    print()
    print(f"Content Statistics:")
    print(f"  Words:              {metrics['total_words']:,}")
    print(f"  Sentences:          {metrics['total_sentences']:,}")
    print(f"  Syllables:          {metrics['total_syllables']:,}")
    print(f"  Avg Words/Sentence: {metrics['avg_words_per_sentence']}")
    print(f"  Avg Syllables/Word: {metrics['avg_syllables_per_word']}")
    print()
    print(f"Readability Scores:")
    print(f"  Flesch-Kincaid Grade Level: {metrics['flesch_kincaid_grade']}")
    print(f"  Flesch Reading Ease:        {metrics['flesch_reading_ease']} ({interpret_fre_score(metrics['flesch_reading_ease'])})")
    print()
    print(f"GEO Target: Grade {target_grade} or below")
    print()

    # Get recommendations
    recommendations = get_recommendations(metrics, target_grade)

    print("Recommendations:")
    for rec in recommendations:
        print(rec)
    print()

    # Exit code based on pass/fail
    if metrics['flesch_kincaid_grade'] <= target_grade:
        print("STATUS: ✅ PASS - Content is AI-friendly")
        sys.exit(0)
    else:
        print("STATUS: ⚠️  NEEDS IMPROVEMENT - Content may be too complex for optimal AI citations")
        sys.exit(1)


if __name__ == '__main__':
    main()
