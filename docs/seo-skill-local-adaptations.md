# SEO Skill Local Adaptations

This log records source-diverging changes made after the unchanged transfer was preserved in baseline commit `9d8e07f9c31f6611213bcee30fd1fecf44fd811b`.

## 2026-09-15: Codex product-policy compatibility

Installed build: `codex-cli 0.154.0-alpha.6.2`

The installed metadata parser rejected `api` in `policy.products` and reported these accepted spellings:

- `chatgpt` / `CHATGPT`
- `codex` / `CODEX`
- `atlas` / `ATLAS`

Official OpenAI documentation describes `agents/openai.yaml` as optional UI, dependency, and invocation-policy metadata and documents `allow_implicit_invocation`; it does not currently document `policy.products`. The accepted product values above therefore come from this installed parser's runtime validation, not from a broader portability claim.

### Adaptation

Deleted only the `- api` list item from each imported `agents/openai.yaml`. The remaining `chatgpt`, `codex`, and `atlas` values, all interface fields, and `allow_implicit_invocation: true` were preserved. No `SKILL.md`, reference, script, asset, writing template, or validator was changed.

This is a local compatibility adaptation, not an unchanged part of the original export. The exact source versions remain recoverable from baseline commit `9d8e07f` and the transfer file.

### Verification

- Structured `skills/list` with `forceReload: true`: 14 repository skills, 14 enabled, 0 list errors, and 14 loaded interface objects.
- Repository `invalid openai.yaml` warnings: 0.
- Fresh model-visible skill list: 14/14 imported skills present.
- `allow_implicit_invocation: true`: preserved in 14/14 files.
- Original export hashes still match 53/67 imported files. The only 14 expected divergences are the metadata files listed below.
- The bundled `quick_validate.py` could not run because PyYAML is not installed. No dependency was installed. The installed Codex parser successfully loaded every changed metadata file.

### Metadata hash record

| Skill | Original export SHA-256 | After product-policy adaptation SHA-256 |
|---|---|---|
| `ai-first-content-writer` | `edca8b42299bc4e54593b32a0e795198a93447976cc0da77a112de1834c8b520` | `e9d6387c2e36918724a8c43dd574df9f264d1ac477314119cacdf38bb1c17438` |
| `cluster-blog-writer` | `19e70a976811730ffdbc06cac7278ef0aad375d39ababb4c05a94d0c7676df24` | `855efb9801868455de56a671c025104a7b81b03ba7102e20f7386fe5efcee309` |
| `family-law-paid-landing-page-strategist` | `38ed45f1d841c9569657f2a8aad574a6b787ee7f77d9bf2e063bfa043575bcd1` | `8fb1eecfe3aec9cb328b7b7e4a77bd47aa7a1380b4fb94ed11a539071e36d378` |
| `family-law-red-team-qa-reviewer` | `28214f2987b682f5e344fe0fed87719d72f46f44eb9b7daa0f25c557b6728419` | `760bd8690eee388836490bffb471932efa765fd5de664ab30ef5216cd697f7b0` |
| `family-law-service-area-seo` | `41fa18740f4de9b748ee1b022172776944b63b087baee723ceb7bc4a4958ba22` | `fe476a27d37035841117fcf6d45036ae4af7c52f29f1860e8c52b43470d64e34` |
| `family-law-service-pages` | `194ad04a01e4fbe9013e35f9ac36825549d082ba8269ac7c3ef997d35910b97a` | `8aca6d98f37a9316b303cdbf4498520f8c54617aad07baf0307dab2b0dd934a4` |
| `family-law-situational-pages` | `0b7b5ba635fb3c0f1e76393f0ef7fbdcf89b34660832936a929ee846ba0c086b` | `9637e3ce7184c9817d8dfc4d1cbdfd885e413102127e72332728e5da5ebd5a86` |
| `legal-content-accuracy-qa` | `3ccaec48e6c59ffa33c04e96490607f1fa424afab275518efd380a4ab64bc5ce` | `ce01929ce6094696848ba7c427b8d46cd2810f9b15b7b8bd4dabeb2f8d03335d` |
| `qa-output-checker` | `69a58cf0217186b69be485b8f68ac86164577e3160cc06b13afbc33f8e914990` | `d8323fbc3de28ad9fbc535a7ac0df0f3134b9949d9e96ec8eabf0143f7211195` |
| `recursive-self-improvement` | `da9f7944d9c0869471cd1c4b4b5ee98c6dc7f1340d9afe06b37c15f1df4324ab` | `65bbb1237e4dcea26da61e3b3174e05dd269b8340197e8cfab4c55bee358a8a2` |
| `seo-marketing-sage` | `f770b4575810467574a51a5bb03f086f149c5e09e0ab0f427716006e83b3ba7b` | `e94612e4665a348a75c94f283968d612fb17b13696cc4ea578326fd87aec0584` |
| `servicecu-voice` | `cfad915f6e9945e1b39a2c7eaad11261296370844d3a4d062069588d83ede2fd` | `d86e918a8d511e012d2ca7b376b1ab20d5d41153167253effdbe31c5cf9da095` |
| `sterling-voice` | `36d9bd4f3c3ce9cbea88d69f5cb21323646445d87b36be16b6d761c6fe12eaaa` | `1475dcda5d44a10dcd69a111e759771ceb2b2b108bb843ec8a5b773e337ac05b` |
| `write-blattner-voice` | `18919f9198feccb28c2ebe5f99dadb01926ecade5eb78ff9e800d18d196e5c7d` | `5e56dd30c2b6dd05aa1b4b2270bcab9b4a89a418a5a6b211fd33c371b35d5e43` |

Recheck this adaptation after a Codex upgrade because the parser's accepted enum may change.

