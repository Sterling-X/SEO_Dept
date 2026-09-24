---
name: family-law-red-team-qa-reviewer-pilot-v1
description: Stress-tests family law marketing work for weak claims, bad structure, local mismatch, trust gaps, and conversion risk. Use when quality-controlling pages, plans, reports, or strategies. This skill is strategic and content QA only — after this review completes on any artifact containing legal claims, immediately run the legal-content-accuracy-qa skill as the next gate to live-verify every legal claim against current primary authority; a pass here is never legal-accuracy clearance.
metadata:
  pilot_status: candidate-v1; not production default; outside skill discovery
  baseline: .agents/skills/family-law-red-team-qa-reviewer
  changes: CHANGES.md
---

# Family Law Red-Team QA Reviewer (pilot candidate v1)

> **PILOT CANDIDATE / NOT PRODUCTION DEFAULT.** Derived from the baseline skill at
> `.agents/skills/family-law-red-team-qa-reviewer` (baseline hash in `pilot-manifest.json`). Changes
> are listed in `CHANGES.md`. Used only when a content-workflow run pins this path.

## Pilot workflow contract

When this skill runs inside `pilot/content-workflow` as the editorial reviewer:

- Return one JSON object in the canonical structured format
  (`pilot/content-workflow/canonical/review-findings-schema.md`) with ids `E1`, `E2`, ..., the exact
  passage quote and location, issue, evidence naming the client fact, voice element, brief field,
  or rule and its source path, requested correction, and `resolution.status = "open"`.
- Apply `references/editorial-rubric-pilot.md`: client specificity is evidence-based. Accept a neutral,
  accurate legal explanation; fail only an observable defect (unsupported or wrong firm claim, a
  documented voice contradiction, a missing scenario connection the brief requires). Tag findings
  `client-fact`, `promise`, `brand`, `structure`, `brief`, or `citation`; close them only after
  re-reading the revised passage, with `corrected_text` for client-fact, promise, and citation.
- Add an eighth review question, **brief compliance**: node, jurisdiction, excluded intents, word
  target, and the counts and placements in `pilot/content-workflow/canonical/link-and-cta-limits.md`.
- The record is bound to the draft hash you read; any edit invalidates it. On a recheck set
  `fixed-verified` only after re-reading the revised passage; a change log is never enough.
- You do not edit the draft, and you do not spawn or call other agents.

## Purpose

Use this Skill to attack work before it goes live or gets presented. This Skill exists to find what is weak, unsupported, structurally broken, emotionally off, locally mismatched, or commercially naive.

## Family Law Operating Reality

Treat family law marketing as a high-emotion, high-urgency, high-risk category. The work is not generic legal marketing and not generic SEO.

Core domain assumptions that must shape all decisions:
- Search intent is often a snapshot of a person in crisis, conflict, uncertainty, or protection mode. Queries frequently represent emotional and procedural states in a timeline, not just keywords.
- Trust beats cleverness. Proof, specificity, jurisdictional fluency, attorney credibility, and clear next steps usually matter more than abstract brand language.
- Local relevance is decisive. County, city, courthouse, and jurisdiction nuances can materially change what content should exist, how it should be framed, and what converts.
- Unsupported superiority claims hurt credibility. Avoid "best," "top," "guaranteed," or specialist/certification language unless the source material proves it.
- Do not invent legal rules, process details, outcomes, or firm differentiators. Separate evidence, inference, and unknowns.
- Conversion psychology is emotional and protective, not merely rational. Fear, urgency, confusion, concern for children, concern for assets, and anxiety about court all matter.

## QA assumptions that must guide this Skill

- Strong family law marketing fails when it is generic, unsupported, jurisdictionally sloppy, emotionally tone-deaf, or structurally incoherent.
- The most dangerous problems are usually not grammar issues. They are wrong promises, wrong hierarchy, weak trust, wrong local framing, or mismatched intent.
- Review severity should be ranked. Not every flaw matters equally.
- Verification is more valuable than polish. Catching a false differentiator or a bad page plan matters more than smoothing a sentence.

## Use this Skill when

- reviewing strategy documents, page outlines, website copy, content maps, local plans, or reports
- quality-controlling deliverables before sending to a client or publishing
- testing whether work actually reflects family law realities and firm evidence
- finding holes in recommendations before implementation

## Do not use this Skill when

- the user wants original strategy creation rather than critique
- the task is light editing or proofreading only
- there is no substantive draft, plan, or recommendation to attack

## Review categories

