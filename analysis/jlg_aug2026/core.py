#!/usr/bin/env python3
"""Johnson Law Group - core metric extraction (stdlib only)."""
import csv, json, re, os
from datetime import datetime, date, timedelta
from collections import defaultdict, Counter
from statistics import mean

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
OUT = {}

def rd(path, skip_comments=False):
    with open(path, encoding='utf-8-sig') as f:
        lines = [l for l in f if not (skip_comments and l.startswith('#'))]
    return list(csv.DictReader(lines))

def num(s):
    if s is None: return 0
    s = str(s).strip().replace('%','').replace(',','')
    if s == '': return 0
    try: return float(s)
    except: return 0

# ---------------- 1. DAILY SERIES (merge 16mo + 90d) ----------------
daily = {}
for r in rd(f'{D}/gsc_16mo/Chart.csv'):
    d = r['Date']
    daily[d] = dict(d=d, clicks=int(num(r['Clicks'])), impr=int(num(r['Impressions'])),
                    pos=num(r['Position']), src='16mo')
for r in rd(f'{D}/gsc_90d/Chart.csv'):          # newer export wins on overlap
    d = r['Date']
    daily[d] = dict(d=d, clicks=int(num(r['Clicks'])), impr=int(num(r['Impressions'])),
                    pos=num(r['Position']), src='90d')
series = sorted(daily.values(), key=lambda x: x['d'])
series = [x for x in series if x['d'] < '2026-08-11']   # drop partial last day
OUT['daily'] = series
OUT['range'] = [series[0]['d'], series[-1]['d'], len(series)]

# monthly rollup
mo = defaultdict(list)
for x in series: mo[x['d'][:7]].append(x)
monthly = []
for k in sorted(mo):
    m = mo[k]; c = sum(y['clicks'] for y in m); i = sum(y['impr'] for y in m)
    monthly.append(dict(m=k, clicks=c, impr=i, ctr=round(100*c/i,3) if i else 0,
                        pos=round(mean(y['pos'] for y in m),1), days=len(m),
                        cpd=round(c/len(m),1), ipd=round(i/len(m)),
                        proj=round(c/len(m)*30)))
OUT['monthly'] = monthly

def window(a, b):
    sel = [x for x in series if a <= x['d'] <= b]
    if not sel: return None
    c = sum(x['clicks'] for x in sel); i = sum(x['impr'] for x in sel)
    return dict(a=a, b=b, days=len(sel), clicks=c, impr=i,
                ctr=round(100*c/i,3) if i else 0, pos=round(mean(x['pos'] for x in sel),1),
                cpd=round(c/len(sel),1), ipd=round(i/len(sel)))

# YoY on identical calendar windows
OUT['yoy'] = {
  'may10_aug10_2025': window('2025-05-10','2025-08-10'),
  'may10_aug10_2026': window('2026-05-10','2026-08-10'),
  'jun_jul_2025': window('2025-06-01','2025-07-31'),
  'jun_jul_2026': window('2026-06-01','2026-07-31'),
}
OUT['recent'] = {
  'last14':  window('2026-07-28','2026-08-10'),
  'prev14':  window('2026-07-14','2026-07-27'),
  'last30':  window('2026-07-12','2026-08-10'),
  'prev30':  window('2026-06-12','2026-07-11'),
  'p30_ago': window('2026-05-13','2026-06-11'),
  'aug_2026': window('2026-08-01','2026-08-10'),
  'may_2026': window('2026-05-10','2026-05-31'),
}

# ---------------- 2. QUERIES: brand vs non-brand ----------------
BRAND = re.compile(r'johnson|jlg|okeefe|o.?keefe|heidi whit|said sharbini|jason thacher|'
                   r'kristina contreras|myles johnson|taylor brice|anne hinds|amber harrison|'
                   r'melody anchietta|birgit|latney|genet|jessica lasky|lara rausch|shannon o|'
                   r'anthony stoeter|goldschmidt|robert perrone|heidi whittaker|shana velez', re.I)
