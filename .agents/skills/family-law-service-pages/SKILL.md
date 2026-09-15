---
name: family-law-service-pages
description: "Produce full-copy family law service pages (Core Practice Area hubs and Procedural child pages) delivered as DOCX files. Use this skill whenever the user asks to write, draft, build, or produce a family law service page, practice area page, or legal process page for any family law firm in any U.S. state. Trigger on requests mentioning divorce pages, custody pages, child support pages, alimony pages, property division pages, paternity pages, guardianship pages, or any similar family law service content. Also trigger when the user says 'build the next service page', 'write the core page for [topic]', 'create the procedural page for [topic]', or references a family law site architecture or page hierarchy. Do NOT use for blog content (use cluster-blog-writer instead) or for non-family-law verticals."
---

# Family Law Service Page Writer

## Purpose

This skill produces publication-ready family law service pages as DOCX files. It covers two page types within a defined site architecture:

- **Core Practice Area Pages** -- canonical hub pages for major family law services (Divorce, Child Custody, Child Support, etc.)
- **Procedural Pages** -- child pages under a Core hub that explain a specific legal process, filing pathway, or court-driven workflow (Contested Divorce, Uncontested Divorce, Child Support Modification, etc.)

Every page produced must serve a distinct role in the site hierarchy, maintain clean intent separation, follow strict internal linking rules, reflect the firm's brand voice, and include researched and verified state-specific legal content.

---

## Session Start: Collect Client Context

Before writing any page, confirm you have the following. If a brief or intake document was provided, pull from it. Otherwise, ask the user to supply:

### Required Inputs
1. **Page type** -- Core Practice Area or Procedural
2. **Practice area** -- Divorce, Child Custody, Child Support, Spousal Support/Alimony, Property Division, Paternity, Guardianship
3. **Specific topic** -- for Procedural pages, the exact process (e.g., Contested Divorce, Child Support Enforcement)
4. **State** -- the U.S. state for jurisdiction-specific content
5. **City or region** -- if the firm targets a specific metro or county
6. **Firm name** -- for trust signals and branded references
7. **Firm website URL** -- for internal link construction
8. **Brand voice** -- how the firm sounds. This is not optional. The user should provide a voice brief, style guide, example copy, or verbal description of the firm's personality, tone, and how they talk to clients. If no formal guide exists, ask the user to describe: how the firm would explain something to a prospective client sitting across the table, what words or phrases the firm uses naturally, what tone they avoid, and what makes their voice different from a generic law firm website.
9. **Parent hub URL** -- for Procedural pages, the URL of the Core hub this page lives under

### Conditional Inputs (ask if not provided)
10. **Related Procedural pages** -- titles and URLs of sibling/child procedural pages that exist or are planned
11. **Related Situational pages** -- titles and URLs of situational pages that exist or are planned
12. **Firm differentiators** -- what sets this firm apart (experience, approach, credentials, case results)
13. **Attorney or team info** -- names, titles, credentials for trust signals
14. **State-specific notes** -- any known statutes, terminology, residency rules, filing requirements, or court procedures the user wants included
15. **Local court context** -- county-specific filing details, court names, procedural quirks

### Optional Inputs
16. **Trust signals** -- awards, bar associations, case volume, years of experience, client testimonials
17. **Tools or resources** -- calculators, checklists, downloadable forms the firm offers
18. **Target audience notes** -- who the page primarily speaks to (e.g., mothers filing for custody, high-net-worth spouses)

Once all required inputs are confirmed, state the page type, practice area, state, and proceed to the appropriate template.

---

## Page Type Routing

After collecting inputs, read the appropriate reference template before writing:

- **Core Practice Area Page** → Read `references/core-hub-template.md`
- **Procedural Page** → Read `references/procedural-template.md`

Follow the template section by section. Do not skip required sections. Conditional sections should be included when the practice area or state context warrants them.

---

## Shared Content Standards

These rules apply to both page types.

### Voice and Tone

The firm's brand voice is the primary voice driver. Every section of every page should sound like this firm talking to a prospective client, not like a generic legal content template.

**Before writing anything, internalize the brand voice provided during session start.** Read it, understand it, and write through it. If the firm is direct and no-nonsense, write that way. If the firm is warm and reassuring, write that way. If the firm leads with confidence and aggression, write that way. The voice should be consistent from the first paragraph to the last.

