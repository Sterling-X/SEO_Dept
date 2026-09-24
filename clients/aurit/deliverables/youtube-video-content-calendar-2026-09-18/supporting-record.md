# Aurit Mediation YouTube Video Content Calendar: Supporting Record

Prepared: September 18, 2026. Strategist: Casey's SEO Strategist (Claude Code session). Client: The Aurit Center for Divorce Mediation, auritmediation.com. Deliverable: `Aurit Mediation | YouTube Video Content Calendar - Sept 2026` (xlsx in this folder; native Google Sheet in Casey's My Drive).

## Request

Research live web trends for a new YouTube video content calendar for Aurit Mediation, identify trending topics and the questions users consistently seek answers to about mediation and the industry, and develop a calendar in the format of Casey's historical calendars, organised specifically for Aurit.

## Scope decisions made by the strategist

- Market scope: Arizona. The about page lists Arizona only and claims "10,000+ Arizona Families Helped"; a thin `/california/` page exists (320 words). California is recorded as an open question, not a calendar scope.
- Format lineage: Kalish & Jaggars six-tab structure (Calendar, Recording Briefs, Shorts, Topic Research, Publishing Plan, AI Search Briefs) with the Hicks Family Lawyers Legend, Order, Hub Section, Internal Link Target, Featured Speaker and CTA conventions and header styling (Arial 10, white on navy 101F3C, frozen header). Two tabs added for Aurit: Legal Verification and Evidence Sources.
- Governing constraint honoured: the client's 2026 Strategic Plan (Q3-4 tab, rows 85-88) sets an ARCHITECTURE GATE: no standalone Video Support Hub; default to an on-page module on `/resources/`; support pages only for approved videos with distinct intent; no embed-only pages. Every calendar row maps to an existing live page; rows that would need a new page are flagged "ARCHITECTURE GATE: requires approval".
- Live check: `/resources/` returns 404 on the live site (WebFetch, 2026-09-18). The gate's default home does not exist yet; the Publishing Plan states this dependency rather than presenting `/resources/` as a destination.
- Family-law architecture authority: `context/architecture/Family_Law_StructureV2.html` governs family-law architecture decisions in this repository. This calendar makes no architecture decision; it maps videos to Aurit's existing live pages and the client's own hub maps, and flags where a page would need approval.

## Evidence inventory (all in `evidence/`)

| File | Contents | Provenance |
|---|---|---|
| `aurit_brief.md` | Consolidated verified client facts, assets, gate text, format lineage, endpoint availability | Compiled 2026-09-18 |
| `aurit_keyword_research.csv`, `aurit_kw_vol.csv`, `aurit_priorities.csv` | 103 keywords with volume, difficulty, SERP features (36 with Video, several with AI Overview); 43 content priorities | Drive: "Aurit \| Comp. Gap, KW Research & Nav Layout", modified 2026-07-30 |
| `aurit_ai_content_plan.csv` | 82 planned AI-first supporting articles with primary conversational queries | Drive: "Aurit_Detailed_AI_Supporting_Content_Plan_2026_27", modified 2026-09-08 |
| `aurit_live_url_match*.csv` (4 files) | Client hub maps: H2 sections, intents, best live URL, coverage (Full/Partial/No Match) | Drive: "Aurit_Live_URL_Match_Production", modified 2026-09-10 |
| `aurit_live_pages.csv` | 192 live direct-200 pages: path, title, H1, word count, template | Parity audit crawl, 2026-09-17 |
| `autocomplete_sweep.csv` | 1,012 unique Google (745) and YouTube (267) autocomplete suggestions from 40 seeds x 12 question prefixes (960 requests) | Collected 2026-09-18 |
| `youtube_search_sweep.csv` | 585 YouTube results across 30 queries: rank, title, views, age, length, channel | Collected 2026-09-18 |
| `format_template_hicks_2026-09.xlsx` | Casey's Hicks calendar, used for format only | Drive, 2026-09-10 |
| Workflow JSON outputs (added on completion) | Seven research lenses, synthesis, adversarial verdicts, draft, legal verification, completeness critic | 2026-09-18 |

## Client facts verified 2026-09-18 (auritmediation.com via WebFetch; curl is blocked by Cloudflare)

