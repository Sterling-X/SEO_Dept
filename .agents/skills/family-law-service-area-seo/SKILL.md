---
name: family-law-service-area-seo
description: Analyzes family law firm service-area hubs and city/county pages (hub-and-spoke) to diagnose local SEO signals, avoid practice-page cannibalization, and output a reusable blueprint + templates. Also produces publication-ready service-area hub and child page copy as DOCX files. Use this skill whenever the user asks to audit, build, write, or produce a geographic service-area page (state hub, county page, city page) for any family law firm, or when reverse-engineering competitor location page strategies. Trigger on requests mentioning service area pages, location pages, areas we serve, city pages, county pages, geo pages, or hub-and-spoke geographic architecture. Also trigger when the user says 'build the service area hub', 'write the Colorado page', 'create city pages', or any similar geographic page production request. Do NOT use for practice area pages (use family-law-service-pages instead) or blog content (use cluster-blog-writer instead).
---

# Family Law Service Area SEO

## Scope

This skill covers two modes:

1. **Analysis Mode** -- Reverse-engineer competitor service-area pages, diagnose local SEO signals, identify cannibalization risks, and output a reusable blueprint.
2. **Production Mode** -- Build publication-ready service-area hub pages and child pages (county/city) as DOCX files.

This skill is **only** for:
- Family law firms (divorce & family law attorneys, family law-focused mediation practices)
- Service-area SEO involving state / county / city coverage pages

This skill is **not** for:
- Other industries (home services, medical, ecommerce, etc.)
- Practice area pages (use family-law-service-pages skill instead)
- Blog content (use cluster-blog-writer skill instead)
- "Fake location" strategies (implying staffed offices where none exist)

> Guardrail: Provide SEO analysis and content strategy, not legal advice. Do not claim outcomes.

---

## Core Principle: What a Service-Area Page Is and Is Not

### What a service-area page IS for

A service-area page (state hub, county page, city page) exists to:
- Win **service + geo** searches ("divorce lawyer Denver," "family law attorney El Paso County, CO")
- Demonstrate **local credibility** (office proximity, court knowledge, county-specific proof)
- **Route users to practice-area pages** for topical depth
- Convert local-intent searchers (call / consult / book)

### What a service-area page is NOT for

A service-area page is NOT a place to explain legal concepts. It is not a mini practice area page. It does not teach the reader what child support is, how equitable distribution works, or what factors courts consider for custody. That content belongs on the canonical practice-area pages and ONLY on those pages.

### The Content Weight Rule (mandatory)

Every service-area page must follow this approximate content distribution:

- **60-70% geographic substance** -- office-to-court mapping, courthouse references, counties and communities served, local proof (reviews with location attribution, attorney presence by region), local logistics
- **10-15% practice-area routing** -- a tight service list that links to canonical practice pages. No explainers. No process breakdowns. No legal education.
- **15-25% conversion and trust** -- CTAs, differentiators grounded in local knowledge, "what to expect when you call," FAQs localized to geographic and process questions

If the practice-area content on a service-area page exceeds the geographic content, the page is broken. Stop writing and restructure.

### Anti-Cannibalization Rules (mandatory)

These are not suggestions. Violating any of these creates a page that competes with the firm's own practice-area pages for the same keywords.

1. **Primary keyword for every service-area page = service + geo.** Not the practice area alone.
2. **Practice area routing is a list, not a content section.** Each practice area gets ONE sentence max and a link. No H3 subsections per practice area. No statute references. No "how it works" content.
3. **No legal education on service-area pages.** If a sentence explains what a court considers, how a formula works, or what a legal process involves, it belongs on the practice-area page. Delete it from the service-area page and link to where it lives.
4. **The page's unique value comes from geography, not topic.** Every section should contain something a practice-area page would never carry: courthouse names, county references, office proximity, community lists, local logistics, geo-attributed reviews.
5. **Internal links from service-area pages to practice pages use service-only anchors.** No geo in the anchor text. Varied and natural, not "Learn about X" repeated for every practice area.
6. **Internal links from practice pages to service-area pages use geo anchors.** "Family law attorneys in El Paso County" or "Our Denver office."

### The "Learn About" Trap (explicitly banned)

Do not use "Learn about our [practice area]" or "Learn more about [topic]" as anchor text. This pattern:
- Sounds generic and template-driven
- Becomes visually and structurally repetitive when used across 6-8 practice areas
- Fails to differentiate the destination pages from each other
- Signals to both users and search engines that the content is boilerplate

Instead, use natural, varied, contextual anchors that describe what the reader will find:
- "See how we handle divorce in Colorado"
- "How parental responsibilities are decided"
- "What Colorado courts consider for maintenance"
- "Child support in Colorado"

Every anchor should be different. Every anchor should read like a natural sentence ending, not a navigation label.

### Single-Placement Rule (revised per colorado-service-area-hub-v9 canonical)

Internal destination URLs appear in tightly bounded placements. The hard rule is no body-prose duplication of links that already live in catalog modules; the soft pattern accommodates the hub's actual multi-CTA structure.

**Allowed placements per URL class:**

- **Practice-area URLs** (e.g., `/divorce/`, `/child-custody/`): appear in **two** places maximum: once in the "Family Law We Handle" catalog and once in the "Related Pages" footer. Do not link a practice page from body prose, FAQ answers, or any other module.
- **City and county URLs** (e.g., `/colorado/locations/denver/`, `/colorado/counties/denver-county/`): appear **once** per page, in the Communities and Counties Served catalog. Do not duplicate in body prose.
- **CTA destination URLs** (`/contact-us/` and equivalent scheduling endpoints): may appear up to **four** times: typically across the above-the-fold inline CTA paragraph (P3), the second inline CTA at the end of the Why Trust section ("Ready to talk?"), the third inline CTA in the closing section, and the Related Pages footer. More than four uses signals over-CTA-stuffing. All four placements are inline; never as standalone banners.
- **Statute citations** (e.g., `leg.colorado.gov/...`): appear once in body as a numeric citation marker (`[1]`) and once in the Sources entry. That dual placement is the standard footnote convention and is exempt from the rule.
- **All other internal URLs** (attorney bio hub, reviews, parent state hub): appear **once**, in the Related Pages footer or at the natural single placement.

**Banned patterns regardless of count:**
- Linking the same destination from body prose AND a catalog module
- Tag-on "See our X page" or "Learn more at" links anywhere
- Multi-link clusters in body sentences outside a catalog row

**Validator behavior:** the pre-delivery validator hard-fails on five or more occurrences of any URL and warns on two to four (which should be spot-checked against this rule). Statute body+Sources pairs are exempt.

### Lead-In Requirement (Hard Requirement)

In non-catalog body prose (above-the-fold paragraphs, "Why [Geo] Families Trust" sections, FAQ answers, mid-page narrative), every link must be embedded inside a sentence whose meaning is incomplete without the linked topic. The link is not tagged on after the thought is already finished.

GOOD: "Custody disputes in [County] go before judges in the [Judicial District] court at [Courthouse]; we [practice in that courtroom regularly](url)."
- The link is part of the sentence's noun phrase.

BAD: "Custody disputes in [County] go before judges in the [Judicial District] court at [Courthouse]. See our [practice area page](url)."
- The link is a tagged-on "see also."

