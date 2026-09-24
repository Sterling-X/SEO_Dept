---
name: content-workflow
description: Pilot content-production workflow coordinator for one client page (situational-page route first). Runs the intake gate, dispatches the content-writer, legal-reviewer, and editorial-reviewer agents, records hash-bound structured reviews, enforces at most two repair rounds, and delivers only when the deterministic readiness check passes. Explicit invocation only; not the production default.
disable-model-invocation: true
---

# Content workflow (pilot v1)

You are the coordinator: the primary SEO Strategist conversation. `AGENTS.md` governs
everything it covers. The pilot rules are in
`pilot/content-workflow/canonical/workflow-rules.md`; read that file and
`pilot/content-workflow/canonical/review-findings-schema.md` before the first dispatch.

This skill is a pilot. It does not replace the production skills, does not promote
lessons into `AGENTS.md`, and is invoked only explicitly (`/content-workflow` in Claude
Code, `$content-workflow` in Codex).

## Host mapping

| Step | Claude Code | Codex |
|---|---|---|
| Writer | `Agent` tool, `subagent_type: content-writer` (`.claude/agents/content-writer.md`) | spawn custom agent `content_writer` (`.codex/agents/content_writer.toml`) |
| Legal reviewer | `subagent_type: legal-reviewer` | custom agent `legal_reviewer` |
| Editorial reviewer | `subagent_type: editorial-reviewer` | custom agent `editorial_reviewer` |
| Independent strategy review (unchanged) | `seo-reviewer` | `seo_reviewer` |
| Scripts | `Bash` | shell |

All agent files are generated adapters of `pilot/content-workflow/canonical/roles/`. If
an agent type is not available, activation has not happened in this session; follow
`pilot/content-workflow/README.md` "Activation" and start a fresh session. Do not
impersonate a role inline as a substitute.

## Arguments

The text after the command, if any, names the run directory. Otherwise create one:
`pilot/content-workflow/runs/<client-slug>-<node-or-topic>-<YYYY-MM-DD>/`. (Claude Code
substitutes `$ARGUMENTS`; Codex shows the typed text; both hosts pass it in the same place.)

## Procedure

### 0. Frame and recall

Frame the assignment per `AGENTS.md` (client, domain, page role, jurisdiction,
deliverable, evidence, authorized changes). Perform the room-filtered MemPalace recall
`AGENTS.md` requires. Load only the client brief in scope.

### 1. Intake gate

Write `run.json` (schema `pilot/content-workflow/canonical/schemas/run.schema.json`):
client name, domain, slug; jurisdiction; page type and architecture node; every skill the
run will use pinned by path and SHA-256 (candidate skills live under
`pilot/content-workflow/candidates/skills/`); every source pinned by run-relative path
and SHA-256 (approved client facts, voice brief when the domain is unrouted, legal
source notes with URLs and verification dates); the voice route; the expected citations;
required reviews; `rounds.max_repair_rounds` (2 or fewer); and, under `export.validators`, every
validator the pinned page-writing skill declares in its `pilot-manifest.json`, by name (the
situational candidate declares `structural` and `page`; their commands take the export path and
`<run>/manifest.json`). The intake gate reports `VALIDATORS_UNDECLARED` until they are declared.

```bash
python3 pilot/content-workflow/scripts/pin.py <run-dir> --skills <path-to-SKILL.md>... --sources <run-relative path>...
python3 pilot/content-workflow/scripts/readiness_check.py <run-dir> --stage intake
```

Any `INCOMPLETE` reason stops the affected work. Report the missing item; do not draft
around it.

### 1b. Pre-draft legal verification (family-law pages)

List every material legal claim the page will need (jurisdiction, posture, authority). Dispatch the
legal reviewer with `stage: predraft` and the pinned sources; it verifies each planned claim live
and returns a Verification Log with a row per claim. Record it:

```bash
python3 pilot/content-workflow/scripts/record_review.py <run-dir> --input <predraft.json> --runtime claude --agent legal-reviewer --stage predraft --round 0
```

Then write the `Confirmed` authorities into `run.json` `citations` (one identity per URL; more than
six needs `citations_ceiling_rationale`) and pin the legal source notes. The writer may draft only
`Confirmed` claims. Any `Unverifiable` or `Correction-needed` row blocks the run until resolved.

