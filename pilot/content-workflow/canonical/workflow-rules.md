# Content-workflow rules (pilot v1, canonical)

These rules are the single source for the pilot content-production workflow. The Claude
and Codex adapters under `../adapters/` are generated from this directory by
`scripts/build_adapters.py`; edit here, never in a generated file. `AGENTS.md` remains
authoritative for everything it covers (role, precedence, recall, review, Git). Where this
file is narrower than `AGENTS.md`, the narrower pilot rule applies only inside a pilot run.

## Participants

| Role | Owns | Never |
|---|---|---|
| Coordinator (the primary SEO Strategist conversation) | Intake gate, dispatch, recording reviews, integration, disagreements, the final artifact, delivery, the single learning pass | Marks a finding fixed-verified on the writer's word; edits a review record's findings |
| Content writer | The draft and its change log inside the run directory | Marks findings resolved; writes outside the run directory; delegates |
| Legal reviewer | Independent verification of material legal claims against current authority; structured findings; rechecks | Edits the draft; approves from memory; delegates |
| Editorial reviewer | Usefulness, client specificity, brand fidelity, structure, unsupported promises, brief compliance; structured findings; rechecks | Edits the draft; loads a second client's voice; delegates |
| Mechanical QA | Deterministic checks executed by `scripts/mechanical_qa.py` | Judges accuracy or quality |

Reviewers are read-only and hold no delegation capability where the host can enforce it
(Claude: tool allowlist; Codex: `sandbox_mode = "read-only"` plus instruction). In Codex,
the no-delegation rule is instruction-only because the custom-agent format exposes no
depth or tool restriction (verified against the Codex subagent documentation on
2026-09-23).

## Run directory

Every run lives in one directory (`pilot/content-workflow/runs/<run-id>/`, Git-ignored):

```
run.json                 manifest: client, jurisdiction, page type, pinned skills, pinned sources, voice route, citations, validators
manifest.json            the generator manifest the pinned skill consumes (when the skill has a generator)
draft.md                 the text reviewers read; rendered from manifest.json with scripts/render_draft.py (Markdown; [[n]](url) markers; Sources last)
export/<file>.docx       the exported artifact
sources/                 pinned client facts, voice brief, legal source notes (never committed)
reviews/<role>-<stage>-r<round>.json   review records (schema: canonical/schemas/review-record.schema.json)
changes.md               writer's change log keyed by finding id
readiness-report.json    written by scripts/readiness_check.py
delivery-status.json     written by scripts/deliver.py
```

## Stage 0: intake gate

Work on a stage does not begin until `readiness_check.py --stage intake` reports no
intake failures. Required before drafting:

- client `name`, `domain`, `slug`;
- `jurisdiction`;
- `page_type.kind` and, for family-law pages, `page_type.architecture_node_id`;
- every skill the run will use, pinned by repository-relative `path` and `sha256`, with
  every `required_files` entry of the skill's `pilot-manifest.json` present;
- every source pinned by `path` and `sha256`, present on disk;
- a voice route: the domain resolves in `canonical/client-routing.json` to exactly one
  voice skill whose `SKILL.md` exists, or the domain is unrouted and an approved voice
  brief is pinned as a source. Inference from the vertical is not a route.

A missing item yields status `INCOMPLETE` with a reason code. Nothing is drafted around it.

## Stage 1: drafting with checkpoints

1. The writer produces `draft.md` (and, for a generator-backed skill, the manifest the
   generator consumes) from the pinned skill, the single voice source, approved client
   facts, and pinned legal sources.
2. Legal checkpoint: the legal reviewer verifies the material claims of the checkpoint
   draft and returns findings. Editorial checkpoint: the editorial reviewer returns
   findings on structure, brief compliance, and client specificity. Both are recorded with
   `stage = "checkpoint"`, `round = 0`, bound to the draft hash they read.
3. The writer corrects against the finding ids and logs each change.

Checkpoints may be skipped only when the coordinator records why in `run.json`
(`checkpoints.skipped_reason`); the final reviews are never skipped.

## Stage 2: final review of the complete revised document

The legal reviewer and the editorial reviewer each review the complete revised `draft.md`
(`stage = "final"`, `round = 0`). Mechanical QA runs on `draft.md` and the exported DOCX.
All three records are bound to the hashes of what they reviewed.

