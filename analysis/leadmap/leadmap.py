#!/usr/bin/env python3
"""Lead-origin map pipeline. One client, one date window, one self-contained HTML sheet.

    python3 analysis/leadmap/leadmap.py --client "Michael Ireland" --days 60

Stages, each cached so re-runs are cheap:
  1 resolve    client name/id -> SterlingX_Client_ID
  2 probe      what this client actually tracks (hired? lead-level zip? date coverage?)
  3 pull       lead-level rows from BigQuery for the window
  4 dedupe     phone/email collisions + firm-internal notification records
  5 geocode    phone exchange (NPA-NXX) -> rate-center city + coordinates
  6 geometry   county polygons for the client's home state, outline dissolved from them
  7 build      aggregate to origin points, pick the conversion metric
  8 render     inject into template.html

Design rule: PROBE, DON'T ASSUME. Clients differ in what they track. 18 of them carry
lead-level zip in <dataset>.call_data; 9 record Funded Agreement (hired). A client with
neither gets exchange-derived cities and a consults metric; a client with hired data gets
a real hire rate. Stage 2 decides, and stage 8 labels the sheet accordingly, so the output
never implies precision or outcomes the source data cannot support.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
PROJECT = "sterlingx-insights"
FACT = f"`{PROJECT}.all_clients_offline_conversion.all_firms_offline_conversion`"
UA = "RocketClicks-SEO-Analysis/1.0 (cshea@rocketclicks.com)"

# Conversion_Status values, shallowest -> deepest.
FUNNEL = ["New Leads", "Qualified Potential Clients", "Consults Scheduled",
          "Consults Complete", "Funded Agreement"]
HIRED = "Funded Agreement"
# Words in a firm name that also appear in other firms' dataset names. Excluded from the
# dataset-name probe so "Fanash Family Law" does not match arizona_family_law.
GENERIC_NAME_WORDS = {"family", "legal", "group", "associates", "attorneys", "attorney",
                      "lawyers", "lawyer", "firm", "office", "offices", "pllc", "llc",
                      "llp", "mediation", "divorce", "partners", "counsel", "solutions"}

STATE_FIPS = {
 "AL":"01","AK":"02","AZ":"04","AR":"05","CA":"06","CO":"08","CT":"09","DE":"10","DC":"11",
 "FL":"12","GA":"13","HI":"15","ID":"16","IL":"17","IN":"18","IA":"19","KS":"20","KY":"21",
 "LA":"22","ME":"23","MD":"24","MA":"25","MI":"26","MN":"27","MS":"28","MO":"29","MT":"30",
 "NE":"31","NV":"32","NH":"33","NJ":"34","NM":"35","NY":"36","NC":"37","ND":"38","OH":"39",
 "OK":"40","OR":"41","PA":"42","RI":"44","SC":"45","SD":"46","TN":"47","TX":"48","UT":"49",
 "VT":"50","VA":"51","WA":"53","WV":"54","WI":"55","WY":"56"}
STATE_NAME = {
 "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado",
 "CT":"Connecticut","DE":"Delaware","DC":"District of Columbia","FL":"Florida","GA":"Georgia",
 "HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas",
 "KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts",
 "MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana",
 "NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico",
 "NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma",
 "OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
 "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont",
 "VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}

COUNTY_URL = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"

INTERNAL_LOCALPARTS = {"wordpress", "no-reply", "noreply", "donotreply", "admin", "webmaster"}


def log(*a):
    print(*a, flush=True)


def die(msg):
    sys.exit(f"ERROR: {msg}")


def ensure_cache():
    os.makedirs(CACHE, exist_ok=True)


# ---------------------------------------------------------------- BigQuery helpers
def bq(sql, max_rows=100000):
    """Run a query, return list of dicts. Shells out to bq so no python client is needed."""
    cmd = ["bq", "query", "--use_legacy_sql=false", "--format=csv",
           f"--max_rows={max_rows}", sql]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        err = p.stderr.strip()
        if "Reauthentication" in err or "credentials" in err.lower():
            die("BigQuery auth expired. Run:  gcloud auth login")
        die(f"bq failed:\n{err[:1200]}")
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    if len(lines) < 2:
        return []
    return list(csv.DictReader(lines))


# ---------------------------------------------------------------- 1. resolve client
def resolve_client(q):
    rows = bq(f"SELECT DISTINCT SterlingX_Client_ID AS id, SterlingX_Client_Name AS name "
              f"FROM {FACT} WHERE SterlingX_Client_Name IS NOT NULL")
    if not rows:
        die("no clients found in the fact table")
    ql = q.strip().lower()
    exact = [r for r in rows if r["id"].lower() == ql or r["name"].lower() == ql]
    if exact:
        return exact[0]
    # token-subset match: "michael ireland" -> "Michael Ireland & Associates"
    toks = [t for t in re.split(r"[^a-z0-9]+", ql) if t]
    cand = [r for r in rows if all(t in r["name"].lower() for t in toks)]
    if len(cand) == 1:
        return cand[0]
    if len(cand) > 1:
        die("ambiguous client %r — candidates: %s" % (q, ", ".join(c["name"] for c in cand)))
    die("no client matches %r. Known clients:\n  %s"
        % (q, "\n  ".join(sorted(r["name"] for r in rows))))


# ---------------------------------------------------------------- 2. probe capabilities
def probe(cid, name, zip_dataset=None):
    """Establish what this client tracks before pulling anything."""
    caps = {}
    rows = bq(f"""
      SELECT Conversion_Status AS st, COUNT(*) AS n,
             MIN(SUBSTR(Conversion_Event_Date,1,10)) AS first_d,
             MAX(SUBSTR(Conversion_Event_Date,1,10)) AS last_d
      FROM {FACT} WHERE SterlingX_Client_ID='{cid}' GROUP BY 1""")
    caps["stages"] = {r["st"]: int(r["n"]) for r in rows}
    caps["hired_tracked"] = caps["stages"].get(HIRED, 0) > 0
    caps["last_event"] = max((r["last_d"] for r in rows), default=None)
    caps["first_event"] = min((r["first_d"] for r in rows), default=None)

    # Deepest stage this client actually records -> the conversion metric for the map.
    tracked = [s for s in FUNNEL if caps["stages"].get(s, 0) > 0 and s != "New Leads"]
    caps["metric_status"] = tracked[-1] if tracked else None

    # Does a per-client dataset carry lead-level zip? (18 clients do; it is a better
    # geocode than the phone exchange, and worth surfacing even if unused here.)
    # Match only on the client's distinctive name words. Generic words such as
    # "family" match other firms' datasets (Fanash Family Law matched
    # arizona_family_law on 2026-09-23), and a zip column that exists but is empty is
    # not a zip source, so each candidate is checked for populated rows before it is
    # reported on the sheet.
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    words = [w for w in slug.split("_") if len(w) > 3 and w not in GENERIC_NAME_WORDS]
    if zip_dataset:
        like = f"table_schema='{zip_dataset}'"
    else:
        like = " OR ".join(f"LOWER(table_schema) LIKE '%{w}%'" for w in words) or "FALSE"
    zrows = bq(f"""
      SELECT table_schema, table_name, column_name
      FROM `region-us`.INFORMATION_SCHEMA.COLUMNS
      WHERE table_name='call_data'
        AND (LOWER(column_name)='zip_code' OR LOWER(column_name)='postal_code')
        AND ({like})""")
    log(f"      zip probe: {'dataset ' + zip_dataset if zip_dataset else 'name words ' + (', '.join(words) or 'none')}"
        f" -> candidates {[z['table_schema'] for z in zrows] or 'none'}"
        + ("" if zrows or zip_dataset else " (a misspelled dataset name will not match; use --zip-dataset)"))
    caps["zip_source"] = None
    for z in zrows:
        ds, col = z["table_schema"], z["column_name"]
        filled = bq(f"""
          SELECT COUNTIF(TRIM(CAST({col} AS STRING)) != '') AS n
          FROM `{ds}.call_data`""")
        n = int(filled[0]["n"]) if filled else 0
        if n > 0:
            caps["zip_source"] = {"dataset": ds, "column": col, "filled": n}
            break
        log(f"      {ds}.call_data.{col} exists but is empty; ignored as a zip source")
    return caps


# ---------------------------------------------------------------- 3. pull
def pull(cid, frm, to):
    return bq(f"""
      WITH cohort AS (
        SELECT * FROM {FACT}
        WHERE SterlingX_Client_ID='{cid}'
          AND SAFE.PARSE_DATE('%Y-%m-%d', SUBSTR(Origin_Date_Created,1,10))
              BETWEEN DATE('{frm}') AND DATE('{to}')
      )
      SELECT
        Origin_Lead_ID AS lead_id,
        MIN(SUBSTR(Origin_Date_Created,1,19)) AS created_at,
        SAFE.PARSE_DATE('%Y-%m-%d', SUBSTR(MIN(Origin_Date_Created),1,10)) AS created_date,
        COALESCE(ANY_VALUE(NULLIF(Origin_First_Name,'')), ANY_VALUE(NULLIF(CRM_First_Name,''))) AS first_name,
        COALESCE(ANY_VALUE(NULLIF(Origin_Last_Name,'')),  ANY_VALUE(NULLIF(CRM_Last_Name,'')))  AS last_name,
        COALESCE(ANY_VALUE(NULLIF(Origin_Email_Name,'')), ANY_VALUE(NULLIF(CRM_Email,'')))      AS email,
        COALESCE(ANY_VALUE(NULLIF(Origin_Phone_Number,'')), ANY_VALUE(NULLIF(CRM_Phone_Number,''))) AS phone,
        ANY_VALUE(Origin_Platform) AS platform,
        COALESCE(ANY_VALUE(NULLIF(Origin_Marketing_UTM_Campaign,'')),
                 ANY_VALUE(NULLIF(CRM_Marketing_UTM_Campaign,''))) AS utm_campaign,
        ANY_VALUE(NULLIF(Origin_GCLID,'')) AS gclid,
        STRING_AGG(DISTINCT Conversion_Status, '|' ORDER BY Conversion_Status) AS statuses
      FROM cohort GROUP BY Origin_Lead_ID
      ORDER BY created_at DESC""")


# ---------------------------------------------------------------- 4. dedupe
def digits(phone):
    d = re.sub(r"\D", "", phone or "")
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return d if len(d) == 10 else None


def is_internal(r, client_name):
    """Firm's own notification mail / records named after the firm are not leads."""
    em = (r.get("email") or "").strip().lower()
    if em:
        local, _, dom = em.partition("@")
        if local in INTERNAL_LOCALPARTS:
            return True
    nm = f"{r.get('first_name','')} {r.get('last_name','')}".strip().lower()
    cn = client_name.lower()
    if nm and (nm == cn or (len(nm) > 8 and nm in cn)):
        return True
    return False


