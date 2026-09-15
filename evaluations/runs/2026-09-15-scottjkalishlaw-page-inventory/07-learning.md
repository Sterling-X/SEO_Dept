# Provisional Pilot Learning Record

Status: **provisional—not adopted as a general principle**. The user determined that this pilot was not a representative benchmark for the capability the agent system is intended to develop.

## Trigger

The frozen initial answer applied categorical labels too broadly: it treated the `/news/` hub like an excluded news article and excluded landing pages by campaign type without completing page-level dispositions. The review also exposed the danger of carrying a dated-event observation forward after the reusable URL had changed.

## Provisional hypothesis

The pilot produced this proposed principle:

> For hubs, campaign landing pages, and reusable event pages, inspect the live destination individually before applying a page-type exclusion; verify its final URL, canonical and robots declarations, distinct role, internal discovery, duplication risk, and current freshness.

It was temporarily added to `context/seo-principles.md`, then removed from general context when the pilot's benchmark suitability was rejected. No imported skill, application code, validator, dependency, or source-transfer file was changed for this hypothesis.

## Checks performed within the pilot

| Required case | Page(s) checked | Expected protection | Observed result |
|---|---|---|---|
| Original case | `/news/`, the three family-law/custody LPs, and `/south-florida-divorce-family-law-qa-calls/` | Prevent category labels or stale observations from replacing live page evidence. | `/news/` and the LPs qualified after direct checks. The Q&A URL advertised September 17, 2026 on September 15 and was retained with a post-event recheck. |
| Different relevant case | `/articles/` and `/es/articles/` | Confirm the rule works on another archive/hub type. | Both were navigation-linked, self-canonical authority archives and were added; individual posts remain excluded. |
| Unaffected case | `/no-drama-divorce-guide-florida-edition/` | Ensure individual inspection does not force inclusion of every conversion asset. | It remained excluded: `200`, but `noindex,nofollow` with no canonical. The correction did not disturb the existing result. |

## Disposition and bounds

All supporting checks came from the same Scott Kalish site and the same unsuitable pilot. A separate read-only local reassessment found no representative evaluation outside this run supporting the composite hub/campaign/event rule, so it is retained here only as a provisional hypothesis.

Independently established guidance remains unchanged in `context/seo-principles.md`: assess intent and existing content, do not infer cannibalization from overlap alone, distinguish crawlability/indexability/canonicalization, and recheck changeable facts. Those principles preserve the supported constituent behavior without promoting this pilot-specific formulation.

Revisit the hypothesis only through a representative evaluation selected in advance under the capability, relevance, user-decision, inclusion-boundary, and completion-condition rule in `AGENTS.md`.
