# family-law-red-team-qa-reviewer-pilot-v1: changes from baseline

Baseline: `.agents/skills/family-law-red-team-qa-reviewer` at the hash recorded in
`pilot-manifest.json` (unchanged import). Candidate created 2026-09-23. This candidate is the
editorial reviewer's skill in the pilot.

| # | Defect addressed | Change | Where |
|---|---|---|---|
| 1 | Ambiguous client-voice selection. Baseline: "There will be one voice skill present ... scan the available skills list for any skill with 'voice' in the name." This repository holds three voice skills, so the rule can select another client's voice. | Voice source resolved by exact domain route from `pilot/content-workflow/canonical/client-routing.json` (mirror of `AGENTS.md`), or the approved voice brief pinned for an unrouted domain. Opening a second client's voice is prohibited. | `## Voice Source (Required)`, workflow step 1b |
| 2 | Conflicting duplicate-URL requirement. Baseline: "any URL appearing more than once is a hard fail", which contradicts the situational skill's required statute pairing (hyperlinked `[n]` body marker plus Sources entry). | Rule narrowed to internal destination URLs; the statute pairing is exempt; points to the single limits table. | Category 3, failure modes list |
| 3 | Inconsistent link and CTA limits across skills. | Brief-compliance question added, referencing `canonical/link-and-cta-limits.md` as the one table. | `## Pilot workflow contract` |
| 4 | Unstructured findings; rechecks could approve on a change log. | Structured JSON findings (`E1`, `E2`, ...); `fixed-verified` only after re-reading the revised passage; hash binding. | `## Pilot workflow contract` |
| 5 | No explicit no-edit / no-delegation rule. | Added. | `## Pilot workflow contract` |

Preserved unchanged: operating-reality assumptions, the eight review categories, severity
scale, output format, the mandatory legal hand-off, universal guardrails.

Remaining uncertainty: whether the exempted statute pairing should also allow a second body
reference to the same statute for very long pages is an open question (baseline says cite
once at first mention; the pilot enforces once).
