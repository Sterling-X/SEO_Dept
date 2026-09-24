# Research-page fixtures (SYNTHETIC; served by tests/fixture_server.py only)

Every page here is invented for the content-workflow tests. The jurisdiction "Exampleland", the
statutes, the court rule, and the firm are fictional. The pages exist so the research layer can be
exercised end to end (fetch, excerpt binding, currency markers, live re-check, changed law,
unavailable source, future-effective legislation) without touching a real authority. Fixture runs
map the reserved `.example` URLs to the local server with `CW_FIXTURE_URL_REWRITE`; a real run never
rewrites and never fetches a reserved host. Nothing under this directory is legal research.

- `leg/statutes/12.345.html`, `leg/statutes/12.350.html`: the current fixture statutes.
- `leg/statutes/12.360.html`: an enacted section that is not yet effective (future-effective test).
- `leg-changed/statutes/12.350.html`: the same section after a fictional amendment removed the
  language the fixture quotes (changed-law test). `12.345.html` is unchanged in that tree.
- `courts/rules/family/7.html`: the fixture court rule.
- `client/…`: the fixture firm's first-party pages (client-fact evidence and link destinations).
- `leg-marker-changed/statutes/`: `12.345.html` keeps its operative text but carries a new currency
  line (marker-only drift test); `12.350.html` is unchanged.
