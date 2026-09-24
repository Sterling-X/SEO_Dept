# family-law-situational-pages-pilot-v1: changes from baseline

Baseline: `.agents/skills/family-law-situational-pages` at the hashes recorded in
`pilot-manifest.json` (the 2026-09-16 local replacement, unchanged). Candidate created
2026-09-23. The baseline itself was not edited.

## Defects addressed

| # | Defect (from the assignment) | Evidence in the baseline | Change in this candidate |
|---|---|---|---|
| 1 | Conflicting citation-placement and duplicate-URL requirements | `SKILL.md` "In-body format" describes an identifier followed by a bracketed number while the template and generator emit a hyperlinked `[n]` run and the page validator requires the anchor to be exactly `[n]`; the red-team skill calls any repeated URL a hard fail while the situational skill requires the statute pairing. | One format stated in `SKILL.md`, the template, and `canonical/link-and-cta-limits.md`: hyperlinked `[n]` at the first material claim and again with the same number wherever that authority supports a later claim (repeated citations integrated 2026-09-23), first-appearance numbering, one Sources row per source as `[n] label \| URL`; citation repetition declared exempt from the single-placement rule; every other URL exactly once. |
| 2 | Inconsistent link and CTA limits | `SKILL.md` allows up to 2 sibling + 3 secondary links and never states a CTA count; the local `FL-M008` contract requires exactly one parent, one bridge, one CTA; `LOCAL-REPLACEMENT.md` and the template state the CTA count only for the local route. | Counts and placements restated from the single table `pilot/content-workflow/canonical/link-and-cta-limits.md` (table governs on conflict); CTA rule added: exactly one hyperlinked CTA in the final section, at most one non-linked CTA sentence earlier. |
| 3 | Ambiguous client-voice selection | Item 7 instructs a name-pattern scan (`[client-shortname]-voice`) and lists fifteen example names, none of which except `sterling-voice` exists here; a fallback "default to authoritative, empathetic, and direct" voice was allowed. | Voice resolved only by exact domain route from `canonical/client-routing.json` (mirror of `AGENTS.md`); unrouted domain requires a pinned approved voice brief; otherwise INCOMPLETE. Default-voice fallback removed. |
| 4 | Missing templates, scripts, or other required resources | The baseline's named dependencies were absent in the import and are labelled local replacements; nothing declared which files a run needs, and `build-situational.js` located the repository by a fixed `../../..` depth. | `pilot-manifest.json` lists required files including installed Node dependencies (`node_modules/docx`, `node_modules/adm-zip`); the readiness check reports `SKILL_RESOURCE_MISSING`. Generator and render wrapper locate the repository root by marker files (`AGENTS.md` plus the governing V2 HTML), with `SEO_DEPT_ROOT` override. |
| 5 | Reviews recommending fixes without verifying completion | Quality Gates are a writer self-check ("fix it before presenting"). | "Review hand-off (pilot)" section: writer never sets `fixed-verified`; reviewers decide on recheck; findings return by id; changes logged in `changes.md`. |
| 6 | Later edits invalidating earlier legal review | No rule. | Hash binding stated in `SKILL.md`; enforced by `scripts/readiness_check.py` (`REVIEW_STALE`). |
| 7 | Validators accepting citation mismatches or unresolved placeholders | `validate-page.js` checked only hyperlinked markers and the Sources URL/anchor, so a plain-text `[n]`, an unknown `[7]`, or a wrong Sources label passed; placeholder regex matched only `LOCAL DETAIL`, `INSERT`, `TODO`, `TBD` inside brackets, so `[FIRM_NAME]`, `{{county}}`, and bare `TBD` passed. `office/validate.py` had no placeholder or marker checks at all. | Both validators now reject plain-text markers, unknown or out-of-order markers, Sources rows whose id, label, or URL differ from the manifest, and the full placeholder grammar. `test-situational.py` grew from 21 to 34 cases; the 13 new cases include one production-shaped positive and twelve tampered-DOCX negatives. |

## Files changed relative to the baseline

- `SKILL.md`: frontmatter name and description; candidate banner and amendment summary; voice
  routing (Required Inputs item 7, Page Type Routing step 1, Voice and Tone); placeholder rule;
  citation format and source limit; CTA rule and limits-table pointer; Validation section;
  Quality Gates 7 and 13; new "Review hand-off (pilot)" section.
- `references/situational-template.md`: candidate note, citation-row wording, placeholder rule.
- `LOCAL-REPLACEMENT.md`: candidate banner; usage path.
- `scripts/build-situational.js`: repository-root discovery; placeholder grammar for consumer copy
  and publisher metadata.
