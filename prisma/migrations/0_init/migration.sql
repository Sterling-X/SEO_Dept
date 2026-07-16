-- CreateSchema
CREATE SCHEMA IF NOT EXISTS "public";

-- CreateEnum
CREATE TYPE "TemplateType" AS ENUM ('SEO_VISIBILITY', 'LOCAL_SEO', 'CONTENT_AUTHORITY', 'PAID_SEARCH', 'MULTI_CHANNEL');

-- CreateEnum
CREATE TYPE "ImportSourceType" AS ENUM ('SEMRUSH_VISIBILITY', 'SEMRUSH_MAP_PACK', 'SEMRUSH_ORGANIC', 'GSC_QUERY', 'SEMRUSH_RANKINGS_OVERVIEW', 'GSC_PERFORMANCE_ZIP');

-- CreateEnum
CREATE TYPE "ImportJobStatus" AS ENUM ('PENDING', 'PREVIEWED', 'VALIDATED', 'COMMITTED', 'FAILED', 'REPLACED');

-- CreateEnum
CREATE TYPE "KeywordType" AS ENUM ('LOCAL', 'CORE', 'BRANDED', 'OTHER');

-- CreateEnum
CREATE TYPE "ExclusionMatchType" AS ENUM ('CONTAINS', 'EXACT', 'STARTS_WITH', 'ENDS_WITH', 'REGEX');

-- CreateEnum
CREATE TYPE "IssueSeverity" AS ENUM ('ERROR', 'WARNING', 'INFO');

-- CreateEnum
CREATE TYPE "IssueStatus" AS ENUM ('OPEN', 'RESOLVED', 'IGNORED');

-- CreateEnum
CREATE TYPE "DataHealthIssueType" AS ENUM ('UNMAPPED_KEYWORD', 'MISSING_REQUIRED_FIELD', 'DUPLICATE_KEYWORD', 'MISSING_COMPETITOR_MAPPING', 'MISSING_MARKET_VALUE', 'INCOMPLETE_KEYWORD_PAIR', 'DATE_INCONSISTENCY', 'EMPTY_IMPORT', 'KEYWORD_NOT_IN_PROJECT_SET', 'UNDETECTED_BRANDED_QUERY', 'RANK_OUTLIER', 'IMPORT_ERROR', 'FAILED_HEADER_DETECTION', 'MALFORMED_GROUP_HEADER', 'INVALID_RANKING_VALUE', 'MISSING_IMPORT_METADATA', 'DUPLICATE_IMPORT_PERIOD', 'MISSING_GSC_COMPONENT', 'UNDETECTED_PAGE_SPECIFIC_QUERY');

