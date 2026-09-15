# Google API Field Inventory (SEO-Critical Classes)

Extracted from Google API Content Warehouse v0.4.0 (2,795+ classes, 14,014 attributes). This file catalogs the classes and fields most relevant to SEO strategy, ranking analysis, and search visibility diagnosis.

## Table of contents

1. NavBoost and click signals
2. Site quality (NSR/Nsr)
3. Anchor and link systems
4. Indexing and document joining
5. Localized clusters and duplicates
6. Embedded content
7. Snippets and SERP features
8. Entities (WebRef)
9. Knowledge Graph
10. SafeSearch and content classification
11. SpamBrain
12. Quality signals (compressed/composite)
13. Time-based signals
14. Salient terms and topics
15. Sitemap and co-click signals
16. Core Web Vitals and mobile
17. Crawl and fetch
18. Redirect and canonical
19. Restrictions and abuse
20. People/entity modeling

---

## 1) NavBoost and click signals

### QualityNavboostCrapsCrapsClickSignals
Core click signal container from NavBoost. "Craps" is the internal system name.

### QualityNavboostCrapsCrapsData
NavBoost data container holding click patterns, query-level data, and aggregated signals.

### QualityNavboostCrapsCrapsDevice
Device-level click signal segmentation (mobile vs desktop).

### QualityNavboostCrapsFeatureCrapsData
Feature-level NavBoost data for scoring and ranking.

### QualityNavboostCrapsStatsWithWeightsProto
Weighted statistical aggregation of NavBoost click data.

### QualityNavboostGlueVoterTokenBitmapMessage
Token-level bitmap for NavBoost voter signals (click pattern encoding).

### ImageQualityNavboostImageQualityClickSignals
NavBoost click signals specific to image search quality.

### VideoContentSearchNavboostAnchorFeatures
NavBoost features applied to video content anchors.

### ResearchScienceSearchNavboostQueryInfo
NavBoost query information used in science/research search contexts.

### CountryClickDistribution / CountryClickDistributionItem
Geographic distribution of clicks by country. Confirms NavBoost geo-fencing.

**SEO relevance**: These classes confirm NavBoost operates across web, image, and video search. Click signals are weighted, device-segmented, and geographically distributed. The "CrapsClickSignals" class is the core container for per-document click quality data.

---

## 2) Site quality (NSR/Nsr)

### QualityNsrNsrData
Core site-level quality data. NSR likely stands for "Normalized Site Rank" or similar. Fields include cluster uplift, embeddings, and metadata.

### QualityNsrNsrDataClusterUplift
Cluster-level quality boost applied to sites.

### QualityNsrNsrDataEmbedding / EncodedEmbedding
Site-level embedding vectors used in quality scoring.

### QualityNsrNsrDataMetadata
Metadata about the NSR scoring for a site.

### QualityNsrNsrChunksProto / NsrChunksWithSourceInfo
Chunk-level NSR data with source attribution.

### QualityNsrPQData / PQDataSubchunkData
Page Quality data with subchunk granularity.

### QualityNsrExperimentalNsrTeamData / ScoringSignal / WSJData
Experimental scoring signals from the NSR team.

### QualityNsrVersionedFloatSignal / VersionedIntSignal
Versioned quality signals (float and int types) suggesting A/B testing or rollout tracking.

### QualityNsrKetoKetoVersionedData
Keto-versioned quality data (named scoring variant).

**SEO relevance**: NSR is the site-level quality scoring system. It uses embeddings, cluster analysis, versioned signals, and page-quality subchunks. This is likely the system that aggregates page-level signals into site-level quality assessments (what the leak analysis suggests may map to "Panda" behavior). Versioned signals confirm Google tests and iterates on quality scoring.

---

## 3) Anchor and link systems

### Anchors
Container: `anchor` (list), `indexTier`, `targetDocid`, `targetSite`, `targetUrl`, drop counters for homepage/local/nonlocal/redundant/supplemental anchors.

