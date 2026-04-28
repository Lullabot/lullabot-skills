# Core Web Vitals Guide

Core Web Vitals are a set of specific metrics that Google considers important in a webpage's overall user experience. They are critical ranking factors and should be prioritized in any SEO optimization effort.

## The Three Core Web Vitals

### 1. Largest Contentful Paint (LCP)

**What it measures:** Loading performance - the time it takes for the largest content element to become visible.

**Target Threshold:**
- Good: ≤ 2.5 seconds
- Needs Improvement: 2.5 - 4.0 seconds
- Poor: > 4.0 seconds

**What counts as LCP:**
- `<img>` elements
- `<image>` elements inside `<svg>`
- `<video>` elements (poster image)
- Element with background image loaded via CSS
- Block-level text elements (paragraphs, headings)

**Common Causes of Poor LCP:**
- Slow server response times
- Render-blocking JavaScript and CSS
- Slow resource load times (images, fonts)
- Client-side rendering delays

**Optimization Strategies:**

1. **Optimize Server Response Time**
   - Use a CDN
   - Cache assets
   - Serve HTML statically when possible
   - Use HTTP/2 or HTTP/3
   - Establish early connections (dns-prefetch, preconnect)

2. **Eliminate Render-Blocking Resources**
   - Minify CSS and JavaScript
   - Defer non-critical CSS
   - Inline critical CSS
   - Defer or async load non-critical JavaScript
   - Remove unused CSS/JavaScript

3. **Optimize Images**
   - Compress images (TinyPNG, ImageOptim)
   - Use modern formats (WebP, AVIF)
   - Implement responsive images (srcset)
   - Set explicit width/height to prevent layout shifts
   - Preload critical images: `<link rel="preload" as="image">`

4. **Optimize Fonts**
   - Use font-display: swap or optional
   - Preload key fonts
   - Use variable fonts to reduce file count
   - Subset fonts to include only needed characters

5. **Reduce Client-Side Rendering**
   - Use server-side rendering (SSR)
   - Pre-render static content
   - Use static site generation where possible

---

### 2. First Input Delay (FID)

**What it measures:** Interactivity - the time from when a user first interacts with your page to when the browser responds.

**Note:** FID is being replaced by Interaction to Next Paint (INP) in March 2024.

**Target Threshold:**
- Good: ≤ 100 milliseconds
- Needs Improvement: 100 - 300 milliseconds
- Poor: > 300 milliseconds

**Common Causes of Poor FID:**
- Long-running JavaScript tasks
- Large JavaScript bundles
- Heavy JavaScript execution
- Long main thread blocking time

**Optimization Strategies:**

1. **Break Up Long Tasks**
   - Split large JavaScript bundles
   - Use code splitting
   - Implement lazy loading for non-critical scripts
   - Use web workers for heavy computations

2. **Reduce JavaScript Execution Time**
   - Minimize and compress JavaScript
   - Remove unused JavaScript
   - Use tree shaking to eliminate dead code
   - Defer third-party scripts

3. **Minimize Main Thread Work**
   - Reduce complexity of event handlers
   - Debounce/throttle input handlers
   - Use passive event listeners
   - Avoid large, complex layouts

4. **Keep Request Counts Low and Transfer Sizes Small**
   - Use HTTP/2 multiplexing
   - Implement resource hints (preload, prefetch)
   - Minimize third-party code
   - Use a CDN

---

### 3. Cumulative Layout Shift (CLS)

**What it measures:** Visual stability - unexpected layout shifts during page load.

**Target Threshold:**
- Good: ≤ 0.1
- Needs Improvement: 0.1 - 0.25
- Poor: > 0.25

**Common Causes of Poor CLS:**
- Images without dimensions
- Ads, embeds, and iframes without dimensions
- Dynamically injected content
- Web fonts causing FOIT/FOUT (Flash of Invisible/Unstyled Text)
- Actions waiting for network response before updating DOM

**Optimization Strategies:**

1. **Always Include Size Attributes on Images and Videos**
   ```html
   <img src="image.jpg" width="640" height="360" alt="...">
   ```
   - Use CSS aspect-ratio for responsive images
   - Reserve space with aspect ratio boxes

2. **Never Insert Content Above Existing Content**
   - Reserve space for dynamic content
   - Use skeleton screens or placeholders
   - Load ads in reserved spaces
   - Use transform animations instead of layout properties