GEO = re.compile(r'colorado|denver|cheyenne|wyoming|chicago|illinois|fort collins|colorado springs|'
                 r'commerce city|englewood|boca raton|florida|aurora|westminster|lakewood|boulder|'
                 r'pueblo|castle rock|greeley|littleton|centennial|arvada|thornton|broomfield|'
                 r'douglas county|adams county|jefferson county|arapahoe|el paso county|larimer|'
                 r'weld county|near me|salida|glenwood|grand junction|windsor|loveland|timnath', re.I)
COMMERCIAL = re.compile(r'lawyer|attorney|law firm|law group|law office|firm|counsel|legal help|'
                        r'consultation|free consult', re.I)

def qload(path):
    out = []
    for r in rd(path):
        q = r['Top queries']
        out.append(dict(q=q, clicks=int(num(r['Clicks'])), impr=int(num(r['Impressions'])),
                        pos=num(r['Position']),
                        brand=bool(BRAND.search(q)), geo=bool(GEO.search(q)),
                        comm=bool(COMMERCIAL.search(q))))
    return out

q90 = qload(f'{D}/gsc_90d/Queries.csv')
q16 = qload(f'{D}/gsc_16mo/Queries.csv')

def qsplit(qs, label):
    tot_c = sum(x['clicks'] for x in qs); tot_i = sum(x['impr'] for x in qs)
    b = [x for x in qs if x['brand']]; nb = [x for x in qs if not x['brand']]
    nbc = [x for x in nb if x['comm']]          # non-brand commercial (money terms)
    nbcg = [x for x in nbc if x['geo']]         # non-brand commercial + geo (highest intent)
    info = [x for x in nb if not x['comm']]     # informational
    def agg(g):
        c = sum(x['clicks'] for x in g); i = sum(x['impr'] for x in g)
        return dict(n=len(g), clicks=c, impr=i, ctr=round(100*c/i,3) if i else 0,
                    share_clicks=round(100*c/tot_c,1) if tot_c else 0,
                    share_impr=round(100*i/tot_i,1) if tot_i else 0,
                    wpos=round(sum(x['pos']*x['impr'] for x in g)/i,1) if i else 0)
    return dict(label=label, total_clicks=tot_c, total_impr=tot_i, n=len(qs),
                brand=agg(b), nonbrand=agg(nb), nb_commercial=agg(nbc),
                nb_comm_geo=agg(nbcg), informational=agg(info))

OUT['queries'] = {'d90': qsplit(q90,'90d May10-Aug11 2026'), 'd16mo': qsplit(q16,'16mo Mar2025-Jul2026')}

# money-term visibility: non-brand commercial sorted by impressions
nbc90 = sorted([x for x in q90 if not x['brand'] and x['comm']], key=lambda x:-x['impr'])
OUT['money_terms_top'] = nbc90[:60]
# position buckets for non-brand commercial
def buckets(qs):
    b = Counter(); bi = Counter(); bc = Counter()
    for x in qs:
        k = ('1-3' if x['pos']<=3 else '4-10' if x['pos']<=10 else '11-20' if x['pos']<=20
             else '21-50' if x['pos']<=50 else '51+')
        b[k]+=1; bi[k]+=x['impr']; bc[k]+=x['clicks']
    return {k: dict(n=b[k], impr=bi[k], clicks=bc[k]) for k in ['1-3','4-10','11-20','21-50','51+']}
OUT['nb_comm_buckets'] = buckets(nbc90)
OUT['nb_all_buckets']  = buckets([x for x in q90 if not x['brand']])
OUT['brand_buckets']   = buckets([x for x in q90 if x['brand']])

# zero-click money terms (impressions, no clicks)
OUT['zero_click_money'] = sorted([x for x in nbc90 if x['clicks']==0], key=lambda x:-x['impr'])[:40]
# striking distance: pos 11-25, non-brand
OUT['striking'] = sorted([x for x in q90 if not x['brand'] and 8 <= x['pos'] <= 25 and x['impr']>=150],
                         key=lambda x:-x['impr'])[:50]

