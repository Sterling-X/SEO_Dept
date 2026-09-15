# Google Systems Reference

Use this file when the request touches Google internals, leaked API fields, ranking signals, click systems, indexing nuance, anchors/links, localized duplication, entities, Content Warehouse, Document AI, or restrictions.

Source: Google API Content Warehouse v0.4.0 documentation (14,014 attributes across 2,795+ classes), confirmed by ex-Google employees and analyzed by Rand Fishkin / Mike King (May 2024). All definitions below are quoted or paraphrased from the API documentation unless otherwise noted.

## Table of contents

1. How to use this file
2. NavBoost and click systems
3. Links and anchors
4. Localized clusters and hreflang
5. Embedded content and links
6. People and entities
7. Document AI
8. Cloud Content Warehouse
9. Restrictions and gating
10. Full API field inventory
11. Leak interpretation rules
12. Practical SEO translation

---

## 1) How to use this file

Follow this order for any Google-systems question:

1. Give the official definition quoted below when one exists.
2. Explain it in plain English.
3. Translate into practical SEO advice.
4. Clearly label what is **definition**, what is **inference**, and what is **practical advice**.
5. Never claim exact ranking weights or universal live usage from the existence of a field.

For deeper field-level detail, load `reference/12-google-api-field-inventory.md`.

---

## 2) NavBoost and click systems

### Source context
NavBoost is referenced in VP of Search Pandu Nayak's DOJ testimony and described extensively in the May 2024 API leak analysis. Google VP Alexander Grushetsky called NavBoost potentially "more positive on clicks (and likely even on precision / utility metrics) by itself than the rest of ranking." Engineer Paul Haahr's resume describes it as "one of Google's strongest ranking signals."

### What NavBoost does (from leak analysis)

NavBoost is a logs-based ranking system that processes user interaction data:

- **Click counting**: Tracks number of clicks on search results for a given query.
- **Long clicks vs short clicks**: Distinguishes between clicks where users stay on the destination (long/satisfying) versus return quickly to the SERP (short/unsatisfying).
- **Squashed vs unsquashed clicks**: Uses cookie history, logged-in Chrome data, and pattern detection to distinguish organic user clicks from manual or automated click spam. "Squashed" clicks are deduplicated/normalized; "unsquashed" are raw.
- **Query-chaining signals**: If users search for term A, fail to find what they want, then immediately search term B and click a result, the clicked destination can receive a boost for term A. Example from source: users searching "Rand Fishkin" who then search "SparkToro" and click SparkToro.com cause SparkToro to gain relevance for "Rand Fishkin."
- **Host-level quality evaluation**: NavBoost data is aggregated at the host level for overall site quality scoring. The source speculated this could be what Google and SEOs historically called "Panda."
- **Intent classification**: Certain thresholds of clicks on videos or images for a query trigger video or image SERP features for that query and related NavBoost-associated queries.
- **Geo-fencing**: Click data is segmented by country, state/province, and device type (mobile vs desktop). If insufficient data exists for a region or user-agent, Google may apply signals universally.
- **Trending demand detection**: Uses search volume patterns to identify trending queries.

### Additional systems from the leak

- **BabyPanda**: A newer scoring signal mentioned alongside spam signals in quality evaluation.
- **Exact-match domain penalties**: Penalties exist for domain names that exactly match unbranded search queries (e.g., mens-luxury-watches.com).
- **Whitelists**: During Covid-19, Google used whitelists for sites that could rank for Covid-related searches. Similar whitelists were used for election-related information.
- **Chrome/clickstream data**: The source claims Google's desire for clickstream data was a key motivation for creating Chrome (launched 2008), initially gathering data from Toolbar PageRank.

### NavBoost SEO implications

- **Brand demand is the most leverageable ranking factor.** Building navigational demand, branded search volume, and destination preference outside of Google directly strengthens ranking signals.
- **Click satisfaction matters more than click volume.** Long clicks, return visits, and query resolution signal value. Thin pages that bounce users back to the SERP actively hurt.
- **Query-chaining creates entity association.** When your brand becomes the destination users refine toward, you gain relevance for upstream queries.
- **Geo and device segmentation mean local performance is local.** Strong clicks in one market do not automatically transfer to another.
- **Site-level quality is aggregated from page-level signals.** One section of weak pages can drag the whole domain.
- **New sites and small brands face a cold-start problem.** Without click history or brand demand, NavBoost has nothing to amplify. This supports the observation that SEO returns are poor for unknown brands until credibility and demand are established.

---

## 3) Links and anchors

### Official definitions