## Stage 3: repair and recheck, at most two rounds

A round is one writer repair followed by a recheck by every required role, because any
change to the draft hash stales every role's record. Rounds are numbered 1 and 2. A record with `round > max_repair_rounds` (default
2) makes the run `INCOMPLETE` with `ROUNDS_EXCEEDED`; the coordinator reports the
unresolved findings instead of continuing.

On recheck a reviewer re-reads each revised passage and sets `resolution.status` to
`fixed-verified` with `verified_against_draft_sha256` equal to the reviewed draft hash,
or leaves it `open` with a note. `fixed-unverified` (asserted by the writer or the
coordinator) never satisfies a blocking or major finding.

## Invalidation

Any change to `draft.md`, the export, or a pinned source changes its hash. Every review
record whose `subject` hashes (draft, and for legal and editorial records the pinned sources;
for mechanical records the export too) no longer match the current files is stale and no
longer counts. A stale required review yields `REVIEW_STALE`; the fix is a recheck, which counts
toward the round cap once the initial final review exists.

## Findings

Findings follow `canonical/schemas/review-record.schema.json` and
`canonical/review-findings-schema.md`: id, severity (`blocking`, `major`, `minor`,
`note`), affected passage (exact quote and location), issue, supporting evidence,
requested correction, resolution (`open`, `fixed-verified`, `fixed-unverified`,
`disputed`, `withdrawn`, `coordinator-accepted`). The latest record of a role governs the
status of each finding id that role raised; a blocking finding that a later record does
not carry forward is treated as unresolved.

Delivery rules:

- The three final reviews are a fixed floor; `run.json` can add checkpoint kinds but cannot
  remove a final review. A required checkpoint kind is satisfied by presence and shape (it is
  bound to an earlier draft by design); its findings still flow into the resolution rules.
- A `Flagged` Verification Log row does not block by itself; the reviewer surfaces flagged
  claims as findings, which the finding rules then govern.
- A current legal or editorial final record with verdict `not-ready` blocks delivery
  (`REVIEW_VERDICT_BLOCKING`); `ready-with-revisions` passes only if the finding rules below
  are met.
- A current legal final record whose Verification Log contains any `Unverifiable` or
  `Correction-needed` row blocks delivery (`LEGAL_LOG_UNVERIFIED`).
- Mechanical records are gated by currency and verdict; a failed mechanical check is fixed and
  re-run, not carried forward as a finding.
- `blocking` must be `fixed-verified` or `withdrawn` (with a note).
- `major` must not be `open`; `coordinator-accepted` requires a rationale of at least 40
  characters and is reported in the delivery summary as an accepted risk.
- `disputed` preserves disagreement; a disputed blocking finding keeps the run
  `INCOMPLETE`. The coordinator does not force consensus.

## Stage 4: delivery

`scripts/deliver.py <run-dir>` runs the full readiness check, executes every validator the
run declares (a pinned skill that declares validators forces the run to declare them), and
refuses `READY` unless every check passes. Runs marked `fixture: true` are never delivered. It validates the exported document as well as `draft.md`. On
`READY` it copies the export and the readiness report to the delivery directory and
writes `delivery-status.json`. On `INCOMPLETE` it writes the reasons and copies nothing.

## Mechanical validation versus judgment

The readiness check and `mechanical_qa.py` prove only mechanical facts: hashes match,
files exist, citations pair with Sources, no placeholder remains, headings, normalized
consumer-copy paragraph sequences, and word counts agree between draft and export, records
are well formed and current. A recorded
legal or editorial `PASS` is a recorded judgment by a reviewer bound to a hash; the
tooling cannot verify that the judgment was correct and says so in every report.
Attorney review before publication remains required for legal content.

## Client-specific rules

Voice skills and approved briefs carry client-specific rules. They apply only to the
routed client. A rule observed in one client's material is never promoted to a shared
rule from inside a run.

## Learning

Pilot lessons are recorded in `pilot/content-workflow/docs/CHANGES-AND-OPEN-QUESTIONS.md`
during the pilot. They are not promoted into `AGENTS.md`, production skills, or MemPalace
shared rooms by the pilot; promotion follows `learning/README.md` after the pilot is
evaluated. Evaluation criteria stay fixed while the pilot runs.
