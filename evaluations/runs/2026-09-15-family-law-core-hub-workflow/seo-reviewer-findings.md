# SEO Reviewer Findings and Disposition

Date: 2026-09-15
Scope: one independent pass over the Core Practice-Area Hub repair and its initial evidence

## Coordination record

The existing `seo_reviewer` was invoked exactly once after the initial generator, validators, fixture, and render existed. It received the user request, governing files, implementation inventory, and evidence inventory. The reviewer stayed read-only and made no file changes. Its saved response did not expose a model identifier, so none is claimed here. This pass assessed implementation fidelity and evidence; it was not a legal review, SEO competence test, or performance evaluation.

The reviewer confirmed the recovery/replacement provenance, Core-only boundary, pending Procedural status, synthetic claim-free fixture, initial validator passes, six clean rendered pages, and structurally functional DOCX/PDF hyperlinks. It did not clear the initial implementation because it found the issues below.

## Findings and strategist disposition

| Severity | Reviewer finding | Disposition and post-review evidence |
|---|---|---|
| Blocker | A V2-held linked child such as `FL-M013` could pass generation. | **Accepted and fixed.** Targets must now be publishable canonical nodes; held/blocked targets fail, and targets on validation gates require explicit approval evidence. A held-target and an ungated-conditional test fail; an approved conditional-target test passes. |
| Blocker | `Fla. Stat. sec. 61.30` was split into several sentences. | **Accepted and fixed.** Sentence parsing protects common legal abbreviations, initialisms, and section-number decimals. The exact citation-format example parses as two sentences; a four-sentence paragraph still fails. This is parsing evidence, not validation of the example's legal proposition. |
| Material | An additional functional hyperlink could bypass the manifest. | **Accepted and fixed.** The structural validator compares the complete hyperlink multiset with manifested internal links plus the two expected placements for each source. A unique unmanifested URL now fails. |
| Material | Actual H1/opening and required-section order/content were not fully validated. | **Accepted and fixed.** The validator now checks immediate opening paragraphs, actual `firm-help` → `faq` → `cta` order, populated required sections and FAQ answers, and paragraph-by-paragraph DOCX/manifest text and structure parity. Interrupted, reordered, and empty-CTA cases fail. |
| Material | Generated Sources entries used 11 pt instead of the 12 pt contract. | **Accepted and fixed.** Source label and URL runs now use 12 pt. An ephemeral claim-free sourced document passes; a mutated 11 pt Sources entry fails. No second fixture was retained. |
| Material | `[LOCAL DETAIL]` was permitted by the skill but hard-failed by the validator. | **Accepted and fixed.** A complete `[LOCAL DETAIL: description]` in one bold run produces a warning and remains an editorial publication blocker. Malformed/unbold markers and generic placeholders fail. |
| Material | The wrapper selected the newest cached renderer, so the same command could change behavior. | **Accepted and fixed.** The wrapper now selects package `26.819.11345`, verifies renderer SHA-256 `d8fe979f76e11215e146e53484bb4cb4e5f3906b58debed6844171073b187286`, and fails closed. The lock records the same values. |
| Optional | Header/footer absence was an unstated local hard failure. | **Accepted as a provenance correction.** The simple header and page-number footer are now explicitly labeled as a local Core-only contract addition, not a recovered export requirement. Missing-header and missing-footer cases demonstrate the stated check. |
| Optional | A render directory could retain stale higher-numbered PNGs. | **Accepted and fixed.** The wrapper requires an explicit output directory that is absent or empty. A stale-directory case fails before rendering; the post-review render began in an absent directory and produced exactly six PNGs for six PDF pages. |
| Optional | This reviewer record was named in the run README but did not yet exist. | **Accepted and fixed** by this file. |

## Post-review strategist verification

- Regenerated the same single persistent synthetic DOCX fixture from its manifest.
- Passed both primary validators.
- Passed six focused positive checks and observed all 17 required negative failures.
- Reran the pinned renderer into `render-post-review/` and inspected every page at original resolution.
- Confirmed six 612 × 792 point PDF pages, six 1,224 × 1,584 PNGs, five unique hyperlink destinations, and ten wrapped PDF annotation rectangles.
- Confirmed every final PNG is byte-identical to its preserved pre-review counterpart.

No second reviewer pass was requested. The reviewer itself did not rerun generation, installation, negative tests, rendering, legal QA, structured skill discovery, or the earlier dependency search because it was read-only. The strategist performed the relevant post-review mechanical and visual reruns. Synthetic URLs were not tested as live pages, Microsoft Word rendering remains unverified, and no legal QA was applicable because the retained fixture contains no substantive legal claim.
