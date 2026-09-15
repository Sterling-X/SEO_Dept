#!/usr/bin/env python3
"""Dedupe the Ireland Law 60-day lead pull.

Reads  analysis/ireland_leads_60d.csv        (283 raw records)
Writes analysis/ireland_leads_60d_clean.csv  (one row per real lead)

Three passes, in order:
  1. Drop firm-internal system records (WordPress form notifications addressed to the
     firm's own inbox -- these are not leads).
  2. Collapse records sharing a normalized phone number. The phone integration writes a
     second row per inbound call using the caller-ID string, so the same call appears
     twice: once named, once as "WIRELESS CALLER" / "OGLESBY IL" / etc.
  3. Collapse records sharing an email address (catches same-person rows that carry no
     phone at all, e.g. "Griggs, Christi @ San Antonio" vs "Christi Griggs Inquiry").

Deliberately NOT deduped: records whose *name* is a caller-ID placeholder
("SAN ANTONIO TX", "WIRELESS CALLER", "Unknown Caller", "AVVO Unknown"). These share a
name but have distinct phone numbers, so they are distinct leads whose caller name was
never captured. Collapsing on name would destroy real leads.
"""
import csv
import re
import sys
from collections import defaultdict

SRC = "analysis/ireland_leads_60d.csv"
DST = "analysis/ireland_leads_60d_clean.csv"

# Firm's own address -- WordPress notification mail, not a lead.
INTERNAL_EMAILS = {"wordpress@irelandfirm.com"}
INTERNAL_NAMES = {"michael ireland & associates"}


def digits(s):
    return re.sub(r"\D", "", s or "")


def full_name(r):
    return f"{r['first_name']} {r['last_name']}".strip()


def is_placeholder_name(r):
    n = full_name(r)
    return "Unknown" in n or (n and n.replace(" ", "").replace(",", "").isupper())


def richness(r):
    """Higher = keep this row as the surviving record."""
    return (
        int(r["furthest_stage"][0]),          # furthest funnel stage wins
        1 if r["email"].strip() else 0,       # then a real email
        1 if r["phone"].strip() else 0,       # then a phone
        0 if is_placeholder_name(r) else 1,   # then a human-looking name
    )


def merge(group, fields):
    """Keep the richest row, backfilling blank fields from its siblings."""
    best = max(group, key=richness)
    if len(group) > 1:
        for f in fields:
            if not best[f].strip():
                for other in group:
                    if other[f].strip():
                        best[f] = other[f]
                        break
        note = f"[merged {len(group)} source records]"
        best["conversion_notes"] = (
            f"{best['conversion_notes']} {note}".strip() if best["conversion_notes"] else note
        )
    return best


def collapse(rows, keyfn, fields):
    """Group rows by keyfn; rows with an empty key pass through untouched."""
    groups, passthrough = defaultdict(list), []
    for r in rows:
        k = keyfn(r)
        (groups[k] if k else passthrough).append(r)
    merged = [merge(g, fields) for g in groups.values()]
    removed = sum(len(g) - 1 for g in groups.values() if len(g) > 1)
    return merged + passthrough, removed


def main():
    with open(SRC, newline="") as fh:
        rows = list(csv.DictReader(fh))
    fields = list(rows[0].keys())
    start = len(rows)

    # Pass 1 -- drop firm-internal system records.
    kept, internal = [], []
    for r in rows:
        if (r["email"].strip().lower() in INTERNAL_EMAILS
                or full_name(r).lower() in INTERNAL_NAMES):
            internal.append(r)
        else:
            kept.append(r)

    # Pass 2 -- collapse on phone. Pass 3 -- collapse on email.
    kept, by_phone = collapse(kept, lambda r: digits(r["phone"]), fields)
    kept, by_email = collapse(kept, lambda r: r["email"].strip().lower(), fields)

    kept.sort(key=lambda r: r["lead_created_at"], reverse=True)

    with open(DST, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(kept)

    print(f"  raw records                      {start:4d}")
    print(f"  - firm-internal system records  -{len(internal):4d}")
    print(f"  - duplicate caller-ID rows      -{by_phone:4d}  (same phone)")
    print(f"  - duplicate rows                -{by_email:4d}  (same email, no phone)")
    print(f"  = clean leads                    {len(kept):4d}")
    assert start - len(internal) - by_phone - by_email == len(kept), "count mismatch"

    # Verify nothing duplicated survives.
    for label, fn in (("phone", lambda r: digits(r["phone"])),
                      ("email", lambda r: r["email"].strip().lower())):
        seen = defaultdict(int)
        for r in kept:
            k = fn(r)
            if k:
                seen[k] += 1
        dupes = sum(1 for v in seen.values() if v > 1)
        print(f"  residual duplicate {label}s: {dupes}")
        if dupes:
            sys.exit(f"ERROR: {dupes} residual {label} duplicates")


if __name__ == "__main__":
    main()