-- CreateTable
CREATE TABLE "reporting_templates" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "description" TEXT,
    "templateType" "TemplateType" NOT NULL,
    "requiredSources" JSONB NOT NULL,
    "supportedMetrics" JSONB NOT NULL,
    "requiredKeywordFields" JSONB NOT NULL,
    "defaultDashboards" JSONB NOT NULL,
    "defaultQAChecks" JSONB NOT NULL,
    "defaultExclusionCategories" JSONB NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "reporting_templates_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "projects" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "industry" TEXT,
    "category" TEXT,
    "domain" TEXT NOT NULL,
    "normalizedDomain" TEXT NOT NULL,
    "description" TEXT,
    "templateId" TEXT,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "projects_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "markets" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "normalizedName" TEXT NOT NULL,
    "region" TEXT,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "markets_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "intent_groups" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "normalizedName" TEXT NOT NULL,
    "description" TEXT,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "intent_groups_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "keyword_sets" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "keyword_sets_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "keywords" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "keywordSetId" TEXT,
    "marketId" TEXT,
    "intentGroupId" TEXT,
    "text" TEXT NOT NULL,
    "normalizedText" TEXT NOT NULL,
    "keywordType" "KeywordType" NOT NULL,
    "isPrimaryTarget" BOOLEAN NOT NULL DEFAULT false,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "notes" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "keywords_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "keyword_pairs" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "localKeywordId" TEXT NOT NULL,
    "coreKeywordId" TEXT NOT NULL,
    "notes" TEXT,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "keyword_pairs_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "competitors" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "domain" TEXT NOT NULL,
    "normalizedDomain" TEXT NOT NULL,
    "name" TEXT,
    "isPrimary" BOOLEAN NOT NULL DEFAULT false,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "competitors_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "import_mapping_profiles" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "sourceType" "ImportSourceType" NOT NULL,
    "name" TEXT NOT NULL,
    "mapping" JSONB NOT NULL,
    "requiredFields" JSONB NOT NULL,
    "isDefault" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "import_mapping_profiles_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "import_jobs" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "mappingProfileId" TEXT,
    "sourceType" "ImportSourceType" NOT NULL,
    "status" "ImportJobStatus" NOT NULL DEFAULT 'PENDING',
    "fileName" TEXT NOT NULL,
    "fileSize" INTEGER,
    "mimeType" TEXT,
    "uploadDate" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "originalHeaders" JSONB,
    "columnMappings" JSONB,
    "rowCount" INTEGER NOT NULL DEFAULT 0,
    "validRowCount" INTEGER NOT NULL DEFAULT 0,
    "errorCount" INTEGER NOT NULL DEFAULT 0,
    "warningCount" INTEGER NOT NULL DEFAULT 0,
    "replaceExisting" BOOLEAN NOT NULL DEFAULT false,
    "summary" JSONB,
    "committedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "import_jobs_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "import_validation_issues" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "rowNumber" INTEGER,
    "field" TEXT,
    "severity" "IssueSeverity" NOT NULL,
    "code" TEXT,
    "message" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "import_validation_issues_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "raw_import_files" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "originalName" TEXT NOT NULL,
    "parsedColumns" JSONB NOT NULL,
    "sizeBytes" INTEGER,
    "mimeType" TEXT,
    "storagePath" TEXT,
    "fileHash" TEXT,
    "rawContent" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "raw_import_files_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "raw_import_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "rowNumber" INTEGER NOT NULL,
    "rawData" JSONB NOT NULL,
    "transformedData" JSONB,
    "issues" JSONB,
    "isValid" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "raw_import_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "semrush_visibility_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "keywordId" TEXT,
    "keywordText" TEXT NOT NULL,
    "normalizedKeyword" TEXT NOT NULL,
    "competitorId" TEXT,
    "competitorDomain" TEXT NOT NULL,
    "normalizedCompetitorDomain" TEXT NOT NULL,
    "visibilityScore" DOUBLE PRECISION NOT NULL,
    "position" INTEGER,
    "capturedAt" TIMESTAMP(3) NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "marketId" TEXT,
    "rankingContext" TEXT,
    "device" TEXT,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "semrush_visibility_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "semrush_map_pack_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "keywordId" TEXT,
    "keywordText" TEXT NOT NULL,
    "normalizedKeyword" TEXT NOT NULL,
    "domain" TEXT NOT NULL,
    "normalizedDomain" TEXT NOT NULL,
    "position" INTEGER NOT NULL,
    "capturedAt" TIMESTAMP(3) NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "marketId" TEXT,
    "device" TEXT,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "semrush_map_pack_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "semrush_organic_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "keywordId" TEXT,
    "keywordText" TEXT NOT NULL,
    "normalizedKeyword" TEXT NOT NULL,
    "domain" TEXT NOT NULL,
    "normalizedDomain" TEXT NOT NULL,
    "position" INTEGER NOT NULL,
    "capturedAt" TIMESTAMP(3) NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "marketId" TEXT,
    "device" TEXT,
    "searchVolume" INTEGER,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "semrush_organic_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "gsc_query_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "query" TEXT NOT NULL,
    "normalizedQuery" TEXT NOT NULL,
    "clicks" INTEGER NOT NULL DEFAULT 0,
    "impressions" INTEGER NOT NULL DEFAULT 0,
    "ctr" DOUBLE PRECISION,
    "averagePosition" DOUBLE PRECISION,
    "dateRangeStart" TIMESTAMP(3),
    "dateRangeEnd" TIMESTAMP(3),
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "isBrandExcluded" BOOLEAN NOT NULL DEFAULT false,
    "isPageExcluded" BOOLEAN NOT NULL DEFAULT false,
    "exclusionReasons" JSONB,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "currentClicks" INTEGER NOT NULL DEFAULT 0,
    "previousClicks" INTEGER NOT NULL DEFAULT 0,
    "currentImpressions" INTEGER NOT NULL DEFAULT 0,
    "previousImpressions" INTEGER NOT NULL DEFAULT 0,
    "currentCtr" DOUBLE PRECISION,
    "previousCtr" DOUBLE PRECISION,
    "currentPosition" DOUBLE PRECISION,
    "previousPosition" DOUBLE PRECISION,
    "exclusionStatus" TEXT,
    "exclusionReasonText" TEXT,

    CONSTRAINT "gsc_query_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "semrush_ranking_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "keywordId" TEXT,
    "marketId" TEXT,
    "keywordText" TEXT NOT NULL,
    "normalizedKeyword" TEXT NOT NULL,
    "tags" TEXT,
    "intents" TEXT,
    "domain" TEXT NOT NULL,
    "normalizedDomain" TEXT NOT NULL,
    "capturedAt" TIMESTAMP(3) NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "rank" INTEGER,
    "rankingType" TEXT,
    "landingUrl" TEXT,
    "difference" DOUBLE PRECISION,
    "searchVolume" INTEGER,
    "cpc" DOUBLE PRECISION,
    "keywordDifficulty" DOUBLE PRECISION,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "semrush_ranking_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "gsc_import_meta" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "searchType" TEXT,
    "dateRangeLabel" TEXT,
    "currentRangeLabel" TEXT,
    "previousRangeLabel" TEXT,
    "appliedFilters" JSONB,
    "rawFilters" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "gsc_import_meta_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "gsc_page_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "page" TEXT NOT NULL,
    "normalizedPage" TEXT NOT NULL,
    "currentClicks" INTEGER NOT NULL DEFAULT 0,
    "previousClicks" INTEGER NOT NULL DEFAULT 0,
    "currentImpressions" INTEGER NOT NULL DEFAULT 0,
    "previousImpressions" INTEGER NOT NULL DEFAULT 0,
    "currentCtr" DOUBLE PRECISION,
    "previousCtr" DOUBLE PRECISION,
    "currentPosition" DOUBLE PRECISION,
    "previousPosition" DOUBLE PRECISION,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "gsc_page_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "gsc_country_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "country" TEXT NOT NULL,
    "normalizedCountry" TEXT NOT NULL,
    "currentClicks" INTEGER NOT NULL DEFAULT 0,
    "previousClicks" INTEGER NOT NULL DEFAULT 0,
    "currentImpressions" INTEGER NOT NULL DEFAULT 0,
    "previousImpressions" INTEGER NOT NULL DEFAULT 0,
    "currentCtr" DOUBLE PRECISION,
    "previousCtr" DOUBLE PRECISION,
    "currentPosition" DOUBLE PRECISION,
    "previousPosition" DOUBLE PRECISION,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "gsc_country_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "gsc_device_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "device" TEXT NOT NULL,
    "normalizedDevice" TEXT NOT NULL,
    "currentClicks" INTEGER NOT NULL DEFAULT 0,
    "previousClicks" INTEGER NOT NULL DEFAULT 0,
    "currentImpressions" INTEGER NOT NULL DEFAULT 0,
    "previousImpressions" INTEGER NOT NULL DEFAULT 0,
    "currentCtr" DOUBLE PRECISION,
    "previousCtr" DOUBLE PRECISION,
    "currentPosition" DOUBLE PRECISION,
    "previousPosition" DOUBLE PRECISION,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "gsc_device_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "gsc_search_appearance_records" (
    "id" TEXT NOT NULL,
    "importJobId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "appearance" TEXT NOT NULL,
    "normalizedAppearance" TEXT NOT NULL,
    "currentClicks" INTEGER NOT NULL DEFAULT 0,
    "previousClicks" INTEGER NOT NULL DEFAULT 0,
    "currentImpressions" INTEGER NOT NULL DEFAULT 0,
    "previousImpressions" INTEGER NOT NULL DEFAULT 0,
    "currentCtr" DOUBLE PRECISION,
    "previousCtr" DOUBLE PRECISION,
    "currentPosition" DOUBLE PRECISION,
    "previousPosition" DOUBLE PRECISION,
    "sourceRowNumber" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "gsc_search_appearance_records_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "brand_exclusion_terms" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "term" TEXT NOT NULL,
    "normalizedTerm" TEXT NOT NULL,
    "category" TEXT,
    "matchType" "ExclusionMatchType" NOT NULL DEFAULT 'CONTAINS',
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "notes" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "brand_exclusion_terms_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "page_exclusion_terms" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "term" TEXT NOT NULL,
    "normalizedTerm" TEXT NOT NULL,
    "category" TEXT,
    "matchType" "ExclusionMatchType" NOT NULL DEFAULT 'CONTAINS',
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "notes" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "page_exclusion_terms_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "dashboard_snapshots" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "reportingMonth" TIMESTAMP(3) NOT NULL,
    "snapshotData" JSONB NOT NULL,
    "generatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "dashboard_snapshots_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "saved_dashboard_views" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "pageKey" TEXT NOT NULL,
    "filters" JSONB NOT NULL,
    "isDefault" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "saved_dashboard_views_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "data_health_issues" (
    "id" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    "importJobId" TEXT,
    "reportingMonth" TIMESTAMP(3),
    "issueType" "DataHealthIssueType" NOT NULL,
    "severity" "IssueSeverity" NOT NULL,
    "status" "IssueStatus" NOT NULL DEFAULT 'OPEN',
    "title" TEXT NOT NULL,
    "details" TEXT NOT NULL,
    "affectedEntity" TEXT,
    "affectedId" TEXT,
    "metadata" JSONB,
    "resolvedAt" TIMESTAMP(3),
    "resolvedNote" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "data_health_issues_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "reporting_templates_slug_key" ON "reporting_templates"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "projects_slug_key" ON "projects"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "projects_normalizedDomain_key" ON "projects"("normalizedDomain");

