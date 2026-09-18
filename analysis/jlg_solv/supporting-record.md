# Johnson Law Group — SoLV month over month by location

Date: 2026-09-18. Source: `sterlingx-insights.firm_marketing_localbrandmanager.johnsonlaw_localbrandmanager_geogrids`
(Local Brand Manager geogrid export). 687 rows, 2026-02-11 to 2026-09-14.
Query: `analysis/jlg_solv/solv_monthly.sql`. Output: `analysis/jlg_solv/solv_monthly.csv`.

## Data handling decisions (each verified against the table)

1. **Location key is `geogrid_config_id`, not `business_place_id`, address, or store code.**
   Englewood switched from a street address to `Service Area Business` on 2026-07-13;
   Cheyenne appears under three name/address spellings; Chicago has a NULL store code.
   `geogrid_config_id` is 1:1 with the 8 locations across all 687 rows.
2. **Deduped the 2026-03-20 double scan.** 12 (location, term) pairs ran twice ~4 minutes
   apart that day (e.g. Englewood "englewood divorce lawyers" 0.71 and 0.66). Averaged
   within (location, term, day) so the day carries single weight.
3. **Fort Collins term mix changed.** `divorce attorney` and `fort collins divorce attorney`
   were added 2026-06-01, giving it 6 terms vs 4 everywhere else. Excluded from the trend
   so the month-over-month comparison is like-for-like.
4. **Dropped 2026-05-27**, a partial run where Fort Collins, Denver and Colorado Springs
   each recorded only 1 of 4 terms. A single-term day would bias that day's average.
5. **Months are averages of scan days, not of rows**, so a month is not weighted by how
   often the scanner happened to run. Cadence is irregular: 1 scan day in Feb, 2 in Mar,
   2 in Apr, 2 in May (1 usable), then weekly from June (5/4/6/2).
6. **September is partial** — through 2026-09-14 only (2 of ~4 weekly scans).
7. **SoLV is stored 0-1**; reported here as a percentage.

## Metric semantics (verified behaviourally, formula not vendor-confirmed)

`agr` is average rank across grid points where the listing appeared; `atgr` penalizes
non-appearance as 21. Grid coverage recovers as `(21 - atgr) / (21 - agr)`.

SoLV behaves as a top-3 (map pack) share of grid points: rank 1.0 everywhere = 100%
(Commerce City geo-modified terms), rank 3.56 everywhere = 60.6% (Englewood
"englewood family lawyers"), rank ~14 = 0% (Denver, Cheyenne). The exact vendor formula
is **unverified**; treat the top-3 reading as an inference from these observations.

**This matters because SoLV 0% has two distinct causes**, separable only via `agr`
(August 2026 figures):

| Location | SoLV | agr | atgr | Grid coverage | Reading |
|---|---|---|---|---|---|
| Commerce City, CO | 90.5% | 1.78 | 1.93 | 99.2% | Dominant |
| Englewood, CO | 21.4% | 8.92 | 11.65 | 62.2% | Real but geo-term dependent |
| Colorado Springs, CO | 6.8% | 11.80 | 16.58 | 43.9% | Weak |
| Chicago, IL | 2.2% | 11.35 | 19.13 | 20.0% | Very weak |
| Fort Collins, CO | 1.0% | 14.81 | 16.72 | 68.7% | Broad presence, never top-3 |
| Cheyenne, WY | 0.0% | 15.33 | 16.31 | 87.3% | Visible in 87% of grid, never top-3 |
| Denver, CO | 0.0% | 14.89 | 20.68 | 6.5% | Near-absent from grid |
| Boca Raton, FL | 0.0% | 0 | 21 | 0.0% | Absent entirely, every scan |

## Monthly SoLV % (scan days in parens)

| Location | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep* | Aug->Sep |
|---|---|---|---|---|---|---|---|---|---|
| Commerce City, CO | - | - | 92.00 (2) | 89.50 (1) | 89.35 (5) | 89.31 (4) | 90.10 (5) | 91.50 (2) | +1.40 |
| Englewood, CO | 22.00 (1) | 25.75 (2) | 16.00 (1) | 11.25 (1) | 22.20 (5) | 21.31 (4) | 19.10 (5) | 27.13 (2) | +8.03 |
| Colorado Springs, CO | 2.75 (1) | 9.13 (2) | 7.50 (1) | 5.50 (1) | 6.95 (5) | 6.88 (4) | 6.40 (5) | 7.63 (2) | +1.23 |
| Chicago, IL | - | - | 2.25 (2) | 2.00 (1) | 1.90 (5) | 1.88 (4) | 2.20 (5) | 2.13 (2) | -0.07 |
| Fort Collins, CO | 0.00 (1) | 0.63 (2) | 0.50 (1) | 0.50 (1) | 0.60 (5) | 0.75 (4) | 0.75 (5) | 0.75 (2) | 0.00 |
| Cheyenne, WY | - | - | 0.00 (2) | 0.00 (1) | 0.00 (5) | 0.00 (4) | 0.00 (5) | 0.00 (2) | 0.00 |
| Boca Raton, FL | - | - | 0.00 (2) | 0.00 (1) | 0.00 (5) | 0.00 (4) | 0.00 (5) | 0.00 (2) | 0.00 |
| Denver, CO | 0.00 (1) | 0.06 (2) | 0.00 (1) | 0.00 (1) | 0.00 (5) | 0.00 (4) | 0.00 (5) | 0.00 (2) | 0.00 |

