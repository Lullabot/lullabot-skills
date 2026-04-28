#!/usr/bin/env python3
"""
E-E-A-T Signal Analyzer

Detects Experience, Expertise, Authoritativeness, and Trustworthiness signals
in web content. E-E-A-T is critical for both SEO rankings and GEO (AI citation
likelihood).

Usage:
    python3 analyze_eeat.py <html_file_or_url>

Checks:
    1. Author bylines with credentials
    2. External authoritative links (citations)
    3. Publish and last-modified dates
    4. Quoted content and expert attributions
    5. Trust signals (certifications, affiliations)
    6. Overall E-E-A-T score

References:
    - references/geo_best_practices.md section 4
    - references/seo_checklist.md "Content Quality" section
"""

import sys
import re
import json
from html.parser import HTMLParser
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CREDENTIAL_PATTERNS = [
    r'\bPh\.?D\.?\b', r'\bM\.?D\.?\b', r'\bM\.?B\.?A\.?\b',
    r'\bM\.?S\.?\b', r'\bB\.?S\.?\b', r'\bB\.?A\.?\b',
    r'\bJ\.?D\.?\b', r'\bEd\.?D\.?\b', r'\bD\.?O\.?\b',
    r'\bR\.?N\.?\b', r'\bC\.?P\.?A\.?\b', r'\bP\.?M\.?P\.?\b',
    r'\bC\.?F\.?P\.?\b', r'\bC\.?F\.?A\.?\b',
    r'\bDr\.?', r'\bProf\.?', r'\bProfessor\b',
]

AUTHORITATIVE_TLDS = {'.gov', '.edu', '.mil'}

AUTHORITATIVE_DOMAINS = {
    'who.int', 'nih.gov', 'cdc.gov', 'fda.gov', 'epa.gov',
    'nasa.gov', 'nature.com', 'science.org', 'pubmed.ncbi.nlm.nih.gov',
    'scholar.google.com', 'ieee.org', 'acm.org', 'reuters.com',
    'apnews.com', 'bbc.com', 'bbc.co.uk',
}

TRUST_CERT_PATTERNS = [
    r'\bISO\s*\d{4,5}\b', r'\bSOC\s*[12]\b', r'\bSOC\s*2\b',
    r'\bHIPAA\b', r'\bGDPR\b', r'\bPCI[\s-]DSS\b', r'\bFedRAMP\b',
    r'\bCCPA\b', r'\bFERPA\b',
]

ATTRIBUTION_PATTERNS = [
    r'according to\s+[A-Z]',
    r'(?:said|says|stated|noted|explained|reported)\s+[A-Z]',
    r'(?:—|--|-)\s*[A-Z][a-z]+\s+[A-Z]',  # — Jane Smith
    r'[""]\s*(?:—|--|-)\s*[A-Z]',           # closing quote — Name
]

BYLINE_PATTERNS = [
    r'(?:^|\n)\s*[Bb]y\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
    r'[Ww]ritten\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
    r'[Aa]uthor:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
    r'[Rr]eviewed\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
]

DATE_PATTERNS = [
    r'\b\d{4}-\d{2}-\d{2}\b',                          # 2024-01-15
    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b',
    r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b',
    r'\b\d{1,2}/\d{1,2}/\d{4}\b',
]


# ---------------------------------------------------------------------------
# HTML Parsers
# ---------------------------------------------------------------------------

