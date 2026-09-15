# Shared SEO Skills

Portable project skills are stored as folders under:

```text
.agents/skills/<skill-name>/SKILL.md
```

Each skill may include its own `scripts/`, `references/`, `assets/`, or other supporting resources. Keep a skill narrowly scoped, document when it should trigger, and avoid embedding client-specific confidential data in a portable skill.

The unchanged SEO transfer was imported on 2026-09-15: 14 skills, 67 payload files, and 504,131 payload bytes. All 67 destination files match their declared source sizes and SHA-256 hashes. See [the import report](../../docs/seo-skill-import-report.md) for the inventory and [the compatibility contract](../../docs/seo-skill-compatibility.md) before using a workflow.

Four source workflows remain incomplete: `family-law-service-pages`, `family-law-situational-pages`, `family-law-service-area-seo`, and `cluster-blog-writer`. Their exact missing dependencies and repair order are recorded in the compatibility document. Do not claim their absent validations passed.

Client voice is explicitly routed by domain:

- `sterlinglawyers.com` → `sterling-voice`
- `jmblattner.com` → `write-blattner-voice`
- `servicecu.org` → `servicecu-voice`

## Verify installation and discovery

Actual discovery was checked with `codex-cli 0.154.0-alpha.6.2` on 2026-09-15:

- a structured resolver reload returned all 14 skills as repository-scoped and enabled, with zero list errors; and
- a fresh model-prompt render included all 14 imported names and descriptions.

All imported `agents/openai.yaml` files warn on the unsupported `api` product value in this Codex build. That optional interface metadata is ignored, but all 14 core `SKILL.md` entrypoints are discovered. The imported metadata remains unchanged so any compatibility repair can be reviewed separately.

For later versions or sessions:

1. Confirm the folder contains a readable `SKILL.md` at the path above.
2. Reload skills or start a fresh Codex conversation in this repository.
3. Confirm the expected repository skill appears in structured discovery and in the model-visible skill list.
4. Separately test the matched workflow and every required capability; discovery does not prove execution.

Finding a `SKILL.md` on disk confirms file presence only. Resolver and model-visible listings confirm discovery; they do not confirm correct triggering, dependency availability, output quality, or SEO performance.
