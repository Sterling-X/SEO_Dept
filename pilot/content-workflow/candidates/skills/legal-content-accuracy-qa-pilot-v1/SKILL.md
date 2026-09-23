---
name: legal-content-accuracy-qa-pilot-v1
description: "Final legal-accuracy gate for law-firm and legal content. Verifies every material legal claim against the current text of governing primary authority (statutes, court rules, official forms, regulations, case law) fetched LIVE via web search during the review, never from model memory. Use whenever the user asks to verify legal accuracy, fact-check legal content, check statutes, citations, deadlines, waiting periods, residency rules, or thresholds, run a legal QA, or live-check a page. ALSO trigger automatically as the next gate whenever family-law-red-team-qa-reviewer or qa-output-checker completes on content containing legal claims (rules, deadlines, eligibility, procedures, rights, remedies); those skills do not verify legal accuracy. Applies to service, procedural, situational, location, and landing pages, blogs, FAQs, calculators, and reports in any practice area and any U.S. jurisdiction. Do NOT use for content with no legal claims, for drafting, or as a substitute for strategic or mechanical QA."
metadata:
  pilot_status: candidate-v1; not production default; outside skill discovery
  baseline: .agents/skills/legal-content-accuracy-qa
  changes: CHANGES.md
---

# Legal Content Accuracy QA (pilot candidate v1)

> **PILOT CANDIDATE / NOT PRODUCTION DEFAULT.** Derived from the baseline skill at
> `.agents/skills/legal-content-accuracy-qa` (baseline hashes in `pilot-manifest.json`). Changes
> are listed in `CHANGES.md`. Used only when a content-workflow run pins this path.

## Pilot workflow contract

When this skill runs inside `pilot/content-workflow`, the following bind the review:

- **Structured output.** In addition to the prose sections below, return one JSON object in the
  canonical structured format (`pilot/content-workflow/canonical/review-findings-schema.md`):
  findings with ids `L1`, `L2`, ..., severity, the exact passage quote and location, issue,
  evidence (authority, official URL, access date, what the text says), requested correction, and
  `resolution.status = "open"`; the Verification Log rows as `verification_log`; and
  `checks_not_performed`. The coordinator records it with `scripts/record_review.py`, which
  rejects a finding whose quote is not in the draft.
- **Hash binding.** The record is bound to the SHA-256 of the draft you read. Any later edit
  invalidates it; a recheck is required. Do not describe a prior pass as still valid after an edit.
- **Corrections are requests, not edits.** You do not edit the draft or write replacement copy that
  you then approve. "Suggested replacement" wording below is guidance for the writer.
- **Fixed means re-read.** On a recheck, set `fixed-verified` only after re-reading the revised
  passage against the authority. A change log, a writer's assertion, or a coordinator's summary is
  never a basis for `fixed-verified`. Otherwise leave the finding `open` with a note.
- **Verdict mapping.** `Ready` -> `ready`; `Ready after the required revisions` ->
  `ready-with-revisions`; `Not ready` -> `not-ready`.
- **Voice source.** Load only the voice source pinned in `run.json` (resolved by exact domain
  route). Do not scan for voice skills by name.
- **No delegation.** Do not spawn or call other agents.

## Purpose

Conduct a high-rigor legal-accuracy review of law-firm marketing content before it is published, updated, or approved. This is the final content-quality checkpoint for material that may be read by consumers making legal decisions.

This review is an editorial and factual safeguard. It does not constitute legal advice and does not replace review by a licensed attorney familiar with the relevant jurisdiction and matter. Never claim attorney-level approval or legal clearance.

## The core mandate: live verification, never memory

The failure mode this skill exists to kill is the plausibility pass: a legal claim that sounds right, matches training-era knowledge, and is wrong or stale today.

**Do not rely on model memory alone. Locate and read the current governing authority for every material legal claim, fetched live during this review session.** Model memory is a hypothesis generator for where to look. It is never a verification source.

Operationally:

- Use the available web search and page fetch tools to locate and read the official source text for each claim during the review. Prefer official domains: state legislature sites (e.g., `docs.legis.*.gov`, `legis.*.gov`), state court sites (`*.courts.gov`, `*courts.gov`), agency sites, and federal sources (`uscourts.gov`, `ecfr.gov`, `uscis.gov`, `law.cornell.edu` only as a locator to the official cite).
- Fetch the specific section or rule page, not an entire chapter, unless the absolute-language check requires reading surrounding provisions.
- Batch efficiently: when multiple claims cite the same statute or chapter, fetch it once and run every claim against the fetched text. Batching the fetch never excuses skipping the per-claim support test.
- Some official sites (including some state legislature domains) block automated page fetch. When that happens, use the official site's own indexed text as returned in search results, corroborate against a second reputable source, prefer versions showing the statute's history line so amendments are visible, and note the fetch limitation in the Verification Log.
- If a source cannot be reached or corroborated during the session, the claim is **Unverifiable**, never passed. Say so in the output.
- Recheck the live page even if a draft was previously approved. Treat previous AI reviews, prior QA passes, and earlier drafts as hypotheses, not verified authority. Verify every proposed correction independently before recommending it.
- Use the current date as the review date unless another date is provided.