class EEATParser(HTMLParser):
    """Parse HTML for E-E-A-T signals."""

    def __init__(self):
        super().__init__()
        # Meta / schema
        self.meta_tags = []
        self.json_ld_scripts = []
        self._in_json_ld = False
        self._json_ld_buf = []

        # Links
        self.links = []  # (href, text, is_external)

        # Blockquotes
        self.blockquotes = []
        self._in_blockquote = False
        self._blockquote_buf = []

        # Time elements
        self.time_elements = []

        # Text content
        self.text_chunks = []
        self._skip_depth = 0
        self._skip_tags = {'script', 'style', 'nav'}
        self._in_link = False
        self._link_text = []
        self._link_href = None

        # Author-related elements
        self.author_elements = []
        self._in_author_el = False
        self._author_el_tag = None
        self._author_buf = []

        # About / bio sections
        self.has_about_author = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag in self._skip_tags:
            self._skip_depth += 1

        # JSON-LD
        if tag == 'script' and attrs_dict.get('type') == 'application/ld+json':
            self._in_json_ld = True
            self._json_ld_buf = []

        # Meta tags
        if tag == 'meta':
            self.meta_tags.append(attrs_dict)

        # Links
        if tag == 'a':
            href = attrs_dict.get('href', '')
            self._in_link = True
            self._link_text = []
            self._link_href = href

        # Blockquotes
        if tag == 'blockquote':
            self._in_blockquote = True
            self._blockquote_buf = []

        # Time elements
        if tag == 'time':
            dt = attrs_dict.get('datetime', '')
            if dt:
                self.time_elements.append(dt)

        # Author-related class/id/rel — use word-boundary check to avoid
        # false positives on "authority" / "authoritative"
        cls = attrs_dict.get('class', '')
        id_attr = attrs_dict.get('id', '')
        rel = attrs_dict.get('rel', '')
        combined = f'{cls} {id_attr} {rel}'.lower()
        # Split on whitespace and non-alphanumeric to get tokens
        tokens = re.split(r'[^a-z0-9]+', combined)
        has_author_token = any(
            t in ('author', 'authors', 'byline') for t in tokens
        )
        has_about_token = 'about' in tokens
        if has_author_token:
            self._in_author_el = True
            self._author_el_tag = tag
            self._author_buf = []
        if has_author_token and has_about_token:
            self.has_about_author = True

    def handle_data(self, data):
        if self._in_json_ld:
            self._json_ld_buf.append(data)
            return

        if self._skip_depth > 0:
            return

        text = data.strip()
        if text:
            self.text_chunks.append(text)

        if self._in_link:
            self._link_text.append(text)

        if self._in_blockquote:
            self._blockquote_buf.append(text)

        if self._in_author_el:
            self._author_buf.append(text)

        # Check for "about the author" in visible text
        if 'about the author' in data.lower():
            self.has_about_author = True

    def handle_endtag(self, tag):
        if tag in self._skip_tags and self._skip_depth > 0:
            self._skip_depth -= 1

        if tag == 'script' and self._in_json_ld:
            raw = ''.join(self._json_ld_buf)
            try:
                self.json_ld_scripts.append(json.loads(raw))
            except json.JSONDecodeError:
                pass
            self._in_json_ld = False

        if tag == 'a' and self._in_link:
            link_text = ' '.join(self._link_text).strip()
            self.links.append((self._link_href, link_text))
            self._in_link = False

        if tag == 'blockquote' and self._in_blockquote:
            text = ' '.join(self._blockquote_buf).strip()
            if text:
                self.blockquotes.append(text)
            self._in_blockquote = False

        if self._in_author_el and tag == self._author_el_tag:
            text = ' '.join(self._author_buf).strip()
            if text:
                self.author_elements.append(text)
            self._in_author_el = False


# ---------------------------------------------------------------------------
# Detection Modules
# ---------------------------------------------------------------------------

def detect_authors(parser):
    """Detect author bylines and credentials."""
    authors = []
    credentials = []
    full_text = ' '.join(parser.text_chunks)

    # 1. Meta author tag
    for meta in parser.meta_tags:
        if meta.get('name', '').lower() == 'author':
            content = meta.get('content', '').strip()
            if content:
                authors.append(('meta_tag', content))

    # 2. JSON-LD author
    for schema in parser.json_ld_scripts:
        schemas = schema if isinstance(schema, list) else [schema]
        for s in schemas:
            author = s.get('author')
            if not author:
                continue
            if isinstance(author, dict):
                name = author.get('name', '')
                if name:
                    authors.append(('schema', name))
            elif isinstance(author, str):
                authors.append(('schema', author))
            elif isinstance(author, list):
                for a in author:
                    name = a.get('name', '') if isinstance(a, dict) else str(a)
                    if name:
                        authors.append(('schema', name))

    # 3. Author-class elements
    for text in parser.author_elements:
        authors.append(('html_element', text))

    # 4. Byline patterns in visible text
    for pattern in BYLINE_PATTERNS:
        for match in re.finditer(pattern, full_text):
            name = match.group(1) if match.lastindex else match.group(0)
            authors.append(('byline', name.strip()))

    # Deduplicate by name
    seen = set()
    unique_authors = []
    for source, name in authors:
        key = name.lower().strip()
        if key not in seen:
            seen.add(key)
            unique_authors.append((source, name))

    # Detect credentials in full text and author names
    search_text = full_text + ' ' + ' '.join(name for _, name in unique_authors)
    for pattern in CREDENTIAL_PATTERNS:
        for match in re.finditer(pattern, search_text):
            credentials.append(match.group(0))

    return unique_authors, list(set(credentials))


