# SEO Skill Compatibility

Status: 2026-09-15 on `seo-agent-foundation`

This document is the local compatibility contract for skills imported from `SEO_Skills_Transfer.json`. Baseline commit `9d8e07f` preserves the unchanged export. Read this document and [SEO Skill Local Adaptations](seo-skill-local-adaptations.md) before relying on an imported skill. File presence or Codex discovery does not mean that a workflow's dependencies, execution, factual accuracy, or performance have been validated.

## Precedence and boundaries

- Current user, runtime, and repository instructions take precedence over imported skill or voice text.
- The transfer is a data export, not an executable installer. Baseline commit `9d8e07f` preserves all 67 payload files byte-for-byte; the working tree now has 14 explicitly logged metadata adaptations, while the other 53 payload files remain identical to the export.
- Imported files do not supply credentials, connectors, account access, packages, live research, document rendering, or background services.
- Repository files and Git history provide local persistence. They are not ChatGPT memory and do not synchronize the source export.
- Changing facts, legal claims, financial claims, office details, products, rates, policies, and live search behavior still require current authoritative sources.
- Repairs must be separate, attributable changes. Do not describe a newly authored replacement as a recovered original, remove a validation requirement, or claim that an unavailable check passed.

## Client voice routing

Use the domain as the explicit routing key. Load the routed voice before writing or auditing client-specific content.

| Domain | Voice skill |
|---|---|
| `sterlinglawyers.com` | `sterling-voice` |
| `jmblattner.com` | `write-blattner-voice` |
| `servicecu.org` | `servicecu-voice` |

Do not infer a client voice from the vertical alone. Reverify changing client facts even when the correct voice skill is loaded. The external Service Credit Union brand guide mentioned by `servicecu-voice` is not included in the transfer.

## Imported skill status

| Skill | Imported files | Source readiness | Local compatibility note |
|---|---:|---|---|
| `seo-marketing-sage` | 17 | Capability verification pending | All 13 references are present. Its inherited README mentions Claude and a `Skill.md` alias; the actual entrypoint is `SKILL.md`. Current claims still need verification. |
| `family-law-service-pages` | 3 | **Source package incomplete; Core route locally repaired** | The original transfer remains incomplete. The Core Practice-Area Hub route now has a documented local template/generator/structural validator, a genuine separately recovered page validator, isolated dependencies, positive and negative tests, and six-page render inspection. The Procedural route remains pending. |
| `family-law-situational-pages` | 3 | **Source package incomplete** | Missing template and validators. User/runtime instructions resolve the source's conflicting hierarchy and missing-voice language; choose voice explicitly. |
| `family-law-service-area-seo` | 3 | **Source package incomplete** | Missing validator. DOCX production, live research, and sometimes map creation require real local capabilities; literal tool names in source prose are not capability proof. |
| `family-law-paid-landing-page-strategist` | 3 | Capability verification pending | No bundled-file gap found. Client claims and geography still require evidence. |
| `family-law-red-team-qa-reviewer` | 3 | Capability verification pending | Route the client voice explicitly. Legal claims require `legal-content-accuracy-qa` plus actual live primary-source research. |
| `legal-content-accuracy-qa` | 5 | Capability verification pending | Both references are present. An offline pass is not a completed legal-accuracy pass. |
| `qa-output-checker` | 5 | Capability verification pending | Both references are present. `extract-text`, Pandoc, `openpyxl`, and `python-pptx` need separately verified local tools or equivalents; report unavailable checks. |
| `recursive-self-improvement` | 4 | Capability verification pending | The learning record is present. Use the local skill-authoring workflow; no memory sync or background service was installed. |
| `ai-first-content-writer` | 9 | Capability verification pending | All referenced scripts and references are present. Node `docx` is not bundled, the named runtime modules path cannot be assumed, and document rendering remains unverified. Run helpers in an isolated task directory because they use and may overwrite working-directory `content.json`. |
| `cluster-blog-writer` | 3 | **Source package incomplete** | Missing validator. `/mnt/skills/public/docx/SKILL.md` is not an assumed-valid path on this Mac. |
| `sterling-voice` | 3 | Capability verification pending | Route only for `sterlinglawyers.com`; reverify changing office, staff, fee, and service facts. |
| `write-blattner-voice` | 3 | Capability verification pending | Route explicitly for `jmblattner.com`; reverify changing firm facts. |
| `servicecu-voice` | 3 | Capability verification pending | Route for `servicecu.org`; reverify rates, eligibility, products, and other changing facts. |

The original import classified ten skills as `local-capability-verification-pending` and four as `source-package-incomplete`. The Core branch repair below changes local branch readiness, not the original transfer's completeness or any other skill's status. These labels do not describe Codex discovery.

## Incomplete source workflows

The transfer declares these exact missing package-scoped dependencies:

### `family-law-service-pages`

- `.agents/skills/family-law-service-pages/references/core-hub-template.md`
- `.agents/skills/family-law-service-pages/references/procedural-template.md`
- `.agents/skills/family-law-service-pages/scripts/office/validate.py`
- `.agents/skills/family-law-service-pages/scripts/validate-page.js`

Current local disposition:

- `references/core-hub-template.md`: original not found; a labeled Core-only local replacement is now present.
- `references/procedural-template.md`: original not found; still absent and pending.
- `scripts/office/validate.py`: original not found; a labeled Core-only local replacement is now present.
- `scripts/validate-page.js`: recovered unchanged from the companion `Skill-files` bundle outside the JSON transfer and verified at SHA-256 `291452d77e3449e605a6817cdfe27392193638506d69f7430b16b6bd44908c49`.

### `family-law-situational-pages`

- `.agents/skills/family-law-situational-pages/references/situational-template.md`
- `.agents/skills/family-law-situational-pages/scripts/office/validate.py`
- `.agents/skills/family-law-situational-pages/scripts/validate-page.js`

### `family-law-service-area-seo`

- `.agents/skills/family-law-service-area-seo/scripts/validate-page.js`

### `cluster-blog-writer`

- `.agents/skills/cluster-blog-writer/scripts/validate-page.js`

The initial exact repository path/name search found no genuine originals. A later authorized search of Downloads, archives, local skill snapshots, and Git histories recovered only the service-page JavaScript validator above. The paired archive also contains a byte-identical copy of the imported service-page `SKILL.md`, establishing companion provenance. Its README has a future-dated heading inconsistent with its file timestamps, so provenance rests on the byte-level pairing and instructions rather than that heading. No genuine Core template, Procedural template, or package-owned structural validator was found. Repeated filenames in other packages remain distinct dependencies.

The service-page **Core Hub branch** may now be used within the verified commands and limits below. Do not extend that result to its Procedural branch or to the other three source-incomplete workflows. Those pending routes may inform analysis but are not validated finished-document workflows.

## Verified local Core Practice-Area Hub route

Verified on 2026-09-15 against the synthetic fixture under `evaluations/runs/2026-09-15-family-law-core-hub-workflow/`.

### Working commands

From the repository root:

```bash
npm ci --prefix .agents/skills/family-law-service-pages

node .agents/skills/family-law-service-pages/scripts/build-core-hub.js \
  path/to/core-input.json path/to/state-practice-core.docx

python3 .agents/skills/family-law-service-pages/scripts/office/validate.py \
  path/to/state-practice-core.docx --manifest path/to/core-input.json

node .agents/skills/family-law-service-pages/scripts/validate-page.js \
  path/to/state-practice-core.docx

.agents/skills/family-law-service-pages/scripts/render-core-hub.sh \
  path/to/state-practice-core.docx --output_dir path/to/new-or-empty-render-directory \
  --dpi 144 --emit_pdf --verbose
```

Run the reusable positive and negative validator checks with:

```bash
python3 .agents/skills/family-law-service-pages/scripts/test-core-hub.py \
  path/to/state-practice-core.docx path/to/core-input.json path/to/evidence
```

The Node dependencies are isolated by the skill's `package.json` and lockfile. Visual tooling is isolated under the ignored `.venv/` and `.tools/` paths; pinned provenance is in `renderer-tools.lock.json`. `setup-renderer-macos.sh` installs the verified macOS LibreOffice build inside the skill, not globally. `render-core-hub.sh` runs pinned Codex documents renderer package `26.819.11345` unchanged after verifying SHA-256 `d8fe979f76e11215e146e53484bb4cb4e5f3906b58debed6844171073b187286`, with a narrow PyMuPDF compatibility adapter because Poppler is unavailable. It fails closed on a changed renderer and rejects nonempty output directories so stale pages cannot survive.

### Verified capabilities