### AnchorsAnchor
Per-link record: `creationDate`, `origText`, `text`, `fragment`, `sourceType` (HIGH/MEDIUM/LOW/FRESHDOCS), `pagerankWeight`, `firstseenDate`, `lastUpdateTimestamp`, `forwardingTypes`, `parallelLinks`, `locality`.

### AnchorsAnchorSource
Source document attributes for a link.

### AnchorsRedundantAnchorInfo
Sampling/dedup for redundant anchors by (domain, text) pair.

### IndexingDocjoinerAnchorSpamInfo
Spam classification data for anchors at the docjoiner stage.

### IndexingDocjoinerAnchorPhraseSpamInfo
Phrase-level spam detection for anchor text.

### IndexingDocjoinerAnchorStatistics / PerDupStats / RedundantAnchorInfo
Statistical analysis of anchors per document, including per-duplicate stats and redundancy handling.

### IndexingDocjoinerAnchorTrustedInfo
Trust scoring for anchors at the docjoiner level.

### RepositoryWebrefSimplifiedAnchor / SimplifiedAnchors
Simplified anchor representations used in the WebRef entity system.

### RepositoryWebrefAnchorIndices
Anchor indices within the entity annotation system.

**SEO relevance**: The anchor system is multi-layered: raw extraction, spam detection, trust scoring, redundancy dedup, and entity-level simplification. Anchor spam is detected at both individual and phrase level. Trust is explicitly scored.

---

## 4) Indexing and document joining

### CompositeDocIndexingInfo
Indexing metadata for composite (merged) documents.

### CompositeDocQualitySignals
Quality signals attached to composite documents.

### CompositeDocPartialUpdateInfoLastFullIndexingInfo
Tracks when a document was last fully indexed vs partially updated.

### CompressedQualitySignals
Compressed representation of quality signals for efficient storage/retrieval.

### IndexingDocjoinerCDocBuildInfo
Build information for the canonical document in docjoiner.

### IndexingDocjoinerDataVersion / VersionInfo
Version tracking for docjoiner data.

### IndexingDocjoinerServingTimeClusterId / ClusterIds
Serving-time cluster assignments for documents.

### IndexingConverterRobotsInfo
Robots.txt parsing and directive storage.

### IndexingConverterShingleFingerprint
Shingle-based fingerprinting for content deduplication.

### IndexingCrawlerIdServingDocumentIdentifier
Document identification at the crawler/serving boundary.

### IndexingPrivacyAccessAccessRequirements
Access requirements and privacy controls for indexed content.

### IndexingBadSSLCertificate
Bad SSL certificate detection during indexing.

**SEO relevance**: Documents go through multiple processing stages: crawl, conversion, docjoining, quality scoring, and serving. The system tracks partial vs full indexing, version history, cluster assignments, and access requirements. Bad SSL is explicitly flagged.

---

## 5) Localized clusters and duplicates

### IndexingDupsLocalizedLocalizedCluster
Top-level localized cluster container.

### IndexingDupsLocalizedLocalizedClusterCluster
Cluster record: `clusterId`, `clusterType`, `filteringEnabled`, `language`, `regionCode`, `urlRegionCode`.

### IndexingDupsLocalizedLocalizedClusterTargetLink / Link / LinkAnnotationSourceInfo / Metadata / TargetDocData
Localized target link with annotation source, metadata, and target document data.

### IndexingDupsLocalizedLocalizedClusterTargetLinkSets
Groups target links by context: `hreflangTargetLink`, `inbodyTargetLink`, `outlinksTargetLink`.

### IndexingDupsLocalizedLocalizedClusterLinkBasedClusterInfo / LinkData / LinkMember
Legacy link-based cluster info with crawl timestamps and annotation sources.

### IndexingDupsComputedLocalizedAlternateNamesLocaleEntry
Computed alternate names for localized content by locale.

**SEO relevance**: Full pipeline for localized duplicate handling. Three input channels (hreflang, inbody, outlinks) feed cluster membership. Filtering can suppress duplicates in SERPs. Legacy and current systems coexist.

---

## 6) Embedded content

### IndexingEmbeddedContentEmbeddedContentInfo
Core embedded content container with docjoins membership.

