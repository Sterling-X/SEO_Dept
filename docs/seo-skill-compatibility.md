# SEO Skill Compatibility

Status: 2026-09-17 on `seo-agent-foundation`; research-first precedence bullet added 2026-09-24 on `content-workflow-pilot`

This document is the local compatibility contract for skills imported from `SEO_Skills_Transfer.json`. Baseline commit `9d8e07f` preserves the unchanged export. Read this document and [SEO Skill Local Adaptations](seo-skill-local-adaptations.md) before relying on an imported skill. File presence or Codex discovery does not mean that a workflow's dependencies, execution, factual accuracy, or performance have been validated.

## Precedence and boundaries

- Current user, runtime, and repository instructions take precedence over imported skill or voice text.
- The transfer is a data export, not an executable installer. Baseline commit `9d8e07f` preserves all 67 payload files byte-for-byte. Subsequent metadata and bounded workflow changes are recorded in [SEO Skill Local Adaptations](seo-skill-local-adaptations.md); use that log rather than assuming current byte identity.
- Imported files do not supply credentials, connectors, account access, packages, live research, document rendering, or background services.
- Repository files and Git history remain the authoritative local implementation. Project-local MemPalace provides scoped reference continuity only; it is not ChatGPT memory and does not synchronize or supersede the source export.
- Changing facts, legal claims, financial claims, office details, products, rates, policies, and live search behavior still require current authoritative sources.
- Current-source research is mandatory before any imported skill's drafting, audit, or verification workflow relies on a legal or changeable factual claim (`AGENTS.md`, "Current-source research", added 2026-09-24). The placeholder-first instructions in the imported skill text (`[LOCAL DETAIL: ...]`, `[VERIFY: ...]`, "leave a placeholder rather than guessing", "use a clearly labeled placeholder") are superseded on conflict: research first; a placeholder marks only a fact confirmed unobtainable now, and the work stays incomplete until it is researched or removed. The imported skill files are preserved unchanged as the fallback text; the pilot candidates under `pilot/content-workflow/candidates/skills/` carry the research-first wording and the enforcing tooling.
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
| `family-law-situational-pages` | 3 | **Source package incomplete; FL-M008 route locally repaired** | The missing originals remain unavailable. A labeled local template, generator, validators, tests, and render wrapper are demonstrated only for `FL-M008` High-Conflict Divorce. Other Situational routes remain pending; choose client voice explicitly. |
| `family-law-service-area-seo` | 3 | **Source package incomplete** | Missing validator. DOCX production, live research, and sometimes map creation require real local capabilities; literal tool names in source prose are not capability proof. |
| `family-law-paid-landing-page-strategist` | 3 | Capability verification pending | No bundled-file gap found. Client claims and geography still require evidence. |
| `family-law-red-team-qa-reviewer` | 3 | Capability verification pending | Route the client voice explicitly. Legal claims require `legal-content-accuracy-qa` plus actual live primary-source research. |
| `legal-content-accuracy-qa` | 5 | Capability verification pending | Both references are present. An offline pass is not a completed legal-accuracy pass. |
| `qa-output-checker` | 5 | Capability verification pending | Both references are present. `extract-text`, Pandoc, `openpyxl`, and `python-pptx` need separately verified local tools or equivalents; report unavailable checks. |
| `recursive-self-improvement` | 4 | Capability verification pending | The coordinator-owned shared-learning instructions, bounded candidate router, v3 instructions-only MemPalace reminder, and structured reviewer contribution have been checked. The router has eight focused tests and the reminder has six; direct child/reviewer recall, automatic deduplicated creation, fresh-session recall, and representative mutation gates have bounded lifecycle evidence. No `Stop` hook, remote sync, transcript capture, or background service is installed. |
| `ai-first-content-writer` | 9 | Capability verification pending | All referenced scripts and references are present. Node `docx` is not bundled, the named runtime modules path cannot be assumed, and document rendering remains unverified. Run helpers in an isolated task directory because they use and may overwrite working-directory `content.json`. |
| `cluster-blog-writer` | 3 | **Source package incomplete** | Missing validator. `/mnt/skills/public/docx/SKILL.md` is not an assumed-valid path on this Mac. |
| `sterling-voice` | 3 | Capability verification pending | Route only for `sterlinglawyers.com`; reverify changing office, staff, fee, and service facts. |
| `write-blattner-voice` | 3 | Capability verification pending | Route explicitly for `jmblattner.com`; reverify changing firm facts. |
| `servicecu-voice` | 3 | Capability verification pending | Route for `servicecu.org`; reverify rates, eligibility, products, and other changing facts. |

The original import classified ten skills as `local-capability-verification-pending` and four as `source-package-incomplete`. The Core branch and bounded `FL-M008` repairs below change only their documented local route readiness, not the original transfer's completeness or any other skill's status. These labels do not describe Codex discovery.

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

