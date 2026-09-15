# Source Inventory for Independent Review

Run: `2026-09-15-scottjkalishlaw-page-inventory`  
Business: `https://scottjkalishlaw.com/`  
Research date: 2026-09-15  
Criteria: [00-evaluation-criteria.md](00-evaluation-criteria.md)

This is the evidence inventory given to `seo_reviewer` before the strategist's initial answer. It does not contain that answer or ask the reviewer to agree with a proposed list.

## Original task supplied to the reviewer

Identify the site's main commercial and authority-building pages for an SEO dashboard. Include main practice-area pages, other substantial conversion or authority pages where justified, and physical-office location pages only when name, address, phone, and actual-office evidence support them. Exclude blog posts and news articles, general service-area pages without verified office evidence, duplicate URLs, redirect variants, and irrelevant utility pages. Prioritize navigation-linked pages while checking the sitemap and relevant internal links for meaningful omissions. Treat commercial importance as inference unless actual conversion or revenue data supports more.

Required outputs are a plain URL list, a separate evidence table, and a short inspection record. The review must apply the frozen criteria without inventing evidence.

## Discovery sources inspected

| Source | Result |
|---|---|
| [English homepage](https://scottjkalishlaw.com/) | Live `200`, self-canonical, indexable; header, dropdowns, page CTAs, footer, and internal service links inspected. |
| [Spanish homepage](https://scottjkalishlaw.com/es/) | Live `200`, self-canonical, indexable; navigation, homepage links, and language routing inspected. |
| [robots.txt](https://scottjkalishlaw.com/robots.txt) | Live `200`; declares `https://scottjkalishlaw.com/sitemap_index.xml`. |
| [XML sitemap index](https://scottjkalishlaw.com/sitemap_index.xml) | Live `200`; lists page, post, and local sitemaps. |
| [Page sitemap](https://scottjkalishlaw.com/page-sitemap.xml) | Live `200`; 133 URL entries inspected and filtered. |
| [Post sitemap](https://scottjkalishlaw.com/post-sitemap.xml) | Live `200`; 30 post entries identified as excluded article content. |
| [Local sitemap](https://scottjkalishlaw.com/local-sitemap.xml) | Live `200`; only links `locations.kml`. |
| [Location KML](https://scottjkalishlaw.com/locations.kml) | Live `200`; one placemark, but address and phone fields are empty, so it supplies no office proof. |
| [Human sitemap](https://scottjkalishlaw.com/sitemap/) | Inspected as an internal discovery aid; the sitemap page itself is utility, not a proposed landing page. |

Direct page checks used live GET responses, final destinations, robots metadata, and declared canonical markup. Search extraction intermittently returned `429` or internal errors; direct GET checks succeeded for the recorded candidates. No analytics, Search Console, call tracking, CRM, conversion, or revenue data was available.

## English navigation and page-role inventory

The current English header/dropdowns link the seven core practice pages, attorney hub and three biographies, location hub and three location pages, resources hub and resources, and contact page. The homepage and footer add the family-law overview, consultation, mission, and reviews pages.

### Core and commercial hierarchy checked

Every URL in this section returned `200` at the requested URL, declared a self-canonical, and was indexable unless a specific exception is stated.

- Homepage and family-law overview:
  - `https://scottjkalishlaw.com/`
  - `https://scottjkalishlaw.com/family-law-attorney/`
- Header-linked core practices:
  - `https://scottjkalishlaw.com/florida/divorce/`
  - `https://scottjkalishlaw.com/florida/child-custody/`
  - `https://scottjkalishlaw.com/florida/child-support/`
  - `https://scottjkalishlaw.com/florida/alimony/`
  - `https://scottjkalishlaw.com/florida/property-division/`
  - `https://scottjkalishlaw.com/florida/paternity/`
  - `https://scottjkalishlaw.com/florida/prenup-postnup/`
- Sitemap/internal-link service omissions:
  - `https://scottjkalishlaw.com/florida/guardianship-in-florida/`
  - `https://scottjkalishlaw.com/family-law-attorney/florida-restraining-orders-injunctions/`
- Current procedural service children:
  - `https://scottjkalishlaw.com/florida/divorce/contested/`
  - `https://scottjkalishlaw.com/florida/divorce/uncontested/`
  - `https://scottjkalishlaw.com/florida/child-custody/modification/`
  - `https://scottjkalishlaw.com/florida/child-custody/emergency-custody-orders/`
  - `https://scottjkalishlaw.com/florida/child-custody/parenting-plans/`
  - `https://scottjkalishlaw.com/florida/child-support/enforcement/`
  - `https://scottjkalishlaw.com/florida/child-support/modification/`
  - `https://scottjkalishlaw.com/florida/alimony/temporary-support/`
  - `https://scottjkalishlaw.com/florida/property-division/equitable-distribution/`
  - `https://scottjkalishlaw.com/florida/paternity/establishing-paternity/`
- Restraining-order service children:
  - `https://scottjkalishlaw.com/family-law-attorney/florida-restraining-orders-injunctions/domestic-violence-injunctions-or-restraining-orders/`
  - `https://scottjkalishlaw.com/family-law-attorney/florida-restraining-orders-injunctions/dating-violence-injunctions-or-restraining-orders-2/`
  - `https://scottjkalishlaw.com/family-law-attorney/florida-restraining-orders-injunctions/repeat-violence-injunctions-or-restraining-orders/`
  - `https://scottjkalishlaw.com/family-law-attorney/florida-restraining-orders-injunctions/sexual-violence-injunctions-or-restraining-orders/`
  - `https://scottjkalishlaw.com/family-law-attorney/florida-restraining-orders-injunctions/stalking-injunctions-restraining-orders-florida/`
- Additional substantial practice/resource candidates:
  - `https://scottjkalishlaw.com/family-law-attorney/florida-divorce-law/divorce-costs/`
  - `https://scottjkalishlaw.com/florida/locations/west-palm-beach/divorce/`
  - `https://scottjkalishlaw.com/florida/locations/west-palm-beach/child-custody/`
  - `https://scottjkalishlaw.com/florida/locations/west-palm-beach/child-support/`
  - `https://scottjkalishlaw.com/florida/locations/west-palm-beach/alimony/`
  - `https://scottjkalishlaw.com/florida/locations/west-palm-beach/property-division/`
  - `https://scottjkalishlaw.com/florida/locations/west-palm-beach/paternity/`
  - `https://scottjkalishlaw.com/florida/locations/west-palm-beach/prenup-postnup/`

The ten current procedural children contain service-specific sections and consultation CTAs. The divorce children, emergency custody, equitable distribution, and establishing-paternity pages were linked from their inspected parent hubs. The other five were found in the XML and human sitemaps and link back upward, but were not observed from their parent hub. The five restraining-order children are distinct service pages; domestic violence is linked from the family-law overview and repeat violence from the restraining-order hub, while the others were sitemap-discovered.

All seven West Palm Beach practice pages were deterministically checked and are `200`, self-canonical, and indexable. They are office-market service pages supported by the verified West Palm Beach office, not seven additional offices.

### Authority and conversion candidates checked

Every URL below returned `200`, a self-canonical, and index/follow metadata.

- Attorney authority:
  - `https://scottjkalishlaw.com/florida/attorneys/`
  - `https://scottjkalishlaw.com/florida/attorneys/scott-kalish/`
  - `https://scottjkalishlaw.com/florida/attorneys/dara-jaggars/`
  - `https://scottjkalishlaw.com/florida/attorneys/serena-pomeranz/`
- Location/office authority:
  - `https://scottjkalishlaw.com/florida/locations/`
  - `https://scottjkalishlaw.com/florida/locations/west-palm-beach/`
  - `https://scottjkalishlaw.com/florida/locations/miami/`
  - `https://scottjkalishlaw.com/florida/locations/fort-lauderdale/`
- Durable tools and lead resources:
  - `https://scottjkalishlaw.com/florida-divorce-guide-and-resources/`
  - `https://scottjkalishlaw.com/florida/child-support/calculator/`
  - `https://scottjkalishlaw.com/florida/alimony/calculator/`
  - `https://scottjkalishlaw.com/florida-divorce-process-explained/`
  - `https://scottjkalishlaw.com/florida-divorce-podcast/`
  - `https://scottjkalishlaw.com/south-florida-divorce-family-law-qa-calls/`
  - `https://scottjkalishlaw.com/how-smart-moms-protect-their-kids-during-divorce-florida/`
  - `https://scottjkalishlaw.com/10-secrets-to-every-successful-divorce/`
  - `https://scottjkalishlaw.com/divorce-and-children-live-webinar/`
- Trust and conversion:
  - `https://scottjkalishlaw.com/family-law-attorney-reviews/`
  - `https://scottjkalishlaw.com/firm-mission/`
  - `https://scottjkalishlaw.com/book-a-strategy-meeting/`
  - `https://scottjkalishlaw.com/contact-us/`

The resource hub directly links the calculators, process video, podcast, Q&A, Smart Moms training, and 10 Secrets guide. The divorce-and-children webinar and divorce-cost page are substantial, indexable sitemap/hreflang candidates. Page role, navigation, internal linkage, and CTAs support commercial or authority classification as an inference only.

## Physical-office evidence

| Candidate page | First-party NAP and office evidence | Corroboration and uncertainty |
|---|---|---|
| `https://scottjkalishlaw.com/florida/locations/west-palm-beach/` | Kalish & Jaggars, PLLC; 2161 Palm Beach Lakes Blvd, Suite 302, West Palm Beach, FL 33409; `(561) 208-1859`. Dedicated page and schema, office image, directions, arrival information; areas-served page calls it the main office and says it accepts in-person meetings. | [Florida Bar profile](https://www.floridabar.org/directories/find-mbr/profile/?num=1018603) corroborates firm and Suite 302. [Sunbiz](https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResultDetail?aggregateId=flal-l19000197795-6a8d263e-f8b0-4e93-80fd-7c237b77519e&directionType=CurrentList&inquirytype=EntityName&listNameOrder=KALISHHOLDINGS+L240001696700&searchNameOrder=KALISHJAGGARSTAUB+L190001977951&searchTerm=KALIPARK+LLC) and other current site blocks say Suite 309. Multiple site phone numbers also appear. High confidence actual main office; suite/NAP cleanup is unresolved. |
| `https://scottjkalishlaw.com/florida/locations/fort-lauderdale/` | Kalish & Jaggars, PLLC; 500 E. Broward Blvd, Suite 1710, Fort Lauderdale, FL 33394; `(954) 302-4280`. Dedicated page and schema, explicit office language, directions, parking, elevator/arrival instructions, and statement that staff greet clients in Suite 1710. | [Office Edge](https://officeedge.com/fort-lauderdale/contact/) operates Suite 1710 as shared/virtual and meeting space. The firm calls it appointment-only. One contact block says ZIP 33393 rather than 33394. Medium confidence physical meeting office; dedicated or continuously staffed occupancy is not established. |
| `https://scottjkalishlaw.com/florida/locations/miami/` | Kalish & Jaggars, PLLC; 701 Brickell Ave, Suite 1550, Miami, FL 33131; `(786) 551-1105`. Dedicated page and schema, explicit office language, directions, valet/garage arrival, and local contact information. | [Office Edge](https://officeedge.com/locations/) identifies Suite 1550 as executive/virtual-office and meeting space. The firm calls it appointment-only. Medium confidence physical meeting office; dedicated or continuously staffed occupancy is not established. |

The [contact page](https://scottjkalishlaw.com/contact-us/) and [areas-served hub](https://scottjkalishlaw.com/florida/areas-served/) also distinguish the West Palm Beach main office from appointment-based Miami and Fort Lauderdale offices. The office hub is a directory page, not a fourth office. No current Boca Raton office was supported; current site evidence routes Boca Raton clients to West Palm Beach.

## Spanish candidate inventory

The task was not limited to English. The Spanish homepage is indexable and linked through the language switch, and the page sitemap exposes 28 English/Spanish hreflang pairs. Omitting the language section without an explicit restriction would leave out live commercial and authority pages.

All 24 candidates below were individually checked: each returned `200` at the requested URL, declared a self-canonical, and was indexable.

- Home and service hierarchy:
  - `https://scottjkalishlaw.com/es/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/divorcio/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/custodia-de-los-hijos-y-tiempo-compartido-en-florida/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/divorcio/explicacion-de-los-costes-del-divorcio-en-florida-con-un-abogado-matrimonialista/`
- Restraining-order hierarchy:
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/ordenes-de-restriccion-ordenes-judiciales/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/ordenes-de-restriccion-ordenes-judiciales/medidas-cautelares-u-ordenes-de-alejamiento-por-violencia-en-la-pareja/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/ordenes-de-restriccion-ordenes-judiciales/medidas-cautelares-u-ordenes-de-alejamiento-por-violencia-domestica/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/ordenes-de-restriccion-ordenes-judiciales/medidas-cautelares-u-ordenes-de-alejamiento-por-violencia-reiterada/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/ordenes-de-restriccion-ordenes-judiciales/medidas-cautelares-u-ordenes-de-alejamiento-por-violencia-sexual/`
  - `https://scottjkalishlaw.com/es/el-mejor-abogado-de-derecho-familiar-sirviendo-a-las-familias-en-los-condados-de-broward-palm-beach-y-miami-dade/ordenes-de-restriccion-ordenes-judiciales/medidas-cautelares-contra-el-acoso/`
- Authority, locations, and conversion:
  - `https://scottjkalishlaw.com/es/bufete-de-divorcio-y-familia-de-florida/bufete-de-derecho-de-familia-y-divorcio-de-florida/`
  - `https://scottjkalishlaw.com/es/acerca-de/`
  - `https://scottjkalishlaw.com/es/abogada-dara-jaggars/`
  - `https://scottjkalishlaw.com/es/serena-sobre/`
  - `https://scottjkalishlaw.com/es/contacta-con-nosotros/`
  - `https://scottjkalishlaw.com/es/concierta-una-reunion-estrategica/`
  - `https://scottjkalishlaw.com/es/opiniones-de-abogados-de-derecho-de-familia/`
- Durable resources:
  - `https://scottjkalishlaw.com/es/guia-del-divorcio-en-florida-comprende-facilmente-el-proceso-de-divorcio-en-florida/`
  - `https://scottjkalishlaw.com/es/explicacion-del-proceso-de-divorcio-en-florida/`
  - `https://scottjkalishlaw.com/es/podcast-sobre-el-divorcio-en-florida/`
  - `https://scottjkalishlaw.com/es/10-secretos-de-todo-divorcio-con-exito/`
  - `https://scottjkalishlaw.com/es/como-protegen-las-madres-inteligentes-a-sus-hijos-durante-el-divorcio-florida-3-pasos-obvios-pero-comunmente-ignorados-repeticion/`
  - `https://scottjkalishlaw.com/es/divorcio-e-hijos-lo-que-debes-saber-para-proteger-mejor-a-tus-hijos-durante-el-divorcio/`

Spanish architecture uncertainties: several current English core practices and all three dedicated office pages have no Spanish counterpart. The Spanish divorce hreflang points to an English URL that redirects to the current divorce page; Spanish custody points to the legacy overlapping English custody page. Some Spanish resource cards lead to English destinations. Several extracted titles/headings or mixed-language sections appear inconsistent. Legal and translation accuracy were not reviewed.

## Material exclusions and anomalies supplied for review

| Candidate/family | Observed reason or unresolved issue |
|---|---|
| `/articles/`, `/news/`, post-sitemap URLs, and Spanish article counterparts | Excluded blog/news content under the task rule. |
| `/florida/areas-served/` and descendants | Service-area coverage pages, not distinct physical offices. Pages that reference the West Palm Beach office do not become additional offices. |
| `/florida/` | Redirects to the homepage; exclude redirect variant. |
| `/family-law-attorney/florida-divorce-law/` | Redirects to canonical `/florida/divorce/`; exclude redirect variant. |
| `/strategy-meeting/` | Redirects to `/book-a-strategy-meeting/`; exclude redirect variant. |
| `/family-law-attorney/child-custody-and-timesharing-florida/` | `200`, self-canonical, and indexable, but overlaps the navigation-prioritized `/florida/child-custody/`. Candidate for consolidation/cannibalization analysis rather than primary-list duplication. |
| `/no-drama-divorce-guide-florida-edition/` | Header/footer-linked lead page, but `noindex,nofollow`, no declared canonical detected, and absent from all XML sitemaps. Exclude from the organic landing-page set; it could be tracked separately as conversion support. |
| `/family-law-lp/`, `/child-custody-lp/`, Spanish PPC landing variants | Overlapping campaign/landing variants without confirmed organic role; exclude pending campaign context. |
| `/business-and-commercial-litigation/` | `200`, self-canonical, indexable, and commercial, but only sitemap-discovered and conflicts with current repeated statements that the firm exclusively practices family law. Treat as secondary/legacy pending business confirmation. |
| `/top-criminal-defense/` and descendants | Current top page is noindex/no canonical and the subject conflicts with current exclusive-family-law positioning. |
| Thank-you pages, privacy policy, search/feed/system URLs, human sitemap, thin folder parents | Utility, post-conversion, system, or insufficiently substantial for this dashboard. |
| `/es/bufete-de-divorcio-y-familia-de-florida/` | Indexable but approximately 258 extracted visible words including shared chrome; essentially a heading and shared form. Thin folder parent, not a substantial distinct page. |
| `/es/articles/`, `/es/mapa-del-sitio/`, staff biography | Blog/utility or outside the main attorney authority set. |

## Access and evidence limits

- Live evidence is a dated snapshot and can change.
- Canonical and robots checks verify page declarations, not Google index status.
- No analytics or business data supports claims of traffic, leads, revenue, or relative commercial value.
- External authoritative firm-specific corroboration was found for West Palm Beach, not for Miami or Fort Lauderdale. Shared-office-provider evidence supports physical meeting facilities but not dedicated or continuously staffed firm occupancy.
- No legal claims, translated legal accuracy, or content quality were validated.
- The inventory is curated for main landing-page monitoring, not a claim that every indexable URL was crawled or every dashboard metric was designed.
