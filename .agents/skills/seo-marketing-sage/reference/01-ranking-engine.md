# Ranking Engine Reference

Use this file for ranking drops, winner/loser diagnosis, SERP interpretation, signal prioritization, and demand creation strategy.

## 1) Ranking diagnosis model

Treat rankings as the outcome of interacting systems, not one magic factor.

Work through this stack:

1. **Intent fit**  
   Does the page type match what the SERP is rewarding?

2. **Topical and entity fit**  
   Does the page clearly satisfy the query and related entities, subtopics, and use cases?

3. **Architecture and internal support**  
   Is the page easy to discover, well-linked, and part of a coherent neighborhood?

4. **Authority and trust support**  
   Does the page/site have enough external validation to compete?

5. **Demand and brand pull**  
   Is the brand or destination already wanted by searchers for this topic?

6. **Freshness / update relevance**  
   Is the query freshness-sensitive, and is the page current enough?

7. **Localization / device / format fit**  
   Does the SERP prefer local, mobile, video, forum, docs, product, or comparison patterns?

8. **Quality / anti-spam filters**  
   Could the page or site be held back by thinness, duplication, templating, UX mismatch, or trust deficits?

## 2) Query classes

Classify the query before recommending anything:

- navigational
- brand-adjacent / entity-led
- transactional
- commercial investigation
- informational
- local / geo-modified
- support / problem-solving
- mixed intent

When a query is brand-adjacent or navigation-heavy, classic content optimization alone often underperforms. Brand demand, entity clarity, and user destination preference matter more.

## 3) What the SERP is teaching you

Read the winner pattern before prescribing.

Check:
- dominant page type
- dominant content format
- commercial vs informational mix
- whether forums, videos, tools, docs, or marketplaces dominate
- whether the SERP is entity-heavy
- whether results cluster by locale or subtopic
- whether titles emphasize comparisons, pricing, location, templates, or definitions

Then answer:
- what page archetype is winning?
- what proof or trust layer is common?
- what depth or UX pattern is common?
- what information gain is still missing?

## 4) Demand creation and ranking leverage

Do not reduce rankings to links + keywords. In many categories, off-SERP demand materially changes outcomes.

### Why this matters (Google systems context)

The leaked Google API documentation and DOJ testimony confirm that NavBoost, Google's click-based ranking system, is one of the most powerful ranking signals in the system. NavBoost operates at both the page level and the host level, meaning site-wide engagement patterns can produce boosts or demotions. Key mechanics:

- **Destination preference**: When users search a general term, fail to find a specific brand, then refine their query to that brand and click, the brand gains ranking strength for the original term.
- **Long clicks vs short clicks**: Engaged visits signal satisfaction. Quick bounces signal failure. These are tracked and scored.
- **Host-level quality**: NavBoost aggregates click quality at the domain level for site-wide evaluation. This is speculated to relate to what was once called "Panda."
- **Geo-fenced click data**: Click signals are segmented by country, state/province, and device type. Regional performance matters independently.
- **Brand as ranking input**: The trajectory in Google's systems is toward rewarding established, recognized brands. Branded search demand is not a vanity metric; it is an upstream ranking signal.

For full definitions and field-level detail, see `reference/09-google-systems-reference.md`, section 2 (NavBoost) and section 3 (Links/Anchors). For the complete API field inventory, see `reference/12-google-api-field-inventory.md`.

### Demand levers

Use these when intent patterns matter:
- branded search demand
- thought leadership and PR
- community distribution
- owned audience growth
- partner ecosystems
- category education that makes your brand the remembered destination
- remarketing and multi-touch campaigns that increase direct and brand recall
- click satisfaction optimization (fulfilling the title/snippet promise to earn long clicks)
- off-SERP brand mentions that drive navigational search behavior

This does not replace SEO fundamentals. It changes how hard those fundamentals can work.

## 5) Ranking drop framework

When a page or section drops, classify the drop:

### A. Intent mismatch
Symptoms:
- impressions hold, rankings soften, CTR falls
- competitors with different page types win
- page covers the topic but not the use case the SERP now prefers

Fixes:
- change page type or structure
- sharpen title/H1/snippet promise
- add missing sub-intents
- split mixed-intent pages

### B. Authority / trust gap
Symptoms:
- strong relevance but ceilinged positions
- weak link or mention profile
- thin proof, reviews, case studies, or brand signals

Fixes:
- add proof layers
- improve internal support from strong pages
- support with PR / mention campaigns
- build better destination assets

### C. Architecture / internal support gap
Symptoms:
- page exists but has weak internal paths
- orphaned or deep pages
- weak hubs or service/category support

Fixes:
- hubs, child pages, and contextual links
- navigation refinement
- anchor theme consistency
- reduce crawl depth

### D. Technical interference
Symptoms:
- sudden visibility drop after template changes, redesign, migrations, JS shifts, noindex/canonical issues

Fixes:
- validate crawlability, canonicals, redirects, render state, indexing, and structured data

### E. Freshness / staleness
Symptoms:
- losses on recency-sensitive queries
- dated screenshots, examples, or pricing
- SERP shows recently updated content

Fixes:
- refresh content
- add new proof/examples
- rework title/date signals where appropriate

### F. Quality / duplication drag
Symptoms:
- lots of similar pages compete internally
- city/service boilerplate
- low-value pages swell index count

Fixes:
- consolidate
- differentiate
- noindex or canonical low-value variants
- improve information gain

### G. Engagement / click satisfaction gap
Symptoms:
- page ranks but CTR or dwell time is declining
- high impressions, low clicks (SERP presentation problem)
- users click but bounce quickly (content delivery problem)
- brand search volume is flat or declining relative to category growth
- competitors with stronger brand recognition are displacing you

Fixes:
- improve title/meta description to better match user intent and set accurate expectations
- restructure content to deliver the answer faster (above-fold, answer-first)
- improve page experience (load speed, layout stability, mobile UX)
- build off-SERP brand demand through PR, community, advertising, and thought leadership
- audit whether the page type still matches what the SERP rewards (format drift)
- consider whether site-level engagement drag is pulling down individual page performance

Context: NavBoost and click-based signals operate at both the page and host level. A site with consistently poor engagement can be demoted holistically. See `reference/09-google-systems-reference.md`, section 2 for full NavBoost detail. For the underlying API classes (QualityNavboostCraps*, CountryClickDistribution), see `reference/12-google-api-field-inventory.md`, section 1.

## 6) Entity and page mapping

For head terms, explicitly map:
- target entity/entities
- page entity
- supporting entities
- competitor entities
- proof entities (customers, locations, integrations, authors, certifications, awards)

If the page cannot clearly win as the best destination for the underlying entity/problem, create or reposition the right page.

## 7) Experiment menu

When the right move is uncertain, propose tests such as:
- page-type swap or restructure
- title and snippet repositioning
- proof layer addition
- internal-link sprint
- consolidation of overlapping pages
- deeper comparison content
- adding calculators, templates, or tools
- location or persona specialization
- authority campaign support for a specific cluster

## 8) Output pattern for ranking investigations

Use this structure:

- current symptom
- what likely changed
- strongest competing interpretation
- most likely root cause class
- top 3 fixes
- quickest validation step
- 30-day metrics to watch

## 9) Guardrails

- Do not claim exact ranking weights.
- Do not pretend any internal Google field is a direct recipe.
- Translate uncertainty into experiments, not fake certainty.
