---
name: qa-output-checker-pilot-v1
description: "QA client-facing deliverables for mechanical and operational errors before they go out. Use whenever a user asks to QA, proof, review, check, or verify a deliverable — reports, proposals, audits, scorecards, strategy docs, or any client-facing document for digital marketing or lead funnel work. Also trigger on 'check this before I send it,' 'proof this report,' 'make sure there are no errors,' or 'review this output.' Catches the human errors strategic review misses: wrong client names, stale dates, broken numbers, placeholder text, internal notes left in, formatting inconsistencies, mismatched data across sections, and unprofessional production quality. Complements family-law-red-team-qa-reviewer (strategic and content quality); this skill handles mechanical and production quality. After this skill completes on any deliverable containing legal claims (statutes, deadlines, procedures, eligibility, rights), immediately run legal-content-accuracy-qa as the next gate — mechanical QA never clears legal accuracy."
metadata:
  pilot_status: candidate-v1; not production default; outside skill discovery
  baseline: .agents/skills/qa-output-checker
  changes: CHANGES.md
---

# QA Output Checker (pilot candidate v1)

> **PILOT CANDIDATE / NOT PRODUCTION DEFAULT.** Derived from the baseline skill at
> `.agents/skills/qa-output-checker` (baseline hashes in `pilot-manifest.json`). Changes are listed
> in `CHANGES.md`. Used only when a content-workflow run pins this path.

## Pilot workflow contract

Inside `pilot/content-workflow`, the mechanical pass on a run is executed by
`python3 pilot/content-workflow/scripts/mechanical_qa.py <run-dir> --round N`, which extracts the
DOCX text itself (no `extract-text` or Pandoc dependency; neither is installed on this machine),
pairs citations with Sources in both draft and export, scans for placeholders, checks parity,
runs any run-declared validators, and writes a hash-bound `mechanical-*` record. The human
checklist below still applies to what the script cannot see (tone, cross-references, visual
quality). A mechanical PASS is evidence that these checks ran against specific hashes; it is not
legal or editorial clearance, and the legal handoff in Step 6 is unchanged.

