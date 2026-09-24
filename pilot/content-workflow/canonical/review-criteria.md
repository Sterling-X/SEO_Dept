# Review criteria (pilot v1, canonical)

Three gates, three different questions. A pass at one gate says nothing about the others.

## Legal (judgment; legal-reviewer role, candidate skill `legal-content-accuracy-qa-pilot-v1`)

- Every planned material legal claim is verified live before drafting (`predraft` record), and
  every drafted claim is verified again at the checkpoint and in the final review, against the
  current text of governing primary authority, with the access date recorded, the `evidence_id`
  of the research record retrieved in this run, and a verbatim excerpt of the retrieved text.
  Prior reviews, saved notes, memory, and brand guidance verify nothing.
- Jurisdiction, amendments and history line, effective date, and legislation status (proposed,
  enacted, effective) are established for every authority; proposed or not-yet-effective law is
  never presented as current law.
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

Client specificity is evidence-based. A neutral, accurate explanation of the law is acceptable
even though another firm could publish the same sentence; the page fails on client specificity
only for an observable defect: a wrong or unsupported firm statement, an offer, fee, process,
credential, staffing, coverage, or outcome claim outside the approved client facts, a documented
voice contradiction, or a missing scenario connection the brief requires. Name the passage and
the brief criterion. Never demand branded language inside a legal standard.

- Usefulness: answer-first opening, the reader's decision served early, selective
  procedure, no blog sprawl or listicle framing.
- Client specificity: firm statements trace to approved client facts, and changeable facts
  among them to a first-party page retrieved in this run (`client-facts` `evidence_ids`);
  brand guidance governs voice, not facts; no generic boilerplate; no other client's facts.
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
- Research evidence: every legal authority, citation, and client-facts page has a record
  retrieved in this run (nonce, retrieval time within `max_age_days`, HTTP 200, content and
  text hashes, excerpt present, currency marker present, jurisdiction matching, legislation
  status effective), and its page is re-fetched live at the research and delivery checks with
  the excerpt still present. Verified Verification Log rows name a record and quote its text.
- Required resources of each pinned skill exist.
- Voice route resolves to exactly one source.
- Citations: body markers, Sources entries, and `run.json` citations agree in set, order
  (first appearance 1..n), label, and URL, in both the draft and the export; every source is
  cited at least once and may be cited again with the same number wherever it supports a later
  material claim; markers are hyperlinked to the source URL in both (`[[n]](url)` in the draft,
  a hyperlink anchored `[n]` in the export).
- Placeholders: none of the placeholder grammar remains in draft or export (numeric
  citation markers and Markdown links are not placeholders; accented names are not
  placeholders).
- Export parity: heading sequence and the normalized consumer-copy paragraph sequence equal
  between draft and export (anything before the H1, such as a publisher block, is excluded);
  word count within a capped 2% tolerance; client name present in both; no forbidden term.
- Export cleanliness: no tracked changes, field codes, comments, hidden text, or embedded
  alternate content in the DOCX.
- Rendered pages: every page image of the exact export exists, is hashed, and carries an
  inspector's observation; the inspection is a recorded judgment bound to the export hash.
- Review records: present for every required review, well formed, current, rounds within
  cap, findings resolved per `workflow-rules.md`.
- Optional skill validators (structural and page-level) executed with exit codes recorded
  when the run declares them.

A mechanical PASS establishes none of the legal or editorial judgments above.
