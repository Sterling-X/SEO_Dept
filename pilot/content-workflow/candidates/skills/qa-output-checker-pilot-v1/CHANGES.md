# qa-output-checker-pilot-v1: changes from baseline

Baseline: `.agents/skills/qa-output-checker` at the hashes recorded in `pilot-manifest.json`
(unchanged import). Candidate created 2026-09-23. This candidate is the mechanical-QA skill
in the pilot.

| # | Defect addressed | Change | Where |
|---|---|---|---|
| 1 | Missing required tools. The baseline DOCX commands call `extract-text` and Pandoc, neither installed here (compatibility doc, 2026-09-17). | Content-workflow runs use `scripts/mechanical_qa.py`, which extracts DOCX text with the standard library and writes a hash-bound record. | `## Pilot workflow contract`, Step 2 |
| 2 | Validators accepting citation mismatches or unresolved placeholders, and the inverse: the baseline grep `\[.*\]` flags every numeric citation marker as a placeholder, so a reviewer either ignores the tool or strips valid citations. | Placeholder grammar defined: numeric `[n]` markers are not placeholders; every other bracketed token, `{{...}}`, `<<...>>`, `TODO`, `TBD`, `FIXME`, `XXX`, `TK`, `lorem ipsum` blocks delivery. Accented names are not placeholders. | `## Pilot workflow contract`, Universal checklist |
| 3 | Mechanical PASS could be read as clearance. | Record labelled as mechanical evidence only; legal hand-off unchanged. | `## Pilot workflow contract` |

| 4 | No rendered-page inspection record existed (patch render gate). | `render_inspect.py` renders with the pinned renderer, hashes every page, and requires a per-page observation bound to the export hash; readiness refuses without it (integrated 2026-09-23). | `## Pilot workflow contract` |
| 5 | Export could carry fields, revisions, or hidden text unnoticed (patch output reconciliation). | Readiness `export-clean` check rejects tracked changes, field codes, comments, hidden text, and embedded content (integrated 2026-09-23). | `scripts/cw_common.py` |

Preserved unchanged: all checklists, error patterns, report format, verdict scale, Step 6
legal hand-off, Rocket Clicks branding rules.

Remaining uncertainty: the bracket-token rule will flag legitimate bracketed prose such as
"[sic]"; none appears in the situational-page contract, and a false positive is reported as
a reason the coordinator can inspect, never silently accepted.