Rendered pages: the coordinator runs `scripts/render_inspect.py <run-dir> --round N --render` (pinned
renderer release and hash from the page skill's `renderer-tools.lock.json`), then views every page
image and attests with a per-page observation (`--attest`). Delivery requires that record to be
bound to the exact export hash with every page inspected. Text extraction never substitutes for
viewing the pages; a missing renderer leaves the run INCOMPLETE.

Research evidence (2026-09-24): `readiness_check.py --stage research` and every delivery check verify
that each legal authority, citation, and client-facts page has a `research/EV<n>.json` record
retrieved in this run (nonce, retrieval time, excerpt present, currency marker, jurisdiction,
legislation status) and re-fetch every record live (`RESEARCH_MISSING`, `RESEARCH_REUSED`,
`RESEARCH_STALE`, `RESEARCH_INVALID`, `RESEARCH_JURISDICTION_MISMATCH`, `LEGISLATION_NOT_EFFECTIVE`,
`RESEARCH_UNAVAILABLE`, `RESEARCH_EXCERPT_DRIFT`). The mechanical pass confirms the delivery folder
carries `research-ledger.md` with every source, retrieval time, currency statement, and live re-check
result, and that no ledger row reads "not re-checked". A ledger row proves retrieval, not that the
source supports the claim; the legal hand-off in Step 6 is unchanged.

Placeholder grammar for content-workflow runs: numeric citation markers `[1]`, `[2]`, ... are not
placeholders. Every other bracketed token (`[LOCAL DETAIL: ...]`, `[FIRM_NAME]`, `[INSERT ...]`,
`[TBD]`), `{{...}}`, `<<...>>`, `TODO`, `TBD`, `FIXME`, `XXX`, `TK`, and `lorem ipsum` is a
placeholder that blocks delivery. Accented or non-ASCII names are not placeholders.

## Purpose

Catch the mechanical, operational, and production errors that make otherwise good work look sloppy or damage client trust — before the deliverable leaves the building.

This skill is **not** a strategic or content reviewer. It does not evaluate whether the strategy is correct or whether the analysis is sound. That is the job of the `family-law-red-team-qa-reviewer` skill.

This skill finds:
- Wrong or inconsistent client names, firm names, and contact details
- Placeholder text, template artifacts, and internal notes left in
- Date and period errors — stale dates, wrong months, inconsistent time ranges
- Number and data errors — figures that contradict each other across sections
- Broken formatting — headers out of hierarchy, missing page numbers, orphaned sections
- Unprofessional language — hedging, filler phrases, casualisms that don't belong in a client report
- Structural completeness — missing sections that were promised or referenced
- Brand and template compliance — wrong logo, wrong colors, wrong fonts vs. the Rocket Clicks standard

---

## When to Use This Skill

Use **before any deliverable is sent to a client.** Priority use cases:

- Territory analysis reports
- SEO audits and strategy decks
- Monthly performance reports
- Lead funnel / waterfall diagnostics
- Paid search reports (SQR analysis, account audits)
- Proposals and scope documents
- Content plans and site architecture documents
- Any DOCX, PPTX, XLSX, or PDF going to a client

**Run this skill after the content is complete.** It is the last gate before delivery, not a drafting tool.

---

## Workflow

### Step 1 — Identify the deliverable type

Determine which checklist(s) apply. Deliverable types and their primary checklists:

| Deliverable | Primary Checklist | Secondary Checklists |
|---|---|---|
| Territory analysis report (DOCX) | Universal + DOCX | Data integrity, Report-specific |
| SEO audit / strategy (DOCX or PPTX) | Universal + format-specific | Data integrity |
| Monthly performance report | Universal + Data integrity | Report-specific |
| Waterfall / funnel diagnostic | Universal + Data integrity | Report-specific |
| Paid search report | Universal + Data integrity | XLSX (if data tabs included) |
| Proposal / scope doc | Universal + DOCX | Completeness |
| PPTX deck | Universal + PPTX | — |
| XLSX data file | Universal + XLSX | Data integrity |

### Step 2 — Inspect the file programmatically (if file is provided)

If the user has uploaded or referenced a file:

**For DOCX:**
```bash
# Extract text for analysis
extract-text document.docx

# Check for tracked changes still present
pandoc --track-changes=all document.docx -o /tmp/check.md && grep -i "ins\|del\|comment" /tmp/check.md | head -20

# Search for placeholder patterns (content-workflow runs: mechanical_qa.py does this and excludes numeric citation markers)
# Baseline pattern `\[.*\]` flags every citation marker; use the narrower form below when grepping by hand.
python3 pilot/content-workflow/scripts/mechanical_qa.py <run-dir> --round <N>   # preferred
# extract-text is not installed here; if a text dump is available:
grep -iE "\[(?!\d+\])[^]]+\]|TBD|\bTK\b|TODO|PLACEHOLDER|INSERT|LOREM|FIXME|XXX|<<.*>>|YOUR NAME|CLIENT NAME|FIRM NAME" -P document.txt
```

**For XLSX:**
```python
import openpyxl
wb = openpyxl.load_workbook('file.xlsx')
# Check for formula errors, empty required cells, placeholder text
for sheet in wb.sheetnames:
    ws = wb[sheet]
    for row in ws.iter_rows(values_only=True):
        for cell in row:
            if cell in ['#REF!', '#DIV/0!', '#VALUE!', '#N/A', '#NAME?', '#NULL!', '#NUM!']:
                print(f"Formula error found: {cell}")
```

**For PPTX:**
```python
from pptx import Presentation
prs = Presentation('file.pptx')
for i, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                text = para.text
                # Check for placeholders
                if any(p in text.upper() for p in ['[', 'TBD', 'TODO', 'PLACEHOLDER', 'INSERT', 'LOREM']):
                    print(f"Slide {i+1}: possible placeholder: {text[:80]}")
```

### Step 3 — Run all applicable checklists

Work through each checklist in `references/checklists.md` for the deliverable type. Check every item. Do not skip items because they seem unlikely — the most embarrassing errors are the ones that "seem unlikely."

### Step 4 — Produce the QA report

Use the output format defined at the end of this skill. Every failed check must be cited with the specific location in the document (page number, section name, slide number, tab name, cell reference).

### Step 5 — Verdict

One of three outcomes:
- **PASS** — ready to send, no issues found
- **PASS WITH FIXES** — sendable after specific corrections are made (list them)
- **HOLD** — one or more critical errors that must be resolved before sending

### Step 6 — Legal-content handoff (mandatory when legal claims are present)

Scan the deliverable for legal claims: anything stating what the law requires, permits, or prohibits, deadlines, waiting or residency periods, eligibility rules, statutory citations, procedures, rights, remedies, or consequences. If any are present:

1. State explicitly in the QA verdict that legal accuracy was **not** verified by this pass.
2. Invoke the `legal-content-accuracy-qa` skill as the next gate. That skill verifies every material legal claim against the current text of governing primary authority, fetched live during its review — it is the only gate authorized to clear legal accuracy.
3. Never present a PASS from this skill as legal-accuracy clearance.

---

## Universal Checklist (All Deliverables)

Run this on every deliverable regardless of type.

### Client Identity
- [ ] Client firm name is spelled correctly and consistently throughout
- [ ] Client firm name matches the name on file — check for: wrong legal entity, old name, common nickname used where formal name is needed
- [ ] Client contact name is correct and spelled correctly (check against brief or CRM)
- [ ] Client's market / location is correct (especially in territory analysis — verify county, state, city spellings)
- [ ] No references to a different client remain anywhere in the document

### Dates and Time Periods
- [ ] Report date / cover date is current
- [ ] All data periods are consistent (e.g., if report is for Q1 2026, no charts showing Q4 2024 data without explicit labeling)
- [ ] "As of" dates on statistics are stated and are not more than 12 months stale for market data
- [ ] No references to "last year" or "next year" without a specific year attached
- [ ] Seasonal references are correct for the stated period

### Rocket Clicks / Internal Branding
- [ ] Rocket Clicks name is spelled correctly throughout (not "Rocket Click," "RocketClicks," "RC")
- [ ] No internal Slack language, acronyms, or shorthand that a client would not recognize
- [ ] No internal project codes, ticket numbers, or task IDs visible
- [ ] No internal names or emails visible that were not intended for the client

### Placeholder and Template Artifacts
- [ ] No `[INSERT]`, `[TBD]`, `[CLIENT NAME]`, `[FIRM NAME]`, `[DATE]`, `[MARKET]`, `[LOCAL DETAIL: ...]` or equivalent brackets remaining (numeric citation markers `[n]` are not placeholders)
- [ ] No "Lorem ipsum" or dummy text present
- [ ] No `TODO`, `FIXME`, `TK`, `XX`, `XXX` markers remaining
- [ ] No comments or track-changes visible in the final document
- [ ] No example or sample data that was not replaced with real client data
- [ ] No `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?` formula errors in any data

### Professionalism and Tone
- [ ] No hedging phrases that undermine authority: "I think," "maybe," "sort of," "kind of," "probably," "I'm not sure but"
- [ ] No casual language inappropriate for a client document: "basically," "honestly," "to be fair," "tbh," "lol," "super"
- [ ] No first-person plural that implies the client is included in Rocket Clicks work: "we should..." (unless intentional)
- [ ] Sentence fragments used only where clearly intentional for stylistic effect
- [ ] No all-caps words outside of proper acronyms (reads as shouting)
- [ ] Numbers formatted consistently: commas in thousands, $ signs where appropriate, % symbols consistent

### Completeness
- [ ] All sections referenced in the table of contents or executive summary are present in the document
- [ ] All figures, tables, and charts referenced in the text are actually present
- [ ] All appendices referenced in the body are present
- [ ] No broken cross-references (e.g., "see Section 4" where Section 4 doesn't exist)
- [ ] Conclusion or recommendation section is present and actually makes a recommendation

---

## Data Integrity Checklist (Reports with Numbers)

Run on any deliverable containing metrics, scores, or quantitative analysis.

### Internal Consistency
- [ ] Numbers cited in the executive summary match numbers in the body
- [ ] Numbers in charts match numbers in tables match numbers in text — all three must agree
- [ ] Totals in tables actually sum correctly
- [ ] Percentages add up to 100% where they should (or explain why they don't)
- [ ] Year-over-year or period-over-period comparisons use the same base — confirm periods are truly comparable
- [ ] Sample sizes are stated wherever percentages are derived from survey or sample data

### Source and Citation Integrity
- [ ] Every statistic has a source attribution (government, published study, or stated as internal client data)
- [ ] No statistics cited as "[source]" or "[citation needed]" — all must be resolved
- [ ] ACS data cited with specific table code and year (e.g., ACS 5-Year Estimates, Table B19013, 2023)
- [ ] Web search data cited with the search query and date retrieved
- [ ] No statistics presented as current if the source is more than 3 years old without flagging the vintage

### Territory Analysis Specific
- [ ] Territory score totals are mathematically correct (sum of dimension scores)
- [ ] Population figures cross-check against known county population (sanity check — Palm Beach County is ~1.5M, not 150K or 15M)
- [ ] Income figures are in the right units (dollars, not thousands of dollars)
- [ ] Vacancy rates expressed as percentages of total housing units, not occupied units
- [ ] Competitor review counts and ratings match what was actually seen in screenshots (do not inflate)

### Waterfall / Funnel Specific
- [ ] Each conversion rate is derived correctly: numerator ÷ denominator stated
- [ ] No conversion rate > 100%
- [ ] Funnel stages are in the correct order (Calls → PCs → QPCs → Opps → Consults → Quotes → FAs)
- [ ] Dollar gap calculations: Missed FAs × avg PMV = revenue gap (verify arithmetic)
- [ ] JIT capacity flags use the correct thresholds (Consult Days > 2, answer rate > 85%)

### Paid Search / Performance Report Specific
- [ ] Impression, click, and conversion figures are for the stated date range only
- [ ] CTR = Clicks ÷ Impressions (verify a spot check)
- [ ] Conversion rate = Conversions ÷ Clicks (verify a spot check)
- [ ] ROAS = Revenue ÷ Spend (verify a spot check)
- [ ] No metrics showing negative spend or negative impressions (data pull error)
- [ ] Month-to-date vs. full-month figures are clearly distinguished

---

## DOCX Checklist

Run on all Word document deliverables.

### Formatting Structure
- [ ] Heading hierarchy is correct: H1 → H2 → H3, no skipped levels
- [ ] Consistent heading styles used throughout (not a mix of manually bolded text and Heading styles)
- [ ] Page numbers present in footer
- [ ] Header contains document title and/or client name
- [ ] Cover page is complete: client name, report title, date, Rocket Clicks branding
- [ ] Table of contents (if present) matches actual section headings and page numbers
- [ ] No orphaned headings at the bottom of a page with no content following

### Tables and Data
- [ ] All tables have consistent column widths within each table
- [ ] Table headers are present and bolded
- [ ] No tables that break across pages without repeating header row
- [ ] No cells containing only a single character or clearly truncated content

### Visual Elements
- [ ] All images are clear and not pixelated at final document size
- [ ] No broken image placeholders (empty boxes where images should be)
- [ ] Screenshot annotations (if any) are readable at print size
- [ ] Consistent margin sizes throughout (not sections with different margins)

---

## PPTX Checklist

Run on all PowerPoint/slide deck deliverables.

### Slide Structure
- [ ] Slide count matches what was promised or scoped
- [ ] Every slide has a title
- [ ] Title slides use the correct Rocket Clicks or client deck template
- [ ] No slides with default "Click to add title" or "Click to add text" placeholder text
- [ ] Slide numbers present and sequential

### Content
- [ ] No slide is text-only when a chart or visual was clearly intended
- [ ] No speaker notes visible in the delivered version that were meant to be internal
- [ ] Bullets are parallel in structure (all start with verbs, or all start with nouns — not mixed)
- [ ] No bullet points that are full paragraphs (> 2 lines per bullet is a flag)
- [ ] Consistent font sizes across body slides (do not mix 18pt and 11pt on the same slide type)

### Visuals
- [ ] All charts have axis labels and a title
- [ ] Legend is present on all multi-series charts
- [ ] No chart data that contradicts the narrative on the same slide
- [ ] No missing data points shown as zeroes when they should be absent

---

## XLSX Checklist

Run on all spreadsheet deliverables.

### Structure
- [ ] Tab names are descriptive (not "Sheet1", "Sheet2")
- [ ] Each tab has a clear purpose — no unused blank tabs
- [ ] Input cells distinguished from formula cells (blue text for inputs per industry standard)
- [ ] No hardcoded numbers inside formulas that should be in an input cell

### Data Quality
- [ ] No formula errors: `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`, `#NULL!`, `#NUM!`
- [ ] All cells that should sum actually sum (spot-check 3 totals)
- [ ] No negative values in fields that cannot logically be negative (review counts, impressions, population)
- [ ] Date cells formatted as dates, not text strings
- [ ] Currency cells include $ and consistent decimal places (no mixing $1,000 and $1000.00)
- [ ] Percentage cells formatted as percentages, not decimals (25% not 0.25)

### Usability
- [ ] Filter or freeze panes set for tables with more than 10 rows
- [ ] Column widths accommodate content (no truncated text unless intentional)
- [ ] Print area set correctly if the file is expected to be printed

---

## Common Human Error Patterns — Know These by Memory

These are the errors most commonly found in Rocket Clicks deliverables right before sending:

**The Copy-Paste Swap** — Client A's name or data appears in Client B's report. Happens when using a prior report as a template. *Check: search the entire document for every client name you've worked on in the past 90 days.*

**The Stale Date** — Cover page says January, but it's now April. Or a chart's date range is from last year's report. *Check: every date in the document.*

**The Orphaned Placeholder** — One `[INSERT COMPETITOR DATA HERE]` survived in the middle of Section 3. *Check: search for `[`, `TBD`, `TODO`, `TK`, `XX`.*

**The Math Drift** — Executive summary says 12% vacancy rate. The data section says 9.5%. Both were correct at different stages of drafting. *Check: every number in exec summary against its source section.*

**The Wrong Firm Name** — "Sterling Lawyers" appears in a Vasquez de Lara report because that was the last example used. *Check: search for all client firm names in your recent work.*

**The Internal Aside** — "Note to self: confirm this with Tyler before sending" survived in a text box. Or a comment in Word is still there. *Check: all comments, text boxes, and speaker notes.*

**The Decimal Disaster** — Per capita income shows as $45 instead of $45,447 because a formula divided by 1,000 without intending to. *Check: all income and dollar figures against the source data.*

**The Singular/Plural Mismatch** — "The firm have strong reviews" — subject-verb agreement error from editing around a sentence. *Check: read every sentence that was recently edited.*

**The Dangling Reference** — "As shown in Figure 4" but Figure 4 was deleted. Or "See the appendix" but the appendix is empty. *Check: every cross-reference.*

**The Wrong Score Total** — A scorecard shows 7+6+5+4+3+2+1 = 32, but the model caps at 27. Addition error in the summary. *Check: all arithmetic in scorecards and totals tables.*

---

## QA Report Output Format

Use this format for every QA review.

---

### QA VERDICT
**[PASS / PASS WITH FIXES / HOLD]**

Brief rationale (1–2 sentences).

---

### CRITICAL ISSUES (Must fix before sending)
Issues that would embarrass the team, damage client trust, or contain materially wrong information.

**[Issue #]** | **[Category]** | **[Location]**
> Description of the error. Exact text or value that is wrong. What it should be.

---

### HIGH PRIORITY (Fix before sending, but not blocking)
Issues that reduce quality or professionalism but are unlikely to cause immediate damage.

**[Issue #]** | **[Category]** | **[Location]**
> Description. What to change.

---

### MEDIUM / LOW (Fix if time allows)
Minor polish items.

**[Issue #]** | **[Category]** | **[Location]**
> Description.

---

### WHAT PASSED
Brief list of areas that checked clean. Gives the team confidence in what not to re-review.

---

### TOTAL ISSUES FOUND
- Critical: X
- High: X
- Medium/Low: X
- **Total: X**

---

## Reference Files

- `references/checklists.md` — All checklists in checklist-only format (no explanations) for fast reference during review
- `references/error-patterns.md` — Extended catalog of error patterns by deliverable type with real examples
