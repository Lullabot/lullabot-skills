# Content Structure Guide for GEO Optimization

## Overview

Proper content structure is critical for both user experience and AI citation rates. This guide covers BLUF format, question-based headers, FAQ sections, and other structural elements optimized for GEO.

## BLUF: Bottom Line Up Front

### What is BLUF?

BLUF is a writing approach that places the most important information—the "bottom line"—at the beginning of content. For GEO, this means starting with a direct, concise answer before providing details.

### Why BLUF Matters for GEO

- AI extracts and cites direct, concise answers
- 50-70 word answers are optimal for AI Overviews
- Users (and AI) get immediate value
- Improves engagement and reduces bounce rate
- Featured snippet optimization

### BLUF Structure

**First Paragraph (50-70 words):**
- Direct answer to the main query
- Complete, self-contained information
- Conversational and accessible
- Think: "What would I want in an AI Overview?"

**Following Paragraphs:**
- Expand on the BLUF
- Provide context and details
- Include examples and evidence
- Link to related information

### BLUF Examples

**Topic: "What is SEO?"**

✅ **Good BLUF (61 words):**
```
SEO (Search Engine Optimization) is the practice of improving website
visibility in search engine results. It involves optimizing content,
technical elements, and building authority through links. Good SEO
increases organic traffic and helps potential customers find your
business online without paying for ads.
```

❌ **Poor - Too Short (22 words):**
```
SEO stands for Search Engine Optimization. It's a way to get more
visitors to your website from Google.
```

❌ **Poor - Too Long (95 words):**
```
Search Engine Optimization, commonly abbreviated as SEO, represents a
comprehensive digital marketing discipline that encompasses a wide variety
of strategies, techniques, and best practices aimed at improving a
website's visibility and ranking position within search engine results
pages, thereby increasing the quantity and quality of organic (non-paid)
traffic to the site by making it more accessible, relevant, and
authoritative in the eyes of search engine algorithms, which ultimately
helps businesses attract potential customers who are actively searching
for related products, services, or information.
```

**Topic: "How to optimize images for SEO"**

✅ **Good BLUF (68 words):**
```
Image optimization for SEO involves three key steps: compress file sizes
to improve page speed, add descriptive alt text for accessibility and
search engines, and use descriptive file names before uploading. Modern
formats like WebP reduce file size by 30% compared to JPEG. These changes
help images rank in image search and improve overall page performance.
```

### BLUF Testing

Use `scripts/check_bluf.py` to validate:
```bash
python3 scripts/check_bluf.py page.html
```

**Checks:**
- First paragraph word count (50-70 target)
- Whether it's a direct answer
- Sentence structure completeness
- Quality scoring

## Question-Based Headers

### Why Questions Work for GEO

- Long-tail queries of 8+ words are 7x more likely to trigger AI Overviews
- Users search in natural language questions
- AI favors content that directly answers queries
- Improves content scanability and structure

### Target Metrics

- **Goal:** 30%+ of H2/H3 headers should be questions
- **Ideal:** Questions should be 8+ words (long-tail)
- **Format:** Natural language, how users actually search

### Question Patterns

**Common Question Starters:**
- What is/are...?
- How do/does...?
- How to...?
- Why does/do...?
- When should...?
- Where can...?
- Which...?
- Who...?

### Header Conversion Examples

| Non-Question Header | Question-Based Header |
|---------------------|----------------------|
| Benefits of Local SEO | What are the benefits of local SEO? |
| Page Speed Optimization | How do I improve my page speed for SEO? |
| Keyword Research | How to do keyword research for SEO? |
| Mobile Optimization | Why is mobile optimization important for SEO? |
| Core Web Vitals | What are Core Web Vitals and why do they matter? |
| Backlink Building | How can I build quality backlinks to my website? |

### Long-Tail Question Examples (8+ words)

✅ **Optimal for GEO:**
- "How do I optimize my Drupal website for voice search results?" (11 words)
- "What are the best practices for implementing FAQ schema markup?" (10 words)
- "Why does page speed affect my search engine rankings in 2025?" (11 words)

⚠️ **Good but shorter:**
- "How to optimize images for SEO?" (6 words)
- "What is schema markup?" (4 words)

### Testing Headers

Use `scripts/analyze_headings.py` for automated analysis:
```bash
python3 scripts/analyze_headings.py page.html
```

