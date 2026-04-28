# Technical SEO Reference Guide

This guide covers technical SEO requirements and best practices for ensuring search engines can properly crawl, index, and rank your website.

## Crawlability

### robots.txt

**Purpose:** Control which parts of your site search engines can access.

**Location:** Must be at root domain: `https://example.com/robots.txt`

**Basic Syntax:**
```
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /

Sitemap: https://example.com/sitemap.xml
```

**Best Practices:**
- Always include sitemap reference
- Test in Google Search Console
- Don't block CSS/JavaScript (needed for rendering)
- Use Allow to override Disallow for subdirectories
- Be cautious with wildcard blocking

**Common Patterns:**
```
# Block specific bot
User-agent: BadBot
Disallow: /

# Block file types
User-agent: *
Disallow: /*.pdf$
Disallow: /*.doc$

# Crawl delay (non-Google)
User-agent: *
Crawl-delay: 10
```

**Critical Errors:**
- Blocking important pages
- Blocking CSS/JS (prevents proper rendering)
- Syntax errors causing misinterpretation
- No sitemap reference

---

### XML Sitemaps

**Purpose:** Help search engines discover and prioritize content.

**Location:** Referenced in robots.txt, submitted to Search Console.

**Basic Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**Limitations:**
- Maximum 50,000 URLs per sitemap
- Maximum 50MB uncompressed
- Use sitemap index for larger sites

**Sitemap Index:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-products.xml</loc>
    <lastmod>2024-01-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-blog.xml</loc>
    <lastmod>2024-01-15</lastmod>
  </sitemap>
</sitemapindex>
```

**Best Practices:**
- Include only canonical URLs
- Update lastmod when content changes
- Use priority thoughtfully (not all pages at 1.0)
- Submit to Google Search Console and Bing Webmaster Tools
- Create separate sitemaps by content type
- Include images, videos in specialized sitemaps
- Keep sitemaps updated (regenerate regularly)

**Optional Elements:**
- `<changefreq>`: Hint for crawl frequency (often ignored)
- `<priority>`: Relative importance (0.0 to 1.0)
- `<lastmod>`: Last modification date (recommended)

---

### Internal Linking

**Purpose:** Help search engines discover pages and distribute link equity.

**Best Practices:**
- Every page accessible within 3-4 clicks from homepage
- Use descriptive anchor text
- Link to important pages from high-authority pages
- Implement breadcrumb navigation
- Create topic clusters (pillar pages + supporting content)
- Avoid excessive links (100-150 per page maximum)
- Fix broken internal links

**Link Equity Distribution:**
- Homepage typically has highest authority
- Strategic internal linking passes authority
- Deep pages need multiple quality internal links
- Use dofollow for internal links (default)

**Orphan Pages:**
- Pages with no internal links pointing to them
- Won't be discovered by crawlers
- Must be in sitemap or have direct external links

---

## Indexability

### Canonical Tags

**Purpose:** Specify the preferred version of duplicate or similar pages.

**Implementation:**
```html
<link rel="canonical" href="https://example.com/preferred-url">
```

**Use Cases:**
- Paginated content
- Product variations (size, color)
- HTTP vs HTTPS
- www vs non-www
- URL parameters (tracking, sorting)
- Print versions
- Mobile vs desktop versions

**Best Practices:**
- Self-referencing canonical on all pages
- Point to the most complete version
- Use absolute URLs, not relative
- Ensure canonical URL is accessible (not 404)
- Avoid canonical chains (A→B→C)
- One canonical per page

**Common Mistakes:**
- Canonical pointing to 404 or redirect
- Multiple canonical tags
- Canonical on paginated pages pointing to page 1
- Conflicting signals (canonical + noindex)

---

### Meta Robots Tags

**Purpose:** Control how search engines index and follow links on specific pages.

**Implementation:**
```html
<meta name="robots" content="noindex, nofollow">
```

**Directives:**
- `index` / `noindex`: Allow/prevent indexing
- `follow` / `nofollow`: Allow/prevent following links
- `noarchive`: Prevent cached copy
- `nosnippet`: Prevent snippet in search results
- `max-snippet:[number]`: Limit snippet length
- `max-image-preview:[setting]`: Control image preview size
- `max-video-preview:[number]`: Limit video preview length

**Common Uses:**
```html
<!-- Prevent indexing but allow crawling links -->
<meta name="robots" content="noindex, follow">

<!-- Block specific bot -->
<meta name="googlebot" content="noindex">

<!-- Prevent all (same as above for most bots) -->
<meta name="robots" content="none">

