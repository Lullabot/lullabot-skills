---
name: seo-expert
description: "This skill should be used when users need SEO audits, website optimization recommendations, technical SEO analysis, or competitive research. Use when users request to analyze a website's search engine performance, identify SEO issues, or get prioritized action items to improve rankings. Ideal for tasks like 'audit this website for SEO' or 'what are the top issues affecting this site's SEO performance.'"
---

# SEO Expert (with GEO Optimization)

## Overview

This skill enables comprehensive SEO and GEO (Generative Engine Optimization) auditing for websites. It analyzes traditional SEO factors plus AI-readiness: content structure for AI citations, schema markup for AI extraction, readability for conversational queries, and question-based formatting.

**Key Insight:** 52% of searches now trigger AI Overviews. 92.36% of AI citations come from Google's top 10 organic results. Strong SEO is prerequisite for GEO success.

## Quick Start

Trigger this skill when users request:
- "Audit [website] for SEO issues"
- "Optimize [site] for AI search and citations"
- "Check if [website] is ready for Google AI Overviews"
- "Analyze [page] for GEO optimization"
- "Help me improve [content] for ChatGPT/Perplexity citations"

The skill provides detailed audit reports with 5-15 prioritized recommendations covering both traditional SEO and GEO optimization.

## Website Auditing Workflow

To conduct a comprehensive SEO + GEO audit:

1. **Gather baseline data** using scripts:
   - Run `scripts/lighthouse_audit.sh [url]` to get performance/SEO metrics
   - Run `scripts/check_robots.sh [url]` to analyze robots.txt
   - Run `scripts/check_sitemap.sh [url]` to validate XML sitemap

2. **Analyze page structure and meta data**:
   - Use WebFetch to retrieve the target page HTML
   - Run `scripts/extract_meta.py [html_file]` to extract meta tags AND validate GEO-critical schema (FAQ, HowTo, Article)
   - Run `scripts/analyze_headings.py [html_file]` to check heading hierarchy AND question-based headers for GEO

3. **Analyze GEO content optimization**:
   - Run `scripts/check_readability.py [html_file]` to ensure 8th-grade reading level
   - Run `scripts/check_bluf.py [html_file]` to validate Bottom Line Up Front format
   - Run `scripts/analyze_eeat.py [html_file]` to score E-E-A-T signals (authors, citations, dates, trust)
   - Review first paragraphs for 50-70 word direct answers

4. **Evaluate against best practices**:
   - Consult `references/seo_checklist.md` for comprehensive SEO audit criteria
   - Review `references/geo_best_practices.md` for AI optimization strategies
   - Check `references/content_structure_guide.md` for BLUF, FAQ, and question-based formatting
   - Review `references/technical_seo.md` for technical requirements
   - Check `references/core_web_vitals.md` for performance thresholds

5. **Generate prioritized recommendations**:
   - Use `assets/audit_report_template.md` as the report structure
   - Apply `assets/priority_matrix.md` to rank issues by impact/effort
   - Include both traditional SEO and GEO recommendations
   - Focus on 5-15 actionable items with clear implementation steps

## GEO (Generative Engine Optimization) Analysis

### Content Structure (CRITICAL)
- **BLUF Format**: Run `scripts/check_bluf.py [html_file]` to validate 50-70 word direct answers at the top
- **Readability**: Run `scripts/check_readability.py [html_file]` to ensure 8th-grade reading level (Flesch-Kincaid)
- **Question Headers**: Enhanced `scripts/analyze_headings.py [html_file]` detects question-based H2/H3 headers (target: 30%+)
- **Long-tail**: Identify 8+ word headers (7x more likely to trigger AI Overviews)

### E-E-A-T Signals (CRITICAL)
- **E-E-A-T Analysis**: Run `scripts/analyze_eeat.py [html_file]` for comprehensive trust signal detection
- Detects author bylines with credentials (PhD, MD, CPA, etc.)
- Counts external authoritative links (.gov, .edu, established orgs)
- Verifies publish/modified dates in meta, schema, and visible content
- Finds blockquotes and expert attributions
- Checks trust signals (ISO, HIPAA, privacy policy, author bios)
- Scores each E-E-A-T dimension out of 25 for a 0-100 total

