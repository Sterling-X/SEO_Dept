Drop the PRIOR-90 Search Console export here, then run:  python3 ninety_compare.py

  Search Console -> Performance -> Search results
  Date range -> Custom -> 2026-02-12 to 2026-05-12
  (Do not use a preset. "Last 3 months" gives you the CURRENT window, not the prior one.)
  Export -> Download CSV -> unzip the whole folder into this directory.

Expected files: Chart.csv  Pages.csv  Queries.csv  Devices.csv  Countries.csv
That single export unblocks the page-, query-, device- and country-level 90-over-90.
