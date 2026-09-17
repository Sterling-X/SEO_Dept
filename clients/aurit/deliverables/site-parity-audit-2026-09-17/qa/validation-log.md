# Aurit Rendered and Endpoint Validation Log

Validation date: September 17, 2026

Method: read-only connected-browser inspection plus targeted HTTP and DNS checks. No form was submitted.

## Rendered page samples

| Sample | Staging observation | Live observation | Result |
|---|---|---|---|
| Homepage, desktop | Blue/Google Sans redesign; different navigation, hero, sections, CTAs, rating, footer, and consultation behavior | Green/Recoleta design with the current live sections, CTA/modal, newsletter, and footer | Not 1:1 |
| Homepage, mobile | Different menu, stacking, copy, CTAs, sections, and phone/rating display at a 390 x 844 CSS viewport | Current live mobile design at the same CSS viewport | Not 1:1 |
| `/about/` | 998 rendered words, 40 images, no page form, Google Sans H1 | 1,340 rendered words, 49 images, one page form, Recoleta H1 | Material template/content change |
| Article `/3-ways-parents-can-help-their-kids-adjust/` | 339 rendered words; title/author/adjacent articles/sidebar shown, article body absent | 1,932 rendered words; substantive article body shown | Critical template failure |
| `/category/divorce-mediation/` | 231 main-content words; green background, one form, changed browser title | 231 main-content words; white background, two forms | Content retained; metadata/template changed |
| `/divorce-mediation-guide/` | 3,104 main-content words, 13 images, no page form | 3,104 main-content words, 16 images, one page form | Core content retained; global template changed |
| Scottsdale city | Root path `/scottsdale/`, 974 rendered words, 3 images, Google Sans H1 | Nested path `/locations/arizona/scottsdale/`, 2,255 rendered words, 36 images, Recoleta H1 | Material URL/content/design change |
| Maricopa service area | 1,367 main-content words, one image, no page form | 1,367 main-content words, five images, one page form | Core content retained; links/assets/form changed |
| Michael Aurit team page | 82 main-content words, four images, no page form | 82 main-content words, nine images, one page form | Core content retained; contact/global template changed |
| `/free-consultation/` | Native six-field POST form with action ending in `#`; common broken form iframe also present but hidden | Visible functioning third-party form iframe | Different conversion implementation; submission untested |

Rendered word counts include page chrome unless the row explicitly says main-content words. Site-specific browser zoom was compensated for the matched homepage viewport checks.

## Interaction checks

| Interaction | Staging | Live |
|---|---|---|
| Desktop navigation dropdown | Worked | Worked |
| Mobile menu | Worked | Worked |
| FAQ accordion | Worked | Worked |
| Welcome video | Opened a Vimeo iframe after click | Vimeo player rendered | Worked with different implementation |
| Homepage carousel controls | Research and review rails moved | Current live carousel rendered | Staging controls worked; content/design differ |
| Primary consultation CTA | Scrolled to staged consultation section on tested CTA | Opened current live consultation flow | Different behavior |
| `Book My Consult` modal | Opened a frame that did not load its form | Loaded the live lead form | Staging failed |

## Endpoint evidence

| Target | Check | Result |
|---|---|---|
| `https://discover.stagingaurit.wpengine.com/l/1087043/2025-07-01/7btyzt` | DNS A/CNAME and rendered iframe | No DNS answer; form could not load |
| Live counterpart on `discover.auritmediation.com` | HTTP/browser | Endpoint resolved and the form rendered |
| `https://stagingaurit.wpengine.com/wp-content/uploads/2025/12/judge-gavel.jpeg` | Direct HTTP and rendered image dimensions | HTTP 404; image rendered at 0 x 0 |
| Staging `/robots.txt` | Direct HTTP | `User-agent: *` and `Disallow: /` |
| Live `/robots.txt` | Direct HTTP | Allows crawling except WordPress admin and declares the sitemap |

## Known exclusions

- No lead, checkout, account, newsletter, or consultation form submission.
- No CRM, notification-email, consent-storage, analytics-event, or call-routing validation.
- No exhaustive visual check of all 170 mapped pairs. Source/metadata crawling covered the full saved corpus; rendered checks sampled each material template family.
- No accessibility, performance, security, or legal-accuracy review.
- Automated direct-fetch authorization behavior for the live Vimeo endpoint was not counted as a visible failure because the player rendered in the browser.