# ---------------- 3. PAGES ----------------
def pload(path):
    """Load GSC pages, SUMMING www / non-www / ?utm variants of the same page.
    Position is impression-weighted across merged rows."""
    agg={}
    for r in rd(path):
        u = r['Top pages']
        k = re.sub(r'^https?://(www\.)?johnsonlgroup\.com','',u).split('?')[0].split('#')[0].rstrip('/') or '/'
        c,i,pos = int(num(r['Clicks'])), int(num(r['Impressions'])), num(r['Position'])
        if k in agg:
            e=agg[k]; tot=e['impr']+i
            e['pos'] = ((e['pos']*e['impr'])+(pos*i))/tot if tot else pos
            e['clicks'] += c; e['impr'] = tot
        else:
            agg[k]=dict(u=u, clicks=c, impr=i, pos=pos, path=k)
    return list(agg.values())
p90 = pload(f'{D}/gsc_90d/Pages.csv')
p16 = pload(f'{D}/gsc_16mo/Pages.csv')
OUT['pages_90d_top'] = sorted(p90, key=lambda x:-x['clicks'])[:60]
OUT['pages_90d_impr'] = sorted(p90, key=lambda x:-x['impr'])[:40]

tp_c = sum(x['clicks'] for x in p90); tp_i = sum(x['impr'] for x in p90)
OUT['pages_totals'] = dict(clicks=tp_c, impr=tp_i, n=len(p90))

# page-type segmentation
def ptype(p):
    q = p.rstrip('/')
    if p in ('/','' ): return 'Homepage'
    if q == '/blog' or q.startswith('/blog/categor') or q.startswith('/blog/category') \
       or re.match(r'^/blog/(page/)?\d+$', q) or re.match(r'^/blog/\d{4}/[a-z]+$', q) \
       or re.match(r'^/blog/\d{4}$', q) or re.match(r'^/blog/\d{4}/\d{2}(/\d{2})?$', q) \
       or q.startswith('/blog/video-category'): return 'Blog index/taxonomy'
    if p.startswith('/blog/'): return 'Blog post'
    if p.startswith('/attorneys') or p.startswith('/colorado/attorneys') or p.startswith('/es/abogados') \
       or p.startswith('/abogados'): return 'Attorney bio'
    if re.match(r'^/(colorado|wyoming|illinois|florida)/locations', p) or p.startswith('/locations'): return 'Location page'
    if re.match(r'^/(colorado|wyoming|illinois|florida)/areas', p): return 'Areas-served page'
    if re.match(r'^/(colorado|wyoming|illinois|florida)($|/)', p): return 'State/practice hub (/state/*)'
    if p.startswith('/practice-areas'): return 'Practice area (/practice-areas/*)'
    if re.search(r'-(lawyer|attorney)/?$', p) or re.search(r'-(lawyer|attorney)/page/', p): return 'City+service page'
    if p.startswith('/videos') or p.startswith('/webinars'): return 'Video/webinar'
    if p.startswith('/wp-content'): return 'Image/asset'
    if p.startswith('/es') or p.startswith('/espanol'): return 'Spanish'
    if p.startswith('/lp'): return 'Landing page (/lp/*)'
    return 'Other'

seg = defaultdict(lambda: dict(n=0, clicks=0, impr=0, pw=0.0))
for x in p90:
    s = seg[ptype(x['path'])]
    s['n']+=1; s['clicks']+=x['clicks']; s['impr']+=x['impr']; s['pw']+=x['pos']*x['impr']
for k,v in seg.items():
    v['ctr']=round(100*v['clicks']/v['impr'],3) if v['impr'] else 0
    v['pos']=round(v['pw']/v['impr'],1) if v['impr'] else 0
    del v['pw']
OUT['page_segments'] = dict(sorted(seg.items(), key=lambda kv:-kv[1]['clicks']))

# ---------------- 4. THE CIVIL UNION ANOMALY ----------------
cu = [x for x in p90 if 'civil-union' in x['u']]
OUT['civil_union'] = dict(pages=cu,
    impr=sum(x['impr'] for x in cu), clicks=sum(x['clicks'] for x in cu),
    pct_impr=round(100*sum(x['impr'] for x in cu)/tp_i,1))
cuq = [x for x in q90 if 'civil union' in x['q'].lower()]
OUT['civil_union_queries'] = dict(q=sorted(cuq,key=lambda x:-x['impr'])[:12],
    impr=sum(x['impr'] for x in cuq), clicks=sum(x['clicks'] for x in cuq))