### 2. Draft with checkpoints (required)

Dispatch the writer with: the run directory, the pinned skill path, the single voice
source, the approved client facts path, the pinned legal sources, and the instruction to
write only inside the run directory, to save the generator manifest as `<run>/manifest.json`, and
to render `draft.md` from it with `scripts/render_draft.py`. When the checkpoint draft exists, dispatch the
legal reviewer and the editorial reviewer in parallel with: the run directory, the draft
path, the pinned sources, the canonical findings schema, and `stage: checkpoint`.

Record each returned JSON immediately, before anything else changes:

```bash
python3 pilot/content-workflow/scripts/record_review.py <run-dir> --input <findings.json> --runtime claude --agent legal-reviewer --stage checkpoint --round 0
```

(`--runtime codex --agent legal_reviewer` in Codex.) The recorder verifies every quoted
passage exists in the draft and stamps the draft, export, and source hashes.

Return findings to the writer by id. The writer logs changes in `changes.md` and never
marks anything fixed-verified.

Both checkpoints are required for family-law pages; there is no skip.

### 3. Final review of the complete revised document

When the writer reports the complete revised draft and export, dispatch the legal
reviewer and the editorial reviewer on the full document (`stage: final`, `round: 0`),
then run mechanical QA:

```bash
python3 pilot/content-workflow/scripts/mechanical_qa.py <run-dir> --round 0
```

### 3b. Render and inspect every page

```bash
python3 pilot/content-workflow/scripts/render_inspect.py <run-dir> --round 0 --render
```

View every `render/r0/page-N.png` at rendered resolution (Claude: the Read tool on each image; a
human inspector otherwise). Write an attestation JSON with a specific observation per page and a
`pass` or `fail` verdict, then:

```bash
python3 pilot/content-workflow/scripts/render_inspect.py <run-dir> --round 0 --attest <attestation.json>
```

The record is bound to the exact export hash; a re-export requires a new render and inspection.

### 4. Repair and recheck (at most two rounds)

If any blocking or major finding is open, or a legal or editorial verdict is `not-ready`, or
the legal Verification Log has an `Unverifiable` or `Correction-needed` row: writer repairs
against finding ids, then every required role rechecks the revised document (`--round 1`,
then `--round 2`), because the new draft hash stales every record. Re-run
`mechanical_qa.py` at the same round.
A reviewer sets `fixed-verified` only after re-reading the revised passage; you never set
it for them. After round 2 stop repairing and report what remains.

`coordinator-accepted` is available for `major` findings only, outside the protected categories
(`legal-accuracy`, `citation`, `client-fact`, `promise`), with a written rationale, and is recorded
with `python3 pilot/content-workflow/scripts/dispose_finding.py <run-dir> --role <role> --id <id>
--accept --rationale "..."` (never by editing a reviewer's record). Never use it on a blocking
finding or on a legal or client-fact error; those close only when the raising reviewer re-reads the
corrected passage and records it in `corrected_text`. Preserve `disputed` findings.

### 5. Deliver

```bash
python3 pilot/content-workflow/scripts/deliver.py <run-dir>
```

`READY` copies the export and readiness report to `pilot/content-workflow/deliveries/`.
`INCOMPLETE` copies nothing and lists reason codes. Delivery executes the declared validators
against the exported file; it cannot be skipped. Do not hand-edit records to reach
`READY`; fix the underlying problem or report `INCOMPLETE`.

### 6. Independent review and learning pass

For a client-facing deliverable, run the read-only `seo-reviewer` / `seo_reviewer` on
the final artifact and supporting record as `AGENTS.md` requires, and resolve its
findings against evidence. Then run the single learning pass. Record pilot lessons in
`pilot/content-workflow/docs/CHANGES-AND-OPEN-QUESTIONS.md`; do not promote them into
production instructions from inside a run.

## What the tooling proves and does not prove

The readiness check proves hashes, presence, citation pairing, placeholder absence,
parity, record shape, currency, and round limits. It records but cannot verify legal or
editorial judgment. Say so in every delivery summary. Attorney review before publication
remains required for legal content.