def placeholder_name(r):
    nm = f"{r.get('first_name','')} {r.get('last_name','')}".strip()
    return ("unknown" in nm.lower()
            or (bool(nm) and nm.replace(" ", "").replace(",", "").isupper()))


def dedupe(rows, client_name, metric_status):
    def deep(r):
        return 1 if metric_status and metric_status in (r.get("statuses") or "") else 0

    def richness(r):
        return (deep(r), 1 if (r.get("email") or "").strip() else 0,
                1 if (r.get("phone") or "").strip() else 0,
                0 if placeholder_name(r) else 1)

    def collapse(rs, keyfn):
        groups, through, removed = defaultdict(list), [], 0
        for r in rs:
            k = keyfn(r)
            (groups[k] if k else through).append(r)
        out = []
        for g in groups.values():
            best = max(g, key=richness)
            if len(g) > 1:
                removed += len(g) - 1
                for f in list(best):
                    if not (best.get(f) or "").strip():
                        for o in g:
                            if (o.get(f) or "").strip():
                                best[f] = o[f]
                                break
                # keep the deepest funnel status reached by any sibling
                best["statuses"] = "|".join(sorted(
                    {s for o in g for s in (o.get("statuses") or "").split("|") if s}))
            out.append(best)
        return out + through, removed

    start = len(rows)
    kept = [r for r in rows if not is_internal(r, client_name)]
    n_internal = start - len(kept)
    kept, n_phone = collapse(kept, lambda r: digits(r.get("phone")))
    kept, n_email = collapse(kept, lambda r: (r.get("email") or "").strip().lower())
    kept.sort(key=lambda r: r.get("created_at") or "", reverse=True)
    return kept, {"start": start, "internal": n_internal, "phone": n_phone, "email": n_email,
                  "kept": len(kept)}


