#!/usr/bin/env python3
"""QA pass 2 - fixed normalization + role-accuracy and guardrail checks."""
import csv, re, os, html as htmlmod, unicodedata

HTML = os.path.expanduser("~/Downloads/preview (1).html")
OUT = os.path.expanduser("~/SEO_Dept/analysis/Aurit_2026_Strategy_Buildout_Divorce_ChildSupport_ChildCustody_SpousalMaintenance.csv")

TAGS = {"divorce-mediation": "Divorce Mediation",
        "child-support-mediation": "Child Support Mediation",
        "child-custody-mediation": "Child Custody Mediation",
        "spousal-maintenance-mediation": "Spousal Maintenance Mediation"}

raw = open(HTML, encoding="utf-8", errors="replace").read()
starts = {m.group(1): m.start() for m in re.finditer(r'<section id="([^"]+)" class="root-block[^"]*"', raw)}
keys = list(starts)
blocks = {k: raw[starts[k]:(starts[keys[i+1]] if i+1 < len(keys) else len(raw))] for i, k in enumerate(keys)}


def norm(s):
    """Aggressive normalization: strip tags, unify all dash/quote variants, collapse space, casefold."""
    s = re.sub(r"<[^>]+>", "", s)
    s = htmlmod.unescape(s)
    s = unicodedata.normalize("NFKD", s)
    for ch in "‐‑‒–—―−":
        s = s.replace(ch, "-")
    for ch in "‘’ʼ":
        s = s.replace(ch, "'")
    for ch in "“”":
        s = s.replace(ch, '"')
    s = re.sub(r"\s+", " ", s)
    return s.strip().casefold()


parsed = {}
for k in TAGS:
    b = blocks[k]
    parsed[k] = dict(
        featured=[norm(x) for x in re.findall(r'<span class="badge">H3 CARD</span><span class="name">(.*?)</span>', b)],
        textlinks=[norm(x) for x in re.findall(r'<span class="badge">TEXT LINK</span><span class="name">(.*?)</span>', b)],
        onhub=[norm(x) for x in re.findall(r'<li class="on-title"><span class="badge">(?:SECTION FIRST|ON-PAGE)</span>(.*?)</li>', b)],
        gov=[norm(x) for x in re.findall(r'<li><strong>\[(DO NOT BUILD|HOLD|CONSOLIDATE)\]</strong>(.*?)</li>', b) for x in [x[1]]],
        h2s=[norm(x) for x in re.findall(r'<span class="heading-tag h2">H2 - NOT LINKED</span>(.*?)</h3>', b)],
    )

gen = list(csv.reader(open(OUT, encoding="utf-8-sig")))
rows = [r for r in gen[1:] if r[3]]
blob = norm(" ".join(r[2] + " " + r[3] for r in rows))

fails = []

print("=" * 80)
print("QA-2A  COVERAGE (normalized: em/en dashes, curly quotes unified)")
print("=" * 80)
for k, tag in TAGS.items():
    p = parsed[k]
    for label, items in [("child links", p["featured"] + p["textlinks"]), ("on-hub topics", p["onhub"]),
                         ("H2 sections", p["h2s"]), ("governance", p["gov"])]:
        miss = [t for t in items if t not in blob]
        status = "PASS" if not miss else "FAIL " + str(miss)
        if miss:
            fails.append((tag, label, miss))
        print(f"  {tag:<30}{label:<15}{len(items):>3} items   {status}")

print()
print("=" * 80)
print("QA-2B  H2 SECTIONS EMBEDDED IN THE PARENT HUB ROW (consolidated model)")
print("=" * 80)
for k, tag in TAGS.items():
    want = len(parsed[k]["h2s"])
    hubrow = [r for r in rows if r[2].startswith("Core Service Hub Page") and tag in r[2]]
    if len(hubrow) != 1:
        fails.append((tag, "hub row count", len(hubrow)))
        print(f"  {tag:<30}FAIL - {len(hubrow)} hub rows")
        continue
    d = hubrow[0][3]
    got = len(re.findall(r"^H2 SECTION \d+ - ", d, re.M))
    inside = [t for t in parsed[k]["h2s"] if t in norm(d)]
    # on-hub topics for this hub must also live inside the hub row, not anywhere else
    onhub_inside = [t for t in parsed[k]["onhub"] if t in norm(d)]
    okk = (want == got == len(inside)) and len(onhub_inside) == len(parsed[k]["onhub"])
    if not okk:
        fails.append((tag, "H2 embed", f"{want}/{got}/{len(inside)}"))
    print(f"  {tag:<30}HTML H2s {want}  /  embedded blocks {got}  /  titles present {len(inside)}"
          f"  /  on-hub topics in hub row {len(onhub_inside)}/{len(parsed[k]['onhub'])}"
          f"   {'PASS' if okk else 'FAIL'}")
    # hub hours must equal frame + declared module hours
    declared = sum(int(x) for x in re.findall(r"\((\d+) hrs\)", d))
    booked = sum(float(v) for v in hubrow[0][5:] if v)
    hmatch = declared == booked
    if not hmatch:
        fails.append((tag, "hub hours", f"declared {declared} vs booked {booked}"))
    print(f"    hours: declared in description {declared}  /  booked in month columns {booked:g}"
          f"   {'PASS' if hmatch else 'FAIL'}")

