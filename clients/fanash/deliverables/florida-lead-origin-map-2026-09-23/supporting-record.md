# Fanash Family Law — Florida Lead Origin Map, trailing 365 days

**Prepared:** 2026-09-23 · **Client:** Fanash Family Law (fanashfamilylaw.com), SterlingX_Client_ID `8a4bb5d3-2988-4b58-901a-d7ebdb015a10` · **Requested by:** Casey · **Requests:** "create a similar html [to the Ireland lead-origin map] for Fanash family law in florida ... use all the lead data you can get from the past year to today"; then "add hires and make those more prominent"; then "create a toggle so I can turn off and on leads and on and off hires".

## Deliverable

| File | What it is |
|---|---|
| `analysis/out/fanash-family-law-lead-origin-map-365d-2026-09-23.html` | The sheet: zoomable Florida county map, origin bubbles, hired dots and label counts, Leads/Hired layer switches, office marker, sortable origins table |
| `~/Downloads/Fanash_Family_Law_FL_Lead_Origin_Map_365d_2026-09-23.html` | Delivered copy; SHA-256 in `qa/final-sha256.txt` matches the repo file |
| `analysis/out/fanash-family-law-lead-origin-map-365d-2026-09-23.json` | Meta and aggregated origin points, no PII |
| `analysis/out/fanash-family-law-lead-origin-map-365d-2026-09-23.csv` | Lead-level extract (names, emails, phones). **Git-ignored** via `analysis/out/.gitignore`; regenerate with the command below |
| `analysis/leadmap/offices_fanash.json` | Office record, reused by future runs |
| `qa/` | Final run log, DOM dump of the delivered file's rendered notes, screenshots of the three layer states and the footer, SHA-256 |

Regenerate: `python3 analysis/leadmap/leadmap.py --client "Fanash" --days 365 --offices analysis/leadmap/offices_fanash.json --outdir analysis/out`

## Window and source

- Window: 2025-09-24 through 2026-09-23 inclusive (365 days). Fact-table coverage runs 2024-03-20 to 2026-09-22, so the window is fully covered; last recorded event 2026-09-22 (7 leads on 09-21, so the feed is current).
- Source: `sterlingx-insights.all_clients_offline_conversion.all_firms_offline_conversion`, cohort by `Origin_Date_Created` in window, all milestone rows rolled up per lead. Only 1 of 1,392 leads carries a weekend date, so the date is an intake-entry date rather than first-contact time.
- Conversion metric: **Hired** (`Conversion_Status = 'Funded Agreement'`). Fanash records it (260 rows all time), so the sheet shows a real hire rate rather than a fallback stage. Counts are hired-to-date.

## Headline figures

| Measure | Value |
|---|---|
| Raw lead records | 1,404 |
| Same-phone duplicate rows removed | 12 |
| Firm-internal records removed | 0 |
| Unique leads in window | 1,392 |
| Leads plotted in Florida (Florida-issued number) | 946 |
| Hired among plotted | 83 (8.8%) |
| Origin cities (rate centers) | 88 |
| Excluded: phone exchange out of state | 405 (36 of them hired, 8.9%) |
| Excluded: no phone | 30 (8 of them hired) |
| Excluded: exchange unresolved | 11 |
| Hired in the whole window | 127 |

Top origins. Rates are hired-to-date; the sheet withholds rates below 5 leads and rounds to whole percents below 50 leads, and this table follows the same rule.

| Origin (rate center) | Leads | Hired | Rate |
|---|---|---|---|
| Orlando | 224 | 21 | 9.4% |
| Cocoa (see Brevard note) | 87 | 5 | 5.7% |
| Kissimmee | 85 | 6 | 7.1% |
| Winter Park | 81 | 6 | 7.4% |
| Tampa (five billing zones merged) | 38 | 4 | 11% |
| Lakeland | 33 | 4 | 12% |
| Winter Haven | 28 | 0 | 0% |
| Leesburg | 22 | 3 | 14% |
| Daytona Beach | 19 | 1 | 5% |
| Miami | 19 | 4 | 21% |
| Melbourne | 17 | 1 | 6% |
| Sanford | 17 | 3 | 18% |

The four largest origins are 50% of plotted leads. Volume concentrates on Orange and Osceola counties around the single Orlando office, with Brevard (Cocoa + Melbourne + Titusville ≈ 111) and Polk (Lakeland + Winter Haven + Lake Wales + Bartow + Haines City + Fort Meade ≈ 81) as the next tiers. Winter Park's rate center straddles Orange and Seminole; Seminole proper (Sanford, Oviedo) is about 19. Tampa Bay and South Florida are thin.

## What the reader must not misread