**Catalog modules are exempt** from the Lead-In Requirement because they are structurally lists. In a catalog row, the descriptor sentence (under 15 words) following the linked anchor performs the same function: it tells the reader what the linked page covers. Each catalog descriptor should be specific and unique, not "Learn about [topic]" boilerplate.

### Banned Linking Patterns

- "See our [topic] page" sentences appended to a paragraph in body prose
- "Learn more at [link]" or "Click here for [link]" tag-ons (this overlaps with the Learn About Trap, restated for completeness)
- Multi-link clusters (two or more links in the same body sentence) outside a catalog module
- Duplicate links across catalog modules and body prose for the same destination
- Any link whose anchor text is the bare URL or a generic phrase like "click here," "this page," or "learn more"

---

## Mode Routing

If the user provides competitor URLs to analyze, use **Analysis Mode** (Steps 1-6 below).
If the user asks to build, write, or produce a service-area page, use **Production Mode** (see Production Mode section below).
If the user asks for both, analyze first, then produce.

---

## Analysis Mode

### Inputs (Required + Optional)

**Required URLs** (do not start analysis until all 3 are present):
- HUB_URL_1: {HUB_URL_1}
- HUB_URL_2: {HUB_URL_2}
- CHILD_URL: {CHILD_URL}

**Strongly recommended context** (if provided, use it; if not, infer cautiously and label as inferred):
- CLIENT_NAME: {CLIENT_NAME}
- STATE(S) SERVED: {STATES_SERVED}
- PRIMARY PRACTICE AREAS (3-8)
- PRIMARY PRACTICE-AREA PAGE URLS (canonical): {PRACTICE_PAGE_URLS}
- OFFICES (addresses + cities): {OFFICE_LIST}
- CONVERSION GOAL: {CTA_GOAL} (call / form / book consult)
- TARGET SERVICE-AREA LIST: {TARGET_GEOS}

### Evidence Rules (No Hallucinations)

- Only reference on-page elements you can observe.
- If schema, maps, or NAP are not visible, state: "Not observed in the provided page content."
- Do not claim pages "rank" unless ranking data is provided.
- If content appears templated/duplicated, explicitly diagnose it and propose scalable fixes.

### Step 1 -- Individual Page Analysis (repeat for EACH URL)

For each URL, produce:

1. **Page Purpose and Intent** -- primary keyword, intent alignment, funnel position, cannibalization risk
2. **Content Structure** -- title/H1, heading hierarchy, section breakdown, depth vs gaps, semantic entities (cities, courts, landmarks)
3. **Content Weight Assessment** -- what percentage of the page is geographic substance vs practice-area content vs conversion/trust? Flag if practice-area content outweighs geographic content.
4. **Local SEO Signals** -- geo modifier placement, service-area mentions, NAP, office-vs-serving clarity, maps/schema, local proof
5. **Internal Linking Strategy** -- hub/spoke links, practice-area page links, anchor text quality, breadcrumbs
6. **Topical Authority Signals** -- breadth vs depth match for local intent, E-E-A-T signals for law
7. **Conversion and UX** -- above-fold CTA, contact options, trust placement, readability, friction

End each page's section with:
- Why it is structured to rank (based on observable elements)
- Top 5 opportunities
- Priority fixes: P1 (high impact/low effort), P2, P3

### Step 2 -- Hub Page Strategy Comparison

Compare structural similarities/differences, taxonomy depth, geo organization, authority distribution, content-uniqueness patterns, UX quality.

### Step 3 -- Child/Hub Relationship Analysis

Evaluate content uniqueness vs duplication, localization depth, keyword differentiation, internal linking hierarchy, whether it strengthens or weakens overall architecture.

### Step 4 -- What They Are Doing Right

Extract repeatable patterns: crawlable directory structures, nearest-office blocks, service+geo anchors, conversion modules, trust modules, court/local proof.

### Step 5 -- What They Are Doing Wrong

Identify: thin/redundant content, weak localization, cannibalization (test specifically for practice-area content weight exceeding geographic content weight), poor internal linking, mismatched supporting content.

### Step 6 -- Strategic Blueprint Output

Deliver reusable blueprint per the templates in the Production Mode section below.

### Analysis Output Format