### IndexingEmbeddedContentEmbeddedLinksInfo
Links found within embedded content.

### IndexingEmbeddedContentEmbedderInfo
Embedder importance and identification.

### IndexingEmbeddedContentFetchHostCount / Counter
Fetch operation counters by host for embedded resources.

### IndexingEmbeddedContentFetchUrlResponseMetadata
Response metadata from fetching embedded URLs.

### IndexingEmbeddedContentLinkInfo
Link information within embedded contexts.

### IndexingEmbeddedContentPageSizeInfo
Page size tracking for embedded content.

### IndexingEmbeddedContentRenderCacheStats / RenderingFetchStats / RenderingOutputMetadata
Rendering pipeline stats for embedded content: cache hits, fetch stats, output metadata.

### IndexingEmbeddedContentSelectionResult
Selection/filtering results for embedded content processing.

**SEO relevance**: Embedded content goes through its own render-fetch-cache pipeline. Embedder importance is tracked. Links within embedded content are treated differently from direct page links.

---

## 7) Snippets and SERP features

### ExtraSnippetInfoResponse / MatchInfo / QuerySubitem / Tidbit / TidbitAnchorInfo
Snippet generation with match info, query decomposition, and anchor-derived tidbits.

### GenericSnippetResponse
Generic snippet container.

### ListSnippetResponse / Row
List-format snippet with row structure.

### LongStructuredSnippet / Entry
Long-form structured snippet with entries.

### MustangReposWwwSnippetsSnippetCandidate / CandidateFeature / RanklabFeatures
Snippet candidates with ranking features for snippet selection.

### MustangSnippetsRenderedToken
Token-level rendering for snippets.

### QualityPreviewChosenSnippetInfo / TidbitInfo
Final selected snippet with tidbit details.

### QualityPreviewRanklabSnippet / RanklabTitle
Ranking-lab features for snippet and title evaluation.

### QualityPreviewSnippetBrainFeatures / DocumentFeatures / ExperimentalFeatures / QualityFeatures / QueryFeatures / QueryTermCoverageFeatures / RadishFeatures
Multi-dimensional snippet scoring: brain model, document quality, query coverage, and experimental features.

### QualitySnippetsTruncationSnippetBoldedRange / Position
Snippet truncation and bold-range positioning.

### SnippetExtraInfoSnippetCandidateInfo / ExtendedSnippet / ScoringInfo / SnippetsBrainModelInfo
Extended snippet scoring with brain-model integration.

### SnippetsLeadingtextLeadingTextAnnotation / Piece / Info
Leading text annotation for snippet generation.

**SEO relevance**: Snippet selection is a multi-stage ranking problem with its own ML models ("SnippetBrain"). Query term coverage, document quality, anchor tidbits, and ranking features all influence which snippet appears. Title evaluation has its own ranklab features.

---

## 8) Entities (WebRef)

### RepositoryWebrefWebrefEntity / EntityId / EntityRelationship
Core entity with ID and relationships.

### RepositoryWebrefEntityAnnotations
Entity annotations on documents.

### RepositoryWebrefEntityScores / DetailedEntityScores
Entity-level scoring and detailed score breakdowns.

### RepositoryWebrefMention / MentionScores / DetailedMentionScores / MentionComponent / CompoundMention
Mentions of entities within documents with scoring.

### RepositoryWebrefEntityJoin
Join/merge operations for entities across sources.

### RepositoryWebrefGlobalNameInfo / GlobalLinkInfo
Global name and link information for entities.

### RepositoryWebrefDocumentMetadata
Document-level metadata within the entity system.

### RepositoryWebrefCategoryAnnotation / CategoryInfo
Category classification for entities.

### RepositoryWebrefLatentEntities / LatentEntity
Latent (implicit/inferred) entity detection.

### RepositoryWebrefTripleAnnotation / TripleAnnotations / TripleMention
Knowledge-graph-style triple annotations on documents.

### RepositoryWebrefReferencePageScores
Scores for entity reference pages.

