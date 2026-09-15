# Technical SEO Reference

Use this file for crawlability, indexation, rendering, canonicalization, migrations, international SEO, faceted navigation, schema, and site health.

## 1) Classify the issue correctly

Separate:

- **crawlability**: can bots fetch the URL and key resources?
- **rendering**: can bots and users reach the meaningful content?
- **indexability**: can the URL be stored and served?
- **canonicalization**: is the right URL being consolidated?
- **rankability**: does the page deserve to rank?
- **measurement**: are changes being captured reliably?

## 2) High-value checks

### Discovery and crawl
- robots.txt
- XML sitemaps
- orphan pages
- crawl depth
- internal links from strong pages
- JS dependency for key navigation/content
- parameter traps
- pagination and faceted navigation

### Indexation
- meta robots / X-Robots-Tag
- canonicals
- duplicate templates
- parameter variants
- soft-404 behavior
- thin / near-empty pages
- staging leakage
- noindex template bugs

### Canonicalization
- self-referencing canonical on canonical pages
- absolute, consistent canonical targets
- redirect + canonical alignment
- slash/case/protocol consistency
- subdomain duplication
- hreflang only to canonical URLs

### Rendering
- SSR vs CSR availability
- hydration failures
- blocked JS/CSS
- content hidden behind interactions
- lazy-loading that never renders
- deferred navigation or content

## 3) Faceted navigation rules

For ecommerce and filtered URLs:
- identify combinations that deserve indexation
- prevent crawl waste on useless combinations
- align canonicals with index strategy
- preserve user utility without exploding index count
- use internal linking intentionally to support valuable facets

## 4) Migration workflow

Before launch:
- URL inventory
- redirect map
- canonical target list
- metadata parity
- internal-link update plan
- XML sitemap update
- staging crawl
- analytics annotations
- rollback triggers

Launch-day:
- validate redirects
- validate canonicals
- validate robots / noindex
- check render state
- submit sitemaps
- spot-check templates and high-value pages

Post-launch:
- compare indexed pages
- compare rankings and clicks by template/page type
- monitor 404s, redirect chains, and soft-404s
- validate key conversions
- patch internal links and missed redirects quickly

## 5) International and hreflang

For multi-region/multi-language sites:
- ensure each market has a clear purpose
- use canonical URLs only in hreflang sets
- keep return tags complete where applicable
- differentiate content when targeting separate markets
- align language/region signals with on-page content, currency, shipping, proof, and localization
- avoid near-duplicate market pages with weak differentiation

## 6) Schema usage

Recommend schema only when it matches visible content and a real page purpose.

Common types:
- Organization
- LocalBusiness
- Breadcrumb
- Product
- Service
- FAQ
- Article
- BlogPosting
- Review / AggregateRating
- HowTo
- Event

Never use fantasy markup disconnected from the page.

## 7) Core Web Vitals and UX

Treat performance as one part of indexability, usability, and conversion:
- biggest bottleneck first
- mobile experience first where relevant
- prioritize template-level wins
- tie performance fixes to business pages, not just overall averages

## 8) Output pattern

For technical recommendations, specify:
- issue type
- affected templates/pages
- why it matters
- recommended fix
- owner
- dependency
- validation step
- expected leading indicator