1. Executive Summary (10 bullets max)
2. Individual Page Analysis (per URL)
3. Hub Comparison
4. Child/Hub Relationship
5. What They Are Doing Right
6. What They Are Doing Wrong
7. Blueprint (hub structure, child structure, linking model, templates, do/don't)
8. Priority Roadmap (P1/P2/P3 with impact + effort)

---

## Production Mode

### Session Start: Minimum Inputs

Production starts from a minimum prompt. The user provides:

1. **Page type** -- state hub, county page, or city page
2. **State** -- the U.S. state
3. **Target geography** -- for child pages, the specific county or city; for hub pages, the state itself
4. **Firm name** -- the firm's brand or website

Everything else is gathered autonomously per the Research Protocol below. The skill does not wait for an exhaustive input checklist before starting research. It asks the user only for input that the Research Protocol cannot produce, or when ambiguity blocks production.

If the user volunteers additional context upfront (verified courthouse data, curated testimonials, internal procedural notes, specific CTA preferences), the skill incorporates it and skips the corresponding research steps. The minimum prompt is the floor, not the ceiling.

---

### Research Protocol

Execute these steps in order before writing any body copy. Cache results across the session. If a step fails to surface data, log a `[VERIFY: ...]` flag for the dev notes block and continue. Do not block production on a single missing data point unless it is the primary geography itself.

#### Step 1 -- Load Brand Voice (Hard Prerequisite)

Check available_skills for a voice skill matching the firm. Voice skills follow the convention `{brand}-voice` (e.g., sterling-voice, vasquezdelara-voice, drake-voice, johnsonlgroup-voice).

- If a voice skill exists: load it. Internalize the firm's tone, vocabulary, CTA patterns, and messaging pillars before continuing. Write through that voice from the first paragraph to the last.
- If no voice skill exists: stop and ask the user to describe how the firm sounds. Do not write body copy against a placeholder voice.

This step is non-negotiable. Voice is loaded fresh from the skill at session start, never inferred from memory of past sessions. The above-the-fold intro especially must reflect the firm's actual persuasion pattern (emotional truth then structure, authority then empathy, direct then supportive). Do not default to a generic "we serve X in Y" opening unless that is genuinely how the firm sounds.

#### Step 2 -- Map the Firm's Footprint

Use web_fetch to pull the firm's public information. Typical entry points:

- Firm homepage
- Locations or offices page (common paths: /locations, /offices, /our-offices, /contact)
- Attorneys or team page (common paths: /attorneys, /our-team, /lawyers)
- Practice areas hub (common paths: /practice-areas, /services, /family-law)
- sitemap.xml as a fallback if the site is JavaScript-heavy and content does not surface through normal page fetches

Extract and cache:

- Every office: address, phone, hours, which state(s) it serves
- Every attorney: name, title, bar admissions, biography URL, regions covered
- Every practice area URL: confirmed canonical URL for each practice area (these become the routing targets for the page)
- Existing service-area pages: any state hub, county pages, or city pages already published (used for parent and sibling linking)

#### Step 3 -- Define the Target Geography

For a state hub:

- All offices located in or serving the target state
- Metro region clusters based on office locations and state geography (Front Range, Fox Valley, Twin Cities Metro, Pikes Peak Region). Cluster names should match how locals refer to regions, not census MSAs
- Counties served by each office (default: the county the office sits in plus immediately adjacent counties; expand if the firm's site documents wider coverage)
- Coverage model for the rest of the state (virtual consultation, travel, or not served)

For a county page:

- The target county and its county seat
- Cities and communities within the county (cross-reference U.S. Census, county government site, or Wikipedia)
- The firm's nearest office to this county, with approximate drive distance to the county seat
- Whether the firm's site documents coverage of this specific county

For a city page:

- The target city
- The county the city sits in. If the city spans multiple counties (Kansas City, Texarkana, parts of the Twin Cities), name both and identify which is primary for family law filing
- Neighborhoods, districts, or named communities within the city
- The firm's nearest office to this city, with drive distance
- Nearby cities in the same metro that could become sibling pages later

#### Step 4 -- Locate Court Infrastructure

For each relevant county, web search for:

- Family or divorce court name (state-specific terminology: Circuit Court, District Court, Superior Court, Family Court, Court of Common Pleas)
- Courthouse address
- Clerk of court address if different from the courthouse
- For multi-court counties (counties with separate Family Division courts), the specific court that hears divorce, custody, and support matters

This data goes IN the office-to-court table on the hub, and IN the local logistics section on child pages. It does not stay in dev notes if it has been verified through research. If a courthouse address cannot be confirmed through public search, flag `[VERIFY: courthouse address for {County}]` and continue.

#### Step 5 -- Compile Local Proof

Search for evidence of the firm's actual presence in the target geography:

- Testimonials with location attribution (firm reviews page, Google Business Profile reviews if visible, "results" or "case stories" pages)
- Community involvement (bar association leadership, sponsorships, local nonprofit work)
- Attorney ties (bar admissions specific to the geography, biographical mentions of living or practicing in the area, named experience in local courts)
- Years of practice in the geography if documented

Do not fabricate. If a category yields nothing public, omit it from the page rather than invent it. The skill prefers a thinner page with verifiable proof over a fuller page with manufactured credibility.

#### Step 6 -- Confirm Parent and Sibling URLs

For a state hub: check whether any county or city pages already exist on the firm's site. If yes, those become the destinations for community and county names in the "Communities and Counties Served" section.

For a county or city page: confirm the state hub URL exists. If the hub is not yet built, flag `[VERIFY: hub URL once published]` and use a placeholder breadcrumb.

For a city page: identify nearby cities that may become sibling pages later. Lateral linking can be added in a future revision; for now, the page links up to the county and the state hub only.

#### Step 7 -- Compile Verification Flags

Every `[VERIFY: ...]` flag raised during research goes into the dev notes block at the bottom of the DOCX. Categorize them:

- **Public data not surfaced** (courthouse address, office hours): the user can usually verify quickly
- **Firm-internal data** (proprietary procedural knowledge, unattributed testimonials, community involvement the firm has but does not publish): the user must supply if they want it on the page
- **Structural items** (parent hub URL, sibling page URLs): become live as the page set is built out

The dev notes block is for verification flags and schema recommendations. It is not a hiding place for data that belongs on the page itself.

---

### When to Ask the User

The Research Protocol handles most of what previous versions of this skill collected via input checklist. Ask the user only when:

- A voice skill is not loaded AND no voice description has been provided
- The firm has multiple offices and it is genuinely unclear which serves the target geography (two offices roughly equidistant from the county seat with no documented assignment)
- The firm operates in states or practice areas the user did not mention, and the discrepancy materially changes the page (the user asks for a Wisconsin hub but the firm has both Wisconsin and Illinois offices with different practice menus)
- The target geography appears to fall outside the firm's documented service area
- The user has explicitly requested a pre-write review of research findings

Do NOT ask the user for:

- Office addresses, phone numbers, attorney lists, or practice page URLs (public)
- Courthouse names or addresses (public)
- Lists of cities, counties, or neighborhoods (public)
- Drive distances, modality logic, or metro cluster names (calculable)
- Anything the Research Protocol is designed to surface

Asking for input the skill should gather autonomously is a process failure, not user-friendliness.

---

### Pre-Write Summary (Conditional)

For complex pages, present a brief research summary back to the user before writing:

- Offices in scope, with the nearest office to the target geography flagged
- Courthouse(s) being referenced
- Cities, counties, or neighborhoods that will appear on the page
- Practice page URLs being routed to
- Any [VERIFY] flags already raised

Trigger the pre-write summary when:

- Building a state hub with five or more offices
- The county or city has ambiguous office assignment (two offices roughly equidistant)
- Research surfaced material that contradicts how the user framed the request
- The user explicitly asked for a pre-write pause ("review the research first," "show me what you found before drafting")

For straightforward pages (a single county served by a single office, a city with a clear nearest office and county assignment, a hub with one or two offices), proceed directly to writing. The pre-delivery self-audit catches structural issues; the dev notes block surfaces verification needs. A pre-write pause on every page slows production for no quality gain.

### Universal Writing Guardrails (Apply Regardless of Brand Voice)

These rules apply to every service-area page regardless of which firm it is written for. Violating any of them constitutes a failed delivery.

- **No em dashes.** Use commas, periods, colons, or parentheses instead. This applies to body copy, bullets, headings, CTAs, FAQs, and dev notes. Em dashes are the recurring style violation on this skill's output when not explicitly blocked.
- **No AI phrasing patterns.** Avoid "navigating the complexities of," "in today's world," "it's important to note," "in the ever-evolving landscape of," and similar tells.
- **No outcome guarantees.** Do not promise results, rankings, timelines, or case outcomes. The service-area page's promise is access to the firm's capability, not a specific outcome.
- **No manufactured urgency or fear-mongering.** State the stakes honestly. Do not inflate them.
- **Use "you/your" to address the reader.** Use "our team" or the firm name to reference the firm.
- **No legal education.** See the anti-cannibalization rules in the Core Principle section. Service-area pages route to practice pages. They do not teach the law.

---

## Hub Page Template (State-Level)

### Title Tag
{STATE} Family Law Attorneys | {OFFICE_COUNT} Offices | {BRAND}

### H1
Write in the brand voice. Not a keyword-stuffed formula. The H1 should feel like the firm's actual positioning statement with a geographic anchor.

Examples (vary by voice):
- "Your North Star for Family Law in Colorado" (guidance brand)
- "Colorado Family Law Attorneys Who Fight for What Matters" (aggressive brand)
- "Family Law Representation Across Colorado" (straightforward brand)

### Above-the-Fold (3 paragraphs, 100-180 words)

Per the `colorado-service-area-hub-v9` canonical, the hub above-the-fold is three paragraphs ending in an inline bold CTA. There is no separate "Primary CTA Block" after the intro; the CTA is paragraph 3.

- **Paragraph 1: Positioning only.** Name the emotional reality the reader is sitting in (the moment of family transition, the feeling that no one is steering), then pivot to what the firm stands for and the core differentiator that backs it up. Written in the brand voice. This paragraph's job is to establish the firm's promise to the reader (single-focus practice, settlement-first, fight-and-compassion, board-certified specialization, guidance-based model, whatever the firm's actual position is) and the one or two reasons that promise is credible. The state name is the only geographic reference permitted in Paragraph 1. Do NOT list counties, cities, metros, regions, courthouses, or office addresses here. Geographic enumeration in this slot creates redundancy with the Communities and Counties Served section below and dilutes the positioning the paragraph is supposed to be doing.

- **Paragraph 2: Service modality.** Where the firm meets clients (in person at named offices, by video, by phone), framed in a way that does not encode a specific office count or county list (those details belong in the office-to-court table and the Communities section). Do NOT include trust stats, review counts, or CTA language. Modality only.

- **Paragraph 3: Inline bold CTA paragraph.** Canonical format: `**Schedule a no-pressure consultation: **call **(central consultation phone)** or [book a time online](contact-us URL). [Single value statement reinforcing what the consultation actually delivers.]` Replaces any standalone CTA banner. The same inline-CTA pattern is reused at the end of the Why Trust section ("**Ready to talk? **") and in the closing section ("**Call (phone)** or [schedule a consultation online](url)"). Three placements total, never as a separate banner.

**Positioning paragraph done right** (compressed example, brand voice would adjust the wording):
> When your family is in transition, you want a firm whose entire focus is families in transition. [BRAND] is built around one thing: family law. That single focus, paired with [the firm's specific differentiator pulled from the voice skill: settlement-first approach, board-certified specialization, guidance-based model, fight-and-compassion identity, etc.], is what we bring to [STATE] families when the stakes feel personal.

The differentiator slot is filled from the loaded brand voice skill, not from defaults. Do not insert pricing structures, billing models, or firm-specific operational claims unless the voice skill confirms them. If the voice skill does not specify a differentiator that fits the positioning slot, lean on the firm's stated focus or values rather than inventing operational specifics.

**Positioning paragraph done wrong** (the county-stuffing failure pattern):
> [BRAND] serves Milwaukee County, Waukesha County, Dane County, Brown County, Outagamie County, Winnebago County, and surrounding areas across Wisconsin with our team of family law attorneys focused on divorce, custody, and support.

The first version positions the firm. The second version is a directory listing dressed up as prose. The county list belongs in the Communities and Counties Served section below, where readers expect to scan for their geography. Putting it in Paragraph 1 wastes the positioning slot and forces the same content to appear twice on the page.

Do NOT open with a practice-area definition or legal explainer. Do NOT open with firm history. Do NOT open with a county or city list. The reader wants to know: who is this firm, and is it the right fit for me?

### CTA Pattern (inline, not banners)

The hub canonical uses **three inline bold CTA paragraphs**, not standalone banners or callout boxes:

1. **Above-the-fold P3.** "**Schedule a no-pressure consultation: **call **(phone)** or [book a time online](url). [Value statement.]"
2. **End of Why Trust section.** "**Ready to talk? **Call **(phone)** or [schedule a no-pressure consultation](url)."
3. **Closing section before Related Pages.** "**Call ****(phone)** or [schedule a consultation online](url). [Short follow-up sentence about scheduling.]"

All three placements route to the same central consultation phone and the same `/contact-us/` (or equivalent scheduling) URL. The validator accepts up to four occurrences of the CTA URL (three inline + one in the Related Pages footer).

Do not insert a separate "Primary CTA Block" between sections, a colored CTA banner, a callout box, or a standalone CTA table. The intro paragraph IS the first CTA placement; do not duplicate it.

### "What We Handle" (routing module, NOT a content section)

One intro sentence. Then a bulleted list:
- Each bullet: linked practice area name + one-sentence descriptor (under 15 words) + link to canonical practice page
- Links as the practice area name itself, not "Learn about" or "Learn more"
- No H3 subsections per practice area
- No legal explainers, statute references, or process breakdowns
- Total section length: 150-250 words max

This section's job is to say "yes, we handle your issue" and move the reader to the right page. Nothing more.

### Communities and Counties Served

This section is the SEO anchor scaffold for the firm's eventual hub-and-spoke architecture. It must be structured so that county and city names are clean, isolated anchor candidates ready to become hyperlinks the moment child pages launch, with no copy editing required.

**Required structure (three layers, each carrying a distinct anchor function):**

- **Layer 1 -- Regional cluster (H3 heading, NOT an anchor target).** Each H3 is a metro or regional cluster name like "Greater Houston Metro," "Denver Metro," "Colorado Springs and Pikes Peak Region," "Northern Colorado," or "Greater [Major City] Metro." H3s organize the page for human navigation; they do not map to a child page and remain plain text.
- **Layer 2 -- County (bolded inline label, anchor target).** Within each regional H3, every county served is a bolded inline label followed by a colon. This label is the anchor target for the county-level child page (e.g., `/[state]/[county]/`). Format: `**Brazoria County:** [city list]`.
- **Layer 3 -- Cities (comma-separated catalogue, each an anchor target).** Each city in the comma-separated list following a county label is a discrete word ready to wrap as a hyperlink to its city-level child page (e.g., `/[state]/locations/[city]/`).

**Structure example (Greater Houston Metro, four counties, single regional cluster):**

```
H3: Greater Houston Metro
[short context paragraph: which offices serve this metro, what the
county and city labels lead to once child pages exist]

- Brazoria County: Pearland, Angleton, Manvel, Alvin, ...
- Harris County: Houston, Pasadena, Webster, Clear Lake
- Galveston County: League City, Galveston, Texas City, ...
- Fort Bend County: Sugar Land, Missouri City, Stafford, ...

H3: Beyond the Greater Houston Metro
[paragraph: virtual coverage statement, how cases are routed]
```

**Structure example (Colorado, multiple regional clusters):**

```
H3: Denver Metro
- Denver County: Denver
- Arapahoe County: Englewood, Centennial, Cherry Hills Village
- Adams County: Commerce City, Brighton, Henderson, Thornton
- Douglas County: Castle Rock, Castle Pines, Lone Tree, Parker
- Jefferson County: Lakewood
- Broomfield County

H3: Colorado Springs and the Pikes Peak Region
- El Paso County: Colorado Springs
- Teller County

H3: Northern Colorado
- Larimer County: Fort Collins, Loveland, Timnath
- Weld County: Greeley, Windsor

H3: Beyond the Front Range
[paragraph: virtual coverage statement]
```

**Why this structure:**
- The H3 is a regional/metro cluster, which matches how clients actually think about geography ("I'm in the Houston metro," "I'm in the Bay Area"), not how the legal system filing structure works ("I'm in Galveston County")
- Bolded county labels are visually compact, fit many counties under one H3, and each is an isolated anchor candidate
- Comma-separated city lists let every city be a discrete word ready for hyperlinking without prose surgery
- It scales: firms with one major metro (e.g., SMB in Greater Houston) get one H3 plus a "Beyond" section; firms with multiple distinct regions (e.g., Johnson Law Group across Colorado) get one H3 per region

**Patterns to avoid:**
- H3 = county name. This makes each county its own section, inflates the page, and loses the regional mental model. (This was an earlier iteration of this skill; it has been replaced.)
- Counties and cities buried in flowing prose with mid-sentence commas. The cities then have to be surgically wrapped as anchors, which makes future linking expensive.
- A flat alphabetical list of every city the firm serves. Loses the regional grouping that helps readers locate themselves.
- Mixing county labels and city labels in the same bullet without visual hierarchy. The county is the parent anchor; the cities sit under it.

**Anchor-routing rules for the developer (document in dev notes):**
- Regional H3s are NOT anchored
- Each bolded county label becomes a hyperlink to its county page when that page exists
- Each city in the comma-separated catalogue becomes a hyperlink to its city page when that page exists
- The Office-to-Court Map county column should anchor to the same county pages once they exist, coordinated with the Communities section so each county has a single canonical anchor target
- If a city straddles two counties (Friendswood across Harris/Galveston, Kansas City across Jackson/Wyandotte), list it under one canonical county only to give the city a single anchor target

Once child pages are built, the developer wraps each bolded county label and each city in the catalogue with the appropriate hyperlink. No copy rewrite required.

This section sits above the Office-to-Court Map intentionally. The reader's mental model is "I live in X county, do you serve me?" so the page answers that question first before explaining where the firm's offices sit and which courts they work in.

### Office-to-Court Map (the local substance this page needs)

This is where the page earns its geographic authority. This section is also where the skill most often fails: the default move is to produce prose paragraphs because they feel like "writing," when the actual requirement is a structured module with discrete data points on the page itself.

**Section heading on the rendered page:**
The internal section name is "Office-to-Court Map" but the H2 in the actual deliverable should be reader-centric, not operational. Examples that work: "Where You Are, Where Your Case Is Heard," "Where Your Case Is Filed and Why It Matters," "How Our Offices Map to the Courts." The reader-centric phrasing reframes the section from "here is our internal operations data" to "here is what this means for you." Operational headings like "Office-to-Court Map" or "Service Area Locations" are flagged as default moves that should be replaced with reader-centric phrasing during writing.

**Required elements:**
- A table (not prose) mapping each office to: office address, primary counties served, nearest district or family court name, and court address. The table is mandatory. Prose is not a substitute.
- A short paragraph covering how the firm handles counties not directly adjacent to an office (virtual consultation, travel, coordination with local courts).

**Where verified data goes:**
- If the user has provided verified courthouse names and addresses, they belong IN the table body on the page. They do not belong only in dev notes. Dev notes are for flagging what needs checking, not for hiding data that belongs on the page.
- If an address is unverified at the time of writing, put a `[VERIFY: ...]` placeholder in the table cell AND add a verification item to the dev notes section.

This section should be the most information-dense geographic content on the page. If the section is only prose and the verified courthouse data is sitting in dev notes, the page has failed its primary SEO job.

### Mid-Page Rhythm Break (inline, not a banner)

The hub canonical does NOT use a styled mid-page CTA banner. Earlier versions of this skill prescribed one; that guidance is superseded. The rhythm break between the Office-to-Court Map and the Why Trust section is handled by section spacing and headings, not by a colored callout.

The CTA work that a mid-page banner would have done is absorbed into the **second inline bold CTA paragraph** at the end of the Why Trust section ("**Ready to talk? **Call **(phone)** or [schedule a no-pressure consultation](url)."). That placement is sufficient. Do not add a banner before, after, or in place of it.

If a firm's brand voice requires a brand-promise statement to break up the page visually (rare, and only if the voice skill documents this pattern), it should be set as a short bold paragraph in the firm's voice. Never as a styled banner table or callout box.

### Why [Geo] Families Trust [BRAND] (the trust block)

A focused, brand-voiced trust block with **five bold-lead paragraphs**, ordered to mirror how the canonical hub does it. The hub's pattern is: consultation philosophy → case-building philosophy → operational transparency (portal) → complex-case capability → preparation-over-guarantees.

**Required structure:**
- Five paragraphs, each opening with a bold lead-in phrase (literal DOCX bold formatting on a `TextRun`, not just a short opening sentence)
- Each paragraph 60-90 words; brand voice throughout
- The bold lead-ins are short and declarative (e.g., "The first call isn't a sales call.", "We build cases the way you'd want yours built.", "A client portal that keeps you in the loop.", "We're staffed for cases that don't fit a template.", "No outcome guarantees. Only preparation.")
- After the five paragraphs, close the section with the **second inline bold CTA paragraph** of the page: `**Ready to talk?** Call **(central consultation phone)** or [schedule a no-pressure consultation](contact-us URL).`

**Approved lead-in archetypes** (the firm's voice skill specifies which apply; reuse these archetypes verbatim across hub and child pages. This is intentional consistency, not duplication, because each page is a separate entry point for a different geographic search intent):

- Consultation philosophy ("The first call isn't a sales call.", "We listen first.")
- Case-building philosophy ("We build cases the way you'd want yours built.", "Two cases never look the same.")
- Operational transparency ("A client portal that keeps you in the loop.", "You will always know where your case stands.")
- Complex-case capability ("We're staffed for cases that don't fit a template.", "When the case isn't simple, the work has to match.")
- Preparation over guarantees ("No outcome guarantees. Only preparation.", "We commit to the preparation, not to the result.")

The scanability of this section depends on the lead-ins being literally bold. Paragraphs with un-bolded opening phrases fail this section even if the content is correct. The closing inline CTA is the second of three inline CTA placements on the page.

### What to Expect When You Call (consultation process section)

H2: "What to Expect When You Call"

Open with one short intro sentence: "Our consultation process is straightforward and built around three things you need before any decisions get made:"

Then a **three-item bulleted list** (NOT numbered) where each bullet has a bold lead-in followed by a short descriptor. The three items mirror the hub's "listen → explain → map":

- **We listen first.** Tell us what is happening. The short version is fine, and we will ask the questions that matter.
- **We explain what [State] law says.** In plain English. No lecture, no scare tactics, no pressure.
- **We map the next step.** You will leave the consultation with a clear sense of what comes next: filing, responding, gathering records, or pausing to think it through.

Adapt the wording to the firm's voice, but keep the three-step "listen → explain → map" architecture and the bullet-with-bold-lead format. **Numbered lists are a pattern violation**; the canonical hub uses bullets because the three steps are equally weighted, not sequential gates.

### FAQs (4-6, localized)

FAQs on a service-area page should be geographic and process-oriented, NOT practice-area questions.

Good service-area FAQ topics:
- "Which courthouse will my case be filed in?" (with specific courthouse names)
- "Do I have to come into an office, or can we work virtually?"
- "My ex moved out of state. Can you still help?" (if multi-state capability exists)
- "What does it cost to hire a family law attorney?" (brief, routes to consultation)
- "How long will my case take?" (brief, mentions state-specific minimums only)
- "I do not know what kind of legal help I need yet." (consultation-forward)

Bad service-area FAQ topics (these belong on practice-area pages):
- "How is child support calculated in [state]?"
- "What factors do courts consider for custody?"
- "What is equitable distribution?"

### Closing Section: "Talk to a [Geo] Family Law Attorney"

The page body ends with a confident recap section that mirrors the canonical hub's closing. Structure:

- **H2:** "Talk to a [State] Family Law Attorney" (on a hub) or "Talk to a [County/City] Family Law Attorney" (on a child page)
- **Recap paragraph:** 2-3 sentences in brand voice. The hub's pattern is "We know [geo's] courts. We know the path through this kind of case. And we will walk you through what comes next before you commit to anything." Adapt to the firm's voice, keeping the confident-assertion + process-promise architecture.
- **Third inline bold CTA paragraph:** `**Call ****(central consultation phone)** or [schedule a consultation online](contact-us URL). [Routing sentence about how the firm will assign the right attorney and office.]`

This is the third and final inline CTA placement on the page. No standalone banner.

### Related Pages (footer)

H3 nested under the Closing Section's H2: "Related Pages"

A single bulleted list of 10-13 internal links. The hub pattern includes:

1. (Child pages only) The parent state hub URL as the first item, anchored "[State] family law (state hub)"
2. All practice-area URLs that appear in "What We Handle" (linked again here per the catalog+footer dual-placement convention)
3. Attorney bio hub URL ("Meet our attorneys")
4. Reviews page URL ("Client reviews")
5. Contact/consultation URL ("Contact and consultation")

Anchor text is the page name itself (e.g., "Divorce", "Child Custody", "Meet our attorneys", "Contact and consultation"), not "Learn about..." or "Click here for...".

This section is the canonical second placement for practice URLs (counted under the Single-Placement Rule). It is also the single placement for the attorney hub, reviews page, and parent state hub URL.

### Dev Notes Block

Include at the bottom of every page, AFTER the Related Pages footer, separated by a divider. The dev notes are reference material for the publishing team and SEO, not for the CMS body.

Required sections:

**Verification Status:** bulleted list of verified facts (office NAPs, courthouse names and addresses, judicial district assignments, voice-skill claims like portal availability or attorney credentials). Note the verification source (NAP file, Google Places lookup, state judicial branch, voice skill citation) and re-verify dates if relevant.

**URL and Linking:** bulleted list of URL conventions, slug confirmations needed, anchor-text discipline notes, inbound linking instructions (how the parent hub or sibling pages should link to this page).

**Schema recommendations:** LegalService for offices, FAQPage for FAQ sections, BreadcrumbList for the page's place in site hierarchy, AggregateRating only if backed by publishable reviews.

**Follow-Up Items:** open `[VERIFY: ...]` flags categorized as public data, firm-internal data, or structural items pending the firm's URL convention or roster.

---

## Child Page Template (County or City Level)

### Title Tag
Family Law Attorney in {CITY}, {STATE} | {BRAND}
-- or --
{COUNTY} County Divorce and Custody Lawyers | {BRAND}

### H1
Written in brand voice with geo anchor. Not a keyword formula.

### Above-the-Fold (3 paragraphs, 100-180 words)

Child pages use the **same 3-paragraph structure as the hub** (positioning + modality + inline bold CTA). The only difference is that the geographic anchor is the target county or city, not the state.

- **Paragraph 1: Positioning + geo anchor.** One short paragraph in the brand voice that establishes the firm's promise and core differentiator, then anchors to the county or city by name. The county or city name is the only geographic reference allowed in this paragraph. Do NOT list neighborhoods, communities, suburbs, or adjacent towns here; those belong in the "Neighborhoods We Serve" / "Local Coverage Detail" section below. Do NOT name the courthouse here either; the courthouse appears in P1 only if it is part of the positioning hook (e.g., "an attorney who understands the [Court Name] where your case will actually be heard"), not as a standalone fact.

- **Paragraph 2: Service modality.** A short paragraph stating the nearest office and the modality options (in person, by video, by phone). Do not include trust stats, review counts, or CTA language. Modality only. If no office serves the area directly, state "serving {CITY_OR_COUNTY} by video and phone" without implying an in-person presence.

- **Paragraph 3: Inline bold CTA paragraph.** Same canonical format as the hub: `**Schedule a no-pressure consultation:** call **(central consultation phone)** or [book a time online](contact-us URL). [Single value statement.]` This is the first of three inline CTA placements; no standalone banner follows it.

### Family Law We Handle in [Geo] (practice routing)

Same rules as the hub page. H2 phrased as "Family Law We Handle in [County/City]." One intro sentence, then 8-10 bulleted practice areas in the canonical hub format:

- `[**Practice Area Name**](canonical URL): One-sentence descriptor under 15 words.`

Practice URLs match the firm's documented slug convention (the hub establishes this; do not invent). Anchor text is the practice area name in bold, linked. No "Learn about" patterns. No geo in the anchor.

### [Geo] Neighborhoods We Serve / Local Coverage Detail

H2 phrased as "{City} Neighborhoods We Serve" for a city page, or "{County} Communities We Serve" for a county page where the county contains multiple incorporated cities.

For a single-city county page (e.g., Denver County where the City of Denver IS the county), use a flat structure with bolded inline cluster labels and comma-separated neighborhood lists, no H3 subheads per cluster, no links on neighborhood names (since neighborhoods rarely have their own child pages):

```
**Central [City]:** Neighborhood A, Neighborhood B, Neighborhood C, ...
**North [City]:** Neighborhood D, Neighborhood E, ...
```

For a multi-city county page, use the same regional-cluster anchor architecture as the hub (H3 region + bolded county label + comma-separated city links).

Close the section with one short sentence inviting readers whose neighborhood isn't listed to call and confirm coverage.

### Where You Are, Where Your Case Is Heard (office-to-court table)

Same H2 phrasing as the hub. For a child page, the table typically has a single body row (the office that serves this geography paired with the courthouse where this county's cases are heard). The columns are identical to the hub: Office | Counties Served | Primary Courthouse.

Below the table, one short paragraph explaining the local logistics in prose (which courthouse handles family law dockets, which division, parking notes only if verified). Do NOT publish unverified procedural specifics. Flag `[VERIFY: ...]` in dev notes for any claim that needs firm-side confirmation.

### Why [Geo] Families Trust [BRAND]

Same five-bold-lead-paragraph structure as the hub's trust block. The five lead-in archetypes (consultation philosophy, case-building, portal transparency, complex-case capability, preparation-over-guarantees) are reused verbatim or near-verbatim across hub and child pages. This is intentional consistency, not duplication, because each page is a separate entry point for a different geographic search intent.

Close the section with the second inline bold CTA paragraph (`**Ready to talk?**` + phone + contact-us link).

### What to Expect When You Call

Same H2, same intro sentence, same three bullets with bold leads as the hub. Reuse verbatim. The "Colorado law" reference in bullet 2 stays as the state name, not the county.

### Frequently Asked Questions (4-6, localized to the county or city)

H3 for each question. Localize the FAQs to the target geography:

- "Where will my [County] family law case be filed?" (specific courthouse + judicial district)
- "Do I have to come into the [Office City] office, or can we handle this virtually?"
- "What if my spouse recently moved out of state?" (UCCJEA-aware answer if multi-state capability exists)
- "Does it matter which [City] neighborhood I live in?" (or similar geographic granularity question)
- "How much will it cost?" (brief, routes to consultation)
- "I am not sure what kind of legal help I need yet." (consultation-forward)

Bad FAQ topics (these belong on practice-area pages, not service-area pages):
- "How is child support calculated in [State]?"
- "What factors do courts consider for custody?"
- "What is equitable distribution?"

### Closing Section: "Talk to a [Geo] Family Law Attorney"

Same structure as the hub's closing section. H2 + 2-3-sentence recap paragraph in brand voice + third inline bold CTA paragraph.

### Related Pages (footer)

H3 nested under the closing H2. The child page's Related Pages list mirrors the hub's, with one addition: the **parent state hub URL** appears as the first item, anchored "[State] family law (state hub)" or similar.

---

## Pre-Delivery Self-Audit (Mandatory Before DOCX Output)

Before handing any service-area page to the user, run this audit against the draft. If any item fails, fix it before delivering. Do not deliver a doc with open audit items and do not ask the user to fix failures that are yours to resolve.

**Structure and substance:**
- [ ] Title tag, meta description, and URL labeled at the top of the deliverable (bold-label format above the H1), not buried in dev notes
- [ ] Service + geo in Title + H1 + first paragraph (natural, not stuffed)
- [ ] H1 carries the firm's brand identity anchor + geo (e.g., "Your North Star for Family Law in [Geo]" for guidance-brand firms; the firm's actual brand-voice equivalent for other brands)
- [ ] Above-the-fold is **3 paragraphs**: P1 positioning + geo anchor (state on hub, county/city on child), P2 service modality only, P3 inline bold CTA paragraph
- [ ] P2 does NOT include trust stats, review counts, or CTA language. Modality only.
- [ ] P3 follows the canonical inline CTA format: bold action lead, bolded central consultation phone, contact-us link with descriptive anchor, single value statement
- [ ] **No standalone CTA banners, tables, or callout boxes** anywhere on the page. CTAs are inline bold CTA paragraphs at three placements only: end of above-the-fold (P3), end of Why Trust section, closing section before Related Pages
- [ ] Clear office vs serving language (no misrepresentation)
- [ ] Practice area content is a routing list, not explainer sections
- [ ] Practice area routing is under 250 words total
- [ ] No legal education content (statute references, process breakdowns, factor lists) on the page
- [ ] Geographic substance is the majority of the page content (60-70%)
- [ ] Communities and Counties Served uses the regional-cluster anchor architecture: H3 = region (not anchored), bolded inline label = county (anchor target), comma-separated list = cities (anchor targets). NOT one H3 per county. NOT cities buried in flowing prose with mid-sentence commas.
- [ ] If a city straddles two counties (e.g., Friendswood across Harris/Galveston), it appears under one canonical county only so it has a single anchor target
- [ ] Office-to-Court Map H2 in the rendered page is reader-centric phrased ("Where You Are, Where Your Case Is Heard"), not operational ("Office-to-Court Map," "Service Area Locations")
- [ ] Office-to-Court Map is rendered as a table (not prose substitute)
- [ ] Communities and Counties Served section appears ABOVE the Office-to-Court Map section (client-first ordering)
- [ ] Verified courthouse names and addresses appear IN the table body, not only in dev notes
- [ ] Why [Geo] Families Trust [BRAND] section uses five bold-lead paragraphs (literal DOCX bold formatting on lead-ins) following the canonical archetypes: consultation philosophy, case-building, portal transparency, complex-case capability, preparation-over-guarantees
- [ ] Why Trust section closes with the second inline bold CTA ("**Ready to talk?**" pattern)
- [ ] What to Expect When You Call section uses **bullets** (not numbered list) with bold lead-ins; three items mirroring "listen → explain → map"
- [ ] FAQs are localized to geography and process, not practice-area education
- [ ] Closing section uses H2 "Talk to a [Geo] Family Law Attorney" with a confident recap paragraph + third inline bold CTA
- [ ] Related Pages H3 nested under the closing H2, with 10-13 footer links; child pages include the parent state hub URL as the first item

**Linking and voice:**
- [ ] Practice URLs appear up to 2x (catalog body + Related Pages footer). CTA destination URLs (e.g., /contact-us/) appear up to 4x (three inline CTAs + footer). 5+ occurrences of any URL is a hard fail.
- [ ] Links to canonical practice-area pages use service-only anchors (no geo in anchor)
- [ ] Link anchors are varied and natural (no repeated "Learn about X" pattern)
- [ ] Lead-In Requirement: in non-catalog body prose, every link is embedded in a sentence whose meaning is incomplete without the linked topic. No "See our X page" tag-ons. Catalog rows are exempt because the descriptor sentence performs the same function.
- [ ] No multi-link clusters in body prose outside catalog modules
- [ ] No bare URL or generic ("click here," "this page," "learn more") used as anchor text in body
- [ ] Written in the firm's brand voice, loaded from the voice skill at session start (not inferred from memory)
- [ ] Smart apostrophes and quotes used throughout (U+2019, U+2018, U+201C, U+201D), not straight ASCII

**Pre-delivery validator:**
- [ ] `node scripts/validate-page.js path/to/page.docx` has been run and exited 0. Hard-fails on 5+ URL occurrences, tag-on patterns, em dashes, banned AI-tells, generic/bare-URL anchors, and citation/Sources mismatches. Soft-warns on 2-4 URL occurrences (expected catalog+footer + CTA destination patterns). Do not present the file until the validator passes.

**Style guardrails (match the Universal Writing Guardrails section):**
- [ ] No em dashes anywhere (body, bullets, headings, CTAs, FAQs, dev notes)
- [ ] No AI phrasing patterns ("navigating the complexities of," "in today's world," "in the ever-evolving landscape of," etc.)
- [ ] No outcome guarantees, manufactured urgency, or fear-mongering

**Conversion and delivery:**
- [ ] Three inline bold CTA paragraphs at the canonical placements (above-the-fold P3, end of Why Trust, closing section before Related Pages). All three route to the central consultation phone and `/contact-us/`. No standalone CTA banners.
- [ ] For child pages: parent state hub link appears as the first item in the Related Pages footer
- [ ] Dev notes block with Verification Status, URL and Linking, and Follow-Up Items subsections

**Research provenance:**
- [ ] Research Protocol (Steps 1-7) was executed before writing began. Office, attorney, practice URL, courthouse, and proof data on the page came from web_fetch or web_search, not from inference or memory of past sessions
- [ ] Every data point on the page is either verified through research, supplied by the user, or marked with a `[VERIFY: ...]` flag. No data point is presented as fact without one of those three sources

Failed items must be fixed before delivery. A doc with known audit failures is a failed delivery, not a draft.

---

## Do / Don't Summary

**DO**
- Build service-area pages to win service + geo queries while supporting practice-page authority
- Put the page's content weight in geographic substance: courts, offices, counties, communities, local proof
- Route to practice pages with a tight, linked list and varied anchor text
- Lead the "why us" section with court knowledge and local familiarity, not generic claims
- Write in the firm's brand voice from the first sentence to the last
- Include a "what to expect" conversion section that reduces friction for local-intent searchers
- Localize FAQs to geographic and process questions, not practice-area topics
- Be explicit about service modality (office vs virtual vs travel)
- Include dev notes for everything that needs verification

**DON'T**
- Write practice-area explainers on service-area pages (this is the most common and most damaging mistake)
- Use H3 subsections per practice area on a service-area page
- Include statute references, legal formulas, factor lists, or "how it works" content
- Use "Learn about X" or "Learn more about Y" as repeated anchor text
- Write in a generic template voice when a brand voice skill exists
- Lead with differentiators that have nothing to do with the geography (portal, multi-state, credentials come after court knowledge)
- Put practice-area FAQ questions on a geographic page
- Copy/paste large sections across every county/city page
- Imply staffed offices where none exist
- Publish without dev notes flagging what needs verification

---

## Reference: Common Failure Modes

These patterns have been observed in production and should be actively avoided:

**Failure: County stuffing in Paragraph 1.** Cramming a list of counties, cities, or metros into the opening positioning paragraph because it feels like "establishing service area." This collapses the positioning slot into a directory listing, and then forces the same content to appear again in the Communities and Counties Served section below. Fix: Paragraph 1 positions the firm (emotional reality + promise + core differentiator). Paragraph 2 carries office cities and virtual availability. Communities and counties live in their own dedicated section. The state name (hub) or target county/city name (child page) is the only geographic reference allowed in Paragraph 1.

**Failure: Per-county H3 architecture in the Communities section.** Giving every county its own H3 plus a paragraph plus a city list. This inflates the page, loses the regional mental model clients actually use ("I'm in the Houston metro," not "I'm in Brazoria County"), and forces awkward prose-level anchoring of cities buried inside flowing sentences. Fix: regional cluster as H3 (not anchored), bolded county label as inline anchor target, comma-separated city catalogue where each city is a discrete anchor candidate. See the Communities and Counties Served section for the full pattern.

**Failure: Operational heading on the Office-to-Court Map.** Publishing the H2 as "Office-to-Court Map," "Service Area Locations," or "Our Office Locations." Operational headings frame the section as the firm's internal data rather than as something useful to the reader. Fix: reader-centric phrasing in the rendered page ("Where You Are, Where Your Case Is Heard"). The internal section name in this skill stays "Office-to-Court Map" for instructional clarity, but the H2 in the deliverable is reader-centric.

**Failure: Standalone CTA banner duplicating an inline CTA.** Adding a styled banner table or callout block right after the above-the-fold paragraphs, even though P3 already contains the inline bold CTA. The reader gets the same phone-and-link content twice in a row, which reads as desperate and breaks the page rhythm. Fix: delete the banner. The canonical hub uses inline bold CTA paragraphs only (three placements (P3, end of Why Trust, closing section), and never a standalone banner table.

**Failure: Trust stat or CTA verb stuffed into above-the-fold P2.** Writing P2 as "Our [City] office serves [County] clients in person, by video, and by phone. The [City] office holds a 4.0-star rating across roughly 200 Google reviews. Call (XXX) XXX-XXXX or request a no-pressure consultation." This stacks modality + trust + CTA when the structure expects P2 = modality only and P3 = inline CTA. Fix: P2 carries service modality only. Trust signals belong in the Why Trust section. CTA work belongs in P3 (the inline bold CTA paragraph).

**Failure: Practice-area mini-pages on the hub.** Giving each practice area its own H3 section with state-specific legal substance (income-shares model, parental responsibilities terminology, advisory maintenance guidelines). This creates 8 mini practice-area pages that cannibalize the canonical practice pages. Fix: collapse to a routing list.

**Failure: "Learn about" anchor spam.** Using "Learn about our divorce representation," "Learn about custody," "Learn about child support" as the anchor text for every internal link. Reads like a directory, signals template content, provides no differentiation between destinations. Fix: varied, contextual, sentence-ending anchors.

**Failure: Generic voice.** Writing "[Firm] represents individuals and families across [State] in divorce, child custody, child support..." when the firm's actual voice leads with emotional truth and guidance metaphors, or with directness and aggression, or with warmth and reassurance. The voice skill exists for a reason. Fix: load the voice skill, internalize the persuasion pattern, write through it.

**Failure: Numbered "What to Expect" list instead of bullets.** Rendering the consultation process as `1. We listen first. 2. We explain... 3. We map...` when the canonical hub uses bullets with bold lead-ins. Fix: use bullets, not numbered list. The three steps are equally weighted, not sequential.

**Failure: Practice-area FAQs on a geographic page.** Answering "How is child support calculated in [State]?" on the service-area hub when that question belongs on the child support practice page. Fix: FAQs on service-area pages are about courts, offices, consultations, costs, timelines, and virtual access.

**Failure: Office direct phone in CTA copy.** Using the office's individual direct line (e.g., the Denver office's `(720) 706-5703`) in the inline bold CTA paragraphs when the firm has a centralized consultation/intake line (e.g., `(720) 640-8463`). Fix: CTA phone is always the central consultation line. Office direct lines may appear in the Office-to-Court Map table or in dev notes for reference, but never in CTAs.

---

## Reference: Patterns From Sample Pages

Use these as pattern-recognition prompts when auditing or building:

- **Lean directory hubs** can work when they cluster cities by region/metro, make the link list scannable, and add a coverage statement with conversion modules.
- **State landing + geo link directory hubs** can work when they combine strong conversion modules, reinforce practice pages with internal links, and avoid looking like a thin link farm.
- **Common failure mode on county pages:** H1 is localized but the body is mostly brand boilerplate or practice-area content. Fix: add county-specific proof/logistics + align supporting content to the county.

---

## DOCX Output

When producing service-area pages, deliver as .docx files following the docx skill. Read the docx skill SKILL.md before generating output. Follow the formatting standards defined in the family-law-service-pages skill (Arial, US Letter, heading sizes, paragraph spacing, hyperlink implementation) for consistency across the firm's page set.

### Page metadata at the top of the deliverable

Every service-area page DOCX opens with three bold-label metadata lines, in this order, ABOVE the H1:

```
**Title tag: **{Page title}
**Meta description: **{Up to 160 characters}
**URL (suggested): **{Relative URL path}
```

These are page metadata, not dev notes. They tell the publishing team exactly what to set in the CMS. The dev notes block at the bottom of the document is for verification flags, internal linking instructions, and schema recommendations, not for fields that belong in the CMS interface.

### URL conventions

URL slugs follow the firm's documented structure. Confirm against the firm's live sitemap during research. The canonical conventions used by Johnson Law Group (the reference firm for this skill's hub-aligned examples) are:

- **State hub:** `/{state}/` (e.g., `/colorado/`)
- **County child page:** `/{state}/counties/{county-slug}-county/` (e.g., `/colorado/counties/denver-county/`)
- **City child page:** `/{state}/locations/{city-slug}/` (e.g., `/colorado/locations/colorado-springs/`)
- **Practice pages:** root-level for single-state firms and state-nested for multi-state firms whose practice pages vary by jurisdiction. Confirm the firm's actual pattern; do not assume.

If the firm's convention differs (e.g., `/{state}/{county-slug}-county/` without the `counties/` segment), use what the firm publishes and flag the convention in dev notes.

### Pre-delivery

Before generating the DOCX, run the Pre-Delivery Self-Audit above. Fix every failed item before writing the file. Do not deliver a doc with open audit items.

After generating the DOCX, run the pre-delivery validator (`node scripts/validate-page.js path/to/page.docx`). The validator hard-fails on:
- 5+ occurrences of any single URL (over-duplication)
- Tag-on link patterns ("See our X page", "Learn more at", "Click here for")
- Generic or bare-URL anchor text
- Em dashes anywhere in the document
- Banned AI-tell phrases (navigate, delve, dive deep, unpack, leverage, in today's X world, "it's not just X, it's Y")
- "North Star" used more than once (or more than allowed by the firm's voice skill convention; for JLG, max 1 use, in the H1)
- Citation/Sources mismatches

The validator soft-warns on 2-4 URL occurrences as informational (expected catalog+footer and CTA destination patterns). Do not present the file until the validator exits 0.

### File naming

- `{state}-service-area-hub.docx`
- `{state}-{county}-county.docx`
- `{state}-{city}-city.docx`