### RepositoryWebrefProductMetadata
Product-specific entity metadata.

### RepositoryWebrefPersonalizationContextOutput / Outputs
Personalization context for entity interpretation.

### RepositoryWebrefAnnotationRatings
Quality ratings for entity annotations.

### RepositoryWebrefBookEditionMetadata
Book edition entity metadata.

### RepositoryWebrefFreebaseType / OysterType
Entity typing from Freebase and Oyster systems.

**SEO relevance**: WebRef is Google's core entity understanding system. Entities are scored, categorized, typed, joined across sources, and annotated on documents. Latent entity detection means Google can infer entities even without explicit mentions. Entity scores influence document relevance. Reference page scores indicate which pages Google considers authoritative for an entity.

---

## 9) Knowledge Graph

### KnowledgeGraphTriple / TripleObj / TripleObjProto / TripleProvenance
Knowledge Graph triples with object values and provenance tracking.

### KnowledgeGraphQualifier / QualifierSet
Qualifiers on KG triples (time, context, conditions).

### KnowledgeGraphNestedStruct / PredicateObjs
Nested structures within KG data.

### KnowledgeGraphDateTimeProto
Date/time representation in KG.

### KnowledgeAnswersEntityType
Entity types within the answers system.

### KnowledgeAnswersIntentQueryFunctionCall / FunctionCallSignals
Intent-query function calls with signals for answer generation.

**SEO relevance**: The Knowledge Graph stores structured triples with provenance. Qualifiers add context to facts. The answers system interprets queries as function calls against entity data. Building structured, verifiable entity data increases the chance of Knowledge Panel and featured snippet inclusion.

---

## 10) SafeSearch and content classification

### ClassifierPornClassifierData / Classification
Porn classification data and results.

### ClassifierPornDocumentData
Document-level porn classification.

### ClassifierPornQueryClassifierOutput / MultiLabelClassifierOutput
Query-level porn classification (single and multi-label).

### ClassifierPornQueryStats
Statistics on porn-query classification.

### ClassifierPornReferrerCounts
Referrer analysis for porn classification.

### ClassifierPornSiteData / VersionedScore
Site-level porn classification with versioned scores.

### ClassifierPornSiteViolenceStats
Violence statistics at the site level.

### SafesearchImageOffensiveAnnotation
Image-level offensive content annotation.

### SafesearchInternalImageSignals
Internal signals for SafeSearch image classification.

### SafesearchVideoClassifierOutput / VideoContentSignals / MultiLabelClassificationInfo
Video SafeSearch classification with multi-label output.

### ImageSafesearchContentBrainPornAnnotation / OCRAnnotation / OffensiveSymbolDetection
Image-level SafeSearch using brain models, OCR, and symbol detection.

### PornFlagData
Porn flag data container.

**SEO relevance**: SafeSearch operates at document, site, query, image, and video levels. Site-level scores are versioned (tracked over time). Referrer patterns feed classification. OCR and symbol detection mean embedded text in images is analyzed. Sites with even partial adult or violent content risk site-level classification that affects all pages.

---

## 11) SpamBrain

### SpamBrainData
Core SpamBrain data container.

### SpamBrainScore
SpamBrain scoring output.

### SpamCookbookAction
Spam action recipes/rules.

### SpamMuppetjoinsMuppetSignals
Spam signals from the Muppet joins system.

**SEO relevance**: SpamBrain is Google's ML-based spam detection system. It produces scores and triggers actions. The "Cookbook" actions suggest rule-based responses to detected spam patterns. SpamBrain operates alongside older spam systems.

---

## 12) Quality signals (compressed/composite)

### CompressedQualitySignals
Compressed quality signal representation for efficient processing.

### CompositeDocQualitySignals
Quality signals on composite (merged/canonical) documents.

### QualityAuthorityTopicEmbeddingsVersionedItem
Topical authority embeddings with versioning. Confirms topic-level authority scoring exists.

### QualityCopiaFireflySiteSignal
Copia/Firefly site-level signal.

### QualityRankembedMustangMustangRankEmbedInfo / CompressedEmbedding
Rank-level embeddings used in Mustang (serving system) with compression.

