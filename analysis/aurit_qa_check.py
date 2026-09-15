#!/usr/bin/env python3
"""QA: cross-check the generated strategy CSV against preview (1).html and the V4 architecture CSV."""
import csv, re, os, html as htmlmod

HTML = os.path.expanduser("~/Downloads/preview (1).html")
ARCH = os.path.expanduser("~/Downloads/Aurit%20Mediation%20-%20Architecture%20Master%20Production%20V4 - Master_Architecture.csv")
OUT = os.path.expanduser("~/SEO_Dept/analysis/Aurit_2026_Strategy_Buildout_Divorce_ChildSupport_ChildCustody_SpousalMaintenance.csv")

TARGETS = ["divorce-mediation", "child-support-mediation", "child-custody-mediation",
           "spousal-maintenance-mediation"]

raw = open(HTML, encoding="utf-8", errors="replace").read()

# --- split top-level <section id="..." class="root-block ..."> ---------------
sections = {}
for m in re.finditer(r'<section id="([^"]+)" class="root-block[^"]*"', raw):
    sections[m.group(1)] = m.start()
keys = list(sections)
bounds = {}
for i, k in enumerate(keys):
    end = sections[keys[i + 1]] if i + 1 < len(keys) else len(raw)
    bounds[k] = raw[sections[k]:end]


def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    return htmlmod.unescape(s).replace("’", "'").replace("–", "-").strip()


parsed = {}
for k in TARGETS:
    blk = bounds[k]
    # header counts
    pills = re.findall(r'<div class="count-pill"><strong>(\d+)</strong><span>([^<]+)</span>', blk)
    counts = {clean(lbl): int(n) for n, lbl in pills}
    # featured cards + text links + on-hub topics
    featured = [clean(x) for x in re.findall(r'<span class="badge">H3 CARD</span><span class="name">(.*?)</span>', blk)]
    textlinks = [clean(x) for x in re.findall(r'<span class="badge">TEXT LINK</span><span class="name">(.*?)</span>', blk)]
    onhub = [clean(x) for x in re.findall(r'<li class="on-title"><span class="badge">(?:SECTION FIRST|ON-PAGE)</span>(.*?)</li>', blk)]
    gov = [clean(x) for x in re.findall(r'<li><strong>\[(?:DO NOT BUILD|HOLD|CONSOLIDATE)\]</strong>(.*?)</li>', blk)]
    h2s = [clean(x) for x in re.findall(r'<span class="heading-tag h2">H2 - NOT LINKED</span>(.*?)</h3>', blk)]
    parsed[k] = dict(counts=counts, featured=featured, textlinks=textlinks,
                     onhub=onhub, gov=gov, h2s=h2s)

# --- load generated CSV ------------------------------------------------------
gen = list(csv.reader(open(OUT, encoding="utf-8-sig")))
hdr, genrows = gen[0], [r for r in gen[1:] if r[3]]
blob = "\n".join(r[2] + "\n" + r[3] for r in genrows)
projnames = [r[2] for r in genrows]