- `scripts/validate-page.js`: placeholder grammar; plain-text marker detection; first-appearance
  order; Sources-row id/label/URL parity; paragraph-joined full text so word-boundary checks work.
- `scripts/office/validate.py`: placeholder grammar; marker set/order/count; Sources-row id and
  label parity.
- `scripts/render-situational.sh`: repository-root discovery for the delegated Core renderer.
- `scripts/test-situational.py`: production-shaped synthetic manifest and twelve tampered-DOCX
  negatives.
- New: `pilot-manifest.json`, `CHANGES.md`.

Unchanged: `agents/openai.yaml` (inert outside discovery), `assets/icon.svg`, `package.json`,
`package-lock.json`, the V2 link-authority contract, the content model, and DOCX geometry.

## Preserved client-specific rules

The `FL-M008` link-authority contract (one parent link to `FL-PA-DIV`, one bridge to `FL-M004`,
one CTA, exact V2 edges for anything else) is preserved as written. It is a family-law
architecture rule, not a generalization of one client's requirement. No Fanash, Sterling,
Blattner, or Service Credit Union rule was added to this candidate.

## Baseline behaviour demonstrated during candidate development

The six tampered-DOCX negatives were run against both validator sets on 2026-09-23
(`pilot/content-workflow/docs/CHANGES-AND-OPEN-QUESTIONS.md` records the table). The baseline
page validator (`validate-page.js`) accepted all six. The baseline structural validator
(`office/validate.py`) accepted the wrong Sources label outright and rejected the other five only
as a side effect of its DOCX-versus-manifest word-count parity check, which would not fire when
the manifest itself carries the same defect; it had no placeholder or citation-marker check. The
candidate validators reject all six for the stated reason.

## Refinements integrated 2026-09-23 (comparison with SEO_Dept_Refined_Content_Skills_v1.patch)

- Repeated citations share one source identity (patch F08/E04): the generator, both validators,
  and the readiness check now accept the same `[n]` wherever that authority supports a later
  material claim; numbering still follows first appearance and each source has one Sources row.
  Validator hyperlink arithmetic counts markers, not sources.
- Source ceiling reassessed: six is a readability guideline; seven or more require
  `quality_contract.source_ceiling_rationale` (40+ characters) naming the claim coverage; twelve is
  a sanity limit. The V2 architecture states no source count, so no architecture requirement is
  affected; the FL-M008 link-authority contract is unchanged. Against the compatibility rule that
  a validation requirement is never removed (`docs/seo-skill-compatibility.md`): the baseline's
  hard six-source cap is replaced, not dropped, by three checks together: the recorded rationale,
  the readiness gate's `LEGAL_PREDRAFT_COVERAGE` (every citation needs a Confirmed pre-draft
  verification row), and the twelve-source sanity limit.
- Render dependency repaired without bypassing integrity checks: `scripts/render-situational.sh`
  is now self-contained, reads the pinned release and SHA-256 from this candidate's
  `renderer-tools.lock.json` (Codex documents renderer 26.905.11957, revalidated by reading the
  installed script and rendering an existing six-page FL-M008 DOCX), reuses the Core skill's
  Git-ignored LibreOffice and PyMuPDF installs by path, and keeps the empty-output-directory,
  exact-path, and hash checks. The baseline Core wrapper is untouched and still fails closed.
- Pre-draft legal verification and required checkpoints are workflow rules (canonical) that this
  skill's hand-off section now states.
- Candidate regression suite: 38 cases (four new: repeated citation positive, seven sources with
  rationale positive, seven without rationale negative, thirteen sources negative).

## Remaining uncertainties

- Rendered output is produced by LibreOffice 26.8.0 with Liberation Sans substituting for Arial;
  Microsoft Word fidelity is unverified. The production Core wrapper remains pinned to an
  uninstalled renderer release and is a separate production repair.
- Readiness for Situational nodes other than `FL-M008` is not claimed.
- The bracket-token placeholder rule will flag legitimate bracketed prose such as "[sic]".
  None appears in the situational contract; a hit is reported for inspection, never accepted
  silently.
- Repeated citation is resolved (2026-09-23): one identity and number per authority, cited at
  the first material claim and again wherever the same authority supports a later claim; the
  generator and both validators accept repeats and require each source to be cited at least
  once (see "Repeated citations" above).
- 2026-09-23 (Sterling run, editorial checkpoint uncertainty 4): the template's page contract
  named "Florida divorce", "equitable distribution", and "alimony" from the first Florida run;
  reworded jurisdiction-neutral so a Wisconsin run reads the same contract.
