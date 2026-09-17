---
name: family-law-situational-pages
description: "Produce full-copy family law situational pages delivered as DOCX files. Use this skill whenever the user asks to write, draft, build, or produce a family law situational page, scenario page, fact-pattern page, or issue-specific service page for any family law firm in any U.S. state. Trigger on requests mentioning high-conflict divorce, relocation disputes, move-away custody, hidden assets, business-ownership divorce, back child support, fathers' rights, supervised visitation, grandparents guardianship, or any similar family law scenario page. Also trigger when the user says 'build the situational page for [topic]', 'write the scenario page for [topic]', or references a family law site architecture where the page lives under a core hub but is not a process page. Do NOT use for Core Practice Area pages or Procedural pages (use family-law-service-pages instead). Do NOT use for blog content (use cluster-blog-writer instead) or for non-family-law verticals."
---

# Family Law Situational Page Writer

## Local repository status

> **LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL**

The imported transfer omitted the template and executable validation workflow named below. This repository now has a bounded local replacement for the demonstrated `FL-M008` High-Conflict Divorce route only. Read `LOCAL-REPLACEMENT.md` before use. Other Situational nodes remain dependency-incomplete and must be reported as pending rather than routed through this workflow.

For `FL-M008`, the governing Family Law V2 HTML remains authoritative for classification, hierarchy, and its explicitly recorded relationships. The local schema distinguishes that authority from three separate requirements: one skill-required parent-Hub navigation link to the actual V2 parent, one skill-required process bridge to `FL-M004` Contested Divorce under that parent, and one consultation CTA. The parent and process links are not claimed as outgoing V2 edges and must omit `v2_edge_id`; additional architecture links still require exact outgoing V2 edges. Every destination requires a documented direct-200, zero-redirect, right-service screen. This replacement does not use the Core Hub content template.

## Purpose

This skill produces publication-ready family law situational pages as DOCX files. It covers one page type within a defined site architecture:

- **Situational Pages** -- child pages under a Core Practice Area hub that explain a specific client circumstance, fact pattern, high-friction scenario, or real-world problem with clear legal-service relevance (Relocation and Move-Away Custody Disputes, High-Conflict Divorce, Hidden Assets and Financial Misconduct, etc.)

Situational pages are not broad Core Practice Area hubs. They are not Procedural pages. They are not blog posts or educational articles with a contact form attached.

Every page produced must serve a distinct role in the site hierarchy, maintain clean intent separation, follow strict internal linking rules, reflect the firm's brand voice, and include researched and verified state-specific legal content.

---

## Session Start: Collect Client Context

Before writing any page, confirm you have the following. If a brief or intake document was provided, pull from it. Otherwise, ask the user to supply:

### Required Inputs
1. **Practice area** -- Divorce, Child Custody, Child Support, Spousal Support/Alimony, Property Division, Paternity, Guardianship
2. **Specific situation/topic** -- the exact client problem or fact pattern (e.g., High-Conflict Divorce, Relocation and Move-Away Disputes, Hidden Assets and Financial Misconduct, Fathers' Rights in Custody Cases)
3. **State** -- the U.S. state for jurisdiction-specific content
4. **City or region** -- if the firm targets a specific metro or county
5. **Firm name** -- for trust signals and branded references
6. **Firm website URL** -- for internal link construction
7. **Brand voice** -- how the firm sounds. This is not optional, and this skill does not ask the user to describe the voice in free text if a canonical voice skill exists for the client.

   **Voice skill load is a hard prerequisite.** Before writing any page content, check for a matching client voice skill in the available skills list. Voice skills follow the naming pattern `[client-shortname]-voice` (examples: `sterling-voice`, `vasquezdelara-voice`, `tde-voice`, `scottbrown-voice`, `lisavance-voice`, `lancaster-voice`, `johnsonlgroup-voice`, `ramage-voice`, `meyerpink-voice`, `kalish-voice`, `gjesdahl-voice`, `fanash-voice`, `drake-voice`, `aurit-voice`, `cutrer-voice`).

   **If a matching voice skill exists:** Read the full SKILL.md for that voice skill before drafting. The voice skill is canonical. It defines who the firm is, how they sound, what they sell, and where the guardrails are. User-provided voice direction in this session supplements the voice skill but does not override it. If the user provides guidance that conflicts with the voice skill, default to the voice skill and flag the conflict for resolution.

   **If no matching voice skill exists:** Ask the user to supply a voice brief, style guide, example copy, or verbal description covering how the firm explains things to a prospective client, the words and phrases they use naturally, the tone they avoid, and what differentiates them from a generic law firm website. Recommend building a voice skill for the client before producing more pages.
8. **Parent hub URL** -- the Core Practice Area hub this page lives under
9. **Closest related Procedural page(s)** -- titles and URLs of the process page or pages this situation most naturally bridges to. If they do not exist yet, the user should say so.

### Conditional Inputs (ask if not provided)
10. **Related Situational pages** -- titles and URLs of adjacent scenario pages that exist or are planned
11. **Related Core or Procedural pages** -- titles and URLs of adjacent pages outside the immediate parent/process relationship
12. **Firm differentiators** -- what sets this firm apart (experience, approach, credentials, case results)
13. **Attorney or team info** -- names, titles, credentials for trust signals
14. **State-specific notes** -- any known statutes, terminology, procedural posture, or substantive issues the user wants included
15. **Local court context** -- county-specific filing details, court names, procedural quirks
16. **Target audience notes** -- who the page primarily speaks to (e.g., mothers opposing relocation, fathers seeking parenting time, spouses who suspect hidden assets)

### Optional Inputs
17. **Trust signals** -- awards, bar associations, case volume, years of experience, client testimonials
18. **Tools or resources** -- calculators, checklists, downloadable forms the firm offers
19. **Known internal link rules or URL conventions** -- if the site uses a specific naming structure
20. **Target keyword notes** -- if the user already has keyword mapping or search-intent data

Once all required inputs are confirmed, restate the situation, parent hub, closest procedural path, state, and proceed through the Classification Gate before writing.

---

## Classification Gate

Before writing, classify the requested topic. This step is mandatory.

A requested topic must be classified as one of the following:

- **Core Practice Area Page** -- broad service hub
- **Procedural Page** -- legal process, filing pathway, court mechanism, or formal case route
- **Situational Page** -- specific client circumstance, fact pattern, high-friction issue, or real-world problem with clear hiring relevance
- **Blog / Educational Page** -- primarily informational or thought-leadership content

### Fast Classification Test

- **Broad service category** = Core Practice Area
- **Process / mechanism / pathway** = Procedural
- **Scenario / problem / fact pattern** = Situational
- **Topic education without strong service intent** = Blog / Educational

### Critical Distinction

A Procedural page is about the **legal pathway**.

A Situational page is about the **client's problem within that pathway**.

### Examples

- **Child Custody Lawyer in Illinois** = Core Practice Area
- **Child Custody Modification in Illinois** = Procedural
- **Relocation and Move-Away Custody Disputes in Illinois** = Situational
- **5 Things Parents Should Know Before Requesting a Relocation After Divorce** = Blog / Educational

- **Emergency Child Custody Orders in Illinois** = Procedural
- **Custody Cases Involving Abuse, Neglect, or Immediate Safety Concerns in Illinois** = Situational
- **What to Do If Your Child Is in Immediate Danger During a Custody Dispute** = Blog / Educational

- **Divorce Mediation in Florida** = Procedural
- **High-Conflict Divorce in Florida** = Situational
- **Is Mediation Better Than Court in Florida Divorce Cases?** = Blog / Educational

### If the Topic Fails the Gate

If the topic is not truly Situational, do not force it into that category. State the correct classification, explain why, and recommend the proper architectural role. Where appropriate, suggest a valid situational reframing.

Examples:
- If the user requests **Contested Divorce**, explain that it is Procedural, not Situational.
- If the user requests **What Is Equitable Distribution?**, explain that it is Blog / Educational unless recast as a service or scenario page.
- If the user requests **Hidden Assets in Divorce**, explain whether the page belongs under Divorce or Property Division based on which cluster most clearly owns the intent.

---

## Page Type Routing

After collecting inputs and passing the Classification Gate:

1. **Confirm voice skill is loaded.** Before reading the template or drafting any content, verify the matching `[client]-voice` skill has been read in full. If it has not, load it now. If no matching voice skill exists and the user has not supplied a voice brief, stop and resolve that before proceeding.
2. **Read the template.** `references/situational-template.md`

Follow the template section by section. Do not skip required sections. Conditional sections should be included when the practice area, fact pattern, or state context warrants them.

If the topic does not qualify as Situational, stop and return the correct classification instead of drafting the page.

---

## Shared Content Standards

These rules apply to every Situational page.

### Voice and Tone

The firm's brand voice is the primary voice driver. Every section of every page should sound like this firm talking to a prospective client, not like a generic legal content template.

**Before writing anything, internalize the loaded voice skill.** The matching `[client]-voice` skill was loaded at session start as a hard prerequisite. Read it, understand it, and write through it. If the firm is direct and no-nonsense, write that way. If the firm is warm and reassuring, write that way. If the firm leads with confidence and aggression, write that way. The voice should be consistent from the first paragraph to the last.

**Voice skill authority:** The loaded voice skill is canonical. It defines positioning, tone, cadence, vocabulary, phrases to use, phrases to avoid, and brand guardrails. User-provided voice direction for this session supplements but does not override. If session direction conflicts with the voice skill, default to the voice skill.

**Where voice shows up:**
- How the situation is framed (clinical vs. empathetic vs. urgent vs. matter-of-fact)
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

**If no voice skill and no user-provided voice brief exist:** Default to authoritative, empathetic, and direct. The reader is going through one of the hardest experiences of their life. Respect that by leading with substance, not setup. Flag to the user that the output will be stronger once a voice skill is built for the client, and recommend doing that before producing additional pages.

### Readability

- Maximum 3 sentences per paragraph in body sections.
- Keep sentences short and direct. Target 15-25 words per sentence as a baseline. Anything over 30 words should be split or restructured. Legal content does not require legal-length sentences.
- Vary sentence rhythm. Follow a longer explanatory sentence with a short, declarative one. Monotonous sentence length kills readability regardless of word count.
- Every H2 must be scannable: the heading plus the first sentence should communicate the core point.
- Use bullet lists for collections of factors, risks, documents, options, or decision points.
- Use numbered lists for sequential steps only. Situational pages generally summarize process rather than walking through every step.
- No walls of text. Break up dense legal content into digestible blocks.
- Write for a stressed person scanning on their phone, not a paralegal reading at a desk.

### Answer-First Structure

The reader landed on this page with a question. Answer it immediately. Not after a definition. Not after context-setting. The answer comes first.

**Paragraph 1: Answer the question behind the search.**
Ask yourself: what is this person actually trying to find out? A parent searching "can I move out of state with my child after divorce in Illinois" wants to know whether court approval may be required, what factors matter, and what legal obstacles could stop the move. A spouse searching "my husband is hiding assets in divorce" wants to know what signs matter, what remedies may be available, and how a lawyer can respond. Lead with that answer. The primary keyword should appear naturally, but the paragraph's job is to give the reader what they came for, not to define the topic in the abstract.

**Paragraph 2: Ground the stakes and expand.**
Now that the reader has the answer, tell them why the details matter. What is at risk. What related legal process usually gets triggered. What they should understand before making decisions. This paragraph earns the reader's attention for the rest of the page.

**What not to do:**
- Do not open with a textbook definition.
- Do not open with emotional preamble or empathy statements.
- Do not open with firm history, credentials, or positioning. That comes later.
- Do not open with generic legal disclaimers.
- Do not open with listicle framing ("Here are five things to know"). That is article behavior, not service-page behavior.

### Situational Page Definition and Writing Standard

A Situational page is a **commercially relevant, scenario-specific legal page**.

It should not read like a broad service hub. It should not read like a full process guide. It should not read like a blog article in disguise.

A strong Situational page sits between two bad extremes:

- **Too procedural** -- it turns into a dry explanation of the legal mechanism and forgets the lived conflict that brought the reader here.
- **Too blog-like** -- it turns into an educational article with loose structure, weak commercial intent, and no clear architectural role.

The correct writing standard is:

**core service page + scenario specificity + selective procedural explanation**

A Situational page should borrow:
- From a service page: structure, clarity, commercial relevance, and conversion support
- From a strong article: specificity, realism, nuance, and practical relevance

A Situational page must not become:
- A blog post in disguise
- A generic explainer
- A listicle
- A soft educational article with weak hiring relevance
- A keyword catch-all
- An FAQ dump with no clear page intent
- A diluted hybrid that overlaps the parent hub or a Procedural page

A Situational page must:
- Define the specific situation clearly
- Explain why the situation creates legal conflict or strategic difficulty
- Show what is at stake
- Identify the issues courts and lawyers often focus on
- Explain common complications, risks, and mistakes
- Bring in only the procedural explanation needed to show the next legal path
- Explain how legal representation helps in this scenario

### State-Specific Content: Research and Verification

Before writing any state-specific content, research and verify the legal details for [STATE]. This is not optional. Do the work before drafting, not after.

**What to research for every page:**
- Governing statutes and code sections relevant to the situation
- Statutory factors, presumptions, burdens, or thresholds that apply
- Rights, protections, remedies, or limitations tied to the specific fact pattern
- Related procedural pathways and filing mechanisms the situation commonly triggers
- Evidence, documentation, or factual showings that matter
- Consequences of non-compliance, delay, concealment, interference, or bad conduct where relevant

**How to handle verified details:**
- Include state-specific details as factual content. Do not hedge with "may" or "might" when the statute is clear.
- Cite specific statutes using the footnote citation format (see Citation Rules below).
- Use the state name naturally throughout the content where jurisdiction matters.
- Integrate local court names, filing locations, and county-specific details when provided by the user.

**How to handle unverifiable details:**
- If a detail is hyper-local (county-specific court rules, specific judge procedures, current filing fee dollar amounts) and the user has not provided it, use a clear placeholder: `[LOCAL DETAIL: describe what goes here]`
- Do not fabricate statute numbers, fee amounts, case law, or county-specific practices. If you cannot confirm it, leave a placeholder rather than guessing.
- Placeholders should be rare. Most state-level legal details are researchable.

### Citation Rules

Cite statutes sparingly. The goal is to ground legal claims in authority, not to make the page read like a brief.

**When to cite:**
- Cite a statute at first mention when introducing a specific legal rule, factor set, threshold, burden, or remedy.
- Do not cite the same statute again after it has been introduced. Once the reader knows which law governs the issue, every subsequent reference does not need a repeat citation.

**When not to cite:**
- General descriptions of how a situation commonly arises unless a specific legal rule is being introduced
- Restatements of information already cited earlier on the page
- FAQ answers that summarize content already covered and cited in the body sections above

**In-body format:** Place the official source identifier at the point of first reference, followed by a bracketed sequential number.
Example: `Illinois courts evaluate the child's best interests using statutory factors listed in 750 ILCS 5/602.7 [1]`

**Sources section format (end of document):**
```text
[N] [Full source identifier] | [Full URL if available]
```

**Rules:**
- Each unique statute or source gets one citation number. Do not assign multiple numbers to the same statute.
- Aim for no more than 4-6 unique citations on a Situational page. If you are citing more than that, you are over-citing.
- The Sources section appears as the last element of the document.

---

## Internal Linking Rules

The generic defaults in this imported section remain advisory outside a governing client architecture. For the demonstrated local `FL-M008` route, V2 controls classification, hierarchy, and any link asserted as an explicit V2 relationship. A missing V2 edge does not cancel the skill's separate parent-navigation or process-bridge requirements. Schema version 2 records each link's actual `supporting_authority`: `skill-parent-navigation` for the actual V2 parent Hub, `skill-process-bridge` for bounded `FL-M004`, `consultation-cta` for the final contact invitation, or `v2-explicit-relationship` for an additional exact outgoing V2 edge. Do not assign a `v2_edge_id` to the two skill-required links or the CTA.

### Single-Placement Rule (Hard Requirement)

Every **internal** destination URL appears **exactly once** per page. No internal URL may be linked from two or more locations on the same page. This applies to the parent Core hub, sibling Situational pages, Procedural bridges, and any other internal page linked from this content.

**Scope clarification:** This rule does NOT apply to external statutory and authority citations. By skill design, a cited statute appears twice on the page: once as a numeric citation marker (e.g., `[1]`) hyperlinked to the statute URL in the body, and once as the corresponding Sources entry. That dual placement is the standard footnote convention and is required, not a violation.

If a topic naturally surfaces in multiple sections, choose the strongest single placement (see Strongest-Placement Selection below) and rewrite the other mentions as plain text without the link. Run a duplicate-URL scan before delivery, with the body-vs-Sources statute pattern excluded.

### Strongest-Placement Selection

When deciding where to place a single link, prefer the location where the surrounding prose is most directly *about* the linked page's topic. Hierarchy of strength, strongest first:

1. Body section paragraph or bullet whose subject matter IS the linked page's topic.
2. FAQ question whose answer would otherwise duplicate the linked page's purpose.
3. Section transition paragraph that introduces a related sub-topic.
4. Next Steps module (for the directional bridge to the most likely Procedural pathway).

Never choose: a generic "Related Resources" cluster, a "See also" footer paragraph, or a multi-link sentence that bundles unrelated pages together.

### Lead-In Requirement (Hard Requirement)

The link must be embedded inside a sentence whose meaning is incomplete without the linked topic. The reader should understand WHY they would click before they reach the link. The surrounding prose leads INTO the linked topic; the link is not tagged on after the thought is already finished.

GOOD: "When the dispute centers on a planned move, the case shifts into Colorado's [relocation and move-away framework](url)."
- The sentence is about the linked framework. The link IS the topic.

BAD: "Colorado has its own relocation rules. See [Colorado relocation and move-away disputes](url)."
- The link is a tagged-on "see also."

BAD: "For more, see our pages on [X](url), [Y](url), and [Z](url)."
- Multi-link cluster. Resources dump.

### Banned Linking Patterns

- "See our [topic] page" sentences appended to a paragraph
- "Learn more at [link]" or "Click here for [link]" tag-ons
- Multi-link clusters (two or more links in the same sentence) outside the dedicated Related Issues / Next Steps module
- "Resources" or "Helpful links" subsections in the body
- Any link whose anchor text is the bare URL or a generic phrase like "click here," "this page," or "learn more"
- The same destination URL used as multiple distinct anchors anywhere on the page

### Situational Pages

- **Required structural link out:** Link back to the parent Core Practice Area hub. Linked exactly once at its strongest placement.
- **Required process bridge:** Link to the closest relevant Procedural page when it exists. A Situational page should usually point the reader toward the legal pathway most likely to apply. Linked exactly once.
- **Allowed sibling situation links:** Cross-link to directly adjacent Situational pages only when comparison is genuinely useful. Max 2 sibling Situational cross-links, each linked exactly once.
- **Allowed secondary contextual links:** Max 3 links to related content outside the immediate parent/process relationship. These go inline where overlap is genuine, in a Next Steps module, or in a brief Related Issues list near the bottom. Each destination linked exactly once.
- **Do not use links to compensate for bad classification.** If a section starts doing another page's full job, cut it back and link instead.

### Relationship to Other Page Types

- **Core Practice Area hubs** should link down to Situational pages when a scenario is naturally referenced.
- **Procedural pages** should bridge to Situational pages when the process commonly turns on a specific conflict or complication.
- **Situational pages** do not replace either page type. They sit between broad service intent and process intent.

### Placement Rules

- Internal links go inline within relevant content, not clustered in a generic "Resources" dump.
- The "Related Issues" module near the bottom is for secondary contextual links only, not for repeating structural links already placed above.
- A "Next Steps" module is the appropriate place for directional links to the next logical page in the user journey.

### Link Implementation in DOCX Output

All links in the DOCX must be functional, clickable hyperlinks using `ExternalHyperlink` from docx-js. No bracket annotations. No placeholder text. Real links.

**Internal page links:**
- Use the anchor text as the visible hyperlink text. Style it bold and in a distinct color (e.g., #2E5090).
- The `link` property on ExternalHyperlink should point to the full target URL (e.g., `https://[firm-domain]/illinois/child-custody/relocation-disputes/`).
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
`[state]-[specific-topic]-situational.docx`
Examples: `illinois-relocation-disputes-situational.docx`, `florida-high-conflict-divorce-situational.docx`

### Validation

After generating the DOCX, run two scans before presenting it to the user:

1. `python3 scripts/office/validate.py path/to/page.docx --manifest path/to/workflow-input.json` for structural validation.
2. `node scripts/validate-page.js path/to/page.docx --manifest path/to/workflow-input.json` for the page-level pre-delivery scan.

For the locally demonstrated route, generate with `node scripts/build-situational.js path/to/workflow-input.json path/to/florida-high-conflict-divorce-situational.docx` and render with `scripts/render-situational.sh ... --output_dir path/to/empty-directory`. Run `python3 scripts/test-situational.py` before relying on the workflow. The scripts exit non-zero if any tested hard rule fails.

---

## Quality Gates

Before delivering the DOCX, verify the following. If any gate fails, fix it before presenting:

1. **Classification accuracy** -- Is the topic truly Situational and not better treated as a Core, Procedural, or Blog page?
2. **Intent separation** -- Does this page serve scenario-specific service intent without drifting into broad hub copy or a full process guide?
3. **Answer-first** -- Do the first two paragraphs directly address the primary situational search intent?
4. **Structural links** --
   a. Does the local `FL-M008` manifest contain exactly one `skill-parent-navigation` link to its actual V2 parent, exactly one `skill-process-bridge` link to `FL-M004`, and exactly one `consultation-cta` after the final CTA heading?
   b. Do the parent and process links omit `v2_edge_id` and remain described as skill-required navigation, not outgoing V2 edges? Does the CTA omit every V2 target/path/edge field?
   c. Does every additional `v2-explicit-relationship` link identify an exact outgoing V2 edge and pass the V2 target gate?
   d. Does every destination have dated direct-200, zero-redirect, right-service evidence?
   e. Does each unique destination URL appear EXACTLY ONCE? Run a duplicate-URL scan before delivery. (Statute body+Sources pairs are exempt.)
   f. Is each link embedded as a lead-in (surrounding prose is *about* the linked topic), NOT as a tag-on "See our X page"?
   g. Are any links clustered in a multi-link sentence outside the Related Issues / Next Steps module? If yes, redistribute them to their strongest individual placements.
   h. Are secondary contextual links within the allowed maximums?
5. **Selective process explanation** -- Does the page explain only as much procedure as the reader needs before routing them to the Procedural page?
6. **Not blog-like** -- Does the page avoid listicle framing, article-style sprawl, and loose educational tone?
7. **State-specific verification** -- Have all state-specific legal claims been researched and verified? Are statutes cited with proper footnote references?
   - **Per-citation claim test:** For every statute cited, read ONLY the cited section's text and ask whether it directly supports the surrounding sentence. A statute about post-decree disputes is NOT authority for an initial-case proposition. A statute about subsection (4) is NOT authority for a claim made under subsection (1.5)(b). If the cited section does not directly govern the claim, the citation is misapplied; remove it or replace it with the correct authority.
   - **Subsection precision:** When citing a subsection, verify the subsection actually contains what the page claims it contains. Do not conflate adjacent subsections.
   - **Statutory paraphrase fidelity:** Where the page paraphrases a legal term ("rebuttable presumption," "clear and convincing evidence," "shall not be ordered unless"), the paraphrase must match the statute's actual structure.
   - Are any remaining `[LOCAL DETAIL]` placeholders limited to truly unverifiable hyper-local information?
8. **No cannibalization risk** -- Does this page avoid competing with the parent hub or a Procedural page for the same keyword intent?
9. **Paragraph discipline** -- No paragraph exceeds 3 sentences in body content?
10. **No fabricated law** -- No invented statute numbers, case names, filing details, or local court practices? Every legal reference is research-backed?
11. **Citation discipline** -- Is each statute cited only once at first mention? Are there no more than 4-6 unique citations? Does the page read like a service page, not a legal brief?
12. **Readability** -- Is the page scannable? Would a stressed person in a legal crisis be able to find what they need quickly?
13. **Voice skill fidelity** -- Was the matching `[client]-voice` skill loaded before drafting? Does the page read like that specific firm, not a generic family law site? Does the tone, cadence, vocabulary, and positioning match the voice skill's guardrails? Do the flagship sections (opening paragraphs, "How [FIRM_NAME] Can Help," CTAs) especially sound on-brand?

---

## Known Cluster Architecture

Use this reference to understand expected page relationships when planning links and avoiding overlap.

### Divorce
- Related Procedural: Contested Divorce, Uncontested Divorce, Legal Separation, Divorce Mediation, Collaborative Divorce
- Situational: High-Conflict Divorce, Military Divorce, Divorce During Pregnancy, Divorce Involving Domestic Violence
- Usually routed elsewhere: Hidden Assets and Financial Misconduct, Business Ownership, and Business Valuation typically belong under Property Division; Long-Term Marriage Divorce often belongs under Spousal Support / Alimony

### Child Custody
- Related Procedural: Child Custody Modification, Parenting Plans, Emergency Custody Orders
- Situational: Relocation / Move-Away Disputes, High-Conflict Custody, Parenting Time Disputes, Supervised Visitation, Custody Cases Involving Abuse or Neglect, Fathers' Rights in Custody Cases, Custody for Unmarried Parents

### Child Support
- Related Procedural: Child Support Modification, Child Support Enforcement
- Situational: Support Disputes After Income Changes, Back Child Support / Arrears, Self-Employed or Variable Income Support, Child Support Disputes Involving Shared Parenting Time

### Spousal Support / Alimony
- Related Procedural: Temporary Spousal Support, Long-Term Spousal Support
- Situational: Long-Term Marriage Divorce, High-Income Spousal Support Disputes, Cohabitation and Support Modification Issues

### Property Division
- Related Procedural: Equitable Distribution, Marital vs. Separate Property
- Situational: Divorce Involving Business Ownership, Business Valuation and Division, Hidden Assets and Financial Misconduct, Retirement and Pension Division Disputes

### Paternity
- Related Procedural: Establishing Paternity, Challenging Paternity
- Situational: Paternity for Unmarried Parents, Fathers' Rights After Paternity Is Established, Disputed Parentage Cases

### Guardianship
- Related Procedural: Guardianship of a Minor, Adult Guardianship, Temporary Guardianship
- Situational: Emergency Guardianship, Grandparents Seeking Guardianship, Guardianship When Parents Are Unavailable or Incapacitated

---

## Publishing Sequence Awareness

When the user asks to build a page, verify where it falls in the production order:

1. Core Practice Area hubs are built first.
2. Highest-priority Procedural pages are built immediately after their hub.
3. Situational pages follow after the parent hub exists and at least one closely related Procedural page exists or is planned.
4. Additional Situational pages should be built after the cluster has enough structural context to support clean linking.

If a user requests a Situational page and the parent Core hub does not yet exist, flag this: "The parent Core hub for [PRACTICE_AREA] should be built first to establish the authority anchor. Want to start there instead, or proceed with the Situational page knowing the hub will follow?"

If a user requests a Situational page and no closely related Procedural page exists, flag this: "This Situational page is strongest when it can bridge to a related Procedural page that explains the legal pathway. We can proceed now, but the supporting Procedural page should be added next."

For Child Custody specifically: Relocation / Move-Away Disputes and High-Conflict Custody usually follow after the Child Custody hub plus Child Custody Modification and Parenting Plans.

For Divorce specifically: High-Conflict Divorce usually follows after the Divorce hub and Contested Divorce.
