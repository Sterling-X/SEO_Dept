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
      "passage": {"location": "H2 'Parenting decisions', paragraph 2", "quote": "exact text copied from the draft"},
      "issue": "what is wrong and why it matters to a reader",
      "evidence": {"authority": "Fla. Stat. § 61.13(2)(c)", "url": "https://official.example/...", "accessed": "2026-09-23", "note": "what the fetched text says"},
      "requested_correction": "the smallest change that makes the passage correct",
      "resolution": {"status": "open", "verified_against_draft_sha256": null, "verified_by": null, "note": null}
    }
  ],
  "verification_log": [
    {"claim": "condensed claim", "location": "…", "authority": "…", "url": "…", "accessed": "2026-09-23", "result": "Confirmed", "notes": "…"}
  ],
  "checks_not_performed": ["…"],
  "learning_contribution": {"result_and_evidence": "…", "corrections_or_methods": "none", "lesson_candidate": "none", "uncertainty_or_disagreement": "…"}
}
```

Field rules:

- `id`: role prefix plus number (`L1`, `E3`, `M2`). Ids persist across rounds so a
  recheck can update the same finding.
- `severity`: `blocking`, `major`, `minor`, `note` (meaning per role file).
- `passage.quote`: copied verbatim from the reviewed draft. `record_review.py` rejects a
  finding whose quote cannot be found in the draft after whitespace normalization; this
  keeps findings anchored to the version under review.
- `evidence`: for legal findings, the authority, its official URL, the access date, and
  what the text says. For editorial findings, the client fact, voice element, brief field,
  or rule violated, with its source path.
- `resolution.status`: `open`, `fixed-verified`, `fixed-unverified`, `disputed`,
  `withdrawn`, `coordinator-accepted`. Reviewers set `open`, `fixed-verified` (rechecks
  only), `disputed`, or `withdrawn`. The coordinator may set `coordinator-accepted` on a
  `major` finding only, with a rationale in `note`. Nobody sets `fixed-verified` without
  re-reading the revised passage.
- `verification_log`: required for the legal role; optional otherwise.
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
