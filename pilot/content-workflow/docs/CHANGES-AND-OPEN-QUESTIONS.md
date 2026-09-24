# Content-workflow pilot: changes, evidence, and open questions

Created 2026-09-23 on branch `content-workflow-pilot`. This file is the pilot's record of
what changed relative to the baseline skills, what evidence supports each change, and what
remains unresolved. Nothing here is promoted into `AGENTS.md`, the production skills, or
MemPalace shared rooms by the pilot itself; promotion follows `learning/README.md` after the
pilot is evaluated. Evaluation criteria (the six rejection tests plus the accented-name
acceptance) were fixed before implementation and were not changed to make the pilot pass.

## Known workflow defects and their disposition

| # | Defect | Baseline evidence | Pilot disposition | Where enforced |
|---|---|---|---|---|
| 1 | Conflicting citation-placement and duplicate-URL requirements | Situational `SKILL.md` "In-body format" (identifier then bracketed number) versus the local template/generator (hyperlinked `[n]` run only); red-team skill "any URL appearing more than once is a hard fail" versus the required statute pairing. | One citation format and an explicit pairing exemption in `canonical/link-and-cta-limits.md`, the situational candidate, the editorial candidate, and the editorial role. | Skill text; `citation_issues()` in `scripts/cw_common.py`; candidate validators |
| 2 | Inconsistent link and CTA limits | Situational skill: up to 2 sibling + 3 secondary links, no CTA count; local `FL-M008` contract: exactly one parent, one bridge, one CTA. | Single table `canonical/link-and-cta-limits.md`; both candidates defer to it; CTA count added. | Skill text; editorial reviewer criteria (judgment) |
| 3 | Ambiguous client-voice selection | Situational skill: name-pattern scan with fifteen example names, one of which exists here; red-team skill: "there will be one voice skill present", but three exist. | Exact domain route from `canonical/client-routing.json` (mirror of `AGENTS.md`; a test asserts equality); unrouted domain requires a pinned approved brief; no default voice; no inference. | `intake_checks()` voice section (`VOICE_MISMATCH`, `VOICE_UNROUTED`, `VOICE_SKILL_MISSING`) |
| 4 | Missing templates, scripts, or other required resources | The import lacked the named template and validators (local replacements exist); nothing declared what a run requires; generator resolved the repository by fixed depth. | `pilot-manifest.json` per candidate with `required_files` (including installed Node dependencies); marker-based repository-root discovery. | `SKILL_RESOURCE_MISSING`, `SKILL_PATH_MISSING`, `SKILL_HASH_MISMATCH` |
| 5 | Reviews recommending fixes without verifying completion | Legal skill Verification Log allowed result `Corrected` in the same pass; quality gates were writer self-checks. | `Corrected` removed; `Correction-needed` added; `fixed-verified` only on recheck after re-reading; `fixed-unverified` never satisfies blocking or major; recorder refuses `fixed-verified` in an initial final review. | `evaluate_reviews()`; `record_review.py` |
| 6 | Later edits invalidating earlier legal review | No rule. | Every record carries subject hashes; a hash change makes it stale; a `fixed-verified` resolution must reference the current draft hash. | `REVIEW_STALE`, `FINDING_BLOCKING_UNRESOLVED` (stale verification) |
| 7 | Validators accepting citation mismatches or unresolved placeholders | See the table below. | Both candidate validators and the readiness check reject plain-text markers, unknown or out-of-order markers, Sources id/label/URL mismatch, and the full placeholder grammar in draft and export. | `CITATION_MISMATCH`, `PLACEHOLDER_UNRESOLVED`; candidate `validate-page.js`, `office/validate.py` |

## Baseline versus candidate validators on tampered DOCX files (2026-09-23)

Method: build a production-shaped synthetic FL-M008 document with two sources using the
baseline generator, tamper `word/document.xml`, and run each validator set. `PASS` means the
validator accepted the tampered file.

| Tampered case | Baseline page | Baseline structural | Candidate page | Candidate structural |
|---|---|---|---|---|
| plain-text `[1]` marker appended | PASS | FAIL (word-count parity only) | FAIL | FAIL |
| unknown `[7]` marker appended | PASS | FAIL (word-count parity only) | FAIL | FAIL |
| wrong Sources label | PASS | PASS | FAIL | FAIL |
| `[FIRM_NAME]` appended | PASS | FAIL (word-count parity only) | FAIL | FAIL |
| `{{county}}` appended | PASS | FAIL (word-count parity only) | FAIL | FAIL |
| bare `TBD` appended | PASS | FAIL (word-count parity only) | FAIL | FAIL |

The baseline structural failures in five rows come from its DOCX-versus-manifest word-count
check, which would not fire if the manifest carried the same defect; the baseline had no
placeholder or citation-marker check of its own.

## Preserved client-specific rules

- The `FL-M008` link-authority contract (parent hub, `FL-M004` bridge, CTA, exact V2 edges) is
  a family-law architecture rule and is preserved verbatim in the situational candidate.
- Voice skills for `sterlinglawyers.com`, `jmblattner.com`, and `servicecu.org` are untouched
  and are selected only by exact domain.
- The recovered Core page validator's Johnson Law Group `North Star` logic is out of scope
  (Core route) and unchanged.
- No rule observed in one client's material was generalized.

## Test evidence

- `pilot/content-workflow/tests/test_readiness.py`: 55 tests, all passing on 2026-09-23 (about
  two minutes; every READY fixture is rendered through the pinned renderer) after
  both independent review rounds and the comparison-patch integration (pre-draft legal
  verification, required checkpoints, render inspection bound to the export hash, protected
  closure categories, coverage-based source ceiling, export cleanliness) (Python 3.14.6, Node 20.20.1). The fixture is
  generator-backed: every run builds its export with the candidate's real
  `build-situational.js`, renders `draft.md` from the same manifest with
  `scripts/render_draft.py`, and executes the candidate's structural and page validators
  through `run.json` `export.validators`. Covered: the six required rejections (missing
  required review; draft edited after review; unresolved blocking finding in three statuses
  plus dropped; mismatched citations in the export, in the draft Sources, and a plain-text
  marker in the draft; four placeholder forms in draft and export; eight missing-dependency
  variants including resource-hash drift and undeclared validators), the accented client name
  acceptance, voice routing, rounds cap, fixture-flag guard, major-finding disposition,
  mechanical fail-then-pass, judgment verdict and Verification Log gating, checkpoint finding
  closed at the initial final review, required-review floor, pinned-source staleness,
  paragraph parity, hand-written record re-validation, recorder refusals (quote, role/agent,
  echoed hash, missing agent file), delivery refusal (incomplete and fixture), delivery success,
  adapter sync, routing parity with `AGENTS.md`, single-source placeholder grammar, candidate
  manifests and baseline provenance, and the candidate regression suite.
- Candidate `scripts/test-situational.py`: 38 cases (21 baseline cases unchanged plus 17 new),
  all passing.
- Baseline suites unchanged and still passing: `.codex/hooks/test-seo-learning-loop.py` (8),
  `.codex/hooks/test-mempalace-recall-reminder.py` (6), baseline
  `.agents/skills/family-law-situational-pages/scripts/test-situational.py` (21).

## Independent review round (2026-09-23)

The read-only `seo-reviewer` reviewed the complete pilot and returned two blockers, fifteen
material improvements, and nine optional refinements. Dispositions, each verified against the
code before acting:

| Finding | Disposition |
|---|---|
| B1: a failed mechanical record followed by a passing one left a "dropped" blocking finding, so the documented fail-then-fix path could never reach READY | Confirmed and fixed: mechanical records are gated by currency and verdict only; test `test_mechanical_fail_then_pass_is_ready`. |
| B2: legal and editorial verdicts and the Verification Log were displayed but never evaluated | Confirmed and fixed: `REVIEW_VERDICT_BLOCKING` for a current `not-ready` or `fail` final; `LEGAL_LOG_UNVERIFIED` for any `Unverifiable` or `Correction-needed` row; `ready-with-revisions` passes only when the finding rules pass (coordinator decision, documented). |
| M1: a checkpoint finding fixed before the initial final review had no legal state | Fixed: the recorder and the gate accept `fixed-verified` at final round 0 for an id raised in a prior checkpoint record of the same role. |
| M2: text said only roles with open findings recheck; the hash rule stales every record | Fixed in `workflow-rules.md` and the skill: every required role rechecks when the draft hash changes. |
| M3: only `SKILL.md` was hashed | Fixed: `pin.py` hashes every `required_files` entry into the pin; intake compares them; a pin without the files map is `SKILL_PIN_MISSING`. |
| M4: declared validators could be skipped silently and were never executed in tests | Fixed: `VALIDATOR_SKIPPED`, `VALIDATORS_UNDECLARED` (a pinned skill that declares validators forces the run to declare them by name), `--no-validators` removed from delivery; validators run in every fixture. |
| M5: no generator-built export had ever been checked | Fixed: the fixture is generator-backed (see Test evidence). Parity ignores the generator's publisher block by starting at the H1. |
| M6: parity compared only headings and word count | Fixed: normalized consumer-copy paragraph sequences must be identical; tolerance capped at 2%. |
| M7: `reviews.required` could be lowered | Fixed: the three finals are a fixed floor. |
| M8: intake accepted zero sources and citations | Fixed: `INTAKE_MISSING_SOURCE` for situational, core-hub, and procedural kinds. |
| M9: pinned-source changes did not stale reviews | Fixed: `subject.sources_sha256` is compared for every required record. |
| M10: Markdown citation form undefined (smoke finding E2) | Decided: `draft.md` uses `[[n]](url)`; a plain `[n]` fails `citations-draft`; `render_draft.py` emits the form; roles, criteria, and limits table updated. |
| M11: placeholder grammar in three code copies | Partly fixed: `canonical/placeholder-patterns.json` is the source `cw_common.py` loads; a test fails if either candidate validator or the candidate generator drifts from it. The link/CTA counts remain prose in the situational candidate with the table declared governing. |
| M12: legal live fetch depends on a permission grant denied in headless mode | Documented in README limitations; `.claude/settings.json` not changed. |
| M13: two overstatements about what records prove | Fixed: hash wording corrected; notice now says the tool cannot verify who produced a record; the gate re-applies the recorder's quote and round-0 rules to current records. |
| M14: activation symlinks' Git state unstated | Decided and documented: the eight symlinks are not committed and are Git-ignored; activation is local and explicit. |
| M15: Codex path read as verified; `$ARGUMENTS` is Claude-only | Fixed: Codex section labelled not verified live; Arguments text host-neutral. The reviewer's remaining uncertainty about the Claude-only frontmatter key is resolved by the offline render experiment above (Codex loads the skill with the key present). |
| Optional 1, 2, 3, 4, 5, 6, 7, 8, 9 | Adopted: fixture runs are refused by `deliver.py` without `--allow-fixture`; role/agent consistency check; `--force` keeps the superseded record under `reviews/superseded/`; README verification table filled and `npm ci` added to activation; enumeration note added; count provenance cited in the limits table; schema additions (`files`, `word_target`, `compare_headings`, sha256 pattern, tolerance maximum); TOML quote escaping; echoed draft hash compared by the recorder. |

Round 2 recheck (same reviewer, changed surfaces only): no blockers remaining; three small
material items and eight optional refinements, all adopted: `pilot-manifest.json` is now hashed
into every skill pin; a checkpoint kind in `reviews.required` is satisfied by presence and
shape; the skill's step 1 declares validators and `manifest.json` is part of the run layout;
`VALIDATORS_UNDECLARED` compares validator names; the recorder's prior-id set uses checkpoint
records only; `Flagged` log rows are documented as non-blocking; the editorial role no longer
raises plain markers; the writer role lists the renderer's supported block and run types; the
tests import `pin.py` instead of re-implementing it; README wording and this record updated.