- Karen Aurit, Founder and CEO (no degrees or licences stated on her team page). Michael Aurit, Founder, Mediator; J.D. in Conflict Resolution, Pepperdine University. Andrew Weber, Lead Mediator. About page: "licensed Arizona attorney-mediators and mediation specialists", "over a decade", "10,000+ Arizona Families Helped", "7-Time Best of Our Valley winners".
- Pricing: flat fee, "$4,000-$7,800" total for most divorces, "$2,000-$3,800" per person; 0% financing "as low as $92/month"; "Free 1-hour consultation".
- Process: free consultation; Meeting 1 foundation; Meetings 2-3 financial; Meetings 3-4 parenting plan; mediator drafts the Marital Settlement Agreement and helps file; "3-5 sessions over 2-4 months"; sessions "typically last 2 hours"; in person or virtual; "60-day waiting period (Arizona requirement)" (client statement; statute verification recorded in the Legal Verification tab).
- Locations named on site: Scottsdale, Glendale, Gilbert, Chandler, Tucson, Flagstaff, Goodyear, Phoenix. Staffed-office status: Unknown - verification required.
- Existing video assets: YouTube "The Aurit Center For Divorce Mediation" (@auritdivorcemediation, 9 subscribers, 8 videos, last upload 2022-10-13, brand film 9,010 views); YouTube "Aurit Mediation" (created 2025-06-27, 0 videos); 16 Vimeo talking-head assets (Michael and Karen, Sept 2025, ClickUp task 86b6nuw3n still in backlog); 3 Vimeo embeds live on site.
- 13 live FAQ questions on `/frequently-asked-questions/`; 94 live blog posts (list in `aurit_live_pages.csv`).

## Method

1. Located historical calendars (Hicks xlsx, Kalish Google Sheet) and dumped their structure; confirmed no prior Aurit YouTube sheet exists in ClickUp or Drive.
2. Pulled client-owned demand and architecture evidence from Drive (Sheets API) and the 2026-09-17 parity crawl.
3. Verified client facts live; inventoried both YouTube channels (RSS) and Vimeo/YouTube embeds (oEmbed).
4. Ran deterministic autocomplete and YouTube search sweeps as shared evidence.
5. Multi-agent workflow: seven research lenses (autocomplete/PAA, YouTube performance, forums, AI search, Arizona legal/news, competitors, client fit) -> synthesis and scoring -> batched adversarial verification (evidence skeptic and fit/compliance skeptic per candidate) -> structured draft -> live legal-fact verification and completeness critic.
6. Strategist consolidation, workbook build (`qa/build_workbook.py`), deterministic validation (`qa/validate_workbook.py`), independent `seo-reviewer` review, resolution of findings, upload (`qa/upload_to_drive.sh`), commit.

## Endpoint availability recorded for this run

Working: Google suggest (web and YouTube), YouTube search HTML, YouTube RSS, YouTube and Vimeo oEmbed, WebFetch on auritmediation.com, WebSearch, Google Drive and Sheets APIs (gcloud user credential with Drive scope). Failing: Reddit JSON (403), Google Trends API (429), Google SERP HTML (no People Also Ask rendered), Wayback availability API (non-JSON), curl on auritmediation.com (Cloudflare block). Community and trend evidence therefore came through WebSearch and dated secondary sources; this is disclosed in the workbook Legend.

## Open questions for Casey / Aurit (not decided here)

1. Channel consolidation: two YouTube channels exist. Options are presented in the Publishing Plan; no channel was chosen.
2. California scope: `/california/` exists but the firm describes itself as Arizona-only.
3. `/resources/` is 404 live although the master architecture names it as the L1 supporting root and the default video module home.
4. Whether the eight named locations are staffed offices or meeting locations.
5. Whether Michael Aurit's ASU Lodestar faculty role (client blog, undated) is current, and how Karen Aurit's credentials should be stated on camera.

## Review record

(Filled in after `seo-reviewer` returns: material findings, evidence-based dispositions, unresolved disagreement.)

## Verification summary

(Filled in after build: validator result, legal verification counts, reconciliation counts, Drive upload confirmation, commit hash.)
