# Comprehensive SEO Audit Checklist

This checklist provides a systematic approach to evaluating website SEO performance. Use it to ensure thorough coverage during audits.

## Technical SEO

### Crawlability
- [ ] robots.txt exists and is properly configured
- [ ] No critical pages blocked by robots.txt
- [ ] XML sitemap exists and is accessible
- [ ] Sitemap submitted to Google Search Console
- [ ] Sitemap includes all important pages
- [ ] No broken links (404 errors)
- [ ] No redirect chains (multiple 301s)
- [ ] Server returns proper HTTP status codes
- [ ] No orphan pages (pages with no internal links)

### Indexability
- [ ] Canonical tags properly implemented
- [ ] No duplicate content issues
- [ ] Meta robots tags used appropriately
- [ ] No accidental noindex tags on important pages
- [ ] Parameter handling configured (for dynamic URLs)
- [ ] Pagination properly implemented (rel=next/prev or View All)
- [ ] International targeting configured (hreflang tags)

### Site Architecture
- [ ] Logical URL structure
- [ ] URLs are readable and keyword-rich
- [ ] Maximum 3-4 clicks to reach any page
- [ ] Internal linking strategy in place
- [ ] Breadcrumb navigation implemented
- [ ] HTML sitemap available
- [ ] Proper use of subdomains vs. subdirectories

### Security & Protocol
- [ ] HTTPS/SSL certificate installed
- [ ] All pages served over HTTPS
- [ ] No mixed content warnings
- [ ] HSTS header implemented
- [ ] Security headers configured (CSP, X-Frame-Options)

### Mobile Optimization
- [ ] Mobile-responsive design
- [ ] Viewport meta tag configured
- [ ] Mobile-friendly test passes
- [ ] No mobile-specific blocking (popups, interstitials)
- [ ] Touch elements properly sized (48x48px minimum)
- [ ] Mobile page speed optimized

### Performance
- [ ] Page load time < 3 seconds
- [ ] LCP (Largest Contentful Paint) < 2.5s
- [ ] FID (First Input Delay) < 100ms
- [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] Images optimized (compressed, proper formats)
- [ ] Lazy loading implemented for images
- [ ] Critical CSS inlined
- [ ] JavaScript deferred or async loaded
- [ ] Browser caching configured
- [ ] CDN implemented for static assets
- [ ] Minified CSS and JavaScript
- [ ] GZIP/Brotli compression enabled

## On-Page SEO

### Title Tags
- [ ] Unique title for every page
- [ ] Primary keyword in title
- [ ] Title length 50-60 characters
- [ ] Brand name included (usually at end)
- [ ] Compelling and click-worthy
- [ ] Matches search intent

### Meta Descriptions
- [ ] Unique description for every page
- [ ] Primary keyword in description
- [ ] Length 150-160 characters
- [ ] Compelling call-to-action
- [ ] Matches search intent
- [ ] Accurate summary of page content

### Header Tags
- [ ] One H1 tag per page
- [ ] H1 contains primary keyword
- [ ] Logical heading hierarchy (H1 → H2 → H3)
- [ ] No skipped heading levels
- [ ] Headings describe content structure
- [ ] Keywords naturally included in subheadings

### Content Quality
- [ ] Content matches search intent
- [ ] Comprehensive coverage of topic
- [ ] Original, not duplicated
- [ ] Proper grammar and spelling
- [ ] Readable (Flesch Reading Ease > 60)
- [ ] E-E-A-T signals present (expertise, authority, trust)
- [ ] Regular content updates
- [ ] Adequate content length (1000+ words for competitive topics)
- [ ] Multimedia content included (images, videos)

### Images
- [ ] Descriptive, keyword-rich file names
- [ ] Alt text on all images
- [ ] Appropriate file formats (WebP, JPEG, PNG)
- [ ] Compressed file sizes
- [ ] Responsive images (srcset)
- [ ] Lazy loading implemented
- [ ] Image sitemaps for important images

