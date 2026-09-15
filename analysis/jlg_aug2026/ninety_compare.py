#!/usr/bin/env python3
"""True 90-over-90 harness.

WHAT A REAL 90/90 NEEDS: two exports of the SAME dimension over two adjacent,
non-overlapping 90-day windows. Search Console's UI exports carry no date column
on the Pages / Queries / Devices / Countries tabs, so those tabs can only ever be
compared by pulling the export twice with the date filter set differently.

Current windows (anchored to the last complete day, 2026-08-10):
    CURRENT  2026-05-13 .. 2026-08-10
    PRIOR    2026-02-12 .. 2026-05-12

Drop a prior-window export into data/gsc_prior90/ and this script produces the
full page-, query-, device- and country-level 90/90 automatically. Until then it
reports exactly which comparisons are live and which are blocked, and falls back
to a clearly-labelled 'vs 16-month norm' cut that is NOT a 90/90.
"""
import csv, json, os, re, sys
from collections import defaultdict
from datetime import date, timedelta

H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'data')
PRIOR_DIR = os.path.join(D, 'gsc_prior90')
CUR_DIR   = os.path.join(D, 'gsc_90d')
SIXTEEN   = os.path.join(D, 'gsc_16mo')
DAYS16    = 487                     # span of the 16-month export