### Schema Markup (CRITICAL)
- **FAQ Schema**: Validates FAQ Schema (highest priority for GEO)
- **HowTo Schema**: Check for process/tutorial content structured data
- **Article Schema**: Verify author information and dates (E-E-A-T signals)

### Key GEO Principles
1. **Strong SEO First**: 92.36% of AI citations come from top 10 organic results
2. **Natural Language**: AI mentions exact keywords only 5.4% of the time
3. **Conversational Tone**: Target 8th-grade readability for AI-friendly content
4. **Direct Answers**: 50-70 word BLUF format optimal for AI citations
5. **Structured Data**: FAQ Schema drives 3.2x higher AI citation rates

## Technical SEO Analysis

For technical SEO issues, evaluate:

- **Crawlability**: robots.txt, XML sitemaps, internal linking
- **Indexability**: canonical tags, noindex directives, duplicate content
- **Site Architecture**: URL structure, navigation, breadcrumbs
- **Security**: HTTPS/SSL, mixed content warnings
- **Mobile**: Responsive design, mobile-first indexing
- **Performance**: Page speed, Core Web Vitals, lazy loading

## On-Page Optimization

Evaluate:

- **Title Tags**: Uniqueness, keyword placement, length (50-60 chars)
- **Meta Descriptions**: Compelling copy, keywords, length (150-160 chars)
- **Header Tags**: Proper H1-H6 hierarchy, keyword usage
- **Content Quality**: Readability, depth, E-E-A-T signals
- **Images**: Alt text, file size optimization, modern formats (WebP)
- **Internal Links**: Relevant anchor text, strategic link placement
- **Schema Markup**: Appropriate structured data types

## Performance Analysis

Core Web Vitals are critical ranking factors:

- **LCP (Largest Contentful Paint)**: Target < 2.5s
- **FID (First Input Delay)**: Target < 100ms
- **CLS (Cumulative Layout Shift)**: Target < 0.1

## Report Generation

Structure audit reports with:

1. **Executive Summary**: 2-3 sentence overview of site health
2. **Critical Issues**: High-impact problems requiring immediate attention
3. **Priority Recommendations**: 5-15 actionable items with issue description, current vs. desired state, implementation steps, and priority rating
4. **Performance Metrics**: Lighthouse scores and Core Web Vitals
5. **Next Steps**: Sequenced action plan

## Resources

### scripts/

**Full-Site Crawling:**
- `crawl_site.sh` - LibreCrawl wrapper with tier configs (tier1/2/3)
- `generate_crawl_report.py` - Transform crawl JSON to client reports
- `compare_crawls.py` - Month-over-month comparison analysis

**Traditional SEO:**
- `lighthouse_audit.sh` - Google Lighthouse performance/SEO metrics
- `check_robots.sh` - Analyze robots.txt configuration
- `check_sitemap.sh` - Validate XML sitemap structure

**GEO Optimization:**
- `check_readability.py` - Flesch-Kincaid readability (target: 8th grade)
- `check_bluf.py` - BLUF (Bottom Line Up Front) validation
- `analyze_headings.py` - Question-based header detection (target: 30%+)
- `extract_meta.py` - GEO schema validation (FAQ, HowTo, Article)
- `analyze_eeat.py` - E-E-A-T signal detection (0-100 score)

### references/

- `seo_checklist.md` - Comprehensive audit checklist
- `core_web_vitals.md` - Performance thresholds and optimization
- `technical_seo.md` - Technical requirements and best practices
- `meta_tags_guide.md` - Essential meta tags and implementation
- `schema_markup_guide.md` - Common schema.org types with examples
- `geo_best_practices.md` - 15 essential GEO practices
- `content_structure_guide.md` - BLUF format, question headers, FAQ sections
- `readability_standards.md` - Flesch-Kincaid targets and writing techniques

### assets/
- `audit_report_template.md` - Structured template for audit reports
- `priority_matrix.md` - Framework for prioritizing issues by impact/effort
