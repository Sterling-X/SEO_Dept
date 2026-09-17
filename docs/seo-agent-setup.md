# SEO Agent Setup

Use this guide for everyday assignments. `AGENTS.md` governs agent behavior, and `docs/seo-skill-compatibility.md` is the current capability authority.

## Give the agents an assignment

Open a Codex conversation at the repository root and paste the fields that matter. Omit what is genuinely unknown; the strategist should reuse existing evidence, make reasonable in-scope decisions, and ask only when an answer would materially change the decision or block required work.

```text
Client: [name and domain]
Outcome: [decision, diagnosis, plan, draft, or other deliverable]
Page or site role: [URL, section, page type, architecture node, jurisdiction]
Evidence: [files, exports, URLs, date ranges, prior records]
Deliverable: [format and save location]
Allowed changes: [read-only, or the files/systems the agents may change]
Constraints: [scope limits, claims to avoid, URLs to retain, prohibited actions]
Git and publication: [use repository default, or explicitly prohibit commit/push/publication]
Success checks: [review, legal, data, links, render, or other required QA]
```

Explicit task constraints override repository defaults. Always complete **Git and publication**: `AGENTS.md` currently defaults completed tasks to commit and push unless the assignment says otherwise. State website, application, or external-account authority when relevant.

## Everyday workflow

1. Identify the outcome, client, page role, relevant skills, evidence, governing sources, and known compatibility limits. For substantive work, retrieve only prior demonstrated lessons that match the task and confirm their recorded scope and state. Check for conflicting instructions before proceeding.
2. Complete the in-scope work supported by the evidence. Verify changing facts and label missing facts or measures as unknown, not zero.
3. Proactively use the read-only `seo_reviewer` for substantive strategy, architecture, causal diagnosis, workflow changes, and client-facing deliverables; the assignment does not need to name it. The strategist adjudicates findings against evidence, makes final edits, and reports unresolved disagreement. Follow the task's review cap; otherwise use no more than two focused repair and recheck rounds.
4. Run the applicable factual, legal, calculation, mechanical, link, and rendered-output checks. A mechanical pass is not legal, strategic, or performance proof.
5. Return the deliverable, a concise verification summary, and only the remaining decisions that require user attention.

## Automation boundaries

| Mechanism | What it does | Boundary |
|---|---|---|
| `AGENTS.md` and matching skill metadata | Load on a new Codex run and instruct targeted lesson retrieval, substantive review, reconciliation, persistence, and later reuse. | These are model instructions. They do not prove the right lesson was selected or the reviewer was invoked on every qualifying task. |
| Project `UserPromptSubmit` hook | After its exact definition is trusted, a read-only helper filters likely substantive SEO prompts and supplies allowlisted shared-record paths and section headings as candidate pointers. | It does not inject lesson text, read client files or transcripts, log prompts, invoke an agent, decide relevance, or save a lesson. |
| `.codex/agents/seo-reviewer.toml` | Defines the independent reviewer as read-only and prohibits it from spawning agents. | Codex currently skips `agent` hook handlers, so reviewer invocation and strategist reconciliation remain instruction- and model-dependent. |
| Repository records | Preserve approved corrections with provenance, scope, state, checks, and revisit conditions. | Persistence is a file change, not model-weight training, native memory, or an always-running service. |

### Activate the project hook

Start an interactive Codex CLI session at this repository root, enter `/hooks`, inspect the command from `.codex/hooks.json`, and trust that exact non-managed hook definition. Then start a new conversation or reload the IDE session. Project trust does not replace hook-definition trust, and a changed definition must be reviewed again. Future helper behavior changes must use a new versioned filename and update the hook definition instead of silently modifying a trusted target. Do not bypass this review with `--dangerously-bypass-hook-trust`.

Until that step is completed, Codex skips the executable candidate router. The `AGENTS.md` workflow still loads in a fresh repository session and remains the authority for lesson retrieval and reviewer use.

## Copy-and-paste examples

### Prioritize an SEO cluster

```text
Client: [client and domain]
Outcome: Recommend the next five actions for the [topic] cluster; do not write pages yet.
Page or site role: [hub and relevant child pages]
Evidence: Use the existing client record, architecture, page evidence, and supplied performance files.
Deliverable: A concise prioritized plan with evidence, dependencies, hypotheses, and success signals.
Allowed changes: Save the plan under [path]; do not change the website or application.
Constraints: Do not invent demand, traffic, lead, or revenue evidence. No broad crawl.
Git and publication: Do not commit, push, or publish.
Success checks: Have seo_reviewer assess the priorities independently and reconcile material disagreements.
```

### Produce a tested family-law Core Hub draft

```text
Client: [firm and domain]
Outcome: Produce a proposed replacement for [current URL].
Page or site role: [V2 Core Practice-Area Hub node], [jurisdiction]. Retain the implementation URL.
Evidence: Current page, verified client material, governing V2 architecture, and current official legal sources.
Deliverable: One DOCX and one concise supporting record.
Allowed changes: Create or revise only the scoped deliverable and its supporting record.
Constraints: Use only supported client claims. No live-site or application change.
Git and publication: Do not commit, push, or publish.
Success checks: Run the Core Hub workflow, seo_reviewer, legal QA, link checks, document validation, and fresh render inspection.
```

