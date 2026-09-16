# Coordinator instruction

Spawn exactly one custom subagent with `agent_type: seo_reviewer`, `task_name: wisconsin_divorce_core_revision_review`, and `fork_turns: none`. Give that reviewer the task below, wait for it to finish, and return its findings verbatim. Do not perform the substantive review yourself. Do not spawn any other agent. The reviewer is read-only and must not edit files.

# Reviewer task

Independently review the revised Wisconsin Divorce Core Hub copy and the actual V2 records. This is one substantive review pass, not a score of reviewer effectiveness.

## Original revision task

The strategist was asked to:

1. Preserve V2 IDs, page types, hierarchy, relationships, requiredness, and gates while mapping each eligible node to a separate verified client URL. Use direct Wisconsin destinations; restore collaborative, mediation, and legal-separation links; retain high-conflict as a Situational child with a contextual link; do not change site routing.
2. Correct `FL-M030` and `FL-M033` to Practice-Area Educational Page / Educational / Optional.
3. Revise as Sterling, bring fixed-fee/service choices earlier, replace repetitive “a lawyer can” language, distinguish mediation from collaborative divorce, remove outside-observer commentary, and preserve verified legal qualifications. Treat 5-8 sources as guidance, not a cap.
4. Record that V2/client path differences do not establish migration need; the two filing pages need ownership review without a predetermined consolidation or redirect; omitting Optional `FL-M030` does not block the hub; consultation terms remain unpromised.
5. Add focused client-URL-mapping regressions without weakening jurisdiction, relationship, or V2 gate checks.

## Files to inspect

- Governing V2 data: `/Users/rocketclicks_1/SEO_Dept/context/architecture/Family_Law_StructureV2.html`
- Readable architecture guide: `/Users/rocketclicks_1/SEO_Dept/context/architecture/family-law-architecture-v2.md`
- Revised workflow input and full copy: `/Users/rocketclicks_1/SEO_Dept/clients/sterling/deliverables/wisconsin-divorce-core/workflow-input.json`
- Revised DOCX: `/Users/rocketclicks_1/SEO_Dept/clients/sterling/deliverables/wisconsin-divorce-core/wisconsin-divorce-core.docx`
- Supporting record: `/Users/rocketclicks_1/SEO_Dept/clients/sterling/deliverables/wisconsin-divorce-core/supporting-record.md`
- Generator: `/Users/rocketclicks_1/SEO_Dept/.agents/skills/family-law-service-pages/scripts/build-core-hub.js`
- Regression harness: `/Users/rocketclicks_1/SEO_Dept/.agents/skills/family-law-service-pages/scripts/test-core-hub.py`
- Regression summary: `/Users/rocketclicks_1/SEO_Dept/evaluations/runs/2026-09-15-family-law-core-hub-workflow/validation-client-url-mapping/negative-test-summary.md`
- Relevant skill/voice rules: `/Users/rocketclicks_1/SEO_Dept/.agents/skills/family-law-service-pages/SKILL.md` and `/Users/rocketclicks_1/SEO_Dept/.agents/skills/sterling-voice/SKILL.md`

## Fixed review criteria

- V2 and client URL fields are genuinely separate; client pathname differences do not weaken exact V2 identity, classification, relationship, requiredness, or gate validation.
- The enabled client URLs are direct Wisconsin destinations and the DOCX targets them, not redirecting V2-path URLs.
- Required children `FL-M003` through `FL-M008` are appropriately represented; `FL-M008` remains Situational; `FL-M030` and `FL-M033` are Educational/Optional.
- The copy speaks directly as Sterling, gives useful service guidance early, distinguishes mediation and collaborative divorce accurately, and avoids internal architecture or outside-observer commentary.
- Legal and business claims do not outrun the supplied primary/first-party evidence.
- The filing-page and consultation unknowns are framed without predetermined action or promises.
- Source count is judged by usefulness and support, not a numeric cap.
- Relevance and prioritization come before suggestions to expand. More research or more output does not establish better judgment.

## Source inventory already checked by the strategist

Direct `200`, zero-redirect client URLs checked 2026-09-15:

- Hub: `https://www.sterlinglawyers.com/wisconsin/divorce/`
- `FL-M003`: `https://www.sterlinglawyers.com/wisconsin/divorce/collaborative/`
- `FL-M004`: `https://www.sterlinglawyers.com/wisconsin/divorce/contested-divorce/`
- `FL-M005`: `https://www.sterlinglawyers.com/wisconsin/divorce/mediation/`
- `FL-M006`: `https://www.sterlinglawyers.com/wisconsin/divorce/separation/`
- `FL-M007`: `https://www.sterlinglawyers.com/wisconsin/divorce/uncontested-divorce/`
- `FL-M008`: `https://www.sterlinglawyers.com/wisconsin/divorce/high-conflict-divorce/`
- `FL-M033`: `https://www.sterlinglawyers.com/wisconsin/divorce/temporary-orders-in-divorce/`
- Filing candidates: `https://www.sterlinglawyers.com/wisconsin/divorce/file-for-divorce/` and `https://www.sterlinglawyers.com/wisconsin/divorce/how-to-file-for-divorce-in-wisconsin/`

Primary legal sources in the draft: Wis. Stat. §§ 767.301, 767.315, 767.335, 767.61, 767.56, 767.41, 767.511, 767.35; Wisconsin SCR 20:2.4; and *Kemper Independence Insurance Co. v. Islami*, 2021 WI 53, ¶ 18. Business evidence is the current Wisconsin pricing, collaborative-service, and hub pages. No current Wisconsin statute defining collaborative divorce was found, so those mechanics must stay attributed to Sterling's published service.

## Output

Return concrete findings only, ordered by severity: Blocker, Material, Optional. For each finding, identify the exact file/location, evidence, why it matters, and the smallest correction. Explicitly say if there are no Blocker or Material findings. Do not invent objections, propose broad crawling, edit files, or score your own effectiveness.
