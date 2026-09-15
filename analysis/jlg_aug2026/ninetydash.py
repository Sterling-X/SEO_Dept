#!/usr/bin/env python3
"""Compute the 90-over-90 payload and merge it into chartdata.json."""
import csv, json, os, re, glob
from collections import defaultdict
from datetime import date, timedelta

H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'data')
def rd(p):
    with open(p, encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def n(s):
    s = str(s).replace('%','').replace(',','').strip()
    try: return float(s)
    except: return 0.0
def dt(s): return date(int(s[:4]), int(s[5:7]), int(s[8:10]))
def norm(u):
    u = re.sub(r'^https?://(www\.)?johnsonlgroup\.com','',u); return u.split('?')[0].rstrip('/') or '/'

daily = {}
for r in rd(f'{D}/gsc_16mo/Chart.csv'):
    daily[r['Date']] = dict(c=int(n(r['Clicks'])), i=int(n(r['Impressions'])), p=n(r['Position']))
for r in rd(f'{D}/gsc_90d/Chart.csv'):
    daily[r['Date']] = dict(c=int(n(r['Clicks'])), i=int(n(r['Impressions'])), p=n(r['Position']))
END = date(2026, 8, 10)
def win(end, days):
    s = end - timedelta(days=days-1)
    return s, end, sorted(k for k in daily if s <= dt(k) <= end)
def agg(ks):
    c = sum(daily[k]['c'] for k in ks); i = sum(daily[k]['i'] for k in ks)
    return dict(days=len(ks), clicks=c, impr=i, ctr=round(100*c/i,3) if i else 0,
                pos=round(sum(daily[k]['p']*daily[k]['i'] for k in ks)/i,2) if i else 0,
                cpd=round(c/len(ks),1) if ks else 0, ipd=round(i/len(ks)) if ks else 0)

CUR, PRI, YOY = win(END,90), win(END-timedelta(days=90),90), win(END.replace(year=2025),90)
A, B, Y = agg(CUR[2]), agg(PRI[2]), agg(YOY[2])
d_imp = (A['impr']-B['impr'])*(B['ctr']/100)
d_ctr = A['impr']*((A['ctr']-B['ctr'])/100)

subs = []
for j in range(6):
    e = END - timedelta(days=30*j); s,_,ks = win(e,30); g = agg(ks)
    subs.append(dict(label=f"{s.strftime('%d %b')} – {e.strftime('%d %b')}", **g))
subs.reverse()

# civil-union denominator test
def pagg(p):
    o = defaultdict(lambda:[0,0])
    for r in rd(p):
        k = norm(r['Top pages']); o[k][0]+=int(n(r['Clicks'])); o[k][1]+=int(n(r['Impressions']))
    return o
P16, P90 = pagg(f'{D}/gsc_16mo/Pages.csv'), pagg(f'{D}/gsc_90d/Pages.csv')
CU = '/blog/2021/october/what-is-a-civil-union-in-colorado'
cu90, cu16 = P90[CU], P16[CU]
cu_flat = cu16[1]*90/487

top_impr = [dict(u=k, impr=i, clicks=c, ctr=round(100*c/i,3) if i else 0)
            for k,(c,i) in sorted(P90.items(), key=lambda t:-t[1][1])[:12]]

# Semrush matched panel
series = defaultdict(dict); vol = {}
for path in sorted(glob.glob(f'{D}/ranks/*.csv')):
    lines = open(path, encoding='utf-8-sig').read().split('\n')
    st = next(i for i,l in enumerate(lines) if l.startswith('Keyword,'))
    hdr = list(csv.reader([lines[st]]))[0]
    dates = [(c, re.search(r'_(\d{8})$',c).group(1)) for c in hdr
             if re.search(r'_(\d{8})$',c) and not c.endswith(('_type','_landing'))]
    pid = re.search(r'_(\d+)_position', path).group(1)
    for r in csv.DictReader(lines[st:]):
        k=(pid,r['Keyword']); vol[k]=n(r.get('Search Volume'))
        for col,d in dates:
            v=(r.get(col) or '').strip()
            if v and v!='-':
                try: series[k][d]=int(v)
                except ValueError: pass
alld = sorted({d for s in series.values() for d in s}); mid = alld[len(alld)//2]
f1 = [d for d in alld if d<=mid]; f2 = [d for d in alld if d>mid]
def half(s,ds):
    v=[s[d] for d in ds if d in s]; return sum(v)/len(v) if v else None
rows=[]
for k,s in series.items():
    a,b = half(s,f1), half(s,f2)
    if a is not None and b is not None: rows.append((a,b,vol.get(k,0)))
tv = sum(r[2] for r in rows)
sem = dict(n=len(rows), a=f"{f1[0][4:6]}/{f1[0][6:]}", b=f"{f2[-1][4:6]}/{f2[-1][6:]}",
           unw_a=round(sum(r[0] for r in rows)/len(rows),2), unw_b=round(sum(r[1] for r in rows)/len(rows),2),
           w_a=round(sum(r[0]*r[2] for r in rows)/tv,2), w_b=round(sum(r[1]*r[2] for r in rows)/tv,2),
           vol=round(tv), worse=len([r for r in rows if r[1]-r[0]>3]),
           better=len([r for r in rows if r[1]-r[0]<-3]))
sem['flat'] = sem['n']-sem['worse']-sem['better']

C = json.load(open(f'{H}/chartdata.json'))
C['n90'] = dict(
  cur=dict(**A, s=str(CUR[0]), e=str(CUR[1])), pri=dict(**B, s=str(PRI[0]), e=str(PRI[1])),
  yoy=dict(**Y, s=str(YOY[0]), e=str(YOY[1])),
  d_imp=round(d_imp), d_ctr=round(d_ctr), d_tot=A['clicks']-B['clicks'],
  subs=subs, top_impr=top_impr, sem=sem,
  cu=dict(impr90=cu90[1], clicks90=cu90[0], impr16=cu16[1], flat90=round(cu_flat),
          mult=round(cu90[1]/cu_flat,1), share_of_rise=round(100*(cu90[1]-cu_flat)/(A['impr']-B['impr'])),
          ex_ctr=round(100*(A['clicks']-cu90[0])/(A['impr']-cu90[1]),3)),
)
json.dump(C, open(f'{H}/chartdata.json','w'), indent=1, default=str)
print(f"clicks {B['clicks']:,} -> {A['clicks']:,} ({100*(A['clicks']/B['clicks']-1):+.1f}%)")
print(f"impr   {B['impr']:,} -> {A['impr']:,} ({100*(A['impr']/B['impr']-1):+.1f}%)")
print(f"CTR    {B['ctr']}% -> {A['ctr']}%   pos {B['pos']} -> {A['pos']}")
print(f"decomp volume {d_imp:+.0f} / rate {d_ctr:+.0f} = {A['clicks']-B['clicks']:+}")
print(f"civil-union {cu90[1]:,} impr = {C['n90']['cu']['mult']}x its flat rate, {C['n90']['cu']['share_of_rise']}% of the rise")
print("wrote chartdata.json (+n90)")