**Where voice shows up:**
- How problems are framed (clinical vs. empathetic vs. urgent vs. matter-of-fact)
- How the firm refers to itself and its work
- How legal concepts are explained (formal vs. conversational vs. plain-spoken)
- Sentence rhythm and word choice
- The "How [FIRM_NAME] Can Help" section especially -- this must sound like the firm, not like boilerplate

**Guardrails that apply regardless of brand voice:**
- Use "you/your" to address the reader. Use "our team" or "[FIRM_NAME]" when referencing the firm.
- Do not make guarantees about legal outcomes.
- Do not use fear-mongering or manufactured urgency.
- Do not use obvious AI phrasing patterns ("navigating the complexities of," "in today's world," "it's important to note").
- Do not use em dashes.

**If no brand voice is provided:** Default to authoritative, empathetic, and direct. The reader is going through one of the hardest experiences of their life. Respect that by leading with substance, not setup. But flag to the user that the output will be stronger once they provide voice direction.

### Readability
- Maximum 3 sentences per paragraph in body sections.
- Keep sentences short and direct. Target 15-25 words per sentence as a baseline. Anything over 30 words should be split or restructured. Legal content does not require legal-length sentences.
- Vary sentence rhythm. Follow a longer explanatory sentence with a short, declarative one. Monotonous sentence length kills readability regardless of word count.
- Every H2 must be scannable: the heading plus the first sentence should communicate the core point.
- Use bullet lists for collections of items, options, factors, or requirements.
- Use numbered lists for sequential steps only.
- No walls of text. Break up dense legal content into digestible blocks.
- Write for a stressed person scanning on their phone, not a paralegal reading at a desk.

### Answer-First Structure
The reader landed on this page with a question. Answer it immediately. Not after a definition. Not after context-setting. The answer comes first.

**Paragraph 1: Answer the question behind the search.**
Ask yourself: what is this person actually trying to find out? A parent searching "child support lawyer Miami" wants to know what determines how much they pay or receive and whether an attorney can help them get a fair result. A parent searching "child custody attorney Florida" wants to know how custody is decided and what they can do to protect their time with their child. Lead with that answer. The primary keyword should appear naturally, but the paragraph's job is to give the reader what they came for, not to define a legal term in the abstract.

**Paragraph 2: Ground the stakes and expand.**
Now that the reader has the answer, tell them why the details matter. What is at risk. What the process looks like at a high level. What they should understand before making decisions. This paragraph earns the reader's attention for the rest of the page.

**What not to do:**
- Do not open with a textbook definition ("Child support is a court-ordered obligation that..."). That is a definition, not an answer.
- Do not open with emotional preamble or empathy statements.
- Do not open with firm history, credentials, or positioning. That comes later.
- Do not open with generic legal disclaimers.

### State-Specific Content: Research and Verification

Before writing any state-specific content, research and verify the legal details for [STATE]. This is not optional. Do the work before drafting, not after.

**What to research for every page:**
- Governing statutes and code sections (e.g., Fla. Stat. sec. 61.30 for child support)
- Residency and filing requirements
- Mandatory waiting periods
- Court process steps and filing procedures
- Statutory factors courts must consider
- Eligibility criteria and qualifying thresholds
- Financial formulas or calculation methods (e.g., income shares model, percentage of income)
- Rights and protections granted by state law
- Consequences of non-compliance or failure to act

**How to handle verified details:**
- Include state-specific details as factual content. Do not hedge with "may" or "might" when the statute is clear.
- Cite specific statutes using the footnote citation format (see Citation Rules below).
- Use the state name naturally throughout the content where jurisdiction matters.
- Integrate local court names, filing locations, and county-specific details when provided by the user.

**How to handle unverifiable details:**
- If a detail is hyper-local (county-specific court rules, specific judge procedures, current filing fee dollar amounts) and the user has not provided it, use a clear placeholder: `[LOCAL DETAIL: describe what goes here]`
- Do not fabricate statute numbers, fee amounts, or case law. If you cannot confirm it, leave a placeholder rather than guessing.
- Placeholders should be rare. Most state-level legal details are researchable.

### Citation Rules

Cite statutes sparingly. The goal is to ground legal claims in authority, not to make the page read like a brief.