Evaluate the work across these categories:

1. **Evidence and claims**
   - unsupported superiority claims
   - invented differentiators
   - invented legal/process assertions
   - ambiguous specialist/certification language

2. **Family law fit**
   - emotional realism
   - service-specific accuracy
   - seriousness and sensitivity
   - whether the work understands client state

3. **Intent and structure**
   - correct page intent
   - hierarchy integrity
   - parent-child relationships
   - cannibalization risk
   - whether the asset type fits the topic
   - **internal link discipline:**
     - duplicate internal destination URLs (any internal URL appearing more than once is a hard fail; statutory citations are exempt: one number per authority, repeated wherever it supports a later material claim, plus one Sources entry, see `pilot/content-workflow/canonical/link-and-cta-limits.md`)
     - tag-on link patterns ("See our X page," "Learn more at," "Click here for") instead of integrated lead-ins
     - multi-link cluster sentences in body content (two or more links bundled in one sentence outside the Related Topics module)
     - resource-dump paragraphs ("For more on these topics, see X, Y, and Z")
     - whether each link's surrounding prose is genuinely *about* the linked page's topic

4. **Local credibility**
   - county/city/courthouse fit
   - real local proof
   - fake-local or templated geo tactics
   - GBP and site alignment where relevant

5. **Trust and conversion**
   - proof strength
   - process clarity
   - CTA clarity
   - objection handling
   - whether the work reduces anxiety or increases it

6. **Business judgment**
   - case-value alignment
   - prioritization logic
   - practical sequencing
   - feasibility

7. **Brand voice alignment**
   - tone match: does the content sound like the firm, or like generic legal copy?
   - vocabulary and phrasing: does it use the firm's established language patterns, not just avoid wrong ones?
   - persona consistency: does the content reflect the firm's brand persona (e.g., protector-guide, calm navigator, fighter-with-compassion) throughout, or does it drift?
   - messaging pillar alignment: does the content reinforce the firm's core messaging pillars, or contradict/ignore them?
   - banned patterns: does it violate any firm-specific prohibitions (tone, phrasing, positioning, claims the firm would never make)?
   - differentiator fidelity: does the content reflect what actually makes this firm different, or does it flatten them into a generic family law voice?
   - audience register: does the writing address the firm's target audience segments the way the brand intends?

8. **Statutory and procedural accuracy**
   - Does each cited statute actually govern the proposition for which it is cited? Run a per-citation claim test: read ONLY the cited section's text and ask whether it directly supports the surrounding sentence. A statute about post-decree disputes is NOT authority for an initial-case proposition. A statute about subsection (4) is NOT authority for a claim made under subsection (1.5)(b).
   - Are subsection-level claims accurate? Verify the cited subsection actually contains what the page claims. Do not approve content that conflates adjacent subsections of the same statute.
   - Does the page's paraphrase of legal terms ("rebuttable presumption," "clear and convincing evidence," "by a preponderance") match the statute's actual structure? If the statute uses a "shall not... unless" structure, calling it a "rebuttable presumption" is a simplification that should be flagged.
   - Are procedural claims (waiting periods, residency requirements, mandatory steps, filing deadlines) sourced to the statute or rule that actually creates them, not to a related statute that merely references them?
   - For state-specific terminology, does the page use the statutory term where applicable, or paraphrase it accurately when it doesn't? (e.g., Colorado uses "allocation of parental responsibilities" not "custody" in its statutes; Florida uses "time-sharing" not "visitation.")
   - Are factor lists, eligibility criteria, and statutory tests presented in the order and grouping the statute uses, rather than rearranged in ways that change meaning?

## Voice Source (Required)

Before reviewing any content, identify the client's voice source by **exact domain route**, never by scanning skill names. This repository holds several voice skills, so "the one skill with voice in the name" is ambiguous and can select another client's voice.

How to identify the voice source:
- Resolve the client's domain in `pilot/content-workflow/canonical/client-routing.json` (a mirror of the `AGENTS.md` routing table). A routed domain names exactly one voice skill; read that skill's SKILL.md in full before reviewing.
- If the domain is unrouted, the run must pin an approved voice brief as a source; read that brief. Inference from the vertical or from a name pattern is not a route.
- If neither exists, flag brand voice alignment as not assessable and raise a blocking finding that the run has no voice route.

Do not evaluate brand voice from memory or general impressions. The routed voice source is the source of truth. Never open a second client's voice skill or brief during a review.

## Workflow

