# Fixture: valid-run (synthetic)

Everything here is synthetic test data for the readiness-check tests. The client
"Gómez & Núñez Family Law, P.A.", its domain, the jurisdiction "Exampleland", the statutes,
the URLs, and every review record are invented. Nothing in this directory is a real
deliverable, a real review, or legal information. The accented client name is deliberate: the
checks must accept it.

`tests/test_readiness.py` assembles a run directory from these files and from
`tests/fixture_manifest.py`: it pins the real candidate skills by hash (SKILL.md plus every
required resource), builds the checkpoint draft from generator manifest v0 with the candidate
skill's real `build-situational.js`, renders `draft.md` from the same manifest with
`scripts/render_draft.py`, records the checkpoint and initial final reviews against it, then
builds manifest v1 (the revision), re-renders, records the round-1 rechecks, and runs
mechanical QA with the candidate's structural and page validators declared in `run.json`.