**When to cite:**
- Cite a statute at first mention when introducing a specific legal rule, threshold, requirement, or calculation method.
- Do not cite the same statute again after it has been introduced. Once the reader knows Fla. Stat. sec. 61.30 governs child support guidelines, every subsequent reference to the guidelines does not need a repeat citation.

**When not to cite:**
- General descriptions of how a process works (unless introducing a specific rule for the first time)
- Restatements of information already cited earlier on the page
- FAQ answers that summarize content already covered and cited in the body sections above

**In-body format:** Place the official source identifier at the point of first reference, followed by a bracketed sequential number.
Example: `Florida uses an income shares model to calculate child support. Fla. Stat. sec. 61.30 [1]`

**Sources section format (end of document):**
```
[N] [Full source identifier] | [Full URL if available]
```

**Rules:**
- Each unique statute or source gets one citation number. Do not assign multiple numbers to the same statute.
- Aim for no more than 5-8 unique citations on a Core page and 4-6 on a Procedural page. If you are citing more than that, you are over-citing.
- The Sources section appears as the last element of the document.


---

## Internal Linking Rules

These are non-negotiable. They come from the site architecture and exist to prevent cannibalization, consolidate authority, and guide user journeys.

### Single-Placement Rule (Hard Requirement)

Every **internal** destination URL appears **exactly once** per page. No internal URL may be linked from two or more locations on the same page. This applies to procedural children, situational children, and sibling Core hubs.

**Scope clarification:** This rule does NOT apply to external statutory and authority citations. By skill design, a cited statute appears twice on the page: once as a numeric citation marker (e.g., `[1]`) hyperlinked to the statute URL in the body, and once as the corresponding Sources entry. That dual placement is the standard footnote convention and is required, not a violation.

If an internal topic naturally surfaces in multiple sections, choose the strongest single placement (see Strongest-Placement Selection below) and rewrite the other mentions as plain text without the link. Run a duplicate-URL scan before delivery, with the body-vs-Sources statute pattern excluded.

### Strongest-Placement Selection

When deciding where to place a single link, prefer the location where the surrounding prose is most directly *about* the linked page's topic. Hierarchy of strength, strongest first:

1. Body section paragraph or bullet whose subject matter IS the linked page's topic (e.g., the "supervised visitation" link sits in the bullet that defines supervised parenting time).
2. FAQ question whose answer would otherwise duplicate the linked page's purpose.
3. Section transition paragraph that introduces a related sub-topic.

Never choose: a generic "Related Resources" cluster, a "See also" footer paragraph, or a multi-link sentence that bundles unrelated children together.

### Lead-In Requirement (Hard Requirement)

The link must be embedded inside a sentence whose meaning is incomplete without the linked topic. The reader should understand WHY they would click before they reach the link. The surrounding prose leads INTO the linked topic; the link is not tagged on after the thought is already finished.

GOOD: "These cases are governed by a separate analysis under Colorado's [relocation and move-away framework](url)."
- The sentence is about the relocation framework. The link IS the topic.

GOOD: "A well-built [Colorado parenting plan](url) governs holidays, school breaks, transportation, and how disputes get resolved."
- The link is part of the noun phrase the sentence is built around.

BAD: "Colorado has its own relocation rules. See [Colorado relocation and move-away disputes](url)."
- The link is a tagged-on "see also." The sentence ended before the link began.

BAD: "For deeper guidance on individual processes, see our pages on [X](url), [Y](url), and [Z](url)."
- This is a resources-dump cluster. Three links in one sentence, none of them earned by the surrounding prose.

### Banned Linking Patterns

- "See our [topic] page" sentences appended to a paragraph
- "Learn more at [link]" or "Click here for [link]" tag-ons
- Multi-link clusters (two or more links in the same sentence) outside the dedicated Related Topics module
- "Resources" or "Helpful links" subsections in the body
- Any link whose anchor text is the bare URL or a generic phrase like "click here," "this page," or "learn more"
- The same destination URL used as multiple distinct anchors anywhere on the page

### Core Practice Area Pages
- **Required structural links out:** Link to each published Procedural child page. Each child page is linked exactly once, at its strongest placement.
- **Allowed secondary contextual links:** Max 4 links to related Core pages (e.g., Divorce hub linking to Child Custody hub where topics overlap). These go in the Related Topics module near the bottom. They are not primary navigation. Each related Core hub appears exactly once.
- **Required structural links in:** Every Procedural page under this hub must link back to it.

