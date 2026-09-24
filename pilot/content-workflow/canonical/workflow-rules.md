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
| Legal reviewer | Pre-draft verification of every planned material legal claim, checkpoint reviews, independent final review; structured findings; rechecks | Edits the draft; approves from memory; delegates |
| Render inspector (the coordinator, or a named human) | Views every rendered page of the exact export and records a per-page observation that quotes words on that page | Attests pages it did not view |
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

Stage numbering: 0 intake, 1 pre-draft legal verification, 2 drafting with checkpoints, 3 final
review of the complete revised document, 4 render inspection, 5 repair and recheck, 6 delivery.

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

Sources: one citation identity per canonical authority URL. Six sources is a readability
guideline, not a cap; claim coverage governs. A run that expects more than six must record
`citations_ceiling_rationale` (40+ characters) naming the claims that need them; twelve is a
sanity limit (`SOURCE_CEILING`).

## Stage 1: pre-draft legal verification (required for family-law pages)

Before any material legal claim is drafted, the legal reviewer verifies the planned claims live
against current primary authority and returns a `predraft` record: a Verification Log row per
planned claim with authority, official URL, access date, and result. The record is bound to the
pinned sources (its `subject.sources_sha256`), not to a draft. The writer may draft only claims
that have a `Confirmed` row; a claim without one is omitted or the run is `INCOMPLETE`. The gate
requires the record (`legal-predraft`), requires every `run.json` citation URL to have a
`Confirmed` row (`LEGAL_PREDRAFT_COVERAGE`), and blocks on any `Unverifiable` or
`Correction-needed` row (`LEGAL_LOG_UNVERIFIED`). Re-pinning a source stales it.

## Stage 2: drafting with checkpoints

1. The writer produces `draft.md` (and, for a generator-backed skill, the manifest the
   generator consumes) from the pinned skill, the single voice source, approved client
   facts, and pinned legal sources.
2. Legal checkpoint: the legal reviewer verifies the material claims of the checkpoint
   draft and returns findings. Editorial checkpoint: the editorial reviewer returns
   findings on structure, brief compliance, and client specificity. Both are recorded with
   `stage = "checkpoint"`, `round = 0`, bound to the draft hash they read.
3. The writer corrects against the finding ids and logs each change.

For family-law page kinds both checkpoints are required (presence and shape; they are bound to
the checkpoint draft by design). There is no skip. Their findings flow into the resolution rules.

## Stage 3: final review of the complete revised document

The legal reviewer and the editorial reviewer each review the complete revised `draft.md`
(`stage = "final"`, `round = 0`). Mechanical QA runs on `draft.md` and the exported DOCX.
All three records are bound to the hashes of what they reviewed.

## Stage 4: render inspection of the exact export

`scripts/render_inspect.py <run> --round N --render` renders the export through the pinned
skill's render wrapper (exact renderer release and SHA-256 from that skill's
`renderer-tools.lock.json`; isolated LibreOffice and PyMuPDF; fails closed) and writes a
`render-final` record with every page image hashed and `verdict: pending`. The inspector views
every page image and attests with a per-page observation (`--attest`); the record is bound to the
exact export hash. Delivery requires a current `render-final` record with verdict `pass`, every
page inspected, and page hashes unchanged (`RENDER_UNINSPECTED`, `RENDER_EVIDENCE_MISMATCH`,
`RENDER_FAILED`). A changed export invalidates it. Missing rendering capability leaves the run
`INCOMPLETE`; nothing substitutes for viewing the pages.

## Stage 5: repair and recheck, at most two rounds

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
`note`), category (`legal-accuracy`, `citation`, `client-fact`, `promise`, `brand`,
`structure`, `brief`, `mechanical`, `render`, `other`), affected passage (exact quote and
location), issue, supporting evidence, requested correction, resolution (`open`,
`fixed-verified`, `fixed-unverified`, `disputed`, `withdrawn`, `coordinator-accepted`). The latest record of a role governs the
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
- Mechanical and render records are gated by currency and verdict; a failed mechanical check or
  a render defect is fixed by re-run or re-export and a fresh render and inspection, not carried
  forward as a finding. The gate re-applies the render inspector's rules to the record itself:
  each page observation must quote three consecutive words of that page's rendered text, the page
  text and image hashes must match those recorded at render time, and a `pass` with a blocking or
  major render finding that is not `fixed-verified` or `withdrawn` is refused (`RENDER_FAILED`).
- A coordinator disposition may also apply to a major, non-protected finding whose latest record
  omitted it (`dropped`); the disposition is bound to the draft hash and reported with the run.
- Evidence-based closure: `fixed-verified` is set only by the raising reviewer after re-reading
  the revised passage, against the current draft hash; for the protected categories
  `legal-accuracy`, `citation`, `client-fact`, and `promise` it must also carry
  `corrected_text` that appears in the current draft. `withdrawn` is set only by the raising
  reviewer with a reason. A suggested correction, a writer's change log, or a coordinator's
  note never closes a finding.
- `blocking` must be `fixed-verified` or `withdrawn`; coordinator acceptance is never available
  for a blocking finding.
- `major` must not be `open`; `coordinator-accepted` is available only outside the protected
  categories, requires a rationale of at least 40 characters, and is reported in the delivery
  summary as an accepted risk. A legal-accuracy or client-fact error is never accepted. The
  coordinator records it with `scripts/dispose_finding.py`, which writes
  `reviews/coordinator-dispositions.json` bound to the current draft hash; reviewer records are
  never edited.
- Severity, category, and the raising reviewer are taken from the first record that carried
  the finding id. A later record that changes them is `FINDING_DRIFT`; a closure recorded by a
  different agent does not count.
- `disputed` preserves disagreement; a disputed blocking finding keeps the run
  `INCOMPLETE`. The coordinator does not force consensus.

## Stage 6: delivery

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
