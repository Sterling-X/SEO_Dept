#!/usr/bin/env python3
"""Build the dashboard data payload."""
import csv, json, re, os
from collections import defaultdict
from statistics import mean

H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H,'data')
M = json.load(open(f'{H}/metrics.json'))
MIG = json.load(open(f'{H}/migration.json'))
def rd(p, skipc=False):
    with open(p, encoding='utf-8-sig') as f:
        ls=[l for l in f if not (skipc and l.startswith('#'))]
    return list(csv.DictReader(ls))
def n(s):
    s=str(s).replace('%','').replace(',','').strip()
    try: return float(s)
    except: return 0.0

C = {}
C['monthly'] = [m for m in M['monthly']]
C['weekly']  = M['weekly']
C['yoy']     = M['yoy']
C['recent']  = M['recent']

# --- brand vs nonbrand share ---
q = M['queries']['d90']
C['mix'] = dict(
  brand=dict(clicks=q['brand']['clicks'], impr=q['brand']['impr'], ctr=q['brand']['ctr']),
  nonbrand=dict(clicks=q['nonbrand']['clicks'], impr=q['nonbrand']['impr'], ctr=q['nonbrand']['ctr']),
  nb_comm=q['nb_commercial'], nb_comm_geo=q['nb_comm_geo'], info=q['informational'],
  total_clicks=q['total_clicks'], total_impr=q['total_impr'])

# --- CTR curve: brand vs non-brand at the SAME position bands (internal benchmark) ---
BRAND = re.compile(r'johnson|jlg|okeefe|o.?keefe|heidi whit|said sharbini|jason thacher|'
                   r'kristina contreras|myles johnson|taylor brice|anne hinds|amber harrison|'
                   r'melody anchietta|birgit|latney|genet|jessica lasky|lara rausch|shannon o|'
                   r'anthony stoeter|goldschmidt|robert perrone|heidi whittaker|shana velez', re.I)
qs=[]
for r in rd(f'{D}/gsc_90d/Queries.csv'):
    t=r['Top queries']
    qs.append(dict(q=t,c=int(n(r['Clicks'])),i=int(n(r['Impressions'])),p=n(r['Position']),
                   b=bool(BRAND.search(t))))
BANDS=[(1,3,'1–3'),(3,5,'3–5'),(5,10,'5–10'),(10,20,'10–20'),(20,999,'20+')]
def curve(sel):
    o=[]
    for lo,hi,lab in BANDS:
        g=[x for x in sel if lo<=x['p']<hi]
        i=sum(x['i'] for x in g); c=sum(x['c'] for x in g)
        o.append(dict(band=lab,impr=i,clicks=c,ctr=round(100*c/i,3) if i else 0,n=len(g)))
    return o
C['ctr_brand']    = curve([x for x in qs if x['b']])
C['ctr_nonbrand'] = curve([x for x in qs if not x['b'] and 'civil union' not in x['q'].lower()])

# --- position buckets, non-brand commercial ---
C['buckets'] = [dict(band=k, **v) for k,v in M['nb_comm_buckets'].items()]

# --- impression concentration: top pages by impressions ---
pg = sorted([dict(u=re.sub(r'^https?://(www\.)?johnsonlgroup\.com','',x['u']).rstrip('/') or '/',
                  impr=x['impr'], clicks=x['clicks'], pos=x['pos'])
             for x in M['pages_90d_impr']], key=lambda x:-x['impr'])[:12]
C['impr_concentration'] = pg
C['pages_total_impr'] = M['pages_totals']['impr']
C['pages_total_clicks'] = M['pages_totals']['clicks']

# --- migration dumbbell ---
def short(u):
    s=u.split('/')[-1] or u
    return (s[:44]+'…') if len(s)>45 else s
C['migration'] = [dict(label=short(r['old']), old=r['old'], before=r['hist90'], after=r['now90'],
                       pct=r['pct'])
                  for r in sorted(MIG['migration_pairs'], key=lambda x:x['delta'])[:12]]
C['migration_total'] = dict(
    pairs=len(MIG['migration_pairs']),
    before=round(sum(r['hist90'] for r in MIG['migration_pairs'])),
    after=sum(r['now90'] for r in MIG['migration_pairs']))