- **Anchors** (`GoogleApi.ContentWarehouse.V1.Model.Anchors`): Contains a list of anchor objects plus metadata including `indexTier`, `targetDocid`, `targetSite`, `targetUrl`, and multiple drop counters (`homepageAnchorsDropped`, `localAnchorsDropped`, `nonlocalAnchorsDropped`, `redundantAnchorsDropped`, `supplementalAnchorsDropped`).
- **AnchorsAnchor** (`GoogleApi.ContentWarehouse.V1.Model.AnchorsAnchor`): Individual anchor/link record with fields including `creationDate`, `origText`, `text`, `fragment`, `sourceType`, `pagerankWeight`, `firstseenDate`, `lastUpdateTimestamp`, `forwardingTypes`, `parallelLinks`, `locality`.
- **pagerankWeight**: "Weight to be stored in linkmaps for pageranker."
- **AnchorsAnchorSource**: "Attributes of the source document for the link."
- **AnchorsRedundantAnchorInfo**: Sampling and deduplication logic for redundant anchors by (domain, text) pair.

### Source type quality tiers

The API defines explicit quality tiers for link sources:

- **TYPE_HIGH_QUALITY**: Top-tier source pages (lowest numeric value = highest quality)
- **TYPE_FRESHDOCS**: Treated same as HIGH for anchor-importance and duplicate-removal
- **TYPE_MEDIUM_QUALITY**: Mid-tier source pages
- **TYPE_LOW_QUALITY**: Bottom-tier source pages (highest numeric value = lowest quality)

### Key anchor fields explained

- **sourceType**: Quality tier of the source page. Determines how much weight the anchor carries.
- **pagerankWeight**: Numeric weight used by the PageRanker system. Stored in linkmaps.
- **firstseenDate**: When the link was first discovered. Indicates link age and freshness.
- **lastUpdateTimestamp**: When link information was last refreshed. Freshness signal.
- **creationDate**: Used for history tracking; also used in Freshdocs Twitter indexing (retweet as anchor of original tweet).
- **forwardingTypes**: How the anchor target forwards to a canonical URL. Indicates whether link equity merges cleanly or is lost through redirect chains.
- **parallelLinks**: Additional same-domain links from the same source page. Indicates potential dilution.
- **locality**: Relatedness or structural quality metric between source and target.
- **origText**: Original anchor text as found on the source page.
- **text**: Processed/normalized anchor text.
- **fragment**: URL fragment (hash) of the anchor target.

### Anchor drop counters

The system tracks how many anchors are dropped during processing:
- `homepageAnchorsDropped`: Local homepage anchors dropped in AnchorAccumulator
- `localAnchorsDropped`: Local non-homepage anchors dropped
- `nonlocalAnchorsDropped`: Non-local anchors dropped
- `redundantAnchorsDropped`: Redundant anchors dropped in linkextractor
- `supplementalAnchorsDropped`: Supplemental anchors dropped (deprecated)

### PageRank variants (from leak analysis)

The leak references multiple versions of PageRank:
- `rawPagerank`: A base or unprocessed PageRank value
- A deprecated PageRank referencing "nearest seeds"
- `firstCoveragePageRank`: PageRank from when the document was first served/indexed

This suggests PageRank has evolved significantly from the original 1998 paper and exists in multiple forms internally.

### SEO implications for links

- **Not all links are equal, and Google explicitly tiers them.** Source quality, freshness, anchor text, forwarding behavior, locality, and parallelism all factor in.
- **Link freshness matters.** Both discovery date and last-update date are tracked. Stale link profiles may lose relative value.
- **Redirect chains affect equity transfer.** The `forwardingTypes` field suggests clean canonical paths preserve value better than messy redirects.
- **Redundant anchors are deduplicated.** Mass-generating identical anchor text from the same domain is explicitly handled and dropped.
- **Anchor text still matters but is processed.** Both original and normalized text are stored, meaning Google can see through minor text manipulations.
- **Locality/relatedness between source and target is measured.** Topically relevant links from related pages carry more weight.
- **Link reclamation is high-value.** Existing links with clean forwarding and high source quality are more valuable than chasing new low-quality links.

---

## 4) Localized clusters and hreflang

### Official definitions

- **IndexingDupsLocalizedLocalizedClusterTargetLink**: "Message containing information about the localized URL linked to from this document."
- **IndexingDupsLocalizedLocalizedClusterCluster**: Contains `clusterId`, `clusterType`, `filteringEnabled`, `language`, `regionCode` (Stable), `urlRegionCode`.
- **IndexingDupsLocalizedLocalizedClusterTargetLinkSets**: Tracks localized URL link sets by context type.