1. **Plotted totals are leads carrying a Florida-issued number, not the Florida book.** Origins are rate-center cities derived from the phone exchange, which marks where the number was issued, not where the caller lives. The 405 leads excluded as out of state hired at 8.9% (36 of 405), comparable to the 8.8% for Florida-issued numbers. **Hypothesis:** most of those 405 are Florida residents whose mobile number was issued elsewhere (top exchange states NY 64, CA 35, GA 25, VA 21, NJ 20). If so, the Florida book is roughly 35–45% larger than the plotted 946. Hire-rate parity is the only support for this; it is an inference, not a demonstration. Fanash's CallRail `customer_state` field cannot corroborate it because CallRail derives `customer_city` and `customer_state` from the phone number's original assigned location (CallRail API v3 documentation, fetched 2026-09-23), the same geography as the exchange lookup. An earlier draft of this record cited that field as corroboration; the reviewer caught it and it is withdrawn. Total hires in the window are 127; the sheet's 83 is the Florida-number subset.
2. **Two lead populations are blended.** By origin platform over the 1,392 leads: Clio Grow 756 leads, 112 hired (14.8%); Manual Intake 636 leads, 15 hired (2.4%), first seen 2026-01. The 8.8% headline and every city rate mix a ~15% CRM-captured population with a 2.4% manually logged one, in proportions that vary by city. What "Manual Intake" captures operationally (prospects, or every logged inbound call) is **unknown**; if those rows are not prospects, lead counts are inflated by up to 46%. The sheet now states the split in its Source note. Reviewer finding, verified from the extract.
3. **Cocoa is a Brevard rate center, not the city of Cocoa (hypothesis).** In the exchange cache, 60 distinct 321-area-code exchanges resolve to "Cocoa" against 15 to "Melbourne", while the Melbourne/Palm Bay area has roughly three times Cocoa/Rockledge's population. Many Brevard wireless blocks appear to be homed to the Cocoa rate center. Read Cocoa 87 as "Brevard County numbers", not as demand in Cocoa itself. Reviewer finding; exchange counts verified, carrier homing not confirmed.
4. **Rates are hired-to-date.** Leads created Sep 2025–Mar 2026 hired at 11.1% (67 of 606); Apr–Sep 2026 at 7.6% (60 of 786); the last 90 days at 7.2% (30 of 417). Recent leads have had less time to sign, so the blended 8.8% and recent-heavy cities read low. The Hired note on the sheet now says so.
5. **City precision only.** Zooming reveals more labels, not more precision. The precision column reads "City (exchange)".
6. **No lead-level zip exists for Fanash.** Established by a manual query, not by the pipeline probe: the CallRail export `fanishe_family_law.call_data` (misspelled dataset name; `company_name` "Fanash Family Law", business phone 800-468-0777) has a `zip_code` column with 0 of 374 rows populated and covers only 2025-09-08 to 2025-11-07. The probe's name match (`%fanash%`) cannot find a misspelled dataset; it now logs its candidates and accepts `--zip-dataset`. The form webhook source named in `clients.clients.Web_Form_Summary_Mapping` lives in a different project and was not queried.

## Volume over time (observations)

Unique leads by month of intake entry, split by origin platform (Clio Grow / Manual Intake): Sep 2025 (7 days) 19/0 · Oct 77/0 · Nov 59/0 · Dec 41/0 · Jan 2026 69/67 · Feb 65/66 · Mar 71/72 · Apr 51/67 · May 61/73 · Jun 65/79 · Jul 64/99 · Aug 70/97 · Sep 1–22: 44/16.

- **January step (+95).** About 70% is the Manual Intake source appearing (0 → 67); about 30% is Clio Grow rising 41 → 69, consistent with the January family-law seasonal peak. The `clients.clients` record creation date (2026-02-15) postdates the step and is not the explanation; an earlier draft of this record said it might be.
- **September dip.** Manual Intake logged nothing Sep 1–14, 1 lead in the week of Sep 8, then 14 in the week of Sep 15; Clio Grow ran 44 in 22 days against 70 in August (about −17% per weekday). The feed is current (last event 2026-09-22), so this is not pipeline lag. **Hypothesis:** an intake-process change around Sep 1 paused manual logging. Ask the client what changed.

## Data quality flags

- Platform mix: Manual Intake+call 535, Clio Grow+call 506, Clio Grow 131, Clio Grow+webform 98, Manual Intake 93 (raw labels; families as above).
- The 12 removed rows were same-phone collisions on the same lead; the pipeline cannot tell caller-ID artefacts from genuine repeat entries, so "duplicate" means same phone.
- The first pipeline run reported `arizona_family_law.call_data` as a Fanash zip source because the generic word "family" matched. Corrected before delivery (pipeline change 1).