print()
print("=" * 80)
print("QA-2C  ROLE ACCURACY - does each child page carry the HTML's role label?")
print("=" * 80)
role_fail = 0
for k, tag in TAGS.items():
    p = parsed[k]
    for title in p["featured"] + p["textlinks"]:
        want = "featured h3 card" if title in p["featured"] else "supporting text link"
        hit = [r for r in rows if norm(r[2]).startswith(("core", "live")) and f"- {title} (" in norm(r[2])]
        if not hit:
            print(f"  FAIL  no row  [{tag}] {title}")
            role_fail += 1
            continue
        if len(hit) > 1:
            print(f"  FAIL  {len(hit)} rows [{tag}] {title}")
            role_fail += 1
            continue
        if want not in norm(hit[0][2]):
            print(f"  FAIL  role    [{tag}] {title}  -> expected '{want}'  got '{hit[0][2]}'")
            role_fail += 1
print(f"  {'ALL ROLE LABELS MATCH HTML' if role_fail == 0 else str(role_fail)+' role mismatches'}"
      f"   {'PASS' if role_fail == 0 else 'FAIL'}")
if role_fail:
    fails.append(("all", "role labels", role_fail))

print()
print("=" * 80)
print("QA-2D  GUARDRAILS - no on-hub topic or governance item may get its own build row")
print("=" * 80)
buildrows = [r for r in rows if r[2].startswith(("Core Situational", "Core Comparison", "Core Process",
                                                 "Core Educational", "Core Resource", "Core FAQ", "Live Page"))]
leak = []
for k, tag in TAGS.items():
    for t in parsed[k]["onhub"] + parsed[k]["gov"]:
        for r in buildrows:
            # a build row's own page name is the text after "- " on line 2, before " ("
            m = re.search(r"\n- (.+?) \(", r[2])
            if m and norm(m.group(1)) == t:
                leak.append((tag, t, r[2].replace("\n", " ")))
print(f"  on-hub / governance topics wrongly given a page row: {len(leak)}   "
      f"{'PASS' if not leak else 'FAIL'}")
for l in leak:
    print("    ", l)
if leak:
    fails.append(("all", "guardrail leak", leak))

print()
print("=" * 80)
print("QA-2E  EVERY BUILD ROW TRACES BACK TO AN HTML CHILD LINK")
print("=" * 80)
all_html_children = set()
for k in TAGS:
    all_html_children |= set(parsed[k]["featured"]) | set(parsed[k]["textlinks"])
orphan = []
for r in buildrows:
    m = re.search(r"\n- (.+?) \(", r[2])
    if m and norm(m.group(1)) not in all_html_children:
        orphan.append(m.group(1))
print(f"  build rows with no matching HTML child link: {len(orphan)}   {'PASS' if not orphan else 'FAIL'}")
for o in orphan:
    print("     ", o)
if orphan:
    fails.append(("all", "orphan build rows", orphan))

print()
print("=" * 80)
print("QA-2F  ROW-TYPE INVENTORY")
print("=" * 80)
from collections import Counter
kinds = Counter(r[2].split("\n")[0] for r in rows)
for kk, v in sorted(kinds.items(), key=lambda x: -x[1]):
    print(f"  {kk:<45}{v}")
print(f"  {'TOTAL':<45}{len(rows)}")

print()
print("=" * 80)
print("FINAL:", "ALL CHECKS PASS" if not fails else f"{len(fails)} CHECK GROUP(S) FAILED")
print("=" * 80)
