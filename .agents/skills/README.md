# Shared SEO Skills

Portable project skills are stored as folders under:

```text
.agents/skills/<skill-name>/SKILL.md
```

Each skill may include its own `scripts/`, `references/`, `assets/`, or other supporting resources. Keep a skill narrowly scoped, document when it should trigger, and avoid embedding client-specific confidential data in a portable skill.

The unchanged SEO transfer was imported on 2026-09-15: 14 skills, 67 payload files, and 504,131 payload bytes. Baseline commit `9d8e07f` preserves all 67 files at their verified source hashes. Fourteen metadata files were adapted afterward for this Codex build; see [the local adaptation log](../../docs/seo-skill-local-adaptations.md). Read [the import report](../../docs/seo-skill-import-report.md) and [the compatibility contract](../../docs/seo-skill-compatibility.md) before using a workflow.

Four imported source packages were incomplete. The Core Practice-Area Hub branch of `family-law-service-pages` now has a separately documented and tested local repair, including a genuine recovered page validator; its Procedural branch remains pending. `family-law-situational-pages`, `family-law-service-area-seo`, and `cluster-blog-writer` remain incomplete. See the compatibility document for exact status and do not extend the Core result to any pending branch.

Client voice is explicitly routed by domain:

- `sterlinglawyers.com` → `sterling-voice`
- `jmblattner.com` → `write-blattner-voice`
- `servicecu.org` → `servicecu-voice`

## Verify installation and discovery

Actual discovery was checked with `codex-cli 0.154.0-alpha.6.2` on 2026-09-15:

- a structured resolver reload returned all 14 skills as repository-scoped and enabled, with zero list errors; and
- a fresh model-prompt render included all 14 imported names and descriptions.

The original `agents/openai.yaml` files warned on unsupported product value `api`. The local adaptation removed only that value. Current verification returns all 14 interface objects and zero repository metadata warnings while preserving `allow_implicit_invocation: true` in every skill.

For later versions or sessions:

1. Confirm the folder contains a readable `SKILL.md` at the path above.
2. Reload skills or start a fresh Codex conversation in this repository.
3. Confirm the expected repository skill appears in structured discovery and in the model-visible skill list.
4. Separately test the matched workflow and every required capability; discovery does not prove execution.

Finding a `SKILL.md` on disk confirms file presence only. Resolver and model-visible listings confirm discovery; they do not confirm correct triggering, dependency availability, output quality, or SEO performance.
