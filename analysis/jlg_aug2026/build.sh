#!/usr/bin/env bash
# Full rebuild. ORDER MATTERS: chartdata.py writes chartdata.json from scratch,
# then rankdash.py and ninetydash.py each read it and merge their own key back in.
# Running chartdata.py alone silently drops DATA.ranks and DATA.n90 and the
# dashboard throws on render. Always use this script.
set -euo pipefail
cd "$(dirname "$0")"

echo "1/6 core.py       (GSC + GA4 metrics)"        && python3 core.py       > /dev/null
echo "2/6 migration.py  (URL migration + vanished)" && python3 migration.py  > /dev/null
echo "3/6 chartdata.py  (writes chartdata.json)"    && python3 chartdata.py  > /dev/null
echo "4/6 ranks.py      (Semrush position tracking)"&& python3 ranks.py      > /dev/null
echo "5/6 rankdash.py   (merges DATA.ranks)"        && python3 rankdash.py   > /dev/null
echo "6/6 ninetydash.py (merges DATA.n90)"          && python3 ninetydash.py > /dev/null

python3 - <<'PY'
import json, sys
c = json.load(open('chartdata.json'))
need = ['monthly','weekly','mix','ctr_brand','migration','vanished','ga4_conv','bloat','ranks','n90']
missing = [k for k in need if k not in c]
if missing:
    sys.exit(f"FAIL: chartdata.json is missing {missing}")
html = open('dashboard_template.html').read().replace('__DATA__', json.dumps(c))
open('JLG-Organic-Diagnostic.html','w').write(html)
print(f"built JLG-Organic-Diagnostic.html  ({len(html)//1024} KB, all {len(need)} data keys present)")
PY