def detect_citations(parser, page_url=None):
    """Count and classify external links."""
    external_links = []
    authoritative_links = []

    page_domain = ''
    if page_url:
        parsed = urlparse(page_url)
        page_domain = parsed.netloc.lower()
        if page_domain.startswith('www.'):
            page_domain = page_domain[4:]

    for href, text in parser.links:
        if not href or href.startswith('#') or href.startswith('mailto:'):
            continue

        # Normalize protocol-relative URLs (//example.com/page)
        if href.startswith('//'):
            href = 'https:' + href

        try:
            parsed = urlparse(href)
        except Exception:
            continue

        if not parsed.netloc:
            continue

        domain = parsed.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]

        # Skip same-domain links
        if page_domain and domain == page_domain:
            continue

        external_links.append((href, text, domain))

        # Check if authoritative
        is_auth = False
        for tld in AUTHORITATIVE_TLDS:
            if domain.endswith(tld):
                is_auth = True
                break
        if domain in AUTHORITATIVE_DOMAINS:
            is_auth = True

        if is_auth:
            authoritative_links.append((href, text, domain))

    return external_links, authoritative_links


def detect_dates(parser):
    """Verify publish and last-modified dates."""
    dates = {}  # key: type, value: date string
    full_text = ' '.join(parser.text_chunks)

    # 1. Meta tags
    date_meta_names = {
        'article:published_time': 'published',
        'article:modified_time': 'modified',
        'datepublished': 'published',
        'datemodified': 'modified',
        'date': 'published',
        'last-modified': 'modified',
        'dcterms.date': 'published',
        'dcterms.modified': 'modified',
    }

    for meta in parser.meta_tags:
        name = meta.get('name', meta.get('property', '')).lower()
        content = meta.get('content', '').strip()
        if name in date_meta_names and content:
            dates[date_meta_names[name]] = ('meta', content)

    # 2. JSON-LD dates
    for schema in parser.json_ld_scripts:
        schemas = schema if isinstance(schema, list) else [schema]
        for s in schemas:
            if s.get('datePublished'):
                dates['published'] = ('schema', s['datePublished'])
            if s.get('dateModified'):
                dates['modified'] = ('schema', s['dateModified'])

    # 3. <time> elements
    for dt in parser.time_elements:
        if 'published' not in dates:
            dates['published'] = ('time_element', dt)

    # 4. Visible date patterns
    visible_dates = []
    for pattern in DATE_PATTERNS:
        for match in re.finditer(pattern, full_text):
            visible_dates.append(match.group(0))

    return dates, visible_dates


def detect_quotes(parser):
    """Detect quoted content and expert attributions."""
    # Join with single space and normalize whitespace for cross-tag matches
    full_text = re.sub(r'\s+', ' ', ' '.join(parser.text_chunks))

    # Blockquotes from HTML
    blockquotes = parser.blockquotes

    # Attribution patterns
    attributions = []
    for pattern in ATTRIBUTION_PATTERNS:
        for match in re.finditer(pattern, full_text, re.IGNORECASE):
            # Get surrounding context (up to 80 chars)
            start = max(0, match.start() - 20)
            end = min(len(full_text), match.end() + 60)
            context = full_text[start:end].strip()
            attributions.append(context)

    return blockquotes, attributions