<!-- Allow but limit snippet -->
<meta name="robots" content="max-snippet:100">
```

**X-Robots-Tag HTTP Header:**
For non-HTML resources (PDFs, images):
```
X-Robots-Tag: noindex, nofollow
```

**Best Practices:**
- Don't mix conflicting directives
- Test with Google Search Console
- Use noindex for: thin content, duplicate pages, private pages
- Avoid accidentally noindexing important pages
- Remove noindex when ready to launch

---

### Duplicate Content

**Problem:** Same/similar content on multiple URLs confuses search engines.

**Solutions:**

1. **Canonical Tags** (preferred method)
   ```html
   <link rel="canonical" href="https://example.com/original">
   ```

2. **301 Redirects**
   - Permanently redirect duplicates to canonical version
   - Passes link equity
   - Best for: URL migration, removing parameters

3. **Parameter Handling** (Google Search Console)
   - Tell Google how to handle URL parameters
   - Useful for: faceted navigation, tracking codes

4. **Noindex**
   - Last resort for thin/low-value variations
   - Doesn't pass link equity

**Common Duplicate Content Issues:**
- www vs non-www
- HTTP vs HTTPS
- Trailing slash variations
- URL parameters (tracking, session IDs)
- Printer-friendly versions
- Paginated series
- Product variations
- Scraped/syndicated content

---

## Site Architecture

### URL Structure

**Best Practices:**
- Short and descriptive
- Include target keywords
- Use hyphens (not underscores)
- Lowercase only
- Logical hierarchy
- Avoid deep nesting (max 4-5 levels)

**Good Examples:**
```
https://example.com/products/category/product-name
https://example.com/blog/seo-tips-2024
https://example.com/about/team
```

**Bad Examples:**
```
https://example.com/index.php?id=123&cat=45
https://example.com/this_is_a_very_long_url_with_underscores
https://example.com/level1/level2/level3/level4/level5/page
```

**URL Parameters:**
- Avoid when possible
- Use for: filtering, sorting, pagination
- Configure in Search Console
- Consider canonical tags

---

### Breadcrumbs

**Purpose:** Navigation aid + structured data for search engines.

**HTML Structure:**
```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/category">Category</a></li>
    <li aria-current="page">Product</li>
  </ol>
</nav>
```

**Schema Markup:**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "Home",
    "item": "https://example.com"
  },{
    "@type": "ListItem",
    "position": 2,
    "name": "Category",
    "item": "https://example.com/category"
  },{
    "@type": "ListItem",
    "position": 3,
    "name": "Product"
  }]
}
```

**Benefits:**
- Better UX
- Rich results in search
- Helps search engines understand site structure

---

## Security & Protocol

### HTTPS/SSL

**Why it matters:**
- Confirmed ranking signal
- Required for HTTP/2
- User trust and security
- Chrome marks HTTP as "Not Secure"

**Implementation Checklist:**
- [ ] Install valid SSL certificate
- [ ] Redirect all HTTP to HTTPS (301)
- [ ] Update internal links to HTTPS
- [ ] Update canonical tags to HTTPS
- [ ] Update sitemap to HTTPS
- [ ] Update Search Console property
- [ ] Fix mixed content warnings
- [ ] Update CDN/external resources to HTTPS

**Mixed Content:**
```html
<!-- Bad: HTTP resource on HTTPS page -->
<img src="http://example.com/image.jpg">

<!-- Good: HTTPS or protocol-relative -->
<img src="https://example.com/image.jpg">
<img src="//example.com/image.jpg">
```

---

### HSTS (HTTP Strict Transport Security)

**Purpose:** Force HTTPS connections, prevent downgrade attacks.

**Implementation:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**Parameters:**
- `max-age`: Seconds to remember (1 year = 31536000)
- `includeSubDomains`: Apply to all subdomains
- `preload`: Eligible for browser preload lists

---

## Mobile Optimization

### Mobile-First Indexing

**What it means:** Google primarily uses mobile version for indexing and ranking.

**Requirements:**
- Mobile and desktop content should be equivalent
- Structured data on both versions
- Images accessible and properly sized
- Meta tags identical

### Viewport Configuration

**Required Meta Tag:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Common Configurations:**
```html
<!-- Basic responsive -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Prevent zoom (not recommended) -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

<!-- Fixed width (not recommended for mobile) -->
<meta name="viewport" content="width=1024">
```

### Responsive Design

**Best Practices:**
- Fluid layouts (%, em, rem instead of px)
- Flexible images (max-width: 100%)
- CSS media queries for breakpoints
- Touch-friendly tap targets (48x48px minimum)
- Readable text without zooming (16px base)
- No horizontal scrolling
- Fast mobile page speed

**Testing:**
- Google Mobile-Friendly Test
- Chrome DevTools Device Mode
- Real device testing
- PageSpeed Insights mobile score

---

### Mobile-Specific Issues

**Problems to Avoid:**
- Flash content
- Unplayable videos
- Faulty redirects (mobile to wrong page)
- Intrusive interstitials
- Small font sizes
- Touch elements too close together
- Content wider than screen

