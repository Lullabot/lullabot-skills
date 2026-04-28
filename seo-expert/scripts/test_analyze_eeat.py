#!/usr/bin/env python3
"""Unit tests for analyze_eeat.py detection modules."""

import unittest

from analyze_eeat import (
    EEATParser,
    calculate_score,
    detect_authors,
    detect_citations,
    detect_dates,
    detect_quotes,
    detect_trust_signals,
    rating_label,
)


def _parse(html):
    """Helper: parse HTML and return EEATParser."""
    parser = EEATParser()
    parser.feed(html)
    return parser


# ---- Minimal HTML (no signals) ----
MINIMAL_HTML = """
<html><head><title>Test</title></head>
<body><p>Hello world.</p></body></html>
"""

# ---- Rich HTML (all signals) ----
RICH_HTML = """
<html>
<head>
  <title>Expert Guide to SEO</title>
  <meta name="author" content="Dr. Jane Smith">
  <meta property="article:published_time" content="2025-01-15">
  <meta property="article:modified_time" content="2025-06-01">
  <script type="application/ld+json">
  {
    "@type": "Article",
    "author": {"@type": "Person", "name": "Dr. Jane Smith"},
    "datePublished": "2025-01-15",
    "dateModified": "2025-06-01"
  }
  </script>
</head>
<body>
  <div class="author-bio">
    <p>By Dr. Jane Smith, PhD</p>
    <p>About the Author: Dr. Smith has 20 years of experience.</p>
  </div>
  <article>
    <p>Published January 15, 2025. Updated June 1, 2025.</p>
    <p>According to Dr. John Doe, SEO requires consistent effort.</p>
    <blockquote>Search engine optimization is essential for visibility.</blockquote>
    <p>We are ISO 27001 certified and HIPAA compliant.</p>
    <a href="https://www.nih.gov/research">NIH Research</a>
    <a href="https://example.edu/paper">University Paper</a>
    <a href="https://www.cdc.gov/data">CDC Data</a>
    <a href="https://example.com/other">Other Site</a>
    <a href="/privacy-policy">Privacy Policy</a>
    <a href="/terms-of-service">Terms of Service</a>
  </article>
</body>
</html>
"""


class TestAuthorDetection(unittest.TestCase):
    def test_no_authors_in_minimal(self):
        parser = _parse(MINIMAL_HTML)
        authors, creds = detect_authors(parser)
        self.assertEqual(len(authors), 0)
        self.assertEqual(len(creds), 0)

    def test_meta_author(self):
        html = '<html><head><meta name="author" content="Alice Jones"></head><body></body></html>'
        parser = _parse(html)
        authors, _ = detect_authors(parser)
        names = [name for _, name in authors]
        self.assertIn('Alice Jones', names)

    def test_schema_author(self):
        html = '''<html><head>
        <script type="application/ld+json">{"@type":"Article","author":{"name":"Bob Lee"}}</script>
        </head><body></body></html>'''
        parser = _parse(html)
        authors, _ = detect_authors(parser)
        names = [name for _, name in authors]
        self.assertIn('Bob Lee', names)

    def test_byline_pattern(self):
        html = '<html><body><p>By Sarah Connor</p></body></html>'
        parser = _parse(html)
        authors, _ = detect_authors(parser)
        names = [name for _, name in authors]
        self.assertIn('Sarah Connor', names)

    def test_credentials_detected(self):
        html = '<html><body><p>By Dr. Jane Smith, PhD, MBA</p></body></html>'
        parser = _parse(html)
        _, creds = detect_authors(parser)
        cred_text = ' '.join(creds)
        self.assertIn('PhD', cred_text)

    def test_author_element_class(self):
        html = '<html><body><div class="author-info"><span>Mark Twain</span></div></body></html>'
        parser = _parse(html)
        authors, _ = detect_authors(parser)
        self.assertTrue(any('Mark Twain' in name for _, name in authors))

    def test_rich_html_authors(self):
        parser = _parse(RICH_HTML)
        authors, creds = detect_authors(parser)
        self.assertGreaterEqual(len(authors), 1)
        self.assertGreater(len(creds), 0)