**Provides:**
- Percentage of question-based headers
- Long-tail heading identification
- Conversion suggestions
- H2/H3 specific analysis

## FAQ Content & Schema

### FAQ Pages vs FAQ Schema — Know the Difference

These are two separate things that are often conflated:

- **FAQ pages** are a UX/content pattern — a dedicated page listing questions and answers. These often become dumping grounds for outdated, disorganized content and are generally a UX anti-pattern.
- **FAQ Schema** (FAQPage structured data) is technical markup that helps search engines and AI models parse Q&A content. This remains highly valuable for AI citations.

**Recommendation:** Embed Q&A content within topical pages rather than creating standalone FAQ pages. A program page with 5 well-maintained questions about admissions is far more useful than a catch-all FAQ page with 50 stale entries.

### Why FAQ Schema Still Matters for GEO

- Pages with FAQ Schema are 3.2x more likely to appear in AI Overviews
- 44% increase in AI citations compared to pages without FAQ Schema
- Provides direct answers AI can extract and attribute
- Natural question-answer format matches how users query AI tools

**Important context:** Google removed FAQ rich results for most sites in August 2023 ([announcement](https://developers.google.com/search/blog/2023/08/howto-faq-changes)). FAQ Schema no longer generates those expandable SERP features for most publishers. However, the Schema still signals content structure to AI models, which is where its value now lives.

### FAQ Quality Checklist for GEO

Before adding FAQ Schema to any content, ensure it meets this quality bar:

- [ ] **Genuine user questions** — based on real search queries, support tickets, or user research (not invented by the content team)
- [ ] **Substantive answers** — 50-300 words per answer; enough to be useful, not so long they lose focus
- [ ] **Active maintenance** — questions and answers reviewed at least quarterly; stale content removed
- [ ] **Topically coherent** — all Q&A on a page relates to that page's topic (no catch-all dumps)
- [ ] **Limited scope** — max 5-10 questions per page; if you need more, split across topical pages
- [ ] **Embedded in context** — Q&A appears on the relevant topical page, not on a standalone FAQ page

### FAQ Structure

**Question (H2 or H3):**
- Actual user question
- Natural language
- 8+ words ideal

**Answer (2-3 paragraphs):**
- Direct, complete response
- 50-300 words (longer than a snippet, shorter than an article)
- Include examples if relevant
- Link to detailed resources

### FAQ Example

```html
<!-- Embedded Q&A on a program page — NOT a standalone FAQ page -->
<h2>What is the difference between on-page and off-page SEO?</h2>

<p>On-page SEO refers to optimizations you make directly on your website,
including content quality, title tags, meta descriptions, header structure,
and internal linking. You have full control over these elements.</p>

<p>Off-page SEO involves factors outside your website, primarily backlinks
from other sites, social signals, and brand mentions. These signals tell
search engines that others find your content valuable and trustworthy.</p>
```

### FAQ Schema Implementation

**Add FAQ Schema to well-maintained Q&A content that passes the quality checklist above:**

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is the difference between on-page and off-page SEO?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "On-page SEO refers to optimizations you make directly on your website, including content quality, title tags, meta descriptions, header structure, and internal linking. Off-page SEO involves factors outside your website, primarily backlinks from other sites, social signals, and brand mentions."
    }
  }]
}
</script>
```

**Note:** FAQ rich results were removed for most sites in August 2023. The value of this Schema is now primarily for AI model comprehension and citation, not SERP features.

## Lists and Formatting

### Why Lists Work for GEO

- Highly favored by AI for extraction
- Easy to scan and understand
- Natural fit for step-by-step content
- Featured snippet optimization

### List Types

**Numbered Lists (Ordered):**
- Use for: Steps, processes, rankings, sequences
- Implies order matters
- Good for HowTo content

```html
<ol>
  <li>Research keywords</li>
  <li>Optimize content</li>
  <li>Build backlinks</li>
</ol>
```

**Bulleted Lists (Unordered):**
- Use for: Features, benefits, options, tips
- No specific order
- Good for FAQ answers

```html
<ul>
  <li>Improved search visibility</li>
  <li>Increased organic traffic</li>
  <li>Better user experience</li>
