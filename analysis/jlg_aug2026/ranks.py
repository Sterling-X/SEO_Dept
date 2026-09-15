#!/usr/bin/env python3
"""Semrush position-tracking forensics: 5 city projects, 2026-03-25 -> 2026-08-11."""
import csv, json, re, os, glob
from collections import defaultdict, Counter

H = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(H, 'data', 'ranks')

def load(path):
    with open(path, encoding='utf-8-sig') as f:
        lines = f.read().split('\n')
    # skip the 4-line preamble block delimited by dashed rules
    start = 0
    for i, l in enumerate(lines):
        if l.startswith('Keyword,'):
            start = i; break
    rows = list(csv.DictReader(lines[start:]))
    hdr = list(csv.reader([lines[start]]))[0]
    dates = []
    for c in hdr:
        m = re.search(r'_(\d{8})$', c)
        if m and not c.endswith('_type') and not c.endswith('_landing'):
            dates.append((c, m.group(1)))
    return rows, dates, hdr

def norm(u):
    if not u: return ''
    return re.sub(r'^https?://(www\.)?johnsonlgroup\.com', '', u).split('?')[0]

# URL architecture classes
def arch(u):
    p = norm(u)
    if not p: return None
    if p.startswith('/colorado/locations/') or p.startswith('/wyoming/locations/'): return 'nested-city'
    if p.startswith('/colorado/') or p.startswith('/wyoming/'): return 'nested-state'
    if p.startswith('/practice-areas/'): return 'practice-areas'
    if p.startswith('/blog/'): return 'blog'
    if p in ('/', ''): return 'homepage'
    if re.match(r'^/[a-z-]+-(lawyer|attorney)/?$', p): return 'flat-legacy'
    return 'other'

CITY = re.compile(r'/locations/([a-z-]+)/')
def city_of(u):
    m = CITY.search(norm(u))
    return m.group(1) if m else None

files = sorted(glob.glob(f'{D}/*.csv'))
projects = []

for path in files:
    rows, dates, hdr = load(path)
    pid = re.search(r'_(\d+)_position', path).group(1)
    # infer the project's city from most common landing city
    cc = Counter()
    for r in rows:
        for col, dt in dates:
            u = r.get(col + '_landing') or ''
            c = city_of(u)
            if c: cc[c] += 1
    label = cc.most_common(1)[0][0] if cc else 'unknown'
    projects.append(dict(pid=pid, label=label, rows=rows, dates=dates, path=path))
    print(f"{pid}  {label:16} keywords={len(rows):4}  dates={len(dates)}  span {dates[0][1]}->{dates[-1][1]}")

print()

# ---------- 1. architecture switchover timeline ----------
arch_by_date = defaultdict(Counter)
for pr in projects:
    for r in pr['rows']:
        for col, dt in pr['dates']:
            a = arch(r.get(col + '_landing') or '')
            if a: arch_by_date[dt][a] += 1

print("URL ARCHITECTURE OF RANKING PAGES OVER TIME (count of keyword-days)")
print(f"{'date':10} {'flat-legacy':>11} {'nested-city':>11} {'nested-state':>12} {'practice':>9} {'blog':>6} {'home':>5} {'total':>6}")
arch_series = []
for dt in sorted(arch_by_date):
    c = arch_by_date[dt]; tot = sum(c.values())
    arch_series.append(dict(d=dt, flat=c['flat-legacy'], nested=c['nested-city'],
                            nstate=c['nested-state'], pa=c['practice-areas'],
                            blog=c['blog'], home=c['homepage'], total=tot))
    if dt in ('20260325','20260401','20260408','20260415','20260422','20260506','20260603','20260701','20260801','20260811'):
        print(f"{dt:10} {c['flat-legacy']:>11} {c['nested-city']:>11} {c['nested-state']:>12} "
              f"{c['practice-areas']:>9} {c['blog']:>6} {c['homepage']:>5} {tot:>6}")

# ---------- 2. per-keyword first vs last ----------
def series(r, dates):
    out = []
    for col, dt in dates:
        v = (r.get(col) or '').strip()
        if v and v != '-':
            try: out.append((dt, int(v), (r.get(col+'_type') or '').strip(), norm(r.get(col+'_landing') or '')))
            except ValueError: pass
    return out

