# High-Conflict Divorce Situational template

> **LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL**
>
> This is a bounded FL-M008 template derived from the imported Situational skill and the governing Family Law V2 record. It is not the Core Practice-Area Hub template and must not be generalized to another node without a separate demonstrated adaptation.
>
> **PILOT CANDIDATE v1** of the template; baseline hash in `../pilot-manifest.json`. Changes: citation-row wording and the placeholder rule below.

## Page contract

The page owns the reader's high-conflict circumstance: repeated escalation, difficult communication, control or non-cooperation, parenting friction, safety concerns, financial opacity, and the practical need for structure. It does not own:

- a broad explanation of divorce in the page's jurisdiction (the parent Core hub owns that);
- the procedural lifecycle of a Contested Divorce case;
- a complete treatment of parenting plans or placement schedules, property division, alimony or maintenance, mediation, discovery, enforcement, or protective orders; or
- a diagnostic label for either spouse.

Use selective legal and procedural explanation only when it helps the reader understand what makes the high-conflict circumstance consequential or what decision to make next.

## Required publisher block

The generator creates a clearly separated proposed-draft block before the consumer copy. The manifest supplies:

- retained client implementation URL;
- proposed canonical URL and explicit URL-retention decision;
- proposed title tag;
- proposed meta description;
- CMS page title;
- Open Graph/Twitter title and description;
- proposed H1, robots direction, and media note;
- V2 node, role, and reference path; and
- proposed-draft status.

The V2 path is an architecture reference. It is not a command to replace a client's retained implementation URL.

## Required consumer-copy sequence

1. **H1:** Scenario-specific High-Conflict Divorce heading.
2. **Opening paragraph 1:** Answer the decision behind the search. State what a high-conflict pattern changes and what the reader should prioritize.
3. **Opening paragraph 2:** Clarify the stakes without defining all divorce law or predicting trial.
4. **Scenario section (`role: scenario`):** Describe observable patterns and decisions, not personality diagnoses.
5. **Stakes section (`role: stakes`):** Explain the limited parenting, safety, financial, or evidence consequences relevant to this circumstance.
6. **Strategy section (`role: strategy`):** Give practical, non-prescriptive steps that help create structure and preserve reliable information.
7. **Firm-help section (`role: firm-help`):** Explain only verified services and supported ways counsel can help.
8. **Optional FAQ section (`role: faq`):** Include only scenario-specific questions that do not recreate general Divorce or Contested Divorce copy.
9. **CTA section (`role: cta`):** Direct, supported contact language without guarantees, unsupported urgency, pricing, or consultation claims. The final consultation invitation carries the single `consultation-cta` link.
10. **Sources:** Generated from the manifest and always last.

At least five H2 sections are required. The `scenario`, `strategy`, `firm-help`, and `cta` roles are mandatory; `stakes` is strongly expected when the content supports it.

## Manifest content blocks

Supported blocks:

```json
{"type":"p","runs":[{"type":"text","text":"..."}]}
{"type":"h2","role":"scenario","text":"..."}
{"type":"h3","role":"faq-question","text":"..."}
{"type":"ul","items":[{"runs":[{"type":"strong","text":"Lead-in: "},{"type":"text","text":"..."}]}]}
{"type":"ol","items":[{"runs":[{"type":"text","text":"..."}]}]}
```

Supported run types:

```json
{"type":"text","text":"..."}
{"type":"strong","text":"..."}
{"type":"internal_link","link_id":"link-1","text":"descriptive anchor"}
{"type":"citation","source_id":1,"text":"[1]"}
```

The first two content blocks must be paragraphs. A body citation appears at the first material claim supported by that source, numbered by first appearance, and may reappear with the same number wherever that source supports a later material claim; the generator creates the matching Sources row `[n] label | URL` with the manifest label verbatim, and the validators check marker set, order, count, Sources-row id, label, and URL. The body-marker plus Sources-row pairing is the required footnote convention, not a duplicate URL.

## Link authority rule for this local route

V2 remains authoritative for `FL-M008` classification, hierarchy, and its explicitly recorded relationships. A missing V2 edge does not cancel the Situational skill's separate parent-navigation and process-bridge requirements. Schema version 2 therefore requires every manifested link to state its actual `supporting_authority`:

- `skill-parent-navigation`: exactly one contextual link to the actual V2 parent, `FL-PA-DIV`. It must match the parent's V2 node, path, publishability, and gate, but it must omit `v2_edge_id`. The link direction comes from the skill and is not claimed as an outgoing V2 edge.
- `skill-process-bridge`: exactly one contextual bridge to `FL-M004` Contested Divorce under the same parent. It must match V2 page type `Practice-Area Procedural Page`, role `Core Procedure`, path, publishability, and gate, but it must omit `v2_edge_id`. Its direction also comes from the skill.
- `consultation-cta`: exactly one verified, same-domain, direct-200 contact link in the final CTA section. It must set `destination_kind` to `consultation-contact` and omit `target_node_id`, `v2_reference_path`, and `v2_edge_id` because the contact route is not a V2 node.
- `v2-explicit-relationship`: optional additional links must name an exact outgoing edge from `FL-M008` in `v2_edge_id` and pass the existing V2 target checks. `FL-M013` remains rejected while its target gate is Hold.

All four authority types retain the common dated destination evidence, right-service fit, single-placement, descriptive-anchor, and same-domain requirements. The three structural authorities above are required for this bounded `FL-M008` workflow, so an empty `link_manifest` is invalid. The requirements do not establish workflow readiness for any other Situational node.

## Mechanical limits

- 1,100–1,700 consumer-copy words, excluding the publisher block and Sources.
- No more than three sentences in a body paragraph.
- Proper Word headings and list numbering; no Unicode bullet characters.
- Arial 12 pt body, H1 18 pt, H2 15 pt, H3 13 pt; US Letter; one-inch margins.
- No em dashes, tag-on link language, or duplicate internal destination URLs.
- No placeholder of any form at delivery. Research comes first: a detail the writer lacks is retrieved during the run (`research_fetch.py`) and verified, not placeholdered. `[LOCAL DETAIL: ...]` is the only valid interim form, is permitted only for a fact the coordinator confirmed cannot be researched in this run, is reported in `changes.md`, and is never delivered; bracketed non-numeric tokens of any other form fail validation.
- Claim coverage governs the source count: six is a guideline, more than six needs a recorded rationale, twelve is a sanity limit; every material legal claim still requires assignment-specific live primary-authority verification before drafting and again in review.