Current local disposition:

- No genuine original was recovered for any of the three named dependencies.
- Each named path now contains a **LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL** scoped to the demonstrated `FL-M008` High-Conflict Divorce route.
- `scripts/build-situational.js`, `scripts/render-situational.sh`, `scripts/test-situational.py`, isolated Node dependencies, and `LOCAL-REPLACEMENT.md` supply the bounded executable contract and provenance.
- These additions do not establish readiness for another Situational node and do not use the Core Hub content template.

### `family-law-service-area-seo`

- `.agents/skills/family-law-service-area-seo/scripts/validate-page.js`

### `cluster-blog-writer`

- `.agents/skills/cluster-blog-writer/scripts/validate-page.js`

The initial exact repository path/name search found no genuine originals. A later authorized search of Downloads, archives, local skill snapshots, and Git histories recovered only the service-page JavaScript validator above. The paired archive also contains a byte-identical copy of the imported service-page `SKILL.md`, establishing companion provenance. Its README has a future-dated heading inconsistent with its file timestamps, so provenance rests on the byte-level pairing and instructions rather than that heading. No genuine Core template, Procedural template, or package-owned structural validator was found. Repeated filenames in other packages remain distinct dependencies.

The service-page **Core Hub branch** and the separate `FL-M008` Situational route may now be used only within their respective verified commands and limits below. Do not extend the Core result to its Procedural branch or the `FL-M008` result to other Situational nodes. Other pending routes may inform analysis but are not validated finished-document workflows.

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
- The Procedural template, generator contract, branch-specific tests, and end-to-end validation remain pending. Situational readiness is limited to the separately documented `FL-M008` route; no readiness is claimed for any other Situational node, `family-law-service-area-seo`, or `cluster-blog-writer`.

## Verified local `FL-M008` Situational route

Verified on 2026-09-16 through the Fanash High-Conflict Divorce replacement assignment. The source package remains incomplete; this is a labeled, bounded local replacement.

### Working commands

From the repository root:

```bash
npm ci --prefix .agents/skills/family-law-situational-pages

node .agents/skills/family-law-situational-pages/scripts/build-situational.js \
  path/to/workflow-input.json path/to/florida-high-conflict-divorce-situational.docx

python3 .agents/skills/family-law-situational-pages/scripts/office/validate.py \
  path/to/florida-high-conflict-divorce-situational.docx --manifest path/to/workflow-input.json

node .agents/skills/family-law-situational-pages/scripts/validate-page.js \
  path/to/florida-high-conflict-divorce-situational.docx --manifest path/to/workflow-input.json

.agents/skills/family-law-situational-pages/scripts/render-situational.sh \
  path/to/florida-high-conflict-divorce-situational.docx --output_dir path/to/new-or-empty-render-directory \
  --dpi 144 --emit_pdf --verbose

python3 .agents/skills/family-law-situational-pages/scripts/test-situational.py
```

### Verified capabilities and limits

- The generator reads the governing V2 HTML at runtime and requires the exact `FL-M008` page type, role, reference path, brief type, and word target while keeping the retained client URL separate.
- The Situational contract requires two answer-first opening paragraphs, scenario ownership, selective legal/stakes context, practical strategy, verified firm-help language, a final CTA, optional scenario FAQ, Sources last, and 1,100–1,700 consumer-copy words. It rejects general-Divorce-Hub and Contested-procedure intent substitution.
- Schema version 2 separates four link authorities. V2 remains authoritative for classification, hierarchy, and `v2-explicit-relationship` links, which still require exact outgoing `FL-M008` edges. Separately, this bounded route requires one `skill-parent-navigation` link to the actual V2 parent, one `skill-process-bridge` link to `FL-M004`, and one final `consultation-cta`; none may be mislabeled as an outgoing V2 edge. Every destination still requires dated, direct-200, zero-redirect, right-service evidence, and held V2 targets fail.
- DOCX output and validation cover Letter geometry, one-inch margins, Arial 12 pt body and Sources, styled 18/15/13 pt headings, real lists, metadata, comments/revisions, link and citation binding, placeholders, paragraph limits, and the Situational sequence.
- Twenty-one focused regression cases pass. They cover the three required non-edge authorities, an additional exact `FL-M010` edge, false V2 labels for the Hub and Contested links, missing or wrong authority, wrong V2 targets, invented edge fields, CTA field and placement failures, an empty manifest, Hold status, unverified and duplicate destinations, contamination, missing styles, duplicate rendered links, and 9 pt Sources.
- Rendering delegates only generic DOCX rendering to the pinned Core renderer wrapper. The Situational template, content structure, manifest, and link contract remain separate and are explicitly labeled.
- Mechanical PASS does not establish legal accuracy, client truth, voice quality, service acceptance, intent quality, destination quality, visual quality, or performance. Each production draft still requires current primary authority, client evidence, independent review, mechanical QA, fresh render inspection, and human approval.
- No readiness is claimed for another Situational node. Adapting one requires its own V2 contract, tested branch behavior, and evidence.

