# FL-M008 local replacement record

> **LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL**

The imported Situational-page skill did not include the template, generator, structural validator, page validator, or renderer wrapper named by its instructions. The files listed below are a bounded local replacement for the demonstrated `FL-M008` High-Conflict Divorce assignment. They do not establish workflow readiness for another Situational node.

## Scope

- Architecture node: `FL-M008` High-Conflict Divorce
- V2 page type and role: Practice-Area Situational Page / Situational
- V2 reference path: `/divorce/high-conflict-divorce/`
- V2 brief and target: Situation / Use-Case Brief; 1,100–1,700 words
- Implementation URL: client-specific manifest evidence, kept separate from the V2 reference path
- Other Situational nodes: pending a separate demonstrated adaptation

## Replacement components and provenance

| Component | Status | Basis and reuse boundary |
|---|---|---|
| `references/situational-template.md` | Local replacement | New Situational-specific content contract based on the imported skill and V2 `FL-M008` record. It is not the Core Hub template. |
| `scripts/build-situational.js` | Local replacement | New manifest-driven generator. It reuses the pinned `docx` dependency and generic OOXML/DOCX mechanics already proven by the local Core route; it does not import Core content, headings, template logic, or link rules. |
| `scripts/office/validate.py` | Local replacement | New structural validator. Its ZIP/XML integrity checks reuse general OOXML validation concepts demonstrated by the local Core validator; its Situational contract is independently encoded here. |
| `scripts/validate-page.js` | Local replacement | New FL-M008 page-level validator. It reuses `adm-zip` as a generic DOCX inspection dependency, but it has a separate Situational and V2 link contract. |
| `scripts/render-situational.sh` | Local wrapper | Delegates only document rendering to the already pinned local Core renderer wrapper. No Core content-generation component is invoked. |
| `scripts/test-situational.py` | Local replacement | New positive and negative tests for this scoped route. |
| `package.json` / `package-lock.json` | Local tooling metadata | Pins the same proven generic `docx@9.7.1` and `adm-zip@0.6.1` versions in this skill's own dependency boundary. |

The governing data is read at runtime from `context/architecture/Family_Law_StructureV2.html`. V2 controls classification, hierarchy, and every relationship presented as an explicit V2 edge. Schema version 2 also represents three separate local requirements: parent-Hub navigation, the bounded `FL-M004` process bridge, and a consultation CTA. The first two are skill-required navigation, not outgoing V2 edges; the CTA is not a V2 node. Their manifest records must use those authorities and omit invented edge identifiers. Additional V2 relationship links still require exact outgoing edges.

This schema version supersedes the earlier local exclusive-edge restriction and empty-manifest allowance. It changes only the demonstrated `FL-M008` route and does not alter V2.

## Readiness limit

Passing the included tests means only that the local mechanics detect the tested FL-M008 conditions. It does not verify legal accuracy, client claims, source availability, destination quality, editorial judgment, or rendered visual quality. Those gates remain assignment-specific.

## Usage

Install the isolated pinned dependencies once, then build, validate, and render:

```sh
cd .agents/skills/family-law-situational-pages
npm ci
node scripts/build-situational.js /absolute/path/workflow-input.json /absolute/path/florida-high-conflict-divorce-situational.docx
python3 scripts/office/validate.py /absolute/path/florida-high-conflict-divorce-situational.docx --manifest /absolute/path/workflow-input.json
node scripts/validate-page.js /absolute/path/florida-high-conflict-divorce-situational.docx --manifest /absolute/path/workflow-input.json
scripts/render-situational.sh /absolute/path/florida-high-conflict-divorce-situational.docx --output_dir /absolute/path/empty-render-directory
python3 scripts/test-situational.py
```

## Manifest shape

The generator validates actual values against V2 and does not treat this abbreviated shape as evidence:

```json
{
  "schema_version": 2,
  "workflow": "situational-fl-m008-local-replacement",
  "meta": {
    "architecture_node_id": "FL-M008",
    "v2_reference_path": "/divorce/high-conflict-divorce/",
    "v2_page_type": "Practice-Area Situational Page",
    "v2_role": "Situational",
    "v2_brief_type": "Situation / Use-Case Brief",
    "v2_word_count_target": "1,100–1,700",
    "client_url": "https://client.example/retained-route/",
    "canonical_url": "https://client.example/retained-route/",
    "url_retention_decision": "retain-existing",
    "client_url_status": 200,
    "client_url_redirects": 0,
    "client_url_verified_on": "YYYY-MM-DD",
    "client_url_evidence": "Evidence note",
    "firm_name": "Verified firm name",
    "jurisdiction": "Verified jurisdiction",
    "voice_source": "Path or first-party brief identifier",
    "title_tag": "Proposed title tag",
    "meta_description": "Proposed meta description",
    "cms_title": "Proposed CMS title",
    "social_title": "Proposed social title",
    "social_description": "Proposed social description",
    "h1": "Proposed H1",
    "robots": "index, follow",
    "media_note": "Proposed asset action and alt-text requirement",
    "situational_purpose": "Distinct scenario-specific ownership statement",
    "excluded_intents": ["general-divorce-hub", "contested-divorce-procedure"]
  },
  "link_inventory": {
    "status": "reviewed",
    "reviewed_on": "YYYY-MM-DD",
    "evidence": "Required skill-navigation and consultation destinations screened; additional exact outgoing V2 targets screened separately."
  },
  "link_manifest": [
    {
      "id": "parent-hub",
      "supporting_authority": "skill-parent-navigation",
      "source_node_id": "FL-M008",
      "target_node_id": "FL-PA-DIV",
      "v2_reference_path": "/divorce/",
      "client_url": "https://client.example/verified-divorce-route/",
      "client_url_status": 200,
      "client_url_redirects": 0,
      "client_url_verified_on": "YYYY-MM-DD",
      "client_url_evidence": "Direct response and destination-fit evidence",
      "destination_fit": "verified",
      "anchor": "descriptive parent-Hub anchor",
      "placement": "strongest contextual placement"
    },
    {
      "id": "process-bridge",
      "supporting_authority": "skill-process-bridge",
      "source_node_id": "FL-M008",
      "target_node_id": "FL-M004",
      "v2_reference_path": "/divorce/contested-divorce/",
      "client_url": "https://client.example/verified-contested-route/",
      "client_url_status": 200,
      "client_url_redirects": 0,
      "client_url_verified_on": "YYYY-MM-DD",
      "client_url_evidence": "Direct response and destination-fit evidence",
      "destination_fit": "verified",
      "anchor": "descriptive Contested Divorce anchor",
      "placement": "high-conflict versus contested distinction"
    },
    {
      "id": "consultation-cta",
      "supporting_authority": "consultation-cta",
      "source_node_id": "FL-M008",
      "destination_kind": "consultation-contact",
      "client_url": "https://client.example/verified-contact-route/",
      "client_url_status": 200,
      "client_url_redirects": 0,
      "client_url_verified_on": "YYYY-MM-DD",
      "client_url_evidence": "Direct response and contact-destination evidence",
      "destination_fit": "verified",
      "anchor": "supported consultation invitation",
      "placement": "final CTA section"
    }
  ],
  "quality_contract": {
    "forbidden_terms": ["assignment-specific contamination phrase"]
  },
  "content": [
    {"type": "p", "runs": [{"type": "text", "text": "Answer-first opening."}]},
    {"type": "p", "runs": [{"type": "text", "text": "Stakes-focused opening."}]},
    {"type": "h2", "role": "scenario", "text": "Scenario heading"},
    {"type": "ul", "items": [{"runs": [{"type": "strong", "text": "Lead-in: "}, {"type": "text", "text": "Explanation."}]}]},
    {"type": "p", "runs": [{"type": "text", "text": "Material legal claim. "}, {"type": "citation", "source_id": 1, "text": "[1]"}]}
  ],
  "sources": [
    {
      "id": 1,
      "label": "Official primary-authority identifier",
      "url": "https://official.example/authority",
      "authority": "official-primary",
      "status": 200,
      "verified_on": "YYYY-MM-DD",
      "verification_evidence": "Live verification note"
    }
  ]
}
```

The production `content` array must include the complete 1,100–1,700-word page and all required H2 roles. Each manifested link must appear exactly once as an `internal_link` run; the consultation link must appear after the final `role: cta` H2. Each source must be cited exactly once in body content; the generator adds the matching Sources hyperlink. Bold lead-ins use `strong` runs.