### QualityLabelsGoogleLabelData / Label / LabelProvider
Google-applied labels on content with provider attribution.

### QualityDniDocPreviewRestrictions / ExtendedNewsPreviews
Document preview restrictions and extended news preview data.

### QualityFringeFringeQueryPriorPerDocData
Fringe query classification per document.

### WeboftrustLiveResultDocBoostData
Web of trust live result boosting data.

**SEO relevance**: Quality signals are compressed and attached at multiple levels. Topic authority has versioned embeddings. Google applies its own labels to content. Fringe query handling has per-document data. Web of trust contributes to live result boosting.

---

## 13) Time-based signals

### QualityTimebasedLastSignificantUpdate / Adjustments
Tracks the last significant update to a page with adjustment logic.

### QualityTimebasedDateUnreliability
Measures how unreliable/untrustworthy a page's date signal is.

### QualityTimebasedPageType
Page type classification for time-based scoring.

### QualityTimebasedSyntacticDate / DateRange / Position
Syntactic (text-extracted) date detection with range and position in document.

### QualityTimebasedPetacatDateUnreliability
Petacat-system date unreliability scoring.

**SEO relevance**: Google distinguishes "last significant update" from raw modification dates. Date reliability is explicitly scored. Fake or misleading dates are detectable. Page type influences how time-based signals are applied.

---

## 14) Salient terms and topics

### QualitySalientTermsSalientTerm / SalientTermSet
Salient (important/characteristic) terms extracted from documents.

### QualitySalientTermsDocData
Document-level salient term data.

### QualitySalientTermsSignalData / SignalTermData
Signal-level salient term analysis.

### QualitySalientCountriesSalientCountry / SalientCountrySet
Geographic salience: which countries a document is most relevant to.

**SEO relevance**: Google identifies characteristic terms for each document, not just keyword matches. Salient country detection means geographic relevance is inferred from content, not just hreflang or domain. Writing content that uses the right characteristic terminology strengthens topical relevance.

---

## 15) Sitemap and co-click signals

### QualitySitemapTarget / TargetGroup / TopURL / TwoLevelTarget
Sitemap-derived targets and top URLs.

### QualitySitemapBreadcrumbTarget / BreadcrumbTargetDoc
Breadcrumb-based site structure targets.

### QualitySitemapCoClickTarget / CoClickTargetDoc / CoClickByLocale
Co-click targets: pages that users commonly click together, segmented by locale.

### QualitySitemapScoringSignals / SporcSignals
Scoring and Sporc signals derived from sitemap/co-click data.

### QualitySitemapSubresult / SubresultList
Sub-results generated from sitemap structure.

**SEO relevance**: Google uses co-click patterns to understand site structure and page relationships. Breadcrumb structure feeds into target identification. Co-click data is locale-segmented. This is another click-based signal feeding site understanding beyond NavBoost.

---

## 16) Core Web Vitals and mobile

### IndexingMobileVoltCoreWebVitals
Core Web Vitals data from the Volt system.

### IndexingMobileVoltVoltPerDocData
Per-document mobile performance data.

### IndexingMobileInterstitialsProtoDesktopInterstitials / Details / BasicInfo
Desktop interstitial detection with details.

### MobilePerDocData
General mobile per-document data.

**SEO relevance**: Core Web Vitals are stored per-document. Interstitials are explicitly detected and classified. Mobile performance data is separate from desktop.

---

## 17) Crawl and fetch

### CrawlerChangerateUrlChange / UrlChangerate / UrlHistory / UrlVersion
URL change rate tracking: how often content changes, version history, and change patterns.

### TrawlerCrawlTimes
Crawl timing data.

### TrawlerFetchReplyDataCrawlDates / Redirects
Fetch reply data including crawl dates and redirect information.

### ImageMoosedogCrawlState
Image-specific crawl state tracking.

### HtmlrenderWebkitHeadlessProtoRedirectEvent / RedirectHop
Headless webkit rendering redirect tracking.

