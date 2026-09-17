# External Correction Record: Fanash Hub Destination Screen

**Date:** 2026-09-16  
**Classification:** External correction requested after the original strategist and reviewer work  
**Corrected artifact:** `../destination-screen.md`  
**Preserved prior review:** `destination-screen-seo-reviewer-raw.txt`  
**Correction review:** `destination-screen-external-correction-seo-reviewer-raw.txt`

## Scope and outcome

This correction applies the repository's existing blocker-scope rule to the eight exact destinations in the completed Divorce Core Hub manifest. It does not change the Hub DOCX, manifest, supporting record, V2, a destination page, or the live site.

The corrected content-and-technical screen clears four destinations, holds three for a specific material correction, and holds one for a significant unresolved legal-evidence risk. Current intake acceptance remains a separate, route-specific release dependency for the seven service destinations. It is not treated as evidence that those published services are unavailable.

| Route | Before correction | Corrected Hub-link disposition | Page backlog kept separate |
|---|---|---|---|
| Contested Divorce | Needs correction | Cleared within this screen | Verify explicit plural-attorney metadata and judge-insight language. Generic team wording is not treated as a plural-attorney claim. |
| Divorce Mediation | Unresolved | Cleared for the verified counsel route | Confirm neutral-mediator services separately; preserve explicit counsel and preparation language. |
| Legal Separation | Needs correction | Cleared within this screen | Repair malformed copy and substantiate or narrow plural-provider and volume claims. |
| Uncontested Divorce | Needs correction | Hold only this link | Qualify the categorical opening expectation. Repair the dead outbound rules link separately. |
| Annulment | Needs correction | Unresolved; hold only this link | Primary-authority-check central grounds and consequences; substantiate or narrow volume and judge-experience claims. |
| Gray Divorce | Needs correction | Cleared within this screen | Substantiate or narrow experience details. Current generic team language is not an explicit plural-attorney claim. |
| High-Asset Divorce | Needs correction | Hold only this link | Remove or objectively substantiate “one of Orlando's top”; address other unverified claims in the page backlog. |
| Filing for Divorce | Needs correction | Hold only this link | Correct the universal county-venue statement. Confirm SmartStep applicability separately; coexistence with hourly and hybrid options is not a contradiction. |

## Material evidence corrections