</ul>
```

### List Best Practices

- **Keep items concise:** 1-2 lines per item
- **Parallel structure:** Start each item similarly
- **Semantic HTML:** Use `<ol>` and `<ul>` tags, not `<div>` with bullets
- **Descriptive:** Each item should be self-explanatory

### Testing Lists

Use `scripts/analyze_lists.py` (Phase 3) to check:
- List count and types
- Item length and structure
- Proper HTML markup
- Optimization recommendations

## Featured Snippet Optimization

### Snippet-Ready Content

**Target length:** 40-50 words for paragraph snippets

**Structure:**
1. Direct answer immediately after header
2. Complete, self-contained
3. Clear and concise
4. Natural language

### Snippet Example

```html
<h2>What is a 301 redirect?</h2>

<p>A 301 redirect is a permanent redirect from one URL to another. When
a user or search engine tries to access the old URL, they're automatically
sent to the new location. 301 redirects preserve about 90-99% of SEO value
from the original page.</p>
```

**Why this works:**
- 46 words (optimal for snippets)
- Defines the term clearly
- Explains what happens
- Mentions SEO benefit
- Conversational tone

## Comparison Tables

### Why Tables Work for GEO

- 46-70% of AI citations are product/comparison content
- Structured data easy for AI to parse
- Clear side-by-side information
- High commercial intent

### Table Structure

```html
<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Option A</th>
      <th>Option B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Price</td>
      <td>$99/month</td>
      <td>$149/month</td>
    </tr>
    <tr>
      <td>Support</td>
      <td>Email only</td>
      <td>24/7 phone & email</td>
    </tr>
  </tbody>
</table>
```

### Table Best Practices

- Use semantic HTML (`<table>`, `<th>`, `<td>`)
- Include clear headers
- Keep cells concise
- Balance pros/cons objectively
- Mobile-responsive design

## Content Hierarchy

### Optimal Page Structure

```
H1: Main Topic (only one per page)
├── Introduction (BLUF format)
├── H2: First Subtopic (question format)
│   ├── Paragraph (40-70 words)
│   ├── List or table
│   └── Paragraph
├── H2: Second Subtopic (question format)
│   ├── Paragraph
│   └── H3: Sub-section (question format)
│       └── Paragraph
├── H2: FAQ Section
│   ├── H3: Question 1?
│   ├── Answer paragraph(s)
│   ├── H3: Question 2?
│   └── Answer paragraph(s)
└── Conclusion (summary + CTA)
```

### Hierarchy Best Practices

- **One H1 per page** (main topic)
- **No skipped levels** (don't jump from H2 to H4)
- **Logical nesting** (H3s under H2s they relate to)
- **Descriptive headers** (not "Introduction" or "Overview")
- **Question-based** when appropriate

## Quick Implementation Checklist

**BLUF Format:**
- [ ] First paragraph 50-70 words
- [ ] Direct answer to main query
- [ ] Complete and self-contained
- [ ] Tested with check_bluf.py

**Headers:**
- [ ] 30%+ of H2/H3 are questions
- [ ] Natural language questions
- [ ] Long-tail (8+ words) where possible
- [ ] Tested with analyze_headings.py

**FAQ Content (embed in topical pages, not standalone FAQ pages):**
- [ ] Genuine user questions (from search data or support tickets)
- [ ] Substantive answers (50-300 words each)
- [ ] Max 5-10 questions per page, topically coherent
- [ ] FAQ Schema applied to quality Q&A content
- [ ] Validated with extract_meta.py
- [ ] Maintenance schedule established (quarterly review minimum)

**Lists and Formatting:**
- [ ] Semantic HTML lists
- [ ] Concise list items
- [ ] Tables for comparisons
- [ ] Featured snippet optimization

**Hierarchy:**
- [ ] Single H1 tag
- [ ] Logical nesting
- [ ] No skipped levels
- [ ] Descriptive headers

## Tools

**Included in This Skill:**
- `check_bluf.py` - Validates BLUF format
- `analyze_headings.py` - Question-based header analysis
- `extract_meta.py` - Schema validation
- `check_readability.py` - Ensure 8th-grade level

**External Resources:**
- Google's Rich Results Test - Validate FAQ Schema
- Schema.org - Schema reference
- Answer the Public - Find question variations

## References

- Content structure impacts both UX and GEO performance
- AI favors well-structured, scannable content
- Question-answer format aligns with natural language queries
- Lists and tables improve AI extraction rates