### Target link types

Google tracks localized links from three distinct contexts:
- **hreflangTargetLink**: Links declared via hreflang annotations
- **inbodyTargetLink**: Links found in page body content
- **outlinksTargetLink**: Links found in outgoing link sets

### Cluster fields

- **clusterId**: Unique identifier for the localized cluster
- **clusterType**: Classification of the cluster
- **filteringEnabled**: When true, limits multiple results from the same cluster appearing in the SERP
- **language**: Language code for the cluster
- **regionCode**: Stable region code
- **urlRegionCode**: Region code derived from the URL itself

### Link-based cluster info (legacy)

- **IndexingDupsLocalizedLocalizedClusterLinkBasedClusterInfo**: Legacy metadata including `crawlTimestamp`, `annotationSource`, `url`, `languageCode`.
- **LinkData / LinkMember**: Supporting structures for cluster membership.

### Site-dup rules

- **sitedupRuleId**: List of rule IDs per URL. Set when a cluster spans more than one host and is not otherwise filtered. Controls cross-domain duplicate handling.

### Diagnostics

- **warningMessage**: Debug indicator for early cross-domain link filtering and related processing issues.

### SEO implications for international/localized content

- **Hreflang is not an isolated switch.** Google interprets language/region clusters through multiple signals: hreflang annotations, in-body links, and outlinks.
- **Filtering can suppress weak market pages.** The `filteringEnabled` flag means Google can actively limit visibility of near-duplicate market variants in the same SERP.
- **Country pages need material differentiation.** If content is substantially identical across markets, cluster filtering may hide some versions.
- **Cross-domain localization adds complexity.** The `sitedupRuleId` system handles clusters spanning multiple hosts, meaning ccTLD strategies interact with dedup logic.
- **Keep hreflang sets clean and pointing to canonical URLs.** Misaligned hreflang creates conflicting cluster signals.
- **Align content genuinely with each market.** Currency, legal context, proof, geography, and language must match the declared region.

---

## 5) Embedded content and links

### Official definitions

- **IndexingEmbeddedContentEmbeddedContentInfo**: Information about embedded content within documents, including docjoins membership.
- **EmbeddedLinksInfo**: Metadata about links found within embedded content.
- **EmbedderInfo**: Information about the embedder (the page or entity doing the embedding), including importance signals.
- **FetchHostCount**: Counter for fetch operations by host.
- **FetchUrlResponseMetadata**: Response metadata from URL fetching operations.
- **LinkInfo**: General link information within embedded contexts.

### Plain-English translation

Google tracks not just direct links between pages but also links and content that appear within embedded contexts (iframes, embedded widgets, etc.). The system records who is embedding what, how important the embedder is, and what links exist within embedded content.

### SEO implications

- **Embedded content is not invisible to Google.** Links within embedded contexts are tracked separately.
- **Embedder importance matters.** Being embedded by high-authority pages may carry signal, but the system distinguishes embedded links from direct editorial links.
- **Widget links and embed-based link building are tracked separately.** Do not assume embedded links carry the same weight as contextual editorial links.

---

## 6) People and entities

### Official definitions

- **AppsPeopleOzExternalMergedpeopleapiPerson**: "Merged-person combines multiple sources of data like contacts and profiles."
- **PersonFieldMetadata**: Metadata about individual fields on a person record.
- **PersonMetadata**: Overall metadata about a person entity.
- **PersonMetadataScoringInfo**: Contains `rawMatchQualityScore` and `stExpressionResults` (with `StExpressionResult` containing `name` and `value` pairs). Used for relevance/match quality in directory search contexts.
- **OrganizationProject**: Contains `description`, `name`, `role`, `type`, `url`.
- **OtherKeyword**: Contains `formattedType`, `metadata`, `source`, `type`, `value`.

### Entity data families

The People API covers extensive entity modeling:
- **Identity**: Name, Nickname, Birthday, Gender, About, Photos, CoverPhoto
- **Contact**: Email, Phone, Address, IM, Calendar
- **Professional**: Organization, OrganizationAssignment, OrganizationProject, Occupation, Mission
- **Social**: Membership, CircleMembership, ContactGroupMembership, Affinity, Interest
- **Access control**: FieldAcl, AclEntry, AclEntryScope (with person, membership, circle, and contact group scopes)
- **Platform-specific**: MapsProfile, MapsExtendedData, GplusExtendedData, HangoutsExtendedData, GPayExtendedData, CallerIdExtendedData
- **Scoring**: rawMatchQualityScore, stExpressionResults

