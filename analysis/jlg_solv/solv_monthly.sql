-- Johnson Law Group: SoLV month over month by location.
-- Source: sterlingx-insights.firm_marketing_localbrandmanager.johnsonlaw_localbrandmanager_geogrids
-- SoLV is stored as a 0-1 fraction; output is a percentage.
--
-- Location key is geogrid_config_id, NOT business_place_id/address/store_code:
--   * Englewood switched from a street address to "Service Area Business" on 2026-07-13
--   * Cheyenne appears under 3 name/address spellings
--   * Chicago has a NULL store_code
-- config_id is stable 1:1 with location across all 687 rows.
--
-- Stage 1  dedupe the 2026-03-20 double scan (12 pairs, ~4 min apart) by averaging
--          within (location, term, day)
-- Stage 2  average across each location's consistently-tracked terms -> daily SoLV.
--          Fort Collins added 'divorce attorney' + 'fort collins divorce attorney'
--          on 2026-06-01; excluded so the trend is like-for-like.
-- Stage 3  keep only complete scan days (all 4 consistent terms). Drops 2026-05-27,
--          where 3 locations recorded a single term each.
-- Stage 4  average scan days within the month, so a month is not weighted by how
--          many times the scanner happened to run.
WITH g AS (
  SELECT geogrid_config_id AS cfg, search_term, solv,
         DATE(geogrid_created_at) AS scan_date
  FROM `sterlingx-insights.firm_marketing_localbrandmanager.johnsonlaw_localbrandmanager_geogrids`
),
loc_start AS (
  SELECT cfg, MIN(scan_date) AS first_scan FROM g GROUP BY 1
),
consistent_terms AS (
  SELECT g.cfg, g.search_term
  FROM g JOIN loc_start l USING (cfg)
  GROUP BY 1, 2
  HAVING MIN(g.scan_date) = ANY_VALUE(l.first_scan)
),
labelled AS (
  SELECT g.* FROM g JOIN consistent_terms t USING (cfg, search_term)
),
per_term_day AS (
  SELECT cfg, search_term, scan_date, AVG(solv) AS solv
  FROM labelled GROUP BY 1, 2, 3
),
per_day AS (
  SELECT cfg, scan_date, AVG(solv) AS day_solv, COUNT(DISTINCT search_term) AS terms
  FROM per_term_day GROUP BY 1, 2
),
complete_days AS (
  SELECT * FROM per_day WHERE terms = 4
),
labels AS (
  SELECT geogrid_config_id AS cfg,
         ARRAY_AGG(business_address ORDER BY geogrid_created_at DESC LIMIT 1)[OFFSET(0)] AS latest_addr
  FROM `sterlingx-insights.firm_marketing_localbrandmanager.johnsonlaw_localbrandmanager_geogrids`
  GROUP BY 1
)
SELECT
  c.cfg,
  b.latest_addr,
  FORMAT_DATE('%Y-%m', c.scan_date) AS mo,
  ROUND(AVG(c.day_solv) * 100, 2) AS solv_pct,
  COUNT(*) AS scan_days
FROM complete_days c JOIN labels b USING (cfg)
GROUP BY 1, 2, 3
ORDER BY b.latest_addr, mo