def num(s):
    s = (s or '').strip().replace(',','')
    try: return float(s)
    except: return 0.0

kw = []
for pr in projects:
    for r in pr['rows']:
        s = series(r, pr['dates'])
        if not s: continue
        # baseline = mean of first 3 observations in the first 2 weeks; current = mean of last 3
        early = [x for x in s if x[0] <= '20260408'][:4]
        late  = [x for x in s if x[0] >= '20260801']
        if not early or not late: continue
        b = sum(x[1] for x in early)/len(early)
        c = sum(x[1] for x in late)/len(late)
        kw.append(dict(
            city=pr['label'], k=r['Keyword'], intent=r.get('Intents',''),
            vol=num(r.get('Search Volume')), cpc=num(r.get('CPC')), kd=num(r.get('Keyword Difficulty')),
            base=round(b,1), now=round(c,1), delta=round(c-b,1),
            n_obs=len(s), first=s[0], last=s[-1],
            types=Counter(x[2] for x in s),
            lands=Counter(x[3] for x in s),
            churn=len(set(x[3] for x in s)),
            base_url=early[0][3], now_url=late[-1][3],
        ))

print(f"\nkeyword-city rows with both an early and an August reading: {len(kw)}")

# ---------- 3. SERP feature mix by city ----------
print("\nSERP FEATURE MIX BY CITY PROJECT (share of ranking observations)")
print(f"{'city':16} {'obs':>7} {'organic':>8} {'local':>8} {'ai ovw':>8} {'sitelnk':>8}")
feat = {}
for pr in projects:
    c = Counter()
    for r in pr['rows']:
        for x in series(r, pr['dates']): c[x[2]] += 1
    t = sum(c.values()) or 1
    feat[pr['label']] = dict(obs=t, organic=round(100*c['organic']/t,1), local=round(100*c['local']/t,1),
                             ai=round(100*c['ai overview']/t,1), sl=round(100*c['site links']/t,1),
                             raw=dict(c))
    f = feat[pr['label']]
    print(f"{pr['label']:16} {t:>7} {f['organic']:>7}% {f['local']:>7}% {f['ai']:>7}% {f['sl']:>7}%")

# ---------- 4. biggest commercial declines, weighted by volume ----------
comm = [x for x in kw if x['vol'] >= 10]
dec = sorted([x for x in comm if x['delta'] > 3], key=lambda x: -(x['delta']*max(x['vol'],10)))
print(f"\nBIGGEST VOLUME-WEIGHTED DECLINES (base -> now, positions; + = worse)")
print(f"{'city':14} {'keyword':42} {'vol':>5} {'CPC':>7} {'base':>6} {'now':>6} {'chg':>6}  base URL -> now URL")
for x in dec[:24]:
    print(f"{x['city']:14} {x['k'][:42]:42} {int(x['vol']):>5} {x['cpc']:>7.2f} {x['base']:>6} {x['now']:>6} {x['delta']:>+6} "
          f" {x['base_url'][:38]} -> {x['now_url'][:38]}")

imp = sorted([x for x in comm if x['delta'] < -3], key=lambda x: (x['delta']*max(x['vol'],10)))
print(f"\nBIGGEST VOLUME-WEIGHTED IMPROVEMENTS")
for x in imp[:12]:
    print(f"{x['city']:14} {x['k'][:42]:42} {int(x['vol']):>5} {x['cpc']:>7.2f} {x['base']:>6} {x['now']:>6} {x['delta']:>+6}")

# ---------- 5. did the URL architecture change hurt? ----------
switched = [x for x in kw if arch(x['base_url'])=='flat-legacy' and arch(x['now_url']) in ('nested-city','nested-state')]
stayed   = [x for x in kw if arch(x['base_url'])==arch(x['now_url'])]
def avg(l,f): return round(sum(f(x) for x in l)/len(l),2) if l else 0
print(f"\nMIGRATION EFFECT — keywords whose ranking URL moved flat-legacy -> nested")
print(f"  switched: n={len(switched):4}  avg base pos {avg(switched,lambda x:x['base']):>6}  avg now {avg(switched,lambda x:x['now']):>6}  avg change {avg(switched,lambda x:x['delta']):>+6}")
print(f"  unchanged arch: n={len(stayed):4}  avg base pos {avg(stayed,lambda x:x['base']):>6}  avg now {avg(stayed,lambda x:x['now']):>6}  avg change {avg(stayed,lambda x:x['delta']):>+6}")