### Internal Links
- [ ] Strategic internal linking structure
- [ ] Descriptive anchor text
- [ ] No broken internal links
- [ ] Link to important pages from homepage
- [ ] Related content linked
- [ ] Reasonable number of internal links per page

### URL Structure
- [ ] Short, descriptive URLs
- [ ] Keywords in URL
- [ ] Hyphens separate words (not underscores)
- [ ] Lowercase letters only
- [ ] No unnecessary parameters
- [ ] Consistent structure across site

## Schema Markup (Structured Data)

- [ ] Organization schema on homepage
- [ ] Website/SearchAction schema implemented
- [ ] Article/BlogPosting schema on blog posts
- [ ] Product schema on product pages
- [ ] Review/AggregateRating schema where applicable
- [ ] FAQ schema for FAQ sections
- [ ] Breadcrumb schema implemented
- [ ] Local Business schema (if applicable)
- [ ] Event schema (if applicable)
- [ ] Recipe schema (if applicable)
- [ ] Video schema for video content
- [ ] Schema validates in Google's Rich Results Test

## Local SEO (if applicable)

- [ ] Google Business Profile claimed and optimized
- [ ] NAP (Name, Address, Phone) consistent across web
- [ ] Local business schema markup
- [ ] Location pages for multiple locations
- [ ] Customer reviews encouraged and responded to
- [ ] Local citations built (Yelp, industry directories)
- [ ] Embedded Google Map on contact page

## Social Media Integration

- [ ] Open Graph tags implemented
- [ ] Twitter Card tags implemented
- [ ] Appropriate og:image for social sharing
- [ ] og:title and og:description optimized
- [ ] Social media profiles linked from website

## Analytics & Tracking

- [ ] Google Analytics installed
- [ ] Google Search Console configured
- [ ] Search Console verified
- [ ] Analytics tracking conversions/goals
- [ ] Event tracking configured
- [ ] No duplicate tracking codes
- [ ] Privacy policy compliant with GDPR

## Content Strategy

- [ ] Target keyword research completed
- [ ] Keyword map created (keywords → pages)
- [ ] Content calendar in place
- [ ] Regular content publishing schedule
- [ ] Content addresses user questions
- [ ] Topic clusters and pillar pages strategy
- [ ] Competitor content analysis completed

## Off-Page SEO Considerations

- [ ] Backlink profile healthy (quality over quantity)
- [ ] No spammy or toxic backlinks
- [ ] Disavow file submitted if needed
- [ ] Brand mentions monitoring
- [ ] Guest posting opportunities identified
- [ ] Industry directory submissions
- [ ] Social signals present

## E-commerce Specific (if applicable)

- [ ] Product descriptions unique and detailed
- [ ] Product schema markup
- [ ] Review schema for product ratings
- [ ] Faceted navigation handled properly
- [ ] Out-of-stock pages handled correctly
- [ ] Category pages optimized
- [ ] Checkout process simple and fast

## Accessibility

- [ ] WCAG 2.1 Level AA compliance
- [ ] Proper heading structure for screen readers
- [ ] Alt text on images
- [ ] ARIA labels where appropriate
- [ ] Keyboard navigation functional
- [ ] Sufficient color contrast
- [ ] Form labels properly associated

## Priority Assessment

When conducting audits, categorize issues by priority:

**Critical (Fix Immediately)**
- Indexability blocks (noindex, robots.txt blocking)
- Major technical errors (500s, extensive 404s)
- Security issues (no HTTPS, mixed content)
- Mobile usability failures
- Core Web Vitals failures

**Important (Fix Soon)**
- Missing or poor meta tags
- Broken internal links
- Duplicate content
- Slow page speed
- Missing schema markup
- Poor heading hierarchy

**Enhancement (Optimize When Possible)**
- Image optimization opportunities
- Internal linking improvements
- Content depth expansion
- Social media tags
- Additional schema types
- Advanced technical optimizations
