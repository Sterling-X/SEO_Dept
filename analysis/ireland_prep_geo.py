#!/usr/bin/env python3
"""Simplify Texas county + state geometry for embedding in a standalone HTML map.

Ramer-Douglas-Peucker on every ring, then coordinate rounding.

The source (plotly geojson-counties-fips) is ALREADY heavily simplified -- 254 Texas
counties carry only ~18 vertices each, Harris County just 64. So the tolerance here is
deliberately tiny: rounding to 3 decimals (~0.07px at the rendered scale) is already
visually lossless, and anything more aggressive visibly flattens county shapes. County
lines must stay legible -- that is the point of the map.

The state outline is DERIVED from the counties by edge dissolve rather than taken from a
separate state file, so the border lands exactly on the county mosaic.

Input   /tmp/us-counties.json  (plotly geojson-counties-fips, all 3221 US counties)
Output  analysis/ireland_geo.json
"""
import json

TOL = 0.001
PREC = 3
DST = "analysis/ireland_geo.json"


def perp2(px, py, ax, ay, bx, by):
    """Squared perpendicular distance from p to segment ab."""
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return (px - ax) ** 2 + (py - ay) ** 2
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    cx, cy = ax + t * dx, ay + t * dy
    return (px - cx) ** 2 + (py - cy) ** 2


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
        ax, ay = pts[i]
        bx, by = pts[j]
        for k in range(i + 1, j):
            d = perp2(pts[k][0], pts[k][1], ax, ay, bx, by)
            if d > worst:
                worst, wi = d, k
        if worst > tol2:
            keep[wi] = True
            stack.append((i, wi))
            stack.append((wi, j))
    return [p for p, k in zip(pts, keep) if k]


def clean_ring(ring):
    out = rdp(ring, TOL * TOL)
    out = [[round(x, PREC), round(y, PREC)] for x, y in out]
    # drop consecutive duplicates introduced by rounding
    ded = [out[0]]
    for p in out[1:]:
        if p != ded[-1]:
            ded.append(p)
    if len(ded) < 4:
        return None
    if ded[0] != ded[-1]:
        ded.append(ded[0])
    return ded if len(ded) >= 4 else None


def clean_geom(geom):
    t = geom["type"]
    if t == "Polygon":
        rings = [r for r in (clean_ring(r) for r in geom["coordinates"]) if r]
        return {"type": "Polygon", "coordinates": rings} if rings else None
    if t == "MultiPolygon":
        polys = []
        for poly in geom["coordinates"]:
            rings = [r for r in (clean_ring(r) for r in poly) if r]
            if rings:
                polys.append(rings)
        return {"type": "MultiPolygon", "coordinates": polys} if polys else None
    raise ValueError(t)


def rings_of(geom):
    if geom["type"] == "Polygon":
        return list(geom["coordinates"])
    return [r for poly in geom["coordinates"] for r in poly]


def dissolve(features):
    """Derive the state outline as the union of county polygons.

    Uses the fact that the Census county file is topologically consistent: an edge shared
    by two counties appears exactly twice, so the edges appearing once are precisely the
    state boundary. Stitch those into closed rings.

    Done on the RAW counties, before simplification -- RDP runs per ring independently, so
    simplifying first would make neighbours' shared edges diverge and the matching fail.
    Deriving the outline this way (rather than from a separate state file) guarantees the
    border sits exactly on the county mosaic instead of a few pixels off it.
    """
    def key(p):
        return (round(p[0], 6), round(p[1], 6))

    count = {}
    for f in features:
        for ring in rings_of(f["geometry"]):
            for a, b in zip(ring, ring[1:]):
                ka, kb = key(a), key(b)
                if ka == kb:
                    continue
                count[(ka, kb) if ka < kb else (kb, ka)] = \
                    count.get((ka, kb) if ka < kb else (kb, ka), 0) + 1

    adj = {}
    for (ka, kb), n in count.items():
        if n != 1:
            continue
        adj.setdefault(ka, []).append(kb)
        adj.setdefault(kb, []).append(ka)

    rings, seen = [], set()
    for start in list(adj):
        if start in seen:
            continue
        ring, cur, prev = [start], start, None
        seen.add(start)
        while True:
            nxt = next((n for n in adj.get(cur, []) if n != prev and n not in seen), None)
            if nxt is None:
                # close the ring if we can get back to the start
                if start in adj.get(cur, []):
                    ring.append(start)
                break
            ring.append(nxt)
            seen.add(nxt)
            prev, cur = cur, nxt
        if len(ring) >= 4:
            rings.append([list(p) for p in ring])

    rings.sort(key=len, reverse=True)
    return rings


def main():
    with open("/tmp/us-counties.json") as fh:
        counties = json.load(fh)

    tx_raw = [f for f in counties["features"] if f["properties"].get("STATE") == "48"]
    outline = dissolve(tx_raw)
    print(f"dissolved outline rings: {len(outline)} "
          f"(largest {len(outline[0])} pts, smallest {len(outline[-1])})")

    polys = []
    for ring in outline:
        r = clean_ring(ring)
        if r:
            polys.append([r])
    state = {"type": "Feature", "properties": {"name": "Texas"},
             "geometry": {"type": "MultiPolygon", "coordinates": polys}}

    feats = []
    for f in counties["features"]:
        if f["properties"].get("STATE") != "48":
            continue
        g = clean_geom(f["geometry"])
        if g:
            feats.append({"type": "Feature",
                          "properties": {"name": f["properties"]["NAME"]},
                          "geometry": g})

    out = {
        "counties": {"type": "FeatureCollection", "features": feats},
        "state": state,
    }
    with open(DST, "w") as fh:
        json.dump(out, fh, separators=(",", ":"))

    import os
    n_before = sum(len(r) for f in counties["features"]
                   if f["properties"].get("STATE") == "48"
                   for r in (f["geometry"]["coordinates"] if f["geometry"]["type"] == "Polygon"
                             else [x for p in f["geometry"]["coordinates"] for x in p]))
    n_after = sum(len(r) for f in feats
                  for r in (f["geometry"]["coordinates"] if f["geometry"]["type"] == "Polygon"
                            else [x for p in f["geometry"]["coordinates"] for x in p]))
    print(f"counties: {len(feats)}")
    print(f"vertices: {n_before} -> {n_after}  ({n_after/n_before*100:.1f}%)")
    print(f"output:   {os.path.getsize(DST)/1024:.0f} KB")


if __name__ == "__main__":
    main()
