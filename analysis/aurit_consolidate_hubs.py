#!/usr/bin/env python3
"""
v2: fold the 21 H2 Section Module rows into their 4 parent hub rows.

Rationale: an H2 section module is not a separate deliverable - it is content on the hub URL.
One page = one row = one ticket. Consolidating also makes the sequencing explicit: the hub must be
fully sectioned FIRST so every expansion page has a live parent section and an anchor slot waiting
for it, which is exactly how the V4 architecture instructs production to work
("Strengthen the hub first, build the H2 modules, feature approved child pages...").

Reuses v1's validated row copy verbatim so no child-page wording changes.
"""
import csv, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("v1", os.path.join(HERE, "aurit_strategy_buildout.py"))
v1 = importlib.util.module_from_spec(spec)
sys.stdout = open(os.devnull, "w")          # silence v1's own prints
spec.loader.exec_module(v1)
sys.stdout = sys.__stdout__

HEADER, MONTHS, rows = v1.HEADER, v1.MONTHS, v1.rows

HUBS = [
    ("Divorce Mediation",              "(Divorce Mediation Hub - ",              "/divorce-mediation/"),
    ("Child Support Mediation",        "(Child Support Hub - ",                  "/child-support-mediation/"),
    ("Child Custody Mediation",        "(Child Custody Hub - ",                  "/child-custody-mediation/"),
    ("Spousal Maintenance Mediation",  "(Spousal Maintenance Hub - ",            "/spousal-support-alimony-mediation/"),
]

# new hour placement for the consolidated hub rows (frame + all its modules)
HUB_HOURS = {
    "Divorce Mediation":             {"Sep": 28},
    "Child Support Mediation":       {"Oct": 21},
    "Child Custody Mediation":       {"Nov": 20},
    "Spousal Maintenance Mediation": {"Nov": 9, "Dec": 10},   # 19 hrs split across two sprints
}

SCOPE = {
    "Divorce Mediation": (
        "Scope: complete V4 hub build - page frame plus all SIX H2 section modules on this one URL. "
        "This page must be finished before the 27 expansion pages are briefed, so every child page has a "
        "live parent section and a prepared anchor slot to publish into."),
    "Child Support Mediation": (
        "Scope: complete V4 hub build - page frame plus all FIVE H2 section modules on this one URL. "
        "Finish this page before the 7 expansion pages are briefed, so every child page has a live parent "
        "section and a prepared anchor slot to publish into."),
    "Child Custody Mediation": (
        "Scope: complete V4 hub build - page frame plus all SIX H2 section modules on this one URL. "
        "Finish this page before the 7 expansion pages are briefed, so every child page has a live parent "
        "section and a prepared anchor slot to publish into."),
    "Spousal Maintenance Mediation": (
        "Scope: complete V4 hub build - page frame plus all FOUR H2 section modules on this one URL. "
        "Finish this page before the 9 expansion pages are briefed, so every child page has a live parent "
        "section and a prepared anchor slot to publish into."),
}

PHASING = (
    "PUBLISHING SEQUENCE\n"
    "- Phase 1 (this row): publish the page frame, every H2 heading, every section introduction, and every "
    "unlinked on-hub H3/H4 topic. Those need no child URLs and go live immediately.\n"
    "- Phase 2 (this row): stage the featured-card and text-link slots for each approved child page. Where "
    "the child page is already live, activate the link now. Where it is not, leave the slot built but "
    "unpublished.\n"
    "- Phase 3 (expansion page rows): as each child page publishes, switch on its prepared card or anchor. "
    "No hub rebuild required - the section already exists."
)


