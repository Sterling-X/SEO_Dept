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

- `pilot/content-workflow/tests/test_readiness.py`: 40 tests, all passing on 2026-09-23 after
  both independent review rounds (Python 3.14.6, Node 20.20.1, about 27 seconds). The fixture is
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
- Candidate `scripts/test-situational.py`: 34 cases (21 baseline cases unchanged plus 13 new),
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

## Open questions (UNRESOLVED; not guidance)

1. Whether "cite once at first mention" should permit a second hyperlinked reference to the
   same authority on long pages. The pilot enforces once.
2. Whether the bracket-token placeholder rule should exempt an allowlist (for example
   "[sic]"). No legitimate bracketed prose appears in the situational contract today.
3. Whether checkpoint reviews should be mandatory rather than skippable with a recorded
   reason. The pilot requires only the three final reviews; a checkpoint kind added to
   `reviews.required` is satisfied by presence and shape.
4. Codex cannot restrict a custom agent's tools or spawning by configuration (only
   `sandbox_mode`); the no-delegation rule is instruction-only there. Revisit when the Codex
   custom-agent format gains a tool or depth restriction.
5. The pinned Core renderer fails closed on this machine, so rendered-page inspection of any
   DOCX remains unavailable to the pilot. The pilot does not substitute a renderer.
6. `render_draft.py` supports only the FL-M008 manifest shape. Extending the workflow to
   another page type needs a renderer for that skill's manifest (or a skill that writes
   Markdown directly) before parity checks can apply.
7. Whether `ready-with-revisions` with only minor findings should be deliverable is a
   coordinator preference; the pilot allows it and reports the open minors.

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
- Live delegation: NOT VERIFIED. No Codex session was started from this task (it would spend
  the user's Codex session and needs the interactive host). Exact instruction: open Codex at
  `/Users/rocketclicks_1/SEO_Dept` on branch `content-workflow-pilot` after
  `sh pilot/content-workflow/scripts/activate.sh`, then send
  `$content-workflow pilot/content-workflow/runs/smoke-gomez-nunez-2026-09-23` and ask it to
  dispatch `legal_reviewer` for a stage-final round-0 review only; confirm in the thread that a
  custom agent named `legal_reviewer` ran and that it wrote no file. Until that succeeds, Codex
  is unverified for this workflow.
