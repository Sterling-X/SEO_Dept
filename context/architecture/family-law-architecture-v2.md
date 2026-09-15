# Family Law Architecture V2 Reference

## Authority and scope

The governing artifact is [Family_Law_StructureV2.html](./Family_Law_StructureV2.html), imported byte-for-byte from the supplied download. Its SHA-256 is `21599c066128779163c4b3c0831197d67871ad41ea2bbf1e83bafb739523bc7b` (396,353 bytes). This Markdown file is a working guide; if it differs from the HTML or its embedded data, the HTML governs.

Use V2 for intended family-law architecture decisions. It supersedes historical evaluation excerpts, unfinished Sterling website or project implementations, and generic architecture, linking, or URL defaults in imported skills. Explicit user instructions still take precedence. V2 contains 514 nodes, 3,212 mapped relationships, and 14 visual clusters. It explicitly has **no Family Law pillar**.

## How to read V2

- **Hierarchy:** The node `parent` field and 494 `Canonical parent → child` relationships define ownership. Of those, 489 carry “Use when contextually relevant”; the other five point to non-publishable structural groupings and explicitly are not hyperlinks.
- **Internal links:** The 2,718 `Source-derived internal link` records are directional. Read every arrow from source to destination and preserve the recorded direction. Do not infer a reciprocal, sibling, hub, or navigation link merely from topical proximity.
- **Visual grouping:** Outer boundaries, inner page-role subclusters, clusters, subclusters, dotted ownership guides, and layout coordinates explain the diagram. They do not create hierarchy or links. In particular, a structural non-page may own a visual branch without being a publishable URL.
- **Planning:** Build stages and the Grandparents’ Rights build prerequisite are sequencing aids, not internal links.
- **URLs:** Use only paths present in the node data. A missing path is unresolved, not permission to derive one from another project or a generic convention.

## Practice-area hubs and branches

The Foundation 42 is the Location Hub, Attorneys hub, seven primary practice hubs, and 33 Required core branches. The remaining branch depth is a mix of procedural, situational, educational, resource, and supporting pages. `Optional` and `Conditional` are architecture states, not automatic production approval.

| V2 role | Hub and canonical path | Required Foundation-42 branches or branch summary |
|---|---|---|
| Primary foundation hub | **Divorce** (`FL-PA-DIV`, `/divorce/`) | Collaborative Divorce; Contested Divorce; Divorce Mediation; Legal Separation; Uncontested Divorce; High-Conflict Divorce. Other branches include procedural, situational, educational, resource, and supporting pages. LGBTQ+ Divorce & Parentage and Cultural / Religious / International Divorce are non-page visual groupings beneath Divorce. |
| Primary foundation hub | **Child Custody** (`FL-PA-CUST`, `/child-custody/`) | Child Custody Modification; Emergency Custody Orders; Parenting Plans; High-Conflict Custody; Parenting Time Disputes; Relocation / Move-Away Custody Disputes; Supervised Visitation. Other branches include procedural, situational, educational, resource, and supporting pages. |
| Primary foundation hub | **Child Support** (`FL-PA-SUP`, `/child-support/`) | Child Support Enforcement; Child Support Modification; Back Child Support / Arrears; Child Support Disputes After Income Changes; Self-Employed or Variable Income Support. Other branches include procedural, situational, educational, resource, and supporting pages. |
| Primary foundation hub | **Alimony & Spousal Support** (`FL-PA-ALIM`, `/alimony/`) | Long-Term Spousal Support; Temporary Spousal Support; High-Income Spousal Support Disputes; Long-Term Marriage Divorce. Other branches include procedural, situational, educational, resource, and supporting pages. |
| Primary foundation hub | **Property Division** (`FL-PA-PROP`, `/property-division/`) | Equitable Distribution; Marital vs Separate Property; Divorce Involving Business Ownership; Business Valuation and Division; Hidden Assets and Financial Misconduct. Other branches include procedural, situational, educational, resource, and supporting pages. Business / Entrepreneur / Gig-Economy Divorce is a non-page visual grouping beneath Property Division. |
| Primary foundation hub | **Paternity** (`FL-PA-PAT`, `/paternity/`) | Establishing Paternity; Challenging Paternity. Other branches include procedural, situational, educational, and supporting pages. |
| Primary foundation hub | **Guardianship** (`FL-PA-GUARD`, `/guardianship/`) | Adult Guardianship; Emergency Guardianship; Guardianship of a Minor; Temporary Guardianship. V2 classifies all four as Required procedural pages. Other branches include procedural, situational, educational, and supporting pages. |
| Expansion anchor | **Adoption** (`FL-PA-ADOPT`, `/adoption/`) | Procedural, situational, educational, and supporting branches. International Adoption is Conditional and service/jurisdiction-gated. |
| Expansion anchor | **Prenuptial & Postnuptial Agreements** (`FL-PA-PRE`, `/prenups-postnups/`) | Procedural, situational, educational, and supporting branches. Two postnup situations are Conditional; one is also on architecture hold. |
| Expansion anchor | **Protective Orders & Domestic Violence** (`FL-PA-PROT`, `/protective-orders/`) | The hub and its three procedural branches—Emergency Protective Orders, Restraining Orders / Orders of Protection, and Violations of Protective Orders—are Conditional and service/jurisdiction-gated. Supporting branches sit beneath the hub, including one beneath Emergency Protective Orders. |
| Dependent cluster anchor | **Grandparents’ Rights** (`FL-PA-GPR`, `/grandparents-rights/`) | Conditional on state law and local demand. Its two direct supporting children remain separate from five grandparent pages hierarchically owned by `FL-M048`, Grandparent Visitation and Custody, beneath Child Custody. `FL-M048 → FL-PA-GPR` is a build dependency only; the `FL-M048` note calls for a prominent cross-link **if** the hub is built, but that pair is not a mapped relationship edge. |