\* through 2026-09-14.

## September is a real move, not partial-month noise

Both September scan days sit above the whole August range for all three movers:
Englewood 25.25 then 29.00 (Aug range 18.00-21.00); Commerce City 92.00, 91.00
(Aug 89.25-90.75); Colorado Springs 7.75, 7.50 (Aug 6.00-7.00).

## Limits

- Feb-May monthly figures rest on 1-2 scan days each and are materially less reliable
  than June onward. Do not read Feb->May swings (e.g. Englewood 25.75 -> 11.25) as
  confirmed trend.
- The Englewood `Service Area Business` switch (2026-07-13) does not align with its
  June rise (May 11.25 -> Jun 22.20), so the switch does not explain that move.
- SoLV measures map-pack grid share only. It is not organic ranking and not traffic.

---

# Review corrections applied 2026-09-18

Independent `seo-reviewer` pass raised 1 blocker, 11 material findings, 5 refinements.
Each item below was re-verified against BigQuery by the strategist before adoption;
the reviewer had no database access.

## Confirmed and corrected

1. **September was overstated (reviewer M1) — CONFIRMED, corrected.** The original
   record compared September only to August. Against the full series, Commerce City's
   Sep 91.5 is *below* Apr 92.0 (Apr range 90.0-94.0) and Colorado Springs' Sep 7.6 is
   *below* Mar 9.1 (Mar range 7.5-10.8). Only Englewood is a series high, and narrowly
   (Sep mean 27.1 / range 25.3-29.0 vs Mar mean 25.8 / range 23.3-28.3). All three rose
   on the same two scan days, so a common external cause is as plausible as three
   independent gains. "September is a real move" was withdrawn for Commerce City and
   Colorado Springs and softened for Englewood.

2. **Raw `solv` granularity is 0.01 (reviewer M2) — CONFIRMED by direct query.**
   `SELECT DISTINCT solv` returns 0, 0.01, 0.02, 0.03 ... The reviewer inferred this
   from the monthly lattice without database access; the inference was correct. Consequence:
   any composite below ~1pp is at the measurement floor. Fort Collins (0.00-0.75%) and
   Denver (0.06%) have **no readable top-three trend**, and Chicago's -0.07 Aug->Sep
   "change" is ~1/14th of one raw step. Reporting reduced to 1 decimal; floor disclosed.
   `agr`/`atgr` carry finer precision and are unaffected.

3. **Footprint column is not reproducible from the printed row (reviewer M4) — CONFIRMED
   as a presentation defect, computation upheld.** Footprint is computed per term-scan
   then averaged; `agr`/`atgr` are printed as term-means, and footprint is nonlinear in
   them, so the row-level formula will not reproduce it. Verified on Englewood: per-term
   footprints are 25.1 / 99.9 / 100 / 23.7, mean **62.2%** (the reported figure). The
   reviewer's row-level recomputation of 77.4% is the incorrect method. Footnote added.
   Denver is now stated as "under ~10%" rather than 6.5%, since its denominator (21-agr
   = 6.11) makes it unstable to ±8pp.

4. **Cadence figures in note 5 were global, not per-location (reviewer M5) — CONFIRMED
   as a disclosure defect, no data loss.** August's 6th scan day (2026-08-18) was a
   **Boca Raton-only** scan (verified: 4 terms, one config). No Colorado location was
   scanned that day, so Colorado's August legitimately has 5 scan days and nothing was
   silently dropped. April's apparent 2 days is likewise onboarding, not exclusion:
   Commerce City, Chicago, Boca Raton and Cheyenne began 2026-04-01 while the four
   original locations were next scanned 2026-04-06. Colorado has **21 usable scan days**
   (Feb 1, Mar 2, Apr 1, May 1, Jun 5, Jul 4, Aug 5, Sep 2).

5. **Blocker B1 (cross-location term comparability) — CLEARS for Colorado.** Verified:
   all five Colorado locations track an identical structure of two city-name terms plus
   the same two generic terms (`divorce lawyers`, `family lawyers`). Cross-location
   comparison within Colorado is therefore sound. Not verified for Chicago, Cheyenne or
   Boca Raton, so the original 8-location "Reading" column remains unconfirmed.

