# Aurit Mediation — 2026 Strategy Buildout: QA & Reconciliation Notes

**Deliverable:** `Aurit_2026_Strategy_Buildout_Divorce_ChildSupport_ChildCustody_SpousalMaintenance.csv`
**Sections built:** Divorce Mediation, Child Support Mediation, Child Custody Mediation, Spousal Maintenance Mediation
**Structural source of truth:** `preview (1).html` (Hub Page Format & Expansion Structure V4)
**Metadata source:** Architecture Master Production V4 → `Master_Architecture`
**Format source:** `Aurit Mediation _ 2026 Day Strategic Plan - Internal - Q3-4 2026.csv`

---

## 1. What was built

54 deliverable rows in the strategy sheet's exact 13-column format
(`Status, CU, Projects, Description, Impact, July, Aug, Sep, Oct, Nov, Dec, Jan, Beyond`).

| Row type | Count | What it is |
|---|---|---|
| Core Service Hub Page | 4 | **One row per hub page** — page frame **plus all its H2 section modules**, since those are content on the hub URL, not separate deliverables |
| Child page rows | 45 | One per linked child URL — Situational (18), Process (9), Comparison (6), Resource (6), Educational (5), FAQ (1) |
| Live Page V4 Retrofit | 5 | Already-published pages needing return links, sibling links, and correct hub anchor placement — not re-written |

### One page = one row = one ticket

The 21 H2 section modules are **folded into their parent hub row**, not listed separately. An H2 section
lives on the hub URL, so splitting one page into seven tickets would create artificial handoffs on a single
document. This also matches the sheet's existing convention — *County Service Area Pages* is one row
covering many pages, split 12/12 across July and August.

Each hub description is structured so a writer can build the whole page in one pass:

```
URL: /divorce-mediation/
Scope: page frame plus all SIX H2 section modules on this one URL...

PAGE FRAME (8 hrs)
  - Unlinked H1, 2-3 para overview, trust proof, CTA, jump-link TOC...

H2 SECTION 1 - Compare Divorce Mediation With Other Divorce Options (3 hrs)
  Internal group: Options, Alternatives & Legal Pathways - internal label only, never the public heading
  - Unlinked H2 + 1-2 sentence intro
  - 2 featured cards: Mediation vs Litigation; Divorce Mediator vs Divorce Attorney
  - 1 text link: Mediation vs Collaborative Divorce
  - 2 on-hub topics, unlinked H3/H4, 150-450 words each: Legal Separation Mediation; ...
  Do not surface Annulment Mediation (governance: do not build).
... H2 SECTIONS 2-6 ...

PUBLISHING SEQUENCE
- Phase 1: publish the frame, every H2, every section intro, every unlinked on-hub topic (no child URLs needed)
- Phase 2: stage the card and text-link slots; activate now where the child page is already live
- Phase 3: as each expansion page publishes, switch on its prepared anchor - no hub rebuild
```

Per-section hours stay visible inside the description and are QA-verified to sum to the booked
month-column hours, so the 28 / 21 / 20 / 19 hub totals remain auditable.

**Why this sequencing matters:** the hub is structurally complete before any expansion page is written,
so each child page publishes into a section that already ranks and already passes internal authority —
instead of arriving as an orphan that triggers a hub rewrite.

Each `Projects` name encodes the HTML role explicitly, e.g.
`Core Comparison Content Page / - Mediation vs Litigation (Divorce Mediation - Featured H3 Card)`

Each child `Description` restates the URL, word-count band, tier/wave/priority, required return link,
internal links, hub placement, and legal guardrail from the V4 architecture.

---

## 2. QA results — all checks pass

Verified programmatically against the HTML, not by eye (`aurit_qa_check.py`, `aurit_qa_check2.py`):

| Check | Result |
|---|---|
| Header matches strategy sheet exactly; all rows 13 columns | PASS |
| Duplicate project names | PASS — none |
| All 50 HTML child links covered (27 / 7 / 7 / 9) | PASS |
| All 50 HTML on-hub topics covered (19 / 12 / 8 / 11) | PASS |
| All 21 HTML H2 sections embedded as blocks in the correct parent hub row (6 / 5 / 6 / 4) | PASS |
| Hub hours declared per section sum exactly to hours booked in month columns | PASS (28 / 21 / 20 / 19) |
| All 12 governance items carried as explicit "do not surface" instructions | PASS |
| URL counts reconcile to HTML header pills (28 / 8 / 8 / 10) | PASS |
| Every child page carries the HTML's role (Featured H3 Card vs Supporting Text Link) | PASS |
| **Guardrail:** no on-hub topic or governance item was given its own page row | PASS — 0 leaks |
| Every build row traces back to a real HTML child link (no invented pages) | PASS — 0 orphans |
| Every URL in the plan exists in the V4 architecture CSV (54 distinct) | PASS |

