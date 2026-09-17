# Aurit Full-Site Live vs Staging Parity Audit

Audit date: September 17, 2026

Staging: <https://stagingaurit.wpengine.com/>

Live: <https://auritmediation.com/>

## Decision

**FAIL. Do not approve staging as a 1:1 copy or approve a production cutover.**

The audit found 170 mapped direct-page pairs. None met strict 1:1 source/metadata parity: 169 are mechanically changed and one is a near-match that still differs. Staging also lacks 22 live city pages, has five unmatched direct pages, omits article bodies across the 94-page post template, contains 25 internally linked 404 targets, sends 269 links back to the live host, and uses shared modal form infrastructure that does not resolve.

This is not one isolated homepage redesign. It is a sitewide content, URL, template, navigation, and conversion-path migration with incomplete implementation.

## Scope and evidence boundary

The public-page corpus was built from:

1. Every URL in each XML sitemap index.
2. Recursive same-origin HTML links found on those pages.
3. Direct-page paths found on one host and probed on the opposite host.
4. Sequential rechecks of transient 5xx responses.
5. Rendered browser checks for the homepage at desktop and mobile widths and representative home, standard-page, article, category, guide, city, service-area, team, and consultation templates.

Hostnames, CDN/cache headers, and normal staging infrastructure were normalized or treated as environment differences. Staging's sitewide `robots.txt` block was retained as an expected staging safeguard.

The crawl covered every public page discoverable by these methods. A page absent from both sitemaps and both internal-link graphs cannot be proven absent without a CMS/database export. No forms were submitted, and CRM receipt, email delivery, analytics events, accessibility, performance, legal-claim accuracy, and exhaustive device/browser combinations were not tested.

The final crawl used four workers and completed with no unresolved transient status. An earlier eight-worker snapshot retained live 504 responses for `/category/finances-property/` and `/payment-confirmation/`; direct endpoint checks and the lower-concurrency confirmation both recovered them as direct 200 pages. They are therefore mapped pairs in the final inventory, not structural staging-only gaps.

## Inventory summary

| Measure | Live | Staging | Change |
|---|---:|---:|---|
| Sitemap URLs | 189 | 171 | Staging has 18 fewer |
| Known direct-200 HTML paths | 192 | 175 | Staging has 17 fewer |
| Mapped direct-page pairs | 170 | 170 | 161 same-path plus 8 renamed city pages and 1 uniquely matched landing page |
| Exact source/metadata matches | 0 | 0 | No mapped page is a strict copy |
| Mechanically changed mapped pages | 169 | 169 | Requires page/template review |
| Near-match mapped pages | 1 | 1 | `/best-therapists-in-arizona/`; not a holistic severity rating |
| Unmatched direct pages | 22 live-only | 5 staging-only | Inventory mismatch |

The complete 170-row comparison is in [page-change-inventory.md](page-change-inventory.md). Actual changed title/H1/canonical/robots/schema values are in [page-field-changes.md](page-field-changes.md). Crawl, redirect, metadata, and link-graph evidence is in [crawl-comparison.json](data/crawl-comparison.json) and [technical-crawl-appendix.md](technical-crawl-appendix.md).

## Release blockers and deployment dependencies

### 1. The staging article template omits the articles

Observation:

- All 94 direct-200 staging post URLs return the same 269-word source shell and no substantive source H1.
- Their 94 live counterparts contain 422 to 6,352 words, with a median of 1,954.5 words and a substantive H1.
- A rendered check of `/3-ways-parents-can-help-their-kids-adjust/` showed 339 visible words on staging versus 1,932 on live. The staging page displayed the title, author, adjacent articles, consultation block, categories, and popular posts, but not the article body.

Hypothesis:

- The staging post template or its dynamic-content assignment is not outputting the stored article body. The public evidence does not identify the exact WordPress/Elementor configuration responsible.

Recommendation and acceptance test:

- Restore the article body and substantive H1 at the shared template level for every retained post. If an approved redesign intentionally retires a specific post, replace the empty 200 shell with an approved relevant redirect or retirement response and remove obsolete sitemap/internal-link references. Re-crawl all 94 current post URLs and require either approved body/H1 output or an approved retirement mapping; no empty 200 shell may remain.