Official reference: [Build skills](https://learn.chatgpt.com/docs/build-skills)

## 2026-09-15: `family-law-service-pages` Core Hub workflow

Scope: Core Practice-Area Hub only. The Procedural branch and the three other source-incomplete writing workflows were not repaired.

### Provenance search and recovery

An expanded search covered Downloads and its archives, local Codex/Claude skill snapshots, seven local Git repositories and their histories, unreachable repository blobs, and Spotlight results. It found one genuine companion dependency:

- Source: `/Users/rocketclicks_1/Downloads/Skill-files/validate-page.js`
- Installed: `.agents/skills/family-law-service-pages/scripts/validate-page.js`
- SHA-256 at both locations: `291452d77e3449e605a6817cdfe27392193638506d69f7430b16b6bd44908c49`
- Pairing evidence: `Skill-files.zip` contains this exact validator and a byte-identical copy of the imported `family-law-service-pages/SKILL.md`; the accompanying README assigns the validator to the project's scripts directory and documents `node scripts/validate-page.js <docx>` plus `adm-zip`.

The README heading is dated later than its filesystem and archive timestamps. The recovery claim therefore rests on hashes, archive co-location, the identical skill entrypoint, and interface instructions, not that heading date.

No genuine `core-hub-template.md`, `procedural-template.md`, or package-owned `scripts/office/validate.py` was found. A proprietary runtime validator, architecture inventories, general QA documents, and client deliverables were rejected as originals. Client deliverables were not copied.

### Transparent local replacements

| File | Basis | Limitation |
|---|---|---|
| `references/core-hub-template.md` | Imported service-page standards plus governing V2 node, brief, relationship, path, and gate data | Core-only; not the missing original; does not supply prose or legal research |
| `scripts/build-core-hub.js` | Existing repository `docx-js` patterns, imported DOCX rules, and live parsing of the governing V2 embedded data | Turns reviewed JSON into DOCX; cannot establish strategy, publication state, client truth, or legal accuracy |
| `scripts/office/validate.py` | Deterministic requirements explicitly present in the imported skill, local template, and input manifest | Core-only mechanical checks; no editorial, live-URL, rendered-layout, or legal judgment; header/footer are an explicitly labeled local addition |
| `scripts/test-core-hub.py` | Positive/negative evidence requirement in the compatibility contract | Tests named detections only; broken documents exist only in a temporary directory |
| `scripts/render_support/pdf2image.py` | Narrow adapter for the two `pdf2image` calls made by the packaged Codex renderer | Not a general `pdf2image` implementation; uses PyMuPDF instead of Poppler |
| `scripts/render-core-hub.sh` | Wrapper around the installed Codex documents `render_docx.py` | Pins and verifies one installed renderer build and rejects nonempty output directories; LibreOffice may paginate differently from Word |
| `scripts/setup-renderer-macos.sh` | Reproducible isolated install of the hash-pinned official LibreOffice DMG | macOS arm64 only; installs about 804 MB under the ignored skill-local `.tools/` directory |

The skill entrypoint now routes Core work to the replacement contract, marks Procedural work pending, and applies V2 precedence to hub sets, paths, gates, link direction, Emergency Guardianship classification, and build sequence. `agents/openai.yaml` has a truthful concise interface description; its product list and `allow_implicit_invocation: true` are unchanged from the prior metadata adaptation.

### Initial Core repair hash record (superseded for changed files)

These were the post-repair local hashes before the later schema 2 client-URL mapping correction. They are retained as historical evidence, not presented as the current hashes of files changed later. The recovered validator is the sole unchanged source dependency in this group.

| File | SHA-256 |
|---|---|
| `SKILL.md` | `073087be3652a03671cdae6362b0619f4f9a87e71653371acccf69b968000e9b` |
| `agents/openai.yaml` | `0a49d9dc1b584efdc4398204be3aa60a823bd78cee9eed00b1ca2114296124fa` |
| `references/core-hub-template.md` | `c139a726fffa79c4b44a1d7ff54a348692441ca40f45c0588aa47d011c678d97` |
| `scripts/build-core-hub.js` | `935f0ebf4cd190d0631c2946d05429b3160943b33a3d52dd7190d0686d3ffdd9` |
| `scripts/office/validate.py` | `928b07d4b893d090bf70d64a2afcdeb979df3527c4c828183cc05a942c375d87` |
| `scripts/validate-page.js` (recovered unchanged) | `291452d77e3449e605a6817cdfe27392193638506d69f7430b16b6bd44908c49` |
| `scripts/test-core-hub.py` | `319c8bf8b50e2cd451f7176909e92d47680499fce848dbff444fadbefb309003` |
| `scripts/render-core-hub.sh` | `d45ac934f8502ba6609e019481f4b644c21224baa447daa51e954fa7b277f167` |
| `scripts/render_support/pdf2image.py` | `9affe53e0922ebb6e5428527f17899e47f9ba2c47a070b6df535fe13f42368af` |
| `renderer-tools.lock.json` | `8c94d7daf992ebc87cdf14480b611ac9adb0b6e97a7a59375302b80f39bd5c3a` |

### Isolated dependencies

- Node packages: `docx@9.7.1` and `adm-zip@0.6.1`, pinned by the skill-local `package.json` and `package-lock.json`.
- Visual Python package: `PyMuPDF==1.26.4`, pinned in `requirements-render.txt`.
- Skill-validation package: `PyYAML==6.0.3`, pinned separately in `requirements-skill-validation.txt`.
- Renderer: official LibreOffice 26.8.0 macOS aarch64 DMG, SHA-256 `8858d8058da4f862f47559486814e65efc27294da67c5e4bb56b006b1ee59f89`; Codex documents package `26.819.11345` `render_docx.py`, SHA-256 `d8fe979f76e11215e146e53484bb4cb4e5f3906b58debed6844171073b187286`. Both are recorded in `renderer-tools.lock.json`.

`node_modules/`, `.venv/`, and `.tools/` are ignored inside the skill. No root application dependency file and no global environment was changed.

### Verification

- The Core generator created one explicitly synthetic Divorce fixture with no firm or jurisdiction facts, no substantive legal claim, and no source citation.
- Structural validator: PASS; 1,832 manifest-content words, 14 headings, 10 real list items, five manifested hyperlinks, zero sources. The synthetic warning and any generated Sources section are excluded so the generator and validator measure the same V2 content target.
- Recovered page validator: PASS; five unique body destinations, zero em dashes, zero citations, no warnings.
- Regression harness: six positive checks passed and 17 intentionally altered cases returned nonzero with their required findings. Coverage includes page geometry, duplicate/unmanifested/broken hyperlinks, em dash, immediate opening and role/body order, well-formed versus unbold/generic placeholders, local header/footer, held and ungated conditional targets, citation-aware sentence counting, 12 pt Sources, and stale render output.
- Pinned packaged renderer: six US Letter pages at 144 DPI in a fresh post-review directory; all six PNGs inspected at original resolution. The intermediate PDF retained five unique destinations across ten clickable rectangles because each anchor wrapped across two lines. The final PNGs match the preserved earlier render byte-for-byte. LibreOffice substituted Liberation Sans for Arial on this machine; the DOCX OOXML still declares Arial.
- Mechanical QA: PASS for the synthetic fixture purpose, not publication.
- Legal QA: not applicable because the fixture contains no substantive legal claim; no legal-accuracy pass is claimed.
- Codex skill-creator quick validation: PASS.
- Structured Codex `skills/list` with `forceReload: true`: the adapted skill remained repository-scoped and enabled with the new Core-ready/Procedural-pending description; the result contained zero list errors.

### Read-only reviewer reconciliation

One `seo_reviewer` pass was run after the initial evidence existed. It remained read-only. Its two blockers and five material hardening findings were accepted: target gate enforcement, citation-aware sentence parsing, exhaustive hyperlink reconciliation, actual section sequence/content checks, 12 pt Sources, explicit local-detail behavior, and renderer pinning. Its optional stale-output and header/footer-provenance findings were also addressed. No second reviewer pass was requested; the strategist reran generation, all regressions, and the full visual inspection after the corrections. The saved reviewer record distinguishes its original findings from the later verification.

Evidence is under `evaluations/runs/2026-09-15-family-law-core-hub-workflow/`.

The recovered validator retains Johnson Law Group-specific `North Star` logic and broader phrase matching. Those findings must be interpreted against the applicable client voice and evidence rather than treated as newly invented generic requirements. The Procedural branch remains pending and no result here establishes SEO competence, legal accuracy, editorial quality, or performance.

## 2026-09-15: Core Hub V2/client URL mapping correction

The Wisconsin Divorce revision demonstrated that the initial local Core contract incorrectly treated a V2 reference pathname as the required live client pathname. Sterling had direct, published Wisconsin child destinations whose paths legitimately differed from V2. Requiring the client to mirror V2 would conflate architectural identity with implementation and could manufacture an unsupported migration recommendation.

### Narrow persistent correction

- Advanced the Core input contract to schema 2.
- Kept each node's exact V2 ID, reference path, page type, role, requiredness, directional relationship, and gate as architecture fields.
- Added a separate direct `client_url` mapping with recorded status, redirect count, verification date, publication evidence, and jurisdiction evidence.
- Changed DOCX generation and structural validation to use `client_url` as the clickable destination while continuing to validate the V2 record independently.
- Retained same-origin, matching-jurisdiction, relationship, canonical-gate, held-target, and conditional-approval controls. The generator validates the recorded evidence shape; live verification remains a separate research gate.
- Reclassified the existing 5-8 source target as editorial guidance rather than a mechanical maximum. This does not make source count a quality measure or relax claim-to-source relevance checks.
- Documented that a V2/client path difference alone does not establish a migration, redirect, canonical, or consolidation need.

The correction applies only to the repaired Core Hub route. It does not repair the Procedural branch or any other incomplete writing workflow, and it does not change the governing V2 architecture.

### Demonstration and regression evidence

- **Original case:** `FL-PA-DIV` generated and validated with seven direct Wisconsin client destinations, including V2 `/divorce/collaborative-divorce/` mapped to client `/wisconsin/divorce/collaborative/`, while retaining the exact V2 relationship and gate.
- **Different relevant case:** an ephemeral reserved-domain Wisconsin mapping with `/wisconsin/` inserted into the client paths generated and passed both validators.
- **Unaffected case:** the existing synthetic same-path fixture continued to pass. Existing held-target and unapproved-conditional-target cases continued to fail as required.
- **Focused negatives:** altered V2 path, wrong same-origin jurisdiction, and wrong directional relationship each failed with the expected finding.
- **Source guidance:** a nine-source, claim-free format fixture passed, demonstrating removal of the hard cap without asserting those sources were useful.

The focused harness passed seven positive checks, and 20 intentionally altered cases produced their required failures. Evidence is preserved under `evaluations/runs/2026-09-15-family-law-core-hub-workflow/validation-client-url-mapping/`.

### Historical post-mapping, pre-citation-order hashes

These are local-adaptation hashes recorded after the mapping correction and before the later citation-order correction. They are not original-export hashes or current hashes.

| File | SHA-256 |
|---|---|
| `SKILL.md` | `c5fafde2e8bd8deed826f707b5fa04146e9f9ef3c101dacc8b756917a2cc6fa0` |
| `references/core-hub-template.md` | `ae20f1fa144a44fe739bab4a67a3e341c77eb295febc8b1bf4f594bbd40eacee` |
| `scripts/build-core-hub.js` | `c883627083999f41c6576ca9c3aa07ebdf71bd3915058fa13319454d1003bc51` |
| `scripts/office/validate.py` | `0457c8652cea2ae95ca80cd7bb13e85a57a338b261a537f3e1116e79dab5ff5e` |
| `scripts/test-core-hub.py` | `01e6308dab0510f1bdf165cce234e081a5ac58803558899c0d4a87ae9b03d2b2` |
| synthetic workflow input | `34150ec51d83181478f4f6cd0d5a75b5230aec732e7577e1cded0428955720ba` |
| synthetic DOCX fixture | `932272fde35bd14b64b604f931d7c8b15da2977046830e755c01c7e7ec70b17f` |

One read-only `seo_reviewer` pass on the Wisconsin revision confirmed the actual V2 classifications and the architecture/client separation, then identified stale render evidence and internal CTA commentary. Both material findings were corrected and the affected checks were rerun. That single result does not establish general SEO competence or performance.

## 2026-09-15: Core Hub citation-order correction

The Wisconsin Divorce production draft demonstrated that marker numbers and Sources rows could agree with each other while still beginning out of order in the body. The generator derived numbers from the declared Sources inventory but did not require that inventory to follow first citation appearance. The structural validator compared aggregate hyperlink counts, which could also miss two body citation targets swapped with each other.

### Narrow persistent correction

- Require Core Hub Sources to be declared in first-appearance order, beginning at `[1]` and continuing without gaps.
- Have the generator compare first unique body `citation_id` appearances with the declared source IDs while retaining unique-ID, expected-marker, and exact-one-use checks.
- Have the structural validator independently compare manifest order, visible body-marker order, each marker's hyperlink target, and each Sources row's text and URL.
- Keep citation markers inline with their preceding text; the corrected Wisconsin input contains no breakable whitespace immediately before a marker.
- Preserve schema 2 architecture fields, V2 gates, and client URL mappings unchanged.

### Demonstration and regression evidence

- **Original case:** the Wisconsin Divorce source inventory now follows its actual first appearances (`pricing`, `mediator`, `separation-status`, `separation-relief`, `residency`, `grounds`, `waiting`, `property`, `maintenance`, `custody`, `support`), producing `[1]` through `[11]`; generation and both validators pass.
- **Different relevant case:** the existing nine-source synthetic format case passes in order. A copy with internally consistent marker numbers but a source inventory outside first-appearance order fails at generation; a DOCX with its first two citation relationship IDs swapped fails structural validation even though aggregate URL counts remain unchanged.
- **Unaffected cases:** the no-source synthetic fixture and the divergent V2/client-path positive still pass. Wrong V2 path, wrong jurisdiction, wrong directional relationship, held target, and unapproved Conditional target still fail as required.

The complete focused harness passed seven positive checks, and 22 intentionally altered cases produced their required failures. Evidence is preserved under `evaluations/runs/2026-09-15-family-law-core-hub-workflow/validation-citation-order-final/`.

### Current post-correction hashes

These are local-adaptation hashes, not original-export hashes.

| File | SHA-256 |
|---|---|
| `SKILL.md` | `03976956985d4c65deaaffeacc094c0aff5c131f614df03f8755cc24c7ed2d48` |
| `references/core-hub-template.md` | `e8d2c690eb404fc1e018eca14abfa8754105cbd599cf70e6a63f9c449dd19ff2` |
| `scripts/build-core-hub.js` | `b3b4f92735091bace4e317f6687bb90c1a259775e31b70e1b999fdce6face85e` |
| `scripts/office/validate.py` | `a5df84b3eb7fbc97f665f16c9dac57adc1d5dcdd99330e2388ea2094d4e33a03` |
| `scripts/test-core-hub.py` | `cd8dc600dc2984a20b678bbd1a9fe23b6011c8aeb47214a3ec89a384b2d8df6d` |

This correction addresses citation mechanics only. It does not establish source relevance, legal accuracy, editorial quality, or performance, and it does not repair the pending Procedural route or any unrelated incomplete workflow.

## 2026-09-15: Required Core-child applicability record

The Fanash Florida Divorce production draft demonstrated that V2 Required status and a technically live client destination do not, by themselves, establish jurisdiction fit, current service acceptance, or publication safety. It also demonstrated that a Required child may remain linked only after the generic label is qualified for the governing jurisdiction.

### Documentation convention

For every Required direct Core child that is qualified, excluded, or mapped to a client-specific destination, record the exact V2 status, jurisdiction and client evidence, implementation decision, and any repair or reactivation condition. Treat a direct `200` and an on-topic first-party service claim as link-eligibility evidence, not full destination QA or operational-intake confirmation.

- `FL-M006` Legal Separation is linked with an explicit Florida-alternatives qualification because Florida does not create the generic marital status implied by the node label.
- `FL-M008` High-Conflict Divorce is excluded despite a `200` because cross-topic metadata and copy make the destination publication-unsafe until repaired.
- `FL-M004` Contested Divorce remains eligible because it is a direct, on-topic, published child destination; full destination-page QA remains separate.

This is a documentation-only convention. It does not change V2, the generator, validators, link direction, or activation gates, and it must not automatically block an otherwise valid link. The independent reviewer approved the convention after expanding it beyond excluded children. Client-specific evidence and decisions are preserved in `clients/fanash/deliverables/florida-divorce-core/supporting-record.md`.

## 2026-09-16: Core link-decision documentation clarification

The Fanash finishing revision demonstrated three distinctions that the Required-child convention did not state explicitly:

- A relationship missing from V2 is unspecified by that source. The current Core manifest must not invent or activate an absent edge, but the absence is not a universal prohibition on a future architecture decision supported by governing evidence.
- A repair requirement for an excluded destination governs later activation of that specific link. It does not block a draft that omits the destination.
- `Optional` status alone neither requires nor prevents a link. An Optional child still needs the exact V2 direction, reviewed publication and jurisdiction evidence, and a contextual reason under the local Core rule.

Reviewed frozen checks:

1. **Original case — `FL-M009` Annulment:** V2 classifies it as Procedural / Procedure / Optional with `PASS — CANONICAL` and the exact contextual `FL-PA-DIV → FL-M009` parent-child edge. A live, relevant Fanash destination and one strong process-choice placement support activation; Optional status is preserved but is not the activation reason.
2. **Different relevant case — `FL-M008` High-Conflict Divorce:** A direct `200` does not cure its cross-topic metadata and copy defects. Exclusion remains justified, but repair is a future activation condition rather than a blocker for the current draft.
3. **Unaffected case — cross-hub relationships:** The Fanash draft activates only resolved parent-child edges. Missing cross-hub edges remain unspecified by V2 and are not described as universally prohibited; no new relationship is invented or activated.

The independent reviewer approved this narrow documentation clarification. It changes no V2 relationship, generator rule, validator, link direction, activation gate, or automatic activation behavior.

## 2026-09-16: `family-law-situational-pages` bounded `FL-M008` workflow

The first authorized production use of the imported Situational skill confirmed that its named template and validators were absent. No genuine original was recovered. This adaptation supplies a transparent local replacement for `FL-M008` High-Conflict Divorce only; it does not claim that the source package or other Situational routes are complete.

### Replacement components and provenance

Every new component is labeled **LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL**.

| Component | Provenance and boundary |
|---|---|
| `references/situational-template.md` | New content contract derived from the imported Situational instructions and governing V2 `FL-M008` record; not derived from the Core Hub template. |
| `scripts/build-situational.js` | New manifest-driven generator using pinned `docx` mechanics and runtime V2 parsing; it contains a separate Situational structure, metadata contract, and link contract. |
| `scripts/office/validate.py` | New FL-M008 structural validator using generic OOXML integrity concepts; it does not import the Core page schema. |
| `scripts/validate-page.js` | New FL-M008 page/link validator using `adm-zip`; schema version 2 distinguishes explicit V2 relationships, skill-required navigation, and the consultation CTA. |
| `scripts/render-situational.sh` | Thin wrapper that delegates only generic DOCX rendering to the pinned Core renderer; no Core content template, generator, validator, or link rule is invoked. |
| `scripts/test-situational.py` | New positive and negative route regression suite. |
| `LOCAL-REPLACEMENT.md` | Scope, commands, manifest shape, component provenance, and readiness limits. |
| `package.json` / `package-lock.json` | Isolated `docx@9.7.1` and `adm-zip@0.6.1` dependency boundary. |

The skill entrypoint and interface metadata state that executable local readiness is limited to `FL-M008`. For this route, V2 remains authoritative for classification, hierarchy, and every explicit V2 relationship. The separate Situational requirements for a parent-Hub navigation link and the bounded `FL-M004` process bridge remain active even though neither direction is recorded as an outgoing V2 edge. A final consultation CTA is also required. Held targets and unverified destinations still fail.

### Demonstrated contract and verification

- The manifest separates V2 identity and reference path from the retained client URL and proposed metadata.
- Production inputs require dated direct-200 retained-URL evidence, explicit client/voice/jurisdiction evidence, a dated destination inventory, and live-verified official sources. The shape checks do not independently prove those assertions.
- The consumer-copy contract requires 1,100–1,700 words, two answer-first opening paragraphs, scenario ownership, selective stakes/legal context, practical strategy, verified firm-help language, optional scenario FAQ, a final CTA, and Sources last.
- The DOCX and validators enforce Letter geometry, one-inch margins, Arial 12 pt body and Sources, 18/15/13 pt headings, real lists, one body marker plus one Sources hyperlink per source, manifested internal links, paragraph limits, placeholders, comments/revisions, and metadata.
- The final focused harness passes 21 cases covering the three required navigation/CTA authorities, one additional exact V2 edge, false edge claims, missing or wrong authority, wrong targets, invented V2 fields, CTA placement, an empty manifest, Hold and destination-screen failures, contamination, missing styles, duplicate links, and 9 pt Sources.
- Codex skill-creator quick validation passes using the existing isolated PyYAML environment.
- The assignment-specific draft passed generation, both validators, source/link reconciliation, and fresh render inspection. Its client facts, legal conclusions, provisional SEO hypothesis, and reviewer decisions remain in the client supporting record rather than this workflow log.

### Independent review correction

The read-only `seo_reviewer` found that the initial generator emitted 9 pt Sources while the contract required 12 pt. The generator and structural validator now require 12 pt Sources, and a 9 pt negative regression passes. It also required the compatibility and adaptation records to distinguish the still-incomplete source package from bounded local readiness; those records now do so.

The reviewer's optional suggestion to reject `Draft` in every metadata field was not adopted in this bounded repair. The current output fields are clean, the generator already rejects `Draft` in the title tag, and broader preventive hardening was not necessary to complete the demonstrated `FL-M008` assignment. Revisit that proposal only with a fixed evaluation and route-relevant regression evidence.

### 2026-09-16 targeted navigation-authority correction

The completed `FL-M008` draft exposed an exclusive-edge restriction in the local replacement: it treated the absence of an outgoing V2 edge as sufficient to cancel the Situational skill's separate parent-navigation and process-bridge requirements. That route-specific behavior was incorrect. The schema is now version 2 and requires the actual authority for each link instead of inventing a V2 relationship.

- **Original demonstrated case:** One `skill-parent-navigation` link to the actual V2 parent, one `skill-process-bridge` link to `FL-M004`, and one `consultation-cta` pass without a `v2_edge_id`. Falsely presenting either navigation link as an outgoing V2 edge fails.
- **Different relevant case:** An additional `v2-explicit-relationship` link to `FL-M010` still requires and passes only with exact edge `CL-00068`, the exact V2 path, a publishable target, a passing gate, and destination evidence.
- **Unaffected safeguards:** Empty required navigation, missing or unknown authority, wrong targets, invented V2 fields, a Hold target, unverified or duplicate destinations, duplicate rendered placement, content contamination, and invalid document styles still fail.

This is a demonstrated correction to the bounded `FL-M008` local workflow, not a general SEO principle and not evidence of readiness for another Situational node. Earlier statements in this record that limited every link to an outgoing V2 edge or allowed an empty manifest are superseded by this subsection.

### Current local hashes

These are local-replacement hashes, not original-export hashes.

| File | SHA-256 |
|---|---|
| `SKILL.md` | `f84b557140f5dce3a254ed41aba3e605111c9fab63d518992c1517156a8ee653` |
| `agents/openai.yaml` | `23ba1d9d0848e04170ea99ac30444afb88306fa34a0a1e6b4aca4a24bef59cb6` |
| `LOCAL-REPLACEMENT.md` | `70cd713c2813880a64ac1c1b2c8540268c2f5369dfd69f604683e5a0c1f0de08` |
| `references/situational-template.md` | `261d3601eecfd58219b439cf5f7da93699fd306b3a04f932b69b9391236dae16` |
| `scripts/build-situational.js` | `eff6d635ae1609723814faec5301ee16ed2e6fb5bd439a96f7cea8a90c7ad037` |
| `scripts/office/validate.py` | `aecc448d4acf44f5b2a007ca00913f757887ae70ca802833c9ff466b22744212` |
| `scripts/validate-page.js` | `22321c232fc991604a285085f1ec05cd881b191d9e0aa0b8f40fdb70761450d9` |
| `scripts/render-situational.sh` | `943325f45c33ca57a93beb256cd17a7ec4989892ee0c70b9e15a7167a4a8a959` |
| `scripts/test-situational.py` | `c45ad571da176010409daf9261e7e888a8fb5bc5f1ad68bb6c7138d620d55a1b` |
| `package.json` | `fe05954c68d855027db3ff5c82360ab7b464a14d584e5ae90e84dd701047a7b9` |
| `package-lock.json` | `574066f2ffdb4b809891d2cfafa7e847b26d7e57f7bdc97fb81e450d01eec193` |

This adaptation establishes tested mechanics, not editorial quality, legal accuracy, client truth, link-destination quality, service availability, Microsoft Word fidelity, or SEO performance. Other Situational nodes remain pending separate adaptation and evidence.

## 2026-09-16: Automatic strategist/reviewer learning-loop retrieval

The repository already instructed substantive use of the read-only `seo_reviewer`, evidence-based reconciliation, bounded repair, and evidence-based persistence. The demonstrated gap was retrieval: fresh prompt inspection exposed `AGENTS.md` and recursive-skill metadata but not retained lesson bodies, and no executable lifecycle hook existed.

The smallest retained correction has two layers:

- `AGENTS.md` now requires targeted retrieval of scoped, adopted prior lessons before substantive decisions and proactive reviewer use without a user reminder. `learning/README.md` now distinguishes substantive reusable changes from simple preferences and no-op task completion.
- `.codex/hooks.json` adds a separately trusted `UserPromptSubmit` candidate router. Its versioned helper reads only allowlisted shared record headings, never client files or transcripts, and emits no lesson body. It cannot select the reviewer, adjudicate evidence, or save a lesson because those decisions remain instruction-driven and this Codex version skips `agent` hook handlers.

An initial independent `seo_reviewer` pass required the trust, authority, privacy, scoping, and evidence distinctions implemented above; its final read-only recheck found no remaining blocker or material issue. The focused helper suite passes eight original, different, minor, unrelated, malformed, client-safety, matching, and no-match cases. A clean read-only agent session retrieved the relevant Core path-mapping and bounded `FL-M008` navigation corrections, invoked the project reviewer without being prompted to do so, and incorporated its material qualifications without creating a new lesson. On 2026-09-17 the exact candidate-router handler, hash `sha256:5a7d802fcd07e8a8b4dc1233422e3cf474d6ef0c938bf347504def01dc669a9b`, was confirmed trusted and active. A fresh session received its hook-only context without a trust bypass, completing the previously pending lifecycle check.

The retained learning-record reference changed from SHA-256 `627d9c23cadef1dc256a920bdafd01b62dee88220465ab86c292ab16e6249b6c` to `4846c51d12b236fbd6a5966035efb5e9a1c169fb69746bf5aaeb8fb583442193`. This is a local operational record, not model training, native memory, a guarantee of future reviewer selection, or proof of SEO impact.

## 2026-09-17: Automatic MemPalace recall with approval-gated retention (superseded)

This is the historical first phase, superseded later on 2026-09-17 by the coordinator-owned automatic curated-retention workflow below. Casey initially requested automatic, bounded MemPalace recall for substantive SEO_Dept work without a skill mention, while keeping repository instructions authoritative and every memory mutation approval-gated. At that phase, `AGENTS.md` owned the rule and `.codex/hooks.json` added the versioned, instructions-only `mempalace-recall-reminder-v1.py` alongside the unchanged lesson router; the helper did not inspect, log, or emit prompt text or read transcripts, and it never called MCP.

The installed MemPalace 3.10.0 implementation exposes no MCP read-only annotations. Inspection of its handlers and mutation guards supported exact `approval_mode = "approve"` overrides only for `mempalace_search`, `mempalace_get_drawer`, `mempalace_list_drawers`, `mempalace_kg_query`, `mempalace_kg_timeline`, `mempalace_diary_read`, `mempalace_list_wings`, and `mempalace_list_rooms`. The ignored project-local `.codex/config.toml` retains `default_tools_approval_mode = "writes"`; every unlisted tool remains approval-gated. Autosave and daemon flags remain false, hub forwarding remains off, and no transcript-ingestion, repository-mining, serving, or daemon process is configured or running.

The reminder's three direct tests and the existing router's eight tests pass. Structured hook inspection reports both handlers trusted and active with no warnings or errors; the reminder hash is `sha256:20b92c6d252f12826e0c51a1411f8b71301a91ad1d955843b360daad9bc049ef`. A fresh no-bypass, no-approval session received the exact reminder context, and an ordinary internal task completed a relevant `mempalace_search` without an approval interruption. Separate calls to the unlisted write tool `mempalace_checkpoint` with an empty item list and the mutation-capable `mempalace_delete_by_source` in dry-run mode both failed before dispatch with `MCP tool call requires approval, but approval policy is never`; no palace or repository data changed.

The independent reviewer found no hook or approval-policy defect, but identified stale setup and compatibility records that still described one untrusted hook and pending activation. Those status sentences were corrected in the smallest owning sources. This demonstrated the configured phase-one paths, not that every future task would choose the right query or memory. The per-save approval rule and v1 reminder are historical and must not be used as current policy.

## 2026-09-17: Coordinator-owned automatic curated shared learning

Casey's later explicit authorization superseded routine per-save approval. `AGENTS.md` now requires automatic relevant recall before substantive work and one coordinated learning pass after meaningful completed work. Workers and reviewers return their result and evidence, material mistakes or demonstrated methods, a scoped lesson candidate or `none`, and remaining uncertainty or disagreement. They do not write durable memory or promote shared rules. The primary strategist consolidates concurrent contributions, checks conflicting guidance and counterexamples, obtains read-only review for material behavioral changes, and owns both repository adoption and any durable MemPalace write.

Participating agents use the same project-local `seo_dept` palace through verified read-only MCP access or a source-linked context handoff limited to the assignment. Actual `mempalace_search` calls completed without approval from both a child agent and the custom `seo_reviewer`; this verifies those instances rather than assuming universal inheritance. Repository instructions and evidence remain authoritative. Memory entries provide cross-session continuity and point back to the source task or affected file; shared methodology, role-specific lessons, client-specific facts, and durable unresolved questions stay separated.

The ignored project-local `.codex/config.toml` keeps `default_tools_approval_mode = "writes"` and adds automatic approval only for the minimum retention sequence: exact `mempalace_check_duplicate`, then exact `mempalace_add_drawer` for a confirmed non-duplicate. MemPalace 3.10.0 source inspection found that `mempalace_add_drawer` accepts only `wing`, `room`, `content`, `source_file`, and `added_by` and uses a content-addressed idempotent identifier; it cannot update, overwrite, delete, mine, import, sync, or share. All unlisted mutation tools remain approval-gated. Autosave, transcript ingestion, repository mining, hub forwarding, sharing, serving, and daemon mode remain disabled.

`.codex/hooks.json` replaces v1 with the separately trusted, instructions-only `mempalace-recall-retention-reminder-v3.py` while preserving the lesson router and its ordering. The short-lived v2 candidate was superseded before completion after final review found that an unfiltered wing search could expose one client's facts to another client-scoped assignment. V3 requires room-filtered shared, relevant-role, and exact-current-client searches with a combined small-result cap; if the client room is unknown, agents may list room names but must not search client contents until scope is known. The helper itself never reads a transcript, inspects or logs prompt text, calls MCP, spawns an agent, or writes memory. No `Stop` hook was added. Instead, the v3 context requires no more than one coordinator learning pass per completed task, normally one saved entry, no repeated same-turn save, and at most two focused repair attempts. A save is not a new learning trigger.

The unchanged router's eight focused tests and the v3 reminder's six policy tests pass, including static assertions for exact room filters, unknown-client narrowing, a combined retrieval cap, and prompt/transcript privacy. The exact v3 handler was reviewed and trusted at hash `sha256:3a15803c2f68895d849b1938702bf958056540a7fba01f3f7701117ad2c937c4`. That hash was invalidated by the 2026-09-17 retention-routing rule edit; Codex re-trust is pending. Direct child and reviewer read access is execution-verified as described above. A fresh ordinary documentation task under approval policy `never` searched the palace, checked a new coordinator-write guardrail for duplicates at `0.9`, and created `drawer_seo_dept_operating-rules_b2b6f07d08b2105c0fd38804` without an approval interruption. After v3 trust, a different fresh non-client run listed room names and searched only exact room `operating-rules` with limit three, retrieving that source-linked entry without a skill mention or recall request, wing-wide search, client-room search, or approval. Exact-content duplicate checking returned similarity `1.0`, no second drawer was added, and the wing count remained three at that checkpoint. Separate no-op fresh-session probes confirmed that checkpoint, deletion-by-source, update, mining, and sync remain approval-gated; remote forwarding remains disabled and no sharing tool is allowlisted.

The first automatic-save attempt also exposed MemPalace's per-palace single-writer contention between concurrent MCP connections. Installed 3.10.0 source and a bounded retry confirmed that later mutating calls re-attempt the lease. The smallest correction is now authoritative in `AGENTS.md`: finish agent contributions, serialize coordinator saves across active sessions, never bypass the lock or launch competing writers, wait for the owning coordinator MCP connection to release its lease, retry only within the existing two-repair cap, and report remaining failure accurately. The setup guide carries the operational pointer. After the documentation and v3 isolation repairs, the independent reviewer's final read-only recheck found no blocker or material improvement; it retained the limits that no live client-room fixture or remote-sharing write was attempted and no professional-quality or performance gain was established.

The coordinator's final learning pass then duplicate-checked the reviewed client-room isolation correction, saved it as source-linked drawer `drawer_seo_dept_operating-rules_c92b7411b15d551c16447724`, and read it back successfully. The palace contained four drawers after that save. This memory points to the authoritative v3 implementation; it does not replace it or broaden the static isolation evidence into a live cross-client test.

This architecture is a scoped, reversible workflow change, not evidence that additional memory volume, longer outputs, or more review rounds improve SEO work. Any claimed behavioral benefit still requires fixed original, different-applicable, unaffected, and unsupported-lesson cases, and later natural use must narrow or reverse a rule that causes regression.

## 2026-09-17: Retention room routing and open-question recall repair

A saved project-wide open question was found to hold client-specific examples and one
unsourced geographic assertion in the shared `open-questions` room. The record was
corrected in place and three rules were added to prevent recurrence on both hosts.

### Corrected record

- `drawer_seo_dept_open-questions_9e47f066dd40252101caa0ce` was rewritten with
  `mempalace_update_drawer`, the designated approval-gated update tool. The client
  name, the two county and city examples, and the two-state references were removed.
  The V2 path facts, the line 15 and line 53 citations, both affected authoritative
  files, the `source_file` metadata, and the original `filed_at` were preserved, and a
  `Source task:` clause was added per `AGENTS.md`. Every chunk was re-read individually
  after each update. `mempalace_check_duplicate` against the pre-repair text returned
  no match, which shows the vectors were re-embedded rather than left stale.
- The one independently sourced instance, a county-name recurrence, was deliberately
  not retained in any room. It exists only in the task artifact.
- `mempalace_update_drawer` overwrites without history, so the pre-repair text is not
  recoverable from the palace.

### Rules added

Three sentences were appended to `AGENTS.md` lines 29, 35, and 36 and mirrored verbatim
into the matching paragraphs of
`.codex/hooks/mempalace-recall-retention-reminder-v3.py`, which both hosts load: Codex
through `.codex/hooks.json` and Claude through `.claude/settings.json`.

1. Retained open questions get a bounded recall route, anything recalled from an
   open-question room stays unresolved rather than validated guidance, and
   client-specific content found in the shared room is a routing defect to report
   rather than evidence to apply.
2. Routing follows content scope: client material belongs in that client's room, and a
   missing or not-yet-created client room is never a reason to use a shared room.
3. Every factual assertion carries its supporting evidence or an explicit unverified
   label, inside open questions too.

`.claude/agents/seo-reviewer.md` and `docs/seo-skill-compatibility.md` carried room
enumerations that the recall change made narrower than `AGENTS.md`; both were extended
to match rather than left contradicting the governing rule.

### Separate pre-existing defect found during the repair

`ADDITIONAL_CONTEXT` measured 3513 characters against `additionalContextLimit: 3200`,
so the tail of the retention-safety paragraph was being truncated on Codex only;
Claude's handler sets no limit and received the whole text. The limit is now 5200
against a 4557-character raw payload. A new test bounds both the decoded string and the
raw stdout payload against the configured limit and asserts the closing sentence
survives. Measuring injected context against the configured host limit before appending
is the method that surfaced this.

### Verification

- `.codex/hooks/test-mempalace-recall-reminder.py`: 6 of 6 pass. The 4 pre-existing
  tests are unchanged and still pass, serving as the unaffected case.
- Disposable fixture outside the repository at `/tmp/mp-routing-fixture/`: 6 of 6,
  covering the original failure case (rejected on both required grounds), the repaired
  shared question taken verbatim from the palace (accepted with zero violations), a
  properly scoped client memory (accepted in its client room and rejected as a negative
  control in the shared room), and a client with no directory and no room yet (still
  caught). The fixture found one real defect during hardening: an intermediate repair
  named the client in its own `Source task:` field.
- Frozen criteria, fixed before the runs: the failure case must be rejected for both
  stated reasons, the legitimate shared question must pass with zero violations, and a
  properly scoped client memory must pass in its client room and fail in a shared room.

### Limits

- The fixture predicates are heuristics standing in for strategist judgement. They show
  the rules discriminate these cases; they do not validate the rules generally.
- The evidence-or-label rule is a judgement rule and is not mechanically enforced.
- Editing the handler invalidated its recorded trust hash, so Codex re-trust is pending
  and the truncation fix is unverified on that host. The rules themselves do not depend
  on the hook, since `AGENTS.md` carries them and Codex reads it directly.
- Whether this unresolved architecture question should also be recorded in the V2
  open-decisions section is a pending user decision; that file was not edited.

## 2026-09-24: Current-source research made mandatory (research-first, never placeholder-first)

Branch `content-workflow-pilot`. Source task: full-system audit, repair, and test of the
content-workflow pilot (user request 2026-09-24). Contributing agents: primary strategist
(design, code, tests); `legal-reviewer` and Codex `legal_reviewer` (live integration runs);
`seo-reviewer` (independent review of the change). Verification state: execution-verified in the
pilot test suite and on a fresh client run; the `AGENTS.md` rule outside the pilot is
instruction-only.

### Observed failure

The pilot's gate bound reviews to file hashes but had no mechanical evidence that any source was
retrieved. A Verification Log row proved only a date: the 2026-09-23 fixture pre-draft record said
"nothing fetched" and passed coverage; a row copied from an earlier run, a saved `sources/` note, or
memory would have passed. The writer role and both situational skills carried placeholder-first
instructions ("leave a placeholder rather than guessing").

### Correction adopted

- `AGENTS.md`: new section "Current-source research" (mandatory on every new assignment and every
  standalone skill invocation that drafts, audits, or verifies client-facing content; prior reviews,
  memory, saved files, and brand guidance do not satisfy it; record what was retrieved, when, its
  effective dates, the claims it supports, and retrieval evidence; research before placeholders;
  report incomplete when evidence cannot be obtained). Default workflow step 2 amended to match.
- `docs/seo-skill-compatibility.md`: precedence bullet stating that imported placeholder-first text
  is superseded on conflict and that the imported skill files stay unchanged as the fallback.
- Pilot: `scripts/research_fetch.py` and `scripts/cw_research.py` (per-run nonce; a record is
  written only after a live HTTP 200 fetch with the named excerpt and currency marker present;
  offline rules; live re-fetch; Verification-Log linkage), `readiness_check.py --stage research`,
  new reason codes (`RESEARCH_NOT_OPENED`, `RESEARCH_MISSING`, `RESEARCH_REUSED`, `RESEARCH_STALE`,
  `RESEARCH_INVALID`, `RESEARCH_JURISDICTION_MISMATCH`, `LEGISLATION_NOT_EFFECTIVE`,
  `RESEARCH_UNAVAILABLE`, `RESEARCH_EXCERPT_DRIFT`, `RESEARCH_LIVE_SKIPPED`,
  `LEGAL_LOG_NO_EVIDENCE`), `record_review.py` refusing legal rows without this-run evidence,
  `deliver.py` writing `research-ledger.md`; canonical roles, rules, criteria, schema, coordinator
  skill, and the four candidate skills reworded research-first. Details:
  `pilot/content-workflow/docs/CHANGES-AND-OPEN-QUESTIONS.md`.
- `activate.sh` / `rollback.sh`: a Codex agent copy is recognised by its generator banner so a
  regenerated adapter can be refreshed and removed (defect found today).

### Verification

- `pilot/content-workflow/tests/test_readiness.py`: 74 of 74 pass (55 pre-existing unchanged in
  intent, 19 new: research stage and offline refusal; missing, reused, stale, and timestamp-only
  evidence; fetch-tool refusals; unavailable authority at live check; changed law and marker-only
  drift at live check; wrong jurisdiction and neutral-label bypass; future-effective and proposed
  legislation; legal rows without evidence; unsupported client claims; incorrect citation URL;
  page-bound currency or declared reason; excerpt must be operative text of the cited section;
  link destinations need direct records; nonce rotation; `max_age_days` boundary; fixture flag
  type; unreadable export and render-wrapper failure; research ledger in the delivery). The seven
  tests added after the independent review answer its M2, M4, M9, M10, and O1 items. Fixtures use a local HTTP server and fictional statutes under
  `tests/fixtures/valid-run/research-pages/`; the URL rewrite is honoured only for `fixture: true`.
- Baseline suites unchanged and passing: hook tests 8 and 6; candidate situational suite 38.
- Fresh client run (Git-ignored `runs/sterling-fl-m008-wisconsin-2026-09-24-integration/`): 13 live
  retrievals; INTAKE-COMPLETE; RESEARCH-COMPLETE with every record live-verified. Controlled refusal
  run: failed bill, out-of-state statute, and nonexistent section refused with the intended codes.
- Disposable checkout (`git worktree` plus the working changes): activation created exactly eight
  Git-ignored entries; adapter check, hook tests, and candidate suite passed; the readiness suite
  failed only where rendering needs the Git-ignored LibreOffice and PyMuPDF installs; a foreign
  `.codex/agents` file was refused by activation and left by rollback; full rollback removed all
  eight entries with a clean `git status`.

### Limits

- The rule outside the pilot is instruction-only; nothing mechanically checks a standalone skill
  invocation's research. The reviewer treats a claim without current retrieval evidence as
  unverified.
- The fetch tool proves retrieval, not that a page supports a claim; excerpt selection remains a
  judgment, and a reviewer can quote the coordinator's excerpt without reading further.
- `research_fetch.py` uses this machine's Python TLS trust: revisor.mn.gov fails the handshake under
  Homebrew Python 3.14 / OpenSSL 3.6.3 (system Python and curl succeed), legislature.mi.gov's
  chain does not validate, ilga.gov returns 403 to automated clients, and PDF authorities are not
  extracted. Each fails closed (`RESEARCH_UNAVAILABLE`); none is bypassed.
- Codex headless `legal_reviewer` could not fetch under the read-only sandbox and correctly returned
  `Unverifiable`; live research on Codex is unverified on this host. The interactive Codex session
  remains untested.
