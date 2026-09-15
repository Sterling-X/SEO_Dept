# SEO Strategist and Reviewer Evaluations

These are evaluation designs, not completed tests. No scores or client-specific expected facts have been established.

## Comparison method

Compare two conditions using the same original request, evidence bundle, client context, constraints, and frozen evaluation criteria:

1. **Strategist only:** the strategist produces and finalizes the work without independent review.
2. **Strategist plus reviewer:** the strategist produces an initial answer, `seo_reviewer` reviews it, and the strategist resolves documented findings before finalizing.

Preserve both outputs and the review findings. Do not let either condition see evidence unavailable to the other. Record material differences and user corrections rather than assuming the reviewed condition is better.

Record the Codex version, repository revision, model and reasoning settings when available, run order, elapsed time, and evidence-bundle identifier for each condition so later comparisons can distinguish workflow effects from environment changes.

## Measures

| Measure | What to record |
| --- | --- |
| Factual accuracy | Verified correct and incorrect material claims, with supporting evidence. |
| Completeness | Required request elements and important decision factors covered or omitted. |
| Unsupported claims | Material assertions, causal conclusions, calculations, or citations lacking adequate support. |
| Request compliance | Missed constraints, unauthorized actions, formatting failures, and requested outputs not delivered. |
| User correction effort | Number and substance of corrections, clarifications, or rewrites the user must provide. |
| Time and usage | Elapsed time, model/tool usage, and reviewer overhead when those measurements are available. |

If a measure is unavailable, record it as unavailable. Do not estimate or invent it.

## Initial scenarios

### 1. Commercial page classification and geography

**Task design:** Identify commercial pages from a supplied site inventory and supporting business evidence.

**Required distinctions:** Practice-area hubs, procedural pages, situational pages, verified physical-office pages, location-specific practice pages, and service-area pages. A city mention or service-area page must not be treated as proof of an office.

**Evidence needed for a real run:** Page inventory, page content or metadata, verified office sources, business priorities, and relevant performance data.

### 2. Potential content cannibalization

**Task design:** Assess a suspected overlap between supplied pages without assuming shared keywords prove cannibalization.

**Required distinctions:** Search intent, page purpose, query-level ranking behavior, landing-page performance, internal targeting, canonical/indexing state, and plausible alternatives such as healthy multi-page coverage.

**Evidence needed for a real run:** Page content, target queries, GSC query-page data, rank history when available, index/canonical evidence, and internal-link context.

### 3. Lead decline diagnosis

**Task design:** Diagnose a reported lead decline using a supplied cross-channel evidence bundle.

**Required distinctions:** Search visibility, organic traffic, landing-page conversion, calls/forms, qualification, consult or sales handling, and CRM outcomes. Correlation must not be presented as causation without adequate evidence.

**Evidence needed for a real run:** Comparable date ranges and definitions from GSC, GA4, map visibility, call/form tracking, and CRM or intake systems, including known tracking changes.