# ---------- 6. landing page churn (cannibalisation) ----------
churny = sorted([x for x in kw if x['churn'] >= 3], key=lambda x: -x['churn'])
print(f"\nLANDING-PAGE CHURN — Google keeps swapping which page ranks")
print(f"  keywords tracked with >=3 different ranking URLs: {len(churny)} of {len(kw)} ({round(100*len(churny)/len(kw))}%)")
print(f"  >=5 different URLs: {len([x for x in kw if x['churn']>=5])}")
for x in churny[:10]:
    top = ', '.join(f"{u.split('/')[-2] if u.endswith('/') else u.split('/')[-1]}({n})" for u,n in x['lands'].most_common(4))
    print(f"   {x['churn']:>2} URLs  {x['city']:13} {x['k'][:40]:40}  {top}")

# ---------- 7. AI Overview citations ----------
ai_pages = Counter(); ai_kw = defaultdict(set); ai_by_date = Counter()
for pr in projects:
    for r in pr['rows']:
        for dt, pos, typ, u in series(r, pr['dates']):
            if typ == 'ai overview':
                ai_pages[u] += 1; ai_kw[u].add((pr['label'], r['Keyword'])); ai_by_date[dt] += 1
print(f"\nAI OVERVIEW CITATIONS — {sum(ai_pages.values())} keyword-days across {len(ai_pages)} distinct URLs")
print(f"  keywords ever cited: {len(set(k for s in ai_kw.values() for k in s))}")
for u, n in ai_pages.most_common(12):
    print(f"   {n:>4} days  {u[:70]:70} ({len(ai_kw[u])} kws)")
print("  AI-overview citations by month:", dict(sorted(Counter(d[:6] for d,c in ai_by_date.items() for _ in range(c)).items())))

# ---------- 8. local pack dependence ----------
print("\nLOCAL PACK vs ORGANIC — for keywords currently in the top 3")
for pr in projects:
    top3 = []
    for r in pr['rows']:
        s = series(r, pr['dates'])
        late = [x for x in s if x[0] >= '20260801']
        if late and sum(x[1] for x in late)/len(late) <= 3:
            top3.append(Counter(x[2] for x in late).most_common(1)[0][0])
    c = Counter(top3)
    print(f"  {pr['label']:16} top-3 keywords={len(top3):>3}   local={c['local']:>3}  organic={c['organic']:>3}  ai overview={c['ai overview']:>3}")

out = dict(
  arch_series=arch_series, feat=feat,
  decliners=[{k:v for k,v in x.items() if k not in ('types','lands','first','last')} for x in dec[:30]],
  improvers=[{k:v for k,v in x.items() if k not in ('types','lands','first','last')} for x in imp[:15]],
  migration_effect=dict(
      switched_n=len(switched), switched_base=avg(switched,lambda x:x['base']),
      switched_now=avg(switched,lambda x:x['now']), switched_delta=avg(switched,lambda x:x['delta']),
      stayed_n=len(stayed), stayed_base=avg(stayed,lambda x:x['base']),
      stayed_now=avg(stayed,lambda x:x['now']), stayed_delta=avg(stayed,lambda x:x['delta'])),
  churn=dict(total=len(kw), ge3=len(churny), ge5=len([x for x in kw if x['churn']>=5]),
             top=[dict(city=x['city'], k=x['k'], n=x['churn'],
                       urls=[u for u,_ in x['lands'].most_common(6)]) for x in churny[:14]]),
  ai=dict(total_days=sum(ai_pages.values()), urls=len(ai_pages),
          kws=len(set(k for s in ai_kw.values() for k in s)),
          top=[dict(u=u, days=n, kws=len(ai_kw[u])) for u,n in ai_pages.most_common(14)]),
  keywords=[{k:v for k,v in x.items() if k not in ('types','lands','first','last')} for x in kw],
)
json.dump(out, open(f'{H}/ranks.json','w'), indent=1, default=str)
print(f"\nwrote ranks.json  ({len(kw)} keyword rows)")