Reviewer disagreement preserved: none outstanding after both rounds. The reviewer's candidate
lesson ("walk the documented failure-then-repair path through a gate, not just the fixture's
passing path") is recorded here as a hypothesis for the `seo-reviewer` role and is not
promoted.

## Independent review of the refinement integration (2026-09-23, two rounds)

The same read-only `seo-reviewer` reviewed the comparison-patch integration. Round 1 returned
one blocker and eight material items; round 2 (recheck of the changed surfaces) returned no
blocker, three material items, one optional item, and three design notes. Dispositions, each
checked against the code and covered by a test where the row names one:

| Finding | Disposition |
|---|---|
| B1: a failed render record followed by a passing one could never reach READY (the render-inspector finding stayed "dropped") | Confirmed and fixed: render-inspector findings are gated like mechanical ones (currency, verdict, and no unresolved blocking/major render finding); `attest()` refuses `pass` with such a finding; test `test_render_fail_then_reexport_then_pass_is_ready`. |
| M1: closure could be self-referential; severity, category, or raising agent could drift between records; an unmapped agent name was accepted | Fixed: the origin record fixes all three (`FINDING_DRIFT`); `fixed-verified` requires `verified_by` and the closing record's agent to equal the raising agent; the recorder refuses unmapped `claude`/`codex` agents; test `test_closure_is_origin_based_and_drift_is_refused`. |
| M2: no sanctioned path for coordinator acceptance | Fixed: `dispose_finding.py` writes `reviews/coordinator-dispositions.json` (major, non-protected, rationale of 40+ characters, bound to the draft hash). Regression found by `test_major_finding_disposition` and fixed: `review_files()` no longer loads that file as a review record. |
| M3: `corrected_text` was presence-only | Fixed: 20+ characters, different from the targeted quote, present in the draft (recorder and gate); `test_protected_findings_need_reviewer_evidence_to_close`. |
| M4: nothing proved pre-draft verification preceded drafting | Fixed: the recorder refuses a round-0 predraft record when `draft.md` or `manifest.json` exists; `LEGAL_PREDRAFT_LATE`; coverage is the union of `Confirmed` URLs across current predraft records; `test_predraft_must_precede_drafting`. |
| M5: stale "cite once" wording | Fixed in `link-and-cta-limits.md`, the situational candidate (`SKILL.md` in-body format, footnote convention, single-placement scope clarification), `LOCAL-REPLACEMENT.md`, the template, and the candidate `CHANGES.md` (round-2 finding A1 caught the last two passages). Editing the pinned `SKILL.md` invalidates existing pins by design; the Sterling run was re-pinned. |
| M6: E05 exclusion misattributed to V2 | Fixed: the reason now says V2 governs targets, not placement counts. |
| M7: render attestation not bound to page content | Fixed on the sanctioned path (`attest()` requires three consecutive words of the page text) and, after round-2 finding A2, mirrored in the gate: `RENDER_EVIDENCE_MISMATCH` when a page text file is missing or changed, `RENDER_UNINSPECTED` when an observation does not quote the page, `RENDER_FAILED` for an unresolved blocking or major render finding; `render()` fails closed when the wrapper emits no PDF or an empty page text; `test_gate_reapplies_render_attestation_rules_to_hand_written_records`. |
| M8: compatibility sentence; open questions 1 and 5 | Fixed: the compatibility sentence (validation requirement replaced, not removed) is in the adopted table; open questions 1 and 5 closed with evidence. |
| Round 2 A3: this review was not in the record; counts stale | Fixed: this section; counts updated (55 tests). |
| Round 2 A4: the canonical rules did not state the render-record rule | Fixed in `workflow-rules.md`. |
| Round 2 design notes (optional) | `dispose_finding.py` now walks records in gate order (`record_order_key`); the `dropped`-status disposition is stated in `workflow-rules.md`; the agent-name equality question is recorded as open question 8. |
| Recorder crash on a predraft record (found on the Sterling run, not by the reviewer) | The recorder's summary line indexed a missing draft hash after writing the record; fixed and covered by `test_record_review_cli_records_predraft_before_any_draft_exists`. |
| Render-observation matcher brittleness (found on the Sterling run, not by the reviewer) | The three-consecutive-words binding compared raw whitespace tokens, so a genuine quote written as `H1 'High-Conflict Divorce in Wisconsin',` failed on the attached quote mark and comma (the round-0 attestation had passed on a different phrase). `observation_matches_page()` now strips punctuation attached to words on both sides before matching; the rule itself (three consecutive page words, in order) is unchanged; `test_observation_match_ignores_attached_punctuation`. |
| Record ordering defect (found on the Sterling run, not by the reviewer) | A supplementary pre-draft record recorded as round 1 (one extra Confirmed row for a cited statute) sorted after the round-0 checkpoint, so the gate read the checkpoint's nine `fixed-verified` closures as "dropped" and reported two blocking and three major findings unresolved. `record_order_key()` now places every pre-draft record (no draft to bind to) before every draft-bound record, then orders by round, stage, time; `test_supplementary_predraft_record_does_not_outrank_the_checkpoint`. |

Reviewer disagreement preserved: the reviewer left open whether closure should require the
identical raising agent name or the same role (mixed-host or attorney rechecks); recorded as
open question 8, not decided. The reviewer's candidate lesson ("for each script that writes a
review record, enumerate its refusal rules and add a gate test that a hand-written record
violating each rule is refused") is scenario-checked once here (A2 was exactly such a miss) and
is recorded as a hypothesis for the `seo-reviewer` role, not promoted.

## Full-system audit and research-first repair (2026-09-24)

Source task: the user's 2026-09-24 request to audit, repair, and test the complete pilot, make
current-source research mandatory, replace placeholder-first with research-first, add controlled
tests, run fresh integration tests with the actual agents on both hosts, and test install and
rollback in a disposable checkout. Every row below names its evidence; nothing here reuses the
2026-09-23 results as a new test.

### Defects found by the audit and their disposition

| # | Defect | Evidence | Disposition | Where enforced |
|---|---|---|---|---|
| 8 | No mechanical evidence that any source was retrieved. A Verification Log row proved only a date; the fixture pre-draft record said "nothing fetched" and passed coverage; a row copied from an earlier run or written from a saved `sources/` note would pass. | `readiness_check.py` (2026-09-23) read only `result`, `url`, `accessed`; fixture `legal-predraft-r0.json` notes "FIXTURE: source note read; nothing fetched" | Research evidence layer: `scripts/research_fetch.py` writes `research/EV<n>.json` plus the extracted page text only after a live HTTP 200 fetch with the named excerpt (40+ chars) and currency marker present; each record carries the per-run nonce, retrieval time, content hash, declared jurisdiction, declared legislation status, current-through date, amendments note. Every verified Verification Log row must name a record (`evidence_id`) and quote its text (`excerpt`); `record_review.py` refuses otherwise. | `cw_research.research_problems()`, `legal_log_problems()`; `record_review.py`; `readiness_check.py --stage research` and delivery |
| 9 | Evidence reuse across runs undetectable. Nothing distinguished a record made for this run from one copied from an earlier run or written before the run started. | design gap; the Sterling 2026-09-23 run's `sources/legal-*.md` notes could have been copied into a new run | Per-run research nonce and opening time (`research_fetch.py --init`); a record with another nonce or `run_id`, or retrieved before `opened_at`, is `RESEARCH_REUSED`; older than `max_age_days` (14, max 30) is `RESEARCH_STALE`; an access date before `opened_at` in a log row is refused | `RESEARCH_REUSED`, `RESEARCH_STALE`, `LEGAL_LOG_NO_EVIDENCE` |
| 10 | Timestamps treated as proof. A record or row with a date and no checkable text could pass. | same | A record needs an excerpt present in the retrieved text and a text hash; a row needs a verbatim excerpt found in that text; a record with a date and no excerpt is `RESEARCH_INVALID` ("a timestamp alone is not retrieval evidence") | `validate_record_shape()`, `legal_log_problems()` |
| 11 | No currency check at delivery: law or a client page could change between review and delivery. | design gap | Live re-fetch of every valid record at every research-stage and delivery check: `RESEARCH_UNAVAILABLE`, `RESEARCH_EXCERPT_DRIFT`; `--offline` reports `RESEARCH_LIVE_SKIPPED` and is never READY; `deliver.py` has no offline mode | `research_live_problems()`; `deliver.py` |
| 12 | Jurisdiction and legislation status never recorded or checked; proposed or not-yet-effective law could back a claim of current law. | design gap | Declared jurisdiction and legislation status are checked for consistency: `RESEARCH_JURISDICTION_MISMATCH` (declared jurisdiction must be the run's or federal; neutral labels such as `n/a` no longer pass), `LEGISLATION_NOT_EFFECTIVE` (declared status must be `effective`; a provision effective date after retrieval is refused), a section identifier from the cited authority must appear in the retrieved text, the excerpt may not be the currency marker, and a legal record needs the page's marker or a recorded reason for its absence. Correctness of the declarations is the legal reviewer's judgment. | `research_problems()`, `validate_record_shape()`, `research_fetch.py` |
| 13 | Client facts needed no current first-party evidence; the voice skill alone could support a fee, office, or credential statement. | `client-facts` source had only `verified_on` | `client-facts` source declares `evidence_ids` of first-party pages retrieved in the run (`RESEARCH_MISSING` otherwise); editorial role and red-team candidate require it; brand guidance governs voice, not facts | `research_problems()`; roles; candidate |
| 14 | Placeholder-first instructions. Writer role: "remove the claim or leave a `[LOCAL DETAIL]` placeholder"; situational candidate and baseline: "leave a placeholder rather than guessing". | role and skill text | Research-first wording in the writer role, situational candidate (research section, Quality Gates 7 and 10, template), coordinator skill (Stage 1a), workflow rules (Stage 0b), `AGENTS.md` ("Current-source research"), and `docs/seo-skill-compatibility.md` (imported placeholder-first text superseded on conflict; imported files unchanged as fallback). A `[LOCAL DETAIL]` marker is a reporting device for a fact confirmed unobtainable now, never a way to finish | text; placeholder gate unchanged |
| 15 | Activation and rollback could not handle a regenerated adapter: after `build_adapters.py`, the Codex byte copies no longer matched, `rollback.sh` refused to remove them, and `activate.sh` refused to replace them. | reproduced 2026-09-24 in this checkout | Both scripts recognise a pilot-generated copy by the generator banner on its first line; foreign files are still refused and left in place | `activate.sh`, `rollback.sh`; disposable-checkout test |
| 16 | No reader-facing record of what was retrieved travelled with a delivery (open question 9, partly). | `deliver.py` copied four files | `deliver.py` writes `research-ledger.md` (source, retrieval time, currency statement, live re-check, claims supported from the Verification Log) into the run and the delivery | `deliver.write_ledger()` |

### Tests added (all synthetic; `tests/fixtures/valid-run/research-pages/` and `tests/fixture_server.py`)

`test_readiness.py`: 76 tests, all passing on 2026-09-24 (about 2.5 minutes; 67 before the
independent review, 74 after round 1, 76 after round 2). New: research stage
completes and offline never does; missing, reused (nonce, run_id, before opening), stale,
timestamp-only, edited-text, and excerpt-absent evidence; fetch-tool refusals (excerpt not on page,
unavailable source, 404, marker absent, no legislation status, short excerpt, duplicate id, real run
never rewrites a reserved host, init refuses to reopen); unavailable authority at the live check
blocks delivery and copies nothing; changed law detected at the live check (`leg-changed` tree);
wrong jurisdiction refused, federal accepted; enacted-not-effective, proposed, and future
effective-date refused, and a row relying on such a record refused at the gate; legal rows need
this-run evidence (recorder and gate, including the pre-draft record); unsupported client claims
(no `evidence_ids`, wrong kind, first-party page changed); incorrect citation URL has no evidence;
unreadable export and render-wrapper failure; delivery writes the research ledger; nonce rotation
invalidates every record; marker-only drift at the live check; the `max_age_days` boundary (13 days
23 hours passes, 14 days 1 hour is stale); a legal record needs the page's marker or a declared
reason; an excerpt equal to the marker or a page without the cited section identifier is refused;
neutral jurisdiction labels other than federal do not bypass the check; declared link destinations
need direct records; the fixture flag must be a boolean. Baseline suites unchanged: hooks 8 and 6,
candidate situational 38. The fixture's `accessed` values are stamped
with the test day so fixture rows never predate the run's opening.

### Fresh integration tests (2026-09-24; Git-ignored run directories)

- Coordinator retrieval: `runs/sterling-fl-m008-wisconsin-2026-09-24-integration/` — 13 live
  retrievals (eight Wisconsin statutes with the "updated through 2025 Wis. Act 247 ... Published
  9-4-26" marker, three Sterling first-party pages, two link destinations); INTAKE-COMPLETE;
  RESEARCH-COMPLETE with every record live-verified; the Wisconsin pricing page's fee text did not
  extract (script-rendered), so no pricing-page fact was approved. `coordinator-log.md` in the run.
- Controlled refusal: `runs/refusal-test-wisconsin-2026-09-24/` — failed 2025 SB 161 recorded as
  `proposed`, Fla. Stat. § 61.13 recorded with jurisdiction Florida, § 767.999 fetch refused (HTTP
  404, nothing written); gate INCOMPLETE with `LEGISLATION_NOT_EFFECTIVE`,
  `RESEARCH_JURISDICTION_MISMATCH`, `RESEARCH_MISSING` for S2-S4 and citations 2-4.
- Codex headless (`codex exec`, codex-cli 0.155.0-alpha.16.3, from the repository root): (a)
  `legal_reviewer` under `--sandbox read-only` asked to verify one § 767.001 claim live: the agent
  reported the official URL inaccessible to its web fetch and the in-app browser denied by security
  policy, returned `Unverifiable` with an empty excerpt, and filled nothing from memory (correct
  refusal; live research BLOCKED on this host). (b) `editorial_reviewer` under `--sandbox
  read-only` read `run.json`, `client-facts.md`, and `research/EV9.*`, confirmed the phone string
  is present in the retrieved text, wrote nothing. (c) `content_writer` under `--sandbox
  workspace-write` created exactly the one requested file listing the 13 records; `git status`
  unchanged before and after; the research gate still RESEARCH-COMPLETE. Each spawn was preceded by
  one `collab spawn failed: no thread with id` router error, as on 2026-09-23. Evidence:
  `runs/sterling-fl-m008-wisconsin-2026-09-24-integration/smoke-logs/codex-*`.
- Claude `legal-reviewer` on the refusal run (live WebFetch from this session): R1 Confirmed with a
  verbatim § 767.001(5) excerpt bound to EV1; R2 Correction-needed bound to EV2 (SB 161 failed
  3/23/2026, companion AB 151 also failed, current § 767.41(4)(a)2. has no presumption); R3
  Correction-needed bound to EV3 (2025 Florida Statutes, not Wisconsin); R4 Unverifiable with no
  excerpt (HTTP 404 for both fetchers). The recorder accepted the record; the gate refused with
  `LEGISLATION_NOT_EFFECTIVE`, `RESEARCH_JURISDICTION_MISMATCH`, `RESEARCH_MISSING`,
  `REVIEW_VERDICT_BLOCKING`, `LEGAL_PREDRAFT_COVERAGE`, and `LEGAL_LOG_UNVERIFIED`. This is the
  proof of correct refusal when verification fails, produced by the actual agent against real
  authorities. One live re-check of EV1 timed out (transient); `fetch()` now retries a transport
  failure once, never an HTTP status.
- Claude `legal-reviewer` on the fresh Sterling run (pre-draft C1-C9, live WebFetch of all eight
  record URLs plus five subsection windows and three 2025 Act pages): eight rows Confirmed with
  narrowed wording (nine Confirmed rows across eight records, because C2 was split and EV2 carries C2a and C3), each bound by a verbatim excerpt; planned claim C2 split, its
  sex/race, order-of-importance, and written-reasons part Flagged because the § 767.41 section page
  renders a window ending at sub. (4)(cm); five findings (L1 "not ranked" needs the § 767.41(5)(bm)
  paramount-safety qualification; L2 EV2 does not contain sub. (5)-(6); L3 C3's "only" contradicted
  at the temporary-order stage by § 767.225(1)(a); L4 C5 omits § 767.117(1)(c); L5 terminology note
  on "marital property"). Verdict ready-with-revisions. The recorder accepted the record with every
  row's excerpt found in the stored text; the gate reports coverage for all eight citations and no
  unverified row. The agent also found two coordinator-side record defects, fixed the same day: the
  coordinator's setup script had attached the first History line in the page window (a neighbouring
  section's) as `amendments_note` for six records, and the section pages omit later subsections. All
  eight records were re-fetched with the section's own History line (or none, stated), the misused
  `effective_date` moved to `current_through_date`, and subsection records EV14 (§ 767.41(5)(am)) and
  EV15 (§ 767.41(6)(a)) were retrieved at the agent's request. `research_fetch.py` now refuses an
  amendments note that is not in the retrieved text; extraction by the section's own marker is
  coordinator practice recorded in the coordinator skill.

### Independent review of the research-first change (read-only `seo-reviewer`, 2026-09-24, round 1)

One blocker, ten material items, eight optional items. Dispositions, each checked against the code:

| Finding | Disposition |
|---|---|
| B1: the completion claim for "actual agents in Claude" was unsupported until a real `legal-reviewer` payload with `evidence_id`/`excerpt` passed the recorder | Cleared during the review: the refusal-run record and then the fresh-run pre-draft record (above) were both accepted by `record_review.py` and evaluated by the gate. |
| M1: "fetched in this run" overstated; the layer proves nonce/run-id/time consistency plus excerpt presence, not authenticated provenance (the run directory is writable) | Accepted; reworded in the readiness notice, README, `workflow-rules.md`, `cw_research.py` docstring, the ledger header and footer, the record notice, the schema comment, and `AGENTS.md` ("checked mechanically for retrieval, consistency, and presence"); `research/` added to the writer's instruction-only list. |
| M2: a legal record could carry no page-bound currency evidence | Accepted; a legal authority now needs `--currency-marker` present on the page or `--no-currency-marker "<reason>"` recorded and printed in the ledger; a hand-edited record without either is `RESEARCH_INVALID`. |
| M3: `effective_date` conflated the compilation's current-through date with the provision's effective date, and the ledger printed it as "effective" | Accepted; `current_through_date` added, declared alongside the marker (not checked against its text); `effective_date` is now the provision's own date only; the ledger prints them separately; schema, tests, and the integration run's records updated. |
| M4: jurisdiction and status are declaration-consistency checks; `n/a` bypassed the jurisdiction rule; an excerpt could be page chrome | Accepted: neutral labels narrowed to `federal`/`united states`; a section identifier from the cited authority must appear in the retrieved text (fetch and gate); an excerpt equal to or inside the currency marker is refused; docs say "declared ... checked for consistency". Correctness stays the legal reviewer's judgment. |
| M5: the Codex consequence was unstated | Accepted; README and this record now say the Codex path is not deliverable for any page with a legal claim until open question 12 is decided. |
| M6: the Claude reviewer's WebFetch is a processed rendering, so the verbatim binding is to the coordinator's stored text | Accepted; stated in the Claude host note of the legal-reviewer adapter and in the README limitations; open question 13 records the residual. |
| M7: stale statements (README "AGENTS.md unchanged"; usage string; compatibility status line; evidence paths) | Accepted and corrected; evidence paths verified to exist before commit. |
| M8: "replace placeholder-first" resolved by precedence override rather than editing the five imported files | Reported as a user decision in the completion report (override-by-precedence with the imported files preserved, or attributable local adaptations to the five files with the backup as fallback). |
| M9: link destinations recorded voluntarily, never required or redirect-checked | Accepted; `run.json` `link_destinations` requires a `link-destination` record per URL with zero redirects and a final URL equal to the cited URL; the fetch tool refuses a redirecting destination. |
| M10: untested mechanisms (nonce rotation, marker-only drift, `max_age_days` boundary) | Accepted; three tests added plus tests for the M2, M4, and M9 rules and the fixture-boolean check. |
| O1-O6, O8 | Adopted: fixture flag must be a boolean at intake; `text_extraction` enum checked; ledger rows deduplicated by evidence id and claim; `LEGAL_PREDRAFT_COVERAGE` matches on the same canonical URL set as the recorder (including the record's final URL); wording "before the day the run opened"; operator guidance for a transient `RESEARCH_UNAVAILABLE` (retry later, never `--offline`) in the README; reserved-host suffix match requires a dot boundary. |
| O7: refuse a reviewer excerpt identical to the record's | Not adopted: the failed-bill page in the refusal run has almost no other quotable text, so the rule would force awkward quoting without closing the gap; kept as open question 13. |

Reviewer disagreement preserved: whether override-by-precedence satisfies "replace" (M8) is the
user's call; the WebFetch limitation (M6) is inferred from the tool contract, not observed inside the
subagent. The reviewer's candidate lessons ("when a gate binds operator-declared metadata, check for
neutral values that bypass the rule and whether the docs say declared rather than verified"; "re-check
modification of key files at the end of a long read-only review") are recorded here as hypotheses for
the `seo-reviewer` role, not promoted.


### Independent review round 2 (read-only `seo-reviewer`, 2026-09-24)

No blocker; six material and seven optional items. Dispositions:

| Finding | Disposition |
|---|---|
| M-1: the refusal-run artifacts were produced before the currency-marker rule and would not reproduce under the current code | Confirmed. EV1-EV3 re-fetched under the current rules (EV2 and EV3 with a declared `--no-currency-marker` reason), the same real reviewer payload re-recorded (`--force`; the earlier record is kept under `reviews/superseded/`), and the gate re-run live: INCOMPLETE with `LEGISLATION_NOT_EFFECTIVE` (EV2), `RESEARCH_JURISDICTION_MISMATCH` (EV3), `RESEARCH_MISSING`, `REVIEW_VERDICT_BLOCKING`, `LEGAL_PREDRAFT_COVERAGE`, `LEGAL_LOG_UNVERIFIED`. The refusal run's `readiness-report.json` is now current-code evidence. |
| M-2: an `--offline` check had overwritten the integration run's live `research-report.json` | Confirmed and fixed: offline checks now write `*.offline.json`; the live report was regenerated (15 of 15 records live-verified, `live_checked: true`); test `test_offline_check_writes_a_separate_report`. |
| M-3: the section-identifier rule accepted a bare digit (and cannot tell a TOC or cross-reference page from the section) | Dotted section numbers are now required when the citation has one; bare numbers apply only to citations without a dotted token. The TOC and cross-reference residual is stated in the code docstring and open question 13; the legal reviewer's check that the operative subsection is inside the stored text remains the guard. Test case added. |
| M-4: EV14 and EV15 carried a truncated History line that passed the substring check | Confirmed: the setup script's 600-character cap truncated it. `--amendments` must now run to the end of its line in the retrieved text; EV14 and EV15 re-fetched with the complete line (ending "2025 a. 24 s. 93; 2025 a. 81."). Test case added. |
| M-5, M-6: remaining overstatement in the coordinator skill; "declared" and current-through vocabulary missing in review criteria, README, command reference, and schema ("bound to the marker") | Corrected on each surface named. |
| O-1: link-destination shape accepted a missing `redirects` or `final_url`; marker and reason both present | Fixed in `validate_record_shape`; test extended. |
| O-3: "eight Confirmed rows" | Corrected to nine rows across eight records. |
| O-4: "before the day the run opened" wording | Applied in the rules and coordinator skill. |
| O-6: the recorder did not check a row's record for run id, opening time, or age | Fixed in `legal_log_problems`; test `test_recorder_refuses_rows_bound_to_stale_or_foreign_evidence`. |
| O-2, O-5, O-7 | O-2: integration EV9-EV13 keep the earlier notice text (mixed state recorded here; their rules are unchanged). O-5: EV8's coordinator excerpt is a heading; recorded as an open-question-13 example (the reviewer's row quotes operative text). O-7: row 8 wording updated. |

The reviewer's candidate lesson ("when a fix changes a recorder or gate, re-run the gate on every run
directory cited as evidence and cite the regenerated report; a report produced before the fix, or
overwritten by a later offline run, is evidence about a different code state") is verified by M-1 and
M-2 in this task and is carried into the learning pass.

### Fresh Claude end-to-end run to READY (2026-09-24)

`runs/sterling-fl-m008-wisconsin-2026-09-24-integration/` (Git-ignored), every stage run with the
actual Claude agents from this session and every legal row bound to research retrieved in the run:

| Stage | Agent | Result |
|---|---|---|
| Research | coordinator, `research_fetch.py` | 15 records (8 statutes, 2 subsection windows, 3 firm pages, 2 link destinations); RESEARCH-COMPLETE, 15/15 live-verified |
| Pre-draft | `legal-reviewer` | 9 Confirmed rows across 8 records, 1 Flagged; L1-L5; ready-with-revisions |
| Draft | `content-writer` (second dispatch after a session interrupt) | 1,647 words; generator and both validators exit 0; five overreaches from the interrupted attempt narrowed |
| Checkpoints | `legal-reviewer`, `editorial-reviewer` in parallel | legal 32/34 Confirmed, L1-L5 fixed-verified, L6-L11 new; editorial E1-E6 (E1 major: FL-M039 overlap); both ready-with-revisions |
| Correction | `content-writer` | all ids applied; coordinator decisions: L11 remove the hourly-billing sentence (fee scope unverified), E3 keep client-facts unchanged (re-pinning would stale the pre-draft record); 1,563 words |
| Finals | `legal-reviewer`, `editorial-reviewer` | legal ready, L1-L11 fixed-verified, 43 rows all Confirmed; editorial ready-with-revisions (E2 minor, E7 note, E8 minor open; E1/E4/E5 fixed-verified; E3/E6 withdrawn) |
| Mechanical, render | `mechanical_qa.py`; coordinator viewed all six pages twice | pass; render r0 pass with minor R1, render r1 pass |
| Delivery | `deliver.py` | READY; live re-verification of all 15 records; five files incl. `research-ledger.md` |

Refusals exercised on real output in this run: the recorder refused the editorial final while open
finding E2 still quoted a sentence no longer in the draft (the reviewer re-anchored it); the pre-draft
reviewer declined to Confirm propositions whose operative subsection was outside the stored text
(Flagged with a record request, cleared by EV14/EV15). The page is a test artifact: not published and
not handed to the client; attorney review, a client decision on fee scope, and the FL-M039 ownership
question would precede any hand-off. Open minors E2 (one 31-word sentence), E8, and note E7 remain
visible in the records.

### Disposable checkout (install and rollback)

`git worktree add --detach` at HEAD plus the working changes, then `npm ci` for the candidate:
activation created exactly the eight Git-ignored entries (five symlinks, three byte copies) and left
`git status` clean; `build_adapters.py --check`, both hook suites, and the candidate suite passed
there; the readiness suite ran 67 tests of which 35 passed and 32 failed closed at the render step
because the Git-ignored LibreOffice and PyMuPDF installs are absent in a fresh checkout (the README
activation steps now say so); a foreign `.codex/agents/legal_reviewer.toml` was refused by
activation and left in place by rollback; full rollback removed all eight entries with a clean
`git status`. The worktree was removed afterwards.

### Fetch-tool limits found (fail closed, not bypassed)

`research_fetch.py` uses this machine's Python TLS trust and does not extract PDFs: revisor.mn.gov
fails the handshake under Homebrew Python 3.14 / OpenSSL 3.6.3 (system Python and curl succeed);
legislature.mi.gov's certificate chain does not validate; ilga.gov returns 403 to automated
clients; a PDF authority yields no text. Each is `RESEARCH_UNAVAILABLE`; the affected claims stay
unverified. flsenate.gov, codes.ohio.gov, and docs.legis.wisconsin.gov fetched normally.

## Open questions (UNRESOLVED; not guidance)

1. Resolved 2026-09-23: a source keeps one number and is cited again wherever it supports a
   later material claim (integrated from the comparison patch).
2. Whether the bracket-token placeholder rule should exempt an allowlist (for example
   "[sic]"). No legitimate bracketed prose appears in the situational contract today.
3. Resolved 2026-09-23 for family-law page kinds: legal and editorial checkpoints and the legal
   pre-draft record are required by `required_review_floor()`; a checkpoint kind is satisfied
   by presence and shape. Whether other page kinds should require checkpoints stays open.
4. Codex cannot restrict a custom agent's tools or spawning by configuration (only
   `sandbox_mode`); the no-delegation rule is instruction-only there. Revisit when the Codex
   custom-agent format gains a tool or depth restriction.
5. Resolved for the pilot 2026-09-23: the situational candidate carries its own hash-pinned
   render wrapper on the installed renderer release. The production Core wrapper still fails
   closed and is a separate production repair.
6. `render_draft.py` supports only the FL-M008 manifest shape. Extending the workflow to
   another page type needs a renderer for that skill's manifest (or a skill that writes
   Markdown directly) before parity checks can apply.
7. Whether `ready-with-revisions` with only minor findings should be deliverable is a
   coordinator preference; the pilot allows it and reports the open minors.
8. Closure identity: `fixed-verified` requires the closing record's agent to equal the raising
   agent's name, so a finding raised by `legal-reviewer` (Claude) cannot be closed by
   `legal_reviewer` (Codex) or by a named attorney under `--runtime human`. Whether same-role
   closure should suffice for mixed-host or attorney rechecks is undecided (reviewer round 2,
   2026-09-23); until decided, the raising agent rechecks.
9. `deliver.py` copies the export and the machine-readable reports but produces no reader-facing
   cover note, so the brief basis, attorney-review requirement, and client confirmation items do
   not travel with a hand-off unless the coordinator writes them by hand (seo-reviewer B1,
   2026-09-23). Whether the run should declare disclosures in `run.json` for the delivery step to
   render is undecided.
10. The situational candidate's classification gate screens the parent hub and procedural pages
   but not sibling situational nodes in other clusters that share the page's defining term
   (seo-reviewer M1: FL-M008 versus the live FL-M039 High-Conflict Custody page). Whether the
   intake or the editorial checkpoint should require that screen, and where the shared statutory
   explanation should live, is undecided; hypothesis from one run.
11. `research_fetch.py` cannot record authorities behind TLS chains this Python install rejects,
   sites that block automated clients, or PDF-only publications (2026-09-24). Whether to add a
   pinned certificate bundle, a browser-based retrieval path, or PDF text extraction, and how each
   would keep the fail-closed property, is undecided.
12. Codex headless `legal_reviewer` cannot fetch the web under the read-only sandbox on this host
   (2026-09-24). Whether the interactive Codex session, a network-enabled sandbox policy, or a
   coordinator-side retrieval handoff should carry live research on Codex is undecided.
13. Excerpt selection is a judgment: a reviewer may quote the coordinator's own excerpt without
   reading further, and an excerpt taken from page chrome rather than statutory text would pass the
   mechanical check. Whether to require the reviewer's excerpt to differ from the record's, or to
   require two independent excerpts per authority, is undecided (2026-09-24).

## Refinements integrated from `SEO_Dept_Refined_Content_Skills_v1.patch` (2026-09-23)

The patch (32 files under `skill-releases/family-law-content-pilot-v1/`, not applied) was treated
as comparison material. Its `INTEGRATE.md` itself asks for one coordinator and one readiness
implementation; the existing pilot stays canonical and the useful refinements were folded into it.

### Adopted

| Patch idea (source) | Integration in the existing pilot | Enforcement |
|---|---|---|
| Legal verification before drafting (C04 step 2, F01) | New `legal-predraft` record: the legal reviewer verifies every planned material claim live and returns a Verification Log bound to the pinned sources; the writer may draft only `Confirmed` claims; every `run.json` citation needs a `Confirmed` row | `required_review_floor()`, `LEGAL_PREDRAFT_COVERAGE`, `LEGAL_LOG_UNVERIFIED`; roles and candidate legal skill updated |
| Required section checkpoints during drafting (C04 step 3) | Legal and editorial checkpoints are required for family-law page kinds (presence and shape); the `checkpoints.skipped_reason` escape was removed | `required_review_floor()`, `REVIEW_MISSING` |
| Independent final review of the complete document (C04 step 4) | Already present; wording aligned (every occurrence including title, metadata, FAQs, CTAs) | unchanged gate |
| One source identity per canonical URL, repeated citations keep their number (E04, F08) | Generator, both candidate validators, `render_draft.py`, and `cw_common.citation_issues` accept repeated `[n]`; first-appearance order and one Sources row per source kept | candidate suite cases; `citations-*` checks |
| No arbitrary source maximum; coverage governs (E04, situational step 5) | Six is a readability guideline; seven or more require a recorded coverage rationale in the manifest and in `run.json`; twelve is a sanity limit. The V2 architecture states no source count, so the architecture contract is unaffected. Because `docs/seo-skill-compatibility.md` forbids removing a validation requirement, the baseline hard cap is replaced rather than dropped: rationale plus `LEGAL_PREDRAFT_COVERAGE` (every citation needs a Confirmed pre-draft row) plus the sanity limit | generator; `SOURCE_CEILING`, `LEGAL_PREDRAFT_COVERAGE` |
| Evidence-based client specificity; neutral accurate law acceptable (E02, F10, editorial rubric) | Editorial role and candidate updated; rubric adapted into `references/editorial-rubric-pilot.md` with decision examples | reviewer judgment; role text |
| Required render gate with per-page evidence (C05, records.md, output-qa) | New `render-final` record written by `scripts/render_inspect.py`: pinned renderer (observed hash recorded), every page image and its extracted text hashed, per-page observation that must quote three consecutive words present on that page, bound to the export hash; a failed inspection is repaired by re-export and a fresh render, not by carrying findings; delivery refuses without a current passing record | `RENDER_UNINSPECTED`, `RENDER_EVIDENCE_MISMATCH`, `RENDER_FAILED`, `REVIEW_STALE` |
| Evidence-based closure (C06, F02) | Finding `category`; protected categories (`legal-accuracy`, `citation`, `client-fact`, `promise`) close only by the raising reviewer's `fixed-verified` with `corrected_text` (20+ characters, different from the targeted passage, present in the draft) or the reviewer's own withdrawal; severity, category, and raising reviewer are fixed by the first record (`FINDING_DRIFT`); coordinator acceptance is recorded only through `dispose_finding.py`, never for protected or blocking findings | `evaluate_reviews()` closure rules; recorder; `dispose_finding.py` |
| Export reconciliation rejects fields, revisions, hidden text (CHANGELOG refinements) | `export-clean` mechanical check | `EXPORT_UNCLEAN` |
| Repair and validate the renderer dependency without bypassing checks (user item 4) | Candidate-owned `render-situational.sh` and `renderer-tools.lock.json` pinned to the installed release 26.905.11957 by SHA-256, revalidated by reading the script and rendering an existing six-page FL-M008 DOCX; fail-closed behaviour re-tested (non-empty output dir, tampered hash) | wrapper; `render_inspect.py` |

### Excluded, with reasons

| Patch element | Reason |
|---|---|
| `scripts/content_gate.py`, `job.json` / `draft.json` schema, `validate_release.py` | A second controller and a second record schema. The existing `run.json` + generator manifest + `readiness_check.py` remain the single implementation; equivalent checks were added where missing |
| python-docx `build` exporter | The FL-M008 route already has a tested generator with the V2 link contract; a second exporter would fork the artifact path |
| `reviewer_context_id` independence check | Claude's Agent tool exposes no context id to the subagent; the pilot records agent name, adapter file, and hash instead and states that it cannot authenticate who produced a record |
| `READY_FOR_HUMAN_REVIEW` label | The pilot's `READY` already carries the same meaning in every report notice; renaming would churn tests and docs without changing behaviour |
| Link policy by purpose with `repeat_editorial` exceptions (E05) | The baseline skill's single-placement rule for internal links is retained in the FL-M008 local contract (one parent-hub link, one `FL-M004` bridge, one CTA); V2 governs which targets may be linked, not placement counts, and there is no evidence yet for placement exceptions. The limits table already permits repeated citations and CTA sentences. Kept as an open question for other page kinds |
| Five separately named `seo-pilot-*` skills | The existing uniquely named candidates cover the same roles; adding a second skill set would create duplicate names and two policy sets |
| Editorial rubric's relaxation of the three-sentence paragraph rule to "diagnostic" | The FL-M008 generator and validators enforce the baseline three-sentence rule; relaxing it is a candidate change with no evidence yet |
| Publisher metadata kept out of the consumer DOCX (F09/E06) | The FL-M008 generator's publisher block before the H1 is the baseline artifact the client team reviews; the readiness check already excludes everything before the H1 from parity and reads metadata separately. Changing the artifact shape is a Core-route decision |

### Reconciliation of the MemPalace lesson with this record

On 2026-09-23 the coordinator saved one `REUSABLE LESSON` drawer in the `seo_dept`
`shared-methodology` room (`drawer_seo_dept_shared-methodology_934b8897e054f3d888923a41`,
`source_file` pointing here). This record previously described the same lesson as "recorded here
as a hypothesis and not promoted", which read as a contradiction. The precise state is:

- The lesson is retained in MemPalace for cross-session continuity with verification state
  "scenario-checked twice within one task; not yet exercised on a later task". A MemPalace drawer
  is reference evidence, not an instruction (`AGENTS.md`, "MemPalace recall and retention").
- It has not been promoted into any owning instruction, skill, checklist, or validator
  (`AGENTS.md`, `learning/README.md`, reviewer definitions). Promotion needs the
  `learning/README.md` cycle and a further natural case.
- The round-2 recheck narrowed the lesson ("re-walk the operator procedure whenever a repair adds
  gate conditions"); that narrower form is documented above and not saved separately.

"Unpromoted" therefore means "not an instruction"; "saved" means "retrievable evidence". Both are
true.

A second drawer was saved on 2026-09-23 after the Sterling end-to-end run
(`drawer_seo_dept_shared-methodology_526d63d2d8ad00a009288c08`, `source_file` pointing here):
`REUSABLE LESSON`, a plain-language gloss of a legal term is itself a legal claim and must not name
a party, actor, or standard the statute does not name; reviewer-proposed wording carries no
verification of its own. Verification state recorded in the drawer: execution-verified on one run
(the E5 gloss became L15 and was cured against live authority); hypothesis until a second run. It
is likewise retrievable evidence, not an instruction; promotion into the candidate legal and
editorial skills follows `learning/README.md`. The reviewer-proposed candidate lessons from this
run that were not saved (recheck method after a hash change; quote a whole lettered paragraph
when it creates a presumption; state which word counter gates a run) are recorded in the run's
review records and in the end-to-end section below as hypotheses only.

## End-to-end client run: Sterling Lawyers FL-M008, Wisconsin (2026-09-23)

One complete run of the pilot on a real client page, as the second task requested. The run
directory `runs/sterling-fl-m008-wisconsin-2026-09-23/` and the delivery directory are
Git-ignored (client material); `coordinator-log.md` in the run is the coordinator's timeline.
Nothing was published. The deliverable is a DOCX review copy for attorney and client review.

**Scope and inputs.** Sterling Lawyers, LLC (sterlinglawyers.com), Wisconsin, node FL-M008
(Practice-Area Situational Page, high-conflict divorce), retained URL
`/wisconsin/divorce/high-conflict-divorce/`; voice `sterling-voice` by exact domain route;
architecture links per V2 (parent hub FL-PA-DIV, bridge FL-M004, consultation CTA), each
destination checked live (200, no redirect, self-canonical). Brief basis, disclosed in the run:
no client-approved brief document exists under `clients/sterling/`; the run used the V2 node
brief, the voice skill as the approved brand source, and `sources/client-facts.md` compiled from
the voice skill and first-party pages checked live on 2026-09-23, which states that nothing in
it was confirmed by a client call, a signed brief, or an intake test.

**Sequence and outcome.**

| Stage | Result |
|---|---|
| Pre-draft legal verification (Claude `legal-reviewer`, live fetch of eight Wisconsin statutes, banner "Published 9-4-26") | 10 planned claims confirmed only in narrowed wording; two planned claims were wrong (hybrid abuse-presumption standard; harassment ban attributed to § 767.225 instead of § 767.117); supplementary row for § 767.117 recorded as predraft round 1 |
| Draft (Claude `content-writer`) | 1,664 consumer-copy words, eight sources cited 19 times in first-appearance order, generator and both validators exit 0; two earlier attempts failed the word ceiling |
| Checkpoints | Legal: ready-with-revisions, L1-L9 fixed-verified with `corrected_text`, L10-L12 minor, L13-L14 notes. Editorial: not-ready, E1 major (legal name absent from body), E2 major (unsupported frequency claim), E3-E10 minor, E11-E12 notes |
| Render round 0 (coordinator viewed all six pages) | pass; one minor pagination artifact |
| Correction pass (writer) | 1,697 words; every required and minor finding applied; three optional notes left for budget |
| Finals round 0 | Editorial ready-with-revisions (E1-E10, E12 fixed-verified; E11 withdrawn; new E13, E15 notes; E14 minor: the editorial reviewer's own proposed gloss named a rebutting party). Legal not-ready: L15 major, the same gloss, verified against § 767.41(2)(b)2.c and § 903.01; 38 log rows, 37 Confirmed, 1 Correction-needed |
| Repair round 2 (writer) | one sentence; word-neutral; writer diffed against the round-0 hash and re-matched all 22 `corrected_text` strings |
| Finals round 1 | Both ready. Legal: L1-L12 and L15 fixed-verified against the final hash, L13-L14 withdrawn, 38 of 38 rows Confirmed. Editorial: E1-E10, E12, E14 fixed-verified; E13, E15 open as note-severity optional improvements |
| Mechanical round 1; render round 2 (all six pages viewed) | pass; pass (R1 resolved by re-export, R2 minor phone-number line wrap in the review copy) |
| Readiness and delivery | READY with all seven required records current and hash-bound; `deliver.py` copied four files to the ignored delivery directory |

**Distinguished results.**

- Successful delegation: Claude `content-writer` (three dispatches), `legal-reviewer` (five:
  pre-draft, supplementary pre-draft, checkpoint, final, recheck), `editorial-reviewer` (three).
  Every reviewer wrote nothing; the writer wrote only inside the run. Codex was not used for
  this run; its delegation evidence is the headless smoke tests recorded below.
- Successful rejection: the gate refused delivery at every intermediate state with the expected
  reasons (`MECHANICAL_FAILED` for the missing legal name, `REVIEW_MISSING`, stale
  `fixed-verified` after each draft-hash change, `REVIEW_VERDICT_BLOCKING` and
  `LEGAL_LOG_UNVERIFIED` for L15); `render_inspect.py --attest` refused an attestation whose
  observation quoted the H1 with an attached quote mark and comma (a matcher defect, fixed
  below, not a rule change).
- Successful end-to-end completion: READY reached after two repair rounds, the pilot's cap.

**Defects the run exposed in the pilot, each fixed with a test.** Recorder crash on a pre-draft
record; supplementary pre-draft record (round 1) outranking the round-0 checkpoint in gate
order; observation matcher defeated by punctuation attached to words; candidate template page
contract still worded for Florida. Recorded in the review table above.

**Decision (coordinator).** The pinned generator's consumer-copy word count governs the skill's
word target (1,697 of 1,700 here). The mechanical parity counter reports 1,702 for both draft
and export because it tokenizes with a Unicode word regex while the generator uses an ASCII
one; the parity count exists to compare draft and export with each other and is informational
for the ceiling. No code change; stated here and in the README.

**Independent SEO review of the deliverable (read-only `seo-reviewer`, 2026-09-23).** READY is
supported by the records (every required record bound to the final hashes; blocking and major
closures by the raising reviewers with `corrected_text` present in the draft; the reviewer viewed
all six round-2 pages itself). Dispositions:

| Finding | Disposition |
|---|---|
| B1 (hand-off blocker): the delivery folder carried no reader-facing disclosure of the brief basis, attorney-review requirement, or client confirmation items | Fixed: `COVER-NOTE.md` added to the delivery folder and the run (Git-ignored with them). Scope was the hand-off only; READY is unaffected. Open question 9 records the tooling gap |
| M1: Sterling's live High-Conflict Custody page (V2 FL-M039) covers the same joint-custody presumption, sole custody, abuse presumption, guardian ad litem, and mediation material; `excluded_intents` listed only the hub and the contested procedure | Accepted as a pre-publication dependency: decide which page owns the § 767.41 explanation, trim this page's custody-law depth, add the sibling to `excluded_intents`. Needs a content round beyond the pilot's two-repair cap, so it is recorded (cover note; open question 10) rather than applied; a manifest edit now would invalidate every hash-bound record |
| M2: no Search Console baseline or post-publication check for replacing a roughly 3,500-word indexed page with 1,697 words | Accepted as a measurement limitation; steps in the cover note |
| M3: the fixed-total fee sentence and the single Legal Team tier are accurate to the approved first-party sources but incomplete against the live pricing page (monthly starting figure with a total range; two Legal Team tiers) | Accepted as client confirmation items in the cover note; nothing asserted |
| M4: two gate scripts changed mid-run | Disclosed above (record ordering; observation matcher), each with a regression test; suites green after the changes |
| O1-O6 (answer-first opening; a causal connector in the firm sentence; `voice-route` labelled `kind: "brief"` in run.json; metadata fine; R2; readiness report shows the supplementary pre-draft as "current") | Recorded for a later round; O3 left unchanged to preserve the delivered `run.json` hash |

Reviewer disagreement preserved: whether the custody-law depth is a defect or the consequence of
correctly narrowed legal wording (exceptions must stay); and the live page's word count is an
estimate from two sources that differ by about 1,000 words.

**Remaining limitations, to be stated in any hand-off.** Attorney review before publication is
still required (every legal record says so). No signed client brief. Client confirmation items
surfaced by the editorial reviewer: the voice skill describes Contested pricing as
"monthly-style starting figures with total ranges" while the approved live-page sentence says
the total cost is defined before work starts; and "how a fixed fee fits your case" implies the
strategy session covers fee scope, which the client facts do not publish. Open note-severity
items E13, E15, and R2 are visible in the records. The interactive Codex session remains
untested.

## Host verification record (2026-09-23)

Installed versions: Claude Code 2.1.277 (`~/.local/bin/claude`); Codex CLI 0.155.0-alpha.16.3
(bundled with the VS Code extension `openai.chatgpt-26.917.62051`; the ChatGPT desktop app ships
0.150.0-alpha.8 and the older extension 0.154.0-alpha.6.2). `codex features list` reports
`multi_agent` stable and enabled and `hooks` stable and enabled.

### Claude Code

- Discovery: a fresh headless session (`claude -p`, model haiku, no tools) listed its Agent
  types as `claude, content-writer, editorial-reviewer, legal-reviewer, Explore,
  general-purpose, lead-origin-map, Plan, seo-reviewer, statusline-setup`. The three pilot
  agents are symlinks in `.claude/agents/`, so symlinked agent files are followed.
- Skill: a fresh headless session invoked with `/content-workflow ...` quoted the skill's first
  heading and the three subagent names from its host table, so the symlinked skill directory is
  followed and the `disable-model-invocation` frontmatter is compatible (the description is
  hidden from the model; the user can still invoke it).
- Live delegation, content-writer: a fresh headless session (model sonnet, permission mode
  acceptEdits) spawned `content-writer` (`subagent_stats.by_type = {"content-writer": 1}`). The
  agent verified all four skill pins and five source pins by SHA-256 with individual
  `shasum -a 256` calls, identified the pinned voice brief for the unrouted domain without
  opening any voice skill, wrote exactly `changes.md` in the run directory, and returned the
  four required items. One permission denial occurred: the sandbox rejected a batched `for`
  loop ("Contains simple_expansion"); the agent re-ran one command per file. Raw output:
  `runs/smoke-gomez-nunez-2026-09-23/smoke-logs/writer.json` (Git-ignored).
- Live delegation, legal-reviewer: a fresh headless session (model sonnet) spawned
  `legal-reviewer` (`subagent_stats.by_type = {"legal-reviewer": 1}`). It read the run, the draft,
  the three source notes, and the pinned candidate legal skill; WebFetch and WebSearch were
  denied at the permission layer (headless mode cannot prompt), so it classified every cited
  claim `Unverifiable`, returned verdict `not-ready` with two blocking and one major finding
  (fixture JSON, `fixture: true`), and confirmed it wrote no file. In an interactive session the
  coordinator approves WebFetch; the fixture URLs would still fail because `.example` is reserved.
- Live delegation, editorial-reviewer: a fresh headless session spawned `editorial-reviewer`
  (`by_type = {"editorial-reviewer": 1}`), read only the pinned voice brief for the unrouted
  domain (no voice skill opened), and returned `not-ready` with two major findings (the short
  fixture body versus the 1,100 to 1,700 word target; plain-text `[n]` markers in the Markdown
  draft rather than hyperlinked markers) plus one note. No file written.
- Recorder and delivery on the smoke run: `record_review.py` accepted both returned JSON objects
  (every quoted passage was found in `draft.md`) and stamped the draft hash; `mechanical_qa.py`
  passed on the test-only export; `deliver.py` refused with nine reasons: four
  `SKILL_HASH_MISMATCH` (the candidate SKILL.md files were edited after the run pinned them,
  exactly the invalidation the pin exists for), two `FINDING_BLOCKING_UNRESOLVED`, three
  `FINDING_MAJOR_UNDISPOSED`. Nothing was copied. Raw outputs and extracted findings are in
  `runs/smoke-gomez-nunez-2026-09-23/smoke-logs/` (Git-ignored).
- Headless smoke cost: about USD 1.90 across the five sessions (two haiku probes, three
  sonnet delegations).
- The session in which the pilot was built could not see the new agent types (the Agent
  tool's type list is fixed per session); a new session is required after activation.

### Codex

- Static: all three `.codex/agents/*.toml` symlinks resolve and parse with the required
  `name`, `description`, `developer_instructions` fields and `sandbox_mode` set. The Codex
  skill-creator quick validator accepts all four candidate skills; it flags the Claude-only
  `disable-model-invocation` key on the shared `content-workflow/SKILL.md` as an unexpected
  frontmatter property.
- Offline prompt render (`codex debug prompt-input`, no model call): with the shipped
  `allow_implicit_invocation: false`, `content-workflow` is absent from the model-visible skill
  list, which is the intended explicit-only behaviour. Temporarily setting it to `true` made
  the skill appear under root `r5 = /Users/rocketclicks_1/SEO_Dept/.agents/skills` with the
  `disable-model-invocation` key still present, so the symlinked skill directory is followed and
  the extra key does not break Codex parsing. Files were restored byte-for-byte afterward.
  The render does not list custom agents, so agent discovery could not be confirmed offline.
- Live delegation (headless, 2026-09-23, `codex exec --sandbox read-only --ephemeral --json`,
  codex-cli 0.155.0-alpha.16.3, from the repository root):
  - First attempt with the symlinked `.codex/agents/legal_reviewer.toml`: the model tried to spawn
    `legal_reviewer` and Codex core logged `agent type is currently not available`; delegation
    failed. Probes then showed the regular-file project agent `seo_reviewer` and a regular-file
    copy of the pilot adapter both spawned and replied, while the built-in `explorer` did not
    spawn in exec mode. Conclusion: Codex follows symlinked skill directories but not symlinked
    agent files. `activate.sh` now installs the three Codex agents as byte copies of the generated
    adapters (rollback removes an unmodified copy); `build_adapters.py` stays the only authoring
    point.
  - Second attempt after re-activation: Codex spawned `legal_reviewer` (thread
    `/root/legal_reviewer`), which read the smoke draft, reported its H1, heading count, and marker
    form, and confirmed it wrote nothing; the parent wrote nothing. A trailing
    `collab spawn failed: no thread with id` router error appeared after the reply in every
    successful probe and did not affect the result; it is recorded, not explained.
  - Raw evidence: `runs/smoke-gomez-nunez-2026-09-23/smoke-logs/codex-*.{jsonl,txt,err}`
    (Git-ignored).
  - Third and fourth attempts (later on 2026-09-23, same binary at
    `~/.vscode/extensions/openai.chatgpt-26.917.62051-darwin-arm64/bin/macos-aarch64/codex`;
    `codex` is not on `PATH` in this shell): `editorial_reviewer` spawned under
    `--sandbox read-only`, read the smoke draft, reported its H1, heading count, and client-name
    paragraph count, and wrote nothing; no router error this time. `content_writer` spawned under
    `--sandbox workspace-write` "on retry" (the parent's first spawn call logged the same
    `collab spawn failed: no thread with id` router error, then succeeded), read the draft, and
    created exactly the one requested file `smoke-logs/codex-writer-touch.txt`; `git status`
    before and after showed no tracked-file change. Evidence:
    `smoke-logs/codex-{prompt,events,last-message}-{editorial,writer}.*`, `codex-writer-touch.txt`.
    All three Codex agents are therefore verified for headless delegation; the trailing router
    error remains recorded, not explained.
  - No interactive Codex session was used. Remaining instruction for the interactive check: open
    Codex at `/Users/rocketclicks_1/SEO_Dept` on branch `content-workflow-pilot` after
    `sh pilot/content-workflow/scripts/activate.sh`, then send
    `$content-workflow pilot/content-workflow/runs/smoke-gomez-nunez-2026-09-23` and ask it to
    dispatch `legal_reviewer` for a stage-final round-0 review only; confirm in the thread that a
    custom agent named `legal_reviewer` ran and that it wrote no file. Until that succeeds, the
    interactive Codex path is unverified for this workflow.
