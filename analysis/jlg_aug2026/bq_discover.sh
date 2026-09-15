#!/usr/bin/env bash
# Find the Johnson Law Group data in BigQuery.
# Run AFTER: gcloud auth login
# Read-only: lists projects, datasets and tables, and peeks at row counts / date ranges.
set -uo pipefail

echo "=========================================================================="
echo "ACCOUNT / PROJECT"
echo "=========================================================================="
gcloud config list --format="value(core.account,core.project)" 2>/dev/null

echo
echo "=========================================================================="
echo "PROJECTS"
echo "=========================================================================="
gcloud projects list --format="table(projectId,name)" 2>&1 | head -40

echo
echo "=========================================================================="
echo "DATASETS PER PROJECT"
echo "=========================================================================="
for p in $(gcloud projects list --format="value(projectId)" 2>/dev/null); do
  ds=$(bq --project_id="$p" ls --max_results=200 2>/dev/null | tail -n +3 | awk '{print $1}')
  [ -z "$ds" ] && continue
  echo "--- $p ---"
  for d in $ds; do
    echo "  $d"
  done
done

echo
echo "=========================================================================="
echo "TABLES THAT LOOK LIKE SEARCH CONSOLE / GA4 / JLG"
echo "=========================================================================="
for p in $(gcloud projects list --format="value(projectId)" 2>/dev/null); do
  for d in $(bq --project_id="$p" ls --max_results=200 2>/dev/null | tail -n +3 | awk '{print $1}'); do
    bq --project_id="$p" ls --max_results=500 "$d" 2>/dev/null | tail -n +3 | awk '{print $1}' \
      | grep -iE "searchdata|events_|ga4|analytics|johnson|jlg|gsc|search_console" \
      | sed "s|^|  $p.$d.|" | sort -u | head -12
  done
done
echo
echo "NOTE: GA4 exports appear as events_YYYYMMDD (one table per day, often 400+ tables)."
echo "      GSC bulk exports appear as searchdata_site_impression / searchdata_url_impression."
echo "      Both are date-partitioned, which means a TRUE 90-over-90 on any dimension."