### SEO implications

- **Entities are real objects in Google's systems, not abstractions.** People, brands, and organizations are modeled with structured fields, scoring, and relationships.
- **Author and organization consistency matters.** Google can merge signals across profiles, contacts, and platform data. Inconsistent information fragments the entity.
- **Entity scoring exists.** The `rawMatchQualityScore` field confirms that entities are scored for relevance/quality.
- **Connect people to organizations to projects.** The OrganizationProject model with name, role, type, and url means Google can map people to their work.
- **Platform presence reinforces entity strength.** Maps profiles, social accounts, professional directories, and structured data all feed the merged-person model.
- **E-E-A-T connection**: The leak does not show E-E-A-T as a direct ranking field, but entity modeling infrastructure suggests author recognition and organizational authority feed quality evaluation indirectly.

---

## 7) Document AI

### Official definitions

- **GoogleCloudDocumentaiV1Document**: "Represents the canonical document resource in Document AI."
- **DocumentEntity / EntityNormalizedValue / EntityRelation**: Entities extracted from documents with normalized values and relationships.
- **DocumentPage / PageAnchor / PageAnchorPageRef**: Page-level structure with anchors linking to specific locations.
- **DocumentPageBlock / DetectedBarcode / DetectedLanguage / Dimension / FormField / Image**: Block-level content types within pages.
- **BoundingPoly**: Image annotation polygon for layout geometry.

### SEO implications

- **Google can parse documents deeply**, not just as flat text. Structure, layout, entity relationships, and form fields are understood.
- **Document structure signals quality.** Well-organized documents with clear headings, logical layout, and extractable entities are more machine-friendly.

---

## 8) Cloud Content Warehouse

### Official definitions

- **GoogleCloudContentwarehouseV1UpdateDocumentRequest**: "Request message for DocumentService.UpdateDocument."
- **GoogleCloudContentwarehouseV1UpdateDocumentSchemaRequest**: "Request message for DocumentSchemaService.UpdateDocumentSchema."
- **UpdateOptions**: Options for update operations.
- **UpdateRuleSetRequest**: Request for RuleSetService operations.
- **UserInfo**: User information associated with document operations.
- **Value**: Dynamically-typed value (float, int, string, datetime).
- **WeightedSchemaProperty**: Schema property with associated weight/name.

### SEO implications

- **Do not confuse Content Warehouse APIs with ranking recipes.** This is a document management system.
- **WeightedSchemaProperty confirms Google can weight different schema/property types differently** when evaluating documents.

---

## 9) Restrictions and gating

### Official definitions

- **AbuseiamVerdict**: "Verdict against a target." AbuseIAm generates verdicts based on evaluations and sends them to clients for enforcement.
- **AbuseiamUserRestriction**: "Describes restrictions on where the verdict applies. Please use TakedownManager to evaluate this proto."
- **AbuseiamGeoRestriction**: A table of regions and restrictions. **Most-specific rule wins** (e.g., France overrides EU).
- **AbuseiamGeoRestrictionLocale**: Pairs a `location` with a `restriction`. Defaults to "The world" if not specified.
- **AbuseiamAgeRestriction**: Applies if user age is in **[minAgeYears, ageYears)** range.
- **AbuseiamSpecialRestriction**: Predefined restriction from CDD (Content Decisions Database).
- **AbuseiamContentRestriction**: Pair of Verdicts for ProjectR age/geo gating.

### Logical combinators

- **AbuseiamAndRestriction**: Applies if ALL children apply.
- **AbuseiamOrRestriction**: Applies if ANY child applies.
- **AbuseiamNotRestriction**: Applies if the child does NOT apply (one child only).

### Supporting types

- **AbuseiamRegion**: CLDR Region Codes for affected regions.
- **AbuseiamTarget**: `id` and `type` identifying the verdict target.
- **AbuseiamEvaluation**: Backend evaluations that explain verdicts.
- **AbuseiamVerdictRestriction / VerdictRestrictionContext**: Describes context dimensions where verdicts apply.
- **AbuseiamConstantRestriction**: TRUE always applies; FALSE never applies.
- **AbuseiamHash**: Hashes (simhash, attachment hash, etc.) computed on messages.
- **AbuseiamAbuseType**: `id` and `subtype` for abuse classification.

### SEO implications

- **Content visibility can vary by region and audience.** Most-specific-rule-wins means a page might be visible in one country but restricted in another.
- **Age-gating is range-based.** Content can be restricted for specific age bands.
- **Complex restriction logic exists.** AND/OR/NOT combinators mean filtering rules can be layered.
- **Do not assume uniform global visibility.** Serving behavior may be governed by restriction rules invisible in standard SEO tools.