- Schema 2 keeps the exact V2 reference path, page type, role, requiredness, relationship, and gates separate from the verified client URL. The DOCX uses the direct client URL even when its pathname differs from V2. A path difference is not migration evidence. The generator still rejects held, blocked, noncanonical, nonpublishable, directionally invalid, or mismatched V2 records; targets on a validation gate require explicit approval evidence.
- Synthetic mode rejects client and jurisdiction facts, requires the reserved `example.com` client URL, and rejects sources. Production mode requires firm, jurisdiction, voice, link-inventory, publication-state, direct-200/zero-redirect URL evidence, an ISO verification date, and jurisdiction evidence; the generator checks the evidence shape but does not independently prove live truth.
- DOCX output uses US Letter, one-inch margins, Arial 12 pt body and Sources, 18/15/13 pt styled headings, real bullet/number lists, a locally specified header/page footer, and external OOXML hyperlinks.
- The Core structural validator checks ZIP/XML integrity, required parts, comments/revisions, geometry, styles, paragraph-by-paragraph DOCX/manifest parity, immediate opening and required-section order/content, list structure, the exhaustive manifested hyperlink multiset, source placement/size, first-appearance citation order, exact body-marker/source-URL binding, the 1,800–2,600 manifest-content word target, citation-aware paragraph/sentence limits, and placeholders. Well-formed bold `[LOCAL DETAIL: description]` markers warn; malformed or unbold markers and generic placeholders fail.
- The genuine recovered page validator checks duplicate body URLs, explicit link-pattern and anchor scans, em dashes, its named phrase patterns, citation parity, and its original `North Star` convention.
- A 1,832-content-word synthetic Divorce fixture passed both validators. Seven focused positive checks passed, including a divergent V2/client-path mapping and a nine-source claim-free formatting case. Twenty-two meaningful altered cases produced the required failures, including a changed V2 path, wrong client jurisdiction, wrong directional relationship, held/ungated targets, misordered source declarations, swapped citation targets, unmanifested and broken links, bad sequence/content, 11 pt Sources, generic/unbold placeholders, and stale render output.
- The pinned packaged renderer produced all six Letter pages at 144 DPI in the post-review rerun. Every PNG was visually inspected, and the rendered PDF retained all five unique destinations across their wrapped clickable regions. The final PNGs were byte-identical to the preserved pre-review render.
- The Codex skill-creator quick validator accepts the adapted skill.
- The single read-only `seo_reviewer` pass found the gate, parser, manifest, sequence, source-size, placeholder, and renderer issues above; they were addressed and rerun without a second reviewer pass. Its exact findings and dispositions are saved with the fixture evidence.

### Remaining limitations

- Mechanical validation does not determine intent separation, answer quality, cannibalization, contextual link relevance, voice authenticity, trustworthiness, conversion quality, or SEO performance.
- The recovered JavaScript validator contains Johnson Law Group-specific `North Star` logic and phrase patterns broader than the generic skill text. Preserve its results, but adjudicate client-specific or overbroad findings against the applicable voice and evidence.
- A manifest records publication and gate evidence; the generator does not crawl or independently prove those assertions. V2 hierarchy and visual grouping never substitute for the exact directional relationship check.
- The synthetic fixture contains no substantive legal claim, so legal QA was not applicable. Any production legal claim still requires live primary-authority verification through `legal-content-accuracy-qa`; a structural or mechanical PASS is not legal clearance.
- Human inspection is still required for every render. LibreOffice output can differ slightly from Microsoft Word. This machine's PDF substituted Liberation Sans for the requested Arial, although the DOCX OOXML retains Arial; Word-specific font/layout fidelity remains unverified.
- The Procedural template, generator contract, branch-specific tests, and end-to-end validation remain pending. No readiness is claimed for `family-law-situational-pages`, `family-law-service-area-seo`, or `cluster-blog-writer`.

## Actual Codex discovery

With `codex-cli 0.154.0-alpha.6.2` in this repository on 2026-09-15, the unchanged baseline produced metadata warnings because `api` was unsupported in `policy.products`. A later local adaptation deleted only that unsupported list item from all 14 files. After adaptation:

- a structured `skills/list` request with `forceReload: true` returned all 14 imported skills with `scope: repo` and `enabled: true`, zero list errors, and 14 loaded interface objects;
- a fresh model-prompt render included all 14 names and descriptions under the repository skill root;
- all 14 files retain `allow_implicit_invocation: true`; and
- repository `invalid openai.yaml` warnings fell to zero.

The exact metadata changes and before/after hashes are recorded separately in the adaptation log. The other 53 imported files still match their export hashes. Discovery establishes resolver, interface, and model visibility only; it is not proof that scripts run, dependencies exist, outputs are correct, or SEO performance improves.

## Remaining repair order

Keep repair work outside this import:

1. Keep the verified Core Hub layer stable and require the demonstrated commands for any production Core assignment.
2. Recover the genuine `family-law-service-pages` Procedural template if an authorized source becomes available; otherwise define a separately labeled Procedural contract and fixtures without borrowing Core-only requirements.
3. Repair and test the Procedural branch before describing the service-page skill as fully ready.
4. Repair each remaining workflow's template and validator dependencies independently; do not assume repeated filenames imply shared contents.
5. Verify live primary-source research for legal content and any map capability separately from document mechanics.
6. Test `family-law-service-area-seo` only after its distinct validator and V2-conflicting architecture defaults are resolved.
7. Separately adapt and test `cluster-blog-writer` document routing away from the unavailable `/mnt/skills/public/docx/SKILL.md` path.
8. Require positive and negative fixtures plus full rendered-page inspection before changing any remaining readiness label.

The cluster-blog repair can proceed in parallel once the common DOCX layer is verified.
