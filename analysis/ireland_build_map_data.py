#!/usr/bin/env python3
"""Build the geographic dataset for the Ireland Law lead-origin map.

Ireland Law's lead records carry NO zip, city, county, or state field (see
ireland_leads_60d_NOTES.md). The only geographic signal available is the telephone
area code, plus a caller-ID city string that the phone system writes into the name
field on some records. So every location here is an AREA-CODE REGION, not a point --
roughly county-group precision, and the map must say so.

Reads  analysis/ireland_leads_60d_clean.csv
Writes analysis/ireland_map_data.json
"""
import csv
import json
import re
from collections import defaultdict

SRC = "analysis/ireland_leads_60d_clean.csv"
DST = "analysis/ireland_map_data.json"

# Area code -> (region label, lat, lon, state). Texas codes are plotted; the region
# point is the area code's principal city, or the firm's office city where the firm
# has one inside that area code.
TX = {
    "210": ("San Antonio metro", 29.4241, -98.4936),
    "726": ("San Antonio metro", 29.4241, -98.4936),          # 210 overlay
    "361": ("Victoria / Coastal Bend", 28.8053, -97.0036),
    "830": ("Hill Country / New Braunfels", 29.7008, -98.1245),
    "512": ("Austin", 30.2672, -97.7431),
    "737": ("Austin", 30.2672, -97.7431),                     # 512 overlay
    "713": ("Houston metro", 29.7604, -95.3698),
    "832": ("Houston metro", 29.7604, -95.3698),              # 713 overlay
    "281": ("Houston metro", 29.7604, -95.3698),
    "346": ("Houston metro", 29.7604, -95.3698),
    "956": ("Rio Grande Valley", 26.2034, -98.2300),
    "254": ("Waco / Killeen", 31.5493, -97.1467),
    "915": ("El Paso", 31.7619, -106.4850),
    "903": ("Tyler / Northeast Texas", 32.3513, -95.3011),
    "979": ("Bryan / College Station", 30.6280, -96.3344),
    "936": ("Conroe / Huntsville", 30.3119, -95.4561),
    "469": ("Dallas / Fort Worth", 32.7767, -96.7970),
    "972": ("Dallas / Fort Worth", 32.7767, -96.7970),
    "214": ("Dallas / Fort Worth", 32.7767, -96.7970),
    "817": ("Dallas / Fort Worth", 32.7767, -96.7970),
    "806": ("Lubbock / Amarillo", 33.5779, -101.8552),
    "325": ("Abilene / San Angelo", 32.4487, -99.7331),
    "432": ("Midland / Odessa", 31.9974, -102.0779),
    "409": ("Beaumont / Galveston", 30.0802, -94.1266),
    "940": ("Wichita Falls / Denton", 33.9137, -98.4934),
}

# Out-of-state area codes seen in the data, for the summary table only (not plotted).
OOS = {
    "206": "WA", "360": "WA", "262": "WI", "484": "PA", "267": "PA", "215": "PA",
    "910": "NC", "704": "NC", "919": "NC", "504": "LA", "337": "LA", "318": "LA",
    "815": "IL", "773": "IL", "505": "NM", "301": "MD", "339": "MA", "813": "FL",
    "386": "FL", "407": "FL", "305": "FL", "209": "CA", "323": "CA", "310": "CA",
    "916": "CA", "909": "CA", "502": "KY", "307": "WY", "937": "OH", "513": "OH",
    "970": "CO", "303": "CO", "928": "AZ", "812": "IN", "856": "NJ", "785": "KS",
    "620": "KS", "402": "NE", "931": "TN", "401": "RI", "808": "HI",
}

# Offices, geocoded via Nominatim.
OFFICES = [
    {"name": "San Antonio", "addr": "9901 I-10 W, Ste 215", "zip": "78230",
     "lat": 29.5338207, "lon": -98.5619100},
    {"name": "New Braunfels", "addr": "170 E San Antonio St", "zip": "78130",
     "lat": 29.7036445, "lon": -98.1236057},
    {"name": "Victoria", "addr": "101 W Goodwin Ave, Ste 1025", "zip": "77901",
     "lat": 28.8006686, "lon": -97.0059772},
]