def detect_trust_signals(parser):
    """Check for trust signals: certifications, credentials, affiliations."""
    full_text = ' '.join(parser.text_chunks)
    signals = []

    # 1. Certifications/compliance
    for pattern in TRUST_CERT_PATTERNS:
        for match in re.finditer(pattern, full_text, re.IGNORECASE):
            signals.append(('certification', match.group(0)))

    # 2. Privacy policy / terms links
    for href, text in parser.links:
        text_lower = text.lower() if text else ''
        href_lower = (href or '').lower()
        if 'privacy' in text_lower or 'privacy' in href_lower:
            signals.append(('policy', 'Privacy Policy'))
        if 'terms' in text_lower or 'terms-of-service' in href_lower or 'tos' in href_lower:
            signals.append(('policy', 'Terms of Service'))

    # 3. About the author section
    if parser.has_about_author:
        signals.append(('bio', 'About the Author section'))

    # Deduplicate
    seen = set()
    unique = []
    for kind, desc in signals:
        key = f'{kind}:{desc.lower()}'
        if key not in seen:
            seen.add(key)
            unique.append((kind, desc))

    return unique


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def calculate_score(authors, credentials, external_links, authoritative_links,
                    dates, visible_dates, blockquotes, attributions,
                    trust_signals, has_about_author):
    """
    Score each E-E-A-T dimension 0-25, total 0-100.

    Experience:        Author bylines + first-person presence + expert quotes
    Expertise:         Credentials + authoritative citations + depth
    Authoritativeness: External authoritative links + schema + affiliations
    Trustworthiness:   Dates visible + trust signals + policy links
    """
    # Experience (0-25)
    experience = 0
    if authors:
        experience += 10
    if blockquotes:
        experience += min(len(blockquotes) * 3, 8)
    if attributions:
        experience += min(len(attributions) * 2, 7)

    # Expertise (0-25)
    expertise = 0
    if credentials:
        expertise += min(len(credentials) * 5, 12)
    if authoritative_links:
        expertise += min(len(authoritative_links) * 2, 8)
    if len(external_links) >= 3:
        expertise += 5

    # Authoritativeness (0-25)
    authoritativeness = 0
    if authoritative_links:
        authoritativeness += min(len(authoritative_links) * 3, 12)
    if any(s == 'schema' for s, _ in authors):
        authoritativeness += 5
    cert_signals = [s for s in trust_signals if s[0] == 'certification']
    if cert_signals:
        authoritativeness += min(len(cert_signals) * 3, 8)

    # Trustworthiness (0-25)
    trustworthiness = 0
    if 'published' in dates:
        trustworthiness += 5
    if 'modified' in dates:
        trustworthiness += 5
    if visible_dates:
        trustworthiness += 3
    policy_signals = [s for s in trust_signals if s[0] == 'policy']
    if policy_signals:
        trustworthiness += min(len(policy_signals) * 3, 6)
    if has_about_author:
        trustworthiness += 6

    # Cap each at 25
    experience = min(experience, 25)
    expertise = min(expertise, 25)
    authoritativeness = min(authoritativeness, 25)
    trustworthiness = min(trustworthiness, 25)

    return {
        'experience': experience,
        'expertise': expertise,
        'authoritativeness': authoritativeness,
        'trustworthiness': trustworthiness,
        'total': experience + expertise + authoritativeness + trustworthiness,
    }


