import csv,re
from collections import defaultdict
rows=[]
with open('data/Pages.csv') as f:
    for r in csv.DictReader(f):
        rows.append({'url':r['Top pages'],'c':int(r['Clicks']),'i':int(r['Impressions']),'p':float(r['Position'])})
print("Pages parsed (subset of full export):",len(rows))
tot_c=sum(r['c'] for r in rows); tot_i=sum(r['i'] for r in rows)
print(f"Clicks {tot_c:,} | Impressions {tot_i:,}")

# 1) content age by /blog/YYYY/
yr=defaultdict(lambda:[0,0,0])
blog=0
for r in rows:
    m=re.search(r'/blog/(20\d\d)/',r['url'])
    if m:
        blog+=1; y=m.group(1); yr[y][0]+=1; yr[y][1]+=r['c']; yr[y][2]+=r['i']
print(f"\n=== BLOG CONTENT AGE ({blog} blog URLs in subset) ===")
print(f"{'Year':6}{'Pages':>7}{'Clicks':>9}{'Impr':>10}")
for y in sorted(yr): print(f"{y:6}{yr[y][0]:>7}{yr[y][1]:>9,}{yr[y][2]:>10,}")

# 2) www vs non-www duplication
def norm(u):
    u=re.sub(r'^https?://','',u); u=re.sub(r'^www\.','',u); u=u.split('?')[0]; return u.rstrip('/')
seen=defaultdict(list)
for r in rows: seen[norm(r['url'])].append(r)
wwwdupe=[k for k,v in seen.items() if len(v)>1]
print(f"\n=== www / non-www (or exact) DUPLICATE PATHS: {len(wwwdupe)} ===")
for k in wwwdupe[:12]:
    print(" ",k,"->",[f"{x['c']}cl p{x['p']}" for x in seen[k]])

# 3) truncated-slug near-duplicates (one slug is prefix of another, same dir)
def key(u):
    path=norm(u)
    return path
slugs=[(norm(r['url']),r) for r in rows]
dupe_pairs=[]
for a_path,a in slugs:
    for b_path,b in slugs:
        if a_path!=b_path and len(a_path)<len(b_path) and b_path.startswith(a_path) and len(a_path)>25:
            # avoid dir-vs-child by requiring the tail to be a slug continuation (no extra '/')
            if '/' not in b_path[len(a_path):]:
                dupe_pairs.append((a_path,a,b_path,b))
# dedupe
uniq=set()
print(f"\n=== TRUNCATED-SLUG / OVERLAPPING PAIRS (sample) ===")
cnt=0
for ap,a,bp,b in dupe_pairs:
    kk=(ap,bp)
    if kk in uniq: continue
    uniq.add(kk); cnt+=1
    if cnt<=14:
        print(f"  {a['c']}cl p{a['p']}  {ap[-55:]}\n      vs {b['c']}cl p{b['p']}  {bp[-55:]}")
print(f"  ...total overlapping prefix pairs: {cnt}")

# 4) high-impression but poor rank (decay / misaligned)
decay=[r for r in rows if r['i']>=20000 and r['p']>20]
decay.sort(key=lambda x:-x['i'])
print(f"\n=== HIGH IMPRESSIONS (>=20k) BUT POSITION >20  (misaligned/decayed): {len(decay)} pages ===")
for r in decay[:15]:
    print(f"  {r['i']:>8,} impr  p{r['p']:>5}  {r['c']:>4}cl  {norm(r['url'])[:70]}")
