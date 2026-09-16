# Core Practice-Area Hub Template

> **LOCAL REPLACEMENT, NOT AN ORIGINAL EXPORT FILE.** The source package referenced `references/core-hub-template.md` but did not include it. This replacement is derived from the unchanged `SKILL.md` and the governing `context/architecture/Family_Law_StructureV2.html`; `context/architecture/family-law-architecture-v2.md` is the readable guide. Existing client deliverables were inspected only as corroborating examples and were not copied.

## Scope and limits

This template repairs only the **Core Practice-Area Hub** route. The Procedural route remains unavailable until its distinct template and workflow are recovered or transparently replaced and tested.

The generator and validators establish document mechanics. They do not establish useful strategy, editorial quality, brand authenticity, SEO performance, or legal accuracy. Any production page containing a substantive legal claim still requires live primary-authority research and `legal-content-accuracy-qa` after editorial and mechanical review.

## Required input contract

Use `scripts/build-core-hub.js` with a JSON input file. A production input must provide:

- `workflow: "core-hub"` and `schema_version: 2`.
- One exact V2 Core Practice-Area Hub node ID, `v2_reference_path`, role, and requiredness copied from V2.
- Evidence that any Conditional hub has cleared its V2 service/jurisdiction gate.
- Jurisdiction, verified firm name, a direct client URL with dated status/redirect evidence, and an explicit voice source.
- A reviewed publication/link inventory. This is an evidence assertion, not a live URL check.
- An explicit link manifest. Every enabled link must keep its V2 node ID, `v2_reference_path`, page type, role, and requiredness separate from its verified `client_url`. It must match a directional V2 relationship, state why it belongs, and record publication, direct-200, zero-redirect, verification-date, and jurisdiction evidence. A target on a validation gate also needs `target_gate_approval: "approved"` and `target_gate_evidence`; held or blocked targets cannot be enabled.
- One H1, two opening paragraphs, broad-intent H2 sections, a firm-help/contact section, a Hub FAQ with H3 questions, and a contact CTA.
- Sources only when the body makes claims that need authority. Declare them in first-appearance order; body markers must begin at `[1]`, continue without gaps, and stay bound to the matching Sources row and URL. The generator appends Sources last and requires one body marker per source. Five to eight is an editorial target, not a hard cap; do not remove useful supported information merely to hit the target.

For a clearly labeled synthetic fixture, omit firm and jurisdiction facts, use the reserved `example.com` origin, set `synthetic_fixture: true`, and provide no substantive legal claims or citations. A synthetic fixture can prove only the mechanics exercised by the fixture.

## Architecture gate

The accepted Core Hub set is the 11 V2 nodes whose page type is `Core Practice-Area Hub`, not the seven-item list in the original skill intake section. The generator reads the governing HTML and checks the selected node ID, page type, V2 reference path, role, requiredness, node class, publishability, governance gate, and every manifested relationship.

A V2 reference path identifies the architecture node. A client URL identifies the verified live implementation and may differ. The generator keeps those fields separate, uses the direct client URL in the DOCX, and does not require Sterling or another client to change site routing to resemble V2. A difference alone does not justify a migration, consolidation, canonical, or redirect recommendation.

- Required foundation hubs may proceed when their current V2 gate is `PASS — CANONICAL`.
- Optional hubs are not automatically approved for a client production queue.
- Conditional hubs require documented service/jurisdiction approval.
- A hold, non-publishable target, null URL, or direction mismatch is a hard stop.

Hierarchy, source-derived links, visual grouping, and build dependencies are different data. Do not turn proximity, a cluster boundary, a parent field, or build order into a link. A canonical parent-child relationship permits a contextual link only when the supplied inventory and the page copy justify it. Do not infer reciprocal or sibling links.

## Section sequence

