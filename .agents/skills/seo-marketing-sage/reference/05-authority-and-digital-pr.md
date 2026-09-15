# Authority and Digital PR Reference

Use this file for link earning, mention generation, trust-building assets, reclamation, and authority-gap reduction.

## 1) Authority strategy principles

Default to white-hat, editorial, and product-aware methods:
- original data or research
- useful tools, templates, calculators
- strong founder/SME opinions
- customer stories and proof
- partnerships and ecosystems
- integration pages and resource pages
- PR angles tied to real insight, not fluff

## 2) Evaluate the authority gap correctly

A page/site can fail for authority reasons when:
- relevance is strong but rankings ceiling out
- competitors have stronger link/mention support
- your page lacks proof or trust
- there is little branded search or brand recall in the category

Do not chase raw domain counts blindly. Relevance, editorial placement, traffic potential, and destination choice matter more.

## 3) Backlink and mention evaluation

### Google systems context for link quality

The leaked API documentation confirms that Google classifies linking pages into discrete quality tiers via the `sourceType` field on anchor records:

- **TYPE_HIGH_QUALITY**: Highest tier. Links from these sources carry the most weight.
- **TYPE_MEDIUM_QUALITY**: Middle tier.
- **TYPE_LOW_QUALITY**: Lowest tier.
- **TYPE_FRESHDOCS**: Treated as equivalent to HIGH for anchor-importance and duplicate-removal.

Additional link-level signals from the API: `pagerankWeight` (numeric weight for PageRanker), `locality` (contextual relevance), `parallelLinks` (other links from same page, potential dilution), `forwardingTypes` (redirect/canonical behavior affecting equity transfer), and `firstseenDate`/`lastUpdateTimestamp` (age and freshness).

Redundant anchor dedup operates at the (domain, text) pair level: multiple links from the same domain with the same anchor text are consolidated, not multiplied.

For full field-level detail, see `reference/09-google-systems-reference.md`, section 3. For the complete anchor/link class inventory, see `reference/12-google-api-field-inventory.md`, section 3.

### Evaluation criteria

Assess:
- topic relevance
- editorial context
- source quality tier (high > medium > low)
- link placement and surrounding content
- anchor naturalness and diversity
- destination-page fit
- referral potential
- diversity across source types and domains
- whether the mention supports brand/entity strength even without a followed link
- locality (contextual relatedness between source and target)
- redirect/canonical cleanliness (forwarding behavior affects equity transfer)
- parallel link dilution (many links from one page may each carry less weight)

## 4) Campaign types

### Reclamation
- unlinked mentions
- broken links
- image attribution
- redirect clean-up
- outdated references
- internal mis-links

### Product-led
- free tools
- templates
- calculators
- public datasets
- stats pages
- integration/partner assets

### Editorial / PR-led
- proprietary research
- trend commentary
- founder voice
- contrarian frameworks
- local data angles
- industry benchmark reports

### Ecosystem-led
- partner directories
- marketplaces
- associations
- certifications
- events and speaking
- expert roundups where genuinely additive

## 5) What to specify in recommendations

For each recommendation, include:
- target page
- target audience for the mention/link
- pitch angle
- asset needed
- owner
- timeline
- success metric

## 6) Guardrails

Avoid recommending:
- paid link schemes
- PBNs
- mass guest post farms
- irrelevant directory spam
- manipulative anchor campaigns
- outreach with no legitimate value

## 7) Relationship to rankings

Treat authority work as a support layer that can:
- raise the ceiling for commercial pages
- improve trust for YMYL or high-stakes queries
- accelerate index discovery of new assets
- reinforce brand/entity prominence
- make internal linking harder-hitting by strengthening source sections
- contribute to host-level quality signals (NavBoost aggregates engagement at the domain level; a stronger brand profile can lift the floor for the entire site)
- improve destination preference (brand demand driven by PR, mentions, and thought leadership feeds NavBoost-style click patterns)

### What the leak reinforces about authority strategy

- **Quality over quantity is structural, not just advice.** Google's sourceType tiers mean that one HIGH-quality editorial link is categorically different from dozens of LOW-quality links. This is a discrete classification, not a continuum.
- **Redundant anchor links from one domain are consolidated.** Do not chase volume from a single source.
- **Contextual relevance (locality) is a tracked field.** Topically related links from related sites carry more signal than random placements.
- **Brand demand is an authority multiplier.** Authority work that also drives branded search behavior compounds: it improves link signals and NavBoost signals simultaneously.
