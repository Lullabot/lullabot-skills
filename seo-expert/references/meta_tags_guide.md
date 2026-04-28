# Meta Tags Guide for SEO

This guide covers essential meta tags for SEO and how to implement them effectively.

## Essential Meta Tags

### Title Tag

**Purpose:** Most important on-page SEO element. Appears as clickable headline in search results.

**Syntax:**
```html
<title>Page Title - Brand Name</title>
```

**Best Practices:**
- **Length:** 50-60 characters (512-600 pixels)
- **Uniqueness:** Every page should have unique title
- **Keywords:** Include primary keyword near beginning
- **Brand:** Include brand name (usually at end)
- **Compelling:** Write for users, not just search engines
- **Format:** Page Title | Section | Brand Name

**Good Examples:**
```html
<title>Organic Coffee Beans | Premium Selection | CoffeeShop</title>
<title>How to Train Your Dog: Complete Guide 2024 | PetExperts</title>
<title>Women's Running Shoes - Free Shipping | SportStore</title>
```

**Bad Examples:**
```html
<!-- Too short -->
<title>Home</title>

<!-- Too long (will be truncated) -->
<title>Buy the Best Organic Fair Trade Coffee Beans Online with Free Shipping and 30 Day Money Back Guarantee at CoffeeShop</title>

<!-- Keyword stuffing -->
<title>Coffee, Coffee Beans, Buy Coffee, Organic Coffee, Coffee Shop</title>

<!-- Not unique -->
<title>Products - CoffeeShop</title>
```

**Character Limits by Platform:**
- Google: ~60 characters or 600 pixels
- Bing: ~65 characters
- Mobile: ~78 characters

---

### Meta Description

**Purpose:** Summary shown in search results. Affects click-through rate (CTR), not direct ranking.

**Syntax:**
```html
<meta name="description" content="Compelling page description that includes keywords and a call to action.">
```

**Best Practices:**
- **Length:** 150-160 characters (920-1000 pixels)
- **Uniqueness:** Every page should have unique description
- **Keywords:** Include target keywords naturally
- **CTA:** Include call-to-action
- **Accuracy:** Accurately describe page content
- **Compelling:** Encourage clicks

**Good Examples:**
```html
<meta name="description" content="Shop premium organic coffee beans with free shipping. Ethically sourced, freshly roasted. Order online today and save 20% on your first purchase.">

<meta name="description" content="Learn how to train your dog with our complete 2024 guide. Expert tips, step-by-step instructions, and video tutorials for all breeds.">
```

**Bad Examples:**
```html
<!-- Too short -->
<meta name="description" content="Welcome to our website.">

<!-- Too long (will be truncated) -->
<meta name="description" content="We offer the finest selection of organic fair trade coffee beans sourced from sustainable farms around the world with free shipping on orders over fifty dollars and a thirty day money back guarantee plus our loyalty program gives you points for every purchase.">

<!-- Keyword stuffing -->
<meta name="description" content="Coffee beans, organic coffee, fair trade coffee, buy coffee beans, coffee shop, coffee online.">

<!-- Duplicate/generic -->
<meta name="description" content="Products page">
```

**Note:** Google may generate its own description if:
- None provided
- Too short/vague
- Not relevant to query
- Better text found on page

---

### Meta Robots

**Purpose:** Control crawling and indexing behavior.

**Syntax:**
```html
<meta name="robots" content="index, follow">
```

**Directives:**
- `index` / `noindex`: Allow/prevent indexing
- `follow` / `nofollow`: Allow/prevent link following
- `none`: Same as "noindex, nofollow"
- `noarchive`: Prevent cached version
- `nosnippet`: Prevent description snippet
- `noimageindex`: Don't index images
- `notranslate`: Don't offer translation

**Common Uses:**
```html
<!-- Default (can omit) -->
<meta name="robots" content="index, follow">

<!-- Prevent indexing (staging site, thin content) -->
<meta name="robots" content="noindex, follow">

<!-- Block specific crawler -->
<meta name="googlebot" content="noindex">

<!-- Prevent caching -->
<meta name="robots" content="noarchive">

<!-- Maximum snippet length -->
<meta name="robots" content="max-snippet:100">

<!-- Maximum image preview -->
<meta name="robots" content="max-image-preview:large">
```

---

### Canonical Tag

**Purpose:** Specify preferred URL for duplicate/similar content.

**Syntax:**
```html
<link rel="canonical" href="https://example.com/preferred-url">
```

**Best Practices:**
- Use absolute URLs
- Self-referencing on all pages
- Points to accessible URL (not 404 or redirect)
- One canonical per page
- Consistent with hreflang

**Use Cases:**
```html
<!-- Original page -->
<link rel="canonical" href="https://example.com/product">

<!-- Duplicate/variant points to original -->
<link rel="canonical" href="https://example.com/product">

<!-- HTTPS canonical -->
<link rel="canonical" href="https://example.com/page">
```

---

## Open Graph Tags (Social Media)

**Purpose:** Control how content appears when shared on social media (Facebook, LinkedIn, etc.).

**Required Tags:**
```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
```

**Optional but Recommended:**
```html
<meta property="og:site_name" content="Brand Name">
<meta property="og:locale" content="en_US">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Image description">
```

**Content Types:**
- `website`: General pages
- `article`: Blog posts, news articles
- `product`: E-commerce products
- `video.movie`, `video.episode`, `video.tv_show`, `video.other`
- `music.song`, `music.album`, `music.playlist`

**Article-Specific Tags:**
```html
<meta property="article:published_time" content="2024-01-15T08:00:00+00:00">
<meta property="article:modified_time" content="2024-01-16T10:30:00+00:00">
<meta property="article:author" content="Author Name">
<meta property="article:section" content="Technology">
<meta property="article:tag" content="SEO">
```

