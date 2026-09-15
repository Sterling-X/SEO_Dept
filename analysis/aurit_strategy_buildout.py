#!/usr/bin/env python3
"""
Build the Divorce / Child Support / Child Custody / Spousal Maintenance sections
of the Aurit Mediation 2026 Strategic Plan.

Source of truth for structure:  preview (1).html  (Hub Page Format & Expansion Structure V4)
Source of truth for metadata:   Aurit Mediation - Architecture Master Production V4 (Master_Architecture)
Source of truth for format:     Aurit Mediation _ 2026 Day Strategic Plan - Internal - Q3-4 2026.csv

Output columns match the strategy sheet exactly:
Status, CU, Projects, Description, Impact, July, Aug, Sep, Oct, Nov, Dec, Jan, Beyond
"""
import csv, os

HEADER = ["Status", "CU", "Projects", "Description", "Impact",
          "July", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Beyond"]

MONTHS = ["July", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Beyond"]

rows = []


def add(project, desc, impact, status="", cu="", **hrs):
    """hrs keyword args are month names -> hour value."""
    bad = set(hrs) - set(MONTHS)
    assert not bad, f"bad month key(s) {bad} on {project!r}"
    r = [status, cu, project, desc, impact] + [str(hrs.get(m, "")) if hrs.get(m) else "" for m in MONTHS]
    rows.append(r)


def sep(label):
    rows.append(["", "", label, "", ""] + [""] * 8)


# =============================================================================
# SECTION 1 - DIVORCE MEDIATION
# 28 URLs (1 hub + 27 linked children) | 19 on-hub topics | 7 held/excluded
# =============================================================================
sep("=== DIVORCE MEDIATION HUB CLUSTER (28 URLs / 27 child links / 19 on-hub topics / 7 not surfaced) ===")

add(
    "Core Service Hub Page\n- Divorce Mediation (L1 Main Practice Hub - Optimize & Expand)",
    "URL: /divorce-mediation/ (existing page - optimize and expand)\n"
    "- Rebuild the page opening to V4 format: unlinked H1 Divorce Mediation, 2-3 paragraph overview, "
    "trust proof, primary CTA, and an optional jump-link table of contents pointing to the six H2 section IDs.\n"
    "- Target 1,800-2,800 words on the hub itself.\n"
    "- Establish the six approved H2 topic sections on this single URL. Topic groups are internal "
    "organizational labels only - do not create secondary child hubs or group URLs.\n"
    "- Show roughly 6-10 featured child cards plus organized text-link modules.\n"
    "- Confirm all 27 approved standalone children in this cluster carry a required return link to this hub.\n"
    "Owner: SEO Strategist + Legal SME. Guardrail: state legal information, not individual legal advice; "
    "both spouses remain decision-makers.",
    "Concentrates authority for the highest-value head term in the account on one canonical URL instead of "
    "splitting it across near-duplicate pages. A correctly structured hub gives Google and AI retrieval systems "
    "a clean topical map of the entire divorce cluster, distributes internal PageRank to every approved child "
    "page, and lifts the hub's own eligibility for competitive Arizona divorce mediation queries. Strong "
    "on-hub organization also improves dwell and in-page navigation, feeding NavBoost-style behavioral signals "
    "back into every page beneath it.",
    Sep=8,
)

# --- H2 Section 1: Options, Alternatives & Legal Pathways ---------------------
add(
    "Hub Section Module (H2)\n- Compare Divorce Mediation With Other Divorce Options "
    "(Divorce Mediation Hub - On-Page Section, No URL)",
    "Build on /divorce-mediation/. Internal architecture group: Options, Alternatives & Legal Pathways "
    "(internal label only - never the public heading).\n"
    "Exact build format:\n"
    "- Unlinked H2: Compare Divorce Mediation With Other Divorce Options\n"
    "- 1-2 sentence section introduction\n"
    "- 2 featured cards, each a linked H3 card title plus one sentence: Mediation vs Litigation; "
    "Divorce Mediator vs Divorce Attorney\n"
    "- 1 supporting page as a compact descriptive text link (exact page title as anchor): "
    "Mediation vs Collaborative Divorce\n"
    "- 2 section-first topics written directly on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Legal Separation Mediation; Mediation vs Uncontested Divorce\n"
    "Do not link the H2. Do not create child URLs for the section-first topics. "
    "Do not surface Annulment Mediation (governance: do not build).\n"
    "Publish with whatever child links are already live and add remaining anchors as each child page ships.",
    "Comparison queries carry the highest commercial intent in the cluster and are the terms most often "
    "summarized in AI answers. Housing them under one clearly labeled H2 lets Google associate Aurit with the "
    "full decision set - litigation, attorney, collaborative, legal separation, uncontested - from a single "
    "crawl. Section-first treatment of the two lower-demand alternatives builds semantic coverage without "
    "spawning thin URLs that would cannibalize the featured comparison pages.",
    Sep=3,
)

add(
    "Core Comparison Content Page\n- Mediation vs Litigation (Divorce Mediation - Featured H3 Card)",
    "URL: /divorce-mediation/mediation-vs-litigation/ (existing page - optimize and expand)\n"
    "- Comparison Page Brief, 1,300-2,200 words. Tier 2, Wave 1, Priority High.\n"
    "- Cover cost, timeline, privacy, decision control, emotional load, and the case types each process "
    "genuinely suits.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; When Mediation May Not Be Appropriate.\n"
    "- Placement: featured linked H3 card in the Compare Divorce Mediation With Other Divorce Options module.\n"
    "Guardrail: do not denigrate courts or attorneys; explain the cases each process fits. "
    "Requires Arizona legal review and mediator-neutrality language.",
    "The single highest-intent comparison in the divorce cluster and a frequent citation source when AI systems "
    "explain process differences. Strengthening it captures users at the exact moment they choose a path, and "
    "featured-card placement passes hub authority to the page most likely to turn a researcher into a "
    "consultation.",
    Dec=4,
)

add(
    "Core Comparison Content Page\n- Divorce Mediator vs Divorce Attorney (Divorce Mediation - Featured H3 Card)",
    "URL: /divorce-mediation/divorce-mediator-vs-divorce-attorney/ (existing page - optimize and expand)\n"
    "- Comparison Page Brief, 1,300-2,200 words. Tier 2, Wave 1, Priority High.\n"
    "- Clarify role, neutrality, scope of service, who advises whom, and when independent counsel is "
    "appropriate.\n"
    "- Required return link to Divorce Mediation. Internal links: Independent Legal Review After Mediation; "
    "Pricing; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Compare Divorce Mediation With Other Divorce Options module.\n"
    "Guardrail: do not imply lawyers are unnecessary; encourage independent counsel where appropriate.",
    "Resolves the primary objection that stalls mediation inquiries - whether a neutral is enough without a "
    "lawyer. Explicit role definition is exactly the structured explanation AI systems reward when answering "
    "mediator-versus-attorney questions, and it pre-qualifies users on process fit so fewer unsuitable "
    "inquiries reach the consult calendar.",
    Dec=4,
)

add(
    "Core Comparison Content Page\n- Mediation vs Collaborative Divorce (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/mediation-vs-collaborative-divorce/ (new build)\n"
    "- Comparison Page Brief, 1,300-2,200 words. Tier 4, Wave 3, Priority Medium.\n"
    "- Compare professional team structure, cost, timeline, confidentiality, and what happens if the process "
    "breaks down.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link (exact page title as anchor) in the Compare Divorce Mediation "
    "With Other Divorce Options module.\n"
    "Guardrail: do not disparage collaborative professionals.",
    "Collaborative divorce is the closest substitute service and the one comparison Aurit does not currently "
    "own. Publishing it closes the last gap in the alternative-dispute-resolution cluster, gives search engines "
    "an explicit differentiation signal, and intercepts high-value prospects who have already ruled out court "
    "but have not chosen a provider.",
    Beyond=4,
)

# --- H2 Section 2: Suitability, Participation & Safety ------------------------
add(
    "Hub Section Module (H2)\n- When Divorce Mediation Works and When It May Not "
    "(Divorce Mediation Hub - On-Page Section, No URL)",
    "Build on /divorce-mediation/. Internal architecture group: Suitability, Participation & Safety.\n"
    "Exact build format:\n"
    "- Unlinked H2: When Divorce Mediation Works and When It May Not\n"
    "- 1-2 sentence section introduction\n"
    "- 2 featured cards (linked H3 + one sentence): Is Divorce Mediation Right for Us?; "
    "When Mediation May Not Be Appropriate\n"
    "- 4 supporting descriptive text links: Can Mediation Work If We Disagree?; High-Conflict Divorce "
    "Mediation; Divorce Mediation When Communication Is Difficult; Divorce Mediation When One Spouse Is "
    "Reluctant\n"
    "- 6 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Divorce Mediation When Spouses Disagree About Everything; When Divorce Mediation Works Best; "
    "How to Talk to Your Spouse About Mediation; Divorce Mediation With an Addicted Spouse; "
    "Divorce Mediation When One Spouse Refuses to Sign; Mediation When One Spouse Has Not Responded\n"
    "Keep Mediation Suitability Quiz off the live page until approved. Do not surface Protective Orders and "
    "Divorce Mediation, Restraining Orders / Orders of Protection, or Domestic Violence Divorce Mediation.\n"
    "Guardrail: explicitly address coercive control, violence, hidden assets, and urgent court needs; include "
    "hotline and court self-help resources. Mandatory legal review.",
    "The largest section in the cluster and the one that most directly controls lead quality. Suitability "
    "content filters out matters mediation cannot serve, which protects the firm and lifts consult-to-signed "
    "rates, while six substantive on-hub topics give the page the depth and dwell behavior Google rewards. "
    "Treating safety topics as guarded on-page content rather than standalone service pages keeps Aurit out of "
    "the YMYL risk zone while still earning the semantic coverage those queries generate.",
    Sep=4,
)

add(
    "Core Comparison Content Page\n- Is Divorce Mediation Right for Us? (Divorce Mediation - Featured H3 Card)",
    "URL: /divorce-mediation/is-divorce-mediation-right-for-us/ (new build)\n"
    "- Comparison Page Brief, 1,300-2,200 words. Tier 2, Wave 1, Priority Highest.\n"
    "- Build a self-screening framework: what supports a productive process, what does not, and what to do "
    "instead when mediation is not the right fit.\n"
    "- Required return link to Divorce Mediation. Internal links: When Divorce Mediation Works Best; "
    "When Mediation May Not Be Appropriate; Free Consultation.\n"
    "- Placement: featured linked H3 card in the When Divorce Mediation Works and When It May Not module.\n"
    "Guardrail: explicitly discuss coercive control, violence, hidden assets, and urgent court needs. "
    "Requires legal review.",
    "Captures the exact question most prospects ask before they contact anyone, making it the highest-leverage "
    "top-of-funnel asset in the cluster. Self-qualification content converts above average because users arrive "
    "already reassured, and its question-form framing makes it the page most likely to be surfaced when AI "
    "systems answer whether a specific situation suits mediation.",
    Dec=4,
)

add(
    "Core Comparison Content Page\n- When Mediation May Not Be Appropriate (Divorce Mediation - Featured H3 Card)",
    "URL: /divorce-mediation/when-mediation-may-not-be-appropriate/ (new build)\n"
    "- Comparison Page Brief, 1,300-2,200 words. Tier 2, Wave 1, Priority Highest.\n"
    "- Cover coercion and control dynamics, safety concerns, concealed assets, capacity issues, and urgent "
    "court relief.\n"
    "- Required return link to Divorce Mediation. Internal links: Domestic Violence Resources; "
    "Independent Legal Review After Mediation; Free Consultation.\n"
    "- Placement: featured linked H3 card in the When Divorce Mediation Works and When It May Not module.\n"
    "Guardrail: primary safety and legal guardrail page for the site. Include hotline, emergency, and court "
    "self-help resources plus explicit emergency language. Mandatory legal review before publishing.",
    "Functions as the firm's public disqualification and safety guardrail, which is both an ethical requirement "
    "and a strong E-E-A-T signal in a YMYL category. Search and AI systems weight a provider's willingness to "
    "state when its service does not apply as a trust marker, and internally the page deflects unsuitable "
    "inquiries before they consume consult capacity.",
    Dec=4,
)

add(
    "Core Comparison Content Page\n- Can Mediation Work If We Disagree? (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/can-mediation-work-if-we-disagree/ (new build)\n"
    "- Comparison Page Brief, 1,300-2,200 words. Tier 2, Wave 1, Priority High.\n"
    "- Separate ordinary disagreement from coercion and safety risk; explain how a neutral structures conflict "
    "and keeps negotiation productive.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation When Communication Is "
    "Difficult; High-Conflict Divorce Mediation; Is Divorce Mediation Right for Us?\n"
    "- Placement: compact descriptive text link in the When Divorce Mediation Works and When It May Not module.\n"
    "Guardrail: balanced - disagreement is mediable, coercion and safety concerns are not.",
    "Addresses the most common self-disqualifying belief among otherwise qualified prospects, recovering demand "
    "that would otherwise default straight to litigation. Question-form headings map closely to conversational "
    "and voice queries, improving retrieval in AI answers where the user frames the problem as a doubt rather "
    "than a service search.",
    Jan=4,
)

add(
    "Live Page V4 Retrofit\n- High-Conflict Divorce Mediation (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/high-conflict-divorce-mediation/ - page already published "
    "(ClickUp 86b9330x8, marked Complete). Retrofit only, no new draft:\n"
    "- Add or verify the required return link to the Divorce Mediation hub.\n"
    "- Add or verify sibling links: Can Mediation Work If We Disagree?; Divorce Mediation When Communication "
    "Is Difficult; When Mediation May Not Be Appropriate.\n"
    "- Verify the suitability limit language: high conflict is not the same as coercion or safety risk.\n"
    "- Place as a compact descriptive text link in the When Divorce Mediation Works and When It May Not "
    "module, using the exact page title as anchor text.",
    "Converts an already-published asset into a properly wired cluster node. Return links and sibling links "
    "are what turn isolated situational pages into a cluster Google recognizes as a unit, and correct anchor "
    "placement on the hub delivers authority the page is not currently receiving.",
    Sep=1,
)

add(
    "Core Situational Content Page\n- Divorce Mediation When Communication Is Difficult "
    "(Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/divorce-mediation-when-communication-is-difficult/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Cover shuttle and caucus formats, structured turn-taking, written proposals, and pacing when direct "
    "conversation has broken down.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the When Divorce Mediation Works and When It May Not module.\n"
    "Guardrail: do not imply mediation fixes abusive dynamics.",
    "Targets a distinct behavioral cluster that Google separates from general high-conflict divorce queries. "
    "Explaining concrete process mechanics for poor communicators makes Aurit retrievable for a large group "
    "of searchers who assume they are ineligible, and the process detail is the kind of structured explanation "
    "AI systems prefer to cite.",
    Jan=4,
)

add(
    "Core Situational Content Page\n- Divorce Mediation When One Spouse Is Reluctant "
    "(Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/divorce-mediation-when-one-spouse-is-reluctant/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain voluntary participation, how invitations and neutral outreach work, and realistic options if "
    "the other spouse declines.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the When Divorce Mediation Works and When It May Not module.\n"
    "Guardrail: explain voluntary participation; do not suggest pressure or coercive tactics.",
    "Serves the single-motivated-spouse searcher, who is the most common inbound profile and the most likely "
    "to abandon the process without guidance. Capturing this intent converts a stalled inquiry into a scheduled "
    "consult and adds a differentiated page to a suitability cluster competitors treat only as an FAQ line.",
    Jan=4,
)

# --- H2 Section 3: Process, Timing & Representation ---------------------------
add(
    "Hub Section Module (H2)\n- How the Divorce Mediation Process Works "
    "(Divorce Mediation Hub - On-Page Section, No URL)",
    "Build on /divorce-mediation/. Internal architecture group: Process, Timing & Representation.\n"
    "Exact build format:\n"
    "- Unlinked H2: How the Divorce Mediation Process Works\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): Mediation After Filing for Divorce\n"
    "- 3 supporting descriptive text links: Mediation Before Filing for Divorce; Mediation With Attorneys "
    "Involved; Mediation for Self-Represented Couples\n"
    "- 2 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Partial Agreement Mediation; Divorce by Publication / Missing Spouse Mediation\n"
    "Keep Fast Divorce Mediation off this module until the /quick-divorce-arizona/ audit and "
    "consolidation decision is complete.\n"
    "Guardrail: do not instruct parties to ignore court orders or deadlines; do not overpromise full settlement.",
    "Process transparency is the strongest trust lever on a mediation hub and the section users scroll to "
    "before converting. Organizing timing and representation questions under one H2 reduces pogo-sticking back "
    "to the SERP, and the before-filing versus after-filing split matches how Google separates procedural "
    "intent, making the hub eligible for both query families from one page.",
    Sep=3,
)

add(
    "Core Process Content Page\n- Mediation After Filing for Divorce (Divorce Mediation - Featured H3 Card)",
    "URL: /divorce-mediation/mediation-after-filing-for-divorce/ (new build)\n"
    "- Process Page Brief, 1,200-2,000 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain how mediation fits alongside an open case, coordination with deadlines, and how agreements "
    "reach the court.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: featured linked H3 card in the How the Divorce Mediation Process Works module.\n"
    "Guardrail: do not instruct parties to ignore court orders or deadlines. Requires legal review.",
    "Captures searchers who already have an active case and therefore have urgency, a filing date, and budget "
    "in motion - the fastest-closing segment in the cluster. It also removes the common misconception that "
    "filing forecloses mediation, which currently sends qualified demand to litigation firms.",
    Jan=4,
)

add(
    "Core Process Content Page\n- Mediation Before Filing for Divorce (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/mediation-before-filing-for-divorce/ (new build)\n"
    "- Process Page Brief, 1,200-2,000 words. Tier 3, Wave 3, Priority Medium.\n"
    "- Explain pre-filing sequencing, what can be agreed in advance, and how a mediated agreement becomes "
    "part of the eventual filing.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the How the Divorce Mediation Process Works module.\n"
    "Guardrail: avoid suggesting mediation bypasses legal requirements.",
    "Reaches users at the earliest, cheapest-to-acquire point in the journey, before an attorney relationship "
    "forms. Owning pre-filing intent lengthens the relationship window and pairs with the after-filing page to "
    "give Google complete timeline coverage for Arizona divorce process queries.",
    Beyond=4,
)

add(
    "Core Process Content Page\n- Mediation With Attorneys Involved (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/mediation-with-attorneys-involved/ (new build)\n"
    "- Process Page Brief, 1,200-2,000 words. Tier 3, Wave 3, Priority Medium.\n"
    "- Explain attorney-participating formats, review-only counsel, and how the mediator's neutrality is "
    "preserved when lawyers attend.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the How the Divorce Mediation Process Works module.\n"
    "Guardrail: clarify the mediator remains neutral and attorneys advise their own clients.",
    "Removes the objection that retaining counsel rules out mediation, and positions Aurit as a referral-safe "
    "partner for family-law attorneys rather than a competitor. That dual audience creates a natural "
    "professional-referral link path in addition to the organic ranking benefit.",
    Beyond=4,
)

add(
    "Core Situational Content Page\n- Mediation for Self-Represented Couples "
    "(Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/mediation-for-self-represented-couples/ "
    "(build standalone page from verified partial live coverage)\n"
    "- Situation / Use-Case Brief, 1,100-1,700 words. Tier 3, Wave 3, Priority High.\n"
    "- Explain what mediation looks like without attorneys, where legal information stops and legal advice "
    "begins, and what independent review is still recommended.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; How Mediation Works; "
    "Legal Information vs Legal Advice in Mediation; Independent Legal Review After Mediation; "
    "Court Filing After Mediation in Arizona; Free Consultation.\n"
    "- Placement: compact descriptive text link in the How the Divorce Mediation Process Works module.\n"
    "Guardrail: never imply Aurit represents either spouse or replaces independent legal advice.",
    "Aligns with cost-sensitive no-lawyer search intent, one of the largest and least-served query families in "
    "Arizona family law. It also anchors the legal-information-versus-advice distinction that protects the firm "
    "and reinforces neutrality signals search engines associate with a credible mediation entity.",
    Beyond=4,
)

# --- H2 Section 4: Families & Parenting Situations ----------------------------
add(
    "Hub Section Module (H2)\n- Divorce Mediation for Parents and Families "
    "(Divorce Mediation Hub - On-Page Section, No URL)",
    "Build on /divorce-mediation/. Internal architecture group: Families & Parenting Situations.\n"
    "Exact build format:\n"
    "- Unlinked H2: Divorce Mediation for Parents and Families\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): Divorce Mediation With Children\n"
    "- 2 supporting descriptive text links: Arizona Divorce Mediation for Parents Guide; "
    "Divorce and Children Resource Hub\n"
    "- 4 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Divorce Mediation for Blended Families; Divorce Mediation With a Disabled Spouse or Child; "
    "Divorce Mediation for LGBTQ+ Parents; Divorce Mediation During Pregnancy\n"
    "Cross-link this module to the Child Custody Mediation and Parenting Plan Mediation hubs so parenting "
    "intent is routed, not duplicated.\n"
    "Guardrail: use disability-sensitive and inclusive language; do not overgeneralize. Legal review required "
    "for pregnancy-related timing statements.",
    "Connects the divorce hub to the two parenting hubs without duplicating their content, which is what keeps "
    "custody and parenting-plan pages from cannibalizing each other. The four on-hub family scenarios add "
    "coverage for demographically specific searches at zero URL cost, letting Aurit appear for niche parenting "
    "circumstances while authority stays concentrated on the canonical pages.",
    Sep=4,
)

add(
    "Core Situational Content Page\n- Divorce Mediation With Children (Divorce Mediation - Featured H3 Card)",
    "URL: /divorce-mediation/divorce-mediation-with-children/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain how child-related decisions connect to property and support issues, and how parents keep "
    "children out of the negotiation.\n"
    "- Required return link to Divorce Mediation. Internal links: Child Custody Mediation; "
    "Parenting Plan Mediation; Child Support Mediation; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Divorce Mediation for Parents and Families module.\n"
    "Guardrail: avoid promising custody outcomes; preserve child-centered neutrality.",
    "Parents with minor children are the highest-value and highest-urgency segment of divorce demand. This page "
    "is the bridge asset that carries divorce searchers into the custody, parenting plan, and child support "
    "clusters, multiplying the internal link value of three other hubs while ranking for a high-volume "
    "qualifier in its own right.",
    Jan=4,
)

add(
    "Core Resource Content Page\n- Arizona Divorce Mediation for Parents Guide "
    "(Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/arizona-divorce-mediation-for-parents-guide/ (new build)\n"
    "- Resource / Tool Brief, 1,000-2,500 words plus a downloadable checklist. Tier 4, Wave 6, "
    "Priority Medium.\n"
    "- Assemble an end-to-end parent-facing guide covering preparation, child-focused decision points, and "
    "next steps.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation With Children; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Divorce Mediation for Parents and Families module.\n"
    "Guardrail: include neutral legal-information-not-advice disclaimers and links to core service pages.",
    "Long-form guides earn the links and shares that individual service pages cannot, which raises the "
    "authority of every page they link to. As a gated or semi-gated asset it also captures contact details "
    "from parents who are researching months before they are ready to book, feeding the nurture pipeline.",
    Beyond=5,
)

add(
    "Core Resource Content Page\n- Divorce and Children Resource Hub (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/divorce-and-children-resource-hub/ (new build)\n"
    "- Resource / Tool Brief, 1,000-2,500 words plus curated resource set. Tier 4, Wave 6, Priority Medium.\n"
    "- Curate age-appropriate explanation guidance, co-parenting tools, counseling referrals, and school "
    "communication resources.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation With Children; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Divorce Mediation for Parents and Families module.\n"
    "Guardrail: include neutral legal-information-not-advice disclaimers; avoid clinical or therapeutic claims.",
    "Resource curation attracts informational and citation traffic that pure service pages never reach, and "
    "it is the most natural link-earning asset in the divorce cluster. Demonstrating child-first concern also "
    "strengthens the experience and trustworthiness signals Google weighs heavily in family-law YMYL "
    "assessment.",
    Beyond=5,
)

# --- H2 Section 5: Specific Divorce Situations --------------------------------
add(
    "Hub Section Module (H2)\n- Divorce Mediation for Complex and Unique Situations "
    "(Divorce Mediation Hub - On-Page Section, No URL)",
    "Build on /divorce-mediation/. Internal architecture group: Specific Divorce Situations.\n"
    "Exact build format:\n"
    "- Unlinked H2: Divorce Mediation for Complex and Unique Situations\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): High-Asset Divorce Mediation\n"
    "- 6 supporting descriptive text links: Amicable Divorce Mediation; Uncontested Divorce Mediation; "
    "Gray Divorce Mediation; Gray Divorce Financial Checklist; Same-Sex Divorce Mediation; "
    "Military Divorce Mediation\n"
    "- 5 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Divorce Mediation When One Spouse Is in Another State; Divorce Mediation After Infidelity; "
    "Divorce Mediation After 50; Divorce Mediation for Second Marriages; Divorce Mediation With an "
    "Incarcerated Spouse\n"
    "Guardrail: avoid fault-based framing in Arizona's no-fault context; jurisdiction statements require "
    "legal review.",
    "The widest text-link module on the hub and the primary distribution point for six situational pages that "
    "would otherwise sit orphaned. Grouping them under one H2 tells Google these pages form a single "
    "situational family, which lifts the weakest members on the strength of the cluster, while five on-hub "
    "scenarios absorb long-tail demand without adding thin URLs.",
    Sep=4,
)

add(
    "Live Page V4 Retrofit\n- High-Asset Divorce Mediation (Divorce Mediation - Featured H3 Card)",
    "URL: /divorce-mediation/high-asset-divorce-mediation/ - canonical high-asset page for the divorce hub. "
    "A High-Net-Worth Divorce Mediation page is already published (ClickUp 86b93344j, marked Complete).\n"
    "Retrofit and consolidation:\n"
    "- Confirm which URL is live and canonicalize or 301 the high-net-worth variant into this page. Do not "
    "run two competing high-value pages.\n"
    "- Verify Tier 2 / Wave 1 / Priority Highest depth: 1,100-1,900 words covering privacy, valuation, "
    "advisors, and legal or financial review.\n"
    "- Add or verify the required return link to Divorce Mediation. Internal links: Divorce Mediation; "
    "Pricing; How Mediation Works; Free Consultation.\n"
    "- Keep High-Net-Worth Property Division Mediation as a section-first topic on the Property and Debt "
    "Division hub - it is not a second divorce page.\n"
    "- Placement: featured linked H3 card in the Divorce Mediation for Complex and Unique Situations module.",
    "High-asset queries carry the highest revenue per lead in the practice, and running two near-identical "
    "high-value pages currently splits that authority and risks both underperforming. Consolidating to one "
    "canonical URL recovers the full signal, and featured-card placement puts the firm's most profitable "
    "segment one click from the hub.",
    Oct=2,
)

add(
    "Core Situational Content Page\n- Amicable Divorce Mediation (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/amicable-divorce-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Cover the streamlined path for couples who already agree on most issues, and how to protect the "
    "agreement without creating conflict.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Uncontested Divorce "
    "Mediation; Pricing; How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Divorce Mediation for Complex and Unique Situations "
    "module.\n"
    "Coordinate scope with Uncontested Divorce Mediation to avoid overlap.",
    "Amicable searchers are the fastest and cheapest matters to close and the most likely to leave a strong "
    "review, which compounds local pack performance. The term also signals mediation preference explicitly, "
    "making it one of the best-converting non-brand queries available to the firm.",
    Beyond=4,
)

add(
    "Core Situational Content Page\n- Uncontested Divorce Mediation (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/uncontested-divorce-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain what uncontested means procedurally in Arizona, what still must be documented, and how "
    "mediation supports a clean filing.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Amicable Divorce "
    "Mediation; Court Filing After Mediation in Arizona; Pricing; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Divorce Mediation for Complex and Unique Situations "
    "module.\n"
    "Dependency: coordinate with the /quick-divorce-arizona/ audit and the Divorce Mediation Timeline page "
    "before publishing, to prevent a third competing speed and simplicity page.",
    "Uncontested divorce carries substantially higher search volume than most mediation terms and pulls "
    "cost-motivated searchers who are already screening out attorneys. Capturing that query with a mediation "
    "framing converts a commodity search into a service inquiry, provided the speed-intent cluster is "
    "consolidated rather than duplicated.",
    Beyond=4,
)

add(
    "Live Page V4 Retrofit\n- Gray Divorce Mediation (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/gray-divorce-mediation/ - page already published "
    "(ClickUp 86b81ac3g, marked Complete). Retrofit only, no new draft:\n"
    "- Add or verify the required return link to the Divorce Mediation hub.\n"
    "- Add or verify internal links to Gray Divorce Financial Checklist, Spousal Maintenance After "
    "Retirement, and Retirement Account Division Mediation.\n"
    "- Place as a compact descriptive text link in the Divorce Mediation for Complex and Unique Situations "
    "module using the exact page title as anchor text.",
    "Wires a published page into both the divorce and the retirement or maintenance clusters, which is where "
    "its commercial value actually sits. Cross-cluster linking is how Google recognizes that later-life divorce "
    "spans property, pension, and support intent, raising the page's eligibility across all three.",
    Sep=1,
)

add(
    "Core Resource Content Page\n- Gray Divorce Financial Checklist (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/gray-divorce-financial-checklist/ (new build)\n"
    "- Resource / Tool Brief, 1,000-2,500 words plus downloadable checklist. Tier 3, Wave 6, Priority Medium.\n"
    "- Cover retirement accounts, pensions, Social Security timing considerations, healthcare coverage, "
    "housing, and estate document updates.\n"
    "- Required return link to Divorce Mediation. Internal links: Gray Divorce Mediation; "
    "Retirement Account Division Mediation; Spousal Maintenance After Retirement; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Divorce Mediation for Complex and Unique Situations "
    "module.\n"
    "Guardrail: include neutral legal-information-not-advice disclaimers; recommend independent financial "
    "review. Mediator does not value assets for either party.",
    "Later-life divorce is the fastest-growing segment nationally and the one with the most complex asset "
    "profile, which maps directly to Aurit's highest-value service tier. A practical checklist earns links "
    "from financial-planning and retirement publications, a link neighborhood the site currently has no "
    "presence in.",
    Beyond=5,
)

add(
    "Live Page V4 Retrofit\n- Same-Sex Divorce Mediation (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/same-sex-divorce-mediation/ - page already published "
    "(ClickUp 86b81ac0f, marked Complete). Retrofit only, no new draft:\n"
    "- Add or verify the required return link to the Divorce Mediation hub.\n"
    "- Add or verify internal links to Divorce Mediation, Pricing, How Mediation Works, and Free Consultation.\n"
    "- Verify parenting and property nuance has had expert review; avoid tokenism.\n"
    "- Place as a compact descriptive text link in the Divorce Mediation for Complex and Unique Situations "
    "module using the exact page title as anchor text.\n"
    "Note: Divorce Mediation for LGBTQ+ Parents stays as an unlinked on-hub H3/H4 topic in the Parents and "
    "Families module - it does not become a second URL.",
    "Ensures an existing differentiated page is actually reachable and credited from the hub. Holding the "
    "LGBTQ+ parenting angle as on-hub content rather than a second URL prevents two thin pages from competing "
    "for one small query family while still covering the parentage and rights nuance AI systems treat as a "
    "distinct cluster.",
    Sep=1,
)

add(
    "Core Situational Content Page\n- Military Divorce Mediation (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/military-divorce-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 4, Wave 7, Priority Medium.\n"
    "- Cover residency and jurisdiction, deployment scheduling, the USFSPA framework at a general level, "
    "TRICARE continuity, and remote participation.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Online Divorce "
    "Mediation; Pricing; How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Divorce Mediation for Complex and Unique Situations "
    "module.\n"
    "Guardrail: use careful jurisdiction, benefits, pension, and deployment language. Requires legal review.",
    "Arizona's military population around Luke Air Force Base, Davis-Monthan, and Fort Huachuca creates "
    "geo-qualified demand no local mediation competitor addresses in depth. Deployment schedules also make "
    "this audience unusually well suited to Aurit's online model, so the page reinforces the virtual service "
    "line as well as the divorce cluster.",
    Beyond=4,
)

# --- H2 Section 6: Guides, Tools & FAQs ---------------------------------------
add(
    "Hub Section Module (H2)\n- Arizona Divorce Mediation Guides, Checklists, and FAQs "
    "(Divorce Mediation Hub - On-Page Section, No URL)",
    "Build on /divorce-mediation/. Internal architecture group: Guides, Tools & FAQs.\n"
    "Exact build format:\n"
    "- Unlinked H2: Arizona Divorce Mediation Guides, Checklists, and FAQs\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): Arizona Divorce Mediation Guide\n"
    "- 3 supporting descriptive text links: Questions to Ask a Divorce Mediator; Divorce Mediation FAQ; "
    "Glossary of Arizona Divorce Mediation Terms\n"
    "- No section-first or FAQ topics in this module.\n"
    "Do not surface Questions to Ask a Divorce Mediator - Consolidated Resource Alias "
    "(governance: consolidate into the canonical page, no second URL).",
    "Closes the hub with the resource layer that earns links and captures early-stage researchers, giving the "
    "page a natural conversion off-ramp for users who are not yet ready to book. Keeping the consolidated alias "
    "suppressed protects the canonical resource page from splitting its own authority.",
    Sep=2,
)

add(
    "Core Resource Content Page\n- Arizona Divorce Mediation Guide (Divorce Mediation - Featured H3 Card)",
    "URL: /divorce-mediation/arizona-divorce-mediation-guide/ (new build)\n"
    "- Resource / Tool Brief, 1,000-2,500 words plus checklist. Tier 3, Wave 1, Priority High.\n"
    "- Definitive Arizona-specific walkthrough: process, timing, cost ranges, documentation, filing, and "
    "what happens after agreement.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Court Filing After Mediation in Arizona; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Arizona Divorce Mediation Guides, Checklists, and FAQs "
    "module.\n"
    "Guardrail: include neutral legal-information-not-advice disclaimers and links to core service pages.",
    "The most citable asset in the cluster and the page most likely to be pulled into AI overviews for broad "
    "Arizona divorce mediation questions, because comprehensive state-specific guides are what those systems "
    "prefer to summarize. It also functions as the primary link target for guest posts and niche edits, "
    "concentrating acquired authority where it can flow to every child page.",
    Beyond=5,
)

add(
    "Core Resource Content Page\n- Questions to Ask a Divorce Mediator (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/questions-to-ask-a-divorce-mediator/ (new build)\n"
    "- Resource / Tool Brief, 1,000-2,500 words plus printable question list. Tier 4, Wave 6, Priority High.\n"
    "- Provide vetting questions covering credentials, neutrality, process, fees, and what happens if talks "
    "stall.\n"
    "- Required return link to Divorce Mediation. Internal links: Is Divorce Mediation Right for Us?; "
    "Pricing; How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Arizona Divorce Mediation Guides, Checklists, and FAQs "
    "module.\n"
    "Guardrail: do not target competitor names unfairly. Consolidate the duplicate alias record into this URL.",
    "Reaches prospects at the provider-selection stage, the last decision before contact, and lets Aurit frame "
    "the evaluation criteria on which it is strongest. Publishing the vetting standard rather than a sales "
    "pitch is a durable trust signal and typically produces above-average assisted conversions.",
    Beyond=5,
)

add(
    "Core FAQ Content Page\n- Divorce Mediation FAQ (Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/divorce-mediation-faq/ (new build)\n"
    "- FAQ Module Brief, 600-1,200 words. Tier 4, Wave 6, Priority Medium.\n"
    "- Consolidate the highest-frequency divorce mediation questions with concise, directly answerable "
    "responses. Apply FAQPage schema.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Arizona Divorce Mediation Guides, Checklists, and FAQs "
    "module.\n"
    "Guardrail: include neutral legal-information-not-advice disclaimers. Do not duplicate answers already "
    "written as on-hub H3/H4 topics.",
    "Concise question-and-answer blocks are the format large language models extract most readily, making this "
    "the cheapest page in the cluster per AI citation earned. Structured FAQ markup also increases SERP real "
    "estate and captures the long tail of conversational queries that never justify their own page.",
    Beyond=3,
)

add(
    "Core Educational Content Page\n- Glossary of Arizona Divorce Mediation Terms "
    "(Divorce Mediation - Supporting Text Link)",
    "URL: /divorce-mediation/glossary-of-arizona-divorce-mediation-terms/ (new build)\n"
    "- Educational / Glossary Brief, 800-1,500 words. Tier 4, Wave 6, Priority Medium.\n"
    "- Define Arizona-specific terminology: legal decision-making, parenting time, community property, "
    "spousal maintenance, consent decree, Rule 67.3, conciliation court.\n"
    "- Required return link to Divorce Mediation. Internal links: Divorce Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: compact descriptive text link in the Arizona Divorce Mediation Guides, Checklists, and FAQs "
    "module.\n"
    "Guardrail: include neutral legal-information-not-advice disclaimers.",
    "Establishes the entity vocabulary that ties the whole site together, giving Google and AI systems explicit "
    "definitions that connect Arizona statutory terms to Aurit's service pages. Glossaries also attract "
    "definitional queries and internal-link opportunities from every page in the account, making this the "
    "highest-density internal linking asset available.",
    Beyond=3,
)

# =============================================================================
# SECTION 2 - CHILD SUPPORT MEDIATION
# 8 URLs (1 hub + 7 linked children) | 12 on-hub topics | 2 held/excluded
# =============================================================================
sep("=== CHILD SUPPORT MEDIATION HUB CLUSTER (8 URLs / 7 child links / 12 on-hub topics / 2 not surfaced) ===")

add(
    "Core Service Hub Page\n- Child Support Mediation (L1 Main Practice Hub - Optimize & Expand)",
    "URL: /child-support-mediation/ (existing page - optimize and expand)\n"
    "- Rebuild the page opening to V4 format: unlinked H1 Child Support Mediation, 2-3 paragraph overview, "
    "trust proof, primary CTA, and an optional jump-link table of contents to the five H2 section IDs.\n"
    "- Target 1,600-2,400 words on the hub itself.\n"
    "- Establish the five approved H2 topic sections on this single URL.\n"
    "- Confirm all 7 approved standalone children carry a required return link to this hub.\n"
    "Owner: SEO Strategist + Legal SME. Guardrail: do not imply the mediator can approve deviations; the "
    "court retains final authority. Requires legal review for all guideline statements.",
    "Establishes the canonical Arizona child support mediation entity and separates it cleanly from the "
    "custody and parenting plan hubs, which currently compete for overlapping parent intent. A structured hub "
    "lets Google distinguish support calculation intent from parenting time intent, and routes the five "
    "distinct question families - calculation, income complexity, added expenses, modification, and unmarried "
    "parents - to the right destination instead of a single generic page.",
    Oct=6,
)

add(
    "Hub Section Module (H2)\n- Arizona Child Support Guidelines, Calculations, and Preparation "
    "(Child Support Hub - On-Page Section, No URL)",
    "Build on /child-support-mediation/. Internal architecture group: Calculation, Guidelines & Preparation.\n"
    "Exact build format:\n"
    "- Unlinked H2: Arizona Child Support Guidelines, Calculations, and Preparation\n"
    "- 1-2 sentence section introduction\n"
    "- 3 featured cards (linked H3 + one sentence each): Child Support Calculation Prep for Mediation; "
    "Using the Arizona Child Support Calculator in Mediation; What Income Counts for Child Support in "
    "Mediation\n"
    "- 2 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Child Support Input Worksheet; Deviating From Child Support Guidelines in Mediation\n"
    "Cross-link to the existing on-site Child Support Calculator (ClickUp 86ba3xx29, Complete).\n"
    "Guardrail: court and guideline authority must be explicit. The mediator helps parties understand inputs "
    "and reach agreement; the mediator does not guarantee court approval.",
    "Calculation intent is the single largest query family in child support and the one users act on first. "
    "Featuring three calculation assets under one H2 turns a passive service page into a tool destination, "
    "and connecting the module to the live calculator captures the engagement and return-visit behavior that "
    "drives local ranking signals in a category where competitors publish only static guideline text.",
    Oct=3,
)

add(
    "Core Process Content Page\n- Child Support Calculation Prep for Mediation "
    "(Child Support Mediation - Featured H3 Card)",
    "URL: /child-support-mediation/child-support-calculation-prep-for-mediation/ (new build)\n"
    "- Process Page Brief, 1,200-2,000 words. Tier 3, Wave 1, Priority High.\n"
    "- Specify the documents, income records, parenting time counts, and expense figures parents should "
    "gather before the session.\n"
    "- Required return link to Child Support Mediation. Internal links: Child Support Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Arizona Child Support Guidelines, Calculations, and "
    "Preparation module.\n"
    "Guardrail: court and guideline authority must be clear; the mediator does not guarantee court approval.",
    "Preparation content shortens sessions and improves outcomes, so it pays for itself in delivery efficiency "
    "as well as rankings. It also targets a query stage where the user has already chosen mediation and is "
    "simply organizing, which produces some of the highest booking rates in the account.",
    Dec=4,
)

add(
    "Core Resource Content Page\n- Using the Arizona Child Support Calculator in Mediation "
    "(Child Support Mediation - Featured H3 Card)",
    "URL: /child-support-mediation/using-the-arizona-child-support-calculator-in-mediation/ (new build)\n"
    "- Resource / Tool Brief, 1,000-2,500 words plus tool integration. Tier 3, Wave 4, Priority High.\n"
    "- Walk through each guideline input, show how parenting time and added expenses change the figure, and "
    "explain why the number is a starting point rather than an outcome.\n"
    "- Integrate with or link directly to the existing on-site Child Support Calculator.\n"
    "- Required return link to Child Support Mediation. Internal links: Child Support Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Arizona Child Support Guidelines, Calculations, and "
    "Preparation module.\n"
    "Guardrail: include appropriate disclaimers; results are estimates, not court determinations.",
    "Calculator-related searches are among the highest-volume non-brand terms in Arizona family law and pull "
    "users who are actively quantifying a decision. Pairing the tool with an explanation page converts "
    "calculator traffic that would otherwise bounce, and the interaction time it generates is a strong "
    "engagement signal for the whole hub.",
    Beyond=5,
)

add(
    "Core Educational Content Page\n- What Income Counts for Child Support in Mediation "
    "(Child Support Mediation - Featured H3 Card)",
    "URL: /child-support-mediation/what-income-counts-for-child-support-in-mediation/ (new build)\n"
    "- Educational / Glossary Brief, 800-1,500 words. Tier 4, Wave 4, Priority Medium.\n"
    "- Define gross income under the Arizona guidelines, including bonuses, overtime, self-employment "
    "earnings, benefits, and non-cash compensation.\n"
    "- Required return link to Child Support Mediation. Internal links: Child Support Mediation; "
    "Self-Employed Income and Child Support Mediation; Pricing; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Arizona Child Support Guidelines, Calculations, and "
    "Preparation module.\n"
    "Guardrail: court and guideline authority must be clear; the mediator does not determine income.",
    "Income definition is the most disputed input in every support negotiation and the question parents "
    "research most before a session. Clear definitional content is precisely what AI systems retrieve for "
    "what counts as income queries, and it defuses the argument that most often stalls mediation.",
    Beyond=3,
)

add(
    "Hub Section Module (H2)\n- Child Support Mediation for Complex Income and Employment "
    "(Child Support Hub - On-Page Section, No URL)",
    "Build on /child-support-mediation/. Internal architecture group: Income & Employment Complexity.\n"
    "Exact build format:\n"
    "- Unlinked H2: Child Support Mediation for Complex Income and Employment\n"
    "- 1-2 sentence section introduction\n"
    "- 2 featured cards (linked H3 + one sentence): Self-Employed Income and Child Support Mediation; "
    "High-Income Child Support Mediation\n"
    "- 4 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Variable Income Child Support Mediation; Child Support for Unemployed or Underemployed Parent; "
    "Child Support After Job Loss Mediation; Imputed Income in Child Support Mediation\n"
    "Guardrail: court and guideline authority must be clear; the mediator helps parties understand inputs and "
    "reach agreement, not guarantee court approval.",
    "Income complexity is where guideline calculators fail and where a neutral adds the most value, so this "
    "module carries the strongest commercial argument on the hub. Google isolates variable and self-employment "
    "income as a distinct cluster because the calculation logic differs, and four on-hub scenarios let Aurit "
    "cover that cluster comprehensively without publishing four thin pages.",
    Oct=4,
)

add(
    "Core Situational Content Page\n- Self-Employed Income and Child Support Mediation "
    "(Child Support Mediation - Featured H3 Card)",
    "URL: /child-support-mediation/self-employed-income-and-child-support-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Cover business income versus personal draw, add-backs, depreciation, documentation both parents can "
    "accept, and when a neutral financial professional helps.\n"
    "- Required return link to Child Support Mediation. Internal links: Child Support Mediation; "
    "What Income Counts for Child Support in Mediation; Business Owner Divorce Mediation; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Support Mediation for Complex Income and Employment "
    "module.\n"
    "Guardrail: court and guideline authority must be clear; recommend independent financial review.",
    "Self-employed parents represent the highest-conflict and highest-fee support matters, and they are the "
    "segment most poorly served by generic calculator content. Owning this query connects the child support "
    "cluster to the business owner and property division clusters, creating a cross-hub path toward the "
    "account's most valuable matters.",
    Beyond=4,
)

add(
    "Core Situational Content Page\n- High-Income Child Support Mediation "
    "(Child Support Mediation - Featured H3 Card)",
    "URL: /child-support-mediation/high-income-child-support-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 4, Priority Medium.\n"
    "- Explain what happens above the guideline schedule cap, how parents structure agreements for children's "
    "actual needs, and how privacy is maintained.\n"
    "- Required return link to Child Support Mediation. Internal links: Child Support Mediation; "
    "High-Asset Divorce Mediation; High-Income Spousal Maintenance Mediation; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Support Mediation for Complex Income and Employment "
    "module.\n"
    "Guardrail: court and guideline authority must be clear; avoid figure-specific outcome projections.",
    "Above-cap support is a genuinely under-served query in Arizona and attracts the highest-value parent "
    "profile in the cluster. It also links the support hub to the high-asset divorce and high-income "
    "maintenance pages, reinforcing a premium-segment cluster that AI systems can surface as a coherent "
    "specialty.",
    Beyond=4,
)

add(
    "Hub Section Module (H2)\n- Childcare, Medical, and Other Child Expense Mediation "
    "(Child Support Hub - On-Page Section, No URL)",
    "Build on /child-support-mediation/. Internal architecture group: Additional Child Expenses.\n"
    "Exact build format:\n"
    "- Unlinked H2: Childcare, Medical, and Other Child Expense Mediation\n"
    "- 1-2 sentence section introduction\n"
    "- No featured cards and no text links in this module - it is a content-only section.\n"
    "- 3 section-first topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Medical Insurance and Child Support Mediation; Daycare and Childcare Expense Mediation; "
    "Extracurricular and Unreimbursed Expense Mediation\n"
    "Do not create child URLs for these topics. Promote only if demand and depth later justify a page.\n"
    "Guardrail: court and guideline authority must be clear; the mediator does not determine allocation.",
    "Add-on expenses are the most frequent source of post-decree conflict and therefore a reliable driver of "
    "repeat engagements, but individually the queries are too small to justify separate URLs. Concentrating "
    "all three on the parent page builds the hub's word count and semantic breadth while keeping authority "
    "consolidated, and it feeds the post-decree cluster with qualified internal traffic.",
    Oct=3,
)

add(
    "Hub Section Module (H2)\n- Child Support Modifications, Arrears, and Enforcement "
    "(Child Support Hub - On-Page Section, No URL)",
    "Build on /child-support-mediation/. Internal architecture group: Changes, Arrears & Enforcement.\n"
    "Exact build format:\n"
    "- Unlinked H2: Child Support Modifications, Arrears, and Enforcement\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): Child Support Modification Mediation\n"
    "- 3 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Child Support Review and Adjustment Mediation; Child Support Arrears Discussion in Mediation; "
    "When Child Support Ends in Arizona\n"
    "Do not surface Child Support Enforcement and Mediation (governance: do not build). Enforcement and "
    "contempt are court-action intent - route to post-decree information and legal resources instead.\n"
    "Guardrail: mediation can help parties discuss changes, but modifications require proper filing and "
    "court approval.",
    "Modification intent is recurring revenue: the same family returns every time income or parenting time "
    "changes. Separating discussable modification topics from enforcement, which mediation cannot deliver, "
    "protects the firm from mismatched expectations and keeps Google from associating Aurit with enforcement "
    "queries it cannot serve - a mismatch that damages both conversion rate and topical precision.",
    Oct=3,
)

add(
    "Core Process Content Page\n- Child Support Modification Mediation (Child Support Mediation - Featured H3 Card)",
    "URL: /child-support-mediation/child-support-modification-mediation/\n"
    "ALREADY IN PRODUCTION - ClickUp 86bb2fggu, In-Progress, 4 hours allocated in July. No additional build "
    "hours requested here; this row exists so the cluster reconciles.\n"
    "On publish, confirm V4 placement:\n"
    "- Required return link to Child Support Mediation, plus Post-Decree Mediation.\n"
    "- Featured linked H3 card in the Child Support Modifications, Arrears, and Enforcement module.\n"
    "- Verify the substantial-and-continuing-change framing and that court approval language is present.",
    "Already funded in July. Listed here to confirm hub placement, because a published page that is not "
    "featured on its hub receives none of the internal authority the cluster is designed to distribute.",
    status="In-Progress", cu="https://rocketclicks.clickup.com/t/9014341759/86bb2fggu",
)

add(
    "Hub Section Module (H2)\n- Child Support Mediation for Unmarried Parents "
    "(Child Support Hub - On-Page Section, No URL)",
    "Build on /child-support-mediation/. Internal architecture group: Support for Unmarried Parents.\n"
    "Exact build format:\n"
    "- Unlinked H2: Child Support Mediation for Unmarried Parents\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): Child Support for Unmarried Parents Mediation\n"
    "- No section-first or FAQ topics in this module.\n"
    "Do not surface the duplicate record Child Support Mediation for Unmarried Parents "
    "(governance: consolidate into /child-support-mediation/child-support-for-unmarried-parents-mediation/).\n"
    "Cross-link to Mediation for Unmarried Parents on the Parenting Plan hub so parentage intent routes there.",
    "Unmarried-parent support is procedurally distinct because parentage must be settled first, and Google "
    "treats it as a separate cluster. A single canonical page with the near-duplicate alias suppressed prevents "
    "the two records from splitting the same small query family, and cross-linking to the parenting plan hub "
    "captures the full unmarried-parent journey rather than one slice of it.",
    Oct=2,
)

add(
    "Core Situational Content Page\n- Child Support for Unmarried Parents Mediation "
    "(Child Support Mediation - Featured H3 Card)",
    "URL: /child-support-mediation/child-support-for-unmarried-parents-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain how parentage, parenting time, and shared expenses interact for never-married parents and what "
    "must be established before support can be agreed.\n"
    "- Required return link to Child Support Mediation. Internal links: Mediation for Unmarried Parents; "
    "Parenting Plan Mediation; Pricing; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Support Mediation for Unmarried Parents module.\n"
    "Guardrail: do not imply the mediator establishes legal parentage. Court and guideline authority must "
    "be clear.\n"
    "Dedupe: this is the canonical URL. Retire the duplicate alias record.",
    "Unmarried parents represent a substantial share of Arizona births and are almost entirely unserved by "
    "mediation marketing, which is oriented to divorce. Owning this entry point opens a demand pool with no "
    "meaningful "
    "competition and routes families into the parenting plan and custody clusters where lifetime value is "
    "highest.",
    Beyond=4,
)

# =============================================================================
# SECTION 3 - CHILD CUSTODY MEDIATION
# 8 URLs (1 hub + 7 linked children) | 8 on-hub topics | 3 held/excluded
# =============================================================================
sep("=== CHILD CUSTODY MEDIATION HUB CLUSTER (8 URLs / 7 child links / 8 on-hub topics / 3 not surfaced) ===")

add(
    "Core Service Hub Page\n- Child Custody Mediation (L1 Main Practice Hub - Optimize & Expand)",
    "URL: /child-custody-mediation/ (existing page - optimize and expand)\n"
    "- Rebuild the page opening to V4 format: unlinked H1 Child Custody Mediation, 2-3 paragraph overview, "
    "trust proof, primary CTA, and an optional jump-link table of contents to the six H2 section IDs.\n"
    "- Target 1,800-2,600 words on the hub itself.\n"
    "- Establish the six approved H2 topic sections on this single URL.\n"
    "- Confirm all 7 approved standalone children carry a required return link to this hub.\n"
    "Dependency: coordinate scope with the Parenting Plan Mediation hub to avoid cannibalization - custody "
    "owns decision-making authority and legal framework; parenting plan owns schedules and logistics.\n"
    "Owner: SEO Strategist + Legal SME. Guardrail: avoid promising custody outcomes; preserve child-centered "
    "neutrality; use Arizona terminology (legal decision-making and parenting time, not custody and "
    "visitation) consistently.",
    "Child custody is the highest-volume family-law query family in Arizona and the term most at risk of "
    "cannibalization across the custody, parenting plan, and divorce hubs. A single well-scoped hub using "
    "correct Arizona terminology tells Google which page owns the term, resolves that overlap, and lets the "
    "site rank for the colloquial custody phrasing users search while remaining accurate to the statutory "
    "language the courts and AI systems reference.",
    Nov=6,
)

add(
    "Hub Section Module (H2)\n- Child Custody, Legal Decision-Making, and Your Child's Best Interests "
    "(Child Custody Hub - On-Page Section, No URL)",
    "Build on /child-custody-mediation/. Internal architecture group: Decision-Making & Best Interests.\n"
    "Exact build format:\n"
    "- Unlinked H2: Child Custody, Legal Decision-Making, and Your Child's Best Interests\n"
    "- 1-2 sentence section introduction\n"
    "- 3 featured cards (linked H3 + one sentence each): Legal Decision-Making Mediation; "
    "Legal Decision-Making vs Parenting Time; Best Interests of the Child in Mediation\n"
    "- 1 section-first topic written on the hub as unlinked H3/H4 content, 150-450 words: "
    "Decision-Making for School and Medical Issues\n"
    "Guardrail: avoid promising custody outcomes; preserve child-centered neutrality.",
    "This module carries the statutory vocabulary bridge that the entire custody cluster depends on. Mapping "
    "the colloquial term custody onto Arizona's legal decision-making and parenting time framework is exactly "
    "the disambiguation Google and AI systems need to classify the page correctly, and best-interest content "
    "is the most frequently cited framework in custody answers.",
    Nov=2,
)

add(
    "Core Process Content Page\n- Legal Decision-Making Mediation (Child Custody Mediation - Featured H3 Card)",
    "URL: /child-custody-mediation/legal-decision-making-mediation/ (new build)\n"
    "- Process Page Brief, 1,200-2,000 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain joint versus sole legal decision-making, how final say can be allocated by category, and how "
    "parents build a workable decision protocol.\n"
    "- Required return link to Child Custody Mediation. Internal links: Child Custody Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Custody, Legal Decision-Making, and Your Child's Best "
    "Interests module.\n"
    "Guardrail: avoid promising outcomes; preserve child-centered neutrality.",
    "Legal decision-making is Arizona's actual statutory term and the phrase courts, attorneys, and AI systems "
    "use, yet almost no mediation site targets it directly. Owning the exact statutory language positions "
    "Aurit as the jurisdictionally precise source, which is the strongest differentiator available in a "
    "crowded custody SERP.",
    Jan=4,
)

add(
    "Core Educational Content Page\n- Legal Decision-Making vs Parenting Time "
    "(Child Custody Mediation - Featured H3 Card)",
    "URL: /child-custody-mediation/legal-decision-making-vs-parenting-time/ (new build)\n"
    "- Educational / Glossary Brief, 800-1,500 words. Tier 4, Wave 4, Priority Medium.\n"
    "- Draw the distinction clearly, show how each is decided separately, and correct the assumption that "
    "one determines the other.\n"
    "- Required return link to Child Custody Mediation. Internal links: Child Custody Mediation; "
    "Parenting Time Schedule Mediation; Pricing; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Custody, Legal Decision-Making, and Your Child's Best "
    "Interests module.\n"
    "Guardrail: avoid promising outcomes.",
    "Corrects the most common misconception in Arizona custody and answers a comparison question with clear "
    "search demand. Definitional comparison content is heavily favored in AI retrieval because it resolves "
    "ambiguity in a single passage, and it doubles as the internal-linking hinge between the custody and "
    "parenting plan hubs.",
    Beyond=3,
)

add(
    "Core Educational Content Page\n- Best Interests of the Child in Mediation "
    "(Child Custody Mediation - Featured H3 Card)",
    "URL: /child-custody-mediation/best-interests-of-the-child-in-mediation/ (new build)\n"
    "- Educational / Glossary Brief, 800-1,500 words. Tier 4, Wave 4, Priority Medium.\n"
    "- Walk through the Arizona best-interest factors and how parents apply them to their own decisions in "
    "mediation rather than arguing them to a judge.\n"
    "- Required return link to Child Custody Mediation. Internal links: Child Custody Mediation; Pricing; "
    "How Mediation Works; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Custody, Legal Decision-Making, and Your Child's Best "
    "Interests module.\n"
    "Guardrail: avoid predicting how a court would weigh any factor in a specific case.",
    "The best-interest standard is the legal framework every custody decision is measured against, making this "
    "the most authoritative page in the cluster and a natural citation target. Framing the factors as a "
    "self-application tool rather than courtroom argument also reinforces the mediation positioning while "
    "capturing statutory-research traffic.",
    Beyond=3,
)

add(
    "Hub Section Module (H2)\n- Child Custody Mediation for Co-Parenting and High-Conflict Disputes "
    "(Child Custody Hub - On-Page Section, No URL)",
    "Build on /child-custody-mediation/. Internal architecture group: Co-Parenting, Conflict & Family "
    "Concerns.\n"
    "Exact build format:\n"
    "- Unlinked H2: Child Custody Mediation for Co-Parenting and High-Conflict Disputes\n"
    "- 1-2 sentence section introduction\n"
    "- 3 featured cards (linked H3 + one sentence each): High-Conflict Co-Parenting Mediation; "
    "Co-Parent Communication Mediation; Mediation for Parents Who Disagree\n"
    "- 3 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Custody When a Parent Has Addiction Concerns; Custody When a Parent Has Mental Health Concerns; "
    "Supervised Parenting Time Discussions\n"
    "Guardrail: safety-sensitive. Route addiction, mental health, and supervision topics to suitability and "
    "safety guidance plus emergency and legal resources. Do not imply every high-conflict matter suits "
    "mediation. Avoid clinical claims.",
    "High-conflict co-parenting is where families are actively looking for an alternative to repeat "
    "litigation, which makes it the most motivated audience on the hub. Handling addiction, mental health, "
    "and supervision as guarded on-hub content rather than service pages keeps Aurit clear of claims it "
    "cannot support while still covering searches that would otherwise route entirely to litigation firms.",
    Nov=3,
)

add(
    "Core Situational Content Page\n- High-Conflict Co-Parenting Mediation "
    "(Child Custody Mediation - Featured H3 Card)",
    "URL: /child-custody-mediation/high-conflict-co-parenting-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Cover structured protocols, low-contact arrangements, written communication rules, and how a neutral "
    "reduces escalation points in the plan itself.\n"
    "- Required return link to Child Custody Mediation. Internal links: Co-Parent Communication Mediation; "
    "Parallel Parenting Mediation; When Mediation May Not Be Appropriate; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Custody Mediation for Co-Parenting and High-Conflict "
    "Disputes module.\n"
    "Guardrail: high conflict is not the same as coercion or safety risk. Include suitability limits. "
    "Control overlap with Parallel Parenting Mediation on the Parenting Plan hub.",
    "High-conflict parents generate the most repeat legal spend of any family-law segment, and they search "
    "with urgency after each incident. Owning this term positions mediation as the exit from a litigation "
    "cycle rather than a soft alternative, which is the framing that converts this audience.",
    Jan=4,
)

add(
    "Core Situational Content Page\n- Co-Parent Communication Mediation "
    "(Child Custody Mediation - Featured H3 Card)",
    "URL: /child-custody-mediation/co-parent-communication-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 4, Wave 4, Priority Medium.\n"
    "- Cover communication protocols, response-time expectations, parenting app selection, tone rules, and "
    "what belongs in writing.\n"
    "- Required return link to Child Custody Mediation. Internal links: High-Conflict Co-Parenting Mediation; "
    "Parenting App and Communication Protocol Mediation; Pricing; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Custody Mediation for Co-Parenting and High-Conflict "
    "Disputes module.\n"
    "Guardrail: preserve neutrality; avoid characterizing either parent's communication style.",
    "Communication breakdown is the trigger event that sends co-parents searching, which makes this a "
    "high-frequency, high-engagement entry point. It also creates a natural service extension into "
    "communication-protocol sessions, generating shorter and more repeatable engagements than full custody "
    "mediation.",
    Beyond=4,
)

add(
    "Core Situational Content Page\n- Mediation for Parents Who Disagree "
    "(Child Custody Mediation - Featured H3 Card)",
    "URL: /child-custody-mediation/mediation-for-parents-who-disagree/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 4, Wave 4, Priority Medium.\n"
    "- Explain how a neutral moves parents from position to interest, sequences issues, and secures partial "
    "agreements when full agreement is not immediately reachable.\n"
    "- Required return link to Child Custody Mediation. Internal links: Child Custody Mediation; "
    "High-Conflict Co-Parenting Mediation; Pricing; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Child Custody Mediation for Co-Parenting and High-Conflict "
    "Disputes module.\n"
    "Guardrail: preserve neutrality; do not imply one parent is the obstacle.",
    "Mirrors the divorce cluster's disagreement page and captures the parenting version of the same "
    "self-disqualifying doubt. Plain-language phrasing matches how parents actually search - and how they "
    "phrase questions to AI assistants - rather than the service vocabulary competitors optimize for.",
    Beyond=4,
)

add(
    "Hub Section Module (H2)\n- Relocation and Changes to Existing Child Custody Orders "
    "(Child Custody Hub - On-Page Section, No URL)",
    "Build on /child-custody-mediation/. Internal architecture group: Relocation & Existing Orders.\n"
    "Exact build format:\n"
    "- Unlinked H2: Relocation and Changes to Existing Child Custody Orders\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): Relocation Discussions in Mediation\n"
    "- 1 section-first topic written on the hub as unlinked H3/H4 content, 150-450 words: "
    "Custody Mediation After Temporary Orders\n"
    "Cross-link to Relocation After Divorce Mediation on the Post-Decree hub so pre-decree and post-decree "
    "relocation intent stay separated.\n"
    "Guardrail: preserve legal guardrails around notice requirements and court approval for relocation.",
    "Relocation is a high-urgency, statutorily governed event with strict notice timelines, so searchers act "
    "immediately. Google treats parenting mobility as a cluster separate from standard custody, and keeping "
    "the pre-decree and post-decree relocation pages distinctly scoped lets Aurit hold both without either "
    "page diluting the other.",
    Nov=2,
)

add(
    "Live Page V4 Retrofit\n- Relocation Discussions in Mediation (Child Custody Mediation - Featured H3 Card)",
    "URL: /child-custody-mediation/relocation-discussions-in-mediation/ - a Relocation / Move-Away Mediation "
    "page is already published (ClickUp 86b9332hv, marked Complete). Retrofit only, no new draft:\n"
    "- Confirm the live URL and align it to the approved path, redirecting if the slug differs.\n"
    "- Add or verify the required return link to the Child Custody Mediation hub.\n"
    "- Add or verify internal links to Custody Mediation After Temporary Orders and Relocation After Divorce "
    "Mediation.\n"
    "- Verify Arizona relocation statute references, notice requirements, and best-interest framing are "
    "current.\n"
    "- Place as the featured linked H3 card in the Relocation and Changes to Existing Child Custody Orders "
    "module.",
    "Brings an existing high-intent asset into the hub structure so it finally receives internal authority. "
    "Verifying the statutory notice references also protects accuracy on the one custody topic where an "
    "out-of-date timeline could cause real harm to a reader and real reputational damage to the firm.",
    Nov=1,
)

add(
    "Hub Section Module (H2)\n- Grandparent and Extended-Family Custody Mediation "
    "(Child Custody Hub - On-Page Section, No URL)",
    "Build on /child-custody-mediation/. Internal architecture group: Grandparents & Extended Family.\n"
    "Exact build format:\n"
    "- Unlinked H2: Grandparent and Extended-Family Custody Mediation\n"
    "- 1-2 sentence section introduction\n"
    "- No featured cards and no text links in this module - it is a content-only section.\n"
    "- 2 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Grandparents' Rights Mediation; Grandparent Visitation Discussion in Mediation\n"
    "Do not create child URLs for these topics.\n"
    "SCOPE CHANGE: the existing strategy row Core Situational Content Page - Grandparent Rights Mediation "
    "(4 hours, August) is a standalone page. V4 architecture demotes it to on-hub content. Reallocate those "
    "hours or confirm an exception before building a separate URL.\n"
    "Guardrail: explain the limited circumstances in which mediation may support family discussions; make "
    "clear that third-party legal rights require independent advice. Avoid implying representation.",
    "Third-party visitation is a genuinely under-served Arizona cluster, but the query volume does not support "
    "a standalone page and the legal-rights exposure is high. On-hub treatment captures the semantic coverage "
    "and the occasional high-intent visitor while keeping the firm out of a rights-advocacy position it "
    "cannot occupy as a neutral.",
    Nov=3,
)

add(
    "Hub Section Module (H2)\n- Arizona Child Custody Mediation FAQs and Resources "
    "(Child Custody Hub - On-Page Section, No URL)",
    "Build on /child-custody-mediation/. Internal architecture group: FAQs & Supporting Education.\n"
    "Exact build format:\n"
    "- Unlinked H2: Arizona Child Custody Mediation FAQs and Resources\n"
    "- 1-2 sentence section introduction\n"
    "- No featured cards and no text links in this module.\n"
    "- 1 section-first topic written on the hub as unlinked H3/H4 content: Child Custody Mediation FAQ, "
    "600-1,200 words with FAQPage schema applied to the parent page.\n"
    "Promote to /child-custody-mediation/child-custody-mediation-faq/ only if demand and depth validate it.\n"
    "Guardrail: keep answers concise; link only to approved pages with distinct search intent.",
    "Keeping the custody FAQ on the parent page rather than as a separate URL concentrates schema-eligible "
    "question-and-answer content on the hub itself, which is where the ranking authority already sits. That "
    "gives the hub the conversational coverage AI systems extract from while avoiding a thin FAQ page that "
    "would compete with its own parent.",
    Nov=2,
)

add(
    "Hub Section Module (H2)\n- Emergency Child Custody and Safety Considerations "
    "(Child Custody Hub - On-Page Section, No URL)",
    "Build on /child-custody-mediation/. Internal architecture group: Safety & Emergency Guardrails.\n"
    "Exact build format:\n"
    "- Unlinked H2: Emergency Child Custody and Safety Considerations\n"
    "- 1-2 sentence section introduction\n"
    "- Content section only. No featured cards, no text links, no section-first topics.\n"
    "- State plainly that mediation is not a substitute for emergency court relief or immediate safety "
    "planning, and surface approved emergency, court, and legal resources.\n"
    "Do not surface Custody Mediation and Domestic Violence Concerns, Emergency Custody and Mediation, or "
    "Emergency Parenting Orders Mediation (governance: do not build).\n"
    "CONFLICT TO RESOLVE: the existing strategy backlog contains Core Situational Content Page - Emergency "
    "Custody Mediation (Child Custody - Situational Page). V4 architecture classifies this as Do Not Build. "
    "Retire that backlog row.\n"
    "Guardrail: mandatory legal review. Route urgent matters to emergency help and court resources.",
    "Emergency custody searchers are in crisis and mediation cannot serve them, so ranking for those terms "
    "would generate unservable inquiries and real risk. An explicit guardrail section converts an unservable "
    "query into a trust signal: search and AI systems reward YMYL pages that redirect users to appropriate "
    "help, and it protects the firm from the reputational exposure of appearing to market mediation as an "
    "emergency remedy.",
    Nov=2,
)

# =============================================================================
# SECTION 4 - SPOUSAL MAINTENANCE MEDIATION
# 10 URLs (1 hub + 9 linked children) | 11 on-hub topics | 0 held/excluded
# =============================================================================
sep("=== SPOUSAL MAINTENANCE MEDIATION HUB CLUSTER (10 URLs / 9 child links / 11 on-hub topics / 0 not surfaced) ===")

add(
    "Core Service Hub Page\n- Spousal Maintenance Mediation (L1 Main Practice Hub - Optimize & Expand)",
    "URL: /spousal-support-alimony-mediation/ (existing page - optimize and expand)\n"
    "- Rebuild the page opening to V4 format: unlinked H1 Spousal Maintenance Mediation, 2-3 paragraph "
    "overview, trust proof, primary CTA, and an optional jump-link table of contents to the four H2 "
    "section IDs.\n"
    "- Target 1,600-2,400 words on the hub itself.\n"
    "- Establish the four approved H2 topic sections on this single URL.\n"
    "- Confirm all 9 approved standalone children carry a required return link to this hub.\n"
    "- Use Arizona terminology consistently: spousal maintenance is the statutory term; alimony and spousal "
    "support are the colloquial variants the URL already captures. Do not create separate alimony URLs.\n"
    "Owner: SEO Strategist + Legal SME. Guardrail: avoid outcome promises and one-sided support-position "
    "language; the mediator provides legal information, not individual advice.",
    "Spousal maintenance is the most emotionally and financially charged issue in an Arizona divorce and the "
    "one where both spouses search independently, doubling the effective audience per matter. Consolidating "
    "alimony, spousal support, and spousal maintenance intent on one hub captures all three phrasings without "
    "duplicate URLs, and the existing on-site Alimony Calculator gives this cluster an engagement asset no "
    "local competitor matches.",
    Nov=6,
)

add(
    "Hub Section Module (H2)\n- Types and Duration of Spousal Maintenance in Arizona "
    "(Spousal Maintenance Hub - On-Page Section, No URL)",
    "Build on /spousal-support-alimony-mediation/. Internal architecture group: Types, Duration & Guidelines.\n"
    "Exact build format:\n"
    "- Unlinked H2: Types and Duration of Spousal Maintenance in Arizona\n"
    "- 1-2 sentence section introduction\n"
    "- 3 featured cards (linked H3 + one sentence each): Temporary Spousal Maintenance Mediation; "
    "Long-Term Spousal Maintenance Mediation; Spousal Maintenance for Long-Term Marriage\n"
    "- 4 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Arizona Spousal Maintenance Guidelines in Mediation; Short-Term Marriage Maintenance Mediation; "
    "Rehabilitative Spousal Maintenance Mediation; Lump-Sum Spousal Maintenance in Mediation\n"
    "Arizona's spousal maintenance guidelines were adopted recently and materially changed how amount and "
    "duration ranges are derived. Verify the current version and effective date with the Legal SME before "
    "drafting, and schedule an annual accuracy review.\n"
    "Guardrail: distinguish legal information from advice; use neutral language for both spouses.",
    "Duration is the first question both spouses ask and the input that determines the total value of any "
    "settlement, making this the highest-stakes section on the hub. Arizona's guideline framework is recent "
    "enough that most competing content is out of date, so accurate, current duration content is an "
    "immediately winnable authority advantage with both Google and AI systems that weight recency on "
    "statutory topics.",
    Nov=4,
)

add(
    "Core Process Content Page\n- Temporary Spousal Maintenance Mediation "
    "(Spousal Maintenance Mediation - Featured H3 Card)",
    "URL: /spousal-support-alimony-mediation/temporary-spousal-maintenance-mediation/ (new build)\n"
    "- Process Page Brief, 1,200-2,000 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain interim support during the divorce transition, how parties structure it, and how it relates to "
    "the final award.\n"
    "- Required return link to Spousal Maintenance Mediation. Internal links: Spousal Maintenance Mediation; "
    "Pricing; How Mediation Works; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Types and Duration of Spousal Maintenance in Arizona module.\n"
    "Guardrail: neutral language for both spouses; the mediator provides legal information, not individual "
    "advice.\n"
    "Dedupe: supersedes the backlog row Core Situational Content Page - Temporary Maintenance Mediation.",
    "Temporary support is the most urgent maintenance question because it determines whether a spouse can "
    "cover expenses during the process, which drives immediate action rather than research. Capturing that "
    "urgency early in the divorce timeline also means Aurit is engaged before either party retains "
    "litigation counsel.",
    Jan=4,
)

add(
    "Core Process Content Page\n- Long-Term Spousal Maintenance Mediation "
    "(Spousal Maintenance Mediation - Featured H3 Card)",
    "URL: /spousal-support-alimony-mediation/long-term-spousal-maintenance-mediation/ (new build)\n"
    "- Process Page Brief, 1,200-2,000 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain extended-duration arrangements, review and step-down structures, security provisions, and "
    "termination triggers.\n"
    "- Required return link to Spousal Maintenance Mediation. Internal links: Spousal Maintenance for "
    "Long-Term Marriage; Spousal Maintenance Modification Mediation; Pricing; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Types and Duration of Spousal Maintenance in Arizona module.\n"
    "Guardrail: neutral language for both spouses; no outcome promises.\n"
    "Coordinate scope with Spousal Maintenance for Long-Term Marriage: this page owns award structure and "
    "duration mechanics; that page owns the marriage-length circumstance.",
    "Long-duration awards carry the largest total dollar value of any issue Aurit mediates, so the segment "
    "justifies premium engagement fees. Detailed structural content - step-downs, review triggers, security - "
    "demonstrates the drafting sophistication that convinces high-value couples a neutral can handle their "
    "matter without litigation.",
    Beyond=4,
)

add(
    "Core Situational Content Page\n- Spousal Maintenance for Long-Term Marriage "
    "(Spousal Maintenance Mediation - Featured H3 Card)",
    "URL: /spousal-support-alimony-mediation/spousal-maintenance-for-long-term-marriage/\n"
    "ALREADY FUNDED - the existing strategy row Core Situational Content Page - Long-Term Marriage "
    "Maintenance Mediation carries 4 hours in August. No additional build hours requested here; this row "
    "exists so the cluster reconciles.\n"
    "Action: rename the existing row to the approved architecture page name and confirm V4 placement:\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 4.\n"
    "- Required return link to Spousal Maintenance Mediation.\n"
    "- Featured linked H3 card in the Types and Duration of Spousal Maintenance in Arizona module.\n"
    "- Scope to the marriage-length circumstance and the factors that follow from it; leave award structure "
    "to Long-Term Spousal Maintenance Mediation.",
    "Already funded in August. Listed here to lock the naming and hub placement, because the two long-term "
    "maintenance pages will cannibalize each other unless their scopes are explicitly divided and both are "
    "featured under the same H2.",
    cu="",
)

add(
    "Hub Section Module (H2)\n- How Spousal Maintenance Is Calculated: Income and Tax Factors "
    "(Spousal Maintenance Hub - On-Page Section, No URL)",
    "Build on /spousal-support-alimony-mediation/. Internal architecture group: Calculation, Income & Tax.\n"
    "Exact build format:\n"
    "- Unlinked H2: How Spousal Maintenance Is Calculated: Income and Tax Factors\n"
    "- 1-2 sentence section introduction\n"
    "- 3 featured cards (linked H3 + one sentence each): Spousal Maintenance for Self-Employed Spouses; "
    "How Spousal Maintenance Is Calculated in Arizona; High-Income Spousal Maintenance Mediation\n"
    "- 2 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Imputing Income for Spousal Maintenance; Tax Treatment of Spousal Maintenance\n"
    "Cross-link to the existing on-site Alimony Calculator (ClickUp 86ba3xwy8, Complete).\n"
    "Guardrail: distinguish legal information from advice; tax statements require review and should direct "
    "users to a tax professional.",
    "Calculation is the highest-volume maintenance query family and the one the existing Alimony Calculator "
    "already attracts traffic for without a supporting content layer to convert it. Wiring three calculation "
    "pages and the live tool into one module turns that orphaned tool traffic into hub engagement, and "
    "post-2019 tax treatment remains widely misunderstood, leaving an accuracy gap Aurit can own.",
    Dec=3,
)

add(
    "Core Situational Content Page\n- Spousal Maintenance for Self-Employed Spouses "
    "(Spousal Maintenance Mediation - Featured H3 Card)",
    "URL: /spousal-support-alimony-mediation/spousal-maintenance-for-self-employed-spouses/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 1, Priority High.\n"
    "- Cover business income versus draw, add-backs, fluctuating earnings, documentation both spouses accept, "
    "and when a neutral financial expert is warranted.\n"
    "- Required return link to Spousal Maintenance Mediation. Internal links: Spousal Maintenance Mediation; "
    "Business Owner Divorce Mediation; Self-Employed Income and Child Support Mediation; Free Consultation.\n"
    "- Placement: featured linked H3 card in the How Spousal Maintenance Is Calculated: Income and Tax "
    "Factors module.\n"
    "Guardrail: neutral language for both spouses; recommend independent financial review.",
    "Self-employment income is the most contested input in maintenance and the reason these matters otherwise "
    "escalate to competing forensic experts, which is exactly the cost mediation avoids. The page also links "
    "the maintenance cluster to the business owner and child support self-employment pages, forming a "
    "recognizable business-owner specialty across three hubs.",
    Beyond=4,
)

add(
    "Core Educational Content Page\n- How Spousal Maintenance Is Calculated in Arizona "
    "(Spousal Maintenance Mediation - Featured H3 Card)",
    "URL: /spousal-support-alimony-mediation/how-spousal-maintenance-is-calculated-in-arizona/ (new build)\n"
    "- Educational / Glossary Brief, 800-1,500 words. Tier 3, Wave 4, Priority High.\n"
    "- Walk through eligibility, the statutory factors, and how the current Arizona guidelines produce amount "
    "and duration ranges.\n"
    "- Link to the on-site Alimony Calculator.\n"
    "- Required return link to Spousal Maintenance Mediation. Internal links: Spousal Maintenance Mediation; "
    "Arizona Spousal Maintenance Guidelines in Mediation; Pricing; Free Consultation.\n"
    "- Placement: featured linked H3 card in the How Spousal Maintenance Is Calculated: Income and Tax "
    "Factors module.\n"
    "Guardrail: no individualized estimates; results are ranges, not court determinations. Schedule an annual "
    "guideline accuracy review.",
    "The highest-volume informational query in the maintenance cluster and the natural landing page for "
    "alimony calculator traffic. Because the Arizona guidelines are recent, most competing pages are "
    "outdated - and recency is weighted heavily by both Google and AI systems on statutory topics, making "
    "accurate calculation content an unusually fast ranking win.",
    Beyond=3,
)

add(
    "Core Situational Content Page\n- High-Income Spousal Maintenance Mediation "
    "(Spousal Maintenance Mediation - Featured H3 Card)",
    "URL: /spousal-support-alimony-mediation/high-income-spousal-maintenance-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 4, Priority Medium.\n"
    "- Cover complex compensation, equity and deferred pay, lifestyle analysis, privacy, and structured "
    "buyout alternatives to ongoing payments.\n"
    "- Required return link to Spousal Maintenance Mediation. Internal links: High-Asset Divorce Mediation; "
    "Stock Options and RSUs in Divorce Mediation; Lump-Sum Spousal Maintenance in Mediation; "
    "Free Consultation.\n"
    "- Placement: featured linked H3 card in the How Spousal Maintenance Is Calculated: Income and Tax "
    "Factors module.\n"
    "Guardrail: neutral language for both spouses; recommend independent financial and tax review.",
    "The highest revenue-per-matter page in the maintenance cluster, aimed at couples for whom privacy alone "
    "justifies mediation over public litigation. It completes a premium cross-hub cluster with high-asset "
    "divorce, high-income child support, and equity compensation, which is the specialty positioning most "
    "likely to be surfaced for complex-finance family-law queries.",
    Beyond=4,
)

add(
    "Hub Section Module (H2)\n- Spousal Maintenance for Different Marriage and Life Circumstances "
    "(Spousal Maintenance Hub - On-Page Section, No URL)",
    "Build on /spousal-support-alimony-mediation/. Internal architecture group: Marriage & Life "
    "Circumstances.\n"
    "Exact build format:\n"
    "- Unlinked H2: Spousal Maintenance for Different Marriage and Life Circumstances\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): Stay-at-Home Spouse Divorce Mediation\n"
    "- 1 supporting descriptive text link: Spousal Maintenance After Retirement\n"
    "- 2 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Spousal Maintenance vs Child Support; Can a Prenup Waive Spousal Maintenance?\n"
    "Guardrail: neutral language for both spouses; do not imply a predetermined legal outcome for any "
    "circumstance. Prenup content must not advise on enforceability.",
    "Life-circumstance queries convert well because searchers describe their own situation rather than a "
    "service, so the match feels personal. Keeping the maintenance-versus-child-support distinction on the "
    "hub also resolves a persistent confusion that otherwise sends users to the wrong page entirely, "
    "protecting conversion across two clusters at once.",
    Dec=3,
)

add(
    "Core Situational Content Page\n- Stay-at-Home Spouse Divorce Mediation "
    "(Spousal Maintenance Mediation - Featured H3 Card)",
    "URL: /spousal-support-alimony-mediation/stay-at-home-spouse-divorce-mediation/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 4, Wave 4, Priority High.\n"
    "- Cover career-sacrifice contribution, re-entry and earning capacity, transitional support planning, "
    "health coverage, and access to financial information.\n"
    "- Required return link to Spousal Maintenance Mediation. Internal links: Spousal Maintenance Mediation; "
    "Financial Disclosure in Divorce Mediation; Rehabilitative Spousal Maintenance Mediation; "
    "Free Consultation.\n"
    "- Placement: featured linked H3 card in the Spousal Maintenance for Different Marriage and Life "
    "Circumstances module.\n"
    "Guardrail: neutral language for both spouses - the page must not read as advocacy for the "
    "lower-earning spouse.",
    "Reaches the most anxious and most search-active party in a maintenance matter, typically months before "
    "either spouse files. High-empathy situational content converts strongly at this stage, and because both "
    "spouses must agree to mediate, earning the trust of the more hesitant party is what actually gets the "
    "engagement signed.",
    Beyond=4,
)

add(
    "Core Situational Content Page\n- Spousal Maintenance After Retirement "
    "(Spousal Maintenance Mediation - Supporting Text Link)",
    "URL: /spousal-support-alimony-mediation/spousal-maintenance-after-retirement/ (new build)\n"
    "- Situation / Use-Case Brief, 1,100-1,900 words. Tier 3, Wave 4, Priority Medium.\n"
    "- Cover good-faith retirement as a change in circumstances, fixed-income realities, and how existing "
    "obligations are revisited.\n"
    "- Required return link to Spousal Maintenance Mediation. Internal links: Spousal Maintenance "
    "Modification Mediation; Gray Divorce Mediation; Retirement Account Division Mediation; "
    "Free Consultation.\n"
    "- Placement: compact descriptive text link in the Spousal Maintenance for Different Marriage and Life "
    "Circumstances module.\n"
    "Guardrail: neutral language for both spouses; mediation can address the discussion, but modification "
    "requires proper filing and court approval.",
    "Serves both pre-decree planning for near-retirement couples and post-decree modification demand, so a "
    "single page earns from two distinct query families. It is also the strongest connective asset between "
    "the maintenance, gray divorce, and retirement-asset clusters, which is where Aurit's most affluent "
    "segment sits.",
    Beyond=4,
)

add(
    "Hub Section Module (H2)\n- Modifying, Reviewing, or Ending Spousal Maintenance "
    "(Spousal Maintenance Hub - On-Page Section, No URL)",
    "Build on /spousal-support-alimony-mediation/. Internal architecture group: Modification, Review & "
    "Termination.\n"
    "Exact build format:\n"
    "- Unlinked H2: Modifying, Reviewing, or Ending Spousal Maintenance\n"
    "- 1-2 sentence section introduction\n"
    "- 1 featured card (linked H3 + one sentence): Spousal Maintenance Modification Mediation\n"
    "- 3 section-first / FAQ topics written on the hub as unlinked H3/H4 content, 150-450 words each: "
    "Spousal Maintenance Termination or Reduction Mediation; Spousal Maintenance and Cohabitation "
    "Discussions; Spousal Maintenance Review After Divorce\n"
    "Cross-link to the Post-Decree Mediation hub.\n"
    "Guardrail: mediation can help parties discuss changes, but modification requires proper filing and court "
    "approval. Do not interpret non-modifiable award language for either party.",
    "Modification demand recurs for years after the original matter closes, making this the most efficient "
    "repeat-revenue section in the cluster. Cohabitation and termination questions in particular are searched "
    "with intensity and served almost entirely by litigation firms, so a neutral, non-adversarial answer is "
    "both differentiated and far cheaper to rank for.",
    Dec=3,
)

add(
    "Core Process Content Page\n- Spousal Maintenance Modification Mediation "
    "(Spousal Maintenance Mediation - Featured H3 Card)",
    "URL: /spousal-support-alimony-mediation/spousal-maintenance-modification-mediation/ (new build)\n"
    "- Process Page Brief, 1,200-2,000 words. Tier 3, Wave 1, Priority High.\n"
    "- Explain what qualifies as a substantial and continuing change, how parties document it, how a revised "
    "agreement is drafted, and how it reaches the court.\n"
    "- Required return link to Spousal Maintenance Mediation. Internal links: Post-Decree Mediation; "
    "Spousal Maintenance After Retirement; Pricing; How Mediation Works; Free Consultation.\n"
    "- Placement: featured linked H3 card in the Modifying, Reviewing, or Ending Spousal Maintenance module.\n"
    "Guardrail: mediation can help parties discuss changes, but modification requires proper filing and court "
    "approval. Neutral language for both spouses.",
    "Modification is a shorter, lower-cost engagement that reactivates past clients and reaches former "
    "litigants who never worked with Aurit but want to avoid returning to court. That makes it one of the "
    "few pages in the account that serves both retention and acquisition, and it anchors the maintenance "
    "cluster into the post-decree hub.",
    Beyond=4,
)

# =============================================================================
# WRITE
# =============================================================================
OUT = os.path.expanduser(
    "~/SEO_Dept/analysis/Aurit_2026_Strategy_Buildout_Divorce_ChildSupport_ChildCustody_SpousalMaintenance.csv"
)
with open(OUT, "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADER)
    for r in rows:
        w.writerow(r)

# ---- self-check -------------------------------------------------------------
data = [r for r in rows if r[3]]  # skip separator rows
tot = {m: 0.0 for m in MONTHS}
for r in rows:
    for i, m in enumerate(MONTHS):
        v = r[5 + i]
        if v:
            tot[m] += float(v)
print(f"Wrote {OUT}")
print(f"Rows written (incl. 4 separators): {len(rows)}   deliverable rows: {len(data)}")
print("New hours by month:", {k: round(v, 1) for k, v in tot.items()})
print("New hours total:", round(sum(tot.values()), 1))
existing = {"July": 53.5, "Aug": 44.5, "Sep": 19, "Oct": 26, "Nov": 20, "Dec": 20, "Jan": 20, "Beyond": 0}
print("Combined plan by month:", {m: round(existing[m] + tot[m], 1) for m in MONTHS})