### Diagnose a lead decline

```text
Client: [client and domain]
Outcome: Diagnose the reported organic lead decline and prioritize the next checks or fixes.
Evidence: Supplied GSC, GA4, call/form, and CRM or intake records for [date ranges], including known tracking changes.
Deliverable: A decision memo separating observations, hypotheses, recommendations, and tests.
Allowed changes: Read-only analysis; save only the requested memo.
Constraints: Treat unavailable stages as unknown. Do not change tracking, the website, or source data.
Git and publication: Do not commit, push, or publish.
Success checks: Verify material calculations and have seo_reviewer challenge causality, scope, and priority.
```

## Context the strategist uses

- `AGENTS.md`: role, precedence, operating rules, review, and completion.
- `context/casey.md` and `context/seo-principles.md`: working preferences and cross-client principles.
- `clients/`: only the relevant curated client brief, when one exists; task-specific supporting records remain evidence, not a substitute for a verified brief.
- `.agents/skills/`: only skills matching the assignment.
- `docs/seo-skill-compatibility.md`: current readiness and dependency limits.
- `docs/seo-skill-local-adaptations.md`: attributable changes to imported skills.
- `learning/README.md` and matching retained records: evidence-based correction, validation, and later-retrieval rules.
- Family-law V2 summary and governing HTML: classification, hierarchy, and explicit relationships when applicable.

## Current capability table

Snapshot: 2026-09-16. **Tested** means the exact bounded workflow has reproducible evidence. **Limited** means useful instructions or a task-specific implementation exists but generalized readiness has not been established. **Incomplete** means a required dependency or tested branch is missing.

| Status | Workflow | Supported now | Honest boundary |
|---|---|---|---|
| Tested, bounded | Strategist → `seo_reviewer` → strategist reconciliation | Read-only handoff, categorized findings, evidence-based resolution, and preserved review records have been exercised. | Proves coordination, not universal SEO correctness, business impact, or performance. |
| Limited, hook-assisted | Prior-lesson candidate routing | A read-only `UserPromptSubmit` helper has focused tests for substantive, minor, unrelated, malformed, matching, and no-match prompts. | Lifecycle execution requires separate hook trust. Candidate routing does not prove relevance, reviewer invocation, reconciliation, or lesson validity. |
| Tested, bounded | Family-law Core Practice-Area Hub DOCX | Core generator, V2/manifest checks, validators, regressions, hyperlinks, fresh rendering, and production draft review have run. | Core Hub branch only. Every assignment still needs current client, legal, voice, destination, reviewer, and human-render evidence. Procedural is incomplete. |
| Limited implementation, tested for one node | `FL-M008` High-Conflict Divorce Situational DOCX | Separate local generator, schema, validators, 21 regressions, legal/reviewer gates, navigation checks, and render inspection. | `FL-M008` only; this is a labeled local replacement, not readiness for another Situational node. |
| Limited, assignment-specific | General SEO strategy, paid landing-page strategy, red-team review, AI-first writing, recursive improvement, and voice references | Instructions and references are discoverable and may support scoped work. | General local execution, external capabilities, or output readiness remain unverified; changing client facts still require evidence. |
| Limited, assignment-specific | Mechanical and legal-content QA | Available tools and current primary sources have supported completed client drafts. | Mechanical QA is not editorial or legal clearance. Legal QA requires live primary authority on every run and attorney review before publication. |
| Incomplete | Family-law Procedural pages, Situational nodes other than `FL-M008`, service-area production, and clustered-blog production | May inform analysis and scoping. | Missing or untested route-specific templates, validators, dependencies, or contracts prevent a claimed finished-document workflow. |
| Limited supporting evidence | Reporting imports and deterministic application QA | Supplied Semrush and GSC exports can support normalized inputs, calculations, exclusions, and data-health evidence. | No automatic access to absent metrics; deterministic checks do not establish causality, intent, geography, priority, or business impact. |

Use `docs/seo-skill-compatibility.md` for the detailed, current skill-by-skill contract rather than copying this snapshot into another record.

## How corrections are saved and checked

Classify a correction before retaining it:

- **Verified client fact:** Save it in the relevant client brief or assignment record with source, date, and scope; recheck facts that can change.
- **Hypothesis or client-specific decision:** Keep it explicitly labeled in the assignment record. Do not promote it to a shared rule without evidence.
- **Demonstrated reusable correction:** Update the smallest owning instruction, skill, reference, template, validator, or compatibility record. Preserve the trigger, provenance, prior and corrected behavior, scope, checks, limits, and revisit condition. Record imported-skill divergences in `docs/seo-skill-local-adaptations.md`; use the recursive skill's learning record only when no clearer owner exists.

Before adopting a reusable correction, check the current request, `AGENTS.md`, relevant client context, governing architecture, compatibility notes, and owning skill for conflicts or duplication. Follow `learning/README.md`: use independent review, keep criteria fixed, and check the original case, a different relevant case, and an unaffected case. Limit repair to two additional rounds and preserve unresolved findings.

Verify persistence by reading back the saved rule and rerunning affected checks. On a later relevant task, reload the owning skill and compatibility record, compare actual behavior with the intended correction, and narrow, supersede, or retire the rule if new evidence conflicts. Repository records are not model training, native ChatGPT memory, or a background learning service.