---

## 10) Full API field inventory

For the complete class and field inventory (2,795+ classes, 14,014 attributes), load `reference/12-google-api-field-inventory.md`.

Key class families:

- **Abusiam***: Content restrictions, verdicts, gating (~25 classes)
- **Anchors***: Link/anchor data, source quality, PageRank weights (~4 classes)
- **AppsPeopleOzExternal***: Person/entity modeling, scoring, ACLs (~150+ classes)
- **IndexingDupsLocalized***: Hreflang clusters, localized duplicates (~10 classes)
- **IndexingEmbedded***: Embedded content, embedder info, link info (~6 classes)
- **GoogleCloudContentwarehouse***: Document operations, schemas, rules (~30+ classes)
- **GoogleCloudDocumentai***: Document parsing, pages, entities, layout (~20+ classes)
- **AdsShoppingReporting***: Shopping/offer IDs (~2 classes)
- **AppsDynamite***: Organization info, membership counts (~5 classes)

---

## 11) Leak interpretation rules

### What the leak confirms directionally

- NavBoost and click-based user signals are used in ranking (contradicting years of public denials).
- Chrome/clickstream data feeds the ranking system.
- Long vs short clicks differentiate satisfying vs unsatisfying results.
- Query and destination preference (brand demand) is a powerful ranking lever.
- Whitelists have been used for sensitive topics (Covid, elections).
- Link quality is explicitly tiered (HIGH, MEDIUM, LOW, FRESHDOCS).
- PageRank exists in multiple evolved forms.
- Entities (people, organizations) are modeled with scoring.
- Anchor text is still tracked but may be less dominant than historically assumed.
- Localized clusters can filter near-duplicate market pages.

### Five strategic takeaways (from Fishkin analysis)

1. **Brand matters more than anything else.** Google trends toward ranking powerful, well-known brands over small independents.
2. **E-E-A-T might not matter as directly as some SEOs think.** May be correlated with things Google uses but not a specific ranking field.
3. **Content and links are secondary when navigational intent and user patterns are present.** Consistent user-destination preference can override traditional optimization.
4. **Classic ranking factors (PageRank, anchors, text-matching) have been waning.** But page titles remain important.
5. **For small/medium businesses, SEO is likely to show poor returns until credibility, navigational demand, and reputation are established.**

### Safe interpretation

Use these ideas to improve hypotheses about why brand demand matters, why entity destination preference matters, why localized intent matters, why source-page/link quality matters, why not all indexed pages deserve to exist, why click satisfaction and engagement matter, and why new sites struggle regardless of content quality.

### Unsafe interpretation

Do **not** say:
- "Google definitely uses this exact field in rankings today"
- "This is the exact weight of NavBoost vs links"
- "This one leaked field explains the whole ranking system"
- "The leak proves E-E-A-T is fake"
- "Click manipulation will work" (squashed/unsquashed click detection exists to prevent this)

---

## 12) Practical SEO translation

Use the reference material to improve strategy, not to cosplay certainty.

### Demand and brand
- Build real navigational demand outside of Google search.
- Invest in brand recognition, thought leadership, PR, community, and owned audiences.
- Make your brand the destination users refine toward in query-chaining behavior.

### Content and page quality
- Make page type match query type and SERP reward pattern.
- Optimize for click satisfaction, not just click volume. Long clicks matter.
- Treat site-level quality as aggregated from page-level performance. Prune or improve weak pages.

### Links and authority
- Treat links as unequal by source quality tier, freshness, forwarding type, locality, and anchor text.
- Prioritize context-rich editorial links over mass low-quality links.
- Maintain clean canonical and redirect chains to preserve link equity.
- Reclaim existing high-value links before chasing new low-quality ones.

### Technical and architecture
- Avoid index bloat and thin templating that dilutes site-level quality signals.
- Strengthen internal support structures before blaming external authority gaps.
- Handle market localization carefully with genuine differentiation.
- Keep hreflang clean and aligned with canonical URLs.

### Entities and E-E-A-T
- Keep entity signals (author, organization, brand) coherent across platforms.
- Connect people to organizations to projects with structured data.
- Treat E-E-A-T as correlated with real trust signals, not as a checkbox exercise.

### Measurement and experimentation
- Prefer experiments over dogma when the right answer is uncertain.
- Segment performance by geography and device, reflecting how NavBoost geo-fences data.
- Watch click-through rate and engagement alongside rankings, not just position.