EXPECT_HDR = ["Status", "CU", "Projects", "Description", "Impact",
              "July", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Beyond"]

print("=" * 78)
print("QA 1 - CSV INTEGRITY")
print("=" * 78)
print("  header matches strategy sheet :", "PASS" if hdr == EXPECT_HDR else f"FAIL {hdr}")
widths = set(len(r) for r in gen)
print("  all rows 13 columns           :", "PASS" if widths == {13} else f"FAIL {widths}")
print("  deliverable rows              :", len(genrows))
dupes = [p for p in set(projnames) if projnames.count(p) > 1]
print("  duplicate project names       :", "PASS (none)" if not dupes else f"FAIL {dupes}")

print()
print("=" * 78)
print("QA 2 - HTML COVERAGE (every URL + on-hub topic represented)")
print("=" * 78)
grand_missing = []
for k in TARGETS:
    p = parsed[k]
    urls = p["featured"] + p["textlinks"]
    miss_u = [t for t in urls if t.lower() not in blob.lower()]
    miss_o = [t for t in p["onhub"] if t.lower() not in blob.lower()]
    miss_h = [t for t in p["h2s"] if t.lower() not in blob.lower()]
    miss_g = [t for t in p["gov"] if t.lower() not in blob.lower()]
    grand_missing += miss_u + miss_o + miss_h + miss_g
    print(f"\n  [{k}]")
    print(f"    HTML child links (F+T) : {len(urls):>3}  covered: {len(urls)-len(miss_u):>3}"
          f"{'  MISSING: '+str(miss_u) if miss_u else '  PASS'}")
    print(f"    HTML on-hub topics     : {len(p['onhub']):>3}  covered: {len(p['onhub'])-len(miss_o):>3}"
          f"{'  MISSING: '+str(miss_o) if miss_o else '  PASS'}")
    print(f"    HTML H2 section names  : {len(p['h2s']):>3}  covered: {len(p['h2s'])-len(miss_h):>3}"
          f"{'  MISSING: '+str(miss_h) if miss_h else '  PASS'}")
    print(f"    HTML governance items  : {len(p['gov']):>3}  covered: {len(p['gov'])-len(miss_g):>3}"
          f"{'  MISSING: '+str(miss_g) if miss_g else '  PASS'}")

print()
print("=" * 78)
print("QA 3 - COUNT RECONCILIATION vs HTML HEADER PILLS")
print("=" * 78)
print(f"  {'hub':<32}{'URLs H/G':<12}{'ChildLnk H/G':<15}{'OnHub H/G':<13}{'NotSurf H':<10}")
ok = True
for k in TARGETS:
    p = parsed[k]
    c = p["counts"]
    hub_urls = c["Separate URLs"]
    hub_links = c["Child Links"]
    hub_onhub = c["No-URL Topics"]
    hub_ns = c["Not Surfaced"]
    # generated: count rows scoped to this hub
    tag = {"divorce-mediation": "Divorce Mediation",
           "child-support-mediation": "Child Support Mediation",
           "child-custody-mediation": "Child Custody Mediation",
           "spousal-maintenance-mediation": "Spousal Maintenance Mediation"}[k]
    hubrow = [r for r in genrows if r[2].startswith("Core Service Hub Page") and tag in r[2]]
    pagerows = [r for r in genrows
                if ("Featured H3 Card" in r[2] or "Supporting Text Link" in r[2])
                and f"({tag} - " in r[2]]
    modrows = [r for r in genrows if r[2].startswith("Hub Section Module") and tag.split()[0] in r[2]]
    g_urls = len(hubrow) + len(pagerows)
    g_links = len(pagerows)
    # on-hub topics enumerated inside module descriptions
    g_onhub = sum(len(re.findall(r"[A-Z]", "")) for _ in [])  # placeholder
    onhub_found = sum(1 for t in p["onhub"] if t.lower() in blob.lower())
    row_ok = (g_urls == hub_urls and g_links == hub_links and onhub_found == hub_onhub)
    ok &= row_ok
    print(f"  {tag:<32}{str(hub_urls)+'/'+str(g_urls):<12}"
          f"{str(hub_links)+'/'+str(g_links):<15}"
          f"{str(hub_onhub)+'/'+str(onhub_found):<13}{hub_ns:<10}"
          f"{'PASS' if row_ok else 'FAIL'}")
    print(f"    -> H2 modules: HTML {len(p['h2s'])} / generated {len(modrows)}"
          f"  {'PASS' if len(p['h2s'])==len(modrows) else 'FAIL'}")

print()
print("=" * 78)
print("QA 4 - URL PATHS VALIDATED AGAINST V4 ARCHITECTURE CSV")
print("=" * 78)
arch = list(csv.reader(open(ARCH, encoding="utf-8", errors="replace")))
ahdr = arch[8]
iurl, ipage = ahdr.index("URL Path"), ahdr.index("Page Name")
archurls = set()
for r in arch[9:]:
    if len(r) > iurl and r[iurl].startswith("/"):
        archurls.add(r[iurl].strip())
genurls = set(re.findall(r"URL: (/[a-z0-9\-/]+/)", " ".join(r[3] for r in genrows)))
bad = sorted(u for u in genurls if u not in archurls)
print(f"  distinct URLs in generated plan : {len(genurls)}")
print(f"  not found in V4 architecture    : {'PASS (none)' if not bad else 'FAIL'}")
for b in bad:
    print("     ", b)

print()
print("=" * 78)
print("QA 5 - HOURS")
print("=" * 78)
MONTHS = EXPECT_HDR[5:]
tot = {m: 0.0 for m in MONTHS}
for r in genrows:
    for i, m in enumerate(MONTHS):
        if r[5 + i]:
            tot[m] += float(r[5 + i])
existing = {"July": 53.5, "Aug": 44.5, "Sep": 19, "Oct": 26, "Nov": 20, "Dec": 20, "Jan": 20, "Beyond": 0}
print(f"  {'month':<9}{'existing':<10}{'new':<8}{'combined':<10}")
for m in MONTHS:
    print(f"  {m:<9}{existing[m]:<10}{tot[m]:<8}{existing[m]+tot[m]:<10}")
print(f"  {'TOTAL':<9}{sum(existing.values()):<10}{sum(tot.values()):<8}{sum(existing.values())+sum(tot.values()):<10}")
sched = [existing[m] + tot[m] for m in ["Sep", "Oct", "Nov", "Dec", "Jan"]]
print(f"  Sep-Jan monthly load range: {min(sched)} - {max(sched)} hrs "
      f"({'PASS - within 45-55 capacity band' if 45 <= min(sched) and max(sched) <= 55 else 'FAIL'})")

zero = [r[2].replace("\n", " ") for r in genrows if not any(r[5:])]
print(f"\n  rows with no hours (intentional - already funded elsewhere): {len(zero)}")
for z in zero:
    print("     ", z)

print()
print("=" * 78)
print("OVERALL:", "PASS - no missing items" if not grand_missing and not bad and not dupes
      else f"REVIEW - {len(grand_missing)} missing / {len(bad)} bad urls / {len(dupes)} dupes")
print("=" * 78)
