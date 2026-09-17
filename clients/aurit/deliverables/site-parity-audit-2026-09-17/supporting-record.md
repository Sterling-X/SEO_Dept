# Aurit Site-Parity Audit Supporting Record

Date: September 17, 2026

Staging: <https://stagingaurit.wpengine.com/>

Live: <https://auritmediation.com/>

## Assignment and decision

The user requested a review of all publicly discoverable pages on both sites, documentation of every change, and a downloadable spreadsheet. The release decision is **FAIL: do not approve staging as a 1:1 copy or approve cutover**.

The first decision for remediation is whether the required target remains strict live parity or becomes an explicitly approved redesign. That choice changes the page/template acceptance standard, but it does not waive the universal failures involving missing article bodies, incomplete city migration, failed lead-form infrastructure, staging-only internal 404s, or the broken image.

## Governing evidence and method

- The final corpus combines every XML sitemap URL, recursively discovered same-origin HTML links, counterpart-path probes from one host to the other, and sequential retries for transient 5xx responses.
- The final crawl is closed on both hosts: every discovered same-host internal target has a saved record, including redirects and final 404s. Both `unrecorded_internal_targets` arrays are empty.
- Rendered checks sampled the homepage at desktop and mobile sizes plus representative standard-page, article, category, guide, city, service-area, team, and consultation templates. Interaction and endpoint checks are preserved in `qa/validation-log.md`.
- Pages absent from both public sitemaps and both public link graphs remain unknowable without a CMS/database export.

The narrower content-agent crawl normalized sitemap/canonical pages and produced a smaller 165-pair comparison. It was retained as corroborating template evidence, not as the governing inventory. The final 170-pair inventory is authoritative because it uses the broader recursive, counterpart-probe, retry, and closed-graph method.

An earlier eight-worker snapshot retained live 504s for `/category/finances-property/` and `/payment-confirmation/`, temporarily classifying them as staging-only. Direct endpoint checks and the final four-worker crawl recovered both as direct 200 pages. The final crawl has no unresolved transient status and treats both paths as mapped pairs.

## Final controls

| Control | Live | Staging | Reconciliation |
|---|---:|---:|---|
| Sitemap URLs | 189 | 171 | Saved sitemap diagnostics |
| Direct-200 HTML pages | 192 | 175 | 170 mapped + 22 live-only; 170 mapped + 5 staging-only |
| Mapped direct-page pairs | 170 | 170 | 161 exact-path + 9 unique-slug mappings |
| Exact pairs | 0 | 0 | Strict source/metadata criteria |
| Near-match pairs | 1 | 1 | `/best-therapists-in-arizona/`; still not 1:1 |
| Changed pairs | 169 | 169 | Mechanical label; manual severity documented separately |
| Internally linked final-404 targets | 9 | 25 | 20 staging-only, 5 shared, 4 live-only |
| Internally linked redirect targets | 79 | 37 | Self-links excluded |
| Orphan-like sitemap pages | 10 | 68 | Self-links excluded; redirect inlinks credited to final destinations |
| Cross-environment anchors | 0 | 269 | 26 staged source pages; regular live-domain anchors depend on cutover rewrite policy |

The 94 staged post pages each expose 269 source-extracted words and no substantive H1. Their live counterparts contain 422–6,352 source-extracted words, with a 1,954.5-word median and a substantive H1.

## Independent SEO review and strategist dispositions

The focused independent recheck found the prior closure blocker resolved and no remaining package blocker. It did not perform a fresh external crawl. The subsequent lower-concurrency confirmation changed only the two transiently unavailable live page records and their dependent inventory counts; it did not change the closed-graph method, release blockers, evidence limits, or FAIL decision. The final package was regenerated and revalidated against the corrected counts.

| Reviewer finding | Disposition | Evidence of resolution |
|---|---|---|
| Saved crawl was not closed after sequentially recovered pages | Accepted; release-package blocker resolved | `close_internal_graph` now runs to a fixed point after retries and counterpart probes; both graphs are closed; `qa/test_crawl_closure.py` covers the recovered-page case, a nested two-level case, and an already-closed unaffected case |
| Some resource/DNS/browser claims lacked saved evidence | Accepted | Unsupported aggregate resource totals were removed; endpoint and rendered evidence were narrowed and preserved in `qa/validation-log.md` |
| Mechanical `Material`/`Minor` labels overstated holistic severity | Accepted | Automated labels are now `Exact`, `Near-match`, and `Changed`; manual materiality remains in the audit narrative and rendered QA |
| Regular staging-to-live anchors may be rewritten at cutover | Accepted | These anchors are now a deployment-policy dependency; failed form hosts and staging-domain staff emails remain direct defects |
| Target-state decision should precede repair | Accepted | It is remediation step 1 and appears prominently in the workbook Summary |
| Developer handoff needed actual values and source pages | Accepted | Added page field values, broken-link source paths, redirect tables, URL gaps, full URL inventory, workbook filters, and the technical appendix |
| Orphan and redirect rules were unclear | Accepted | Technical appendix and workbook define self-link exclusion and redirect-destination crediting |
| Exact reproduction command and closure regression were desirable | Accepted | Command is in the audit and workbook Methodology; regression test is included |
| Empty article shells were correctly blocking, but restoration was not the only approved-redesign remedy | Accepted | Final wording allows approved post retirement/redirect mapping while prohibiting empty 200 shells |

## Downloadable workbook contents

`outputs/aurit-parity-audit-2026-09-17/aurit-full-site-parity-audit.xlsx` contains:

- Formula-linked launch controls and prioritized actions on `Summary`.
- All 170 mapped pairs on `Page Comparison`.
- 1,685 actual changed-field rows on `Field Changes`.
- All 27 unmatched direct pages on `URL Gaps`.
- All 34 environment/target broken-link rows with complete source-path lists.
- All 116 environment/target redirect rows with source counts and source paths.
- All 26 cross-environment source pages and their target URLs.
- All 78 orphan-like environment/page rows.
- Twenty-one rendered, interaction, and endpoint QA records.
- All 557 saved URL/target records on `URL Inventory`.
- Scope, definitions, reviewer dispositions, reproduction details, and exclusions on `Methodology`.

## Verification performed

- `python3 -m py_compile` passed for the crawler.
- `qa/test_crawl_closure.py` passed all three fixed regression cases.
- `qa/validate_package.py` passed the JSON, report, technical-appendix, and XLSX reconciliation checks.
- The regenerated JSON reports both graphs closed and zero unrecorded same-host targets.
- Final audit/report counts were reconciled to the saved JSON and technical appendix.
- The workbook was recalculated before export. Formula scans found zero spreadsheet errors before export and after re-import.
- The saved workbook summary re-imported with the expected values: 170 mapped, 0 exact, 1 near-match, 169 changed, 192 live direct pages, 175 staging direct pages, 22 live-only, 5 staging-only, 25 staged linked 404s, 269 staged cross-environment anchors, and 68 staged orphan-like pages.
- All 11 worksheets were rendered and visually reviewed; the saved XLSX Summary was also rendered through macOS Quick Look.
- `unzip -t` reported no compressed-data errors for the final XLSX.

## Remaining evidence limits

- No lead, checkout, account, newsletter, or consultation form was submitted.
- No CRM, notification-email, consent-storage, analytics-event, or call-routing validation was performed.
- Rendered checks sampled template families; all 170 pairs were not individually pixel-compared.
- No accessibility, performance, security, or legal-accuracy review was performed.
- Phone-number variation may be dynamic call tracking and requires owner/routing confirmation.