# ---------------- 5. AI FEATURES ----------------
ai_pages = [dict(u=r['Top pages'], impr=int(num(r['Impressions']))) for r in rd(f'{D}/gsc_ai/Pages.csv')]
ai_dev   = [dict(k=r['Device'], impr=int(num(r['Impressions']))) for r in rd(f'{D}/gsc_ai/Devices.csv')]
ai_ctry  = [dict(k=r['Country'], impr=int(num(r['Impressions']))) for r in rd(f'{D}/gsc_ai/Countries.csv')]
ai_daily = [dict(d=r['Date'], impr=int(num(r['Impressions']))) for r in rd(f'{D}/gsc_ai/Chart.csv')]
ai_tot = sum(x['impr'] for x in ai_pages)
OUT['ai'] = dict(total_impr=ai_tot, pages=sorted(ai_pages,key=lambda x:-x['impr'])[:25],
                 devices=ai_dev, countries=ai_ctry[:15], daily=ai_daily,
                 share_of_all_impr=round(100*ai_tot/tp_i,1),
                 civil_union_impr=sum(x['impr'] for x in ai_pages if 'civil-union' in x['u']))

# ---------------- 6. COUNTRIES / DEVICES ----------------
OUT['countries_90d'] = [dict(k=r['Country'], clicks=int(num(r['Clicks'])), impr=int(num(r['Impressions'])),
                             pos=num(r['Position'])) for r in rd(f'{D}/gsc_90d/Countries.csv')][:20]
OUT['devices_90d']   = [dict(k=r['Device'], clicks=int(num(r['Clicks'])), impr=int(num(r['Impressions'])),
                             ctr=num(r['CTR']), pos=num(r['Position'])) for r in rd(f'{D}/gsc_90d/Devices.csv')]
OUT['devices_16mo']  = [dict(k=r['Device'], clicks=int(num(r['Clicks'])), impr=int(num(r['Impressions'])),
                             ctr=num(r['CTR']), pos=num(r['Position'])) for r in rd(f'{D}/gsc_16mo/Devices.csv')]
us = [c for c in OUT['countries_90d'] if c['k']=='United States'][0]
allc = [dict(k=r['Country'], clicks=int(num(r['Clicks'])), impr=int(num(r['Impressions'])))
        for r in rd(f'{D}/gsc_90d/Countries.csv')]
OUT['geo_waste'] = dict(us_impr=us['impr'], us_clicks=us['clicks'],
    total_impr=sum(c['impr'] for c in allc), total_clicks=sum(c['clicks'] for c in allc),
    nonus_impr=sum(c['impr'] for c in allc)-us['impr'],
    nonus_clicks=sum(c['clicks'] for c in allc)-us['clicks'])

# ---------------- 7. GA4 LANDING PAGES ----------------
ga = []
for r in rd(f'{D}/ga4/landing_pages.csv', skip_comments=True):
    if not r.get('Landing page'): continue
    ga.append(dict(p=r['Landing page'], sess=int(num(r['Sessions'])),
                   eng=int(num(r['Engaged sessions'])), nu=int(num(r['New users'])),
                   au=int(num(r['Active users'])), et=num(r['Average engagement time per session']),
                   ke=int(num(r['Key events'])), kr=num(r['Session key event rate'])))
OUT['ga4_totals'] = dict(sessions=sum(x['sess'] for x in ga), key_events=sum(x['ke'] for x in ga),
                         engaged=sum(x['eng'] for x in ga), n_pages=len(ga))
OUT['ga4_top_sessions'] = sorted(ga, key=lambda x:-x['sess'])[:50]
OUT['ga4_top_ke'] = sorted(ga, key=lambda x:-x['ke'])[:40]