class TestCitationDetection(unittest.TestCase):
    def test_no_external_links_in_minimal(self):
        parser = _parse(MINIMAL_HTML)
        ext, auth = detect_citations(parser)
        self.assertEqual(len(ext), 0)
        self.assertEqual(len(auth), 0)

    def test_authoritative_gov_link(self):
        html = '<html><body><a href="https://www.nih.gov/page">NIH</a></body></html>'
        parser = _parse(html)
        ext, auth = detect_citations(parser)
        self.assertEqual(len(ext), 1)
        self.assertEqual(len(auth), 1)

    def test_edu_link(self):
        html = '<html><body><a href="https://mit.edu/paper">MIT Paper</a></body></html>'
        parser = _parse(html)
        _, auth = detect_citations(parser)
        self.assertEqual(len(auth), 1)

    def test_regular_external_not_authoritative(self):
        html = '<html><body><a href="https://random-blog.com/post">Blog</a></body></html>'
        parser = _parse(html)
        ext, auth = detect_citations(parser)
        self.assertEqual(len(ext), 1)
        self.assertEqual(len(auth), 0)

    def test_same_domain_excluded(self):
        html = '<html><body><a href="https://mysite.com/page">Internal</a></body></html>'
        parser = _parse(html)
        ext, _ = detect_citations(parser, page_url='https://mysite.com/')
        self.assertEqual(len(ext), 0)

    def test_rich_html_citations(self):
        parser = _parse(RICH_HTML)
        ext, auth = detect_citations(parser)
        self.assertGreaterEqual(len(ext), 3)
        self.assertGreaterEqual(len(auth), 2)


class TestDateDetection(unittest.TestCase):
    def test_no_dates_in_minimal(self):
        parser = _parse(MINIMAL_HTML)
        dates, visible = detect_dates(parser)
        self.assertEqual(len(dates), 0)

    def test_meta_published_time(self):
        html = '<html><head><meta property="article:published_time" content="2025-01-15"></head><body></body></html>'
        parser = _parse(html)
        dates, _ = detect_dates(parser)
        self.assertIn('published', dates)

    def test_schema_dates(self):
        html = '''<html><head>
        <script type="application/ld+json">{"@type":"Article","datePublished":"2025-01-15","dateModified":"2025-06-01"}</script>
        </head><body></body></html>'''
        parser = _parse(html)
        dates, _ = detect_dates(parser)
        self.assertIn('published', dates)
        self.assertIn('modified', dates)

    def test_time_element(self):
        html = '<html><body><time datetime="2025-03-20">March 20, 2025</time></body></html>'
        parser = _parse(html)
        dates, _ = detect_dates(parser)
        self.assertIn('published', dates)

    def test_visible_date_patterns(self):
        html = '<html><body><p>Published January 15, 2025</p></body></html>'
        parser = _parse(html)
        _, visible = detect_dates(parser)
        self.assertGreater(len(visible), 0)

    def test_rich_html_dates(self):
        parser = _parse(RICH_HTML)
        dates, visible = detect_dates(parser)
        self.assertIn('published', dates)
        self.assertIn('modified', dates)
        self.assertGreater(len(visible), 0)


class TestQuoteDetection(unittest.TestCase):
    def test_no_quotes_in_minimal(self):
        parser = _parse(MINIMAL_HTML)
        bq, attr = detect_quotes(parser)
        self.assertEqual(len(bq), 0)
        self.assertEqual(len(attr), 0)

    def test_blockquote_detected(self):
        html = '<html><body><blockquote>This is important.</blockquote></body></html>'
        parser = _parse(html)
        bq, _ = detect_quotes(parser)
        self.assertEqual(len(bq), 1)
        self.assertIn('This is important.', bq[0])

    def test_attribution_pattern(self):
        html = '<html><body><p>According to Dr. Smith, SEO matters.</p></body></html>'
        parser = _parse(html)
        _, attr = detect_quotes(parser)
        self.assertGreater(len(attr), 0)

    def test_rich_html_quotes(self):
        parser = _parse(RICH_HTML)
        bq, attr = detect_quotes(parser)
        self.assertGreater(len(bq), 0)
        self.assertGreater(len(attr), 0)


