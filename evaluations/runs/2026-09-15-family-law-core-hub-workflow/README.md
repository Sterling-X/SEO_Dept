# Family-Law Core Hub Workflow Verification

Date: 2026-09-15
Scope: Core Practice-Area Hub branch of `family-law-service-pages` only

## Artifacts

- `synthetic-divorce-core-input.json`: V2-backed structured input and explicit link manifest.
- `synthetic-divorce-core.docx`: claim-free synthetic fixture; not client content and not for publication.
- `validation/positive-structural.txt`: local Core structural validator PASS.
- `validation/positive-page-level.txt`: genuine recovered page validator PASS.
- `validation/negative-test-summary.md`: six focused positive checks and 17 expected-failure regressions.
- `render/page-1.png` through `render/page-6.png`: preserved pre-review rendered page set.
- `render-post-review/page-1.png` through `render-post-review/page-6.png`: final full rendered page set after reviewer corrections.
- `render-post-review/synthetic-divorce-core.pdf`: final visual-review intermediate, not the deliverable.
- `visual-review.md`: page-by-page human inspection.
- `mechanical-qa.md`: Universal and DOCX checklist record.
- `seo-reviewer-findings.md`: independent read-only reviewer pass and resolution, added after review.

## Reproduction

From the repository root:

```bash
npm ci --prefix .agents/skills/family-law-service-pages
node .agents/skills/family-law-service-pages/scripts/build-core-hub.js \
  evaluations/runs/2026-09-15-family-law-core-hub-workflow/synthetic-divorce-core-input.json \
  evaluations/runs/2026-09-15-family-law-core-hub-workflow/synthetic-divorce-core.docx

python3 .agents/skills/family-law-service-pages/scripts/test-core-hub.py \
  evaluations/runs/2026-09-15-family-law-core-hub-workflow/synthetic-divorce-core.docx \
  evaluations/runs/2026-09-15-family-law-core-hub-workflow/synthetic-divorce-core-input.json \
  evaluations/runs/2026-09-15-family-law-core-hub-workflow/validation

core_render_dir=$(mktemp -d /private/tmp/core-hub-render.XXXXXX)
.agents/skills/family-law-service-pages/scripts/render-core-hub.sh \
  evaluations/runs/2026-09-15-family-law-core-hub-workflow/synthetic-divorce-core.docx \
  --output_dir "$core_render_dir" \
  --dpi 144 --emit_pdf --verbose
```

## Verified result

- Generator: accepted exact V2 Core Hub `FL-PA-DIV` and five exact directional `Canonical parent → child` relationships; produced a six-page DOCX.
- Structure: PASS at 1,832 manifest-content words, 14 headings, 10 true list items, and five functional hyperlinks.
- Page-level scan: PASS with five unique body destinations, zero em dashes, zero citations, and no warnings.
- Regression tests: PASS; six focused positive checks passed and all 17 altered cases produced their required failures. The cases cover V2 target gates, citation parsing, exhaustive links, required sequence/content, source sizing, placeholder behavior, local header/footer, and stale render output in addition to the original checks.
- Render: the pinned renderer produced six Letter pages at 144 DPI in a fresh post-review directory. All were inspected at original resolution with no visual blocker, and all six PNG hashes match the preserved pre-review render.
- Reviewer: one read-only `seo_reviewer` pass found two blockers, five material hardening issues, and three optional refinements. All findings were resolved or explicitly adjudicated in `seo-reviewer-findings.md`; the reviewer was not rerun.

The fixture proves only the exercised mechanics. It does not prove production content quality, legal accuracy, live publication, client fit, SEO performance, or the still-pending Procedural branch.