6. **Term-class split added (reviewer M7) — highest-value finding.** The 4-term composite
   averages a bimodal distribution. Split by city-name vs generic (September top-three
   share): Commerce City 100/83, Englewood 54/**0**, Colorado Springs **0.3**/15,
   Fort Collins 0.5/1, Denver 0/0. This establishes that Englewood's September gain came
   entirely from city-name searches (38->54) and is not a generic-market breakthrough,
   and it surfaced a previously unseen anomaly: **Colorado Springs ranks ~8 on generic
   terms but ~15 on its own city name** (verified per-term over 16 scans since 2026-06-01:
   `divorce lawyers` agr 7.77 / 18.2% vs `colorado springs divorce lawyers` agr 14.86 /
   0.3%). That inversion is now the most specific actionable item in the dataset.

7. **Fort Collins' excluded terms hide nothing (reviewer M8) — CHECKED, no change needed.**
   The two terms added 2026-06-01 score 2.5% (`divorce attorney`) and 1.0%
   (`fort collins divorce attorney`). All six terms sit between 0% and 2.5%, so the
   like-for-like exclusion does not understate the location. Footprint on the added terms
   is high (64.8% and 86.5%), reinforcing the broad-presence / no-top-three reading.

8. **Dispersion now reported (reviewer M3).** Monthly min-max added. The 2026-03-20
   duplicate pair (0.71 vs 0.66 on one term) implies roughly 5pp single-scan spread per
   term, so small deltas are not distinguishable. Englewood's +8.03 survives; Commerce
   City's +1.40 and Colorado Springs' +1.23 do not.

## Accepted but out of current scope

9. **Boca Raton is a listing-integrity fault, not a ranking result (reviewer M9).**
   `agr = 0` / `atgr = 21` on every scan for five months means zero appearances across
   169 grid points including the office pin. Realistic causes are a suspended, unverified
   or mis-linked GBP, or a wrong `business_place_id`. Out of scope for the Colorado brief;
   flagged for the account. Cheyenne (87% footprint, 0% top-three) is a distinct
   prominence problem, not the same defect.

10. **Market-size framing (reviewer M10).** The Colorado brief states qualitatively that
    Denver is the largest of the five markets. The specific "83% of tracked volume" and
    local-pack display-rate figures from the 2026-08-11 account analysis were **not
    re-verified here** and are deliberately not used. Re-verifying pack display rates is
    a prerequisite before recommending Denver GBP investment.

## Not adopted

11. **Daily series in place of monthly buckets (reviewer M11).** The 21-point daily series
    was computed and used to check every directional claim, and monthly min-max is now
    reported, but Casey asked for month over month and the brief is owner-facing. The
    daily series stays in the working files rather than the deliverable.

12. **Withholding Feb-May (reviewer's question 4).** Retained and relabelled as single-scan
    snapshots rather than months, which is the reviewer's own recommendation over
    withholding.

## Reviewer items still open

- `consistent_terms` is fragile and `terms = 4` is hardcoded rather than derived per
  location (reviewer O1). It produced correct output here, verified against the 21-day
  Colorado series, but a location with 3 or 5 consistent terms would silently vanish.
  Worth fixing before this query is reused.
- Grid radius/spacing is not verified equal across locations (reviewer O2). `grid_size`
  is 13 and `grid_distance_measure` is `miles` everywhere, but no radius column was
  located. Within-location trends are unaffected because `geogrid_config_id` is stable;
  cross-location comparison of absolute levels carries this caveat.
- The exact SoLV formula remains vendor-unconfirmed, and upstream rounding to 1pp means
  it **cannot** be recovered from this table. Vendor support is the only route.

## GBP performance layer (added 2026-09-18, not yet independently reviewed)

Source: `johnsonlaw_localbrandmanager_gbp_performance`, daily, 2026-01-01 to 2026-09-14.
Companion `..._review_management` is a snapshot with **no date column**, so no review
velocity is available.

**Data-quality gate applied first.** Days where all 8 locations report 0 search
impressions: none Jan-Jul, 5 of 31 in August, 6 of 14 in September. Treated as collection
failure, not real zeros. All trend claims restricted to Jan-Jul; Aug-Sep excluded.

**Seasonality confound.** Jan->Jul comparisons are dominated by January, the seasonal peak
for family law enquiries, and the feed begins 2026-01-01 so no prior year exists. Equal
Feb-Apr vs May-Jul windows used instead. Colorado total: impressions 14,306 -> 17,227
(+20%), actions 1,619 -> 1,323 (-18%), action rate 11.32% -> 7.68% (-32%), same direction
at all five locations.
