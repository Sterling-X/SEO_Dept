import csv, json
from datetime import datetime, date
from statistics import mean

rows=[]
with open('data/Chart.csv') as f:
    for r in csv.DictReader(f):
        rows.append({
            'date': datetime.strptime(r['Date'],'%Y-%m-%d').date(),
            'clicks': int(r['Clicks']),
            'impr': int(r['Impressions']),
            'ctr': float(r['CTR'].strip('%')),
            'pos': float(r['Position']),
        })
rows.sort(key=lambda x:x['date'])
print("Range:", rows[0]['date'], "->", rows[-1]['date'], "| days:", len(rows))

# Monthly rollups
from collections import defaultdict
months=defaultdict(list)
for x in rows:
    months[(x['date'].year,x['date'].month)].append(x)

def ym(k): return f"{k[0]}-{k[1]:02d}"
print("\n=== MONTHLY (clicks sum, impr sum, ctr=clicks/impr, avg pos) ===")
print(f"{'Month':8} {'Clicks':>7} {'Impr':>9} {'CTR%':>6} {'AvgPos':>7} {'Days':>4}")
monthly=[]
for k in sorted(months):
    m=months[k]
    c=sum(x['clicks'] for x in m); i=sum(x['impr'] for x in m)
    ctr=100*c/i if i else 0
    p=mean(x['pos'] for x in m)
    monthly.append((ym(k),c,i,round(ctr,2),round(p,1),len(m)))
    print(f"{ym(k):8} {c:>7} {i:>9} {ctr:>6.2f} {p:>7.1f} {len(m):>4}")

# Period comparisons
def period(a,b):
    sel=[x for x in rows if a<=x['date']<=b]
    c=sum(x['clicks'] for x in sel); i=sum(x['impr'] for x in sel)
    days=len(sel)
    return dict(clicks=c,impr=i,ctr=round(100*c/i,3),pos=round(mean(x['pos'] for x in sel),1),
                days=days, cpd=round(c/days,1), ipd=round(i/days,0))

print("\n=== KEY PERIODS ===")
periods={
 'Baseline Mar20-Aug12 2025 (pre-visibility-shift)': period(date(2025,3,20),date(2025,8,12)),
 'Position-jump era Aug13-Sep11 2025': period(date(2025,8,13),date(2025,9,11)),
 'Post-jump Sep12-Dec31 2025': period(date(2025,9,12),date(2025,12,31)),
 'Q4 2025 (Oct-Dec)': period(date(2025,10,1),date(2025,12,31)),
 'Pre-agency 90d (Dec-Feb)': period(date(2025,12,1),date(2026,2,28)),
 'Agency era Mar1-Jul19 2026': period(date(2026,3,1),date(2026,7,19)),
 'Last 30d (Jun20-Jul19 2026)': period(date(2026,6,20),date(2026,7,19)),
}
for name,p in periods.items():
    print(f"{name}\n   clicks/day={p['cpd']} impr/day={p['ipd']:.0f} CTR={p['ctr']}% pos={p['pos']} (n={p['days']})")

# Same-window YoY: Mar20-Jul19 2025 vs 2026
y25=period(date(2025,3,20),date(2025,7,19))
y26=period(date(2026,3,20),date(2026,7,19))
print("\n=== YoY same window (Mar20-Jul19) ===")
print("2025:",y25)
print("2026:",y26)
print("clicks/day chg %:", round(100*(y26['cpd']-y25['cpd'])/y25['cpd'],1))
print("impr/day chg %:", round(100*(y26['ipd']-y25['ipd'])/y25['ipd'],1))
print("pos chg (pts, neg=better):", round(y26['pos']-y25['pos'],1))

# export monthly json for the report
with open('monthly.json','w') as f:
    json.dump(monthly,f)
print("\nwrote monthly.json")