def rd(p):
    with open(p, encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def n(s):
    s = str(s).replace('%','').replace(',','').strip()
    try: return float(s)
    except: return 0.0
def norm(u):
    u = re.sub(r'^https?://(www\.)?johnsonlgroup\.com','',u)
    return u.split('?')[0].split('#')[0].rstrip('/') or '/'

END  = date(2026,8,10)
CUR_W = (END - timedelta(days=89), END)
PRI_W = (END - timedelta(days=179), END - timedelta(days=90))

def load_dim(path, keycol, keyfn=lambda x: x):
    """Sum duplicate rows — GSC lists www / non-www / ?utm variants separately."""
    o = defaultdict(lambda: {'clicks':0,'impr':0,'posw':0.0})
    if not os.path.exists(path): return None
    for r in rd(path):
        k = keyfn(r[keycol]); c = int(n(r.get('Clicks',0))); i = int(n(r.get('Impressions',0)))
        o[k]['clicks'] += c; o[k]['impr'] += i
        o[k]['posw'] += n(r.get('Position',0)) * i
    for v in o.values():
        v['pos'] = round(v['posw']/v['impr'],2) if v['impr'] else 0
        del v['posw']
    return dict(o)

DIMS = [
    ('Pages',    'Pages.csv',     'Top pages',      norm),
    ('Queries',  'Queries.csv',   'Top queries',    lambda x: x),
    ('Devices',  'Devices.csv',   'Device',         lambda x: x),
    ('Countries','Countries.csv', 'Country',        lambda x: x),
]

print("="*100)
print("90-OVER-90 HARNESS")
print(f"  CURRENT  {CUR_W[0]} .. {CUR_W[1]}")
print(f"  PRIOR    {PRI_W[0]} .. {PRI_W[1]}")
print("="*100)

have_prior = os.path.isdir(PRIOR_DIR) and any(
    os.path.exists(os.path.join(PRIOR_DIR, f)) for _,f,_,_ in DIMS)

print("\nAVAILABILITY")
print(f"  {'dimension':12}{'current 90':>14}{'prior 90':>12}{'true 90/90?':>14}")
status = {}
for name, fn, kc, kf in DIMS:
    c_ok = os.path.exists(os.path.join(CUR_DIR, fn))
    p_ok = os.path.exists(os.path.join(PRIOR_DIR, fn))
    status[name] = (c_ok, p_ok)
    print(f"  {name:12}{'yes' if c_ok else 'MISSING':>14}{'yes' if p_ok else 'MISSING':>12}"
          f"{('YES' if (c_ok and p_ok) else 'blocked'):>14}")
print(f"  {'Daily chart':12}{'yes':>14}{'yes':>12}{'YES':>14}   (Chart.csv carries dates — see ninety.py)")

if not have_prior:
    print(f"""
  BLOCKED. Three of the five comparisons need one more export each. To unblock:

    1. Search Console -> Performance -> Search results
       Set the date range to CUSTOM {PRI_W[0]} .. {PRI_W[1]}
       Export -> CSV, unzip into:  {PRIOR_DIR}/
       That single export unblocks Pages, Queries, Devices AND Countries at once.

    2. GA4 -> Reports -> Acquisition -> Traffic acquisition
       Dimension: Session primary channel group.  Metrics: sessions, new users, key events.
       Comparison ON: {CUR_W[0]}..{CUR_W[1]} vs {PRI_W[0]}..{PRI_W[1]}
       (Also re-pull Landing page with the same comparison if you want page-level GA4.)

    3. Semrush cannot do 90/90 — the campaigns only start 2026-03-25 (140 days total).
       70 over 70 is the arithmetic ceiling until 2026-09-21. It is already computed.
""")

# ---------------- live comparisons ----------------
out = {}
if have_prior:
    for name, fn, kc, kf in DIMS:
        cur = load_dim(os.path.join(CUR_DIR, fn), kc, kf)
        pri = load_dim(os.path.join(PRIOR_DIR, fn), kc, kf)
        if not (cur and pri): continue
        keys = set(cur) | set(pri)
        rows = []
        for k in keys:
            a = cur.get(k, {'clicks':0,'impr':0,'pos':0}); b = pri.get(k, {'clicks':0,'impr':0,'pos':0})
            rows.append(dict(k=k, c_now=a['clicks'], c_pri=b['clicks'], d_c=a['clicks']-b['clicks'],
                             i_now=a['impr'], i_pri=b['impr'], d_i=a['impr']-b['impr'],
                             p_now=a['pos'], p_pri=b['pos']))
        rows.sort(key=lambda r: r['d_c'])
        out[name] = rows
        print(f"\n{'='*100}\n{name.upper()} — 90 OVER 90\n{'='*100}")
        print(f"{'':52}{'clicks':>22}{'impressions':>24}")
        print(f"{'key':52}{'prior':>8}{'now':>7}{'chg':>7}{'prior':>10}{'now':>9}{'chg':>9}")
        for r in rows[:20]:
            print(f"{str(r['k'])[:50]:52}{r['c_pri']:>8}{r['c_now']:>7}{r['d_c']:>+7}"
                  f"{r['i_pri']:>10,}{r['i_now']:>9,}{r['d_i']:>+9,}")
        print("  ... biggest gainers:")
        for r in rows[-8:][::-1]:
            print(f"{str(r['k'])[:50]:52}{r['c_pri']:>8}{r['c_now']:>7}{r['d_c']:>+7}"
                  f"{r['i_pri']:>10,}{r['i_now']:>9,}{r['d_i']:>+9,}")

# ---------------- fallback: current 90 vs the 16-month norm ----------------
print(f"\n{'='*100}")
print("FALLBACK — current 90 days vs the same page's 16-month average rate")
print("NOT a 90-over-90. It answers 'what is running below its own historical norm', which is a")
print("weaker question, but it is the strongest cut available until the prior-90 export exists.")
print("="*100)
P16 = load_dim(os.path.join(SIXTEEN,'Pages.csv'), 'Top pages', norm)
P90 = load_dim(os.path.join(CUR_DIR,'Pages.csv'), 'Top pages', norm)
Q16 = load_dim(os.path.join(SIXTEEN,'Queries.csv'), 'Top queries')
Q90 = load_dim(os.path.join(CUR_DIR,'Queries.csv'), 'Top queries')

def norm_cut(cur, hist, label, keymin=40):
    rows = []
    for k, h in hist.items():
        exp = h['clicks']*90/DAYS16
        if exp < keymin*90/DAYS16: continue
        act = cur.get(k, {'clicks':0,'impr':0})['clicks']
        rows.append(dict(k=k, exp=round(exp,1), act=act, d=round(act-exp,1),
                         pct=round(100*(act/exp-1),1) if exp else 0,
                         i16=h['impr'], i90=cur.get(k,{'impr':0})['impr']))
    rows.sort(key=lambda r: r['d'])
    print(f"\n{label} — worst 15 vs their own 16-month rate  (expected = 16mo clicks x 90/487)")
    print(f"{'key':56}{'expected':>10}{'actual':>8}{'gap':>8}{'%':>8}")
    for r in rows[:15]:
        print(f"  {str(r['k'])[:54]:56}{r['exp']:>10.1f}{r['act']:>8}{r['d']:>+8.1f}{r['pct']:>7.0f}%")
    print(f"\n{label} — best 8")
    for r in rows[-8:][::-1]:
        print(f"  {str(r['k'])[:54]:56}{r['exp']:>10.1f}{r['act']:>8}{r['d']:>+8.1f}{r['pct']:>7.0f}%")
    return rows

pr = norm_cut(P90, P16, 'PAGES')
qr = norm_cut(Q90, Q16, 'QUERIES')
print("\n  CAVEAT: the 16-month window OVERLAPS the current 90 by 71 days, and site-wide clicks")
print("  fell from ~96/day to ~36/day across it, so the 'expected' column is a flat trailing")
print("  average that flatters early-dying pages and penalises late-dying ones. Directional only.")

json.dump(dict(windows=dict(cur=[str(CUR_W[0]),str(CUR_W[1])], pri=[str(PRI_W[0]),str(PRI_W[1])]),
               have_prior=have_prior, comparisons=out,
               norm_pages=pr[:40], norm_queries=qr[:40]),
          open(f'{H}/ninety_compare.json','w'), indent=1, default=str)
print(f"\nwrote ninety_compare.json   (true 90/90 dimensions live: {len(out)})")