**SEO relevance**: Google tracks content change rates at the URL level to optimize crawl scheduling. Redirect chains are recorded during both crawl and render phases. Image crawling has its own state tracking.

---

## 18) Redirect and canonical

### IndexingConverterRawRedirectInfo
Raw redirect information from the converter stage.

### IndexingConverterRedirectChain / RedirectChainHop
Full redirect chain with per-hop data.

### IndexingConverterRedirectParams
Redirect parameters and configuration.

### RepositoryWebrefForwardingUrls
Forwarding/canonical URL data in the entity system.

### RepositoryWebrefSimplifiedForwardingDup
Simplified forwarding duplicate records.

**SEO relevance**: Redirect chains are stored hop-by-hop. The entity system tracks forwarding URLs. Redirect handling at the indexing stage is separate from the entity/canonicalization stage. Clean redirect chains preserve more signal than messy ones.

---

## 19) Restrictions and abuse

### AbuseiamVerdict / VerdictRestriction / VerdictRestrictionContext
Verdicts with restriction dimensions.

### AbuseiamUserRestriction / GeoRestriction / AgeRestriction / SpecialRestriction / ContentRestriction
Restriction types: user, geographic, age, special, content.

### AbuseiamAndRestriction / OrRestriction / NotRestriction / ConstantRestriction
Boolean logic for combining restrictions.

### AbuseiamEvaluation / Target / Region / Hash / AbuseType
Evaluation pipeline: target identification, region coding, content hashing, abuse classification.

**SEO relevance**: Full restriction pipeline from evaluation through verdict to enforcement, with Boolean logic for complex rules. Content can be restricted by geography, age, abuse type, or combinations thereof.

---

## 20) People/entity modeling

### AppsPeopleOzExternalMergedpeopleapiPerson
Merged-person combining contacts and profiles.

### PersonFieldMetadata / PersonMetadata / PersonMetadataScoringInfo
Field-level and entity-level metadata with scoring (rawMatchQualityScore).

### Organization / OrganizationAssignment / OrganizationProject
Organization entities with role assignments and project connections.

### FieldAcl / AclEntry / AclEntryScope
Access control at the field level.

### MapsProfile / MapsExtendedData
Maps-specific profile and extended data.

### SocialGraphApiProtoSearchProfileEntity
Social graph profile entities used in search.

### SocialDiscoveryExternalEntityKey
External entity keys for social discovery.

**SEO relevance**: People are modeled as merged entities from multiple sources with explicit scoring. Organization-project relationships are structured. Maps profiles feed the entity model. Social graph data connects to search profiles.

---

## Class family summary

| Family | Approx classes | SEO domain |
|--------|---------------|------------|
| QualityNavboost* | 8 | Click signals, device/geo segmentation |
| QualityNsr* | 17 | Site quality scoring, embeddings |
| Anchors* / DocjoinerAnchor* | 10 | Link quality, spam, trust, dedup |
| IndexingDupsLocalized* | 14 | Hreflang, localized duplicates |
| IndexingEmbedded* | 17 | Embedded content, render pipeline |
| Snippet* / QualityPreview* | 25+ | Snippet selection, title ranking |
| RepositoryWebref* | 90+ | Entity understanding, scoring, categories |
| KnowledgeGraph* / KnowledgeAnswers* | 80+ | KG triples, query interpretation |
| ClassifierPorn* / Safesearch* | 15 | Content safety classification |
| SpamBrain* / Spam* | 4 | ML spam detection |
| QualityTimebased* | 8 | Freshness, date reliability |
| QualitySalientTerms* / Countries* | 7 | Topical relevance, geo salience |
| QualitySitemap* | 15 | Co-click, breadcrumb, sub-results |
| IndexingMobile* / MobilePerDoc | 5 | CWV, interstitials, mobile perf |
| Crawler* / Trawler* | 8 | Crawl rate, fetch data |
| IndexingConverter* (redirect) | 5 | Redirect chains, canonicalization |
| Abusiam* | 20+ | Content restrictions, gating |
| AppsPeopleOz* | 150+ | People/org entity modeling |
