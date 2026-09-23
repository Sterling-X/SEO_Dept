# Error Pattern Catalog

Extended catalog of error patterns by deliverable type. Organized by how errors typically enter the document and how to detect them.

---

## How Errors Enter Client Documents

Understanding the production workflow reveals where errors cluster.

### Template reuse errors
The most common source of wrong client data. A prior report is used as a template. Find-and-replace is run but misses:
- Client names inside chart titles (not found by text search)
- Client names in image captions or alt text
- Client names embedded in table headers that were converted to images
- Old market names in headers/footers that update independently

**Detection:** After any find-and-replace, search the whole document character-by-character for the old client name. Check headers, footers, and text boxes separately — they are often excluded from standard Find searches.

### Draft-to-final errors
Text survives from an earlier draft state:
- Comments that were internal discussion ("ask Tyler if this is right")
- Placeholder data ("TBD — waiting for keyword data")
- Research notes mixed into narrative paragraphs
- An older version of a number that was updated in one section but not another

**Detection:** Read the document from scratch in presentation mode (not edit mode) — this surface assumptions about final state that editing mode hides.

### Copy-paste math errors
Numbers copied from data sources into reports frequently shift:
- Value copies as formatted string, not number — later arithmetic fails silently
- Off-by-one row in a spreadsheet data pull (picked up the header row's number)
- Wrong column selected in a pivot table
- Percent formatted as decimal or vice versa in the source

**Detection:** For every number in the final report, trace it back to the source data and verify by arithmetic, not by visual match.

### Last-minute edit errors
Changes made in the final 30 minutes before sending are the highest-risk edits:
- A sentence rewritten to fix one word introduces a subject-verb agreement error
- A section moved creates a dangling reference elsewhere
- A number updated in the body but not in the executive summary
- A conclusion added without checking that it matches the scoring in the scorecard

**Detection:** After any last-minute edit, re-run the full universal checklist on the affected section plus any section that references it.

---

## Error Patterns by Deliverable Type

### Territory Analysis Reports

**Scorecard arithmetic errors**
The 9-dimension scorecard is hand-calculated in most drafts. Common errors:
- Dimension scores that don't match the rubric thresholds applied in the narrative
- Total score = sum of 9 scores, but the total shown is from a prior draft with different scores
- Score label (RECOMMENDED/CONDITIONAL/NOT RECOMMENDED) doesn't match the total score range

*How to check:* Add up every dimension score independently. Compare to the displayed total. Verify the label matches the score range in the scoring key.

**Population order-of-magnitude errors**
Palm Beach County: ~1.5M. Broward: ~1.9M. Miami-Dade: ~2.7M. A misplaced decimal or wrong ACS table pull can show 150,000 instead of 1,500,000.

*How to check:* Google the county population and compare the order of magnitude. ACS Table B01003 should show the full population number.

**Income stated in wrong units**
ACS per capita income for Palm Beach County: $45,447. If the formula divided by 1,000 (common in financial models), it shows as $45.45. Median HH income $84,514 divided by 1,000 shows as $84.51 — plausible but wrong.

*How to check:* Median HH income in most U.S. counties is between $40,000 and $150,000. Per capita income is typically $25,000–$60,000. Any figure outside these ranges in a domestic market is almost certainly a units error.

**Competitor review data from a prior search**
Screenshots taken on different days can show different review counts. If the Smappen screenshots are from last month and the map pack screenshots are from today, the review counts won't match.

*How to check:* Verify that all competitor data was pulled on the same day or within the same week. Note the retrieval date in the citations.

**Seasonal vacancy rate misclassified**
The seasonal vacancy flag triggers at > 10% seasonal vacant units as a % of total housing units. A common error is dividing seasonal vacant by total vacant (not total units), which inflates the percentage.

*How to check:* Seasonal vacancy % = Seasonal vacant units ÷ Total housing units. For Palm Beach: 68,613 ÷ 719,461 = 9.5%. Not 68,613 ÷ 114,033 (total vacant) = 60.2%.

---

### Waterfall / Funnel Diagnostic Reports

**Conversion rates calculated backwards**
QPC→Opp rate should be: QPCs who became Opps ÷ total QPCs. Sometimes the numerator and denominator are swapped or the wrong stage is used.

*How to check:* Every rate = (stage output) ÷ (stage input). Each rate should be < 100%. If any rate is > 100%, there's an error.

**Funnel stages out of order in presentation**
The visual or table shows: Calls → QPCs → PCs → Opps — skipping the PC stage or putting QPC before PC. The correct order is:
Calls + Web Leads → PCs → QPCs → Opps → Consults → Quotes → FAs

*How to check:* Verify against the canonical sequence. Every stage in the report must be in this order.

**Dollar gap calculated with wrong PMV**
The revenue impact of a conversion leak = Missed FAs × avg PMV per FA. If the PMV used is a round number not derived from the firm's actual data, or if PMV is confused with total annual revenue, the gap figure will be wrong.

*How to check:* State the PMV figure used and its source. It must be from the client's waterfall data, not assumed.

**Thresholds stated incorrectly**
Common errors: stating the JIT trigger as Consult Days > 3 (it's > 2), or stating the intake staff hiring trigger as 90% answer rate (it's 85%).

*How to check:* Verify all threshold values against the `family-law-revenue-model` and `intake-funnel-diagnostics` skills.

---

### SEO Audit and Strategy Documents

**Keyword volume figures without stated source or date**
Search volumes change significantly over time and vary by tool. Stating "divorce lawyer Palm Beach — 1,200 searches/month" without a source, tool name, and date is unverifiable and may be wrong.

*How to check:* Every search volume figure must state the tool (e.g., Google Keyword Planner, Semrush, Ahrefs) and the date of the data pull.

**Competitor domain authority or DR figures without tool attribution**
Domain Rating (DR) is an Ahrefs metric. Domain Authority (DA) is a Moz metric. They are not interchangeable. Mixing them in a report, or using one without stating which tool produced it, is an error.

*How to check:* Every authority/ranking metric must state the tool that produced it.

**Rank tracking data for wrong location**
A keyword ranking check run from the wrong city or without a local modifier shows national rankings, not local pack rankings. These are materially different for family law.

*How to check:* Confirm that all local rank data was pulled with the correct geographic target (city, state, or zip code).

**Page count or crawl data that predates a site migration**
If the client recently migrated domains or redesigned their site, old crawl data shows pages that no longer exist.

*How to check:* Verify the crawl date. If the site was migrated within the past 6 months, all crawl data from before the migration date must be discarded.

---

### Monthly Performance Reports

**MTD data presented as full-month data**
A report generated on the 18th of the month shows month-to-date figures. If not labeled as MTD, the client reads them as full-month figures and draws wrong conclusions.

*How to check:* Every data period must be stated explicitly. "April 2026" must mean April 1–30. "April 2026 (MTD as of April 18)" is the correct label for partial-month data.

**YoY comparison using mismatched date ranges**
Comparing April 1–30 2026 vs. April 3–30 2025 because the prior year's data pull was offset. One fewer day in the prior period artificially inflates YoY improvement.

*How to check:* Confirm both comparison periods have the same number of days and the same start/end days of week where possible.

**Conversion events double-counted**
Google Analytics, Google Ads, and CRM can all report conversions for the same underlying event. A phone call that is tracked in GA4, recorded as a Google Ads conversion, and logged in the CRM is one conversion, not three.

*How to check:* Report states explicitly what each conversion event is and which platform it is sourced from. No event should appear in multiple rows unless intentional.

**Spend figures excluding platform fees**
Reported spend is sometimes the media cost only, not including management fees. Client-facing reports should be clear about what is included.

*How to check:* State explicitly whether figures include or exclude management fees.

---

### Proposals and Scope Documents

**Scope that contradicts the pricing**
A proposal includes 3 deliverables in the scope section but the pricing table shows line items for 4 deliverables (or vice versa).

*How to check:* Count deliverables in scope section. Count line items in pricing. They must match exactly.

**Timeline that is already in the past**
"Kickoff: January 2026" in a proposal sent in March 2026.

*How to check:* All timeline dates must be in the future relative to the send date.

**Wrong services listed from a prior proposal template**
A proposal for SEO services still mentions "Paid Search Management" in one bullet because the template wasn't fully cleaned.

*How to check:* Search for service names not relevant to this engagement. Read every bullet in the scope section cold.

---

## The Five Most Embarrassing Errors (In Order)

1. **Wrong client name** — Calling the client by another firm's name. Career-damaging and trust-destroying.
2. **Wrong market/location** — Reporting on Orlando when the client is in Tampa, or citing Palm Beach County data in a Broward County report.
3. **Stale cover date** — Report says January. It's April. Signals the work was sitting untouched for months.
4. **Math error in the executive summary** — The number a client reads first is wrong. Everything after is suspect.
5. **Internal note left in** — "Confirm with Tyler before sending this section" survives in the final PDF. Unprofessional and potentially embarrassing if the note is negative.
