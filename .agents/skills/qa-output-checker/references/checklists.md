# QA Checklists — Fast Reference

Condensed checklists for rapid review. No explanations — see SKILL.md for context.

---

## UNIVERSAL (Every deliverable)

**Client Identity**
- [ ] Client firm name correct and consistent throughout
- [ ] No other client's name anywhere in the document
- [ ] Client contact name correct and spelled correctly
- [ ] Client location/market correct (county, state, city)

**Dates**
- [ ] Cover/report date is current
- [ ] All data periods consistent throughout
- [ ] No "last year" / "next year" without specific year
- [ ] Data not more than 12 months stale without flagging

**Rocket Clicks Branding**
- [ ] "Rocket Clicks" spelled correctly (not RocketClicks, Rocket Click, RC)
- [ ] No internal Slack language or shorthand
- [ ] No internal project codes or ticket numbers
- [ ] No internal names or emails not intended for client

**Placeholders**
- [ ] No `[INSERT]`, `[TBD]`, `[CLIENT NAME]`, `[DATE]`, `[MARKET]` or similar
- [ ] No Lorem ipsum
- [ ] No TODO / FIXME / TK / XX / XXX
- [ ] No tracked changes or comments visible
- [ ] No formula errors: #REF! #DIV/0! #VALUE! #N/A #NAME?

**Tone and Language**
- [ ] No hedging: "I think," "maybe," "sort of," "probably," "I'm not sure"
- [ ] No casualisms: "basically," "honestly," "tbh," "super," "lol"
- [ ] Numbers formatted consistently ($, commas, % symbols)
- [ ] No all-caps words outside proper acronyms

**Completeness**
- [ ] All TOC sections are present in body
- [ ] All referenced figures/tables/appendices are present
- [ ] No broken cross-references ("see Section X")
- [ ] Conclusion/recommendation section present and makes an actual recommendation

---

## DATA INTEGRITY

**Internal Consistency**
- [ ] Exec summary numbers match body numbers
- [ ] Chart numbers match table numbers match text numbers
- [ ] Table totals sum correctly
- [ ] Percentages sum to 100% where appropriate
- [ ] Comparison periods are truly comparable

**Citations**
- [ ] Every statistic has a source
- [ ] No `[source]` or `[citation needed]` remaining
- [ ] ACS data: table code + year stated
- [ ] Web data: search query + date retrieved stated
- [ ] No statistics presented as current if source > 3 years old

**Territory Analysis**
- [ ] Score totals are correct arithmetic
- [ ] Population figures pass sanity check (right order of magnitude)
- [ ] Income figures in correct units (dollars not thousands)
- [ ] Vacancy rate = vacant ÷ total housing units
- [ ] Competitor data matches screenshots

**Waterfall / Funnel**
- [ ] Conversion rates: correct numerator ÷ denominator
- [ ] No conversion rate > 100%
- [ ] Funnel stages in correct order
- [ ] Dollar gap arithmetic verified
- [ ] Correct threshold values used (Consult Days > 2; answer rate > 85%)

**Paid Search / Performance**
- [ ] Figures are for stated date range only
- [ ] CTR spot-check: Clicks ÷ Impressions
- [ ] CVR spot-check: Conversions ÷ Clicks
- [ ] ROAS spot-check: Revenue ÷ Spend
- [ ] No negative impressions, clicks, or spend
- [ ] MTD vs. full month clearly distinguished

---

## DOCX

- [ ] Heading hierarchy correct (H1 → H2 → H3, no skipped levels)
- [ ] Consistent heading styles (not manually bolded text)
- [ ] Page numbers in footer
- [ ] Header: doc title and/or client name
- [ ] Cover page complete: client name, title, date, RC branding
- [ ] TOC matches actual headings and page numbers
- [ ] No orphaned headings at bottom of page
- [ ] All table headers present and bolded
- [ ] No tables breaking across pages without repeating header
- [ ] Images clear, not pixelated
- [ ] No broken image placeholders
- [ ] Consistent margins throughout

---

## PPTX

- [ ] Slide count matches scope
- [ ] Every slide has a title
- [ ] No "Click to add title" / "Click to add text" defaults
- [ ] Slide numbers present and sequential
- [ ] No internal speaker notes in delivered version
- [ ] Bullets are parallel in structure
- [ ] No bullets > 2 lines
- [ ] Consistent body font sizes across same-type slides
- [ ] All charts have axis labels, title, and legend (if multi-series)
- [ ] Chart data matches slide narrative

---

## XLSX

- [ ] No tab named "Sheet1" or "Sheet2"
- [ ] No unused blank tabs
- [ ] Input cells distinguished from formula cells
- [ ] No formula errors: #REF! #DIV/0! #VALUE! #N/A #NAME? #NULL! #NUM!
- [ ] Spot-check 3 totals: do they sum correctly?
- [ ] No negative values in logically non-negative fields
- [ ] Date cells formatted as dates, not text
- [ ] Currency cells: $ sign, consistent decimals
- [ ] Percentage cells formatted as %, not decimals
- [ ] Filter/freeze panes on tables > 10 rows
- [ ] Column widths accommodate content
- [ ] Print area set if file is expected to print

---

## QUICK HUMAN ERROR SCAN

Run these five targeted searches on every deliverable:

1. **Name swap:** Search for all Rocket Clicks client firm names worked on in past 90 days — flag any that appear in the wrong document
2. **Placeholder sweep:** Search `[` and `TBD` and `TODO` and `TK` — flag every hit
3. **Number cross-check:** Pull every number from executive summary, verify against its source section
4. **Date audit:** List every date in the document — are they all correct and consistent?
5. **Reference audit:** List every "see Section X" / "Figure X" / "Appendix X" reference — verify each one resolves
