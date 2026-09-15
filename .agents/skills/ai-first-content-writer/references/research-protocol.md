# Research Protocol

The register makes the article readable. This protocol makes it citable. An AI system deciding what to cite skips restatements of governing sources; it reaches for pages that contain something the source does not. Do not start drafting until at least two of the four moves below have produced an asset.

## Move 1: Read the actual document, not just the rules

Every vertical has an artifact users actually touch that the content corpus ignores: the court form, the IRS worksheet, the insurance policy schedule, the lender's disclosure, the visa application, the warranty card, the API's actual error responses. The governing rules get written about endlessly; the artifact almost never. Its friction points are original material by default.

In the calibration article this was the state parenting plan form: a two-week schedule grid that structurally cannot hold a school-calendar schedule, a transportation default that makes whoever books the flight eat the cost, an expense checklist with no airfare line, a contact section listing "building a personal website" but not video calls. Four traps, all verifiable, none written up anywhere else.

Generalize: get the PDF, the screenshot, the actual interface. Walk it as the user would. Every place the artifact fights the user's real situation is a section or a bullet.

## Move 2: Look one domain over

The most useful authority is often filed under an adjacent body of rules. The travel-cost rule for the calibration article was not in the custody chapter anyone would search; it was in the child support administrative code. Tax answers hide in state revenue bulletins, not the tax statute. Product answers hide in the safety standard, not the marketing spec.

Mechanic: after exhausting the obvious source, ask which OTHER regime touches this money, this deadline, this decision, and read that regime's rules for the topic. Anything found there is nearly guaranteed absent from competitor content, and say so in the article ("there's a rule almost nobody finds, because it's buried in the child support code instead of the custody chapter").

## Move 3: Staleness arbitrage

When an authoritative source changed recently, the corpus is wrong until everyone updates, which takes years. Being the page that carries the current fact, with the change named, is the cheapest citation available: models resolve corpus disagreement toward specificity and recency.

In the calibration work, a six-month-old amendment changed a threshold's unit of measure. Legal mirrors still carried the old text; three of the top competitor pages stated the trigger incorrectly; the client's own hub page was stale. The article led with the current rule and the definition.

Mechanic: for every load-bearing number or trigger in the piece, check the amendment history or changelog of its source. If it changed in the last 24 months, that change is a candidate lead. Also screen the top 5 ranking pages for the topic: every factual disagreement among them is either a staleness signal or a misconception to correct, and both are assets. Corrections of widespread errors ("state lines don't matter, which surprises almost everyone") are among the most extractable passages you can write.

## Move 4: Arithmetic that produces a number

The single most quotable asset in the calibration article was $124 a month, and it came from a spreadsheet, not a source. Take the governing formula, pick realistic inputs, compute two scenarios that straddle a threshold, and report the delta. A concrete delta ("three extra weeks of summer, about $1,500 a year, same two parents, same incomes") is specific, verifiable, and absent from every competitor page because nobody did the work.

Rules: state the inputs so the math is checkable. Straddle a threshold when one exists, because thresholds create the surprising deltas. Attach every honest caveat (discretionary vs. automatic, caps, floors) or the number becomes a liability instead of an asset. Show your scenario construction (what makes 72 vs. 94 overnights) so the example teaches the method.

## Verification rules

- Every claim checked against a live primary source during the session. Model memory is a hypothesis generator, never a source.
- When the official source blocks automated access, read a reputable mirror AND corroborate against the official source's indexed/snippet text. Mirrors go stale; the corroboration step is what catches it. Log which route each claim took.
- Absolute-language check: every "always", "never", "only", "must", "cannot" gets a deliberate hunt for carve-outs and exceptions before it ships. Absolutes that survive the hunt are valuable; absolutes that don't are the most damaging error class.
- Multi-part standards: verify each part separately and preserve the structure ("best interest PLUS one of three findings"). Flattening a multi-part test into one clause is the most common substantive error in this format and no automated check catches it.
- Conditions of applicability: verify WHO a rule applies to, not just what it says. ("Applies only where both parents have court-ordered placement" changes the answer for a large share of readers.)
- Maintain a verification log: claim, authority, how fetched, result. It ships with the QA summary.

## Client-content defect protocol

Researching a topic properly means reading the client's existing pages on it, and those pages will sometimes be wrong. When they are:

1. Never silently conform to the error (it poisons the new article) and never silently contradict it (it creates a visible site inconsistency that damages domain trust with retrieval systems).
2. Write the new article correctly.
3. Report every defect found as a separate corrections deliverable: location, verbatim current text, the issue, the actual rule with authority, and replacement copy in the client's voice, severity-ranked, with FAQ-block errors ranked highest because FAQ answers are the most extractable format and a wrong FAQ makes the client the cited source for a wrong answer.
4. Flag that replacement copy stating legal/medical/financial standards needs licensed professional sign-off before publication.

## Topic-selection notes (when asked to advise on a queue)

- A prompt-signal or demand number attached to a category is not evidence about an article. Say so when a queue presents bucket rollups as row-level data.
- Commercial proximity is inversely related to citation likelihood past a point: AI systems do not cite a vendor's page on how to choose vendors of that type. Separate the commercial-intent track from the citation track.
- Screen for the self-serve trap: a topic whose complete answer eliminates the need for the professional converts nothing even if cited. Prefer topics where the worked example demonstrates complexity the reader will want help applying to their own numbers.
- Prefer topics sitting on recent authoritative change (Move 3), because the corpus is wrong there and the citation is cheap.