def rating_label(total):
    """Return a human-readable rating."""
    if total >= 75:
        return '✅ EXCELLENT'
    elif total >= 50:
        return '⚠️  GOOD'
    elif total >= 25:
        return '⚠️  NEEDS IMPROVEMENT'
    else:
        return '❌ POOR'


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_report(authors, credentials, external_links, authoritative_links,
                 dates, visible_dates, blockquotes, attributions,
                 trust_signals, scores, has_about_author):
    """Print structured E-E-A-T analysis report."""

    print('E-E-A-T SIGNAL ANALYSIS')
    print('=' * 80)
    print()

    # --- Authors ---
    print('AUTHOR DETECTION')
    print('-' * 80)
    if authors:
        for source, name in authors:
            print(f'  ✅ Author found ({source}): {name}')
    else:
        print('  ❌ No author byline detected')
        print('     Recommendation: Add author name with "By [Name]" or <meta name="author">')

    if credentials:
        print(f'  ✅ Credentials detected: {", ".join(credentials)}')
    else:
        print('  ⚠️  No credentials detected')
        print('     Recommendation: Include author credentials (degrees, certifications, titles)')
    print()

    # --- Citations ---
    print('CITATIONS & AUTHORITATIVE LINKS')
    print('-' * 80)
    print(f'  External links:      {len(external_links)}')
    print(f'  Authoritative links: {len(authoritative_links)}')

    if authoritative_links:
        print()
        print('  Authoritative sources:')
        for href, text, domain in authoritative_links[:5]:
            label = text[:50] if text else domain
            print(f'    ✅ {label} ({domain})')
        if len(authoritative_links) > 5:
            print(f'    ... and {len(authoritative_links) - 5} more')
    else:
        print('  ❌ No authoritative (.gov, .edu, .mil, or high-trust) links found')
        print('     Recommendation: Cite authoritative sources to boost E-E-A-T')

    if len(external_links) < 3:
        print(f'  ⚠️  Few external links ({len(external_links)})')
        print('     Recommendation: Add 3+ external citations to credible sources')
    print()

    # --- Dates ---
    print('PUBLISH & MODIFIED DATES')
    print('-' * 80)
    if 'published' in dates:
        source, value = dates['published']
        print(f'  ✅ Published date ({source}): {value}')
    else:
        print('  ❌ No published date detected')
        print('     Recommendation: Add datePublished in Article schema or meta tags')

    if 'modified' in dates:
        source, value = dates['modified']
        print(f'  ✅ Modified date ({source}): {value}')
    else:
        print('  ⚠️  No modified date detected')
        print('     Recommendation: Add dateModified to show content freshness')

    if visible_dates:
        print(f'  ✅ Visible dates found: {", ".join(visible_dates[:3])}')
    else:
        print('  ⚠️  No dates visible in page content')
        print('     Recommendation: Display publish/update dates prominently')
    print()

    # --- Quotes & Attributions ---
    print('QUOTED CONTENT & EXPERT ATTRIBUTIONS')
    print('-' * 80)
    if blockquotes:
        print(f'  ✅ Blockquotes found: {len(blockquotes)}')
        for bq in blockquotes[:2]:
            preview = bq[:80] + '...' if len(bq) > 80 else bq
            print(f'     "{preview}"')
    else:
        print('  ⚠️  No blockquotes found')

    if attributions:
        print(f'  ✅ Expert attributions found: {len(attributions)}')
        for attr in attributions[:3]:
            print(f'     ...{attr}...')
    else:
        print('  ⚠️  No expert attributions detected')
        print('     Recommendation: Add quotes with "according to [Expert]" or blockquotes')
    print()

    # --- Trust Signals ---
    print('TRUST SIGNALS')
    print('-' * 80)
    if trust_signals:
        for kind, desc in trust_signals:
            print(f'  ✅ {kind.title()}: {desc}')
    else:
        print('  ⚠️  No trust signals detected')

    if has_about_author:
        print('  ✅ "About the Author" section present')

    if not trust_signals and not has_about_author:
        print('     Recommendation: Add certifications, privacy policy, or author bio section')
    print()

    # --- Overall Score ---
    print('OVERALL E-E-A-T SCORE')
    print('-' * 80)
    total = scores['total']
    label = rating_label(total)

    print(f'  Experience:        {scores["experience"]:>2}/25')
    print(f'  Expertise:         {scores["expertise"]:>2}/25')
    print(f'  Authoritativeness: {scores["authoritativeness"]:>2}/25')
    print(f'  Trustworthiness:   {scores["trustworthiness"]:>2}/25')
    print()
    print(f'  Total: {total}/100 — {label}')
    print()

    if total < 50:
        print('Top recommendations:')
        if not authors:
            print('  1. Add visible author byline with credentials')
        if not authoritative_links:
            print('  2. Cite authoritative sources (.gov, .edu, established orgs)')
        if 'published' not in dates:
            print('  3. Add datePublished in schema or meta tags')
        if not blockquotes and not attributions:
            print('  4. Include expert quotes with attributions')
        if not trust_signals:
            print('  5. Add trust signals (certifications, privacy policy)')
        print()

    print('Reference: references/geo_best_practices.md section 4 (E-E-A-T Signals)')
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def analyze_eeat(html_content, page_url=None):
    """Run full E-E-A-T analysis on HTML content. Returns scores dict."""
    parser = EEATParser()
    parser.feed(html_content)

    authors, credentials = detect_authors(parser)
    external_links, authoritative_links = detect_citations(parser, page_url)
    dates, visible_dates = detect_dates(parser)
    blockquotes, attributions = detect_quotes(parser)
    trust_signals = detect_trust_signals(parser)

    scores = calculate_score(
        authors, credentials, external_links, authoritative_links,
        dates, visible_dates, blockquotes, attributions,
        trust_signals, parser.has_about_author,
    )

    print_report(
        authors, credentials, external_links, authoritative_links,
        dates, visible_dates, blockquotes, attributions,
        trust_signals, scores, parser.has_about_author,
    )

    return scores


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 analyze_eeat.py <html_file_or_url>')
        print('Example: python3 analyze_eeat.py page.html')
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        if input_path.startswith('http://') or input_path.startswith('https://'):
            import urllib.request
            with urllib.request.urlopen(input_path) as response:
                html_content = response.read().decode('utf-8')
            page_url = input_path
        else:
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            page_url = None

        scores = analyze_eeat(html_content, page_url)

        # Exit code: 0 if Good or better, 1 if needs improvement
        sys.exit(0 if scores['total'] >= 50 else 1)

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
