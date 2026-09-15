#!/usr/bin/env python3
"""Build the city-level Texas dataset for the Ireland lead-origin map.

Mirrors the structure of the reference (Johnson) sheet: one origin point per named place,
with a two-tier precision flag, so the map shows individual cities rather than a few
area-code blobs.

  tier "c"  city      -- phone exchange (NPA-NXX) resolved to a named rate-center city
  tier "k"  approx.   -- exchange unresolved; falls back to the area-code region centroid

Texas only, per instruction: out-of-state leads are dropped entirely rather than tabled.
Window is exactly the trailing 60 days, 2026-06-15 through 2026-08-13 inclusive.

Reads  analysis/ireland_leads_60d_clean.csv
       analysis/exchange_cache.json
Writes analysis/ireland_city_data.json
"""
import csv
import json
import re
from collections import defaultdict

SRC = "analysis/ireland_leads_60d_clean.csv"
CACHE = "analysis/exchange_cache.json"
DST = "analysis/ireland_city_data.json"

WIN_FROM, WIN_TO = "2026-06-15", "2026-08-13"   # 60 days inclusive

# Fallback region centroids for Texas area codes whose exchange did not resolve.
TX_FALLBACK = {
    "210": ("San Antonio area", 29.4241, -98.4936), "726": ("San Antonio area", 29.4241, -98.4936),
    "361": ("Coastal Bend area", 28.8053, -97.0036),
    "830": ("Hill Country area", 29.7008, -98.1245),
    "512": ("Austin area", 30.2672, -97.7431), "737": ("Austin area", 30.2672, -97.7431),
    "713": ("Houston area", 29.7604, -95.3698), "832": ("Houston area", 29.7604, -95.3698),
    "281": ("Houston area", 29.7604, -95.3698), "346": ("Houston area", 29.7604, -95.3698),
    "956": ("Rio Grande Valley area", 26.2034, -98.2300),
    "254": ("Waco / Killeen area", 31.5493, -97.1467),
    "915": ("El Paso area", 31.7619, -106.4850),
    "903": ("Northeast Texas area", 32.3513, -95.3011),
    "979": ("Bryan / College Station area", 30.6280, -96.3344),
    "936": ("Conroe area", 30.3119, -95.4561),
    "469": ("Dallas area", 32.7767, -96.7970), "972": ("Dallas area", 32.7767, -96.7970),
    "214": ("Dallas area", 32.7767, -96.7970), "817": ("Fort Worth area", 32.7555, -97.3308),
    "806": ("Lubbock area", 33.5779, -101.8552),
    "325": ("Abilene area", 32.4487, -99.7331),
    "432": ("Midland area", 31.9974, -102.0779),
    "409": ("Beaumont area", 30.0802, -94.1266),
    "940": ("Wichita Falls area", 33.9137, -98.4934),
}

OFFICES = [
    {"name": "San Antonio", "addr": "9901 I-10 W, Ste 215", "zip": "78230",
     "county": "Bexar", "lat": 29.5338207, "lon": -98.5619100},
    {"name": "New Braunfels", "addr": "170 E San Antonio St", "zip": "78130",
     "county": "Comal", "lat": 29.7036445, "lon": -98.1236057},
    {"name": "Victoria", "addr": "101 W Goodwin Ave, Ste 1025", "zip": "77901",
     "county": "Victoria", "lat": 28.8006686, "lon": -97.0059772},
]


def digits(phone):
    d = re.sub(r"\D", "", phone or "")
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return d if len(d) == 10 else None


# Rate-center names carry telco billing-zone suffixes that are not places: "Houston
# Suburban" is Houston, "Seguin EMS" is Seguin. Strip them so one city is one point.
SUFFIX_RE = re.compile(r"\s+(Suburban|EMS|EACS|Zone\s*\d+|Zone\s*[A-Z])\s*$", re.I)


def norm_city(name):
    prev = None
    while prev != name:
        prev = name
        name = SUFFIX_RE.sub("", name).strip()
    return name


def main():
    with open(SRC, newline="") as fh:
        rows = list(csv.DictReader(fh))
    with open(CACHE) as fh:
        cache = json.load(fh)

    total_all = len(rows)
    rows = [r for r in rows if WIN_FROM <= r["lead_created_date"] <= WIN_TO]
    in_window = len(rows)

    places = defaultdict(lambda: {"t": 0, "c": 0, "tier": "c", "lat": 0.0, "lon": 0.0})
    drop_oos = drop_nophone = drop_unknown = 0

    for r in rows:
        consult = 1 if r["consult_scheduled_date"].strip() else 0
        d = digits(r["phone"])
        if not d:
            drop_nophone += 1
            continue
        hit = cache.get(d[:6])
        if hit:
            if hit["state"] != "TX":
                drop_oos += 1
                continue
            key = norm_city(hit["city"])
            p = places[key]
            p["tier"] = "c"
            p["lat"], p["lon"] = hit["lat"], hit["lon"]
        else:
            fb = TX_FALLBACK.get(d[:3])
            if not fb:
                drop_oos += 1          # unresolved AND not a Texas area code
                continue
            key = fb[0]
            p = places[key]
            p["tier"] = "k"
            p["lat"], p["lon"] = fb[1], fb[2]
        p["t"] += 1
        p["c"] += consult

    pts = sorted(({"n": k, "k": v["tier"] == "k", "lat": v["lat"], "lon": v["lon"],
                   "t": v["t"], "c": v["c"]} for k, v in places.items()),
                 key=lambda d: (-d["t"], d["n"]))

    plotted = sum(p["t"] for p in pts)
    consults = sum(p["c"] for p in pts)
    approx = sum(p["t"] for p in pts if p["k"])

    out = {
        "meta": {
            "client": "Michael Ireland & Associates, PLLC",
            "period": "June 15 to August 13, 2026",
            "window_days": 60,
            "snapshot": "August 13, 2026",
            "total_leads": total_all,
            "in_window": in_window,
            "plotted": plotted,
            "consults": consults,
            "origin_points": len(pts),
            "cities": sum(1 for p in pts if not p["k"]),
            "approx_points": sum(1 for p in pts if p["k"]),
            "approx_leads": approx,
            "dropped_oos": drop_oos,
            "dropped_nophone": drop_nophone,
        },
        "points": pts,
        "offices": OFFICES,
    }
    with open(DST, "w") as fh:
        json.dump(out, fh, indent=1)

    m = out["meta"]
    print(f"window {WIN_FROM}..{WIN_TO} ({m['window_days']} days)")
    print(f"  leads in window      {in_window} of {total_all}")
    print(f"  plotted (Texas)      {plotted}")
    print(f"  consults             {consults} ({consults/plotted*100:.1f}%)")
    print(f"  origin points        {len(pts)}  ({m['cities']} city, {m['approx_points']} approx)")
    print(f"  dropped out-of-state {drop_oos}")
    print(f"  dropped no phone     {drop_nophone}")
    assert plotted + drop_oos + drop_nophone == in_window, "count mismatch"
    print(f"\n  {'origin':26s} {'tier':6s} {'leads':>6s} {'cons':>5s}")
    for p in pts[:28]:
        print(f"  {p['n']:26s} {'approx' if p['k'] else 'city':6s} {p['t']:6d} {p['c']:5d}")
    if len(pts) > 28:
        print(f"  ... and {len(pts)-28} more")


if __name__ == "__main__":
    main()
