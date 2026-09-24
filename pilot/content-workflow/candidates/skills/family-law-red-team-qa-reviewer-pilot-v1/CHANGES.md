# family-law-red-team-qa-reviewer-pilot-v1: changes from baseline

Baseline: `.agents/skills/family-law-red-team-qa-reviewer` at the hash recorded in
`pilot-manifest.json` (unchanged import). Candidate created 2026-09-23. This candidate is the
editorial reviewer's skill in the pilot.

| # | Defect addressed | Change | Where |
|---|---|---|---|
| 1 | Ambiguous client-voice selection. Baseline: "There will be one voice skill present ... scan the available skills list for any skill with 'voice' in the name." This repository holds three voice skills, so the rule can select another client's voice. | Voice source resolved by exact domain route from `pilot/content-workflow/canonical/client-routing.json` (mirror of `AGENTS.md`), or the approved voice brief pinned for an unrouted domain. Opening a second client's voice is prohibited. | `## Voice Source (Required)`, workflow step 1b |
| 2 | Conflicting duplicate-URL requirement. Baseline: "any URL appearing more than once is a hard fail", which contradicts the situational skill's statutory citations (hyperlinked `[n]` markers plus a Sources entry). | Rule narrowed to internal destination URLs; statutory citations, including repeated same-number citations (integrated 2026-09-23), are exempt; points to the single limits table. | Category 3, failure modes list |
| 3 | Inconsistent link and CTA limits across skills. | Brief-compliance question added, referencing `canonical/link-and-cta-limits.md` as the one table. | `## Pilot workflow contract` |
| 4 | Unstructured findings; rechecks could approve on a change log. | Structured JSON findings (`E1`, `E2`, ...); `fixed-verified` only after re-reading the revised passage; hash binding. | `## Pilot workflow contract` |
| 5 | No explicit no-edit / no-delegation rule. | Added. | `## Pilot workflow contract` |

| 6 | Client specificity reduced to arbitrary uniqueness (patch F10). | `references/editorial-rubric-pilot.md` (adapted from the comparison release): observable criteria, neutral accurate law acceptable, decision examples; the skill text points to it (integrated 2026-09-23). | new reference, `## Pilot workflow contract` |
| 7 | Closure by suggestion or coordinator note (patch F02/C06). | Categories and `corrected_text`; protected client-fact and promise findings cannot be coordinator-accepted (integrated 2026-09-23). | `## Pilot workflow contract` |

Preserved unchanged: operating-reality assumptions, the eight review categories, severity
scale, output format, the mandatory legal hand-off, universal guardrails.

Resolved 2026-09-23: repeated citations of the same authority with one number are allowed
wherever it supports a later material claim (integrated from the comparison patch).