The staged build sequence is: nine foundation hubs; 33 core branches; the `FL-M048` bridge and `FL-PA-GPR` dependent anchor; three expansion anchors; remaining canonical branch depth; then templates and structural models. The source does not define a total order within each stage. Consult the HTML’s reference table for every branch, stage, prerequisite, metadata field, and path; use the interactive map or embedded relationship data for exact directional edges.

## Location and service-area architecture

These are two distinct branches under the required Location Hub:

```text
Location Hub — FL-OFFICE-INDEX — /locations/
├── [Location] Page — FL-OFFICE-PAGE-TPL — /locations/{office-city}/
│   └── nine location-specific practice-area hub templates — paths unresolved
└── Service Area Hub — FL-SA-INDEX — /service-areas/
    └── [County] Page — FL-SA-COUNTY-TPL — /service-areas/{county}/
        └── [City] Page — FL-SA-LOCATION-PAGE-TPL — path unresolved
```

- A `[Location] Page` is a verified physical-location template. It requires real location evidence and verified name, address, and phone details.
- Its nine Conditional local-practice templates cover Adoption, Alimony, Child Custody, Child Support, Divorce, Guardianship, Paternity, Prenups, and Property Division. Each must confirm that the service is offered locally, stay concise, and link to its comprehensive canonical practice hub. V2 defines no URL for these templates.
- The Service Area Hub is publishable and Required, but County and City pages are Conditional templates. They must use service-area language and must not imply a physical office. V2 defines no City Page URL.
- V2 defines neither a state-hub layer nor a URL for any missing local template. Do not borrow state, county, or city patterns from an imported skill or client implementation.

## Conditional templates and open decisions

All 15 templates are `Instantiate Only` and require instance evidence: an attorney page and attorney-review page, an event detail page, the physical-location page, County and City pages, and the nine location-specific practice hubs. The event template is Optional; the other 14 are Conditional. Defined paths exist only for attorney, attorney-review, event, physical-location, and County templates. The City and nine local-practice paths are intentionally null.

Eleven canonical nodes are on `HOLD — ARCHITECTURE REVIEW`: `FL-M013` Summary Dissolution; `FL-M014` Divorce After Infidelity; `FL-M034` DIY Divorce Forms; `FL-M057` Joint Custody Explained; `FL-M106` Can Men Receive Alimony; `FL-M107` Can a Prenup Waive Alimony?; `FL-M114` Temporary vs Permanent Alimony; `FL-M142` Marital Property Explained; `FL-M145` Separate Property Explained; `FL-M152` Voluntary Acknowledgment and DNA Testing; and `FL-M221` Postnups After Infidelity or Reconciliation. Their embedded notes state the issue to resolve; a listed path does not clear the hold.

Eight other canonical nodes require service/jurisdiction validation: Military Divorce, International Adoption, Postnups During Marriage Trouble, the Protective Orders hub and its three procedural children, and the Grandparents’ Rights hub. Three site nodes—In the News, Privacy Policy, and Terms of Service—remain provisional pending architecture review.

No mapped relationship row has an unresolved relationship status: 3,207 are resolved, and five are non-linkable structural associations. `Template URL pending approved market convention` exists in the embedded status vocabulary but is used by zero relationship rows. The unresolved items are therefore template paths, instance gates, conditional activation, node-level architecture holds, and provisional architecture validations—not missing relationship records that may be invented.

## Precedence over older references

- `evaluations/sterling-divorce-architecture-exercise.md` is a five-case exercise based on a historical 12-row excerpt. Its “omitted 512” wording implies 524 total records, while V2 defines 514 nodes. It also calls the `FL-M025` activation rule unknown; V2 now supplies the rule (firm handles the matter and local demand supports a standalone page), while whether a particular client or market satisfies it remains unresolved. Contextual links proposed by the exercise are not V2-mapped edges unless the embedded relationship data independently contains them.
- The imported `family-law-service-area-seo` skill uses a state-hub model and Johnson Law Group URL examples. Those defaults conflict with V2’s Location Hub fork and cannot determine this architecture or its paths.
- Imported family-law writing skills label Emergency Guardianship as Situational. V2 controls this architecture and classifies `FL-M166` as a Required procedural page.
- Blanket or reciprocal link rules in imported writing skills and generic SEO guidance do not add links to V2. Use the embedded directional relationships and node notes.
- `context/seo-principles.md` and `evaluations/README.md` are compatible general guidance: they separate page roles and verified offices from service areas, but they do not define this tree.
