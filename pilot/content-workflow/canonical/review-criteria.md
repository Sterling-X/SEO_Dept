# Review criteria (pilot v1, canonical)

Three gates, three different questions. A pass at one gate says nothing about the others.

## Legal (judgment; legal-reviewer role, candidate skill `legal-content-accuracy-qa-pilot-v1`)

- Every material legal claim is verified live against the current text of governing
  primary authority during the review, with the access date recorded.
- Per-claim support test: the cited section governs the exact proposition, the right
  subsection, the right procedural posture, no hybrid of provisions, no omitted
  prerequisite or exception.
- Absolute-language claims get the separate exception search across the full statute and
  companion statutes; the search and its result are recorded.
- Multi-part standards keep their and/or logic, burden, and standard of proof. Lists are
  labeled complete or selective correctly. Court discretion is not described as mandatory.
- Procedure, deadlines, waiting and residency periods, and forms are attributed to their
  true source (statute, rule, form, regulation, local rule, practice).
- Pending law is dated and staged; effective dates are current as of the review date.
- Every citation resolves to the intended official source and supports its sentence.
- Terminology is jurisdiction-correct or flagged as a consumer-language decision.
- No misleading implication of guaranteed results, specialist status, dual representation,
  or coverage outside licensure.
- Output: verdict, structured findings, Verification Log (one row per material claim,
  result in {Confirmed, Flagged, Correction-needed, Unverifiable}), residual unknowns.
  Unverifiable is never a pass. Attorney review before publication is still required.

## Editorial (judgment; editorial-reviewer role, candidate skill `family-law-red-team-qa-reviewer-pilot-v1`)

- Usefulness: answer-first opening, the reader's decision served early, selective
  procedure, no blog sprawl or listicle framing.
- Client specificity: firm statements trace to approved client facts; no generic
  boilerplate; no other client's facts.
- Brand fidelity: judged against the one voice source resolved by exact domain route,
  citing the specific voice element matched or violated.
- Structure: required sections and order, heading hierarchy, three-sentence paragraphs,
  scannability, page-role separation from hub and procedural pages.
- Unsupported promises: guarantees, outcomes, superlatives, manufactured urgency,
  pricing, free-consultation claims, specialist or certification language.
- Brief compliance: node, jurisdiction, excluded intents, word target, the limits in
  `link-and-cta-limits.md`, lead-in linking, no tag-on or cluster links.
- Citation-claim fit is a desk check from the text in hand and is labeled as such.

## Mechanical (deterministic; `scripts/mechanical_qa.py` and `scripts/readiness_check.py`)

- Hash pins: skills, sources, draft, export, review subjects.
- Required resources of each pinned skill exist.
- Voice route resolves to exactly one source.
- Citations: body markers, Sources entries, and `run.json` citations agree in set, order
  (first appearance 1..n), count (each once in body), label, and URL, in both the draft
  and the export; markers are hyperlinked to the source URL in both (`[[n]](url)` in the
  draft, a hyperlink anchored `[n]` in the export).
- Placeholders: none of the placeholder grammar remains in draft or export (numeric
  citation markers and Markdown links are not placeholders; accented names are not
  placeholders).
- Export parity: heading sequence and the normalized consumer-copy paragraph sequence equal
  between draft and export (anything before the H1, such as a publisher block, is excluded);
  word count within a capped 2% tolerance; client name present in both; no forbidden term.
- Review records: present for every required review, well formed, current, rounds within
  cap, findings resolved per `workflow-rules.md`.
- Optional skill validators (structural and page-level) executed with exit codes recorded
  when the run declares them.

A mechanical PASS establishes none of the legal or editorial judgments above.