# ---------------------------------------------------------------- 5. geocode exchanges
def save_cache(path, cache):
    """Merge-then-atomic-write. Two clients geocoding at once share this file; a plain
    dump would let the slower run clobber the faster one's new entries."""
    if os.path.exists(path):
        try:
            on_disk = json.load(open(path))
            for k, v in on_disk.items():
                cache.setdefault(k, v)
        except (ValueError, OSError):
            pass
    tmp = path + f".tmp{os.getpid()}"
    json.dump(cache, open(tmp, "w"), indent=0, sort_keys=True)
    os.replace(tmp, path)


def geocode(rows):
    """NPA-NXX -> rate-center city. Cached across clients and runs."""
    ensure_cache()
    path = os.path.join(CACHE, "exchange_cache.json")
    cache = json.load(open(path)) if os.path.exists(path) else {}
    pre = {d[:6] for d in (digits(r.get("phone")) for r in rows) if d}
    todo = sorted(pre - set(cache))
    if todo:
        log(f"  geocoding {len(todo)} new exchanges ({len(pre)-len(todo)} cached)")
    for i, p in enumerate(todo, 1):
        url = f"https://localcallingguide.com/xmlprefix.php?npa={p[:3]}&nxx={p[3:]}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                x = r.read().decode("utf-8", "replace")
            j = x.find("<prefixdata>")
            hit = None
            if j >= 0:
                b = x[j:x.find("</prefixdata>")]
                g = lambda f: (re.search(rf"<{f}>(.*?)</{f}>", b, re.S) or [None, ""])[1].strip()
                if g("rc") and g("rc-lat"):
                    hit = {"city": g("rc"), "state": g("region"),
                           "lat": float(g("rc-lat")), "lon": float(g("rc-lon"))}
            cache[p] = hit
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            cache[p] = None
        if i % 25 == 0 or i == len(todo):
            save_cache(path, cache)
            log(f"    {i}/{len(todo)}")
        time.sleep(0.25)
    save_cache(path, cache)
    return cache


