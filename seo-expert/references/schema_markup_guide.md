# Schema Markup Guide for SEO

Schema.org structured data helps search engines understand your content and can enable rich results in search.

## What is Schema Markup?

**Schema.org** is a collaborative vocabulary for structured data. It helps search engines:
- Understand content context
- Display rich snippets
- Enable enhanced search features
- Improve content categorization

**Formats:**
- **JSON-LD** (Recommended by Google)
- Microdata (HTML attributes)
- RDFa (Resource Description Framework)

**This guide focuses on JSON-LD** as it's the preferred format.

---

## JSON-LD Basics

**Syntax:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TypeName",
  "property": "value"
}
</script>
```

**Placement:** Typically in `<head>` or `<body>`, can be anywhere.

**Multiple Schemas:** Use multiple `<script>` tags or array format.

---

## Common Schema Types

### 1. Organization

**Use for:** Company/organization homepage.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "description": "Brief company description",
  "sameAs": [
    "https://www.facebook.com/examplecompany",
    "https://twitter.com/examplecompany",
    "https://www.linkedin.com/company/examplecompany"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer service",
    "email": "support@example.com",
    "availableLanguage": ["English", "Spanish"]
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94102",
    "addressCountry": "US"
  }
}
```

---

### 2. Website & SearchAction

**Use for:** Homepage, enables site search box in results.

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Example Company",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

---

### 3. Article / BlogPosting

**Use for:** Blog posts, news articles.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "image": [
    "https://example.com/image.jpg",
    "https://example.com/image-4x3.jpg",
    "https://example.com/image-16x9.jpg"
  ],
  "datePublished": "2024-01-15T08:00:00+00:00",
  "dateModified": "2024-01-16T10:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/authorname"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Company",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "description": "Article description or excerpt",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/article"
  }
}
```

**Image Requirements:**
- High resolution (1200px wide minimum)
- Multiple aspect ratios (16x9, 4x3, 1x1)
- Logo: 600x60px

---

### 4. Product

**Use for:** E-commerce product pages.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": [
    "https://example.com/product-image-1.jpg",
    "https://example.com/product-image-2.jpg"
  ],
  "description": "Product description",
  "sku": "SKU123",
  "mpn": "MPN456",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "USD",
    "price": "99.99",
    "priceValidUntil": "2024-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "Example Company"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "89"
  }
}
```

**Availability Values:**
- `https://schema.org/InStock`
- `https://schema.org/OutOfStock`
- `https://schema.org/PreOrder`
- `https://schema.org/Discontinued`

---

### 5. Review / AggregateRating

**Use for:** Product/service reviews.

**Single Review:**
```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "Product",
    "name": "Product Name",
    "image": "https://example.com/product.jpg"
  },
  "author": {
    "@type": "Person",
    "name": "Reviewer Name"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5",
    "worstRating": "1"
  },
  "reviewBody": "This is an excellent product. Highly recommended!",
  "datePublished": "2024-01-15"
}
```

**Aggregate Rating:**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "ratingCount": "89",
    "reviewCount": "72",
    "bestRating": "5",
    "worstRating": "1"
  }
}
```

---

### 6. Breadcrumbs

**Use for:** Navigation breadcrumbs.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://example.com/category"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Product",
      "item": "https://example.com/category/product"
    }
  ]
}
```

---

### 7. FAQ

**Use for:** Frequently Asked Questions pages/sections.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is your return policy?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>We offer a 30-day money-back guarantee on all products.</p>"
      }
    },
    {
      "@type": "Question",
      "name": "Do you ship internationally?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>Yes, we ship to over 100 countries worldwide.</p>"
      }
    }
  ]
}
```

**Notes:**
- Answer text can include HTML
- Minimum 2 questions
- Maximum 1 FAQPage per page

---

### 8. HowTo

**Use for:** Step-by-step instructions.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Bake Chocolate Chip Cookies",
  "description": "Simple recipe for classic chocolate chip cookies",
  "image": "https://example.com/cookie-recipe.jpg",
  "totalTime": "PT45M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "10"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "flour"
    },
    {
      "@type": "HowToSupply",
      "name": "chocolate chips"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "mixing bowl"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Mix ingredients",
      "text": "Combine flour, sugar, and butter in a bowl",
      "image": "https://example.com/step1.jpg",
      "url": "https://example.com/recipe#step1"
    },
    {
      "@type": "HowToStep",
      "name": "Bake",
      "text": "Bake at 350°F for 12 minutes",
      "image": "https://example.com/step2.jpg",
      "url": "https://example.com/recipe#step2"
    }
  ]
}
```

---

### 9. Local Business

**Use for:** Local businesses (restaurants, stores, services).

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Example Coffee Shop",
  "image": "https://example.com/storefront.jpg",
  "@id": "https://example.com",
  "url": "https://example.com",
  "telephone": "+1-555-123-4567",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "San Francisco",
    "addressRegion": "CA",
    "postalCode": "94102",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      "opens": "08:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday", "Sunday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/examplecoffee",
    "https://www.instagram.com/examplecoffee"
  ]
}
```

**More Specific Types:**
- Restaurant
- Hotel
- Store
- AutoRepair
- MedicalOrganization
- etc.

---

### 10. Event

**Use for:** Concerts, conferences, classes, etc.

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "SEO Conference 2024",
  "description": "Annual conference for SEO professionals",
  "image": "https://example.com/event-banner.jpg",
  "startDate": "2024-06-15T09:00:00-07:00",
  "endDate": "2024-06-17T17:00:00-07:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Convention Center",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "123 Main St",
      "addressLocality": "San Francisco",
      "addressRegion": "CA",
      "postalCode": "94102",
      "addressCountry": "US"
    }
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/event/tickets",
    "price": "299",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2024-01-01"
  },
  "performer": {
    "@type": "Person",
    "name": "Keynote Speaker"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Example Company",
    "url": "https://example.com"
  }
}
```