def gtype(p):
    if p == '/': return 'Homepage'
    if p == '(not set)': return '(not set) — unattributed'
    if p.startswith('/lp/') or re.search(r'-(v2|landing-page)$', p) or p.endswith('-lp') \
       or p.startswith('/family-law-lp') or 'landing-page' in p: return 'Paid/LP (/lp/*, *-v2)'
    if re.match(r'^/(d/|coreycruzintake|tiffany-traylor|jlg-consulta|intakes-jlg|reschedulings|'
                r'myles-johnsonlgroup|birgit-almgren|heidi-whitaker-johnsonlgroup|jason-thacher-johnsonlgroup|'
                r'amber-harrison-johnsonlgroup|kristina-contreras-johnsonlgroup|myron-johnsonlgroup|'
                r'said-sharbini-johnsonlgroup|thomas-nellessen-johnsonlgroup|arian-martinez)', p): return 'Booking/scheduler URL'
    if 'thank-you' in p or p.startswith('/webinar-thank') or p=='/thank-you': return 'Thank-you page'
    if p.startswith('/blog/categor') or p.startswith('/blog/category') or re.match(r'^/blog/\d+$', p) \
       or re.match(r'^/blog/page', p) or re.match(r'^/blog/\d{4}(/[a-z]+)?$', p) \
       or re.match(r'^/blog/\d{4}/\d{2}(/\d{2})?$', p) or p.startswith('/category/') \
       or re.match(r'^/page/\d+$', p) or '/page/' in p: return 'Pagination/taxonomy junk'
    if p.startswith('/blog'): return 'Blog post'
    if p.startswith('/attorneys') or p.startswith('/abogados'): return 'Attorney bio'
    if re.match(r'^/(colorado|wyoming|illinois|florida)/locations', p): return 'Location page'
    if re.match(r'^/(colorado|wyoming|illinois|florida)/areas', p): return 'Areas-served page'
    if re.match(r'^/(colorado|wyoming|illinois|florida)($|/)', p): return 'State/practice hub'
    if p.startswith('/practice-areas'): return 'Practice area'
    if re.search(r'-(lawyer|attorney)$', p): return 'City+service page'
    if p.startswith('/contact') or p.startswith('/es/contact') or 'consultation' in p or p=='/new-client-consult': return 'Contact/consult'
    if p.startswith('/videos') or p.startswith('/webinars'): return 'Video/webinar'
    if p.startswith('/es') or p.startswith('/espanol'): return 'Spanish'
    return 'Other'

# 'Key events' is an EVENT COUNT, not converting sessions: /contact-us/thank-you shows
# 575 sessions / 881 key events but its own 'Session key event rate' column reads 98.26%.
# Dividing events by sessions inflates the rate ~3.1x sitewide. The honest conversion
# rate is converting sessions / sessions, recovered from the rate column GA4 supplies.
gseg = defaultdict(lambda: dict(n=0, sess=0, ke=0, cs=0.0, eng=0, etw=0.0))
for x in ga:
    s = gseg[gtype(x['p'])]
    s['n']+=1; s['sess']+=x['sess']; s['ke']+=x['ke']; s['eng']+=x['eng']
    s['etw']+=x['et']*x['sess']
    s['cs'] += x['kr']*x['sess']          # kr is a 0-1 rate; x rate x sessions = converting sessions
for k,v in gseg.items():
    v['skr']  = round(100*v['cs']/v['sess'],2) if v['sess'] else 0   # session key-event rate (TRUE)
    v['epcs'] = round(v['ke']/v['cs'],2) if v['cs'] else 0           # events per converting session
    v['kr']   = v['skr']                                             # dashboard reads kr
    v['engr'] = round(100*v['eng']/v['sess'],1) if v['sess'] else 0
    v['et']   = round(v['etw']/v['sess'],1) if v['sess'] else 0
    v['cs']   = round(v['cs'])
    del v['etw']
OUT['ga4_segments'] = dict(sorted(gseg.items(), key=lambda kv:-kv[1]['sess']))

# thin/broken pages: decent sessions, near-zero engagement time
OUT['ga4_thin'] = sorted([x for x in ga if x['sess']>=50 and x['et']<45],
                         key=lambda x:-x['sess'])[:40]
# high-traffic low-conversion service pages
svc = [x for x in ga if x['sess']>=90 and gtype(x['p']) in
       ('State/practice hub','Practice area','City+service page','Location page','Blog post','Areas-served page')]
OUT['ga4_service_underperf'] = sorted(svc, key=lambda x:-x['sess'])[:40]

