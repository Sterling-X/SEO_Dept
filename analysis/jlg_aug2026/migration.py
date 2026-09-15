#!/usr/bin/env python3
"""Quantify the truncated-slug URL migration + locate the changepoint."""
import csv, json, re, os
from collections import defaultdict
from statistics import mean

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
def rd(p):
    with open(p, encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def n(s):
    s=str(s).replace('%','').replace(',','').strip()
    try: return float(s)
    except: return 0.0

def pages(p):
    """Aggregate GSC page rows by normalised URL.

    The export lists www and non-www (and ?utm-tagged) variants of the same page as
    separate rows. These must be SUMMED — an earlier version assigned instead of
    accumulating, so a later duplicate row silently overwrote the first and hid
    13 URLs / 1,903 clicks from the 16-month totals.
    Position is impression-weighted across the merged rows.
    """
    out={}
    for r in rd(p):
        u=re.sub(r'^https?://(www\.)?johnsonlgroup\.com','',r['Top pages'])
        u=u.split('?')[0].split('#')[0].rstrip('/')
        c,i,pos=int(n(r['Clicks'])),int(n(r['Impressions'])),n(r['Position'])
        if u in out:
            e=out[u]; tot=e['impr']+i
            e['pos']=((e['pos']*e['impr'])+(pos*i))/tot if tot else pos
            e['clicks']+=c; e['impr']=tot
        else:
            out[u]=dict(u=u,clicks=c,impr=i,pos=pos)
    return out
P16, P90 = pages(f'{D}/gsc_16mo/Pages.csv'), pages(f'{D}/gsc_90d/Pages.csv')

# --- identify truncated-slug URLs: a URL that is a strict prefix of another URL,
#     where the truncated tail is >=35 chars (CMS slug cut) ---
keys = list(P16.keys())
pairs = []
for a in keys:
    tail_a = a.split('/')[-1]
    if len(tail_a) < 35: continue
    for b in keys:
        if b == a: continue
        if b.startswith(a) and len(b) > len(a):
            pairs.append((a, b))
# also trailing-dash variants  /slug-  vs /slug
for a in keys:
    if a.endswith('-') and a[:-1] in P16: pairs.append((a, a[:-1]))

seen=set(); rows=[]
for old, new in pairs:
    if (old,new) in seen: continue
    seen.add((old,new))
    o16, n16 = P16[old], P16.get(new, dict(clicks=0,impr=0,pos=0))
    o90 = P90.get(old, dict(clicks=0,impr=0,pos=0))
    n90 = P90.get(new, dict(clicks=0,impr=0,pos=0))
    hist90 = (o16['clicks']+n16['clicks'])*90/487.0     # blended historical rate per 90d
    now90  = o90['clicks']+n90['clicks']
    rows.append(dict(old=old, new=new, old16=o16['clicks'], new16=n16['clicks'],
                     hist90=round(hist90,1), now90=now90, delta=round(now90-hist90,1),
                     pct=round(100*(now90/hist90-1),1) if hist90 else 0,
                     old90=o90['clicks'], new90=n90['clicks'],
                     old_pos=o16['pos'], new_pos=n90['pos'] or n16['pos'],
                     old_impr16=o16['impr'], now_impr=o90['impr']+n90['impr']))
rows = [r for r in rows if r['old16'] >= 20]
# dedupe reciprocal pairs (trailing-dash variants produce A->B and B->A): keep higher old16
canon = {}
for r in rows:
    key = tuple(sorted([r['old'].rstrip('-'), r['new'].rstrip('-')]))
    if key not in canon or r['old16'] > canon[key]['old16']:
        canon[key] = r
rows = sorted(canon.values(), key=lambda r: r['delta'])

print("="*118)
print("TRUNCATED-SLUG MIGRATION CASUALTIES  (old 16mo clicks >= 20)")
print("="*118)
print(f"{'OLD (truncated) URL':60}{'old16':>7}{'new16':>7}{'hist/90d':>9}{'now/90d':>8}{'chg%':>8}")
for r in rows[:30]:
    print(f"{r['old'][:58]:60}{r['old16']:>7}{r['new16']:>7}{r['hist90']:>9}{r['now90']:>8}{r['pct']:>8}")
tot_hist = sum(r['hist90'] for r in rows); tot_now = sum(r['now90'] for r in rows)
print("-"*118)
print(f"{'TOTAL across '+str(len(rows))+' migrated URL pairs':60}{sum(r['old16'] for r in rows):>7}"
      f"{sum(r['new16'] for r in rows):>7}{tot_hist:>9.0f}{tot_now:>8}"
      f"{100*(tot_now/tot_hist-1):>7.1f}%")

# --- URLs that vanished entirely (16mo clicks>=25, zero impressions in 90d) ---
gone = [v for k,v in P16.items() if v['clicks']>=25 and k not in P90]
gone.sort(key=lambda x:-x['clicks'])
print(f"\n{'='*118}\nURLs WITH ZERO IMPRESSIONS IN LAST 90 DAYS (had >=25 clicks in prior 16 months)\n{'='*118}")
print(f"{'URL':72}{'16mo clicks':>12}{'16mo impr':>11}{'pos':>7}")
for g in gone[:30]:
    print(f"{g['u'][:70]:72}{g['clicks']:>12}{g['impr']:>11}{g['pos']:>7}")
# 53 of these are the "old" side of a migration pair and are ALREADY counted in the
# migration bucket above. Reporting the gross figure next to that table double-counts them.
_olds = {r['old'] for r in rows}
gone_indep = [g for g in gone if g['u'] not in _olds]
_gc = sum(g['clicks'] for g in gone)
_ic = sum(g['clicks'] for g in gone_indep)
print(f"\n  >> GROSS       {len(gone)} URLs, {_gc:,} clicks (~{round(_gc*90/487):,}/90d)")
print(f"     of which     {len(gone)-len(gone_indep)} URLs, {_gc-_ic:,} clicks are the 'old' side of a "
      f"migration pair -- ALREADY COUNTED ABOVE")
print(f"  >> INDEPENDENT {len(gone_indep)} URLs, {_ic:,} clicks (~{round(_ic*90/487):,}/90d)"
      f"  <-- the figure to report alongside the migration table")
print("     NB: a flat 16-month average, not a recovery forecast; per-URL death dates are not in these exports.")

# --- CHANGEPOINT: weekly series with rolling means ---
daily={}
for r in rd(f'{D}/gsc_16mo/Chart.csv'):
    daily[r['Date']]=dict(c=int(n(r['Clicks'])),i=int(n(r['Impressions'])),p=n(r['Position']))
for r in rd(f'{D}/gsc_90d/Chart.csv'):
    daily[r['Date']]=dict(c=int(n(r['Clicks'])),i=int(n(r['Impressions'])),p=n(r['Position']))
ds=sorted(k for k in daily if k<'2026-08-11')
print(f"\n{'='*118}\nMONTHLY TIMELINE — where the shifts happened\n{'='*118}")
mo=defaultdict(list)
for d in ds: mo[d[:7]].append(daily[d])
print(f"{'month':9}{'clicks':>8}{'/day':>7}{'impr':>10}{'impr/day':>10}{'CTR%':>7}{'pos':>7}  marker")
prev=None
for k in sorted(mo):
    g=mo[k]; c=sum(x['c'] for x in g); i=sum(x['i'] for x in g)
    cpd=c/len(g); ipd=i/len(g); pos=mean(x['p'] for x in g)
    mark=''
    if prev:
        if ipd < prev[1]*0.80: mark+=' IMPR-DROP'
        if pos < prev[2]-4:    mark+=' POS-JUMP'
        if cpd < prev[0]*0.80: mark+=' CLICK-DROP'
    print(f"{k:9}{c:>8}{cpd:>7.0f}{i:>10}{ipd:>10.0f}{100*c/i:>7.2f}{pos:>7.1f}  {mark}")
    prev=(cpd,ipd,pos)

json.dump(dict(migration_pairs=rows, vanished=gone, vanished_independent=gone_indep),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'migration.json'),'w'),
          indent=1, default=str)
