# SEO Skill Compatibility

Status: 2026-09-15 on `seo-agent-foundation`

This document is the local compatibility contract for the unchanged skills imported from `SEO_Skills_Transfer.json`. Read it before using or changing an imported skill. File presence or Codex discovery does not mean that a workflow's dependencies, execution, factual accuracy, or performance have been validated.

## Precedence and boundaries

- Current user, runtime, and repository instructions take precedence over imported skill or voice text.
- The transfer is a data export, not an executable installer. The 67 payload files remain byte-for-byte identical to the source export.
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

| Skill | Files | Source readiness | Local compatibility note |
|---|---:|---|---|
| `seo-marketing-sage` | 17 | Capability verification pending | All 13 references are present. Its inherited README mentions Claude and a `Skill.md` alias; the actual entrypoint is `SKILL.md`. Current claims still need verification. |
| `family-law-service-pages` | 3 | **Source package incomplete** | Missing templates and validators prevent a claim of validated final-document delivery. DOCX creation plus visual and structural inspection are separate requirements. |
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

Ten skills are marked `local-capability-verification-pending`; four are marked `source-package-incomplete`. These labels describe workflow readiness, not whether Codex discovered the `SKILL.md` entrypoint.

## Incomplete source workflows

The transfer declares these exact missing package-scoped dependencies:

### `family-law-service-pages`

- `.agents/skills/family-law-service-pages/references/core-hub-template.md`
- `.agents/skills/family-law-service-pages/references/procedural-template.md`
- `.agents/skills/family-law-service-pages/scripts/office/validate.py`
- `.agents/skills/family-law-service-pages/scripts/validate-page.js`

### `family-law-situational-pages`

- `.agents/skills/family-law-situational-pages/references/situational-template.md`
- `.agents/skills/family-law-situational-pages/scripts/office/validate.py`
- `.agents/skills/family-law-situational-pages/scripts/validate-page.js`

### `family-law-service-area-seo`

- `.agents/skills/family-law-service-area-seo/scripts/validate-page.js`

### `cluster-blog-writer`

- `.agents/skills/cluster-blog-writer/scripts/validate-page.js`

An exact repository path/name search found no genuine originals. That does not prove they are absent from every authorized source. Repeated filenames are separate package dependencies and must not be assumed to have identical contents.

These four skills may inform analysis, but they must not be represented as validated finished-document workflows until their dependencies are recovered or replaced transparently and the required checks run successfully.

## Actual Codex discovery

With `codex-cli 0.154.0-alpha.6.2` in this repository on 2026-09-15:

- a structured `skills/list` request with `forceReload: true` returned all 14 imported skills with `scope: repo` and `enabled: true`, and returned zero list errors;
- a fresh model-prompt render included all 14 names and descriptions under the repository skill root; and
- all 14 `agents/openai.yaml` files emitted a warning because this build does not accept `api` in `policy.products`. Their interface metadata was ignored, while each core `SKILL.md` entrypoint was still discovered.

The metadata warning is a preserved source compatibility issue, not a hash failure. Do not edit the imported metadata as part of this unchanged import. Discovery establishes resolver and model visibility only; it is not proof that scripts run, dependencies exist, outputs are correct, or SEO performance improves.

## Proposed repair order

Keep repair work outside this import:

1. Search authorized sources for genuine originals and record provenance.
2. Verify shared capabilities: DOCX generation, extraction, rendering, live primary-source research, and any map workflow.
3. Recover the three missing templates, or newly author and clearly label replacements.
4. Repair each missing `scripts/office/validate.py` independently.
5. Repair each package's `scripts/validate-page.js` independently; do not assume repeated filenames imply shared contents.
6. Test `family-law-service-pages` before `family-law-service-area-seo`, which inherits service-page document formatting.
7. Separately adapt and test `cluster-blog-writer` document routing away from the unavailable `/mnt/skills/public/docx/SKILL.md` path.
8. Use positive and negative fixtures plus rendered DOCX inspection before changing readiness labels.
9. Address `agents/openai.yaml` product-policy compatibility as a separate, source-diverging change only if the current Codex build still requires it.

The cluster-blog repair can proceed in parallel once the common DOCX layer is verified.