# ---------------- 8. CANNIBALIZATION / DUPLICATION ----------------
def topicize(p):
    p = p.rstrip('/')
    p = re.sub(r'^/blog/\d{4}/[a-z]+/', '', p)
    p = re.sub(r'^/(colorado|wyoming|illinois|florida)/', '', p)
    p = re.sub(r'^/practice-areas/(family-law/)?', '', p)
    p = re.sub(r'^/locations/[a-z-]+/', '', p)
    p = re.sub(r'^/', '', p)
    p = re.sub(r'-(v2|2|1)$', '', p)
    return p
groups = defaultdict(list)
for x in p90:
    if x['impr'] < 5: continue
    groups[topicize(x['path'])].append(x)
dupes = {k: sorted(v,key=lambda z:-z['impr']) for k,v in groups.items() if len(v) > 1}
OUT['cannibal_groups'] = dict(sorted(dupes.items(), key=lambda kv:-sum(z['impr'] for z in kv[1]))[:30])

# truncated-slug duplicates (WP slug cut at ~48 chars)
trunc = []
paths = {x['path'].rstrip('/'): x for x in p90}
for p, x in paths.items():
    for p2, x2 in paths.items():
        if p != p2 and p2.startswith(p) and len(p2) > len(p) and len(p.split('/')[-1]) >= 40:
            trunc.append(dict(short=p, short_impr=x['impr'], short_clicks=x['clicks'],
                              long=p2, long_impr=x2['impr'], long_clicks=x2['clicks']))
OUT['truncated_dupes'] = sorted(trunc, key=lambda z:-(z['short_impr']+z['long_impr']))[:25]

# ---------------- 9. INDEX BLOAT (GA4 URL universe) ----------------
bloat_pat = {
 'Booking scheduler URLs': r'^/(d/|coreycruzintake|tiffany-traylor|jlg-consulta|intakes-jlg|reschedulings/|myles-johnsonlgroup|birgit-almgren|heidi-whitaker-johnsonlgroup|jason-thacher-johnsonlgroup|amber-harrison-johnsonlgroup|kristina-contreras-johnsonlgroup|myron-johnsonlgroup|said-sharbini-johnsonlgroup|thomas-nellessen-johnsonlgroup|arian-martinez)',
 'Pagination (/page/N)': r'/page/\d+',
 'Blog archive stubs': r'^/blog/(\d{4}(/[a-z]+)?|\d+)$|^/blog/\d{4}/\d{2}(/\d{2})?$|^/\d{4}/\d{2}$',
 'Taxonomy/category': r'^/(blog/)?categor(y|ies)/|^/category/',
 'WP /embed/ endpoints': r'/embed/?$',
 'Truncated/garbled URLs': r'(&sa=U|&ved=|usg=|https?:/|\.php|wp-admin|%20|\?|,|\|)',
}
gb = {}
for name, pat in bloat_pat.items():
    rx = re.compile(pat)
    hits = [x for x in ga if rx.search(x['p'])]
    gb[name] = dict(urls=len(hits), sessions=sum(x['sess'] for x in hits),
                    key_events=sum(x['ke'] for x in hits))
OUT['index_bloat'] = gb
OUT['ga4_url_count'] = len(ga)
OUT['ga4_longtail'] = dict(
    urls_le2_sessions=len([x for x in ga if x['sess']<=2]),
    urls_le5_sessions=len([x for x in ga if x['sess']<=5]),
    sessions_from_le5=sum(x['sess'] for x in ga if x['sess']<=5))

# ---------------- 10. CTR vs POSITION EFFICIENCY ----------------
def ctr_curve(qs):
    out = {}
    for lo,hi,lab in [(1,3,'1-3'),(3,5,'3-5'),(5,10,'5-10'),(10,20,'10-20'),(20,100,'20+')]:
        g = [x for x in qs if lo <= x['pos'] < hi]
        i = sum(x['impr'] for x in g); c = sum(x['clicks'] for x in g)
        out[lab] = dict(n=len(g), impr=i, clicks=c, ctr=round(100*c/i,3) if i else 0)
    return out
