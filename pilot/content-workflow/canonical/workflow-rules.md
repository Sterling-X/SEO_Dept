# Content-workflow rules (pilot v1, canonical)

These rules are the single source for the pilot content-production workflow. The Claude
and Codex adapters under `../adapters/` are generated from this directory by
`scripts/build_adapters.py`; edit here, never in a generated file. `AGENTS.md` remains
authoritative for everything it covers (role, precedence, recall, review, Git). Where this
file is narrower than `AGENTS.md`, the narrower pilot rule applies only inside a pilot run.

## Participants

| Role | Owns | Never |
|---|---|---|
| Coordinator (the primary SEO Strategist conversation) | Intake gate, current-source research (opening the run's research and retrieving every authority and first-party page with `scripts/research_fetch.py`), dispatch, recording reviews, integration, disagreements, the final artifact, delivery, the single learning pass | Marks a finding fixed-verified on the writer's word; edits a review record's findings; hand-writes or copies a research record |
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
run.json                 manifest: client, jurisdiction, page type, pinned skills, pinned sources, voice route, citations, validators, research nonce
research/EV<n>.json      research evidence records, written only by scripts/research_fetch.py after a live fetch (schema: canonical/schemas/research-record.schema.json)
research/EV<n>.txt       the page text as retrieved, hashed into the record
manifest.json            the generator manifest the pinned skill consumes (when the skill has a generator)
draft.md                 the text reviewers read; rendered from manifest.json with scripts/render_draft.py (Markdown; [[n]](url) markers; Sources last)
export/<file>.docx       the exported artifact
sources/                 pinned client facts, voice brief, legal source notes (never committed; notes point at research records, they are not evidence themselves)
reviews/<role>-<stage>-r<round>.json   review records (schema: canonical/schemas/review-record.schema.json)
changes.md               writer's change log keyed by finding id
readiness-report.json    written by scripts/readiness_check.py (carries the research ledger)
research-ledger.md       reader-facing ledger written by scripts/deliver.py: sources retrieved, times, currency, live re-check, claims supported
delivery-status.json     written by scripts/deliver.py
```

## Stage 0: intake gate

Stage numbering: 0 intake, 0b current-source research, 1 pre-draft legal verification, 2 drafting
with checkpoints, 3 final review of the complete revised document, 4 render inspection, 5 repair
and recheck, 6 delivery.

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

Intake also requires the run's research to be opened (`research_fetch.py <run> --init` writes
`research.nonce`, `research.opened_at`, and `research.max_age_days` into `run.json`;
`RESEARCH_NOT_OPENED` otherwise). Nothing retrieved before that moment counts for this run.

## Stage 0b: current-source research (required on every run)

Every material legal claim and every changeable factual claim (services, pricing, locations,
credentials, court procedures, filing fees, statistics, link destinations) rests on a page retrieved
during this run. The coordinator retrieves each authority and each first-party page with
`scripts/research_fetch.py`, which writes `research/EV<n>.json` plus the extracted page text only
when the fetch returned HTTP 200 now and the verbatim `excerpt` (40+ characters) the coordinator
names, and the page's own currency marker when one is given, are present in that text. Each record
carries the run nonce, the retrieval time, the content hash, the declared jurisdiction, and for a
legal authority the declared legislation status (`effective`, `enacted-not-effective`, `proposed`,
...), the compilation's current-through date and the provision's own effective date when the page
states one, the page's currency marker (required, or a recorded reason why the page has none), and
the section's own History line as the amendments note. The excerpt must be operative text, not the
marker, and a section identifier from the cited authority must appear in the retrieved text.

Prior reviews, model memory, saved notes under `sources/`, source files from an earlier run, and
approved brand guidance do not satisfy this stage. Brand guidance governs voice; it proves no
fact. If a required source cannot be retrieved now, the affected claim is unverified and the work
is reported `INCOMPLETE`; nothing is drafted or placeholdered around it.

`readiness_check.py --stage research` (and every delivery check) applies these rules:

- `RESEARCH_MISSING`: a `legal-authority` source, a `run.json` citation, or the `client-facts`
  source (`evidence_ids`) has no valid record retrieved in this run.
- `RESEARCH_REUSED`: a record's nonce or `run_id` is not this run's, or its `retrieved_at` predates
  `research.opened_at`. Evidence from an earlier run is never this run's evidence.
- `RESEARCH_STALE`: a record is older than `research.max_age_days` (default 14, never more than
  30) at check time; re-retrieve.
- `RESEARCH_INVALID`: malformed record, missing or edited page text, an excerpt or currency marker
  that is not in the retrieved text, a record without an excerpt (a timestamp alone is not
  verification), a future retrieval time.
- `RESEARCH_JURISDICTION_MISMATCH`: a legal authority whose declared jurisdiction is neither the
  run's jurisdiction nor federal.
- `LEGISLATION_NOT_EFFECTIVE`: a legal authority whose status is not `effective`, or whose effective
  date is after the retrieval date. Proposed or not-yet-effective law never supports a claim of
  current law.
- Live re-verification, on every research-stage and delivery check: each valid record's URL is
  fetched again. `RESEARCH_UNAVAILABLE` when it cannot be fetched or is not HTTP 200;
  `RESEARCH_EXCERPT_DRIFT` when the current page no longer contains the recorded excerpt or
  currency marker (the law or fact changed; re-research). `--offline` skips the live step and
  reports `RESEARCH_LIVE_SKIPPED`; an offline check is never `READY`, and `deliver.py` has no
  offline mode.

A fixture run (`fixture: true`) may map its reserved `.example` URLs to a local test server with
`CW_FIXTURE_URL_REWRITE`; a real run never rewrites and never fetches a reserved host.

## Stage 1: pre-draft legal verification (required for family-law pages)

Before any material legal claim is drafted, the legal reviewer verifies the planned claims live
against current primary authority and returns a `predraft` record: a Verification Log row per
planned claim with authority, official URL, access date, result, and, for every result except
`Unverifiable`, the `evidence_id` of the research record retrieved in this run for that URL and an
`excerpt` of at least 40 characters quoted verbatim from the text retrieved as that record. The
recorder refuses a verified row without them, a row whose URL is not the one the record
retrieved, an excerpt that is not in the retrieved text, or an access date before the run opened
(`LEGAL_LOG_NO_EVIDENCE` when the gate finds the same in a hand-written record). The record is
bound to the pinned sources (its `subject.sources_sha256`), not to a draft. The writer may draft
only claims that have a `Confirmed` row; a claim without one is omitted or the run is
`INCOMPLETE`. The gate requires the record (`legal-predraft`), requires every `run.json`
citation URL to have a `Confirmed` row (`LEGAL_PREDRAFT_COVERAGE`), and blocks on any
`Unverifiable` or `Correction-needed` row (`LEGAL_LOG_UNVERIFIED`). Re-pinning a source stales it.

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

Research evidence invalidates separately: a record older than `research.max_age_days`, a page
that no longer contains its excerpt at the live re-check, or a rotated research nonce
(`research_fetch.py --init --force`) removes that record's support, and every Verification Log
row that relied on it loses its evidence. The remedy is a fresh retrieval and a legal recheck
against it, never an edit to the record.

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

`scripts/deliver.py <run-dir>` runs the full readiness check including the live research
re-verification, executes every validator the run declares (a pinned skill that declares
validators forces the run to declare them), and refuses `READY` unless every check passes. Runs
marked `fixture: true` are never delivered. It validates the exported document as well as
`draft.md`. On `READY` it copies the export, the readiness report, `run.json`, `draft.md`, and
the reader-facing `research-ledger.md` (every source retrieved, its retrieval time, currency
statement, live re-check result, and the logged claims that rely on it) to the delivery directory
and writes `delivery-status.json`. On `INCOMPLETE` it writes the reasons and copies nothing.

## Mechanical validation versus judgment

The readiness check and `mechanical_qa.py` prove only mechanical facts: hashes match,
files exist, citations pair with Sources, no placeholder remains, headings, normalized
consumer-copy paragraph sequences, and word counts agree between draft and export, records
are well formed and current, each research record's metadata is consistent with this run's nonce
and opening time, its quoted excerpt and currency marker were present in the stored page text and
are present on the live page at check time, and each verified Verification Log row quotes that
stored text. This is consistency and presence evidence, not authenticated provenance: the run
directory is writable. Declared jurisdiction and legislation status are checked for consistency
with the run and the page's section identifier, not for correctness. A recorded legal or editorial `PASS`
is a recorded judgment by a reviewer bound to a hash; the tooling cannot verify that the
judgment was correct, that a retrieved page supports the claim it is cited for, or that the
reviewer read what it quoted, and says so in every report. Attorney review before publication
remains required for legal content.

## Client-specific rules

Voice skills and approved briefs carry client-specific rules. They apply only to the
routed client. A rule observed in one client's material is never promoted to a shared
rule from inside a run.

## Learning

Pilot lessons are recorded in `pilot/content-workflow/docs/CHANGES-AND-OPEN-QUESTIONS.md`
during the pilot. They are not promoted into `AGENTS.md`, production skills, or MemPalace
shared rooms by the pilot; promotion follows `learning/README.md` after the pilot is
evaluated. Evaluation criteria stay fixed while the pilot runs.
