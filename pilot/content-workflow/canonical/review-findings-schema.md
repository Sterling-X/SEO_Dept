# Structured findings (pilot v1, canonical)

Every reviewer returns one JSON object per review. `scripts/record_review.py` stamps the
subject hashes and writes it to `reviews/`. The machine-checked shape is in
`schemas/review-record.schema.json`; this page explains the fields.

```json
{
  "schema": "content-workflow-review/v1",
  "role": "legal-reviewer",
  "stage": "final",
  "round": 0,
  "verdict": "not-ready",
  "findings": [
    {
      "id": "L1",
      "severity": "blocking",
      "category": "legal-accuracy",
      "passage": {"location": "H2 'Parenting decisions', paragraph 2", "quote": "exact text copied from the draft"},
      "issue": "what is wrong and why it matters to a reader",
      "evidence": {"authority": "Fla. Stat. § 61.13(2)(c)", "url": "https://official.example/...", "accessed": "2026-09-23", "note": "what the fetched text says"},
      "requested_correction": "the smallest change that makes the passage correct",
      "resolution": {"status": "open", "verified_against_draft_sha256": null, "verified_by": null, "note": null, "corrected_text": null}
    }
  ],
  "verification_log": [
    {"claim": "condensed claim", "location": "…", "authority": "…", "url": "…", "accessed": "2026-09-24", "result": "Confirmed", "evidence_id": "EV2", "excerpt": "forty or more characters quoted verbatim from the page as retrieved in this run", "notes": "jurisdiction, current-through marker, history line, legislation status, exceptions searched"}
  ],
  "checks_not_performed": ["…"],
  "learning_contribution": {"result_and_evidence": "…", "corrections_or_methods": "none", "lesson_candidate": "none", "uncertainty_or_disagreement": "…"}
}
```

Field rules:

- `id`: role prefix plus number (`L1`, `E3`, `M2`, `R1` for render findings). Ids persist across
  rounds so a recheck can update the same finding; severity, category, and the raising reviewer
  are fixed by the first record that carried the id.
- `severity`: `blocking`, `major`, `minor`, `note` (meaning per role file).
- `category`: `legal-accuracy`, `citation`, `client-fact`, `promise`, `brand`, `structure`,
  `brief`, `mechanical`, `render`, `other`. The first four are protected: no coordinator
  acceptance, and `fixed-verified` needs `corrected_text`.
- `passage.quote`: copied verbatim from the reviewed draft. `record_review.py` rejects a
  finding whose quote cannot be found in the draft after whitespace normalization; this
  keeps findings anchored to the version under review.
- `evidence`: for legal findings, the authority, its official URL, the access date, and
  what the text says. For editorial findings, the client fact, voice element, brief field,
  or rule violated, with its source path.
- `resolution.status`: `open`, `fixed-verified`, `fixed-unverified`, `disputed`,
  `withdrawn`, `coordinator-accepted`. Reviewers set `open`, `fixed-verified` (rechecks
  only), `disputed`, or `withdrawn`. The coordinator may set `coordinator-accepted` on a
  `major` finding only, outside the protected categories, with a rationale in `note`. Nobody
  sets `fixed-verified` without re-reading the revised passage.
- `resolution.corrected_text`: the revised passage the reviewer re-read, copied from the
  current draft. Required for `fixed-verified` in a protected category; the recorder and the
  gate reject text that is not in the draft.
- Stage `predraft` (legal reviewer only): no draft exists; a finding's `passage.location` is the
  planned-claim id and `passage.quote` is the planned claim text the coordinator supplied (it is
  not matched against a draft); the `verification_log` rows are the record's substance and the
  record is bound to `subject.sources_sha256`.
- Role `render-inspector` (stage `final`): carries `render.pages[]` with `page`, `path`,
  `sha256`, `inspected`, `observation`, plus `page_count`, `renderer_release`,
  `renderer_sha256`, and `subject.export_sha256`. Written by `scripts/render_inspect.py`.
- `verification_log`: required for the legal role; optional otherwise. Each row carries `claim`,
  `result` (`Confirmed`, `Flagged`, `Correction-needed`, `Unverifiable`), and `accessed` (the
  actual retrieval date in this run, never earlier than `run.json` `research.opened_at`). Every
  result except `Unverifiable` also carries `evidence_id` (the `research/EV<n>.json` record
  retrieved in this run for that URL) and `excerpt` (40+ characters quoted verbatim from the text
  retrieved as that record). `record_review.py` refuses a row without them, a row whose `url` is not
  the retrieved URL, or an excerpt that is not in the retrieved text; the gate reports the same as
  `LEGAL_LOG_NO_EVIDENCE`. An `Unverifiable` row must explain the failed retrieval in `notes`.
- `learning_contribution`: the four items `AGENTS.md` requires from every participating
  agent.

The record written to disk adds `subject` (the draft, export, and source hashes present at
the moment the recorder ran, which is why the coordinator records immediately after the
reviewer returns; a reviewer may echo the draft hash it was given in `subject.draft_sha256` and
the recorder refuses a mismatch), `reviewer` (runtime, agent name, agent file and its hash),
`recorded_at`, and `judgment_notice` ("recorded judgment; not mechanically verified") for
legal and editorial roles. The tooling cannot verify that a record was produced by the named
reviewer; it re-applies the recorder's integrity rules at delivery so a hand-written record
must at least satisfy them.