-- CreateIndex
CREATE UNIQUE INDEX "markets_projectId_normalizedName_key" ON "markets"("projectId", "normalizedName");

-- CreateIndex
CREATE UNIQUE INDEX "intent_groups_projectId_normalizedName_key" ON "intent_groups"("projectId", "normalizedName");

-- CreateIndex
CREATE UNIQUE INDEX "keyword_sets_projectId_name_key" ON "keyword_sets"("projectId", "name");

-- CreateIndex
CREATE INDEX "keywords_projectId_keywordType_idx" ON "keywords"("projectId", "keywordType");

-- CreateIndex
CREATE UNIQUE INDEX "keywords_projectId_normalizedText_keywordType_marketId_key" ON "keywords"("projectId", "normalizedText", "keywordType", "marketId");

-- CreateIndex
CREATE UNIQUE INDEX "keyword_pairs_localKeywordId_key" ON "keyword_pairs"("localKeywordId");

-- CreateIndex
CREATE UNIQUE INDEX "keyword_pairs_coreKeywordId_key" ON "keyword_pairs"("coreKeywordId");

-- CreateIndex
CREATE UNIQUE INDEX "keyword_pairs_projectId_localKeywordId_coreKeywordId_key" ON "keyword_pairs"("projectId", "localKeywordId", "coreKeywordId");