### Procedural Pages
- **Required structural link out:** Link back to the parent Core hub. Linked exactly once.
- **Allowed sibling links:** Cross-link to directly relevant sibling Procedural pages only when comparison is genuinely useful (e.g., Contested vs. Uncontested Divorce). Max 2 sibling cross-links, each linked exactly once.
- **Allowed secondary contextual links:** Max 3 links to related content outside the immediate hub. These go inline where process overlaps naturally, in a Next Steps module, or in a brief Related Issues list near the bottom. Each destination linked exactly once.
- **Bridge to Situational pages:** When the content naturally leads to a specific scenario (e.g., a Contested Divorce page referencing high-conflict situations), link to the relevant Situational page if it exists. Once.

### Placement Rules
- Internal links go inline within relevant content, not clustered in a generic "Resources" dump.
- The "Related Topics" or "Related Issues" module near the bottom is for secondary contextual links only, not for repeating structural links already placed above.
- A "Next Steps" module is the appropriate place for directional links to the next logical page in the user journey.

### Link Implementation in DOCX Output
All links in the DOCX must be functional, clickable hyperlinks using `ExternalHyperlink` from docx-js. No bracket annotations. No placeholder text. Real links.

**Internal page links:**
- Use the anchor text as the visible hyperlink text. Style it bold and in a distinct color (e.g., #2E5090).
- The `link` property on ExternalHyperlink should point to the full target URL (e.g., `https://[firm-domain]/florida/child-support/child-support-modification/`).
- If the firm domain is unknown, use the relative path as the link target and note it for the dev team.

**Citation reference links:**
- Each in-body citation marker (e.g., `[1]`) must be a clickable hyperlink that links directly to the statute URL.
- Style citation markers as superscript or bracketed, in a muted color (e.g., #666666), so they do not interrupt reading flow.

**Sources section links:**
- Each entry in the Sources section must include a clickable hyperlink to the source URL.

---

## DOCX Output Requirements

Every page is delivered as a .docx file. Follow the docx skill's creation process using `docx-js` via Node.

### Document Structure
- US Letter page size (12240 x 15840 DXA)
- 1-inch margins
- Arial font family
- Body text: 12pt
- H1: 18pt bold
- H2: 15pt bold
- H3: 13pt bold
- Clean paragraph spacing (120 DXA before/after body paragraphs, 240 before headings)

### Content Formatting
- Use proper heading levels (H1 for page title, H2 for main sections, H3 for subsections)
- Use docx-js bullet lists (LevelFormat.BULLET), never unicode bullets
- All internal links and citation references must be functional hyperlinks (see Link Implementation above)
- Use a consistent callout style for `[LOCAL DETAIL]` placeholders -- bold, bracketed notation that's easy to find and fill
- FAQ sections use H3 for each question

### Skimmability
The reader is stressed, distracted, and probably on their phone. Every section must be scannable without reading every word.
- H2 headings should work as a standalone table of contents. A reader who only reads the H2s should understand the full scope of the page.
- The first sentence after every H2 must deliver the section's core point. If a reader only reads the heading and the first sentence, they should get the essential takeaway.
- Use bold lead-ins at the start of bullet points to let readers scan a list without reading full sentences.
- Keep bullet point text to 1-2 sentences after the bold lead-in. If a bullet needs more than that, it should be its own H3 subsection.
- Use whitespace aggressively. Generous spacing between sections (360+ DXA before H2s, 280+ before H3s). No visual clutter.
- No paragraph should require re-reading to understand. If a sentence is complex, split it.

### File Naming
`[state]-[practice-area]-[page-type].docx`
Examples: `florida-divorce-core.docx`, `florida-contested-divorce-procedural.docx`

### Validation
After generating the DOCX, run two scans before presenting it to the user:

1. `python scripts/office/validate.py` for structural validation.
2. `node scripts/validate-page.js path/to/page.docx` (provided alongside this skill) for the page-level pre-delivery scan: duplicate-URL detection, banned linking patterns, em-dash detection, banned-phrase detection, and "North Star" usage count. The script exits non-zero if any hard rule fails. Do not present the file until the validator passes.

---

## Quality Gates

Before delivering the DOCX, verify the following. If any gate fails, fix it before presenting:

1. **Intent separation** -- Does this page serve its designated role (broad service intent for Core, process intent for Procedural) without drifting into the other type's territory?
2. **Answer-first** -- Do the first two paragraphs directly address the primary search intent?
3. **Internal links** --
   a. Are all required structural links present?
   b. Does each unique destination URL appear EXACTLY ONCE? Run a duplicate-URL scan before delivery.
   c. Is each link embedded as a lead-in (surrounding prose is *about* the linked topic), NOT as a tag-on "See our X page"?
   d. Are any links clustered in a multi-link sentence outside the Related Topics module? If yes, redistribute them to their strongest individual placements.
   e. Are secondary contextual links within the allowed maximums?
4. **State-specific verification** -- Have all state-specific legal claims been researched and verified? Are statutes cited with proper footnote references?
   - **Per-citation claim test:** For every statute cited, read ONLY the cited section's text and ask whether it directly supports the surrounding sentence. A statute about post-decree disputes is NOT authority for an initial-case proposition. A statute about subsection (4) is NOT authority for a claim made under subsection (1.5)(b). If the cited section does not directly govern the claim, the citation is misapplied; remove it or replace it with the correct authority.
   - **Subsection precision:** When citing a subsection, verify the subsection actually contains what the page claims it contains. Do not conflate adjacent subsections.
   - **Statutory paraphrase fidelity:** Where the page paraphrases a legal term ("rebuttable presumption," "clear and convincing evidence," "shall not be ordered unless"), the paraphrase must match the statute's actual structure. If the statute uses a "shall not… unless" structure, do not call it a "rebuttable presumption" without flagging the simplification.
   - Are any remaining `[LOCAL DETAIL]` placeholders limited to truly unverifiable hyper-local information?
5. **No cannibalization risk** -- Does this page avoid competing with its parent hub (for Procedural pages) or its child pages (for Core pages) for the same keyword intent?
6. **Paragraph discipline** -- No paragraph exceeds 3 sentences in body content?
7. **No fabricated law** -- No invented statute numbers, case names, or filing details? Every legal reference is research-backed?
8. **Citation discipline** -- Is each statute cited only once at first mention? Are there no more than 5-8 unique citations on a Core page or 4-6 on a Procedural page? Does the page read like a service page, not a legal brief?
9. **Sentence length** -- Are sentences predominantly 15-25 words? Have any sentences over 30 words been split or restructured?
10. **Readability** -- Is the page scannable? Would a stressed person in a legal crisis be able to find what they need quickly?

---

## Known Cluster Architecture

Use this reference to understand the expected page relationships when planning links and avoiding overlap.

### Divorce
- Procedural: Contested Divorce, Uncontested Divorce, Legal Separation, Divorce Mediation, Collaborative Divorce
- Situational: High-Conflict Divorce

### Child Custody
- Procedural: Child Custody Modification, Parenting Plans, Emergency Custody Orders
- Situational: Relocation/Move-Away Disputes, High-Conflict Custody, Parenting Time Disputes, Supervised Visitation

### Child Support
- Procedural: Child Support Modification, Child Support Enforcement
- Situational: Support Disputes After Income Changes, Back Child Support/Arrears, Self-Employed or Variable Income Support

### Spousal Support / Alimony
- Procedural: Temporary Spousal Support, Long-Term Spousal Support
- Situational: Long-Term Marriage Divorce, High-Income Spousal Support Disputes

### Property Division
- Procedural: Equitable Distribution, Marital vs. Separate Property
- Situational: Divorce Involving Business Ownership, Business Valuation and Division, Hidden Assets and Financial Misconduct

### Paternity
- Procedural: Establishing Paternity, Challenging Paternity

### Guardianship
- Procedural: Guardianship of a Minor, Adult Guardianship, Temporary Guardianship
- Situational: Emergency Guardianship

---

## Publishing Sequence Awareness

When the user asks to build a page, verify where it falls in the production order:

1. Core Practice Area hubs are built first.
2. Highest-priority Procedural pages are built immediately after their hub.
3. Remaining Procedural pages follow after the hub exists.

If a user requests a Procedural page and the Core hub does not yet exist, flag this: "The parent Core hub for [PRACTICE_AREA] should be built first to establish the authority anchor. Want to start there instead, or proceed with the Procedural page knowing the hub will follow?"

For Divorce specifically: Contested Divorce and Uncontested Divorce are the first two Procedural pages after the hub.
