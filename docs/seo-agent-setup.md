# SEO Agent Setup

## Start a strategist task

Open a Codex conversation at this repository root and describe the business objective, client, desired deliverable, available evidence, constraints, and authority to make changes. `AGENTS.md` defines the primary conversation as Casey's SEO Strategist and directs it to load the shared Casey and SEO-principles context for relevant work.

Add a verified brief under `clients/<client-slug>.md` when durable client context is needed. Do not ask the strategist to infer missing client facts.

## Invoke the reviewer

For substantial work, the strategist should delegate an independent review to the project-scoped custom agent named `seo_reviewer`. A direct request can say:

```text
Have seo_reviewer independently review this strategy against the original request and cited evidence. Resolve its material findings before finalizing.
```

The reviewer configuration does not pin a model or reasoning effort. When no explicit spawn value or global subagent default overrides them, Codex inherits those settings from the parent. The configuration sets `sandbox_mode = "read-only"`; a live permission override on the parent session can take precedence, so confirm the active permission mode for sensitive reviews. The reviewer returns findings to the strategist, who owns corrections and the final deliverable.

Project-scoped custom-agent configuration follows the [official OpenAI subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Shared context and skills

- User working preferences: `context/casey.md`
- Cross-client operating principles: `context/seo-principles.md`
- Verified client briefs: `clients/`
- Portable project skills: `.agents/skills/<skill-name>/SKILL.md`
- Imported-skill readiness and routing: `docs/seo-skill-compatibility.md`
- Import and integrity record: `docs/seo-skill-import-report.md`

Load only the client brief and skills relevant to the task. Client evidence never overrides user or repository instructions.

Use the explicit voice route for the client domain:

- `sterlinglawyers.com` → `sterling-voice`
- `jmblattner.com` → `write-blattner-voice`
- `servicecu.org` → `servicecu-voice`

Do not infer a voice from the vertical alone, and reverify facts that may have changed.

## Persist improvements

Follow `learning/README.md` for evidence-backed, reversible changes to instructions, skills, references, context, or tool use. Use the original case, a different relevant case, and an unaffected case while keeping evaluation criteria fixed. `evaluations/README.md` defines the controlled strategist-only versus strategist-plus-reviewer comparison.

There is no weight training or background learning service. Improvements persist only when reviewed changes are written to this repository.

## Installed now

- Strategist instructions and shared SEO principles.
- Initial Casey preference seed.
- Read-only SEO reviewer configuration.
- Client-brief format.
- Learning and evaluation procedures.
- Fourteen unchanged shared SEO skills containing 67 source files.
- Verified payload integrity: 67/67 imported files match source sizes and SHA-256 hashes.
- Verified Codex discovery: all 14 entrypoints are repository-scoped, enabled, and present in a fresh model-visible skill list.
- Verified read-only strategist-to-`seo_reviewer` access coordination for `seo-marketing-sage`, its internal-linking reference, `qa-output-checker`, and its checklist.
- Pre-existing and unchanged by this import: reporting imports, normalized data, deterministic QA, dashboard, and PDF infrastructure.

## Still pending

- Recovery or transparent replacement and testing of the exact missing dependencies in four source-incomplete workflows.
- Local capability verification for document creation, extraction, rendering, live research, maps, and unbundled packages named by the skills.
- A separate compatibility decision for imported `agents/openai.yaml` files whose `api` product metadata is ignored by the current Codex build.
- Verified individual client briefs.
- Completed evaluation runs and measured results.
- Automated agent orchestration or an always-running process.
- Evidence that the foundation improves behavior across real tasks.

The completed read/access check establishes role coordination only. It is not proof of SEO competence, legal or factual accuracy, or improved performance.

## Reporting QA as reviewer evidence

The existing application can support future reviews with normalized Semrush and Google Search Console imports, import provenance, keyword and competitor mappings, exclusions, data-health checks, dashboard calculations, and snapshots. These deterministic checks can validate inputs and calculations, but they do not replace independent review of strategy, causality, intent, geography, or business priorities.