Two failures surfaced on the first QA run and were traced to bugs in the *checker*, not the content:
an em-dash vs hyphen normalization miss, and a `"Child"` prefix collision that matched Child Support
modules against Child Custody. Both fixed in pass 2; content was correct as written.

---

## 3. Hours and capacity

Rate card used (derived from the sheet's existing 4-hour situational pages and 5-hour Areas We Serve hub):

| Deliverable | Hrs | | Deliverable | Hrs |
|---|---|---|---|---|
| Hub page frame (1,800–2,800 w) | 8 | | Resource / tool + checklist | 5 |
| Hub page frame (1,600–2,600 w) | 6 | | Situational / Comparison / Process | 4 |
| H2 section, 4–6 on-hub topics | 4 | | Educational / glossary | 3 |
| H2 section, 2–3 on-hub topics | 3 | | FAQ page | 3 |
| H2 section, 0–1 on-hub topics | 2 | | Live page V4 retrofit | 1 |

Rolled up, each hub row books **frame + all its sections**:

| Hub row | Frame | Sections | Total | Scheduled |
|---|---|---|---|---|
| Divorce Mediation | 8 | 20 (6 sections) | **28** | Sep |
| Child Support Mediation | 6 | 15 (5 sections) | **21** | Oct |
| Child Custody Mediation | 6 | 14 (6 sections) | **20** | Nov |
| Spousal Maintenance Mediation | 6 | 13 (4 sections) | **19** | Nov 9 + Dec 10 |

| Month | Existing | New | Combined |
|---|---|---|---|
| July | 53.5 | — | 53.5 |
| Aug | 44.5 | — | 44.5 |
| Sep | 19 | 31 | **50** |
| Oct | 26 | 23 | **49** |
| Nov | 20 | 30 | **50** |
| Dec | 20 | 30 | **50** |
| Jan | 20 | 32 | **52** |
| Beyond | 0 | 120 | 120 |
| | 203 | **266** | 469 |

Sep–Jan lands in a 49–52 hr band against the ~50 hr/month capacity implied by July and August. Nothing
was added to July or August — both are already committed.

**Sequencing follows the architecture's own instruction** (`Master_Architecture` row 3): *"Strengthen the
hub first, build the H2 modules, feature approved child pages, list remaining standalone pages, and keep
section-first or FAQ topics on the parent."* So all four hub pages — frame and every H2
section — land Sep–Dec, and child pages fill in behind them by Tier/Wave priority. The three-phase
publishing sequence in each hub row means no hub is blocked waiting on a child page, and no child page
arrives without a parent section to publish into.

120 hours sit in **Beyond** (~4 months at this rate). That is the honest remainder — 266 hours of work
does not fit in 5 months at 30 spare hours each. Pull items forward by trading against the 18 hrs/month
City Service Area Pages commitment if you want the clusters closed sooner.

---

## 4. Conflicts between the current strategy and the V4 architecture — decisions needed

These are the items I could not resolve from the source files. **Four have hours already allocated**, so
they need a call before those sprints run.

### 4a. Funded rows that V4 demotes to on-hub content (no URL)

| Existing strategy row | Hrs | V4 says | Action |
|---|---|---|---|
| Core Situational Content Page - **Grandparent Rights Mediation** (Child Custody) | **4 (Aug)** | FAQ-only on hub, no URL — Rec #210 | Reallocate the 4 hrs, or approve an exception. Covered by the *Grandparent and Extended-Family Custody Mediation* module row. |
| Core Situational Content Page - **Complex Income Support Mediation** (Child Support) | **4 (Aug)** | *Variable Income Child Support Mediation* is Section-First on hub — Rec #128 | Reallocate the 4 hrs. Covered by the *Complex Income and Employment* module row. |

Both are in the August sprint that is running now. Recommendation: **honor V4 and reallocate**, because
building either as a standalone page creates a thin URL competing with its own hub section.

### 4b. Backlog rows V4 demotes or forbids

| Backlog row | V4 says | Action |
|---|---|---|
| **LGBTQ+ Divorce Mediation** (Divorce) | Section-First on hub — Rec #188 | Retire row; covered on-hub in *Parents and Families* module |
| **Add-On Expenses Mediation** (Child Support) | Three Section-First topics on hub — Recs #131/162/163 | Retire row; covered by *Childcare, Medical, and Other Child Expense* module |
| **Support Deviation Mediation** (Child Support) | FAQ-only on hub — Rec #233 | Retire row; covered in *Guidelines, Calculations, and Preparation* module |
| **Short-Term / Rehabilitative Maintenance Mediation** (Spousal) | Two FAQ-only topics on hub — Recs #239/240 | Retire row; covered in *Types and Duration* module |
| **Emergency Custody Mediation** (Child Custody) | **Governance — Do Not Build** — Recs #258/259/260 | **Retire the row.** Ranking for emergency custody generates inquiries mediation cannot serve. Handled as a guardrail section in the *Emergency Child Custody and Safety Considerations* module |
| **Fast Divorce Mediation** (Divorce) | **Hold / Conditional** — Rec #74 | Do not build. Audit `/quick-divorce-arizona/` first and consolidate against *Uncontested Divorce Mediation* and *Divorce Mediation Timeline* before any new fast-divorce URL |

### 4c. Duplicate high-value page — resolve before Oct

`High-Net-Worth Divorce Mediation` is marked **Complete** (ClickUp 86b93344j), but V4's canonical divorce
page is `/divorce-mediation/high-asset-divorce-mediation/` (Rec #40), with *High-Net-Worth Property
Division Mediation* held as Section-First under the **Property** hub (Rec #87).

Two near-identical pages targeting the firm's most profitable segment will split their own authority.
The Oct retrofit row (2 hrs) covers confirming the live URL and canonicalizing or 301-ing the variant —
**someone needs to confirm which URL is actually live** before that ticket runs.

### 4d. Backlog rows superseded by named rows in this deliverable

Retire these; they are now built under their approved architecture names:

`Divorce Mediation vs Litigation` → Mediation vs Litigation ·
`Divorce Mediation vs Collaborative Divorce` → Mediation vs Collaborative Divorce ·
`Mediation for Self-Represented Couples` → same ·
`Military Divorce Mediation` → same ·
`Temporary Maintenance Mediation` → Temporary Spousal Maintenance Mediation ·
`Communication & Decision-Making Disputes` → splits into **Co-Parent Communication Mediation** (custody
child page) + **Decision-Making for School and Medical Issues** (on-hub)

### 4e. Two rows carry zero hours by design

| Row | Why |
|---|---|
| Child Support Modification Mediation | Already In-Progress, 4 hrs funded in July (86bb2fggu). Row exists so the 8-URL cluster reconciles and to lock hub placement. |
| Spousal Maintenance for Long-Term Marriage | Already funded, 4 hrs in Aug as *Long-Term Marriage Maintenance Mediation*. **Rename that row** to the approved architecture name, and split scope from *Long-Term Spousal Maintenance Mediation* (structure/duration) so the two don't cannibalize. |

### 4f. Sheet hygiene (not blocking)

The bottom ~30 rows of the current sheet have impact tags — `Traffic, Conversions`, `Conversions, Sales
(Monetization), Frequency` — sitting in the **Status** column. That breaks status filtering. Those values
look like they belong in a separate Impact-Category column. New rows use blank Status, matching the
sheet's other planned rows.

---

## 5. Scope covered vs remaining

These four hubs are 54 of the 139 URLs in the V4 architecture.

| Hub / root | URLs | Status |
|---|---|---|
| Divorce Mediation | 28 | **Built** |
| Spousal Maintenance Mediation | 10 | **Built** |
| Child Support Mediation | 8 | **Built** |
| Child Custody Mediation | 8 | **Built** |
| Property and Debt Division Mediation | 16 | remaining |
| How Mediation Works | 14 | remaining |
| Parenting Plan Mediation | 13 | remaining |
| Locations | 12 | remaining |
| About Aurit Mediation | 10 | remaining |
| Post-Decree Mediation | 6 | remaining |
| Pricing / Online Divorce Mediation | 3 + 3 | remaining |
| Home / Contact / Reviews / Resources / Legal | 2+1+1+2+2 | remaining |
| **Total** | **139** | 54 built · 85 remaining |

Highest-value remaining: **Parenting Plan** (13 URLs — and the custody hub is scoped against it, so the
cannibalization boundary stays theoretical until it is built) and **Property and Debt Division** (16 URLs,
Tier 1 Wave 1, and it already has four funded rows sitting in July/Aug: Business Owner, Retirement &
Pension, Real Estate & Home Equity, Business Valuation).

---

## 6. Cross-hub dependencies flagged inside the rows

- **Child Custody ↔ Parenting Plan** — custody owns decision-making authority and legal framework;
  parenting plan owns schedules and logistics. Noted on the custody hub row.
- **Child Custody ↔ Post-Decree** — pre-decree relocation vs post-decree relocation kept distinctly scoped.
- **Child Support ↔ Property** — self-employment income pages cross-link into Business Owner Divorce Mediation.
- **Spousal ↔ Property / Divorce** — high-income maintenance links to high-asset divorce, RSUs, lump-sum.
- **Spousal ↔ Divorce** — Gray Divorce retrofit wires into retirement and maintenance clusters.
- **Two live calculators** (Alimony 86ba3xwy8, Child Support 86ba3xx29) are currently orphaned assets.
  The *Guidelines/Calculations* and *Calculation, Income & Tax* module rows both require cross-linking
  them so calculator traffic converts into hub engagement.

---

## 7. Terminology standard applied throughout

Arizona statutory language, per the architecture's guardrails:
**legal decision-making** (not custody), **parenting time** (not visitation), **spousal maintenance**
(not alimony). Colloquial variants are captured through existing URL slugs
(`/spousal-support-alimony-mediation/`) rather than new URLs.
