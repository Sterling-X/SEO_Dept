import csv, json
from datetime import datetime
from statistics import mean

rows=[]
with open('data/Chart.csv') as f:
    for r in csv.DictReader(f):
        rows.append({'d':r['Date'],'clicks':int(r['Clicks']),'impr':int(r['Impressions']),
                     'ctr':float(r['CTR'].strip('%')),'pos':float(r['Position'])})
rows.sort(key=lambda x:x['d'])

def roll(vals,i,w=7):
    s=vals[max(0,i-w+1):i+1]; return round(sum(s)/len(s),2)
clicks=[x['clicks'] for x in rows]; impr=[x['impr'] for x in rows]
pos=[x['pos'] for x in rows]; ctr=[x['ctr'] for x in rows]
daily=[]
for i,x in enumerate(rows):
    daily.append({'d':x['d'],'c':x['clicks'],'i':x['impr'],'ctr':x['ctr'],'p':x['pos'],
        'cR':roll(clicks,i),'iR':round(roll(impr,i)),'pR':roll(pos,i),'ctrR':roll(ctr,i)})

# monthly
from collections import defaultdict
mo=defaultdict(list)
for x in rows: mo[x['d'][:7]].append(x)
monthly=[]
for k in sorted(mo):
    m=mo[k]; c=sum(y['clicks'] for y in m); im=sum(y['impr'] for y in m)
    monthly.append({'m':k,'c':c,'i':im,'ctr':round(100*c/im,2),'p':round(mean(y['pos'] for y in m),1),'days':len(m)})

devices=[{'k':'Mobile','c':18050,'i':3233753,'ctr':0.56,'p':22.37},
         {'k':'Desktop','c':12087,'i':5489275,'ctr':0.22,'p':28.79},
         {'k':'Tablet','c':316,'i':97207,'ctr':0.33,'p':11.08}]

# GA4 channels excl Paid*, Referral, Cross-network, Display(paid)
# nu=new users, u=total users, eng=engaged sessions, engT=avg engagement time/user (s), ke=key events
channels=[{'k':'Organic Search','u':42220,'nu':54003,'eng':27539,'engT':102.8,'espu':0.65,'ke':5184},
          {'k':'Direct','u':52139,'nu':89185,'eng':20502,'engT':46.8,'espu':0.39,'ke':5110},
          {'k':'Organic Social','u':2172,'nu':3162,'eng':567,'engT':19.5,'espu':0.26,'ke':45},
          {'k':'Organic Video','u':40,'nu':46,'eng':23,'engT':27.3,'espu':0.58,'ke':1},
          {'k':'Organic Shopping','u':33,'nu':59,'eng':0,'engT':0,'espu':0,'ke':0},
          {'k':'AI Assistant','u':17,'nu':34,'eng':11,'engT':47.3,'espu':0.65,'ke':1}]

data={'daily':daily,'monthly':monthly,'devices':devices,'channels':channels}
with open('report_data.json','w') as f: json.dump(data,f,separators=(',',':'))
print("daily",len(daily),"monthly",len(monthly))
print("first",daily[0]['d'],"last",daily[-1]['d'])
# quick sanity: min/max rolling pos
print("min posR",min(d['pR'] for d in daily),"max posR",max(d['pR'] for d in daily))
print("bytes:", len(json.dumps(data)))