## Pipeline changes for this task (`analysis/leadmap/leadmap.py`)

1. **Zip-source probe.** Generic firm-name words (family, legal, group, associates, etc.) are excluded from the dataset-name match; each candidate column is checked for populated rows before it is reported; the probe logs the words used and the candidates found; a new `--zip-dataset` flag pins a dataset the name match cannot find.
2. **Cross-year period label.** The start year is printed when the window spans two calendar years.
3. **Telco billing-zone merge.** Rate centers differing only by a trailing Central/North/South/East/West are merged into the base city when two or more variants share the base or the base already exists as a point. Tampa Central/North/East/West/South (27+4+4+2+1) became Tampa 38, with a lead-weighted centroid. The reviewer judged the rule sound: it runs after the out-of-state filter, the guard protects genuine names ending in a direction word, and prefix-direction places (North Naples, West Palm Beach) are untouched.
4. **Out-of-state conversions surfaced.** `build()` counts excluded out-of-state leads that still reached the metric (`dropped_oos_conv`); the sheet's "Florida only" note states the count and rate.
5. **Origin platform families in meta.** `build()` summarises leads, conversions and first month by platform family (`Clio Grow+call` → `Clio Grow`); the sheet's Source note lists them when there is more than one.

## Template changes (`analysis/leadmap/template.html`)