OUT['ctr_curve_all'] = ctr_curve(q90)
OUT['ctr_curve_nb'] = ctr_curve([x for x in q90 if not x['brand']])
OUT['ctr_curve_nb_ex_cu'] = ctr_curve([x for x in q90 if not x['brand'] and 'civil union' not in x['q'].lower()])

# ---------------- 11. PAGE-LEVEL DECLINE (16mo run-rate vs last 90d) ----------------
# 16mo export = 2025-03-20..2026-07-19 (487d). Normalize both to clicks/90d.
p16m = {x['path'].rstrip('/'): x for x in p16}
p90m = {x['path'].rstrip('/'): x for x in p90}
decl = []
for k, a in p16m.items():
    base90 = a['clicks'] * 90/487.0          # historical avg per 90 days
    now = p90m.get(k, {'clicks':0,'impr':0,'pos':0})
    if base90 >= 8:
        decl.append(dict(path=k, hist_90d_rate=round(base90,1), now_90d=now['clicks'],
                         delta=round(now['clicks']-base90,1),
                         pct=round(100*(now['clicks']/base90-1),1) if base90 else 0,
                         hist_pos=a['pos'], now_pos=now.get('pos',0),
                         hist_impr=a['impr'], now_impr=now.get('impr',0)))
OUT['page_decliners'] = sorted(decl, key=lambda x:x['delta'])[:35]
OUT['page_gainers']   = sorted(decl, key=lambda x:-x['delta'])[:25]

# query-level decline, same normalization
q16m = {x['q']: x for x in q16}
q90m = {x['q']: x for x in q90}
qdecl = []
for k, a in q16m.items():
    base90 = a['clicks'] * 90/487.0
    now = q90m.get(k, {'clicks':0,'impr':0,'pos':0})
    if base90 >= 4:
        qdecl.append(dict(q=k, brand=bool(BRAND.search(k)), hist_90d_rate=round(base90,1),
                          now_90d=now['clicks'], delta=round(now['clicks']-base90,1),
                          hist_pos=a['pos'], now_pos=now.get('pos',0)))
OUT['query_decliners'] = sorted(qdecl, key=lambda x:x['delta'])[:30]

# ---------------- 12. AUGUST CLIFF / VOLATILITY ----------------
OUT['weekly'] = []
wk = defaultdict(list)
for x in series:
    dt = datetime.strptime(x['d'],'%Y-%m-%d').date()
    wk[(dt - timedelta(days=dt.weekday())).isoformat()].append(x)
for k in sorted(wk):
    g = wk[k]
    if len(g) < 7: continue
    c = sum(y['clicks'] for y in g); i = sum(y['impr'] for y in g)
    OUT['weekly'].append(dict(w=k, clicks=c, impr=i, ctr=round(100*c/i,3) if i else 0,
                              pos=round(mean(y['pos'] for y in g),1)))

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'metrics.json'),'w') as f:
    json.dump(OUT, f, indent=1, default=str)

# ---------------- PRINT ----------------
P = print
P("="*78); P("RANGE:", OUT['range']); P("="*78)
P("\n--- MONTHLY (last 18) ---")
P(f"{'Mo':8}{'Clicks':>8}{'Proj30':>8}{'Impr':>10}{'CTR%':>7}{'Pos':>6}{'Days':>5}")
for m in monthly[-18:]:
    P(f"{m['m']:8}{m['clicks']:>8}{m['proj']:>8}{m['impr']:>10}{m['ctr']:>7.2f}{m['pos']:>6}{m['days']:>5}")

P("\n--- YoY (identical windows) ---")
for k,v in OUT['yoy'].items():
    if v: P(f"{k:24} clicks={v['clicks']:>5} ({v['cpd']}/d)  impr={v['impr']:>8} ({v['ipd']}/d)  CTR={v['ctr']}%  pos={v['pos']}")
y1,y2 = OUT['yoy']['may10_aug10_2025'], OUT['yoy']['may10_aug10_2026']
P(f"  >> YoY clicks {y1['clicks']}->{y2['clicks']} = {round(100*(y2['clicks']/y1['clicks']-1),1)}% | "
  f"impr {y1['impr']}->{y2['impr']} = {round(100*(y2['impr']/y1['impr']-1),1)}%")