---

## Rendering & JavaScript

### Client-Side Rendering (CSR) Challenges

**Issue:** Content generated by JavaScript may not be indexed.

**Google's Approach:**
1. Crawls HTML
2. Queues page for rendering
3. Renders JavaScript (when resources available)
4. Indexes rendered content

**Problems:**
- Rendering delay
- Resource-intensive
- May miss dynamically loaded content
- Infinite scroll issues

### Server-Side Rendering (SSR)

**Benefits:**
- Content immediately available to crawlers
- Faster initial page load
- Better for SEO

**Implementation:**
- Next.js (React)
- Nuxt.js (Vue)
- Angular Universal
- Custom Node.js solutions

### Static Site Generation (SSG)

**Benefits:**
- Pre-rendered HTML
- Excellent performance
- Perfect for SEO
- Reduced server load

**Tools:**
- Next.js (Static Export)
- Gatsby
- Hugo
- Jekyll

### Dynamic Rendering

**Approach:** Serve pre-rendered HTML to bots, CSR to users.

**Tools:**
- Rendertron
- Prerender.io
- Puppeteer/Playwright

**Considerations:**
- Cloaking concerns (must be equivalent content)
- Maintenance overhead
- Caching strategies

---

## Status Codes & Redirects

### HTTP Status Codes

**2xx Success**
- `200 OK`: Standard successful response

**3xx Redirection**
- `301 Moved Permanently`: Permanent redirect (passes link equity)
- `302 Found`: Temporary redirect (doesn't pass full link equity)
- `307 Temporary Redirect`: Preserves request method
- `308 Permanent Redirect`: Like 301 but preserves method

**4xx Client Errors**
- `404 Not Found`: Page doesn't exist
- `410 Gone`: Permanently removed
- `403 Forbidden`: Access denied

**5xx Server Errors**
- `500 Internal Server Error`: Generic server error
- `503 Service Unavailable`: Temporary server issue

### Redirect Best Practices

**When to use 301:**
- Permanent URL changes
- Site migration
- HTTPS migration
- Domain changes
- URL structure changes

**When to use 302:**
- A/B testing
- Temporary maintenance
- Geographic redirects
- Time-based redirects

**Avoid:**
- Redirect chains (A→B→C→D)
- Redirect loops
- 302 for permanent changes
- Broken redirect targets (404)

**Testing:**
- Check HTTP headers
- Verify redirect status code
- Test full redirect chain
- Ensure target URL is accessible

---

## International & Multi-Regional SEO

### Hreflang Tags

**Purpose:** Indicate language and regional targeting.

**Implementation:**
```html
<!-- English for US -->
<link rel="alternate" hreflang="en-us" href="https://example.com/en-us/" />

<!-- English for UK -->
<link rel="alternate" hreflang="en-gb" href="https://example.com/en-gb/" />

<!-- Spanish for Spain -->
<link rel="alternate" hreflang="es-es" href="https://example.com/es-es/" />

<!-- Default fallback -->
<link rel="alternate" hreflang="x-default" href="https://example.com/" />
```

**Sitemap Implementation:**
```xml
<url>
  <loc>https://example.com/en-us/</loc>
  <xhtml:link rel="alternate" hreflang="en-gb" href="https://example.com/en-gb/" />
  <xhtml:link rel="alternate" hreflang="es-es" href="https://example.com/es-es/" />
  <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/" />
</url>
```

**Language Codes:**
- ISO 639-1 for language (en, es, fr)
- ISO 3166-1 Alpha 2 for region (US, GB, ES)

**Best Practices:**
- Include self-referencing hreflang
- Include x-default for fallback
- Ensure bidirectional links
- Use absolute URLs
- One implementation method (HTML or sitemap, not both)

---

## Performance Optimization

See `core_web_vitals.md` for detailed performance optimization strategies.

**Quick Technical Checklist:**
- [ ] Enable GZIP/Brotli compression
- [ ] Implement browser caching
- [ ] Minify HTML, CSS, JavaScript
- [ ] Optimize images
- [ ] Use CDN
- [ ] Enable HTTP/2
- [ ] Defer non-critical JavaScript
- [ ] Inline critical CSS
- [ ] Lazy load images
- [ ] Preload critical resources

---

## Tools for Technical SEO

### Auditing Tools
- Screaming Frog SEO Spider
- Sitebulb
- SEMrush Site Audit
- Ahrefs Site Audit
- DeepCrawl

### Google Tools
- Google Search Console
- PageSpeed Insights
- Mobile-Friendly Test
- Rich Results Test
- Structured Data Testing Tool

### Testing Tools
- Chrome DevTools
- Lighthouse
- WebPageTest
- GTmetrix

### Monitoring
- Google Search Console Performance
- Log file analysis
- Real User Monitoring (RUM)
- Uptime monitoring