-- CreateIndex
CREATE UNIQUE INDEX "competitors_projectId_normalizedDomain_key" ON "competitors"("projectId", "normalizedDomain");

-- CreateIndex
CREATE UNIQUE INDEX "import_mapping_profiles_projectId_sourceType_name_key" ON "import_mapping_profiles"("projectId", "sourceType", "name");

-- CreateIndex
CREATE INDEX "import_jobs_projectId_sourceType_reportingMonth_idx" ON "import_jobs"("projectId", "sourceType", "reportingMonth");

-- CreateIndex
CREATE INDEX "import_validation_issues_importJobId_severity_idx" ON "import_validation_issues"("importJobId", "severity");

-- CreateIndex
CREATE UNIQUE INDEX "raw_import_files_importJobId_key" ON "raw_import_files"("importJobId");

-- CreateIndex
CREATE INDEX "raw_import_records_importJobId_rowNumber_idx" ON "raw_import_records"("importJobId", "rowNumber");

-- CreateIndex
CREATE INDEX "semrush_visibility_records_projectId_reportingMonth_idx" ON "semrush_visibility_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "semrush_visibility_records_projectId_keywordId_reportingMon_idx" ON "semrush_visibility_records"("projectId", "keywordId", "reportingMonth");

-- CreateIndex
CREATE INDEX "semrush_map_pack_records_projectId_reportingMonth_idx" ON "semrush_map_pack_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "semrush_map_pack_records_projectId_keywordId_reportingMonth_idx" ON "semrush_map_pack_records"("projectId", "keywordId", "reportingMonth");