class TestTrustSignalDetection(unittest.TestCase):
    def test_no_signals_in_minimal(self):
        parser = _parse(MINIMAL_HTML)
        signals = detect_trust_signals(parser)
        self.assertEqual(len(signals), 0)

    def test_iso_certification(self):
        html = '<html><body><p>We are ISO 27001 certified.</p></body></html>'
        parser = _parse(html)
        signals = detect_trust_signals(parser)
        certs = [s for s in signals if s[0] == 'certification']
        self.assertGreater(len(certs), 0)

    def test_hipaa_detected(self):
        html = '<html><body><p>HIPAA compliant systems.</p></body></html>'
        parser = _parse(html)
        signals = detect_trust_signals(parser)
        self.assertTrue(any('HIPAA' in desc for _, desc in signals))

    def test_privacy_policy_link(self):
        html = '<html><body><a href="/privacy">Privacy Policy</a></body></html>'
        parser = _parse(html)
        signals = detect_trust_signals(parser)
        self.assertTrue(any(desc == 'Privacy Policy' for _, desc in signals))

    def test_terms_link(self):
        html = '<html><body><a href="/terms-of-service">Terms of Service</a></body></html>'
        parser = _parse(html)
        signals = detect_trust_signals(parser)
        self.assertTrue(any(desc == 'Terms of Service' for _, desc in signals))

    def test_about_author_section(self):
        html = '<html><body><p>About the Author: Expert in SEO.</p></body></html>'
        parser = _parse(html)
        signals = detect_trust_signals(parser)
        self.assertTrue(any(s[0] == 'bio' for s in signals))

    def test_rich_html_trust_signals(self):
        parser = _parse(RICH_HTML)
        signals = detect_trust_signals(parser)
        self.assertGreater(len(signals), 0)


class TestScoring(unittest.TestCase):
    def test_minimal_html_low_score(self):
        parser = _parse(MINIMAL_HTML)
        authors, creds = detect_authors(parser)
        ext, auth = detect_citations(parser)
        dates, visible = detect_dates(parser)
        bq, attr = detect_quotes(parser)
        trust = detect_trust_signals(parser)
        scores = calculate_score(
            authors, creds, ext, auth, dates, visible, bq, attr, trust, False
        )
        self.assertLess(scores['total'], 25)

    def test_rich_html_high_score(self):
        parser = _parse(RICH_HTML)
        authors, creds = detect_authors(parser)
        ext, auth = detect_citations(parser)
        dates, visible = detect_dates(parser)
        bq, attr = detect_quotes(parser)
        trust = detect_trust_signals(parser)
        scores = calculate_score(
            authors, creds, ext, auth, dates, visible, bq, attr, trust, parser.has_about_author
        )
        self.assertGreaterEqual(scores['total'], 50)

    def test_each_dimension_capped_at_25(self):
        scores = calculate_score(
            [('meta', 'A')] * 10, ['PhD'] * 10,
            [('h', 't', 'd')] * 20, [('h', 't', 'd')] * 20,
            {'published': ('m', 'v'), 'modified': ('m', 'v')},
            ['2025-01-01'] * 10,
            ['quote'] * 10, ['attr'] * 10,
            [('certification', 'ISO'), ('policy', 'Privacy'), ('policy', 'Terms')] * 5,
            True,
        )
        self.assertLessEqual(scores['experience'], 25)
        self.assertLessEqual(scores['expertise'], 25)
        self.assertLessEqual(scores['authoritativeness'], 25)
        self.assertLessEqual(scores['trustworthiness'], 25)
        self.assertLessEqual(scores['total'], 100)


class TestRatingLabel(unittest.TestCase):
    def test_excellent(self):
        self.assertIn('EXCELLENT', rating_label(75))
        self.assertIn('EXCELLENT', rating_label(100))

    def test_good(self):
        self.assertIn('GOOD', rating_label(50))
        self.assertIn('GOOD', rating_label(74))

    def test_needs_improvement(self):
        self.assertIn('NEEDS IMPROVEMENT', rating_label(25))
        self.assertIn('NEEDS IMPROVEMENT', rating_label(49))

    def test_poor(self):
        self.assertIn('POOR', rating_label(0))
        self.assertIn('POOR', rating_label(24))


if __name__ == '__main__':
    unittest.main()
