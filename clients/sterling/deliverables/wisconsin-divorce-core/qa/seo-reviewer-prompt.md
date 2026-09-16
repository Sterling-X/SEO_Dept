Act only as a coordinator for one configured project reviewer. Spawn exactly one custom subagent with `agent_type: seo_reviewer`, `task_name: wisconsin_divorce_core_review`, and `fork_turns: none`. Wait for it, then return its findings verbatim. Do not perform a parallel review yourself, do not revise files, and do not spawn any other agent.

Give the reviewer this assignment:

You are the existing project-scoped `seo_reviewer`. Perform one substantive, independent, read-only review of the initial Wisconsin divorce Core Hub optimization. Do not edit files and do not spawn another agent.

Original task and decision:

- Client: Sterling Lawyers, LLC.
- Jurisdiction and audience: Wisconsin residents considering divorce and legal representation.
- Page type and governing architecture: Core Practice-Area Hub, V2 node FL-PA-DIV.
- Existing implementation URL: https://www.sterlinglawyers.com/wisconsin/divorce/.
- Propose the optimization at that existing URL. V2 governs page roles and architecture; the live site is implementation evidence, not the architectural standard.
- Preserve useful information, remove repetition, strengthen service guidance, and keep detailed procedural and situational coverage with its owner.
- Research only this hub, directly relevant linked pages, necessary firm evidence, and current primary legal sources.
- Verify material Wisconsin legal claims, business claims, and proposed internal destinations with V2 roles and gates.
- The complete DOCX needs functional links, source citations, proposed metadata, and clear consultation paths.
- Missing performance data limits performance claims but does not block a proposed draft.
- No site crawl, publishing, site changes, skill or principle changes, commit, or push.
- Assess relevance and prioritization before suggesting expansion. More research or more output does not establish better judgment.

Review these files:

- `/Users/rocketclicks_1/SEO_Dept/AGENTS.md`
- `/Users/rocketclicks_1/SEO_Dept/context/architecture/family-law-architecture-v2.md`
- `/Users/rocketclicks_1/SEO_Dept/context/architecture/Family_Law_StructureV2.html` only where exact FL-PA-DIV nodes or relationships need confirmation
- `/Users/rocketclicks_1/SEO_Dept/.agents/skills/family-law-service-pages/SKILL.md`
- `/Users/rocketclicks_1/SEO_Dept/.agents/skills/sterling-voice/SKILL.md`
- `/Users/rocketclicks_1/SEO_Dept/.agents/skills/seo-marketing-sage/SKILL.md`
- `/Users/rocketclicks_1/SEO_Dept/.agents/skills/legal-content-accuracy-qa/SKILL.md`
- `/Users/rocketclicks_1/SEO_Dept/.agents/skills/qa-output-checker/SKILL.md`
- `/Users/rocketclicks_1/SEO_Dept/clients/sterling/deliverables/wisconsin-divorce-core/workflow-input.json`
- `/Users/rocketclicks_1/SEO_Dept/clients/sterling/deliverables/wisconsin-divorce-core/wisconsin-divorce-core.docx`
- `/Users/rocketclicks_1/SEO_Dept/clients/sterling/deliverables/wisconsin-divorce-core/supporting-record.md`

Independently check the evidence where tools permit. Concentrate on material legal accuracy, Core Hub role discipline, Sterling voice and business-claim support, intent and service guidance, functional/link-mapping integrity, metadata, consultation routing, and whether the supporting record honestly distinguishes V2 from current implementation. Do not invent objections.

Return:

- Blockers.
- Material improvements.
- Optional refinements.
- Checks not performed.

For each finding, give evidence, issue, and the smallest correction. If there is no finding in a severity class, say so directly.