# Report the INDEPENDENT set. 53 of the 103 gross "vanished" URLs are the old side of a
# migration pair and are already counted in C['migration_total'] — quoting the gross figure
# next to that table double-counts ~66% of the migration bucket.
_gross = MIG['vanished']; _ind = MIG['vanished_independent']
C['vanished'] = dict(
    n=len(_ind), clicks16=sum(g['clicks'] for g in _ind),
    rate90=round(sum(g['clicks'] for g in _ind)*90/487),
    gross_n=len(_gross), gross_clicks16=sum(g['clicks'] for g in _gross),
    gross_rate90=round(sum(g['clicks'] for g in _gross)*90/487),
    overlap_n=len(_gross)-len(_ind),
    overlap_clicks16=sum(g['clicks'] for g in _gross)-sum(g['clicks'] for g in _ind),
    top=[dict(u=g['u'], clicks=g['clicks'], impr=g['impr'])
         for g in sorted(_ind,key=lambda x:-x['clicks'])[:10]])

# --- GA4 conversion by segment ---
seg = M['ga4_segments']
order = ['Paid/LP (/lp/*, *-v2)','Contact/consult','City+service page','Homepage','Location page',
         'Practice area','Attorney bio','State/practice hub','Blog post','Video/webinar',
         'Pagination/taxonomy junk','Booking/scheduler URL']
C['ga4_conv'] = [dict(seg=k, **seg[k]) for k in order if k in seg]
C['ga4_totals'] = M['ga4_totals']
C['ga4_segments_all'] = seg

# --- thin pages ---
C['thin'] = [dict(p=x['p'], sess=x['sess'], sec=round(x['et'],1), ke=x['ke'])
             for x in M['ga4_thin'] if not x['p'].startswith(('/blog/2','/page/','/blog/page'))][:16]

# --- index bloat ---
C['bloat'] = [dict(k=k, **v) for k,v in M['index_bloat'].items()]
C['bloat'].append(dict(k='URLs with <=5 sessions', urls=M['ga4_longtail']['urls_le5_sessions'],
                       sessions=M['ga4_longtail']['sessions_from_le5'], key_events=0))
C['url_universe'] = M['ga4_url_count']

# --- geo ---
C['geo'] = M['geo_waste']
C['countries'] = M['countries_90d'][:10]
C['devices'] = M['devices_90d']

# --- AI features ---
C['ai'] = dict(total=M['ai']['total_impr'], share=M['ai']['share_of_all_impr'],
               cu=M['ai']['civil_union_impr'], devices=M['ai']['devices'],
               daily=M['ai']['daily'],
               top=[dict(u=re.sub(r'^https?://(www\.)?johnsonlgroup\.com','',x['u']).rstrip('/') or '/',
                         impr=x['impr']) for x in M['ai']['pages'][:10]])

# --- money terms table ---
C['money'] = [dict(q=x['q'], c=x['clicks'], i=x['impr'], p=x['pos'])
              for x in M['money_terms_top'][:22]]
C['striking'] = [dict(q=x['q'], c=x['clicks'], i=x['impr'], p=x['pos'])
                 for x in M['striking'][:20]]

# --- page segments (GSC) ---
C['gsc_segments'] = [dict(seg=k, **v) for k,v in M['page_segments'].items()]

json.dump(C, open(f'{H}/chartdata.json','w'), indent=1, default=str)
print("wrote chartdata.json")
print("months:", len(C['monthly']), "weeks:", len(C['weekly']))
print("\nCTR CURVE brand vs non-brand (same position bands):")
for a,b in zip(C['ctr_brand'], C['ctr_nonbrand']):
    print(f"  pos {a['band']:6} brand {a['ctr']:>6}% ({a['impr']:>6} impr) | non-brand {b['ctr']:>6}% ({b['impr']:>7} impr)")
print("\nmigration total:", C['migration_total'], "\nvanished:", {k:v for k,v in C['vanished'].items() if k!='top'})
print("\nGA4 conv by segment:")
for x in C['ga4_conv']: print(f"  {x['seg']:28} sess={x['sess']:>6} KE%={x['kr']:>6} eng%={x['engr']:>5} sec={x['et']:>6}")
