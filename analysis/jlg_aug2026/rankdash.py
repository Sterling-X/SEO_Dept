#!/usr/bin/env python3
"""Merge rank-tracker aggregates into chartdata.json for the dashboard."""
import json, os, re
from collections import defaultdict, Counter

H = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(f'{H}/ranks.json'))
C = json.load(open(f'{H}/chartdata.json'))
kw = R['keywords']

CTR = {1:.276,2:.149,3:.099,4:.072,5:.053,6:.041,7:.033,8:.028,9:.024,10:.021}
def ctr(p):
    p = max(1, round(p))
    if p <= 10: return CTR[p]
    return .012 if p<=20 else .006 if p<=30 else .002 if p<=50 else .0005

NICE = {'colorado-springs':'Colorado Springs','denver':'Denver','fort-collins':'Fort Collins',
        'commerce-city':'Commerce City','englewood':'Englewood'}

# --- market size vs visibility (search volume by current rank band) ---
mv = defaultdict(lambda: dict(top10=0., mid=0., deep=0., n=0, vol=0.))
for x in kw:
    s = mv[x['city']]; s['n'] += 1; s['vol'] += x['vol']
    if x['now'] <= 10:  s['top10'] += x['vol']
    elif x['now'] <= 30: s['mid'] += x['vol']
    else:                s['deep'] += x['vol']
market = [dict(city=NICE[c], vol=round(v['vol']), top10=round(v['top10']),
               mid=round(v['mid']), deep=round(v['deep']), n=v['n'],
               pct10=round(100*v['top10']/max(v['vol'],1),1))
          for c, v in sorted(mv.items(), key=lambda t: -t[1]['vol'])]

# --- local pack dependence ---
local = [dict(city=NICE[c], local=R['feat'][c]['local'], organic=R['feat'][c]['organic'],
              ai=R['feat'][c]['ai'], obs=R['feat'][c]['obs'])
         for c in ['commerce-city','englewood','fort-collins','colorado-springs','denver']]

# --- top-3 rankings: map pack vs website ---
top3 = defaultdict(lambda: Counter())
for x in kw:
    if x['now'] <= 3: top3[x['city']]['n'] += 1
t3 = [dict(city=NICE[c], n=v['n']) for c, v in top3.items()]

# --- architecture mix at snapshot dates ---
SNAP = ['20260325','20260408','20260603','20260811']
LBL  = {'20260325':'Mar 25','20260408':'Apr 8','20260603':'Jun 3','20260811':'Aug 11'}
amix = []
for r in R['arch_series']:
    if r['d'] in SNAP:
        amix.append(dict(d=LBL[r['d']],
                         flat=r['flat'], nested=r['nested']+r['nstate'],
                         pa=r['pa'], other=r['blog']+r['home'], total=r['total']))
arch_full = [dict(d=r['d'], flat=r['flat'], nested=r['nested']+r['nstate']) for r in R['arch_series']]

# --- position change by what the page was at baseline ---
def archc(p):
    if not p: return None
    if p.startswith(('/colorado/locations/','/wyoming/locations/')): return 'New /colorado/locations/*'
    if p.startswith(('/colorado/','/wyoming/')): return 'State topic /colorado/*'
    if p.startswith('/practice-areas/'): return '/practice-areas/*'
    if p.startswith('/blog/'): return 'Blog post'
    if p in ('/',''): return 'Homepage'
    if re.match(r'^/[a-z-]+-(lawyer|attorney)/?$', p): return 'Old flat /city-service-lawyer'
    return 'Other'
g = defaultdict(list)
for x in kw:
    a = archc(x['base_url'])
    if a: g[a].append(x)
bydelta = sorted([dict(seg=a, n=len(l),
                       base=round(sum(y['base'] for y in l)/len(l),1),
                       now=round(sum(y['now'] for y in l)/len(l),1),
                       delta=round(sum(y['delta'] for y in l)/len(l),1))
                  for a, l in g.items() if len(l) >= 5], key=lambda x: -x['delta'])

# --- paid-equivalent gap ---
gaps = []
for x in kw:
    if x['vol'] > 0 and x['cpc'] > 0:
        v = (x['vol']*CTR[3] - x['vol']*ctr(x['now'])) * x['cpc']
        gaps.append(dict(city=NICE[x['city']], k=x['k'], vol=int(x['vol']), cpc=x['cpc'],
                         now=x['now'], base=x['base'], delta=x['delta'], val=round(v)))
gaps.sort(key=lambda x: -x['val'])
gap_total = round(sum(x['val'] for x in gaps))

# --- head terms ---
head = sorted([dict(city=NICE[x['city']], k=x['k'], vol=int(x['vol']), cpc=x['cpc'],
                    base=x['base'], now=x['now'], delta=x['delta'])
               for x in kw if x['vol'] >= 100], key=lambda x: -x['vol'])

C['ranks'] = dict(
    span='2026-03-25 → 2026-08-11', n_kw=len(kw), n_proj=5,
    market=market, local=local, top3=t3, amix=amix, arch_full=arch_full,
    bydelta=bydelta, gaps=gaps[:14], gap_total=gap_total, head=head,
    churn=R['churn'], ai=R['ai'],
    overall=dict(base=round(sum(x['base'] for x in kw)/len(kw),1),
                 now=round(sum(x['now'] for x in kw)/len(kw),1)),
)
json.dump(C, open(f'{H}/chartdata.json','w'), indent=1, default=str)

print("market size vs visibility:")
for m in market: print(f"  {m['city']:17} vol {m['vol']:>6}  top10 {m['top10']:>5} ({m['pct10']}%)  11-30 {m['mid']:>5}  31+ {m['deep']:>5}")
print("\nposition change by baseline page type:")
for b in bydelta: print(f"  {b['seg']:30} n={b['n']:>3}  {b['base']:>5} -> {b['now']:>5}  ({b['delta']:+})")
print(f"\noverall tracked avg position {C['ranks']['overall']['base']} -> {C['ranks']['overall']['now']}")
print(f"paid-equivalent gap ${gap_total:,}/mo across {len(gaps)} keywords with CPC data")
print("wrote chartdata.json (+ranks)")
