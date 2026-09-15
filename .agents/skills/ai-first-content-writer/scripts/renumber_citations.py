#!/usr/bin/env python3
"""Renumber source citations by order of first appearance."""

import json

d=json.load(open('content.json'))
order=[]
def runs_of(b):
    if b['t']=='p': return b['runs']
    if b['t'] in ('ul','ol'):
        return [r for it in b['items'] if isinstance(it,dict) for r in it['runs']]
    return []
for b in d['blocks']:
    for r in runs_of(b):
        if 'cite' in r and r['cite'] not in order: order.append(r['cite'])
remap={old:new for new,old in enumerate(order, start=1)}
for b in d['blocks']:
    for r in runs_of(b):
        if 'cite' in r:
            r['cite']=remap[r['cite']]; r['text']=f"[{r['cite']}]"
src={s['n']:s for s in d['sources']}
d['sources']=[{**src[o],'n':n} for o,n in sorted(remap.items(), key=lambda kv: kv[1])]
json.dump(d, open('content.json','w'), indent=2)
print(f"renumbered {len(order)} citations in appearance order")
