# legal-content-accuracy-qa-pilot-v1: changes from baseline

Baseline: `.agents/skills/legal-content-accuracy-qa` at the hashes recorded in `pilot-manifest.json`
(unchanged import; the baseline itself was not edited). Candidate created 2026-09-23.

| # | Defect addressed | Change | Where |
|---|---|---|---|
| 1 | Reviews recommended fixes without verifying completion. The baseline Verification Log result vocabulary included `Corrected`, which let a single pass both find and "correct" a claim. | `Corrected` removed from the result vocabulary; replaced by `Correction-needed`. Whether a correction landed is decided only on recheck by re-reading the revised passage and is recorded as the finding's `resolution.status`. | `## Verification Log (mandatory)`, `## Pilot workflow contract` |
| 2 | Later edits invalidated earlier legal review silently. | Review is bound to the draft SHA-256 recorded by `scripts/record_review.py`; any edit invalidates it and requires a recheck. The skill now says so. | `## Pilot workflow contract` |
| 3 | Ambiguous client-voice selection ("load the client's voice skill if present"). | Only the voice source pinned in `run.json`, resolved by exact domain route, may be loaded. Name scanning is prohibited. | `## Inputs` handling rules, `## Pilot workflow contract` |
| 4 | Unstructured findings could not be tracked across rounds. | Structured JSON findings (`L1`, `L2`, ...) with exact passage quotes, evidence, requested correction, and resolution status, plus the Verification Log as `verification_log`. | `## Pilot workflow contract` |
| 5 | No explicit no-delegation rule. | Added. Enforced on Claude by the adapter's tool allowlist; instruction-only on Codex. | `## Pilot workflow contract` |

Preserved unchanged: live-verification mandate, source hierarchy, the nine-step protocol,
absolute-language check, output sections, practice-area checklists, attorney-review caveat.

Remaining uncertainty: the structured JSON adds output length; whether reviewers keep the
prose Verification Log and the JSON consistent has not been measured. No client-specific
rule was generalized.