1. **H1:** the broad service intent for the selected Core Hub.
2. **Opening paragraph 1:** answer the central search need immediately.
3. **Opening paragraph 2:** explain the stakes and orient the reader without firm promotion.
4. **Broad-intent H2 sections:** cover the hub-level questions a reader needs to evaluate the service. Keep child-process detail concise enough to preserve intent separation.
5. **Contextual child placements:** use one enabled manifest link at its strongest relevant placement, one destination once. Do not dump links into a generic resource list.
6. **How the firm can help:** use verified differentiators only. No guarantees or invented facts.
7. **Hub FAQ:** an H2 FAQ heading followed by H3 questions and direct answers.
8. **CTA:** a clear schedule/contact action using verified contact details or site routing.
9. **Sources, conditional:** appended by the generator as the final H2 only when citations exist.

The V2 Hub Service Page Brief sets a target of 1,800–2,600 words, a Hub FAQ, and a schedule/contact CTA. The replacement validator measures the word target but does not decide whether the page deserves that length.

## Content and link representation

Each content block uses one of `h1`, `h2`, `h3`, `p`, `ul`, or `ol`. Mark the firm-help H2 with `role: "firm-help"`, the FAQ H2 with `role: "faq"`, and the CTA H2 with `role: "cta"`. Paragraph and list-item content is an array of runs:

```json
{
  "type": "p",
  "runs": [
    { "text": "A focused " },
    { "text": "collaborative divorce pathway", "link_id": "collaborative" },
    { "text": " can keep process detail out of the broad hub." }
  ]
}
```

Use `link_id` only for links defined in `link_manifest`. Use `citation_id` only for sources defined in `sources`. Do not put a link and citation on the same run. The generator creates real OOXML hyperlinks and true numbered or bulleted lists.

A permitted local-detail marker must use the complete form `[LOCAL DETAIL: description]` within one bold run. It produces a validator warning and must be resolved editorially before publication. A malformed or unbold marker fails validation; `TODO`, `TBD`, and the other generic placeholders remain hard failures.

## Document format

- US Letter: 12,240 × 15,840 DXA.
- One-inch margins.
- Arial: body 12 pt, H1 18 pt, H2 15 pt, H3 13 pt.
- Body spacing: 120 DXA before and after.
- H2 spacing: at least 360 DXA before; H3: at least 280 DXA before.
- H1 → H2 → H3 hierarchy with no skipped level.
- Filename: `[state]-[practice-area]-core.docx`; `synthetic-[practice-area]-core.docx` is reserved for fixtures.
- **Local Core-only contract addition, not recovered from the imported package:** generated Core documents require one simple header and one page-number footer. Field behavior remains render-verified.

## Working commands

Run from the repository root:

```bash
npm ci --prefix .agents/skills/family-law-service-pages
node .agents/skills/family-law-service-pages/scripts/build-core-hub.js input.json output.docx
python3 .agents/skills/family-law-service-pages/scripts/office/validate.py output.docx --manifest input.json
node .agents/skills/family-law-service-pages/scripts/validate-page.js output.docx
```

For the isolated renderer, install the pinned Python requirement and the verified LibreOffice application recorded in `renderer-tools.lock.json`. Then run Codex's packaged renderer through the local wrapper:

```bash
python3 -m venv .agents/skills/family-law-service-pages/.venv
.agents/skills/family-law-service-pages/.venv/bin/pip install -r .agents/skills/family-law-service-pages/requirements-render.txt
.agents/skills/family-law-service-pages/scripts/setup-renderer-macos.sh
core_render_dir=$(mktemp -d /private/tmp/core-hub-render.XXXXXX)
.agents/skills/family-law-service-pages/scripts/render-core-hub.sh output.docx --output_dir "$core_render_dir" --dpi 144 --emit_pdf --verbose
```

The wrapper runs the exact Codex documents renderer release and SHA-256 recorded in `renderer-tools.lock.json`; it fails closed if that file is absent or changed. It also requires an explicit output directory that is absent or empty so stale page images cannot survive a rerun. LibreOffice supplies DOCX-to-PDF conversion, while a narrow, documented PyMuPDF adapter supplies the two `pdf2image` calls because Poppler is absent. This produces one PNG per page, but LibreOffice pagination may differ slightly from Microsoft Word.