**Image Requirements:**
- Minimum: 600x315 pixels
- Recommended: 1200x630 pixels
- Maximum: 8MB
- Formats: JPG, PNG, WebP
- Aspect ratio: 1.91:1

**Testing:**
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

---

## Twitter Card Tags

**Purpose:** Control how content appears when shared on Twitter/X.

**Required Tags:**
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

**Optional:**
```html
<meta name="twitter:site" content="@username">
<meta name="twitter:creator" content="@authorusername">
<meta name="twitter:image:alt" content="Image description">
```

**Card Types:**
- `summary`: Small image thumbnail
- `summary_large_image`: Large image
- `app`: Mobile app promotion
- `player`: Video/audio player

**Summary Card:**
```html
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Description under 200 characters">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

**Large Image Card:**
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Description under 200 characters">
<meta name="twitter:image" content="https://example.com/large-image.jpg">
```

**Image Requirements:**
- Summary: 144x144 minimum (1:1 ratio)
- Large: 300x157 minimum, 4096x4096 maximum (2:1 ratio recommended)
- Maximum: 5MB
- Formats: JPG, PNG, WebP, GIF

**Relationship with Open Graph:**
- Twitter falls back to OG tags if Twitter tags missing
- OG `og:title` → `twitter:title`
- OG `og:description` → `twitter:description`
- OG `og:image` → `twitter:image`

**Testing:**
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)

---

## Viewport Tag (Mobile)

**Purpose:** Control layout on mobile browsers.

**Required for Mobile:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Parameters:**
- `width=device-width`: Match screen width
- `initial-scale=1`: Initial zoom level
- `maximum-scale=5`: Maximum zoom allowed
- `minimum-scale=0.5`: Minimum zoom allowed
- `user-scalable=yes`: Allow/prevent pinch zoom

**Recommended:**
```html
<!-- Standard responsive -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Allow zoom (accessibility) -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
```

**Avoid:**
```html
<!-- Bad: Prevents zoom (accessibility issue) -->
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">

<!-- Bad: Fixed width -->
<meta name="viewport" content="width=1024">
```

---

## Additional Meta Tags

### Charset

**Purpose:** Specify character encoding.

**Required:**
```html
<meta charset="UTF-8">
```

**Best Practice:** Place as early as possible in `<head>` (within first 1024 bytes).

---

### Author

**Purpose:** Specify content author.

```html
<meta name="author" content="Author Name">
```

---

### Keywords (Deprecated)

**Status:** Not used by Google, Bing, or other major search engines.

```html
<!-- Don't use - has no SEO value -->
<meta name="keywords" content="keyword1, keyword2, keyword3">
```

---

### Geo Tags

**Purpose:** Specify geographic location (for local businesses).

```html
<meta name="geo.region" content="US-CA">
<meta name="geo.placename" content="San Francisco">
<meta name="geo.position" content="37.7749;-122.4194">
<meta name="ICBM" content="37.7749, -122.4194">
```

**Note:** Limited impact. Better to use LocalBusiness schema markup.

---

### Theme Color (Mobile)

**Purpose:** Browser UI color on mobile.

```html
<meta name="theme-color" content="#4285f4">
```

---

## Complete Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Character encoding -->
  <meta charset="UTF-8">

  <!-- Viewport -->
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Primary Meta Tags -->
  <title>Organic Coffee Beans | Premium Selection | CoffeeShop</title>
  <meta name="description" content="Shop premium organic coffee beans with free shipping. Ethically sourced, freshly roasted. Order online today and save 20% on your first purchase.">
  <meta name="keywords" content="organic coffee, coffee beans, fair trade coffee">

  <!-- Canonical -->
  <link rel="canonical" href="https://example.com/products/organic-coffee">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://example.com/products/organic-coffee">
  <meta property="og:title" content="Organic Coffee Beans | Premium Selection">
  <meta property="og:description" content="Shop premium organic coffee beans with free shipping. Ethically sourced, freshly roasted.">
  <meta property="og:image" content="https://example.com/images/coffee-beans-og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="https://example.com/products/organic-coffee">
  <meta name="twitter:title" content="Organic Coffee Beans | Premium Selection">
  <meta name="twitter:description" content="Shop premium organic coffee beans with free shipping. Ethically sourced, freshly roasted.">
  <meta name="twitter:image" content="https://example.com/images/coffee-beans-twitter.jpg">
  <meta name="twitter:site" content="@coffeeshop">

  <!-- Robots -->
  <meta name="robots" content="index, follow, max-image-preview:large">

  <!-- Additional -->
  <meta name="author" content="CoffeeShop">
  <meta name="theme-color" content="#6B4423">
</head>
<body>
  <!-- Page content -->
</body>
</html>
```

---

## Testing & Validation

### Tools
- **Google:** Rich Results Test, Mobile-Friendly Test
- **Social:** Facebook Debugger, Twitter Card Validator, LinkedIn Post Inspector
- **General:** Meta Tags Checker, SEO Meta Checker
- **Browser DevTools:** Inspect `<head>` section

### Common Issues
- Missing or duplicate title/description
- Title/description too long or too short
- Incorrect canonical URL
- Missing social media images
- Wrong image dimensions
- Conflicting directives (noindex + canonical)
- Missing viewport tag
- Incorrect character encoding

### Best Practices Checklist
- [ ] Unique title and description on every page
- [ ] Title 50-60 characters
- [ ] Description 150-160 characters
- [ ] Canonical tag on all pages
- [ ] Open Graph tags for social sharing
- [ ] Twitter Card tags
- [ ] Viewport tag for mobile
- [ ] UTF-8 character encoding
- [ ] No conflicting meta robots directives
- [ ] Images meet social media requirements