-- CreateIndex
CREATE INDEX "semrush_organic_records_projectId_reportingMonth_idx" ON "semrush_organic_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "semrush_organic_records_projectId_keywordId_reportingMonth_idx" ON "semrush_organic_records"("projectId", "keywordId", "reportingMonth");

-- CreateIndex
CREATE INDEX "gsc_query_records_projectId_reportingMonth_idx" ON "gsc_query_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "gsc_query_records_projectId_reportingMonth_isBrandExcluded__idx" ON "gsc_query_records"("projectId", "reportingMonth", "isBrandExcluded", "isPageExcluded");

-- CreateIndex
CREATE INDEX "semrush_ranking_records_projectId_reportingMonth_idx" ON "semrush_ranking_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "semrush_ranking_records_projectId_normalizedDomain_reportin_idx" ON "semrush_ranking_records"("projectId", "normalizedDomain", "reportingMonth");

-- CreateIndex
CREATE INDEX "semrush_ranking_records_projectId_keywordId_reportingMonth_idx" ON "semrush_ranking_records"("projectId", "keywordId", "reportingMonth");

-- CreateIndex
CREATE UNIQUE INDEX "gsc_import_meta_importJobId_key" ON "gsc_import_meta"("importJobId");

-- CreateIndex
CREATE INDEX "gsc_import_meta_projectId_reportingMonth_idx" ON "gsc_import_meta"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "gsc_page_records_projectId_reportingMonth_idx" ON "gsc_page_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "gsc_country_records_projectId_reportingMonth_idx" ON "gsc_country_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "gsc_device_records_projectId_reportingMonth_idx" ON "gsc_device_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE INDEX "gsc_search_appearance_records_projectId_reportingMonth_idx" ON "gsc_search_appearance_records"("projectId", "reportingMonth");

-- CreateIndex
CREATE UNIQUE INDEX "brand_exclusion_terms_projectId_normalizedTerm_category_key" ON "brand_exclusion_terms"("projectId", "normalizedTerm", "category");

-- CreateIndex
CREATE UNIQUE INDEX "page_exclusion_terms_projectId_normalizedTerm_category_key" ON "page_exclusion_terms"("projectId", "normalizedTerm", "category");

-- CreateIndex
CREATE UNIQUE INDEX "dashboard_snapshots_projectId_reportingMonth_key" ON "dashboard_snapshots"("projectId", "reportingMonth");

-- CreateIndex
CREATE UNIQUE INDEX "saved_dashboard_views_projectId_slug_key" ON "saved_dashboard_views"("projectId", "slug");

-- CreateIndex
CREATE INDEX "data_health_issues_projectId_reportingMonth_status_idx" ON "data_health_issues"("projectId", "reportingMonth", "status");