## Position in the QA pipeline

This skill is the legal-accuracy gate in a three-gate system. It does not duplicate the other gates.

1. **family-law-red-team-qa-reviewer** — strategic and content quality: claims strength, structure, hierarchy, local credibility, trust, conversion, brand voice. Its statutory category is a desk check on citation-claim fit from the text in hand.
2. **qa-output-checker** — mechanical and production quality: names, dates, placeholders, formatting, data integrity.
3. **legal-content-accuracy-qa (this skill)** — legal and factual accuracy verified live against primary authority.

Run this skill after either of the other gates completes on content containing legal claims, or standalone when legal verification is requested directly. A pass from the other gates is never legal-accuracy clearance.

## Inputs

The user provides the live page URL and/or the complete page content. Infer from those materials when possible:

- Client or law firm
- State and jurisdiction
- Practice area and topic
- Page type (service page, procedural page, FAQ, blog, location page, calculator, etc.)
- Existing citations
- Relevant procedural posture
- Applicable client or compliance rules already provided in the project

If any item cannot be confirmed from the URL, page content, or prior project context, state "Not provided." Do not invent missing context.

Handling rules:

- If the URL and pasted content conflict, treat the pasted content as the version under review, but flag the discrepancy.
- If the live URL cannot be accessed, review the supplied page content and state that the live page, metadata, hyperlinks, and rendered citations could not be independently confirmed.
- Apply only the client-specific and compliance rules confirmed for the active client. Inside a content-workflow run, the only voice source is the one pinned in `run.json` (routed by exact domain via `pilot/content-workflow/canonical/client-routing.json`); do not identify a voice skill by scanning names. Do not import voice, compliance, terminology, or legal-content rules from another client or project.

## Source hierarchy

Prioritize sources in this order:

1. Official codified statutes or constitutions
2. Official court rules and statewide court forms
3. Official administrative regulations and agency guidance
4. Published controlling supreme court and appellate opinions
5. Official local court rules and procedures
6. Secondary sources, only when primary authority is unavailable or additional interpretation is necessary

Law-firm blogs, commercial statute mirrors, aggregators, generic legal guides, and AI summaries may help identify issues, but they must never be the primary basis for approving or correcting a legal claim when official authority is available.

## Workflow

Read `references/verification-protocol.md` before Phase 2 on every run. Read `references/practice-area-checklists.md` at Phase 6.

**Phase 1 — Establish the governing framework.** Identify the controlling jurisdiction, which body of law applies (state, federal, local, tribal, administrative), the procedural posture in play, whether the rule varies by case type, party status, dates, or county, and the current effective date of the governing authority. Never apply a rule from one procedural stage to another without confirming it governs both. Full detail in the protocol reference, Step 1.

**Phase 2 — Extract every checkable legal claim.** Review the page line by line, including introductions, headings, FAQs, examples, tables, CTAs, sidebars, captions, and related-content modules. Introductions and FAQs often oversimplify rules the main body explains more carefully. Every absolute-language claim (always, never, must, automatically, only, cannot, guaranteed, required, no deadline, no limit, no exception) is flagged for the expanded verification in Phase 3. Full extraction taxonomy in the protocol reference, Step 2.

**Phase 3 — Verify each claim live against primary authority.** For each material claim: fetch and read the current governing text, confirm section, subsection, official title, and effective date, check for recent amendments or renumbering, then run the per-claim support test. For every absolute-language claim, run the separate absolute-language check: search the full text of the cited statute and companion statutes on the same topic for carve-outs, exceptions, or contrary provisions, and affirmatively record that the search was performed and what it found. Never clear an absolute claim on citation-match alone. Test multi-part standards for and/or logic, burden, and standard of proof. Classify each statement as legal requirement, court discretion, common practice, local procedure, strategic recommendation, firm process, or illustrative example. Full detail in the protocol reference, Step 3.

**Phase 4 — Completeness, procedure, and time-sensitive law.** Test statutory lists and factor tests against the full official list (Step 4). Verify venue, standing, filing, service, deadlines, waiting and residency periods, and modification, enforcement, and appeal claims, and attribute each rule to its true source: statute, court rule, official form, regulation, local rule, court order, or common practice (Step 5). Confirm the current status of pending bills, recently enacted laws, schedules, fees, forms, and numerical thresholds as of the review date, with exact dates and legislative-stage precision (Step 6).

**Phase 5 — Citations, terminology, and ethics.** Verify every citation resolves live to the intended official source and directly supports the surrounding sentence; run case-law status checks where cases are cited (Step 7). Run the jurisdiction-specific terminology currency check (Step 8). Run the ethical and scope-of-service check for misleading implications such as guaranteed results, specialist status without support, or coverage where the firm is not licensed (Step 9).