# Telco billing-zone decorations that are not place names: "Colorado Springs-Main" is
# Colorado Springs, "Houston Suburban" is Houston, "Seguin EMS" is Seguin.
SUFFIX_RE = re.compile(r"([\s-]+(Suburban|EMS|EACS|Main|Metro|Zone\s*\d+|Zone\s*[A-Z]))\s*$", re.I)


ZONE_RE = re.compile(r"^(.+?)[\s-]+(Central|North|South|East|West)$", re.I)


def norm_city(n):
    prev = None
    while prev != n:
        prev = n
        n = SUFFIX_RE.sub("", n).strip()
    return n


# ---------------------------------------------------------------- 6. geometry
def perp2(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return (px - ax) ** 2 + (py - ay) ** 2
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return (px - (ax + t * dx)) ** 2 + (py - (ay + t * dy)) ** 2


def rdp(pts, tol2):
    if len(pts) < 3:
        return pts[:]
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        worst, wi = -1.0, -1
        for k2 in range(i + 1, j):
            d = perp2(pts[k2][0], pts[k2][1], pts[i][0], pts[i][1], pts[j][0], pts[j][1])
            if d > worst:
                worst, wi = d, k2
        if worst > tol2:
            keep[wi] = True
            stack += [(i, wi), (wi, j)]
    return [p for p, kp in zip(pts, keep) if kp]


def clean_ring(ring, tol=0.001, prec=3):
    out = [[round(x, prec), round(y, prec)] for x, y in rdp(ring, tol * tol)]
    ded = [out[0]]
    for p in out[1:]:
        if p != ded[-1]:
            ded.append(p)
    if len(ded) < 4:
        return None
    if ded[0] != ded[-1]:
        ded.append(ded[0])
    return ded if len(ded) >= 4 else None


def clean_geom(g):
    if g["type"] == "Polygon":
        rs = [r for r in (clean_ring(r) for r in g["coordinates"]) if r]
        return {"type": "Polygon", "coordinates": rs} if rs else None
    ps = []
    for poly in g["coordinates"]:
        rs = [r for r in (clean_ring(r) for r in poly) if r]
        if rs:
            ps.append(rs)
    return {"type": "MultiPolygon", "coordinates": ps} if ps else None


def dissolve(features):
    """State outline = county edges that appear exactly once. Run on RAW geometry: RDP is
    per-ring, so simplifying first would make neighbours' shared edges diverge."""
    def rings(g):
        return list(g["coordinates"]) if g["type"] == "Polygon" else \
               [r for p in g["coordinates"] for r in p]
    cnt = {}
    for f in features:
        for ring in rings(f["geometry"]):
            for a, b in zip(ring, ring[1:]):
                ka = (round(a[0], 6), round(a[1], 6))
                kb = (round(b[0], 6), round(b[1], 6))
                if ka == kb:
                    continue
                key = (ka, kb) if ka < kb else (kb, ka)
                cnt[key] = cnt.get(key, 0) + 1
    adj = {}
    for (ka, kb), n in cnt.items():
        if n == 1:
            adj.setdefault(ka, []).append(kb)
            adj.setdefault(kb, []).append(ka)
    out, seen = [], set()
    for start in list(adj):
        if start in seen:
            continue
        ring, cur, prev = [start], start, None
        seen.add(start)
        while True:
            nxt = next((n for n in adj.get(cur, []) if n != prev and n not in seen), None)
            if nxt is None:
                if start in adj.get(cur, []):
                    ring.append(start)
                break
            ring.append(nxt)
            seen.add(nxt)
            prev, cur = cur, nxt
        if len(ring) >= 4:
            out.append([list(p) for p in ring])
    out.sort(key=len, reverse=True)
    return out


def geometry(state_ab):
    ensure_cache()
    src = os.path.join(CACHE, "us-counties.json")
    if not os.path.exists(src):
        log("  downloading US county geometry (once)")
        req = urllib.request.Request(COUNTY_URL, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=180) as r, open(src, "wb") as fh:
            fh.write(r.read())
    allc = json.load(open(src))
    fips = STATE_FIPS[state_ab]
    raw = [f for f in allc["features"] if f["properties"].get("STATE") == fips]
    if not raw:
        die(f"no counties for state {state_ab}")
    feats = []
    for f in raw:
        g = clean_geom(f["geometry"])
        if g:
            feats.append({"type": "Feature",
                          "properties": {"name": f["properties"]["NAME"]}, "geometry": g})
    polys = [[r] for r in (clean_ring(x) for x in dissolve(raw)) if r]
    return {"counties": {"type": "FeatureCollection", "features": feats},
            "state": {"type": "Feature", "properties": {"name": STATE_NAME[state_ab]},
                      "geometry": {"type": "MultiPolygon", "coordinates": polys}}}


# ---------------------------------------------------------------- 7. build
def build(rows, cache, caps, client, frm, to, days, offices, force_state=None):
    metric = caps["metric_status"]
    places = defaultdict(lambda: {"t": 0, "c": 0, "lat": 0.0, "lon": 0.0})
    st_count = Counter()
    resolved = []
    n_nophone = 0
    for r in rows:
        d = digits(r.get("phone"))
        if not d:
            n_nophone += 1
            continue
        hit = cache.get(d[:6])
        if not hit:
            continue
        st_count[hit["state"]] += 1
        resolved.append((r, hit))

    if not st_count:
        die("no lead could be geocoded; cannot pick a home state")
    home = force_state or st_count.most_common(1)[0][0]

    n_oos = 0
    n_oos_conv = 0   # out-of-state exchanges that still reached the metric: an out-of-state
                     # number is not an out-of-state client (Fanash: 36 of 405 hired, 2026-09-23)
    for r, hit in resolved:
        if hit["state"] != home:
            n_oos += 1
            if metric and metric in (r.get("statuses") or ""):
                n_oos_conv += 1
            continue
        p = places[norm_city(hit["city"])]
        p["t"] += 1
        p["lat"], p["lon"] = hit["lat"], hit["lon"]
        if metric and metric in (r.get("statuses") or ""):
            p["c"] += 1

    # Telco billing zones come in families: "Tampa Central", "Tampa North", "Tampa East",
    # "Tampa West" and "Tampa South" are one city split by the carrier, not five cities
    # (Fanash Family Law, 2026-09-23). Merge a directional family only when at least two
    # variants share the base name or the base is already a point, so a lone rate center
    # whose name merely ends in a direction is left alone. The merged point keeps the
    # base city's coordinates when it exists, otherwise a lead-weighted mean.
    fam = defaultdict(list)
    for k in list(places):
        m = ZONE_RE.match(k)
        if m:
            fam[m.group(1)].append(k)
    for base, ks in fam.items():
        if len(ks) < 2 and base not in places:
            continue
        had_base = base in places
        tgt = places[base]
        wlat, wlon, wt = tgt["lat"] * tgt["t"], tgt["lon"] * tgt["t"], tgt["t"]
        for k in ks:
            v = places.pop(k)
            tgt["t"] += v["t"]
            tgt["c"] += v["c"]
            wlat, wlon, wt = wlat + v["lat"] * v["t"], wlon + v["lon"] * v["t"], wt + v["t"]
        if not had_base and wt:
            tgt["lat"], tgt["lon"] = wlat / wt, wlon / wt
        log(f"      merged {len(ks)} {base} billing zones into {base} ({tgt['t']} leads)")

    pts = sorted(({"n": k, "k": False, "lat": v["lat"], "lon": v["lon"], "t": v["t"], "c": v["c"]}
                  for k, v in places.items()), key=lambda d: (-d["t"], d["n"]))
    plotted = sum(p["t"] for p in pts)

    # Origin platform families over the whole in-window cohort ("Clio Grow+call" -> "Clio Grow").
    # A source that starts mid-window or converts at a very different rate can dominate a
    # month-over-month change or a blended rate (Fanash: Manual Intake began 2026-01, 46% of
    # leads, 2.4% hired vs Clio Grow 14.8%; seo-reviewer finding, 2026-09-23).
    fams = defaultdict(lambda: {"t": 0, "c": 0, "first": None})
    for r in rows:
        fam = (r.get("platform") or "unknown").split("+")[0].strip() or "unknown"
        f = fams[fam]
        f["t"] += 1
        if metric and metric in (r.get("statuses") or ""):
            f["c"] += 1
        mo = str(r.get("created_date") or "")[:7]
        if mo and (f["first"] is None or mo < f["first"]):
            f["first"] = mo
    platforms = sorted(({"name": k, **v} for k, v in fams.items()), key=lambda x: -x["t"])
    convs = sum(p["c"] for p in pts)
    n_unres = len(rows) - n_nophone - len(resolved)

    metric_label = {"Funded Agreement": "Hired",
                    "Consults Complete": "Consults completed",
                    "Consults Scheduled": "Consults booked",
                    "Qualified Potential Clients": "Qualified"}.get(metric, "Conversions")

    return {
        "meta": {
            "client": client["name"], "client_id": client["id"],
            "state_ab": home, "state": STATE_NAME[home],
            "period": (f"{fmt(frm)}, {frm[:4]} to {fmt(to)}, {to[:4]}" if frm[:4] != to[:4]
                       else f"{fmt(frm)} to {fmt(to)}, {to[:4]}"), "window_days": days,
            "date_from": frm, "date_to": to,
            "snapshot": fmt_today(),
            "in_window": len(rows), "plotted": plotted, "conversions": convs,
            "origin_points": len(pts), "cities": len(pts),
            "dropped_oos": n_oos, "dropped_oos_conv": n_oos_conv,
            "dropped_nophone": n_nophone, "dropped_unresolved": n_unres,
            "metric_status": metric, "metric_label": metric_label,
            "hired_tracked": caps["hired_tracked"],
            "zip_source": caps["zip_source"],
            "platforms": platforms,
            "last_event": caps["last_event"],
            "stages": caps["stages"],
        },
        "points": pts,
        "offices": offices,
    }


def fmt(d):
    y, m, dd = d.split("-")
    return f"{dt.date(int(y), int(m), int(dd)):%B %-d}"


def fmt_today():
    return f"{dt.date.today():%B %-d, %Y}"


# ---------------------------------------------------------------- 8. render
def render(data, geo, out_html):
    tpl = open(os.path.join(HERE, "template.html")).read()
    if "__GEO__" not in tpl or "__DATA__" not in tpl:
        die("template.html is missing __GEO__ / __DATA__ placeholders")
    html = (tpl.replace("__GEO__", json.dumps(geo, separators=(",", ":")))
               .replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    open(out_html, "w").write(html)
    return len(html)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Build a client lead-origin map.")
    ap.add_argument("--client", required=True, help="client name or SterlingX_Client_ID")
    ap.add_argument("--days", type=int, help="trailing window length, e.g. 60")
    ap.add_argument("--from", dest="frm", help="YYYY-MM-DD (overrides --days)")
    ap.add_argument("--to", dest="to", help="YYYY-MM-DD (defaults to today)")
    ap.add_argument("--state", help="force home state, 2-letter (default: modal state)")
    ap.add_argument("--offices", help="JSON file: [{name,addr,zip,county,lat,lon}]")
    ap.add_argument("--zip-dataset", dest="zip_dataset",
                    help="dataset whose call_data carries lead-level zip, for when the name probe "
                         "cannot find it (e.g. the misspelled fanishe_family_law)")
    ap.add_argument("--outdir", default="analysis", help="output directory")
    a = ap.parse_args()

    to = a.to or f"{dt.date.today():%Y-%m-%d}"
    if a.frm:
        frm = a.frm
        days = (dt.date.fromisoformat(to) - dt.date.fromisoformat(frm)).days + 1
    elif a.days:
        days = a.days
        frm = f"{dt.date.fromisoformat(to) - dt.timedelta(days=days - 1):%Y-%m-%d}"
    else:
        die("give --days or --from")

    log(f"[1/8] resolving client {a.client!r}")
    client = resolve_client(a.client)
    log(f"      {client['name']}  ({client['id']})")

    log("[2/8] probing what this client tracks")
    caps = probe(client["id"], client["name"], a.zip_dataset)
    log(f"      stages: {', '.join(f'{k}={v}' for k, v in caps['stages'].items()) or 'none'}")
    log(f"      hired tracked: {caps['hired_tracked']}  |  metric: {caps['metric_status']}")
    log(f"      lead-level zip: {caps['zip_source'] or 'none'}")
    log(f"      data coverage: {caps['first_event']} .. {caps['last_event']}")
    if caps["last_event"] and caps["last_event"] < frm:
        die(f"this client's data stops at {caps['last_event']}, before the window {frm}..{to}")

    log(f"[3/8] pulling {frm} .. {to} ({days} days)")
    rows = pull(client["id"], frm, to)
    log(f"      {len(rows)} raw lead records")
    if not rows:
        die("no leads in that window")

    log("[4/8] deduplicating")
    rows, dd = dedupe(rows, client["name"], caps["metric_status"])
    log(f"      {dd['start']} raw -{dd['internal']} internal -{dd['phone']} phone "
        f"-{dd['email']} email = {dd['kept']} leads")

    log("[5/8] geocoding phone exchanges")
    cache = geocode(rows)

    offices = json.load(open(a.offices)) if a.offices else []
    log("[6/8] building origin points")
    data = build(rows, cache, caps, client, frm, to, days, offices, a.state)
    m = data["meta"]
    log(f"      home state {m['state']} ({m['state_ab']}) — {m['plotted']} leads, "
        f"{m['origin_points']} cities, {m['conversions']} {m['metric_label'].lower()}")
    log(f"      excluded: {m['dropped_oos']} out-of-state, {m['dropped_nophone']} no phone, "
        f"{m['dropped_unresolved']} unresolved exchange")

    log(f"[7/8] county geometry for {m['state']}")
    geo = geometry(m["state_ab"])
    log(f"      {len(geo['counties']['features'])} counties")

    os.makedirs(a.outdir, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", client["name"].lower()).strip("-")
    # Window length is part of the name: a 60-day and a 90-day run ending the same
    # day would otherwise write to identical paths and silently clobber each other.
    base = os.path.join(a.outdir, f"{slug}-lead-origin-map-{days}d-{to}")
    json.dump(data, open(base + ".json", "w"), indent=1)
    with open(base + ".csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    log(f"[8/8] rendering")
    n = render(data, geo, base + ".html")
    log(f"\nwrote {base}.html  ({n//1024} KB)")
    log(f"      {base}.csv   ({len(rows)} leads)")
    log(f"      {base}.json")
    if not caps["hired_tracked"]:
        log("\nNOTE: this client has no Funded Agreement records, so the sheet shows "
            f"'{m['metric_label']}' and Hired reads 'Not tracked'. That is a data gap, "
            "not a zero.")
    if caps["zip_source"]:
        log(f"NOTE: {caps['zip_source']['dataset']}.call_data carries "
            f"{caps['zip_source']['column']} — lead-level zip exists for this client and "
            "would geocode more precisely than the phone exchange used here.")


if __name__ == "__main__":
    main()