- **Mediation:** Current first-party copy explicitly says Fanash may serve as counsel for a mediated divorce or help a client prepare for court-ordered mediation. That matches the Hub's counsel route. Whether Fanash also acts as a neutral remains a distinct client/intake question.
- **Pricing:** Fanash's current [pricing page](https://fanashfamilylaw.com/pricing/) presents SmartStep or flat-fee steps, hourly retainers, and hybrid models as options. Coexistence does not establish a contradiction. The remaining question is which matters qualify for each option.
- **Provider and experience language:** The scoped Florida Bar evidence supports checking explicit “attorneys” or “Lawyers” claims. It does not turn generic “team” wording into an explicit attorney-count claim, and firm size does not disprove professional experience.
- **High-Asset comparison:** Current [Florida Bar Rule 4-7.13(b)(3)](https://www-media.floridabar.org/uploads/2026/06/2026_12-JUNE-RRTFB-6-15-2026.pdf) requires comparisons or characterizations of a lawyer's skill, experience, reputation, or record to be objectively verifiable. The rule's comment explains that “the best” or “one of the best” is impermissible when it cannot be factually substantiated. This supports a hold limited to the High-Asset route's prominent “top” claim; no other High-Asset backlog item independently holds the link.
- **Annulment:** The central grounds and consequences are classified as unverified within this screen, not as demonstrably wrong. Their centrality to eligibility supports a route-specific hold until a primary-authority legal review is completed. Optional V2 status is not an exception.

## Filing-venue resolution

The exact observed sentence is: “Divorce cases are filed in the circuit court of the county where at least one spouse resides.” The circuit-court point is not the problem. The county-residence statement is demonstrably overbroad and incorrect as a universal rule.

Current [Fla. Stat. § 47.011](https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&URL=0000-0099/0047/Sections/0047.011.html) supplies general venue bases, while [§ 61.021](https://www.leg.state.fl.us/Statutes/index.cfm?App_mode=Display_Statute&URL=0000-0099/0061/Sections/0061.021.html) supplies the six-month state-residence requirement. They are not interchangeable. The Florida Supreme Court's official [*Goedmakers v. Goedmakers* opinion](https://library.law.fsu.edu/Digital-Collections/flsupct/dockets/70407/op-70407.pdf) reiterates *Carroll*'s rule that a dissolution generally accrues where the spouses were last present with a common intent to remain married and rejects marital-property location as an independent venue basis. The official [*Huber v. Huber*, No. 3D20-1228 opinion](https://flcourts-media.flcourts.gov/content/download/682691/opinion/201228_DC13_10212020_105636_i.pdf) applies that rule even when neither spouse still lives in the last-intact Florida county and distinguishes the situation where the marriage was last intact outside Florida.

**Specific resolver:** Explain that county venue is not determined solely by either spouse's current residence; Florida courts generally look to the last Florida county where the spouses lived together intending to remain married, with different analysis when that place was outside Florida or the respondent is a nonresident. Confirm venue before filing. Commercial citator access was unavailable, so negative-treatment verification is limited to current statutory text and subsequent official appellate treatment.

## Preserved HTTP evidence

The reported rules-link failure was reproduced as two completed HTTP responses on 2026-09-16:

```text
https://www.flcourts.gov/content/download/217912/file/Family-Law-Rules-of-Procedure.pdf
http_code=307
redirect_url=https://flcourts-media.flcourts.gov/content/download/217912/file/Family-Law-Rules-of-Procedure.pdf
exit_message=

https://flcourts-media.flcourts.gov/content/download/217912/file/Family-Law-Rules-of-Procedure.pdf
http_code=404
redirect_url=
exit_message=
```

The empty transport-error field and returned HTTP status distinguish this from a retrieval failure such as a DNS, TLS, timeout, or connection error, where no valid HTTP response would be available. The Fanash Uncontested destination itself returned direct `200`; only its outbound rules source was broken. The current [Florida Courts family-law rules page](https://www.flcourts.gov/Services/family-courts/self-help-information/family-law-rules-and-opinions) returned `200` and is the official replacement starting point.

## Independent reviewer reconciliation

One fresh, bounded, read-only `seo_reviewer` pass checked the corrected distinctions. It found no blocker and agreed with the four cleared destinations, three route-specific correction holds, one unresolved Annulment hold, and the absence of a Hub-wide blocker.

| Reviewer finding | Resolution |
|---|---|
| Annulment's central legal claims needed an explicit evidence classification. | Accepted. They now read **unverified within this screen** while the route-specific legal-evidence hold remains. |
| High-Asset materiality needed current authority. | Accepted. The current Florida Bar advertising rule and handbook now support the “top” comparison hold. |
| “Editorial correction” better matches the requested classification vocabulary for the malformed Legal Separation fragment. | Accepted as a clarity refinement. |

No reviewer disagreement remains unresolved. The reviewer did not perform intake confirmation, a complete Annulment case-law review, the later comprehensive destination audit, analytics review, or Florida-attorney approval.

## Verification and preservation

- All eight exact manifest destinations were rechecked on 2026-09-16 and returned direct `200` responses with no redirect.
- The corrected table contains all eight exact URLs and preserves the established V2 node, role, and requiredness mappings.
- Targeted current first-party checks confirmed the quoted mediation, pricing, provider/team, Uncontested, Annulment, High-Asset, and filing-language evidence.
- Official venue authorities, the June 15, 2026 Florida Bar rules compilation, the current Florida Courts rules page, § 61.031, the Orange County Clerk page, and the Fanash pricing page returned `200`. The superseded compiled-rules target returned the preserved `404` above.
- The prior reviewer response remains unchanged at SHA-256 `8fe7feeaa9f46e0d8908bc731b07086a2da8ef4e9aed403eb17ac2667478147d`.
- No destination copy, Hub link, DOCX, manifest, architecture, application, website, Git history, or publication state was changed.

## Learning disposition and remaining limits

This is an external, client-specific correction, not a principle established by the original agents. No new general SEO principle or workflow change was promoted. The existing `AGENTS.md` strategy-review blocker check already governs the demonstrated scope distinction, so no duplicate learning record was added.

Remaining evidence questions are route-specific: current intake acceptance for seven service destinations; whether Fanash also acts as a neutral mediator; the Annulment page's primary-authority legal review; SmartStep eligibility by matter; and support for the unverified provider-count, experience, volume, judge-insight, and comparison claims. The comprehensive destination audit remains later and separate.