### 2. All 30 live city URLs are lost at their current paths

Observation:

- Live has 30 direct pages under `/locations/arizona/{city}/`.
- Those 30 paths end in 404 on staging. Phoenix includes a redirect to a query URL before the final 404.
- Staging created only eight root-level replacements: `/chandler/`, `/flagstaff/`, `/gilbert/`, `/glendale/`, `/goodyear/`, `/phoenix/`, `/scottsdale/`, and `/tucson/`.
- Twenty-two live city pages have no evident staged replacement.
- The live `/locations/arizona/` parent is indexable, self-canonical, and in the location sitemap. Staging serves the page as `noindex`, supplies no canonical, and omits it from the sitemap.
- The rendered Scottsdale replacement had 974 visible words and three images versus 2,255 words and 36 images on live. Its layout and typography also differ.

Live city pages with no staged replacement:

`anthem`, `apache-junction`, `avondale`, `buckeye`, `casa-grande`, `el-mirage`, `fountain-hills`, `lake-havasu-city`, `marana`, `maricopa`, `mesa`, `paradise-valley`, `peoria`, `prescott`, `queen-creek`, `san-tan-valley`, `sedona`, `sierra-vista`, `sun-city`, `surprise`, `tempe`, and `yuma`.

Recommendation and acceptance test:

- Preserve all 30 live paths and content, or approve an explicit one-to-one redirect and content migration for each page. Require direct-200 or single-hop final-200 behavior, canonical alignment, sitemap inclusion, updated internal links, and content/design QA for every city.

### 3. Consultation and modal form infrastructure is not equivalent

Observation:

- The common staging contact iframe points to `discover.stagingaurit.wpengine.com`, whose DNS A and CNAME lookups return no answer. The live equivalent resolves and loads a form.
- This broken iframe reference was present across the staged HTML corpus and prevents the shared modal path from matching live.
- Additional staged form embeds either use the failed staging form host or use live-host form URLs that redirect to the live homepage instead of a form.
- The staged `/free-consultation/` page renders a native six-field POST form with an action ending in `#`; live renders the visible consultation form in a third-party iframe. They are different conversion implementations.
- No form was submitted, so the visible native staging form's delivery and CRM behavior remain unknown.

Recommendation and acceptance test:

- Point each intended form placement to an approved functioning endpoint, then test visible loading, required-field validation, successful submission, CRM receipt, notifications, consent capture, thank-you behavior, and analytics events in both desktop and mobile states.

### 4. Staging contains 25 internally linked 404 targets

Twenty are staging-only regressions. Five are also broken on live and remain baseline cleanup items.

Staging-only 404s:

- Sitewide: `/glossary/`, `/guides/`, `/parenting-center/`, `/privacy-policy/`, `/terms-conditions/`, `/therapists/`.
- Other: `/quiz/`, `/high-asset-divorce-mediation/`, `/same-sex-divorce-mediation/`, `/spousal-maintenance-mediation/`, `/cultural-difference-mediation/`, `/domestic-abuse-mediation/`, `/military-divorce-mediation/`, `/resources/`, `/calculators/`, `/checklist/`, `/locations/arizona/buckeye/`, `/locations/arizona/phoenix/`, `/locations/arizona/scottsdale/`, and `/spousal-maintenance-calculator/`.

Shared live/staging 404s:

- `/mission/`.
- Four malformed relative statute paths under `/divorce-mediation/legal-separation-mediation/azleg.gov/ars/25/`: `00312.htm`, `00313.htm`, `00317.htm`, and `00329.htm`.

Recommendation and acceptance test:

- Update every source link to a direct intended destination or publish the missing target. Re-crawl until staging has zero internally linked final-404 targets. Track the five shared defects separately so fixing parity does not preserve known live errors.

### 5. Deployment-policy dependency: staging sends users and crawlers back to live

Observation:

- Twenty-six staging pages contain 269 absolute staging-to-live anchor occurrences leading to 63 live targets.
- The largest sources are the service-area hub and county pages, plus mediation service pages.
- Staging also uses seven staff email links at `@stagingaurit.wpengine.com`; live uses the intended `@auritmediation.com` addresses. The live footer additionally exposes `hello@auritmediation.com`, which the staged global footer omits.

Recommendation and acceptance test:

- Confirm the deployment URL-rewrite policy first. Replace links that block isolated staging QA or would remain wrong after cutover; otherwise verify that the launch process deterministically converts approved production-domain anchors. Restore production email destinations in either case. Re-crawl for zero unintended staging-host and cross-environment destinations before cutover.

### 6. A homepage/research image is broken

Observation:

- `/wp-content/uploads/2025/12/judge-gavel.jpeg` returns 404 on staging and is referenced from the homepage, including the `/online-divorce-mediation/` homepage alias.
- Advancing the rendered research carousel exposes the missing-image state.

Recommendation and acceptance test:

- Restore the asset or update the reference, then require a direct-200 image with nonzero rendered dimensions in every carousel state.

## Page and template changes

| Page/template | Verified change | Parity disposition |
|---|---|---|
| Homepage | Different global header, navigation, hero copy, CTAs, research, testimonials, rating display, FAQ treatment, office/map section, footer, typography, colors, forms, and mobile layout. Source-text similarity was 53.5%. | Material |
| Standard content pages | Redesign and content changes vary by page. `/about/` rendered 998 staging words versus 1,340 live; `/pricing/` changes its H1 from `Flat-Fee Pricing` to `Pricing and Flat Fees for Arizona Divorce Mediation`. | Material |
| Article posts, 94 | Staging omits each article body and exposes a blank/non-breaking-space H1 in source. | Critical |
| City pages, 30 live | Eight are rebuilt at new root paths with substantially less content; 22 have no staged replacement. | Critical |
| Service-area pages | Core body copy can remain intact. Maricopa rendered 1,367 main-content words on both hosts, but staging lacked the live form/assets and contained 28 links back to live. | Not 1:1 |
| Divorce mediation guide | The representative guide retained 3,104 main-content words on both hosts, but staged global forms/assets/navigation differ. | Not 1:1 |
| Category archives, 8 | Representative main content had 231 words on both hosts, but title, background, form count, and global template differ. | Material metadata/template change |
| Team pages, 7 | Representative main content remained 82 words, but forms/assets/global footer differ and every staff email uses the staging domain. | Material conversion/contact change |
| Consultation page | Staging uses an inline form; live uses a functioning embedded form. Copy, layout, form implementation, and conversion flow differ. | Critical until submission QA passes |

The homepage also changes displayed review proof from `4.73 stars (based on 90 Ratings)` on live to `4.5 stars (based on 51 Ratings)` on staging. Displayed phone numbers varied during browser checks and may be dynamically inserted call-tracking numbers; ownership and intended routing require confirmation rather than an automatic parity fix.

## URL and sitemap changes

Staging-only sitemap URLs:

- Eight root city pages: `/chandler/`, `/flagstaff/`, `/gilbert/`, `/glendale/`, `/goodyear/`, `/phoenix/`, `/scottsdale/`, `/tucson/`.
- Five new pages: `/contact-us-new-design/`, `/divorce-cost-calculator/`, `/faq/`, `/mediation-expert/`, `/tools/`.

The five staging-only direct pages are `/contact-us-new-design/`, `/divorce-cost-calculator/`, `/faq/`, `/mediation-expert/`, and `/tools/`. The staged `/child-custody/` page is uniquely matched to live `/lp/child-custody/`; the other eight unique-slug matches are the root-level city replacements.

Live-only sitemap URLs:

- `/locations/arizona/` and its 30 city children. Staging's parent exists outside its sitemap; eight children have root-level replacements; 22 remain live-only direct pages.

Both sitemaps include one redirecting post URL, `/courageous-co-parenting-sharing-new-years-resolutions/`, instead of its final `/child-custody-mediation/` destination.

## Metadata, schema, and internal discovery

Observation:

- Across the 161 same-path direct pages, 86 titles differ.
- Ninety-four posts have blank/non-breaking-space H1 source output; `/child-custody-mediation/` has no H1; `/pricing/` has a substantively rewritten H1. Other mechanical H1 differences are mainly spacing/casing serialization and should not be given the same severity.
- `/locations/arizona/` is the material canonical/robots mismatch.
- Staging `/contact/` lacks live's `ContactPage`, `LocalBusiness`, `GeoCoordinates`, `OpeningHoursSpecification`, `PostalAddress`, and `State` schema types.
- Sixty-eight direct, indexable staging sitemap URLs had zero inlinks in the static discovered corpus versus ten on live. This is an orphan-like signal, not proof of no JavaScript-only or external links.
- Staging has dozens of same-host internal links that first redirect. The exact saved-graph count and target table are in the technical appendix. The most widespread point to `/child-support/`, `/contact-us/`, `/how-it-works/`, and seven `/locations/{city}/` aliases rather than their final paths.

Recommendation and acceptance test:

- Restore approved titles, substantive H1s, canonical/indexability signals, contact schema, direct internal destinations, and at least one intentional internal discovery path for each retained indexable page. Validate with a fresh crawl after the URL decision is final.

## Expected environment differences and baseline issues

These should not be misclassified as staging regressions:

- Staging uses nginx/WP Engine while live also uses Cloudflare-facing infrastructure.
- Staging currently blocks all crawling in `robots.txt`. Keep that protection while remediation continues, then intentionally switch to the production allow/admin rules and production sitemap at launch.
- Five broken internal paths are shared by both hosts, as listed above.
- Live has four additional baseline final-404 targets: `/common-reasons-for-divorce/`, `/courageous-co-parenting-the-power-of-reframing/`, `/long-divorce-arizona-take/`, and `/mission-vision-values/`.
- The shared JavaScript/GTM console errors seen during homepage checks are cross-environment maintenance items, not proof of a staging-only parity regression.
- An automated direct fetch of the live Vimeo endpoint returned an authorization response, but the live video rendered in the browser. It is excluded from visible-defect counts.

## Required remediation sequence

1. Decide whether staging must strictly match live or whether the redesign is the approved target. This decision controls the page/template acceptance standard; it does not waive the universal failures below.
2. Restore the retained article bodies and H1 output, or implement an approved retirement/redirect mapping for intentionally retired posts.
3. Approve and implement the 30-city URL/content plan, including the state parent.
4. Repair all form endpoints and complete real submission/CRM/event tests.
5. Fix the 20 staging-only internally linked 404s and the broken image.
6. Apply and verify the approved deployment URL policy for the 269 live-host anchors, and restore all staging-domain email destinations.
7. Repair canonical, robots-at-launch, schema, sitemap, redirected internal-link, and orphan-like discovery issues.
8. Re-run the same full crawl plus desktop/mobile rendered QA. Require all 170 mapped pages to meet the approved acceptance standard and account for every unmatched URL.

## Deliverables

- [Downloadable Excel workbook](../../../../outputs/aurit-parity-audit-2026-09-17/aurit-full-site-parity-audit.xlsx)
- [Full page-by-page change inventory](page-change-inventory.md)
- [Actual page field changes](page-field-changes.md)
- [Technical link and crawl appendix](technical-crawl-appendix.md)
- [Rendered and endpoint validation log](qa/validation-log.md)
- [Machine-readable crawl evidence](data/crawl-comparison.json)
- [Reproducible crawl and comparison script](qa/crawl_compare.py)
- [Workbook builder](qa/build_workbook.mjs)
- [Offline package consistency check](qa/validate_package.py)

Reproduction command from the repository root:

```bash
python3 clients/aurit/deliverables/site-parity-audit-2026-09-17/qa/crawl_compare.py \
  --json clients/aurit/deliverables/site-parity-audit-2026-09-17/data/crawl-comparison.json \
  --inventory clients/aurit/deliverables/site-parity-audit-2026-09-17/page-change-inventory.md \
  --fields clients/aurit/deliverables/site-parity-audit-2026-09-17/page-field-changes.md \
  --technical clients/aurit/deliverables/site-parity-audit-2026-09-17/technical-crawl-appendix.md \
  --max-urls 600 --workers 4
```
