# Content-production workflow pilot (v1)

Branch: `content-workflow-pilot`. Status: pilot, not the production default. Created
2026-09-23 inside the existing SEO_Dept workspace; the SEO Strategist (`AGENTS.md`), the
`seo-reviewer`, the 14 production skills, the learning system, and the MemPalace setup are
unchanged.

The pilot adds a coordinator entry point (`/content-workflow` in Claude Code,
`$content-workflow` in Codex), three specialist agents (content writer, legal reviewer,
editorial reviewer), uniquely named candidate versions of the situational-page skill and its
legal, editorial, and mechanical-QA dependencies, and a deterministic readiness check that
binds review evidence to content hashes and refuses `READY` when evidence is missing, stale,
or blocked.

## Layout

```
pilot/content-workflow/
  README.md                     this file: layout, activation, rollback, usage, limits
  canonical/                    the single copy of role text, rules, criteria, routing, schemas
    roles/{content-writer,legal-reviewer,editorial-reviewer}.md
    workflow-rules.md  review-criteria.md  review-findings-schema.md  link-and-cta-limits.md
    client-routing.json           mirror of the AGENTS.md domain->voice table (tested for equality)
    schemas/run.schema.json  schemas/review-record.schema.json
  adapters/                     GENERATED from canonical/ by scripts/build_adapters.py
    claude/agents/*.md            Claude Code subagents (frontmatter: name, description, tools, disallowedTools)
    codex/agents/*.toml           Codex custom agents (name, description, sandbox_mode, developer_instructions)
  skill/content-workflow/       the entry-point skill, shared by both hosts (SKILL.md + agents/openai.yaml)
  candidates/skills/            candidate skill versions, OUTSIDE every discovery path; pinned by hash per run
    family-law-situational-pages-pilot-v1/   legal-content-accuracy-qa-pilot-v1/
    family-law-red-team-qa-reviewer-pilot-v1/ qa-output-checker-pilot-v1/
    (each: pilot-manifest.json with baseline hashes and required_files; CHANGES.md)
  scripts/
    readiness_check.py  deliver.py  record_review.py  mechanical_qa.py  pin.py  render_draft.py  render_inspect.py  dispose_finding.py
    build_adapters.py  activate.sh  rollback.sh  cw_common.py
  tests/
    test_readiness.py  fixture_manifest.py (synthetic generator manifests)  fixtures/valid-run/ (synthetic)
  docs/CHANGES-AND-OPEN-QUESTIONS.md   defects addressed, evidence, open questions
  runs/        (Git-ignored) one directory per run: client sources, draft, export, reviews, reports
  deliveries/  (Git-ignored) READY exports and their readiness reports
```

## Design in one paragraph

One canonical copy of each role's instructions, the workflow rules, the review criteria, the
findings schema, and the client-voice routing lives under `canonical/`. `build_adapters.py`
wraps the role text in each host's agent format; a test fails if the adapters drift. The
coordinator remains the primary SEO Strategist conversation. Reviewers are read-only and
cannot delegate: on Claude the tool allowlist omits `Agent`, `Write`, `Edit`, and `Bash`; on
Codex `sandbox_mode = "read-only"` plus instruction, because the Codex custom-agent format
exposes no tool or depth restriction. Every review is recorded with the hashes of the draft,
export, and pinned sources present when the recorder ran (the coordinator records immediately
after the reviewer returns; a reviewer may echo the draft hash it was given); a later edit
makes the record stale. Delivery is
refused unless every mechanical check passes and every blocking finding is `fixed-verified`
against the current draft hash or withdrawn, within at most two repair rounds. For family-law
pages the required records are: pre-draft legal verification, legal and editorial checkpoints,
legal and editorial final reviews, mechanical QA, and a rendered-page inspection bound to the
exact export hash. Findings carry a category; legal-accuracy, citation, client-fact, and
promise findings close only when the raising reviewer re-reads the corrected text.

## What the tooling proves, and what it does not

`readiness_check.py`, `mechanical_qa.py`, and `deliver.py` prove mechanical facts: pins and
hashes match, required resources exist, the voice route resolves, citations pair with Sources
in both draft and export, no placeholder remains, headings, normalized consumer-copy
paragraph sequences, and word counts agree between draft and export, review records are well
formed and current, and rounds stay within the cap.
A recorded legal or editorial `PASS` is a judgment bound to a hash. The tooling records it and
cannot verify that it was correct, and every report says so. Attorney review before
publication remains required for legal content.

## Activation (what it changes)

`scripts/activate.sh` adds eight entries and edits no existing file: five symlinks and, for the
Codex agents, three byte copies of the generated adapters (Codex does not follow symlinked agent
files; verified 2026-09-23 with `codex exec`). `build_adapters.py` remains the only place the
agent text is authored; rollback removes a copy only while it is identical to its adapter:

| Symlink created | Target |
|---|---|
| `.claude/agents/content-writer.md` | `pilot/content-workflow/adapters/claude/agents/content-writer.md` |
| `.claude/agents/legal-reviewer.md` | `pilot/content-workflow/adapters/claude/agents/legal-reviewer.md` |
| `.claude/agents/editorial-reviewer.md` | `pilot/content-workflow/adapters/claude/agents/editorial-reviewer.md` |
| `.codex/agents/content_writer.toml` (byte copy) | `pilot/content-workflow/adapters/codex/agents/content_writer.toml` |
| `.codex/agents/legal_reviewer.toml` (byte copy) | `pilot/content-workflow/adapters/codex/agents/legal_reviewer.toml` |
| `.codex/agents/editorial_reviewer.toml` (byte copy) | `pilot/content-workflow/adapters/codex/agents/editorial_reviewer.toml` |
| `.claude/skills/content-workflow` | `pilot/content-workflow/skill/content-workflow` |
| `.agents/skills/content-workflow` | `pilot/content-workflow/skill/content-workflow` |

The candidate skills are never linked into a discovery path. A run pins them by repository
path and SHA-256 in its `run.json`.

The eight activation entries are deliberately **not committed**; they are listed in `.gitignore`
so that checking out the pilot branch does not activate the pilot. Activation is a local, explicit
step on each checkout.

Activation steps:

```bash
cd /Users/rocketclicks_1/SEO_Dept
git checkout content-workflow-pilot
npm ci --prefix pilot/content-workflow/candidates/skills/family-law-situational-pages-pilot-v1   # candidate node_modules are Git-ignored and are required resources
sh pilot/content-workflow/scripts/activate.sh
# Claude Code: start a new session at the repository root (the Agent tool's type list is fixed per session).
# Codex: start a new session at the repository root.
```

The only pre-existing tracked file the pilot edits is `.gitignore` (adds `runs/`, `deliveries/`,
candidate `node_modules/`, and `__pycache__` ignores). The pilot also adds new files under
`pilot/content-workflow/`.

## Rollback

```bash
cd /Users/rocketclicks_1/SEO_Dept
sh pilot/content-workflow/scripts/rollback.sh      # removes exactly the eight activation entries above; touches nothing else
git checkout seo-agent-foundation                   # leaves the pilot branch in place
```

A scoped backup with SHA-256 manifest and step-by-step restore instructions is outside the
repository and outside every discovery path at
`~/SEO_Dept_backups/content-workflow-pilot-2026-09-23/RESTORE.md`. It holds the pre-pilot
`.gitignore`, the pre-existing agent files, the `.claude/skills` symlink map, and byte copies
of the four baseline skills the pilot candidate-copied.

## Using the workflow

### Claude Code

1. Activate (above) and start a new session at the repository root.
2. Type `/content-workflow <run-dir>` (or `/content-workflow` and let the skill create the run
   directory). The skill is explicit-invocation only; the model does not auto-select it.
3. The skill walks the coordinator through: intake gate (`readiness_check.py --stage intake`),
   pre-draft legal verification (`legal-reviewer`, `stage: predraft`, recorded with
   `record_review.py`), writer dispatch (`Agent`, `subagent_type: content-writer`), required
   checkpoint reviews (`legal-reviewer`, `editorial-reviewer`), final reviews of the complete
   revised draft, `mechanical_qa.py`, `render_inspect.py --render` then viewing every page and
   `--attest`, at most two repair rounds (coordinator dispositions only via `dispose_finding.py`),
   `deliver.py`, then the unchanged `seo-reviewer` pass and single learning pass required by
   `AGENTS.md`.

### Codex (delegation verified headless for all three agents; interactive session not yet tested)

1. Activate (above) and start a new session at the repository root.
2. Type `$content-workflow <run-dir>`. `agents/openai.yaml` sets
   `allow_implicit_invocation: false`, so Codex will not select it implicitly.
3. Same procedure; the custom agents are `content_writer`, `legal_reviewer`, and
   `editorial_reviewer` (spawned per the Codex multi-agent documentation; `multi_agent` is a
   stable, enabled feature in the installed `codex-cli 0.155.0-alpha.16.3`).

### Commands the coordinator runs (both hosts)

```bash
python3 pilot/content-workflow/scripts/pin.py <run-dir> --skills <SKILL.md path>... --sources <run-relative path>...
python3 pilot/content-workflow/scripts/readiness_check.py <run-dir> --stage intake
python3 pilot/content-workflow/scripts/record_review.py <run-dir> --input <findings.json> --runtime claude|codex --agent <agent> --stage checkpoint|final --round N
python3 pilot/content-workflow/scripts/mechanical_qa.py <run-dir> --round N
python3 pilot/content-workflow/scripts/render_inspect.py <run-dir> --round N --render      # then view every render/rN/page-*.png
python3 pilot/content-workflow/scripts/render_inspect.py <run-dir> --round N --attest <attestation.json>
python3 pilot/content-workflow/scripts/dispose_finding.py <run-dir> --role <role> --id <id> --accept --rationale "..."
python3 pilot/content-workflow/scripts/deliver.py <run-dir>
```

## Tests

```bash
python3 pilot/content-workflow/tests/test_readiness.py
python3 pilot/content-workflow/candidates/skills/family-law-situational-pages-pilot-v1/scripts/test-situational.py
python3 pilot/content-workflow/scripts/build_adapters.py --check
```