STATE_RE = re.compile(
    r"\b(TX|IL|CA|NY|FL|OH|OK|LA|NM|AZ|CO|WA|GA|NV|MO|AR|KS|TN|NC|MI|PA|IN|WI|MN|"
    r"IA|MS|AL|KY|SC|VA|MD|NJ|MA|OR|UT|NE|ID|WV|NH|ME|MT|ND|SD|WY|VT|RI|DE|CT|HI|AK)\b")


def area_code(phone):
    d = re.sub(r"\D", "", phone or "")
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return d[:3] if len(d) == 10 else None


def main():
    with open(SRC, newline="") as fh:
        rows = list(csv.DictReader(fh))

    regions = defaultdict(lambda: {"t": 0, "c": 0, "q": 0, "codes": set()})
    oos_states = defaultdict(lambda: {"t": 0, "c": 0})
    no_phone = {"t": 0, "c": 0}
    unmapped = defaultdict(int)
    callerid_cities = defaultdict(int)

    for r in rows:
        consult = 1 if r["consult_scheduled_date"].strip() else 0
        qual = 1 if r["qualified_date"].strip() else 0
        ac = area_code(r["phone"])

        name = f"{r['first_name']} {r['last_name']}".strip()
        m = STATE_RE.search(name)
        if m:
            callerid_cities[name.upper()] += 1

        if ac is None:
            no_phone["t"] += 1
            no_phone["c"] += consult
        elif ac in TX:
            label, lat, lon = TX[ac]
            g = regions[label]
            g["t"] += 1
            g["c"] += consult
            g["q"] += qual
            g["lat"], g["lon"] = lat, lon
            g["codes"].add(ac)
        elif ac in OOS:
            st = OOS[ac]
            oos_states[st]["t"] += 1
            oos_states[st]["c"] += consult
        else:
            unmapped[ac] += 1

    pts = sorted(
        ({"n": k, "lat": v["lat"], "lon": v["lon"], "t": v["t"], "c": v["c"],
          "q": v["q"], "codes": sorted(v["codes"])} for k, v in regions.items()),
        key=lambda d: -d["t"])

    tx_total = sum(p["t"] for p in pts)
    tx_consult = sum(p["c"] for p in pts)
    oos_total = sum(v["t"] for v in oos_states.values())
    oos_consult = sum(v["c"] for v in oos_states.values())

    out = {
        "meta": {
            "client": "Michael Ireland & Associates, PLLC",
            "period": "June 14 to August 13, 2026",
            "data_span": "June 15 to August 10, 2026",
            "snapshot": "August 13, 2026",
            "total_leads": len(rows),
            "tx_leads": tx_total,
            "tx_consults": tx_consult,
            "oos_leads": oos_total,
            "oos_consults": oos_consult,
            "no_phone": no_phone["t"],
            "regions": len(pts),
            "hired_tracked": False,
        },
        "points": pts,
        "oos": sorted(({"st": k, "t": v["t"], "c": v["c"]} for k, v in oos_states.items()),
                      key=lambda d: (-d["t"], d["st"])),
        "offices": OFFICES,
        "callerid_cities": sorted(({"n": k, "t": v} for k, v in callerid_cities.items()),
                                  key=lambda d: -d["t"]),
    }

    with open(DST, "w") as fh:
        json.dump(out, fh, indent=1)

    print(f"leads {len(rows)}  TX {tx_total}  out-of-state {oos_total}  no-phone {no_phone['t']}")
    print(f"unmapped area codes: {dict(unmapped) or 'none'}")
    assert tx_total + oos_total + no_phone["t"] + sum(unmapped.values()) == len(rows)
    print(f"\n{'region':32s} {'codes':16s} {'leads':>6s} {'consults':>9s} {'rate':>7s}")
    for p in pts:
        rate = p["c"] / p["t"] * 100
        print(f"  {p['n']:30s} {'/'.join(p['codes']):16s} {p['t']:6d} {p['c']:9d} {rate:6.1f}%")
    print(f"\nout-of-state: {oos_total} leads, {oos_consult} consults, "
          f"{len(out['oos'])} states")
    print(f"TX consult rate {tx_consult/tx_total*100:.1f}%  |  "
          f"OOS consult rate {oos_consult/oos_total*100:.1f}%")


if __name__ == "__main__":
    main()