**Phase 6 — Practice-area-specific checks.** Apply the relevant checklist(s) from `references/practice-area-checklists.md` in addition to Phases 1 through 5. If the page spans more than one practice area, apply each applicable list.

**Phase 7 — Deliver findings** in the output format below, including the mandatory Verification Log.

## Verification Log (mandatory)

Every material legal claim gets a row. This is the enforcement mechanism against plausibility passes: if a claim has no row with a live source and access date, it was not verified.

| # | Claim (condensed) | Page location | Authority | Official source URL | Accessed | Result | Notes |

- **Result** is one of: Confirmed, Correction-needed (the passage must change; the reviewer does not make the change), Flagged (overbroad, incomplete, or misleading), Unverifiable. `Corrected` is not a result this reviewer records: whether a correction landed is decided on recheck by re-reading the revised passage, and that outcome is recorded as the finding's `resolution.status`.
- For absolute-language claims, the Notes column must record the outcome of the exception search ("Full-text and companion-statute search performed; no contrary provision found" or a description of what was found).
- Access dates are the actual dates the source was fetched during this review, not publication dates.
- Do not pad the log with trivial restatements. Log material claims: anything that, if wrong, could mislead a reader about their rights, obligations, deadlines, eligibility, process, or outcomes.

## Output format

**Verdict:** Ready / Ready with revisions / Not ready, with a concise explanation of the overall legal-accuracy result.

**Required.** For every material correction: Section (exact page heading or location), Current text (quote or identify the affected wording), Issue (precisely what is incorrect), Actual rule (the verified legal standard), Why it matters (reader or compliance consequence), Authority (controlling source), Suggested replacement (concise replacement wording).

**Recommended.** Same structure, for statements that are incomplete, overbroad, or potentially misleading but not clearly false.

**Optional.** Only useful, low-risk precision improvements.

**Citation Review.** Correct citations, incorrect citations, missing authority, overbroad citations, outdated titles, subsections, or URLs, and claims requiring local-rule verification.

**Terminology Flags.** Jurisdiction-specific terminology decisions, listed separately from legal errors.

**Accurate as Written.** The most important claims independently verified against authoritative sources, not a reproduction of every claim checked. Never say "everything checks out" unless every material legal claim was evaluated.

**Verification Log.** The full table per the spec above.

**Residual Unknowns.** Anything that could not be verified: missing page text, unavailable local rules, unclear publication date, inaccessible forms, unconfirmed hyperlink targets, facts dependent on the client's actual services, jurisdiction not provided. Use "Not provided" where appropriate.

**Bottom Line.** End with exactly one of: Final status: Ready / Final status: Ready after the required revisions / Final status: Not ready. When the page is not ready as written, name the single most important correction.

## Review rules

- Do not create a legal error by overcorrecting a reasonable consumer-level simplification. Distinguish a true error from a precision improvement.
- Scope corrections to the exact locations where the problem occurs. When the introduction or FAQ is inaccurate but the main body is correct, revise only the inaccurate sections. Do not rewrite the entire page. Preserve accurate plain-language explanations.
- Do not invent local practices, legal outcomes, or statutory interpretations.
- Do not approve a statement merely because it sounds plausible, and never because the citation points to the correct general statute.
- If controlling authorities conflict, the law is unsettled, or courts apply materially different interpretations, do not present one interpretation as universally settled. Explain the conflict, identify the controlling or most authoritative sources, and classify the issue as requiring attorney verification.
- Do not assume an uncited claim is false merely because it lacks a citation; flag it as "Citation or verification needed."
- Consumer-recognition or SEO terminology may remain when appropriate, but the statutory term should be introduced where necessary. Flag terminology decisions rather than silently replacing useful consumer language.

## Recurring failure patterns to watch for

- A multi-part legal test flattened into an absolute
- A statutory list presented as complete with a material item omitted
- Two related statutes blended into a hybrid standard
- Court discretion described as mandatory
- Common practice described as law
- Pending legislation described as current law
- A local rule presented as statewide procedure
- A permitted legal structure described as automatically producing a separate legal result
- A citation that supports the topic generally but not the precise proposition
- An introduction or FAQ that contradicts the more accurate main body
- An absolute claim verified only against its own cited subsection, missing an exception or contrary provision elsewhere in the same statute or in a companion statute on the same topic

## Do not use this skill when

- The content contains no legal claims (pure brand copy, pure performance data)
- The user wants content drafted or rewritten rather than verified
- The task is strategic critique only (family-law-red-team-qa-reviewer) or mechanical proofing only (qa-output-checker)

## Reference files

- `references/verification-protocol.md` — Full operational detail for Steps 1 through 9: governing framework, claim extraction taxonomy, per-claim support test, absolute-language check, multi-part standard testing, list testing, procedural verification, pending-law handling, citation verification, terminology currency, ethics check. Read before Phase 2 on every run.
- `references/practice-area-checklists.md` — Practice-area-specific checklists (family, estate/probate/guardianship, criminal, personal injury, employment, immigration). Read at Phase 6.