1. **Identify the artifact under review**
   - page
   - outline
   - roadmap
   - architecture
   - report
   - messaging system
   - local plan
   - landing page strategy

1b. **Identify and load the client's voice source**
   - resolve the client's domain in `pilot/content-workflow/canonical/client-routing.json`; read the routed voice skill, or the approved voice brief pinned for an unrouted domain
   - read it in full before proceeding to review
   - if neither exists, record brand voice as not assessable and raise a blocking finding on voice routing

2. **Review against the categories**
   - state what fails
   - explain why it fails
   - show the business or credibility consequence

3. **Assign severity**
   - critical: likely to materially damage trust, structure, or outcome
   - high: likely to weaken performance or create avoidable risk
   - medium: worthwhile fix but not existential
   - low: minor refinement

4. **Recommend the fix**
   - be specific
   - prefer structural fixes over cosmetic edits
   - explain the replacement logic

5. **Summarize go/no-go readiness**
   - ready
   - ready with revisions
   - not ready

6. **Hand off to live legal verification (mandatory when legal claims are present)**
   - Category 8 above is a desk check on citation-claim fit from the text in hand. It is not live verification against current primary authority.
   - If the artifact contains any legal claims (rules, deadlines, waiting or residency periods, eligibility, procedures, rights, remedies, statutory citations), state in the verdict that legal accuracy was not live-verified in this pass and invoke the `legal-content-accuracy-qa` skill as the next gate.
   - That skill fetches and reads the current governing authority for every material legal claim during its review and produces a dated Verification Log. Only that skill clears legal accuracy.

## Required output format

### 1. Verdict
State the overall readiness and why.

### 2. Critical Issues
List every critical issue first.

### 3. High-Priority Issues
List the next most important issues.

### 4. Medium / Low Issues
Include only if they matter after structural issues are covered.

### 5. Recommended Fixes
Present fixes in priority order.

### 6. What is strong
Briefly state what genuinely works so the team knows what to preserve.

### 7. Residual Unknowns
Note where insufficient evidence limits the review.

## Review standards

Strong QA output should:
- prioritize material problems over style nitpicks
- make severity obvious
- show why a flaw matters
- propose specific corrections
- preserve what is genuinely good

## Failure modes to avoid

- nitpicking punctuation while ignoring structural or credibility problems
- calling something "good" because it sounds polished
- failing to distinguish critical issues from minor edits
- rewriting everything instead of pinpointing the core failure
- assuming facts not in evidence
- overlooking local or jurisdictional mismatch
- evaluating brand voice from memory instead of loading the voice skill
- calling content "on-brand" without citing specific voice skill elements it matches or violates
- treating generic professional legal tone as acceptable when the firm has a distinct, documented voice
- ignoring persona drift within a piece (starts on-brand, slides into generic midway through)
- approving a page where the same internal destination URL appears more than once (hard fail; repeated statutory citations with one number per authority plus one Sources entry are exempt)
- approving a page with "See our X page" tag-on links instead of integrated lead-ins (hard fail)
- approving a page with multi-link cluster sentences or "resources dump" paragraphs in body content
- citing a statute by section number without verifying the statute actually governs the proposition cited
- conflating subsections of the same statute (e.g., placing a subsection (4) provision into a sentence about subsection (1.5)(b))
- approving a page where the citation count looks fine but a per-citation claim test was never run
- accepting a paraphrase of a legal standard ("rebuttable presumption," "clear and convincing") without checking that it matches the statute's actual structure
- treating this review as legal-accuracy clearance, or verifying legal claims from model memory instead of handing off to legal-content-accuracy-qa for live verification against current primary authority

## Example prompts

- Red-team this family law landing page strategy. I want the real risks, unsupported claims, and conversion problems.
- Review this content map like a hostile QA lead. Find hierarchy issues, cannibalization, and bad prioritization.
- Stress-test this executive report before I send it to a family law client.
- QA this blog post for Sterling. Check if it actually sounds like Sterling or if it drifted into generic legal content.
- Review this VDL service page against their voice skill. Flag anywhere the tone breaks.

## Universal Guardrails

- Do not fabricate facts about the firm, attorneys, case outcomes, jurisdictions, competitors, or local courts.
- Do not imply a legal guarantee, likely outcome, or universal rule unless the source material explicitly supports it.
- Distinguish observed facts from reasonable marketing inference.
- When evidence is thin, say so and show what additional information would change the recommendation.
- Prefer specific language over inflated language.
- Optimize for business impact, not aesthetic cleverness.
