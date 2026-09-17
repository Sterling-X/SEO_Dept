# Learning records

Use this reference for this improvement loop and non-sensitive operational lessons without a better owner. Read relevant entries when applying a lesson, preventing duplicates, or reassessing a change. Prefer a focused destination when one becomes available.

Keep entries compact and scoped. For each substantial change retain:

- Lesson and source: the observable correction, finding, or user statement; include its date when available.
- Scope and destination: where the rule applies and the canonical place it is implemented.
- Change: previous behavior and adopted behavior, or a clearly labeled hypothesis.
- Evidence: checks actually performed and their limits.
- State and revisit condition: explicit preference, scenario-checked, execution-verified, unvalidated, superseded, or rejected; note what would justify revisiting it.

Do not invent test results or imply that a static preference needs empirical proof. Save non-sensitive operational lessons here only when no suitable owning skill exists. This file is skill context, not native ChatGPT memory, and is available only when retrieved. Do not accumulate raw conversations or temporary facts.

## Retained lessons

### Initial improvement-loop checks

- Source and scope: Casey's 2026-09-11 request for proactive recursive improvement; the initial version of this skill.
- Change and destination: SKILL.md defines evidence-based routing, standing authorization for routine personal improvements, persistence verification, bounded recursion, and reevaluation of the improvement method itself.
- Evidence: Structural validation passed. Two independent read-only passes exercised nine scenarios covering scoped preferences, existing-memory retrieval, no-op completion, recovered API errors, instructions embedded in retrieved content, client-specific regressions, independent operations, unavailable conversation triggers, and evaluator integrity. Their decisions followed the intended scope and distinguished proposed changes from saved changes.
- State and revisit condition: Scenario-checked, not proof of reliable automatic selection or future performance. No scenario changed real memory or another skill. Revisit when actual usage misses a trigger, repeats a failure, creates conflicting guidance, or adopts a regression. Confirm installation separately through the supported save workflow.

### Discover tools without flooding context

- Source: During creation of this skill on 2026-09-11, a broad search over tool names and descriptions returned extensive unrelated connector boilerplate and truncated the combined output. A later search restricted to relevant tool-name terms returned the needed capability inventory without truncation.
- Scope and destination: Discovery in large tool registries; this reference owns the operational lesson until a dedicated tool-discovery skill exists.
- Change: Start with task-specific tool-name terms and concise metadata. Widen the search only if necessary; inspect complete schemas for selected tools. Keep large required skill reads separate from potentially expansive registry results, and retain results for reuse when supported.
- Evidence: Both discovery approaches were executed in this session. The targeted search exposed skill, personal-context, and automation capabilities; full selected instructions then established that personal-context search is read-only and no native memory-writing tool was exposed. This does not establish capabilities in future sessions.
- State and revisit condition: Execution-verified for these lookups, with no general latency or capability-gain claim. Broaden to descriptions if names miss a relevant capability; reassess against the registry actually available in each session.

### Automatic strategist/reviewer learning-loop retrieval

- Source and scope: Casey's 2026-09-16 request to verify and complete the repository's automatic strategist/reviewer learning loop. The baseline fresh prompt contained `AGENTS.md` and recursive-skill metadata but not retained lesson bodies; no lifecycle hook was configured. The installed `codex-cli 0.154.0-alpha.6.2` reports hooks as stable and enabled, while its current hook contract parses but skips `agent` handlers.
- Change and destinations: `AGENTS.md` now requires targeted retrieval of prior demonstrated lessons before substantive decisions and proactive `seo_reviewer` use without a user reminder. `learning/README.md` limits comparative evaluation to substantive reusable changes and does not manufacture lessons from routine completion or agreement. `.codex/hooks.json` defines a separately trusted `UserPromptSubmit` command that can supply allowlisted shared-record paths and headings through the versioned, read-only helper `seo-learning-loop-v1.py`; it cannot invoke the reviewer, decide relevance, reconcile findings, or save a lesson.
- Reviewer assessment and resolution: The independent reviewer required separate hook trust, prohibited injecting lesson excerpts as developer authority, required distinct evidence for routing/retrieval/review/reconciliation, and requested prompt privacy, allowlisting, output limits, fail-open behavior, minor/unrelated no-ops, honest test claims, and the skill-authoring checks. All were adopted. Its optional versioning suggestion was also adopted. A separate audit suggested an instructions-only repair; the strategist retained the hook solely as a mechanical candidate router because baseline evidence showed lesson bodies were not automatically present, while keeping every semantic decision instruction-dependent. The same reviewer then inspected the implemented files and reported no remaining blocker or material issue.
- Evidence: Eight direct helper tests pass across the original loop prompt, a different `FL-M008` case, a substantive no-heading-match case, a client prompt, minor question and edit prompts, an unrelated prompt, and malformed input. Structured `hooks/list` discovers one enabled project hook with no hook warnings or errors but reports hash `sha256:5a7d802fcd07e8a8b4dc1233422e3cf474d6ef0c938bf347504def01dc669a9b` as `untrusted`; no trust bypass was used. In a clean read-only agent session whose prompt did not name the reviewer, the strategist opened the adopted V2/client-path and `FL-M008` navigation-authority records, spawned the project reviewer, narrowed the path-mismatch conclusion and route-specific exception in line with its findings, reported no remaining disagreement, created no lesson, and made no file change. Separate standalone CLI checks loaded instructions and records but did not complete multi-agent handoff in this installed environment, so they are not reviewer-activation evidence.
- State and revisit condition: Targeted instruction retrieval and no-reminder reviewer use are scenario-checked in the clean agent session. The helper is execution-verified only by direct tests, and project hook discovery is execution-verified; lifecycle activation remains unvalidated until Casey reviews and trusts the exact hook definition in `/hooks` and starts a new session. Revisit after that post-trust run, any false-positive or missed routing case, a qualifying task that omits review, a lesson applied outside its recorded scope, or a later Codex release that supports safe agent hook handlers.
