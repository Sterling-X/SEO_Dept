-- Michael Ireland & Associates ("Ireland Law") — lead-level detail, trailing 60 days
-- Cohort definition: leads whose Origin_Date_Created falls in 2026-06-14 .. 2026-08-13.
-- All milestone events for those leads are rolled up, regardless of event date, so a
-- lead that came in during the window but converted later still shows its progression.
WITH cohort AS (
  SELECT *
  FROM `sterlingx-insights.all_clients_offline_conversion.all_firms_offline_conversion`
  WHERE SterlingX_Client_ID = 'a9b10ec7-4dfe-4058-bdb5-a53e66176eed'
    AND SAFE.PARSE_DATE('%Y-%m-%d', SUBSTR(Origin_Date_Created, 1, 10))
        BETWEEN DATE('2026-06-14') AND DATE('2026-08-13')
),
rolled AS (
  SELECT
    Origin_Lead_ID                                                        AS lead_id,
    ANY_VALUE(Origin_System_Lead_ID)                                      AS system_lead_id,
    ANY_VALUE(Origin_Platform)                                            AS lead_platform,
    MIN(SUBSTR(Origin_Date_Created, 1, 19))                               AS lead_created_at,
    SAFE.PARSE_DATE('%Y-%m-%d', SUBSTR(MIN(Origin_Date_Created), 1, 10))  AS lead_created_date,

    -- Identity: Origin (webhook/CRM capture) preferred, CRM record as fallback
    COALESCE(ANY_VALUE(NULLIF(Origin_First_Name, '')), ANY_VALUE(NULLIF(CRM_First_Name, ''))) AS first_name,
    COALESCE(ANY_VALUE(NULLIF(Origin_Last_Name, '')),  ANY_VALUE(NULLIF(CRM_Last_Name, '')))  AS last_name,
    COALESCE(ANY_VALUE(NULLIF(Origin_Email_Name, '')), ANY_VALUE(NULLIF(CRM_Email, '')))      AS email,
    COALESCE(ANY_VALUE(NULLIF(Origin_Phone_Number, '')), ANY_VALUE(NULLIF(CRM_Phone_Number, ''))) AS phone,

    -- Zip code: no lead-level postal field exists in this source (see notes)
    CAST(NULL AS STRING)                                                  AS zip_code,

    -- Attribution
    COALESCE(ANY_VALUE(NULLIF(Origin_Marketing_UTM_Campaign, '')),
             ANY_VALUE(NULLIF(CRM_Marketing_UTM_Campaign, '')))           AS utm_campaign,
    MAX(CASE WHEN COALESCE(Origin_GCLID, '') != '' THEN 1 ELSE 0 END) = 1 AS has_gclid,
    ANY_VALUE(NULLIF(Origin_GCLID, ''))                                   AS gclid,
    ANY_VALUE(NULLIF(Origin_GBRAID, ''))                                  AS gbraid,

    -- Funnel milestones
    MIN(CASE WHEN Conversion_Status = 'New Leads' THEN Conversion_Event_Date END)                   AS new_lead_date,
    MIN(CASE WHEN Conversion_Status = 'Qualified Potential Clients' THEN Conversion_Event_Date END) AS qualified_date,
    MIN(CASE WHEN Conversion_Status = 'Consults Scheduled' THEN Conversion_Event_Date END)          AS consult_scheduled_date,
    MIN(CASE WHEN Conversion_Status = 'Consults Complete' THEN Conversion_Event_Date END)           AS consult_complete_date,
    MIN(CASE WHEN Conversion_Status = 'Funded Agreement' THEN Conversion_Event_Date END)            AS funded_agreement_date,

    -- "Hired" == Funded Agreement in this pipeline
    MAX(CASE WHEN Conversion_Status = 'Funded Agreement' THEN 1 ELSE 0 END) = 1 AS is_hired,

    MAX(SAFE_CAST(Conversion_Amount AS FLOAT64))                          AS conversion_amount,
    ANY_VALUE(NULLIF(Conversion_Notes, ''))                               AS conversion_notes,
    ANY_VALUE(NULLIF(CRM_Record_ID, ''))                                  AS crm_record_id,
    STRING_AGG(DISTINCT Conversion_Status, ' | ' ORDER BY Conversion_Status) AS all_statuses,
    COUNT(*)                                                              AS event_row_count
  FROM cohort
  GROUP BY Origin_Lead_ID
)
SELECT
  lead_id, system_lead_id, crm_record_id, lead_platform,
  lead_created_at, lead_created_date,
  first_name, last_name, email, phone, zip_code,
  utm_campaign, has_gclid, gclid, gbraid,
  new_lead_date, qualified_date, consult_scheduled_date,
  consult_complete_date, funded_agreement_date,
  is_hired,
  CASE
    WHEN funded_agreement_date  IS NOT NULL THEN '5 - Funded Agreement (Hired)'
    WHEN consult_complete_date  IS NOT NULL THEN '4 - Consult Complete'
    WHEN consult_scheduled_date IS NOT NULL THEN '3 - Consult Scheduled'
    WHEN qualified_date         IS NOT NULL THEN '2 - Qualified'
    ELSE '1 - New Lead'
  END AS furthest_stage,
  conversion_amount, conversion_notes, all_statuses, event_row_count
FROM rolled
ORDER BY lead_created_at DESC