**Event Status:**
- `https://schema.org/EventScheduled`
- `https://schema.org/EventCancelled`
- `https://schema.org/EventPostponed`
- `https://schema.org/EventRescheduled`

**Attendance Mode:**
- `https://schema.org/OfflineEventAttendanceMode` (In-person)
- `https://schema.org/OnlineEventAttendanceMode` (Virtual)
- `https://schema.org/MixedEventAttendanceMode` (Hybrid)

---

### 11. Video

**Use for:** Video content.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to Train Your Dog",
  "description": "Complete guide to dog training",
  "thumbnailUrl": "https://example.com/video-thumbnail.jpg",
  "uploadDate": "2024-01-15T08:00:00+00:00",
  "duration": "PT10M30S",
  "contentUrl": "https://example.com/video.mp4",
  "embedUrl": "https://example.com/embed/video123",
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": "https://schema.org/WatchAction",
    "userInteractionCount": 5647
  }
}
```

---

### 12. Recipe

**Use for:** Recipe content.

```json
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "name": "Chocolate Chip Cookies",
  "image": [
    "https://example.com/cookie-1x1.jpg",
    "https://example.com/cookie-4x3.jpg",
    "https://example.com/cookie-16x9.jpg"
  ],
  "author": {
    "@type": "Person",
    "name": "Chef Name"
  },
  "datePublished": "2024-01-15",
  "description": "Classic homemade chocolate chip cookies",
  "prepTime": "PT20M",
  "cookTime": "PT12M",
  "totalTime": "PT32M",
  "keywords": "cookies, dessert, baking",
  "recipeYield": "24 cookies",
  "recipeCategory": "Dessert",
  "recipeCuisine": "American",
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": "150 calories",
    "fatContent": "7g",
    "carbohydrateContent": "22g",
    "proteinContent": "2g"
  },
  "recipeIngredient": [
    "2 cups flour",
    "1 cup sugar",
    "1 cup chocolate chips",
    "1/2 cup butter"
  ],
  "recipeInstructions": [
    {
      "@type": "HowToStep",
      "text": "Preheat oven to 350°F"
    },
    {
      "@type": "HowToStep",
      "text": "Mix dry ingredients"
    },
    {
      "@type": "HowToStep",
      "text": "Add wet ingredients and mix"
    },
    {
      "@type": "HowToStep",
      "text": "Bake for 12 minutes"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "127"
  }
}
```

---

## Multiple Schemas on One Page

**Option 1: Multiple script tags**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company"
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Example Company",
  "url": "https://example.com"
}
</script>
```

**Option 2: Array format**
```html
<script type="application/ld+json">
[
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Example Company"
  },
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Example Company",
    "url": "https://example.com"
  }
]
</script>
```

**Option 3: Graph format**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Company"
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com",
      "publisher": {
        "@id": "https://example.com/#organization"
      }
    }
  ]
}
</script>
```

---

## Testing & Validation

### Google Tools
- [Rich Results Test](https://search.google.com/test/rich-results)
- [Schema Markup Validator](https://validator.schema.org/)
- Google Search Console (Enhancement reports)

### Testing Process
1. Run Rich Results Test
2. Fix any errors (red)
3. Address warnings (yellow) if possible
4. Deploy to production
5. Monitor in Search Console

### Common Errors
- Missing required properties
- Invalid property values
- Incorrect date formats
- Wrong image dimensions
- Invalid URLs
- Type mismatches

---

## Best Practices

### General
- Use JSON-LD format
- Place in `<head>` or near relevant content
- Validate before deployment
- Include all required properties
- Use specific types when available
- Keep data accurate and up-to-date
- Match visible page content
- Don't markup hidden content

### Images
- Use high-resolution images
- Include multiple aspect ratios
- Specify width and height
- Use absolute URLs
- Optimize file sizes

### Dates
- Use ISO 8601 format
- Include timezone
- Example: `2024-01-15T08:00:00-08:00`

### Prices
- Always include currency
- Keep prices updated
- Specify availability
- Include priceValidUntil

---

## Schema Priority by Page Type

**Homepage:**
1. Organization
2. WebSite + SearchAction
3. LocalBusiness (if applicable)

**Blog Posts:**
1. Article/BlogPosting
2. Breadcrumbs

**Products:**
1. Product
2. AggregateRating
3. Breadcrumbs

**FAQ Pages:**
1. FAQPage

**How-To Guides:**
1. HowTo or Article

**Local Business:**
1. LocalBusiness
2. Organization

**Videos:**
1. VideoObject

**Recipes:**
1. Recipe

---

## Resources

- [Schema.org Full Documentation](https://schema.org)
- [Google Search Central - Structured Data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [Schema Markup Generator Tools](https://technicalseo.com/tools/schema-markup-generator/)