def title_of(project):
    m = re.search(r"\n- (.+?) \(", project, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def hours_of(row):
    return {m: float(row[5 + i]) for i, m in enumerate(MONTHS) if row[5 + i]}


# ---- collect module rows per hub --------------------------------------------
mods = {h: [] for h, _, _ in HUBS}
for r in rows:
    if r[2].startswith("Hub Section Module"):
        for hub, tok, _ in HUBS:
            if tok in r[2]:
                mods[hub].append(r)
                break
        else:
            raise SystemExit(f"unmatched module row: {r[2]!r}")

assert sum(len(v) for v in mods.values()) == 21, "expected 21 module rows"

# ---- compose new hub descriptions -------------------------------------------
newrows, dropped = [], 0
for r in rows:
    if r[2].startswith("Hub Section Module"):
        dropped += 1
        continue

    if r[2].startswith("Core Service Hub Page"):
        hub = next(h for h, _, _ in HUBS if h in r[2])
        url = next(u for h, _, u in HUBS if h == hub)
        frame_hrs = int(sum(hours_of(r).values()))
        mod_rows = mods[hub]
        mod_hrs = int(sum(sum(hours_of(m).values()) for m in mod_rows))

        parts = [
            f"URL: {url} (existing page - optimize and expand)",
            SCOPE[hub],
            "",
            f"PAGE FRAME ({frame_hrs} hrs)",
        ]
        # original hub bullets, minus the URL line we already wrote
        for line in r[3].split("\n")[1:]:
            parts.append(("  " + line) if line.startswith("-") else line)

        for i, m in enumerate(mod_rows, 1):
            h = int(sum(hours_of(m).values()))
            body = m[3].split("\n")
            grp = ""
            gm = re.search(r"Internal architecture group: (.+?)\.?$", body[0])
            if gm:
                grp = gm.group(1).rstrip(".")
                grp = re.sub(r"\s*\(internal label only[^)]*\)", "", grp).strip()
            parts += ["", f"H2 SECTION {i} - {title_of(m[2])} ({h} hrs)"]
            if grp:
                parts.append(f"  Internal group: {grp} - internal label only, never the public heading")
            # drop per-module phasing note - the global PUBLISHING SEQUENCE block now covers it
            SKIP = ("Exact build format:",
                    "Publish with whatever child links are already live and add remaining anchors "
                    "as each child page ships.")
            for line in body[1:]:
                if line.strip() in SKIP:
                    continue
                parts.append("  " + line if line.startswith("-") else "  " + line)

        parts += ["", PHASING]

        newdesc = "\n".join(parts)
        newimpact = (
            r[4]
            + " Building the page frame and all "
            + {"Divorce Mediation": "six", "Child Support Mediation": "five",
               "Child Custody Mediation": "six", "Spousal Maintenance Mediation": "four"}[hub]
            + " H2 sections as one deliverable means the hub is structurally complete before any expansion "
              "page is written, so each child page publishes into a section that already ranks and already "
              "passes internal authority - rather than arriving as an orphan that triggers a hub rewrite."
        )
        hrs = HUB_HOURS[hub]
        assert int(sum(hrs.values())) == frame_hrs + mod_hrs, \
            f"{hub}: schedule {sum(hrs.values())} != work {frame_hrs + mod_hrs}"

        proj = r[2].replace("(L1 Main Practice Hub - Optimize & Expand)",
                            f"(L1 Main Practice Hub - Optimize, Expand & Build All H2 Sections)")
        newrows.append([r[0], r[1], proj, newdesc, newimpact]
                       + [str(int(hrs[m])) if m in hrs else "" for m in MONTHS])
        continue

    newrows.append(r)

assert dropped == 21

OUT = os.path.join(HERE, "Aurit_2026_Strategy_Buildout_Divorce_ChildSupport_ChildCustody_SpousalMaintenance.csv")
with open(OUT, "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADER)
    for r in newrows:
        w.writerow(r)

data = [r for r in newrows if r[3]]
tot = {m: 0.0 for m in MONTHS}
for r in newrows:
    for i, m in enumerate(MONTHS):
        if r[5 + i]:
            tot[m] += float(r[5 + i])
existing = {"July": 53.5, "Aug": 44.5, "Sep": 19, "Oct": 26, "Nov": 20, "Dec": 20, "Jan": 20, "Beyond": 0}
print(f"Wrote {OUT}")
print(f"Rows: {len(newrows)} total / {len(data)} deliverable  (was 79 / 75 - 21 module rows folded in)")
print("New hours by month :", {k: round(v, 1) for k, v in tot.items()})
print("New hours total    :", round(sum(tot.values()), 1), "(unchanged)")
print("Combined by month  :", {m: round(existing[m] + tot[m], 1) for m in MONTHS})
