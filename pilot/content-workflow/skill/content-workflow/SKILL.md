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
python3 pilot/content-workflow/scripts/research_fetch.py <run-dir> --init          # issues the run's research nonce; nothing retrieved earlier counts
python3 pilot/content-workflow/scripts/pin.py <run-dir> --skills <path-to-SKILL.md>... --sources <run-relative path>...
python3 pilot/content-workflow/scripts/readiness_check.py <run-dir> --stage intake
```

Any `INCOMPLETE` reason stops the affected work. Report the missing item; do not draft
around it.

### 1a. Current-source research (required on every run; research first, never a placeholder first)

Before any claim is planned or drafted, retrieve every source the page will rely on, during this
run, with the fetch tool. Nothing else counts: not a prior run's `sources/` notes, not an earlier
review, not memory, not the voice skill (brand guidance governs voice and proves no fact).

- For each legal authority: `--kind legal-authority`, the official URL, a verbatim `--excerpt` (40+
  characters of the operative text), `--jurisdiction`, `--authority`, `--legislation-status`
  (`effective` is the only status that can support a claim of current law), the page's own
  `--currency-marker` (its "current through" or "published" statement; required, or
  `--no-currency-marker "<why the page states none>"`), `--current-through-date` (the compilation
  date that marker states), `--effective-date` only when the page states the provision's own
  effective date, and `--amendments` (the section's own History line). Check exceptions and
  companion sections while the page is open. Jurisdiction and status are your declarations; the
  gate checks them for consistency, the legal reviewer for correctness.
- For the approved client facts: retrieve each first-party page the facts rest on (services,
  pricing, locations, credentials, contact route, statistics) with `--kind client-fact` and list
  their ids in the `client-facts` source's `evidence_ids`. For link destinations use
  `--kind link-destination`.
- For court procedures and filing fees: the court's or clerk's official page, `--kind
  legal-authority` or `--kind other`, with the fee or procedure text as the excerpt.

```bash
python3 pilot/content-workflow/scripts/research_fetch.py <run-dir> --id EV1 --url <official URL> --kind legal-authority --source-id S1 \
  --excerpt "<verbatim operative text>" --jurisdiction "<state>" --authority "<citation>" --legislation-status effective \
  --current-through-date YYYY-MM-DD --currency-marker "<the page's current-through statement>" --amendments "<the section's own History line>" --supports C1
python3 pilot/content-workflow/scripts/research_fetch.py <run-dir> --id EV9 --url <first-party page> --kind client-fact --source-id client-facts --excerpt "<verbatim fact text>"
python3 pilot/content-workflow/scripts/readiness_check.py <run-dir> --stage research     # offline rules plus a live re-fetch of every record
```

The tool writes a record only when the page returned HTTP 200 now and the excerpt (and marker)
are on it, a section identifier from `--authority` appears in the text, and the excerpt is not the
marker. A refusal means the fact is unverified: report the affected work as `INCOMPLETE` and do
not draft, cite, or placeholder around it. The research stage must report `RESEARCH-COMPLETE`
before the pre-draft dispatch.

Two practices learned on windowed legislature sites (docs.legis.wisconsin.gov, 2026-09-24):

- Take `--amendments` from the section's own History line, the `History:` line that follows the
  `<section> History` marker in the retrieved text, never the first `History:` in the page (that
  is a neighbouring section's). When the rendered window does not reach the marker, omit the note
  and say so in `--notes`; the tool refuses a note that is not in the retrieved text.
- A long section is served as a window that omits later subsections. If a planned claim rests on
  a subsection that is not in the record's `.txt`, retrieve the subsection-anchored URL as its own
  record (for example `/document/statutes/767.41(5)(am)`) so the reviewer can quote it; the legal
  reviewer records `Flagged` with a record request until that exists.

### 1b. Pre-draft legal verification (family-law pages)

List every material legal claim the page will need (jurisdiction, posture, authority). Dispatch the
legal reviewer with `stage: predraft`, the pinned sources, and the research records (`research/`);
it fetches each authority itself, verifies each planned claim live, and returns a Verification Log
with a row per claim that names the `evidence_id` and quotes a verbatim `excerpt` of the retrieved
text, with jurisdiction, currency, amendments, exceptions, and legislation status in `notes`.
Record it:

```bash
python3 pilot/content-workflow/scripts/record_review.py <run-dir> --input <predraft.json> --runtime claude --agent legal-reviewer --stage predraft --round 0
```

The recorder refuses a verified row that names no record from this run, quotes text that is not in
it, cites a URL the record did not retrieve, or carries an access date from before the day the run's research opened.
Then write the `Confirmed` authorities into `run.json` `citations` (one identity per URL; more than
six needs `citations_ceiling_rationale`) and pin the legal source notes (which point at the records;
they are not evidence themselves). The writer may draft only `Confirmed` claims. Any `Unverifiable`
or `Correction-needed` row blocks the run until resolved by a fresh retrieval and recheck.

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

`READY` copies the export, the readiness report, `run.json`, `draft.md`, and
`research-ledger.md` (sources retrieved, retrieval times, currency statements, live re-check
results, claims supported) to `pilot/content-workflow/deliveries/`. `INCOMPLETE` copies nothing
and lists reason codes. Delivery executes the declared validators against the exported file and
re-fetches every research record live; neither can be skipped, and there is no offline delivery.
Do not hand-edit records to reach `READY`; fix the underlying problem or report `INCOMPLETE`.

### 6. Independent review and learning pass

For a client-facing deliverable, run the read-only `seo-reviewer` / `seo_reviewer` on
the final artifact and supporting record as `AGENTS.md` requires, and resolve its
findings against evidence. Then run the single learning pass. Record pilot lessons in
`pilot/content-workflow/docs/CHANGES-AND-OPEN-QUESTIONS.md`; do not promote them into
production instructions from inside a run.

## What the tooling proves and does not prove

The readiness check proves hashes, presence, citation pairing, placeholder absence,
parity, record shape, currency, round limits, and, for each research record, that its metadata
is consistent with this run's nonce and opening time, that its excerpt and currency marker were
present in the stored page text, and that they are present on the live page at check time
(consistency and presence evidence, not authenticated provenance). Declared jurisdiction and
legislation status are checked for consistency, not correctness. It records but cannot verify
legal or editorial judgment, and it cannot prove that a retrieved page supports the claim cited
to it. Say so in every delivery summary. Attorney
review before publication remains required for legal content.