The read-only `seo_reviewer` identified a missing mediation qualification, a definition-first opening, 9 pt Sources, stale compatibility records, and incomplete destination-screen reproduction. The production draft, Source style and validator, negative regression, and records were corrected; exact reconciliation remains with the Fanash deliverable. The reviewer’s optional broader `Draft`-field hardening was deferred because the current fields are clean and this repair is limited to components necessary for `FL-M008`.

## Actual Codex discovery

With `codex-cli 0.154.0-alpha.6.2` in this repository on 2026-09-15, the unchanged baseline produced metadata warnings because `api` was unsupported in `policy.products`. A later local adaptation deleted only that unsupported list item from all 14 files. After adaptation:

- a structured `skills/list` request with `forceReload: true` returned all 14 imported skills with `scope: repo` and `enabled: true`, zero list errors, and 14 loaded interface objects;
- a fresh model-prompt render included all 14 names and descriptions under the repository skill root;
- all 14 files retain `allow_implicit_invocation: true`; and
- repository `invalid openai.yaml` warnings fell to zero.

The product-policy metadata changes and their then-current hashes are recorded separately in the adaptation log. Later Core and bounded Situational repairs create additional documented divergences from the preserved export. Discovery establishes resolver, interface, and model visibility only; it is not proof that scripts run, dependencies exist, outputs are correct, or SEO performance improves.

The installed `codex-cli 0.154.0-alpha.6.2` also reports the `hooks` feature as stable and enabled. The project defines two `UserPromptSubmit` commands in `.codex/hooks.json`: the unchanged read-only candidate router and the instructions-only `mempalace-recall-retention-reminder-v3.py`. Codex supports command hooks that add context, but it currently parses and skips `agent` hook handlers, so neither hook can invoke `seo_reviewer`. Both current command definitions were separately reviewed and trusted on 2026-09-17. The v3 reminder script and its `.codex/hooks.json` entry were edited on 2026-09-17 after that trust decision, so Codex re-trust is pending and the injected context is unverified on that host since the edit. The router's eight focused tests and the v3 reminder's six policy tests pass. No `Stop` hook was added; recall, consolidation, and a single retention decision remain model actions governed by `AGENTS.md`, not code executed by the reminder.

The ignored project-local MCP configuration points participating agents to the same `seo_dept` palace. Actual no-approval `mempalace_search` calls were exercised by a child agent and the custom read-only reviewer; when that access is unavailable or irrelevant, the coordinator must supply a source-linked, assignment-scoped handoff. Recall is room-filtered: client work may query only shared, relevant role, and exact-current-client rooms, plus the matching `open-questions` or exact `client-<client-slug>-open-questions` room when the task turns on an unresolved decision, while non-client work excludes client rooms. For automatic curated retention, the only approved tool pair is exact `mempalace_check_duplicate` followed by exact `mempalace_add_drawer`. Inspection of MemPalace 3.10.0 found that `mempalace_add_drawer` accepts new-drawer fields and produces a content-addressed idempotent ID; it exposes no update, delete, overwrite, mine, import, sync, or share operation. The server default remains `writes`, so all unlisted mutation tools stay approval-gated, with autosave and daemon flags false and hub forwarding off. There is no blanket server approval.

Fresh session `01a0b08c-12bc-73a2-a63e-6d2ed31955e9` performed an ordinary documentation task without a memory-save request under approval policy `never`. It searched the palace, made the scoped source change, called `mempalace_check_duplicate` at `0.9`, and created drawer `drawer_seo_dept_operating-rules_b2b6f07d08b2105c0fd38804` without an approval interruption. After v3 trust, fresh session `01a0b098-2734-7e92-934b-76ac0115e54c` handled a relevant non-client runbook prompt that did not mention a skill or request recall: it listed room names, searched exact room `operating-rules` with limit three, and retrieved the saved drawer without a wing-wide or client-room search. Exact-content duplicate checking returned similarity `1.0`, no second drawer was added, and the wing count remained three at that checkpoint. Under approval policy `never`, `mempalace_checkpoint`, `mempalace_delete_by_source`, `mempalace_update_drawer`, `mempalace_mine`, and `mempalace_sync` were each blocked before dispatch; hub forwarding remains `off`, and artifacts, events, sharing, and all other unlisted tools retain the default gate. These checks establish bounded technical paths, not universal retrieval relevance, valid lesson promotion, professional quality, or SEO performance.

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