Results and the live-delegation smoke tests are recorded in the "Verification status" section
below and in `docs/CHANGES-AND-OPEN-QUESTIONS.md`.

## Verification status (2026-09-23)

| Item | Claude Code 2.1.277 | Codex CLI 0.155.0-alpha.16.3 |
|---|---|---|
| Agent definitions parse | yes (frontmatter read; tools allowlists as designed) | yes (`tomllib`; required fields present; `sandbox_mode` set) |
| Agent discovery after activation | verified: fresh headless session listed `content-writer`, `editorial-reviewer`, `legal-reviewer` | verified headless (`codex exec`): a symlinked `.codex/agents/legal_reviewer.toml` was "agent type is currently not available"; the regular-file copy was spawned. Activation now copies Codex agents |
| Skill discovery after activation | verified: `/content-workflow` loaded in a fresh headless session | verified offline: symlinked skill dir is followed; hidden from the model list only because `allow_implicit_invocation: false` (explicit `$content-workflow` only) |
| Live delegation | verified for all three agents in fresh headless sessions (`subagent_stats.by_type`); reviewers wrote nothing; writer wrote only `changes.md` | verified headless for all three agents (`codex exec`, 2026-09-23): `legal_reviewer` and `editorial_reviewer` under `--sandbox read-only` read the smoke draft, answered, and wrote nothing; `content_writer` under `--sandbox workspace-write` created only the one requested file. A transient `collab spawn failed` router error preceded one successful spawn. Interactive-session behaviour not tested |
| Recorder, mechanical QA, delivery on real agent output | verified on the smoke run: reviews recorded, mechanical pass, delivery refused with nine reasons | same scripts (host-independent) |
| Generator-built export through validators and gate | verified in the test suite: every fixture run builds its DOCX with the candidate generator and executes both candidate validators | same (Node and Python only) |
| End-to-end client run | verified 2026-09-23 on Sterling FL-M008 (Wisconsin): pre-draft legal verification, draft, checkpoints, two repair rounds, finals and rechecks, mechanical QA, three render inspections, READY, delivered to the ignored delivery directory; not published. Record: `docs/CHANGES-AND-OPEN-QUESTIONS.md` | not exercised (Codex agents verified by headless smoke tests only) |
| Unit tests | 55/55 `tests/test_readiness.py` (generator-backed, renders every READY fixture through the pinned renderer); 38/38 candidate suite; adapters in sync | same (Python, Node, and the pinned renderer tooling) |

Codex live delegation is verified for all three pilot agents in headless mode; the interactive
session remains to be exercised. Details and raw evidence locations:
`docs/CHANGES-AND-OPEN-QUESTIONS.md`.

## Limitations and dependencies

- Codex enforces reviewer read-only behaviour through `sandbox_mode` only; the no-delegation
  rule is instruction-only on Codex. Codex live delegation is verified headless only; the
  interactive session is untested.
- The pinned generator's word count governs the skill's word target; the mechanical parity
  count uses a different tokenizer (Unicode versus ASCII word classes) and can differ by a few
  words. It compares draft and export with each other and is informational for the ceiling.
- A run's brief basis must be disclosed in the run: the Sterling run used the V2 node brief, the
  voice skill, and first-party facts checked live, not a signed client brief.
- The legal reviewer's live fetch depends on `WebFetch`/`WebSearch` permission. In a headless
  session those tools are denied and the reviewer must classify every claim `Unverifiable`
  (observed in the smoke run). In an interactive session Claude Code prompts per domain;
  `.claude/settings.json` grants no standing web permission and the pilot does not change it.
- `CLAUDE.md` ("the 14 skills in `.agents/skills/`") and the agent enumeration in
  `docs/seo-agent-setup.md` describe production; after activation both are one short of the
  local truth (the pilot adds one skill symlink and three agents). Those files are not edited
  by the pilot.
- The content writer holds `Bash`, `Write`, and `Edit` (Claude) or `workspace-write` (Codex);
  its rule never to touch `run.json`, `reviews/`, or pinned sources is instruction-only. The
  readiness check re-applies the recorder's integrity rules and hash pins at delivery, which
  is what catches an edited record or a re-pinned source.
- Rendering uses the situational candidate's own pinned wrapper (Codex documents renderer
  26.905.11957, hash-pinned in the candidate's `renderer-tools.lock.json`, revalidated
  2026-09-23) with the Core skill's Git-ignored LibreOffice and PyMuPDF installs. The production
  Core wrapper is untouched and still fails closed; that is a separate production repair.
  Rendered pages come from LibreOffice, so Microsoft Word fidelity is unverified.
- Readiness for Situational nodes other than `FL-M008` is not claimed; the candidate inherits
  the baseline's bounded local replacement.
- Live web verification of legal claims is the legal reviewer's judgment; the tooling records
  access dates and results but cannot confirm them.
- The pilot does not promote lessons into `AGENTS.md`, production skills, or MemPalace shared
  rooms; see `docs/CHANGES-AND-OPEN-QUESTIONS.md`.
