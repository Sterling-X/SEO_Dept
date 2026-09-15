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
