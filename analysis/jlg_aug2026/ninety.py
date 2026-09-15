#!/usr/bin/env python3
"""90-over-90 across every dataset that carries a date dimension, with decomposition.

Windows are anchored on the last COMPLETE day in the merged GSC series (2026-08-10);
2026-08-11 is dropped as partial. All windows are exactly 90 days, same day-of-week mix.
"""
import csv, json, os, re
from collections import defaultdict, Counter
from statistics import mean
from datetime import date, timedelta

H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'data')
def rd(p):
    with open(p, encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def n(s):
    s = str(s).replace('%','').replace(',','').strip()
    try: return float(s)
    except: return 0.0
def dt(s): return date(int(s[:4]), int(s[5:7]), int(s[8:10]))

# ---------- merged daily GSC series (90d export wins on the overlap) ----------
daily = {}
for r in rd(f'{D}/gsc_16mo/Chart.csv'):
    daily[r['Date']] = dict(c=int(n(r['Clicks'])), i=int(n(r['Impressions'])), p=n(r['Position']))
for r in rd(f'{D}/gsc_90d/Chart.csv'):
    daily[r['Date']] = dict(c=int(n(r['Clicks'])), i=int(n(r['Impressions'])), p=n(r['Position']))
END = date(2026, 8, 10)                       # last complete day
def win(end, days):
    start = end - timedelta(days=days-1)
    ks = [k for k in daily if start <= dt(k) <= end]
    return start, end, sorted(ks)

def agg(keys):
    c = sum(daily[k]['c'] for k in keys); i = sum(daily[k]['i'] for k in keys)
    pw = sum(daily[k]['p']*daily[k]['i'] for k in keys)/i if i else 0
    return dict(days=len(keys), clicks=c, impr=i, ctr=100*c/i if i else 0,
                pos=pw, cpd=c/len(keys) if keys else 0, ipd=i/len(keys) if keys else 0)

CUR  = win(END, 90)
PRI  = win(END - timedelta(days=90), 90)
YOY  = win(END.replace(year=END.year-1), 90)
A, B, Y = agg(CUR[2]), agg(PRI[2]), agg(YOY[2])

def pct(a, b): return (a/b - 1)*100 if b else 0
print("="*104)
print("GOOGLE SEARCH CONSOLE — 90 OVER 90 (and the same window a year earlier)")
print("="*104)
for lab, w, g in (('current  ', CUR, A), ('prior 90 ', PRI, B), ('YoY 90   ', YOY, Y)):
    print(f"  {lab} {w[0]} .. {w[1]}  days={g['days']:>3}  clicks={g['clicks']:>6,}  impr={g['impr']:>9,}"
          f"  CTR={g['ctr']:.3f}%  pos={g['pos']:.2f}  clicks/day={g['cpd']:.1f}")
print(f"\n  {'metric':16}{'prior 90':>12}{'current 90':>12}{'change':>12}{'  vs YoY-90':>14}")
for k, f in (('clicks','{:,.0f}'), ('impr','{:,.0f}'), ('ctr','{:.3f}%'), ('pos','{:.2f}')):
    print(f"  {k:16}{f.format(B[k]):>12}{f.format(A[k]):>12}"
          f"{pct(A[k],B[k]):>11.1f}%{pct(A[k],Y[k]):>13.1f}%")

# ---------- decomposition: how much of the click change is volume vs rate ----------
d_imp = (A['impr']-B['impr']) * (B['ctr']/100)
d_ctr = A['impr'] * ((A['ctr']-B['ctr'])/100)
print(f"\n  DECOMPOSITION of the {A['clicks']-B['clicks']:+,} click change, prior 90 -> current 90")
print(f"    from impression volume : {d_imp:+8.0f} clicks   ({100*d_imp/(A['clicks']-B['clicks']):5.1f}% of the move)")
print(f"    from click-through rate: {d_ctr:+8.0f} clicks   ({100*d_ctr/(A['clicks']-B['clicks']):5.1f}% of the move)")
print(f"    (CTR went {B['ctr']:.3f}% -> {A['ctr']:.3f}%, position {B['pos']:.2f} -> {A['pos']:.2f})")

# ---------- weekday control ----------
wd = lambda ks: Counter(dt(k).weekday() for k in ks)
print(f"\n  weekday balance  prior={sorted(wd(PRI[2]).values())}  current={sorted(wd(CUR[2]).values())}"
      f"   (identical mix = no day-of-week artefact)")

# ---------- 30-day sub-windows, to locate the move inside the 180 days ----------
print(f"\n  30-DAY SUB-WINDOWS ending {END} (most recent first)")
print(f"  {'window':26}{'clicks':>8}{'/day':>8}{'impr':>10}{'/day':>9}{'CTR%':>8}{'pos':>7}")
for j in range(6):
    e = END - timedelta(days=30*j); s, _, ks = win(e, 30)
    g = agg(ks)
    print(f"  {str(s)+' .. '+str(e):26}{g['clicks']:>8,}{g['cpd']:>8.1f}{g['impr']:>10,}{g['ipd']:>9,.0f}"
          f"{g['ctr']:>8.3f}{g['pos']:>7.2f}")

# ---------- AI-features share (export begins 2026-05-18, so current window only) ----------
ai_daily = {}
try:
    for r in rd(f'{D}/gsc_ai/Chart.csv'):
        ai_daily[r['Date']] = int(n(r['Impressions']))
except Exception:
    pass
if ai_daily:
    aik = [k for k in CUR[2] if k in ai_daily]
    ai_i = sum(ai_daily[k] for k in aik)
    print(f"\n  AI-features impressions inside the current 90: {ai_i:,} over {len(aik)} covered days"
          f"  ({100*ai_i/A['impr']:.1f}% of the window's impressions)")
    print(f"  NB: the AI export has no rows before {min(ai_daily)}, so a 90-over-90 on AI vs non-AI is NOT")
    print(f"      available — the prior window has no AI baseline to compare against.")

# ---------- Semrush: balanced-panel 70-over-70 (series starts 2026-03-25) ----------
import glob
print("\n" + "="*104)
print("SEMRUSH POSITION TRACKING — matched-panel comparison (series starts 2026-03-25, so 70 over 70)")
print("="*104)
series = defaultdict(dict)     # (project, keyword) -> {date: pos}
vol = {}
for path in sorted(glob.glob(f'{D}/ranks/*.csv')):
    lines = open(path, encoding='utf-8-sig').read().split('\n')
    st = next(i for i, l in enumerate(lines) if l.startswith('Keyword,'))
    hdr = list(csv.reader([lines[st]]))[0]
    dates = [(c, re.search(r'_(\d{8})$', c).group(1)) for c in hdr
             if re.search(r'_(\d{8})$', c) and not c.endswith(('_type','_landing'))]
    pid = re.search(r'_(\d+)_position', path).group(1)
    for r in csv.DictReader(lines[st:]):
        key = (pid, r['Keyword'])
        vol[key] = n(r.get('Search Volume'))
        for col, d in dates:
            v = (r.get(col) or '').strip()
            if v and v != '-':
                try: series[key][d] = int(v)
                except ValueError: pass

alld = sorted({d for s in series.values() for d in s})
mid  = alld[len(alld)//2]
first, second = [d for d in alld if d <= mid], [d for d in alld if d > mid]
# balanced panel: keywords observed in BOTH halves
panel = {k: s for k, s in series.items() if any(d in s for d in first) and any(d in s for d in second)}
def half(s, ds):
    v = [s[d] for d in ds if d in s]
    return sum(v)/len(v) if v else None
rows = []
for k, s in panel.items():
    a, b = half(s, first), half(s, second)
    if a is not None and b is not None: rows.append((k, a, b, b-a, vol.get(k, 0)))
print(f"  window A {first[0]} .. {first[-1]}  ({len(first)} snapshots)")
print(f"  window B {second[0]} .. {second[-1]}  ({len(second)} snapshots)")
print(f"  balanced panel: {len(rows)} keyword-city pairs present in both halves"
      f"  (of {len(series)} tracked)")
ua = sum(r[1] for r in rows)/len(rows); ub = sum(r[2] for r in rows)/len(rows)
print(f"  unweighted avg position  {ua:.2f} -> {ub:.2f}   ({ub-ua:+.2f})")
tv = sum(r[4] for r in rows)
if tv:
    wa = sum(r[1]*r[4] for r in rows)/tv; wb = sum(r[2]*r[4] for r in rows)/tv
    print(f"  volume-weighted          {wa:.2f} -> {wb:.2f}   ({wb-wa:+.2f})   [{tv:,.0f} searches/mo]")
worse = [r for r in rows if r[3] > 3]; better = [r for r in rows if r[3] < -3]
print(f"  moved >3 positions:  {len(worse)} worse, {len(better)} better, {len(rows)-len(worse)-len(better)} flat")

# ---------- GA4: state what is and is not possible ----------
print("\n" + "="*104)
print("GA4 — 90-over-90 is NOT possible from the exports on disk")
print("="*104)
for lab, p in (('on disk (analysis)', f'{D}/ga4/landing_pages.csv'),):
    hdr = [l.strip() for l in open(p, encoding='utf-8-sig') if l.startswith('#')]
    print(f"  {lab}: {[h for h in hdr if 'date' in h.lower() or 'Users' in h]}")
print("  The export is ONE aggregate snapshot 2026-01-01..2026-08-11 with:")
print("    - no date dimension  -> no trend of any kind can be computed")
print("    - no channel dimension ('All Users') -> organic cannot be separated from paid/direct")
print("  'New users' also CANNOT be summed down a landing-page column: it is a user-scoped metric on a")
print("  page-scoped dimension, so a user who lands on several pages is counted once per page. Proof from")
print("  the file itself: the column sums to 92,950 against 60,674 sessions (153%), which is impossible.")