3. **Prefer Transform Animations**
   - Use `transform` and `opacity` (won't cause layout shifts)
   - Avoid animating: width, height, top, left, margin, padding

4. **Optimize Font Loading**
   ```css
   @font-face {
     font-family: 'MyFont';
     font-display: optional; /* or swap */
     src: url('font.woff2') format('woff2');
   }
   ```
   - Use font-display: optional or swap
   - Preload key fonts
   - Consider system fonts

5. **Handle Ads and Embeds Properly**
   - Reserve space for ad slots
   - Style ad container to prevent collapse
   - Avoid placing ads near top of viewport
   - Use placeholder dimensions for embeds

---

## Interaction to Next Paint (INP)

**New metric replacing FID (March 2024)**

**What it measures:** Overall responsiveness - the time from user interaction to visual update.

**Target Threshold:**
- Good: ≤ 200 milliseconds
- Needs Improvement: 200 - 500 milliseconds
- Poor: > 500 milliseconds

**Differences from FID:**
- Considers all interactions (not just first)
- Measures to visual update (not just input delay)
- More comprehensive responsiveness metric

**Optimization strategies are similar to FID** with additional focus on:
- Optimizing event handler code
- Reducing rendering work
- Minimizing layout/style calculations

---

## Measuring Core Web Vitals

### Tools for Measurement

1. **Lab Data (Synthetic Testing)**
   - Google Lighthouse (in Chrome DevTools)
   - PageSpeed Insights
   - WebPageTest
   - Chrome DevTools Performance panel

2. **Field Data (Real User Monitoring)**
   - Chrome User Experience Report (CrUX)
   - Google Search Console (Core Web Vitals report)
   - PageSpeed Insights (field data section)
   - Web Vitals JavaScript library
   - Real User Monitoring (RUM) tools

3. **JavaScript Library**
   ```javascript
   import {onCLS, onFID, onLCP} from 'web-vitals';

   onCLS(console.log);
   onFID(console.log);
   onLCP(console.log);
   ```

### Interpreting Thresholds

Google uses the **75th percentile** of page loads for assessment:
- At least 75% of page loads must meet "Good" threshold
- Measured separately for mobile and desktop
- Based on 28 days of aggregated data

---

## Testing Strategy

### Recommended Testing Approach

1. **Start with Field Data**
   - Check Google Search Console Core Web Vitals report
   - Identify problematic URLs
   - Understand real-user experiences

2. **Use Lab Data for Diagnosis**
   - Run Lighthouse on slow pages
   - Use Chrome DevTools Performance panel
   - Identify specific issues and bottlenecks

3. **Test Across Devices**
   - Mobile performance is typically worse
   - Test on real devices, not just emulation
   - Consider slower networks (3G, 4G)

4. **Monitor Continuously**
   - Set up Real User Monitoring
   - Track metrics over time
   - Monitor after deployments

---

## Common Optimization Patterns

### Priority Order

1. **Fix Critical Issues First**
   - Poor LCP (> 4s)
   - Poor CLS (> 0.25)
   - Poor FID/INP (> 300ms/500ms)

2. **Server and Network**
   - Optimize server response time
   - Implement CDN
   - Enable compression
   - Use HTTP/2+

3. **Critical Rendering Path**
   - Eliminate render-blocking resources
   - Inline critical CSS
   - Defer non-critical JavaScript

4. **Resource Optimization**
   - Compress and optimize images
   - Optimize fonts
   - Minimize JavaScript bundles

5. **Fine-Tuning**
   - Code splitting
   - Resource hints (preload, prefetch, preconnect)
   - Implement caching strategies

### Quick Wins

- Add width/height to all images
- Implement lazy loading
- Use modern image formats (WebP)
- Defer third-party scripts
- Use font-display: swap
- Minify CSS and JavaScript
- Enable text compression (gzip/Brotli)
- Implement browser caching
- Use a CDN

---

## Impact on SEO

### Ranking Factor

- Core Web Vitals are confirmed ranking factors
- Part of "Page Experience" signals
- Tiebreaker between similar content quality
- More important for mobile search

### Threshold Requirements

- Must pass for mobile version (mobile-first indexing)
- Desktop metrics also considered
- Assessed at page level, not site level
- Can affect individual page rankings

### Best Practices

- Prioritize pages with high traffic/visibility
- Focus on pages with conversion goals
- Don't sacrifice content quality for metrics
- Balance user experience with technical optimization
- Monitor changes after optimization
- Test on real devices and networks

---

## Resources and Tools

### Official Google Resources
- [web.dev/vitals](https://web.dev/vitals/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- Google Search Console Core Web Vitals Report
- Chrome DevTools

### Testing Tools
- Lighthouse CI (automated testing)
- WebPageTest
- Chrome User Experience Report API
- Web Vitals Chrome Extension

### Monitoring Solutions
- Google Analytics (with web-vitals library)
- Cloudflare Web Analytics
- Commercial RUM solutions (SpeedCurve, Calibre, etc.)