-- AddForeignKey
ALTER TABLE "projects" ADD CONSTRAINT "projects_templateId_fkey" FOREIGN KEY ("templateId") REFERENCES "reporting_templates"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "markets" ADD CONSTRAINT "markets_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "intent_groups" ADD CONSTRAINT "intent_groups_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "keyword_sets" ADD CONSTRAINT "keyword_sets_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "keywords" ADD CONSTRAINT "keywords_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "keywords" ADD CONSTRAINT "keywords_keywordSetId_fkey" FOREIGN KEY ("keywordSetId") REFERENCES "keyword_sets"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "keywords" ADD CONSTRAINT "keywords_marketId_fkey" FOREIGN KEY ("marketId") REFERENCES "markets"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "keywords" ADD CONSTRAINT "keywords_intentGroupId_fkey" FOREIGN KEY ("intentGroupId") REFERENCES "intent_groups"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "keyword_pairs" ADD CONSTRAINT "keyword_pairs_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "keyword_pairs" ADD CONSTRAINT "keyword_pairs_localKeywordId_fkey" FOREIGN KEY ("localKeywordId") REFERENCES "keywords"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "keyword_pairs" ADD CONSTRAINT "keyword_pairs_coreKeywordId_fkey" FOREIGN KEY ("coreKeywordId") REFERENCES "keywords"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "competitors" ADD CONSTRAINT "competitors_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "import_mapping_profiles" ADD CONSTRAINT "import_mapping_profiles_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "import_jobs" ADD CONSTRAINT "import_jobs_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "import_jobs" ADD CONSTRAINT "import_jobs_mappingProfileId_fkey" FOREIGN KEY ("mappingProfileId") REFERENCES "import_mapping_profiles"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "import_validation_issues" ADD CONSTRAINT "import_validation_issues_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "raw_import_files" ADD CONSTRAINT "raw_import_files_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "raw_import_files" ADD CONSTRAINT "raw_import_files_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "raw_import_records" ADD CONSTRAINT "raw_import_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_visibility_records" ADD CONSTRAINT "semrush_visibility_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_visibility_records" ADD CONSTRAINT "semrush_visibility_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_visibility_records" ADD CONSTRAINT "semrush_visibility_records_keywordId_fkey" FOREIGN KEY ("keywordId") REFERENCES "keywords"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_visibility_records" ADD CONSTRAINT "semrush_visibility_records_competitorId_fkey" FOREIGN KEY ("competitorId") REFERENCES "competitors"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_visibility_records" ADD CONSTRAINT "semrush_visibility_records_marketId_fkey" FOREIGN KEY ("marketId") REFERENCES "markets"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_map_pack_records" ADD CONSTRAINT "semrush_map_pack_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_map_pack_records" ADD CONSTRAINT "semrush_map_pack_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_map_pack_records" ADD CONSTRAINT "semrush_map_pack_records_keywordId_fkey" FOREIGN KEY ("keywordId") REFERENCES "keywords"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_map_pack_records" ADD CONSTRAINT "semrush_map_pack_records_marketId_fkey" FOREIGN KEY ("marketId") REFERENCES "markets"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_organic_records" ADD CONSTRAINT "semrush_organic_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_organic_records" ADD CONSTRAINT "semrush_organic_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_organic_records" ADD CONSTRAINT "semrush_organic_records_keywordId_fkey" FOREIGN KEY ("keywordId") REFERENCES "keywords"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_organic_records" ADD CONSTRAINT "semrush_organic_records_marketId_fkey" FOREIGN KEY ("marketId") REFERENCES "markets"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_query_records" ADD CONSTRAINT "gsc_query_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_query_records" ADD CONSTRAINT "gsc_query_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_ranking_records" ADD CONSTRAINT "semrush_ranking_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_ranking_records" ADD CONSTRAINT "semrush_ranking_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_ranking_records" ADD CONSTRAINT "semrush_ranking_records_keywordId_fkey" FOREIGN KEY ("keywordId") REFERENCES "keywords"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "semrush_ranking_records" ADD CONSTRAINT "semrush_ranking_records_marketId_fkey" FOREIGN KEY ("marketId") REFERENCES "markets"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_import_meta" ADD CONSTRAINT "gsc_import_meta_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_import_meta" ADD CONSTRAINT "gsc_import_meta_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_page_records" ADD CONSTRAINT "gsc_page_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_page_records" ADD CONSTRAINT "gsc_page_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_country_records" ADD CONSTRAINT "gsc_country_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_country_records" ADD CONSTRAINT "gsc_country_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_device_records" ADD CONSTRAINT "gsc_device_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_device_records" ADD CONSTRAINT "gsc_device_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_search_appearance_records" ADD CONSTRAINT "gsc_search_appearance_records_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "gsc_search_appearance_records" ADD CONSTRAINT "gsc_search_appearance_records_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "brand_exclusion_terms" ADD CONSTRAINT "brand_exclusion_terms_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "page_exclusion_terms" ADD CONSTRAINT "page_exclusion_terms_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "dashboard_snapshots" ADD CONSTRAINT "dashboard_snapshots_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "saved_dashboard_views" ADD CONSTRAINT "saved_dashboard_views_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "data_health_issues" ADD CONSTRAINT "data_health_issues_projectId_fkey" FOREIGN KEY ("projectId") REFERENCES "projects"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "data_health_issues" ADD CONSTRAINT "data_health_issues_importJobId_fkey" FOREIGN KEY ("importJobId") REFERENCES "import_jobs"("id") ON DELETE SET NULL ON UPDATE CASCADE;