- **Hires prominent** (Casey's request): every city label carries its conversion count in the hired colour ("Orlando 224 · 21 hired"); the conversion dot keeps area proportional to conversions with a 2.2 px floor and a sheet-coloured ring; the conversion KPI, Hired column cells above zero, and footer total are set in the hired colour; legend reads "Hired (inner dot; count in label)".
- **Layer switches** (Casey's request): the legend's Leads and Hired entries are checkboxes. Both on is the default. Leads only removes dots and label counts and hides the Hired and Rate columns. Hires only hides zero-hire cities, redraws the rest in the hired colour with area proportional to hires on their own scale (largest hire count gets the 20 px bubble), relabels "Orlando 21 hired", filters the table to origins with hires sorted by hires, and sets the header to "83 hires · 32 origins with hires". Both off leaves counties and offices. Label placement re-runs on every switch. `window.setLayers(leads, hires)` supports scripted checks.
- **Wording after review:** "Totals describe leads carrying a FL number, not the whole pipeline" (was "the Florida book", which contradicted the next sentence); the out-of-state conclusion is phrased as a suggestion and fires only when out-of-state conversions are at least 5 (MIN_N) and their rate is at least 75% of the in-state rate; the Hired note adds the hired-to-date clause; the Geocoding note mentions directional zones; precision reads "City (exchange)".
- **Rate precision after review:** rates withheld below 5 leads (was 3) and shown as whole percents below 50 leads; the Rates note explains both.
- **Platform sentence** in the Source note, from pipeline change 5.
- Backward compatible: every new sentence is skipped when its field is absent, so older JSON renders unchanged apart from the wording fixes.

## Verification performed

- Client identity: `clients.clients` row matches name, Orlando address, Florida, website.
- Office: fanashfamilylaw.com/locations/ and /contact-us/ fetched 2026-09-23 list one office, 111 N Orange Ave Suite 800, Orlando FL 32801; geocoded via Nominatim (28.5438004, -81.3787676, Orange County).
- Figures recomputed from the JSON and CSV independently of the sheet by the strategist and again by the reviewer (Σ leads 946, Σ hired 83, 946+405+30+11 = 1,392, 83+36+8 = 127 hires, monthly counts sum to 1,392).
- Final build: `qa/final-run.log` is the run that produced the delivered HTML; `qa/final-render-dom.html` is the rendered DOM of that exact file and contains every expected note sentence; `qa/render-both.png`, `qa/render-leads.png`, `qa/render-hires.png`, `qa/render-footer.png` are headless Chrome renders of it; `qa/final-sha256.txt` shows the Downloads copy is byte-identical. Earlier in the task a template edit used an undefined helper and silently blanked the notes block; it was caught by a DOM dump, which is why the DOM check is now part of the agent's verification steps.
- Regression: Michael Ireland & Associates, 60 days, run on the final code: notes render, platform sentence renders, the out-of-state conclusion is correctly suppressed (1 hire of 62). Side finding: Ireland now records Funded Agreement (27 all time) where it had none on 2026-08-13.

## Independent review (seo-reviewer, read-only, 2026-09-23)

The reviewer recomputed the figures from the JSON and CSV (no PII quoted), fetched the client's site and the CallRail API documentation, and read the pipeline, template, and this record. It reported 2 blockers, 9 material improvements, 8 optional refinements. Dispositions:

| # | Finding | Disposition |
|---|---|---|
| B1 | CallRail `customer_state` is number-derived, so it is not residency evidence; the "mostly Florida residents" claim was overstated and one rate was misquoted | **Accepted, verified against the API docs.** CallRail sentence withdrawn; residency reframed as a hypothesis on hire-rate parity alone; rates corrected to 8.9% vs 8.8%; on-sheet wording softened to "suggests". |
| B2 | The delivered file's notes block had not been verified in its final form; the on-disk DOM dump and footer screenshot predated the last edits | **Accepted.** The check had been run but the artefacts were stale. Final DOM dump, renders, run log and SHA-256 now sit in `qa/` for the exact delivered file. |
| M1 | Manual Intake is 46% of leads, began 2026-01, hires at 2.4% vs Clio Grow 14.8%; the blended rate hides this | **Accepted, verified.** Platform split added to the pipeline meta and the sheet's Source note, and to this record. What Manual Intake captures is an open question for the client. |
| M2 | Both monthly hypotheses were wrong or weakly evidenced | **Accepted, verified.** Replaced with the platform-split observations; only the cause of the Sep 1–14 pause remains a hypothesis. |
| M3 | "Totals describe the Florida book" contradicted the next sentence; "understates by 30%" had an ambiguous base | **Accepted.** Template and record reworded. |
| M4 | Cocoa 87 is probably a Brevard rate-center concentration | **Accepted as hypothesis; exchange counts verified (60 vs 15).** Annotated here and in the summary; a county rollup table is a follow-up, not done. |
| M5 | One-decimal rates on 3–6 leads overstate precision | **Accepted in part.** MIN_N raised to 5 (reviewer suggested 10–20); whole percents below 50 leads. Agent definition updated. |
| M6 | Cohort maturity undisclosed | **Accepted, verified (11.1% vs 7.6%).** Clause added to the Hired note and this record. |
| M7 | PII CSV untracked but unprotected | **Accepted.** `analysis/out/.gitignore` ignores `*.csv`; verified with `git check-ignore`. The root `.gitignore` was left alone because another session has uncommitted edits in it. Pre-existing Ireland lead CSVs under `analysis/` remain tracked from August and are outside this task. |
| M8 | Zip probe reached the right answer for the wrong reason | **Accepted.** Record attributes the empty-zip finding to the manual query; probe now logs candidates and takes `--zip-dataset`. A `company_name` fallback is a follow-up. |
| M9 | Tested version must equal committed version | **Accepted.** Final run from final code; `qa/final-run.log` kept; commit contains exactly the producing files. Peer session `seo-dept-c3` was idle and had no edits under `analysis/leadmap/`. |
| O1 | Label collisions at 1× worsened with the hired suffix | **Not changed.** Casey asked for hires to be prominent; the 3.2× view is clean and labels re-place on zoom. |
| O2 | "City" overstates exchange precision | **Accepted.** Precision reads "City (exchange)". |
| O3 | Geocoding note should mention directional zones | **Accepted.** |
| O4 | 50% "comparable" threshold too loose | **Accepted.** Raised to 75%. Fanash (8.9 vs 8.8) unaffected. |
| O5 | "Lead creation date" is really intake-entry date | **Accepted in the record** (1 weekend-dated lead of 1,392); the template wording is left generic. |
| O6 | "Caller-ID duplicates" overstates what the pipeline knows | **Accepted in the record.** |
| O7 | County narrative misweighted Polk vs Seminole | **Accepted, verified (Polk ≈ 81, Seminole ≈ 19).** |
| O8 | Billing-zone merge rule sound | Noted. |

Checks the reviewer could not perform: execute JavaScript or the pipeline; query BigQuery (raw 1,404 rows, stage counts, `clients.clients` fields, the `fanishe_family_law` zip count, out-of-state state breakdown); confirm localcallingguide's Cocoa homing; confirm what Manual Intake means. The strategist ran the JavaScript and pipeline checks; the BigQuery figures are the strategist's own queries; the last two remain open.

Remaining disagreement: none material. The reviewer would raise MIN_N further than 5; the strategist kept 5 so that mid-sized cities keep a readable rate while the whole-percent rounding removes false precision.

## Open items for Casey / the client

1. What does the `Manual Intake` origin platform capture, and why did it pause Sep 1–14, 2026? This decides whether 636 rows are prospects and what the September dip means.
2. Should Brevard be read as one market? Cocoa 87 is probably Brevard-wide numbers, not Cocoa demand.
3. Read access to `rc-datamart-forms-webhook.webhook_wordpress_fanashfamilylaw.*` is the only plausible lead-level zip source.
