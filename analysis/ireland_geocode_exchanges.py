#!/usr/bin/env python3
"""Resolve each lead's phone exchange (NPA-NXX) to a rate-center city + coordinates.

Why: Ireland's lead records carry no zip/city/county/state, so the Johnson-style
city-level origin map has no address field to plot. The next best real signal is the
telephone exchange -- the first six digits -- which maps to a telco "rate center," a
named city with published coordinates. That yields individual city origins (San Antonio,
Seguin, Boerne, Victoria, Uvalde ...) instead of a handful of area-code blobs.

Caveat carried through to the sheet: a rate center is where the NUMBER was assigned, not
where the person is. For landlines that is effectively their town; for mobiles it is where
the line was activated, so a Texan who kept an old number lands on the old city. This is
an approximation of the same class as the example's "county-level only" tier, and is
labelled as such.

Source: localcallingguide.com XML prefix API (free, public). Results cached to disk so
re-runs cost nothing.
"""
import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from collections import Counter

SRC = "analysis/ireland_leads_60d_clean.csv"
CACHE = "analysis/exchange_cache.json"
UA = "RocketClicks-SEO-Analysis/1.0 (cshea@rocketclicks.com)"
FIELDS = ("rc", "region", "rc-lat", "rc-lon")


def digits(phone):
    d = re.sub(r"\D", "", phone or "")
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return d if len(d) == 10 else None


def lookup(npa, nxx):
    url = f"https://localcallingguide.com/xmlprefix.php?npa={npa}&nxx={nxx}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        x = r.read().decode("utf-8", "replace")
    i = x.find("<prefixdata>")
    if i < 0:
        return None
    block = x[i:x.find("</prefixdata>")]
    out = {}
    for f in FIELDS:
        m = re.search(rf"<{f}>(.*?)</{f}>", block, re.S)
        out[f] = (m.group(1).strip() if m else "")
    if not out["rc"] or not out["rc-lat"]:
        return None
    try:
        return {"city": out["rc"], "state": out["region"],
                "lat": float(out["rc-lat"]), "lon": float(out["rc-lon"])}
    except ValueError:
        return None


def main():
    with open(SRC, newline="") as fh:
        rows = list(csv.DictReader(fh))

    prefixes = Counter()
    for r in rows:
        d = digits(r["phone"])
        if d:
            prefixes[d[:6]] += 1

    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE) as fh:
            cache = json.load(fh)

    todo = [p for p in prefixes if p not in cache]
    print(f"{len(prefixes)} unique exchanges, {len(cache)} cached, {len(todo)} to fetch",
          flush=True)

    ok = fail = 0
    for i, p in enumerate(sorted(todo), 1):
        try:
            cache[p] = lookup(p[:3], p[3:])
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            print(f"  [{i}/{len(todo)}] {p} ERROR {e}", flush=True)
            cache[p] = None
        if cache[p]:
            ok += 1
        else:
            fail += 1
        if i % 25 == 0 or i == len(todo):
            print(f"  [{i}/{len(todo)}] resolved={ok} unresolved={fail}", flush=True)
            with open(CACHE, "w") as fh:
                json.dump(cache, fh, indent=0, sort_keys=True)
        time.sleep(0.25)

    with open(CACHE, "w") as fh:
        json.dump(cache, fh, indent=0, sort_keys=True)

    resolved = sum(prefixes[p] for p in prefixes if cache.get(p))
    total = sum(prefixes.values())
    print(f"\nleads with a resolved city: {resolved}/{total} "
          f"({resolved/total*100:.1f}% of phoned leads)")
    cities = Counter()
    for p, n in prefixes.items():
        c = cache.get(p)
        if c:
            cities[(c["city"], c["state"])] += n
    print(f"distinct cities: {len(cities)}")
    for (city, st), n in cities.most_common(20):
        print(f"  {n:4d}  {city}, {st}")


if __name__ == "__main__":
    sys.exit(main())
