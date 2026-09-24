# Link and CTA limits for situational pages (pilot v1, canonical)

One table, referenced by the candidate situational-page skill, the candidate editorial
(red-team) skill, and the editorial reviewer role. The baseline skills disagreed
(see `docs/CHANGES-AND-OPEN-QUESTIONS.md`, defect 2).

| Element | Count | Placement rule |
|---|---:|---|
| Parent practice-area hub link | exactly 1 | Strongest contextual placement; lead-in sentence about the hub's topic |
| Process bridge to the closest procedural page | exactly 1 when that page exists and is verified; 0 otherwise, reported as a gap | Where the page distinguishes the circumstance from the procedure |
| Sibling situational cross-links | 0 to 2 | Inline, only where comparison is genuinely useful |
| Secondary contextual links | 0 to 3 | Inline, Next Steps, or a short Related Issues list near the end |
| Consultation CTA link | exactly 1 | Inside the final CTA section, before Sources |
| Non-linked CTA sentence earlier in the page | 0 to 1 | Plain text, no guarantee, pricing, urgency, or "free" claim unless the client facts support it |
| Statutory sources | claim coverage governs; 6 is a readability guideline, 12 a sanity limit | One identity and number per authority; cited at first material claim and again wherever the same authority supports a later material claim; listed once in Sources; more than 6 needs a recorded coverage rationale |

Draft form: in `draft.md` every marker is written `[[n]](url)` so the reviewed text carries the
same hyperlink the export carries; a plain `[n]` in the draft fails `citations-draft`. In the
export the marker is a hyperlink whose anchor is exactly `[n]`.

Provenance of the counts: the parent-hub, process-bridge, and CTA counts come from the imported
situational skill's structural-link rules and the bounded `FL-M008` local replacement
(`LOCAL-REPLACEMENT.md`, which labels the bridge as skill-required navigation, not a V2 edge).
They are pilot decisions for situational pages, not a client's rule. The V2 architecture still
governs which additional architecture links may exist; this table never adds a V2 edge.

Single-placement rule: every internal destination URL appears exactly once on the page.
Statutory sources are different: one hyperlinked `[n]` marker at the first material claim, the
same marker again wherever that authority supports a later material claim, and one hyperlinked
URL in Sources. That repetition is the citation convention, not a duplicate. Any other URL that
appears twice is a blocking finding.

Where a governing client architecture applies (family-law V2), additional architecture
links require an exact recorded relationship; the architecture source governs the target
set, and this table governs counts and placement. For the bounded `FL-M008` local route,
the parent hub, the process bridge, and the CTA are the three required links.

Banned patterns: tag-on links ("See our X page", "Learn more at", "Click here"), two or
more links in one sentence outside a Related Issues or Next Steps module, resource-dump
paragraphs, bare-URL or generic anchors, the same destination under two anchors.
