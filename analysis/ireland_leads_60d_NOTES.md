# Michael Ireland & Associates — Lead Pull, Trailing 60 Days

**Pulled:** 2026-08-13 · **Window:** 2026-06-14 → 2026-08-13 · **Source project:** `sterlingx-insights`

## Files

| File | Rows | What it is |
|---|---|---|
| **`ireland_leads_60d_clean.csv`** | **250** | **Deliverable** — deduped, firm-internal records removed |
| `ireland_leads_60d.csv` | 283 | Raw pull, one row per `Origin_Lead_ID` |
| `ireland_leads_60d_deduped.csv` | 257 | Intermediate (phone pass only); superseded |
| `ireland_dedupe.py` | — | Dedupe pass, re-runnable, self-verifying |
| `ireland_leads_60d.sql` | — | The query, re-runnable |

Delivered copy: `~/Downloads/Ireland_Law_Leads_Last60Days_2026-08-13.csv`

### Dedupe accounting

```
  raw records                       283
  - firm-internal system records  -   6   wordpress@irelandfirm.com notifications
  - duplicate caller-ID rows      -  26   same phone, same day
  - duplicate rows                -   1   same email, no phone
  = clean leads                     250
```

**Not** deduped: records whose *name* is a caller-ID placeholder (`SAN ANTONIO TX`,
`WIRELESS CALLER`, `Unknown Caller`, `AVVO Unknown`). 49 rows share a name with another
row but carry **distinct phone numbers**, so they are distinct leads whose caller name was
never captured. Collapsing on name would have destroyed ~49 real leads.

## Source of record

`all_clients_offline_conversion.all_firms_offline_conversion` → filtered to
`SterlingX_Client_ID = 'a9b10ec7-4dfe-4058-bdb5-a53e66176eed'`.

This table is refreshed daily (last storage modification 2026-08-13) and is the only
Ireland lead source that is actually current. Cohort is defined by `Origin_Date_Created`
in the window, then **all** milestone rows for those leads are rolled up regardless of
event date — so a lead that arrived in the window but converted later still shows its
progression.

Actual data span of returned leads: **2026-06-15 → 2026-08-10**. The ~3-day gap at the
end is pipeline lag, so the final partial week (8 leads) is not yet complete.

## Headline numbers

| Metric | Clean | Raw |
|---|---|---|
| Leads | 250 | 283 |
| Consult scheduled | 70 (28.0%) | 70 (24.7%) |
| Qualified potential client | 1 | 1 |
| **Hired / funded agreement** | **0** | **0** |

Weekly lead volume is flat — 28–45/week with no trend. Consults scheduled swing
4–15/week on the same volume, which is a follow-up consistency signal, not a demand signal.

## Two gaps you asked about

### 1. Zip codes do not exist for these leads

There is no lead-level postal field in any Ireland source. Confirmed by scanning every
column in the project (`region-us.INFORMATION_SCHEMA.COLUMNS`) for
`zip`/`postal`. What exists and why none of it works:

- 14 other clients have `<client>.call_data.zip_code` from CallRail. **Ireland's
  `call_data` is a raw PBX/SIP CDR feed** (`call_type`, `orig_ip`, `release_cause`,
  `remote_number`) with no geographic field, and it stopped updating 2026-03-01.
- `clients.clients.postal_code` and `clients.client_profile_locations.zip_code` are the
  *firm's* address, not the lead's.
- `SterlingX_CM_Intake.people.postal_code` is the right shape but the entire
  `SterlingX_CM_*` schema is **empty (0 rows)**.
- The mapped live form source in `clients.clients.Web_Form_Summary_Mapping` is
  `rc-datamart-forms-webhook.webhook_wordpress_ireland.fct_webhook_wordpress_ireland_contactform_expanded`
  — a different GCP project. **Access denied** for cshea@rocketclicks.com. This is the
  most likely place a form-captured zip would live, and it is the one thing worth chasing.

`zip_code` is present as an explicitly empty column in both CSVs so the shape is stable
if the field is backfilled later.

### 2. "Hired" is structurally unavailable for Ireland

`Conversion_Status = 'Funded Agreement'` is the hired/retained signal in this pipeline.
Ireland has **zero such rows, all time** — not zero in the window. Nine other firms do
have them (Sterling Lawyers 18,920 · Meyerpink 1,622 · Johnson 1,061 · VDL 915 · Kalish
780 · SMB 229 · Fanash 179 · TDE 97 · Aurit 39), so this is an Ireland-specific
integration gap, not a table-wide one.

Ireland's furthest recorded stage is Consult Scheduled. The structural tell is in the
per-firm pipeline tables:

- `firm_origin_table` has 9 firms, **including `ireland_origin_table`** — lead ingestion
  is wired up.
- `firm_offline_conversion` has 8 firms, and **Ireland is the only one missing**
  (aurit, johnson, kalishandjaggars, meyerpink, slo, smb, tde, vdl all present).

Every firm with a `*_offline_conversion` table reports funded agreements. Ireland has the
origin half of the pipeline and not the conversion half, which is consistent with New
Leads and Consults Scheduled landing but the retainer stage never being built.

`clients.clients.CRM_Summary_Table_Mapping` is also null for Ireland, but that is *not*
the cause — Sterling Lawyers has a null mapping too and still reports 18,920 funded
agreements. Don't chase the mapping field alone.

**The 0 hires in these files means "not tracked," not "no clients signed."** Do not
report it as a performance number.

## Data quality flags

- **26 duplicate records (9% inflation).** The phone system writes a second lead row per
  inbound call using the caller-ID string — `STEEN RANCH`, `OGLESBY IL`,
  `WIRELESS CALLER`, `AVVO Unknown` — alongside the real named record with the same phone
  and date. 154 of 283 raw records have `Unknown` or ALL-CAPS caller-ID-style names.
  Use the deduped file for any rate that has leads in the denominator.
- **Email present on only 36%** (103/283). Phone is the reliable identifier at 96%.
- `utm_campaign` and `conversion_amount` are 100% null; `gclid` present on 7 records
  (2%). Paid attribution is effectively absent — 276 of 283 leads come in as
  `Origin_Platform = 'crm'` with no campaign data.
- `all_clients.web_form_leads` has 34 Ireland rows dated 2026-02-09 → 02-20 that are
  **webhook test submissions**, not leads (`testing 1 of 3`, `Ramage Contact form test`,
  `python-requests/2.32.5`, `tdeller45@yahoo.com`). Excluded here. Worth deleting.

## To close the gaps

1. Get read access to `rc-datamart-forms-webhook` — the only plausible zip source.
2. Build `firm_offline_conversion.ireland_offline_conversion` and wire the
   retainer/funded-agreement event, matching the 8 firms that already have one. Ireland is
   the only firm with an origin table but no conversion table.
3. Suppress caller-ID-only lead creation at the phone integration, or dedupe on
   normalized phone + date upstream.
