---
name: cluster-blog-writer
description: "Produce SEO-optimized, brand-aligned blog content organized into topical clusters. Use this skill whenever writing, drafting, revising, or producing blog articles as part of a content cluster or content plan -- regardless of industry or client. Trigger on any request to write clustered blog content, work through a blog content plan sequentially, produce a series of articles around a core topic, or continue an ongoing blog production workflow. This skill enforces answer-first structure, paragraph discipline, internal linking standards, sequential cluster workflow, and quality gates before delivery. Use it even if the user only mentions 'the next blog', 'the next article in the cluster', or 'continue the content plan.'"
---

# Cluster Blog Writer

## Purpose

This skill produces publication-ready blog articles organized into topical clusters. It enforces structural, SEO, and quality standards that apply regardless of client, industry, or niche. Brand voice, internal link targets, and client-specific details are loaded per session from the user's content plan or brief.

---

## Session Start: Load Client Context

Before writing the first article in any session, confirm you have the following. If a content plan spreadsheet or brief has been provided, pull from it. If not, ask the user to supply:

1. **Client/brand name and website URL**
2. **Brand voice summary** -- tone, persona, who the reader is, what the brand wants to be known for
3. **Industry and niche** -- what the content covers and what makes this brand's perspective distinct
4. **Content plan or cluster brief** -- list of article topics, primary keywords, related keywords, intent/funnel stage, FAQs, internal link targets (with URLs), and schema type
5. **CTA** -- the conversion action each article should drive toward (if not specified, use a generic "contact us / free consultation / get started" prompt in the brand's voice)
6. **Cluster pillar article** -- the foundational article in the cluster that all others must link back to
7. **Site architecture / service page inventory** -- the client's core service pages and any secondary/supporting pages available for internal linking (with URLs). If not provided, ask for it or confirm the user will supply link targets per article.

Once confirmed, state the cluster topic, identify the first article in sequence, and proceed.

---

## Content Structure Standards

### Answer-First Opening (Mandatory)
The reader's core question -- the search intent behind the article's primary keyword -- must be answered directly within the **first two paragraphs**. Do not open with backstory, emotional setup, or preamble.

- **Paragraph 1:** Deliver the direct answer clearly and concisely. Include the primary keyword naturally.
- **Paragraph 2:** Expand on why the details matter and establish the article's value. Ground it in the brand's voice and perspective.

### Paragraph and Readability Discipline (Mandatory)
- Maximum 2-3 sentences per paragraph in most cases. Break up any block that runs longer.
- Every H2 section must be scannable by reading the heading and first sentence alone.
- Use **bullet lists** for collections of items, options, consequences, or evidence types.
- Use **numbered lists** for sequential steps or checklists.
- Never use dense prose paragraphs where a tight list communicates the same information faster.
- Trim any section that repeats a point already covered.

### Standard Article Structure
1. **Answer-first intro** (2 paragraphs)
2. **Core substance sections** (H2s with H3 subsections where needed -- tight, skimmable)
3. **Misconceptions or common mistakes** (if applicable)
4. **Practical preparation or next steps** (if applicable)
5. **FAQ section** (using FAQs from the content plan or brief)
6. **CTA section** (in the brand's voice, driving toward the specified conversion action)
7. **Sources section** (only when the article contains `[N]` citations -- see External Linking Rules)

---

## What to Avoid (Universal)

These apply to every article regardless of client or industry:
- Generic boilerplate that could come from any brand in any market
- Adversarial, combative, or fear-mongering framing
- Robotic, stiff, or overly formal tone that reads like a textbook
- Obvious AI phrasing patterns (overuse of "it's important to note," "in today's world," "navigating the complexities of," etc.)
- Keyword stuffing or forced SEO phrasing
- Excessive bold, headers, or formatting that hurts readability
- Em dashes (use commas, parentheses, or sentence breaks instead)
- Filler sentences that add word count without adding insight
- Hedging language that undermines authority ("it might be possible that," "some people believe")

---

## Internal Linking Rules

### Core Service Page Link (Mandatory -- First Link in Every Article)
Every article must include a link to the most relevant core service page **within the first two paragraphs**. This is always the first internal link placed in the article, no exceptions.

Match the article's subject to the most relevant page from the client's site architecture. Use the core page's exact keyword as the anchor text.

**How to identify the right page:**
- If the client provided a service page inventory at session start, match against it.
- If a content plan specifies internal link targets, use those.
- If a secondary or more specific page is a stronger match than a top-level core page, link the secondary page first -- but confirm it exists on the site before placing the link. If it does not exist, fall back to the relevant core page.

### Link Sources (Priority Order)
1. **Core service page** -- mandatory first link, placed within the first two paragraphs (see above)
2. **Content plan / brief** -- pull all specified internal link targets and their URLs before writing
3. **Cluster pillar** -- every article must link back to the foundational pillar article using its target keyword as anchor text
4. **Earlier articles in the cluster** -- as the cluster grows, reference and link to prior articles where contextually appropriate
5. **Tool or resource pages** -- if the topic relates to a calculator, guide, or interactive tool the brand offers, link to it

### Placement Rules
- Place links in **contextually relevant** locations — where a reader would naturally want to go deeper.
- Never cluster multiple internal links in the same paragraph.
- Never place a link where the linked topic is not being discussed.

### Single-Placement Rule (Hard Requirement)
Every **internal** destination URL appears **exactly once** per article. If the same target page would naturally be referenced in multiple sections, choose the strongest single placement and rewrite the other mentions as plain text without the link. This applies to the core service page, the cluster pillar, sibling cluster articles, and tool/resource pages.

**Statute citations exempt.** A cited statute appears once in the body as a numeric citation marker (`[1]`) and once as the matching Sources entry, by skill design. That dual placement is required, not a violation.

### Lead-In Requirement (Hard Requirement)
The link must be embedded inside a sentence whose meaning is incomplete without the linked topic. The reader should understand WHY they would click before they reach the link. Tag-on patterns are banned:

BAD: "Property division can get complicated. See our [property division page](url)."
- The sentence ended before the link began.

BAD: "For more on these issues, see [X](url), [Y](url), and [Z](url)."
- Multi-link cluster, also banned by the rule above.

GOOD: "How a court divides marital assets depends on the [equitable distribution analysis](url) the judge applies."
- The link is part of the noun phrase the sentence is built around.

Banned tag-on phrases include "See our [topic] page," "Learn more at," "Click here for," "For more on this, see," and any sentence whose only purpose is to deliver a link after the surrounding thought is already complete.

### Anchor Text Rules
**Pillar links:** Use the pillar page's primary keyword or a close variant as anchor text.

**Cluster-to-cluster links (article to article):** Anchor text must be descriptive but must **not** use the target article's primary keyword. Using the target's exact keyword as anchor text splits keyword signal and risks cannibalization.
- Draw from the target article's related keywords, subtopics, or supporting concepts
- Describe the context or outcome the reader will find -- not the keyword the page is targeting
- The anchor should be natural in the sentence and signal relevance without duplicating the target's SEO focus

**Example:**
- Target article primary keyword: "how to choose a CRM for small business"
- Bad anchor: "how to choose a CRM for small business"
- Good anchor: "what to look for in a CRM platform" or "evaluating CRM options for your team"

**Never use:** "click here," "learn more," or any anchor that provides no topical context.

---

## External Linking Rules

### Authoritative Source Citations (Footnote Method)
When an article references a specific statute, regulation, standard, study, or official guideline, cite it using the footnote citation system described below. Apply this **only when the source genuinely adds value for the reader** -- such as when a specific rule or threshold is being explained, a source is cited directly, or a reader would benefit from verifying the authoritative reference.

Do not add citations to satisfy a quota or simply because a rule or regulation is mentioned in passing.

#### In-Body Citation Format
Place the source identifier (statute number, regulation code, study name) in the text at the point of reference, followed by a bracketed sequential number that serves as an anchor link to the Sources section at the bottom of the article.

**Format:** `[source identifier] [N]`

**Example in body text:**
> Florida courts use an income shares model to calculate support obligations based on both parents' earnings. Fla. Stat. sec. 61.30 [1]

- Use the official source identifier (statute number, regulation code, study name) -- never a keyword, descriptive phrase, or topic summary.
  - Correct: `Wis. Stat. sec. 767.335 [1]` or `OSHA 1910.134 [2]` or `the 2024 HubSpot State of Marketing report [3]`
  - Incorrect: `the law that governs this [1]` or `according to research [2]`
- Every citation instance gets its own sequential number, even if the same source is cited more than once. If Fla. Stat. sec. 61.30 appears in paragraph 2 and again in paragraph 8, it is `[1]` at first mention and `[2]` (or whatever the next number is) at second mention, with a corresponding entry for each in the Sources section.
- `[N]` is an anchor link that jumps the reader to the matching entry in the Sources section at the bottom of the article.

#### Sources Section (Required When Citations Exist)
If the article contains any `[N]` citations, add a **Sources** section as the last section of the article, after the CTA. List every citation sequentially.

**Format per entry:**
```
[N] [Full source identifier] | [Full URL]
```

**Example:**
```
## Sources
[1] Fla. Stat. sec. 61.30 | https://www.flsenate.gov/Laws/Statutes/2024/61.30
[2] OSHA 1910.134 | https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.134
[3] Fla. Stat. sec. 61.30 | https://www.flsenate.gov/Laws/Statutes/2024/61.30
```

**Rules:**
- Every external link in the Sources section must be marked `rel="nofollow"` when published. Note this requirement in the meta block or as an inline routing note so the publisher implements it.
- The `[N]` number in the Sources section is the anchor target that the in-body `[N]` links to.
- Sources are listed in the order they appear in the article, not alphabetically.
- Include the full, direct URL to the official source. Do not use shortened URLs or generic domain links.
- If you cannot verify the exact URL for a source, add `[REVIEW FLAG: verify URL for [source identifier]]` on that entry so the publisher can confirm before going live.

### Meta Block (Required Before Title)
Every article must open with a meta block containing:
- Title
- Primary keyword
- Related keywords
- Intent and funnel stage
- Schema type
- All internal link targets with actual URLs
- Cluster pillar link
- Any tool or resource page links

---

## Workflow Rules

### Sequential, Controlled Production
1. Work through articles in the cluster **one at a time, in exact plan order**
2. For each article: state the topic, its position in the cluster, and its connection to the pillar -- then write
3. **Do not move to the next article** until the current one is explicitly approved
4. Do not skip ahead, merge topics, or produce content for later articles in the same pass

### Pre-Writing Checklist (Before Every Article)
Pull and confirm the following from the content plan before writing:
- [ ] Title (exact match from plan)
- [ ] Primary keyword
- [ ] Related keywords
- [ ] Intent and funnel stage
- [ ] Recommended outline (if provided)
- [ ] FAQs
- [ ] Internal link targets with URLs
- [ ] Schema type
- [ ] CTA (use brand's default if blank)

---

## Quality Gate (Before Delivering Any Article)

Do not present an article until every item below is verified:

- [ ] First two paragraphs directly answer the search intent
- [ ] Brand voice loaded at session start is present and consistent throughout
- [ ] Core service page link is the first internal link in the article, placed within the first two paragraphs, using the core page keyword as anchor text
- [ ] Primary keyword appears naturally in the intro and at least 2-3 other locations
- [ ] All internal links from the plan are placed in contextually correct positions
- [ ] Each unique internal destination URL appears EXACTLY ONCE in the article (Single-Placement Rule). Statute body+Sources pairs are exempt.
- [ ] Every internal link is embedded as a lead-in (surrounding prose is *about* the linked topic), not tagged on as "See our X page" or "Learn more at"
- [ ] No bare URL or generic ("click here," "this page," "learn more") used as anchor text
- [ ] Cluster pillar link is present with keyword-rich anchor text
- [ ] No paragraph exceeds 3 sentences (rare exceptions for examples only)
- [ ] Every H2 section is scannable by heading + first sentence
- [ ] FAQ answers are concise and not redundant with the body
- [ ] CTA uses the brand's voice and specified conversion offer
- [ ] If any `[N]` citations exist in the body, a Sources section is present at the end of the article with a matching entry for every `[N]`
- [ ] Every `[N]` in the body has a corresponding `[N]` entry in Sources, and vice versa (no orphans)
- [ ] Sources entries include the full source identifier and a direct URL; nofollow routing note is present
- [ ] Citation numbers are sequential (no gaps, no duplicates) in the order they appear in the body
- [ ] Schema in meta block matches the plan
- [ ] No generic boilerplate that could come from any brand in any industry
- [ ] No keyword stuffing, forced SEO phrasing, or robotic sentence patterns
- [ ] No em dashes
- [ ] No adversarial or combative framing
- [ ] No obvious AI phrasing patterns
- [ ] Expert review pass completed (see Expert Review Flags section): all flagged claims resolved, softened, or qualified before delivery
- [ ] Pre-delivery validator has been run against the output: `node scripts/validate-page.js path/to/article.docx`. The script must exit 0. It hard-fails on duplicate body URLs, tag-on linking patterns, em dashes, banned AI-tells, and citation/Sources mismatches. Do not present the article until the validator passes.

---

## Expert Review Flags (Self-Audit)

Before delivering any article, perform a full review pass scanning for the following. This is your responsibility, not a handoff to the user.

### What to scan for:
- Claims that state or imply a guaranteed outcome
- Categorical legal, medical, financial, or regulatory assertions without qualifying language
- References to a statute, regulation, rule, standard, or case that could have changed
- Specific numbers, thresholds, or deadlines subject to legislative or policy updates
- Pricing benchmarks, feature comparisons, or statistics that could be outdated or market-specific

### How to resolve:
1. **Soften or qualify** the claim. Add appropriate hedging ("in most cases," "as of [year]," "typically," "under current guidelines") so the statement is accurate without overpromising.
2. **Remove guaranteed-outcome language entirely.** Do not publish any sentence that reads as a promise of results.
3. **Run the per-citation claim test on every cited statute or rule.** For each `[N]` citation, read ONLY the cited section's text and ask whether it directly supports the surrounding sentence. A statute about post-decree disputes is NOT authority for an initial-case proposition. A subsection (4) provision is NOT authority for a claim made under subsection (1.5)(b). If the cited section does not directly govern the claim, the citation is misapplied; remove it or replace it with the correct authority. Do not approve a citation just because the section number is real and the topic is adjacent.
4. **Verify subsection-level claims** by reading the subsection itself. Do not conflate adjacent subsections of the same statute.
5. **Check paraphrase fidelity.** Where the article paraphrases a legal term ("rebuttable presumption," "clear and convincing evidence," "shall not be ordered unless"), the paraphrase must match the statute's actual structure. A "shall not... unless" provision is not the same as a rebuttable presumption.
6. **Use [REVIEW FLAG: reason] sparingly** and only for claims you cannot resolve yourself. The flag means "I could not confidently verify or soften this, and a subject-matter expert should confirm before publishing." It does not mean "I noticed something and am passing it along."

The goal is to deliver clean copy. Flags are a last resort for genuine uncertainty, not a checkbox exercise.

---

## Output Format

Deliver each article as a `.docx` file using the `docx` skill. Before building the file, read `/mnt/skills/public/docx/SKILL.md` for formatting requirements.

Default formatting:
- **Arial** as the base font
- Heading styles with brand colors if provided; default to dark navy (#1B3A5C) for H1/H2 and medium blue (#2E75B6) for H3 if no colors are specified
- Proper list formatting (LevelFormat.BULLET / LevelFormat.DECIMAL -- never unicode bullets)
- Meta block in smaller gray text at the top, separated by a horizontal divider
- **Internal links to published/live pages** must be actual `ExternalHyperlink` elements with the full URL, styled as underlined blue text. These are clickable links in the .docx, not styled text for the publisher to implement later.
- **Cross-article links to unpublished cluster articles** (articles that do not yet have a live URL) use styled TextRun (blue italic) with a bracketed routing note, not ExternalHyperlink with placeholder URLs
- **Citation markers** (`[N]`) in the body must be actual `ExternalHyperlink` elements linking directly to the external source URL. Style them as superscript, underlined, blue text. Each `[N]` is a clickable link in the .docx that opens the statute, regulation, or source page.
- **Sources section** at the end of the article uses a standard H2 heading ("Sources"). Each entry shows the bracketed number and full source identifier as plain text, followed by a pipe separator, then the full URL as an actual `ExternalHyperlink` (clickable, underlined blue text). Include a section-level publisher routing note in smaller gray italic text: `[Publisher: all [N] citation links in the body and all external links in this section must use rel="nofollow"]`