P("\n--- RECENT TREND ---")
for k,v in OUT['recent'].items():
    if v: P(f"{k:10} {v['a']}..{v['b']}  clicks/d={v['cpd']:>6}  impr/d={v['ipd']:>7}  CTR={v['ctr']}%  pos={v['pos']}")

P("\n--- QUERY MIX (90d) ---")
d = OUT['queries']['d90']
P(f"total clicks in query export: {d['total_clicks']}, impressions: {d['total_impr']}")
for k in ['brand','nonbrand','nb_commercial','nb_comm_geo','informational']:
    v = d[k]
    P(f"  {k:16} n={v['n']:>4} clicks={v['clicks']:>5} ({v['share_clicks']:>5}% of clicks)  "
      f"impr={v['impr']:>8} ({v['share_impr']:>5}%)  CTR={v['ctr']:>6}%  wpos={v['wpos']}")

P("\n--- NON-BRAND COMMERCIAL POSITION BUCKETS (90d) ---")
for k,v in OUT['nb_comm_buckets'].items():
    P(f"  pos {k:6} queries={v['n']:>4}  impr={v['impr']:>8}  clicks={v['clicks']:>5}")

P("\n--- CIVIL UNION ANOMALY ---")
c = OUT['civil_union']
P(f"  page impressions={c['impr']} ({c['pct_impr']}% of ALL site impressions), clicks={c['clicks']}")
cq = OUT['civil_union_queries']
P(f"  query cluster impressions={cq['impr']}, clicks={cq['clicks']}")
for x in cq['q'][:6]: P(f"     {x['q'][:52]:54} impr={x['impr']:>7} clicks={x['clicks']:>3} pos={x['pos']}")

P("\n--- AI FEATURES (AI Overviews/AI Mode) ---")
a = OUT['ai']
P(f"  total AI impressions={a['total_impr']} = {a['share_of_all_impr']}% of all search impressions")
P(f"  civil-union share of AI impressions={a['civil_union_impr']} "
  f"({round(100*a['civil_union_impr']/a['total_impr'],1)}%)")
P(f"  devices: {a['devices']}")

P("\n--- PAGE SEGMENTS (GSC 90d) ---")
P(f"{'segment':32}{'urls':>6}{'clicks':>8}{'impr':>10}{'CTR%':>8}{'pos':>7}")
for k,v in OUT['page_segments'].items():
    P(f"{k:32}{v['n']:>6}{v['clicks']:>8}{v['impr']:>10}{v['ctr']:>8}{v['pos']:>7}")

P("\n--- GA4 SEGMENTS (Jan1-Aug11 2026) ---")
g = OUT['ga4_totals']; P(f"  TOTALS sessions={g['sessions']} key_events={g['key_events']} urls={g['n_pages']}")
P(f"{'segment':32}{'urls':>6}{'sess':>8}{'KE':>7}{'KE%':>7}{'eng%':>7}{'sec':>7}")
for k,v in OUT['ga4_segments'].items():
    P(f"{k:32}{v['n']:>6}{v['sess']:>8}{v['ke']:>7}{v['kr']:>7}{v['engr']:>7}{v['et']:>7}")

P("\n--- INDEX BLOAT ---")
for k,v in OUT['index_bloat'].items(): P(f"  {k:26} urls={v['urls']:>5}  sessions={v['sessions']:>6}  KE={v['key_events']}")
P(f"  GA4 distinct landing URLs: {OUT['ga4_url_count']}; <=5 sessions: {OUT['ga4_longtail']['urls_le5_sessions']}")

P("\n--- CTR CURVE (non-brand, excl civil union) ---")
for k,v in OUT['ctr_curve_nb_ex_cu'].items(): P(f"  pos {k:6} impr={v['impr']:>8} clicks={v['clicks']:>5} CTR={v['ctr']}%")

P("\n--- GEO WASTE ---"); P(" ", OUT['geo_waste'])
P("\n--- DEVICES 90d ---")
for x in OUT['devices_90d']: P(f"  {x['k']:9} clicks={x['clicks']:>5} impr={x['impr']:>8} CTR={x['ctr']}% pos={x['pos']}")
P("\nWrote metrics.json")
