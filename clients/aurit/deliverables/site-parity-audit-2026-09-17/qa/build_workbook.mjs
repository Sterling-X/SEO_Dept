import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const repoRoot = process.cwd();
const deliverableDir = path.join(
  repoRoot,
  "clients/aurit/deliverables/site-parity-audit-2026-09-17",
);
const dataPath = path.join(deliverableDir, "data/crawl-comparison.json");
const outputDir = path.join(repoRoot, "outputs/aurit-parity-audit-2026-09-17");
const outputPath = path.join(outputDir, "aurit-full-site-parity-audit.xlsx");
const previewDir = "/tmp/aurit-workbook-previews-2026-09-17";

const data = JSON.parse(await fs.readFile(dataPath, "utf8"));

const COLORS = {
  navy: "#17324D",
  teal: "#0B6E69",
  red: "#B42318",
  redLight: "#FDECEA",
  amber: "#A66300",
  amberLight: "#FFF4D6",
  green: "#1B6B3A",
  greenLight: "#E9F7EF",
  blueLight: "#EAF2F8",
  gray: "#5E6B75",
  grayLight: "#EEF1F4",
  rule: "#B9C4CC",
  white: "#FFFFFF",
  text: "#1F2933",
};
const FONT = "Arial";
const TABLE_START_ROW = 5;
const DATA_START_ROW = 6;

function normalizePath(input) {
  let value = input || "/";
  if (!value.startsWith("/")) value = `/${value}`;
  value = value.replace(/\/{2,}/g, "/");
  if (value !== "/" && !value.endsWith("/")) value += "/";
  return value;
}

function getPathFromUrl(url) {
  try {
    return normalizePath(new URL(url).pathname);
  } catch {
    return normalizePath(url);
  }
}

function colName(index) {
  let value = index + 1;
  let output = "";
  while (value > 0) {
    const remainder = (value - 1) % 26;
    output = String.fromCharCode(65 + remainder) + output;
    value = Math.floor((value - 1) / 26);
  }
  return output;
}

function quoteSheet(name) {
  return `'${name.replaceAll("'", "''")}'`;
}

function rangeRef(sheetName, column, rowCount) {
  const end = DATA_START_ROW + Math.max(rowCount, 1) - 1;
  return `${quoteSheet(sheetName)}!$${column}$${DATA_START_ROW}:$${column}$${end}`;
}

function asText(value) {
  if (value === null || value === undefined || value === "") return "(missing or blank)";
  if (Array.isArray(value)) return value.length ? value.map(asText).join(" | ") : "(none)";
  if (typeof value === "object") {
    return Object.entries(value)
      .map(([key, item]) => `${key}=${item}`)
      .join(" | ");
  }
  return String(value);
}

function normalizedComparable(value) {
  return asText(value).replace(/\s+/g, " ").trim().toLowerCase();
}

function boolStatus(value) {
  return value ? "Same" : "Changed";
}

function pageMap(site) {
  return new Map(site.pages.map((page) => [page.path, page]));
}

function directPages(site) {
  return site.pages.filter(
    (page) => page.status === 200 && page.is_html && page.redirect_count === 0,
  );
}

function primaryVariance(match, live, staging) {
  const reasons = [];
  if ((staging.h1_count || 0) === 0 && (live.h1_count || 0) > 0) reasons.push("Staging H1 missing");
  if (Math.abs(match.word_delta || 0) >= 500) reasons.push("Large source-text volume change");
  if (!match.title_equal) reasons.push("Title changed");
  if (!match.description_equal) reasons.push("Meta description changed");
  if (!match.canonical_path_equal) reasons.push("Canonical path changed");
  if (!match.template_equal) reasons.push("Template family changed");
  if (!match.schema_equal) reasons.push("Schema types changed");
  return reasons.slice(0, 4).join("; ") || "Other source/metadata difference";
}

function sourceMap(site) {
  const output = new Map();
  for (const source of site.pages) {
    for (const link of source.internal_links || []) {
      if (getPathFromUrl(link) === source.path) continue;
      if (!output.has(link)) output.set(link, new Set());
      output.get(link).add(source.path);
    }
  }
  return output;
}

function brokenTargets(site, environment, otherBrokenPaths) {
  const sources = sourceMap(site);
  return site.pages
    .filter((page) => page.status === 404 && sources.has(page.url))
    .sort((a, b) => a.path.localeCompare(b.path))
    .map((page) => {
      const allSources = [...sources.get(page.url)].sort();
      const shared = otherBrokenPaths.has(page.path);
      const classification = shared
        ? "Shared live baseline defect"
        : environment === "Staging"
          ? "Staging-only regression"
          : "Live baseline defect";
      return [
        environment,
        classification,
        page.path,
        page.url,
        page.status,
        allSources.length,
        allSources.join(" | "),
      ];
    });
}

function redirectTargets(site, environment) {
  const sources = sourceMap(site);
  return site.pages
    .filter(
      (page) =>
        page.status === 200 &&
        page.redirect_count > 0 &&
        sources.has(page.url),
    )
    .sort((a, b) => a.path.localeCompare(b.path))
    .map((page) => {
      const allSources = [...sources.get(page.url)].sort();
      return [
        environment,
        page.path,
        page.final_path,
        page.redirect_count,
        allSources.length,
        allSources.join(" | "),
        (page.discovery || []).join(" | "),
      ];
    });
}

function redirectedTarget(site, link) {
  const byUrl = new Map(site.pages.map((page) => [page.url, page]));
  const target = byUrl.get(link);
  if (!target || target.status !== 200) return link;
  return `${site.base}${normalizePath(getPathFromUrl(target.final_url))}`;
}

function orphanPages(site, environment) {
  const inlinks = new Map(site.pages.map((page) => [page.url, new Set()]));
  for (const source of site.pages) {
    if (!source.is_html) continue;
    for (const link of source.internal_links || []) {
      const target = redirectedTarget(site, link);
      if (getPathFromUrl(target) === source.path) continue;
      if (!inlinks.has(target)) inlinks.set(target, new Set());
      inlinks.get(target).add(source.path);
    }
  }
  return site.pages
    .filter((page) => {
      const robots = `${page.meta_robots || ""} ${page.x_robots_tag || ""}`.toLowerCase();
      return (
        page.status === 200 &&
        page.redirect_count === 0 &&
        (page.sitemaps || []).length > 0 &&
        !robots.includes("noindex") &&
        !(inlinks.get(page.url)?.size)
      );
    })
    .sort((a, b) => a.path.localeCompare(b.path))
    .map((page) => [
      environment,
      page.path,
      page.url,
      page.title || "",
      (page.sitemaps || []).join(" | "),
      page.meta_robots || "",
    ]);
}

function pageRecordRows(site, environment) {
  return site.pages
    .slice()
    .sort((a, b) => a.path.localeCompare(b.path))
    .map((page) => [
      environment,
      page.url,
      page.path,
      page.final_url || "",
      page.final_path || "",
      page.status ?? "",
      Boolean(page.is_html),
      page.redirect_count || 0,
      (page.discovery || []).join(" | "),
      (page.sitemaps || []).join(" | "),
      page.title || "",
      page.meta_description || "",
      (page.h1 || []).join(" | "),
      page.h1_count || 0,
      page.canonical || "",
      page.meta_robots || "",
      page.x_robots_tag || "",
      page.template_family || "",
      page.word_count || 0,
      page.image_count || 0,
      (page.schema_types || []).join(" | "),
      page.cross_environment_link_count || 0,
      page.internal_link_count || 0,
      (page.iframe_sources || []).join(" | "),
      (page.form_targets || []).join(" | "),
      (page.image_alt_issues || []).length,
      page.visible_text_sha256 || "",
      page.visible_text_excerpt || "",
      page.error || "",
    ]);
}

const liveByPath = pageMap(data.live);
const stagingByPath = pageMap(data.staging);
const matches = data.comparison.matches;
const liveDirectCount = directPages(data.live).length;
const stagingDirectCount = directPages(data.staging).length;
const samePathMatches = matches.filter((match) => match.mapping_method === "exact-path");
const samePathTitleChanges = samePathMatches.filter((match) => !match.title_equal).length;

const pageComparisonRows = matches.map((match) => {
  const live = liveByPath.get(match.live_path);
  const staging = stagingByPath.get(match.stage_path);
  return [
    match.live_path,
    match.stage_path,
    match.mapping_method,
    match.mapping_confidence,
    match.classification,
    match.text_similarity,
    live.word_count || 0,
    staging.word_count || 0,
    match.word_delta || 0,
    boolStatus(match.title_equal),
    boolStatus(match.description_equal),
    boolStatus(match.h1_equal),
    boolStatus(match.canonical_path_equal),
    boolStatus(match.status_equal),
    boolStatus(match.template_equal),
    boolStatus(match.schema_equal),
    live.h1_count || 0,
    staging.h1_count || 0,
    live.image_count || 0,
    staging.image_count || 0,
    staging.cross_environment_link_count || 0,
    primaryVariance(match, live, staging),
    live.url,
    staging.url,
  ];
});

const fieldDefinitions = [
  ["Title", "title"],
  ["Meta description", "meta_description"],
  ["H1", "h1"],
  ["H1 count", "h1_count"],
  ["Canonical", "canonical"],
  ["Meta robots", "meta_robots"],
  ["X-Robots-Tag", "x_robots_tag"],
  ["Language", "lang"],
  ["Template family", "template_family"],
  ["Source-extracted word count", "word_count"],
  ["Image count", "image_count"],
  ["Schema types", "schema_types"],
  ["Heading counts", "heading_counts"],
  ["Iframe sources", "iframe_sources"],
  ["Form targets", "form_targets"],
  ["Cross-environment links", "cross_environment_links"],
  ["Source-text hash", "visible_text_sha256"],
];
const fieldChangeRows = [];
for (const match of matches) {
  const live = liveByPath.get(match.live_path);
  const staging = stagingByPath.get(match.stage_path);
  for (const [label, key] of fieldDefinitions) {
    if (normalizedComparable(live[key]) === normalizedComparable(staging[key])) continue;
    fieldChangeRows.push([
      match.live_path,
      match.stage_path,
      label,
      asText(live[key]),
      asText(staging[key]),
      match.classification,
      match.mapping_method,
    ]);
  }
}

const gapRows = [
  ...data.comparison.live_only.map((item) => {
    const page = liveByPath.get(item);
    return [
      "Live-only",
      item,
      page?.url || `${data.live.base}${item}`,
      page?.title || "",
      page?.canonical || "",
      "No mapped direct staging page",
    ];
  }),
  ...data.comparison.staging_only.map((item) => {
    const page = stagingByPath.get(item);
    return [
      "Staging-only",
      item,
      page?.url || `${data.staging.base}${item}`,
      page?.title || "",
      page?.canonical || "",
      "No mapped direct live page",
    ];
  }),
];

const liveBrokenPathSet = new Set(
  brokenTargets(data.live, "Live", new Set()).map((row) => row[2]),
);
const stagingBrokenPathSet = new Set(
  brokenTargets(data.staging, "Staging", new Set()).map((row) => row[2]),
);
const brokenRows = [
  ...brokenTargets(data.staging, "Staging", liveBrokenPathSet),
  ...brokenTargets(data.live, "Live", stagingBrokenPathSet),
];
const redirectRows = [
  ...redirectTargets(data.staging, "Staging"),
  ...redirectTargets(data.live, "Live"),
];
const crossEnvironmentRows = ["staging", "live"].flatMap((siteName) => {
  const environment = siteName === "staging" ? "Staging" : "Live";
  return data[siteName].pages
    .filter((page) => (page.cross_environment_link_count || 0) > 0)
    .sort((a, b) => a.path.localeCompare(b.path))
    .map((page) => [
      environment,
      page.path,
      page.cross_environment_link_count || 0,
      page.unique_cross_environment_link_count || 0,
      (page.cross_environment_links || []).join(" | "),
      "Confirm cutover URL-rewrite policy; repair any link that remains cross-environment after deployment.",
    ]);
});
const orphanRows = [
  ...orphanPages(data.staging, "Staging"),
  ...orphanPages(data.live, "Live"),
];
const urlInventoryRows = [
  ...pageRecordRows(data.staging, "Staging"),
  ...pageRecordRows(data.live, "Live"),
];

const renderedQaRows = [
  ["Rendered sample", "Homepage, desktop", "Blue/Google Sans redesign; different navigation, hero, sections, CTAs, rating, footer, and consultation behavior", "Green/Recoleta design with current live sections, CTA/modal, newsletter, and footer", "Not 1:1", "Release blocker under strict parity"],
  ["Rendered sample", "Homepage, mobile", "Different menu, stacking, copy, CTAs, sections, and phone/rating display at 390 x 844 CSS viewport", "Current live mobile design at the same viewport", "Not 1:1", "Release blocker under strict parity"],
  ["Rendered sample", "/about/", "998 rendered words; 40 images; no page form; Google Sans H1", "1,340 rendered words; 49 images; one page form; Recoleta H1", "Material template/content change", "Requires target-state approval and repair"],
  ["Rendered sample", "Article /3-ways-parents-can-help-their-kids-adjust/", "339 rendered words; article body absent", "1,932 rendered words; substantive article body shown", "Critical template failure", "Release blocker under any target state"],
  ["Rendered sample", "/category/divorce-mediation/", "231 main-content words; green background; one form; changed title", "231 main-content words; white background; two forms", "Content retained; metadata/template changed", "Repair if strict parity remains the target"],
  ["Rendered sample", "/divorce-mediation-guide/", "3,104 main-content words; 13 images; no page form", "3,104 main-content words; 16 images; one page form", "Core content retained; global template changed", "Repair assets/form under either target state"],
  ["Rendered sample", "Scottsdale city", "Root /scottsdale/; 974 rendered words; 3 images; Google Sans H1", "Nested /locations/arizona/scottsdale/; 2,255 rendered words; 36 images; Recoleta H1", "Material URL/content/design change", "Needs migration mapping and content decision"],
  ["Rendered sample", "Maricopa service area", "1,367 main-content words; 1 image; no page form", "1,367 main-content words; 5 images; one page form", "Core content retained; links/assets/form changed", "Repair links/assets/form"],
  ["Rendered sample", "Michael Aurit team page", "82 main-content words; 4 images; no page form", "82 main-content words; 9 images; one page form", "Core content retained; contact/global template changed", "Repair staff email and conversion elements"],
  ["Rendered sample", "/free-consultation/", "Native six-field POST form with action ending in #; hidden broken shared iframe", "Visible third-party form iframe", "Different implementation; submission untested", "Validate approved implementation end to end"],
  ["Interaction", "Desktop navigation dropdown", "Worked", "Worked", "Functional", "Design/content parity still differs"],
  ["Interaction", "Mobile menu", "Worked", "Worked", "Functional", "Design/content parity still differs"],
  ["Interaction", "FAQ accordion", "Worked", "Worked", "Functional", "No blocker from tested interaction"],
  ["Interaction", "Welcome video", "Opened Vimeo iframe", "Vimeo player rendered", "Worked with different implementation", "Implementation variance only"],
  ["Interaction", "Homepage carousel controls", "Research and review rails moved", "Current live carousel rendered", "Controls worked; content/design differ", "Repair content/design for strict parity"],
  ["Interaction", "Primary consultation CTA", "Scrolled to staged consultation section", "Opened current live consultation flow", "Different behavior", "Target-state and conversion decision required"],
  ["Interaction", "Book My Consult modal", "Opened a frame that did not load its form", "Loaded the live lead form", "Staging failed", "Release blocker"],
  ["Endpoint", "discover.stagingaurit.wpengine.com form", "No DNS answer; form could not load", "Live counterpart resolved and rendered", "Staging failed", "Release blocker"],
  ["Endpoint", "judge-gavel.jpeg", "HTTP 404; image rendered at 0 x 0", "Not applicable", "Broken staged asset", "Release blocker for affected carousel"],
  ["Endpoint", "robots.txt", "User-agent: *; Disallow: /", "Allows crawling except WordPress admin and declares sitemap", "Expected staging safety difference", "Launch switch dependency, not parity defect"],
  ["Endpoint", "Live Vimeo direct-fetch variance", "Automated endpoint behavior differed", "Player rendered in browser", "Excluded as visible failure", "No release blocker from this check"],
];

const methodologyRows = [
  ["Scope", "Sites compared", "Staging and live Aurit public websites", "https://stagingaurit.wpengine.com/ | https://auritmediation.com/"],
  ["Scope", "Discovery", "Every XML sitemap URL, recursive same-origin HTML links, counterpart-path probes, and sequential retries for transient 5xx responses", "data/crawl-comparison.json"],
  ["Scope", "Closure", `Live closed=${data.live.graph_closure.closed}; staging closed=${data.staging.graph_closure.closed}; zero unrecorded same-host targets`, "data/crawl-comparison.json"],
  ["Definition", "Mapped pair", "Direct 200 HTML pages matched by exact path or a unique slug; unique-slug mappings require manual migration confirmation", "qa/crawl_compare.py"],
  ["Definition", "Exact", "Identical normalized source-extracted body text plus matching title, description, H1, canonical path, and status; not a pixel-level guarantee", "qa/crawl_compare.py"],
  ["Definition", "Near-match", "At least 98% source-text similarity with matching title, H1, and status; not a holistic severity rating", "qa/crawl_compare.py"],
  ["Definition", "Changed", "Fails the strict Exact or Near-match source/metadata criteria; manual severity is documented separately", "qa/crawl_compare.py"],
  ["Definition", "Broken/redirect inlink", "Calculations use the saved link graph and exclude self-links", "technical-crawl-appendix.md"],
  ["Definition", "Orphan-like", "Direct, indexable sitemap page with no saved same-host inlink after self-links are excluded and redirects are credited to the final destination", "technical-crawl-appendix.md"],
  ["Decision", "Target state", "Confirm whether the target remains strict live parity or an approved redesign before page-by-page repair", "aurit-full-site-parity-audit.md"],
  ["Independent review", "Crawl closure blocker", "Accepted and resolved: crawler now closes the graph after recovered pages and counterpart probes; regression test added", "qa/test_crawl_closure.py"],
  ["Independent review", "Evidence preservation", "Accepted: unsupported aggregate resource totals were removed; endpoint/browser evidence was saved in the validation log", "qa/validation-log.md"],
  ["Independent review", "Mechanical labels", "Accepted: labels renamed Exact, Near-match, and Changed; manual materiality is separate", "page-change-inventory.md"],
  ["Independent review", "Cross-host URLs", "Accepted: regular production-domain anchors are conditional on the deployment rewrite policy; failed forms and staging-domain email addresses remain defects", "aurit-full-site-parity-audit.md"],
  ["Independent review", "Developer usability", "Accepted: actual field values, source pages for broken links, redirect evidence, and workbook inventories were added", "page-field-changes.md | technical-crawl-appendix.md"],
  ["Limitation", "Visual coverage", "Rendered QA sampled each material template family; it was not an exhaustive pixel review of all mapped pairs", "qa/validation-log.md"],
  ["Limitation", "Functional systems", "No form submission, CRM, notification email, consent storage, analytics event, or call-routing validation", "qa/validation-log.md"],
  ["Limitation", "Other reviews", "No accessibility, performance, security, or legal-accuracy review", "qa/validation-log.md"],
  ["Limitation", "CMS-only URLs", "Pages absent from both public discovery graphs require a CMS export and remain unknowable from the public crawl", "aurit-full-site-parity-audit.md"],
  ["Reproduction", "Command", "python3 clients/aurit/deliverables/site-parity-audit-2026-09-17/qa/crawl_compare.py --json clients/aurit/deliverables/site-parity-audit-2026-09-17/data/crawl-comparison.json --inventory clients/aurit/deliverables/site-parity-audit-2026-09-17/page-change-inventory.md --fields clients/aurit/deliverables/site-parity-audit-2026-09-17/page-field-changes.md --technical clients/aurit/deliverables/site-parity-audit-2026-09-17/technical-crawl-appendix.md --max-urls 600 --workers 4", "aurit-full-site-parity-audit.md"],
  ["Freshness", "Generated", data.generated_at, "data/crawl-comparison.json"],
];

const workbook = Workbook.create();
const sheetNames = [
  "Summary",
  "Page Comparison",
  "Field Changes",
  "URL Gaps",
  "Broken Links",
  "Redirects",
  "Cross-Environment",
  "Orphan-Like",
  "Rendered QA",
  "URL Inventory",
  "Methodology",
];
const sheets = Object.fromEntries(
  sheetNames.map((name) => [name, workbook.worksheets.add(name)]),
);

function addTableSheet({
  name,
  title,
  note,
  headers,
  rows,
  widths,
  tableName,
  freezeColumns = 1,
  wrapColumns = [],
  tabColor = null,
}) {
  const sheet = sheets[name];
  const lastCol = colName(headers.length - 1);
  const lastRow = TABLE_START_ROW + rows.length;
  sheet.showGridLines = false;
  if (tabColor) sheet.tabColor = tabColor;
  sheet.getRange("A2").values = [[title]];
  sheet.getRange("A2").format = {
    font: { name: FONT, size: 14, bold: true, color: COLORS.navy },
    verticalAlignment: "center",
  };
  sheet.getRange("A3").values = [[note]];
  sheet.getRange(`A3:${lastCol}3`).format = {
    font: { name: FONT, size: 10, italic: true, color: COLORS.gray },
    verticalAlignment: "center",
  };
  sheet.getRange(`A4:${lastCol}4`).format.fill = COLORS.rule;
  sheet.getRange(`A4:${lastCol}4`).format.rowHeight = 2;
  sheet.getRange(`A${TABLE_START_ROW}`).write([headers, ...rows]);
  const used = sheet.getRange(`A2:${lastCol}${Math.max(lastRow, TABLE_START_ROW)}`);
  used.format.font = { name: FONT, size: 10, color: COLORS.text };
  used.format.verticalAlignment = "center";
  sheet.getRange(`A${TABLE_START_ROW}:${lastCol}${TABLE_START_ROW}`).format = {
    fill: COLORS.navy,
    font: { name: FONT, size: 10, bold: true, color: COLORS.white },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    wrapText: true,
    borders: { preset: "inside", style: "thin", color: COLORS.white },
  };
  if (rows.length > 0) {
    const table = sheet.tables.add(
      `A${TABLE_START_ROW}:${lastCol}${lastRow}`,
      true,
      tableName,
    );
    table.style = "TableStyleMedium2";
    table.showFilterButton = true;
    sheet.getRange(`A${DATA_START_ROW}:${lastCol}${lastRow}`).format.rowHeight = 18;
  }
  widths.forEach((width, index) => {
    const column = colName(index);
    sheet.getRange(`${column}2:${column}${Math.max(lastRow, 10)}`).format.columnWidth = width;
  });
  for (const index of wrapColumns) {
    const column = colName(index);
    sheet.getRange(`${column}${DATA_START_ROW}:${column}${Math.max(lastRow, DATA_START_ROW)}`).format.wrapText = true;
  }
  sheet.getRange(`A${TABLE_START_ROW}:${lastCol}${TABLE_START_ROW}`).format.rowHeight = 30;
  sheet.freezePanes.freezeRows(TABLE_START_ROW);
  if (freezeColumns > 0) sheet.freezePanes.freezeColumns(freezeColumns);
  return { sheet, lastCol, lastRow };
}

const pageSheet = addTableSheet({
  name: "Page Comparison",
  title: "Mapped Page Comparison",
  note: "One row per mapped direct-200 page pair. Result labels are strict source/metadata criteria, not holistic severity.",
  headers: ["Live path", "Staging path", "Mapping", "Confidence", "Result", "Text similarity", "Live words", "Staging words", "Word delta", "Title", "Meta description", "H1", "Canonical path", "Status", "Template", "Schema", "Live H1 count", "Stage H1 count", "Live images", "Stage images", "Stage cross-env anchors", "Primary variance", "Live URL", "Staging URL"],
  rows: pageComparisonRows,
  widths: [34, 34, 14, 12, 13, 14, 11, 12, 11, 11, 16, 11, 15, 11, 12, 11, 13, 14, 12, 12, 18, 48, 46, 52],
  tableName: "PageComparisonTable",
  freezeColumns: 2,
  wrapColumns: [21],
  tabColor: COLORS.teal,
});
pageSheet.sheet.getRange(`F${DATA_START_ROW}:F${pageSheet.lastRow}`).format.numberFormat = "0.0%";
pageSheet.sheet.getRange(`E${DATA_START_ROW}:E${pageSheet.lastRow}`).conditionalFormats.add("containsText", { text: "Changed", format: { fill: COLORS.redLight, font: { bold: true, color: COLORS.red } } });
pageSheet.sheet.getRange(`E${DATA_START_ROW}:E${pageSheet.lastRow}`).conditionalFormats.add("containsText", { text: "Near-match", format: { fill: COLORS.amberLight, font: { bold: true, color: COLORS.amber } } });
pageSheet.sheet.getRange(`E${DATA_START_ROW}:E${pageSheet.lastRow}`).conditionalFormats.add("containsText", { text: "Exact", format: { fill: COLORS.greenLight, font: { bold: true, color: COLORS.green } } });

addTableSheet({
  name: "Field Changes",
  title: "Changed Page Fields",
  note: "Actual live and staging values for each changed source/metadata field across the mapped corpus.",
  headers: ["Live path", "Staging path", "Field", "Live value", "Staging value", "Page result", "Mapping"],
  rows: fieldChangeRows,
  widths: [34, 34, 24, 64, 64, 13, 14],
  tableName: "FieldChangesTable",
  freezeColumns: 3,
});

const gapSheet = addTableSheet({
  name: "URL Gaps",
  title: "Unmatched Direct Pages",
  note: "Direct-200 HTML pages with no mapped direct counterpart. Resolve every row before an approved cutover.",
  headers: ["Gap type", "Path", "URL", "Title", "Canonical", "Disposition"],
  rows: gapRows,
  widths: [15, 40, 58, 52, 58, 32],
  tableName: "UrlGapsTable",
  freezeColumns: 2,
  tabColor: COLORS.red,
});
gapSheet.sheet.getRange(`A${DATA_START_ROW}:A${gapSheet.lastRow}`).conditionalFormats.add("containsText", { text: "Live-only", format: { fill: COLORS.redLight, font: { bold: true, color: COLORS.red } } });
gapSheet.sheet.getRange(`A${DATA_START_ROW}:A${gapSheet.lastRow}`).conditionalFormats.add("containsText", { text: "Staging-only", format: { fill: COLORS.amberLight, font: { bold: true, color: COLORS.amber } } });

const brokenSheet = addTableSheet({
  name: "Broken Links",
  title: "Internally Linked Final 404 Targets",
  note: "One row per unique target; self-links excluded. Source paths list every saved page that links to the target.",
  headers: ["Environment", "Classification", "Target path", "Target URL", "Status", "Source page count", "Source paths (all)"],
  rows: brokenRows,
  widths: [13, 27, 48, 62, 10, 18, 95],
  tableName: "BrokenLinksTable",
  freezeColumns: 3,
  tabColor: COLORS.red,
});
brokenSheet.sheet.getRange(`B${DATA_START_ROW}:B${brokenSheet.lastRow}`).conditionalFormats.add("containsText", { text: "Staging-only", format: { fill: COLORS.redLight, font: { bold: true, color: COLORS.red } } });
brokenSheet.sheet.getRange(`B${DATA_START_ROW}:B${brokenSheet.lastRow}`).conditionalFormats.add("containsText", { text: "Shared", format: { fill: COLORS.amberLight, font: { bold: true, color: COLORS.amber } } });

addTableSheet({
  name: "Redirects",
  title: "Internally Linked Redirect Targets",
  note: "One row per linked redirecting target; self-links excluded. Source paths list every saved linking page.",
  headers: ["Environment", "Requested path", "Final path", "Hops", "Source page count", "Source paths (all)", "Discovery"],
  rows: redirectRows,
  widths: [13, 44, 44, 10, 18, 95, 28],
  tableName: "RedirectsTable",
  freezeColumns: 3,
});

addTableSheet({
  name: "Cross-Environment",
  title: "Cross-Environment Anchor Inventory",
  note: "Staging-to-live anchor occurrences. Regular production-domain anchors are conditional on the deployment URL-rewrite policy.",
  headers: ["Environment", "Source path", "Anchor occurrences", "Unique targets", "Target URLs", "Required decision"],
  rows: crossEnvironmentRows,
  widths: [13, 48, 20, 15, 96, 58],
  tableName: "CrossEnvironmentTable",
  freezeColumns: 2,
});

addTableSheet({
  name: "Orphan-Like",
  title: "Orphan-Like Sitemap Pages",
  note: "Direct, indexable sitemap pages with no saved same-host inlink after self-links are excluded and redirects are credited to the final destination.",
  headers: ["Environment", "Path", "URL", "Title", "Sitemap", "Meta robots"],
  rows: orphanRows,
  widths: [13, 48, 62, 58, 30, 48],
  tableName: "OrphanLikeTable",
  freezeColumns: 2,
});

const renderedSheet = addTableSheet({
  name: "Rendered QA",
  title: "Rendered, Interaction, and Endpoint QA",
  note: "Read-only connected-browser inspection plus targeted HTTP/DNS checks. No form was submitted.",
  headers: ["Evidence type", "Test", "Staging observation", "Live observation / comparison", "Result", "Release relevance"],
  rows: renderedQaRows,
  widths: [18, 42, 72, 72, 38, 48],
  tableName: "RenderedQaTable",
  freezeColumns: 2,
  wrapColumns: [1, 2, 3, 4, 5],
});
renderedSheet.sheet.getRange(`A${DATA_START_ROW}:F${renderedSheet.lastRow}`).format.rowHeight = 48;

addTableSheet({
  name: "URL Inventory",
  title: "Complete Saved URL/Target Inventory",
  note: "Every saved live and staging page/target record, including direct pages, redirects, final 404s, and transient errors retained by the closed crawl.",
  headers: ["Environment", "Requested URL", "Requested path", "Final URL", "Final path", "Status", "Is HTML", "Redirect hops", "Discovery", "Sitemaps", "Title", "Meta description", "H1", "H1 count", "Canonical", "Meta robots", "X-Robots-Tag", "Template", "Words", "Images", "Schema types", "Cross-env anchors", "Internal anchor occurrences", "Iframe sources", "Form targets", "Image alt issues", "Source-text hash", "Text excerpt", "Error"],
  rows: urlInventoryRows,
  widths: [13, 58, 44, 58, 44, 10, 11, 13, 28, 30, 52, 70, 52, 12, 58, 46, 28, 18, 10, 10, 44, 17, 23, 70, 42, 16, 68, 88, 34],
  tableName: "UrlInventoryTable",
  freezeColumns: 3,
});

const methodSheet = addTableSheet({
  name: "Methodology",
  title: "Scope, Definitions, Review Dispositions, and Limits",
  note: "This tab defines what the workbook proves, what remains unknown, and how the evidence was produced.",
  headers: ["Category", "Item", "Detail", "Source"],
  rows: methodologyRows,
  widths: [20, 30, 110, 70],
  tableName: "MethodologyTable",
  freezeColumns: 2,
  wrapColumns: [2, 3],
});
methodSheet.sheet.getRange(`A${DATA_START_ROW}:D${methodSheet.lastRow}`).format.rowHeight = 42;

const summary = sheets.Summary;
summary.showGridLines = false;
summary.tabColor = COLORS.navy;
summary.getRange("A1:J25").format.font = { name: FONT, size: 10, color: COLORS.text };
summary.getRange("A2").values = [["Aurit Website Parity Audit"]];
summary.getRange("A2").format = { font: { name: FONT, size: 16, bold: true, color: COLORS.navy } };
summary.getRange("A3").values = [[`Staging versus live | crawl generated ${data.generated_at} | rendered QA completed September 17, 2026`]];
summary.getRange("A3:J3").format = { font: { name: FONT, size: 10, italic: true, color: COLORS.gray } };
summary.getRange("A4:J4").format.fill = COLORS.rule;
summary.getRange("A4:J4").format.rowHeight = 2;
summary.getRange("A6").values = [["Launch decision"]];
summary.getRange("B6:D6").values = [["FAIL – DO NOT CUT OVER", null, null]];
summary.getRange("A6:D6").format = {
  fill: COLORS.redLight,
  font: { name: FONT, size: 12, bold: true, color: COLORS.red },
  verticalAlignment: "center",
};
summary.getRange("A6:D6").format.rowHeight = 30;
summary.getRange("F6").values = [["Target-state decision"]];
summary.getRange("G6:J6").values = [["Confirm strict live parity vs. approved redesign before repairs", null, null, null]];
summary.getRange("F6:J6").format = {
  fill: COLORS.amberLight,
  font: { name: FONT, size: 10, bold: true, color: COLORS.amber },
  verticalAlignment: "center",
};
summary.getRange("F6:J6").format.rowHeight = 30;

summary.getRange("A8:C8").values = [["Control metric", "Value", "What it means"]];
summary.getRange("A8:C8").format = {
  fill: COLORS.navy,
  font: { name: FONT, size: 10, bold: true, color: COLORS.white },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
const summaryMetrics = [
  ["Mapped direct-page pairs", `=COUNTA(${rangeRef("Page Comparison", "A", pageComparisonRows.length)})`, "Every row differs under strict criteria"],
  ["Exact pairs", `=COUNTIFS(${rangeRef("Page Comparison", "E", pageComparisonRows.length)},"Exact")`, "Required count for strict parity is all approved mapped pairs"],
  ["Near-match pairs", `=COUNTIFS(${rangeRef("Page Comparison", "E", pageComparisonRows.length)},"Near-match")`, "Still not 1:1"],
  ["Changed pairs", `=COUNTIFS(${rangeRef("Page Comparison", "E", pageComparisonRows.length)},"Changed")`, "Mechanical label; manual severity varies"],
  ["Live direct-200 HTML pages", `=COUNTA(${rangeRef("Page Comparison", "A", pageComparisonRows.length)})+COUNTIFS(${rangeRef("URL Gaps", "A", gapRows.length)},"Live-only")`, "Known live public inventory"],
  ["Staging direct-200 HTML pages", `=COUNTA(${rangeRef("Page Comparison", "A", pageComparisonRows.length)})+COUNTIFS(${rangeRef("URL Gaps", "A", gapRows.length)},"Staging-only")`, `${liveDirectCount - stagingDirectCount} fewer than live`],
  ["Live-only direct pages", `=COUNTIFS(${rangeRef("URL Gaps", "A", gapRows.length)},"Live-only")`, "Missing direct staging counterparts"],
  ["Staging-only direct pages", `=COUNTIFS(${rangeRef("URL Gaps", "A", gapRows.length)},"Staging-only")`, "New/unmapped staged pages"],
  ["Staging linked 404 targets", `=COUNTIFS(${rangeRef("Broken Links", "A", brokenRows.length)},"Staging")`, "20 staging-only regressions; 5 shared defects"],
  ["Staging cross-env anchors", `=SUMIFS(${rangeRef("Cross-Environment", "C", crossEnvironmentRows.length)},${rangeRef("Cross-Environment", "A", crossEnvironmentRows.length)},"Staging")`, "Conditional on deployment rewrite policy"],
  ["Staging orphan-like pages", `=COUNTIFS(${rangeRef("Orphan-Like", "A", orphanRows.length)},"Staging")`, "Link-graph review queue"],
  ["Saved graph closure", "Closed on both hosts", "Zero discovered same-host targets unrecorded"],
];
summary.getRange("A9").write(summaryMetrics.map(([label]) => [label]));
summary.getRange("B9:B19").formulas = summaryMetrics.slice(0, 11).map(([, value]) => [value]);
summary.getRange("B20").values = [[summaryMetrics[11][1]]];
summary.getRange("C9").write(summaryMetrics.map(([, , meaning]) => [meaning]));
summary.getRange("A9:C20").format = {
  font: { name: FONT, size: 10, color: COLORS.text },
  verticalAlignment: "center",
  borders: { insideHorizontal: { style: "thin", color: COLORS.rule } },
};
summary.getRange("B9:B20").format = { font: { name: FONT, size: 11, bold: true, color: COLORS.navy }, horizontalAlignment: "right", verticalAlignment: "center" };

summary.getRange("E8:J8").values = [["Priority", "Issue", "Evidence", "Release treatment", "Next action", "Acceptance check"]];
summary.getRange("E8:J8").format = {
  fill: COLORS.navy,
  font: { name: FONT, size: 10, bold: true, color: COLORS.white },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
};
const actionRows = [
  ["P0", "Article template omits body content", "94 staged posts each expose 269 source-extracted words and no substantive H1", "Empty 200 shells block under any target state", "Restore approved content or implement approved retirement/redirect mapping", "No staged post serves an empty 200 shell; retained posts have approved body/H1"],
  ["P0", "City URL/content migration incomplete", "22 live city pages have no staged replacement; 8 renamed cities are materially rebuilt", "Block until migration is approved and mapped", "Create/approve destination matrix and redirects", "Every live city URL has approved content and tested final destination"],
  ["P0", "Lead-form modal fails", "Staged discover host has no DNS answer; tested modal does not load", "Block", "Restore approved form endpoint and validate submissions", "Form, CRM, email, consent, analytics, and routing tests pass"],
  ["P0", "Internal 404s", "25 staged linked 404 targets: 20 staging regressions plus 5 shared defects", "Block staging regressions", "Repair destinations and source links by template", "Zero unintended staged internal 404 targets"],
  ["P0", "Broken carousel asset", "judge-gavel.jpeg returns 404 and renders 0 x 0", "Block affected component", "Restore or replace the approved image", "Asset returns 200 and renders at intended dimensions"],
  ["P1", "Cross-environment URLs and staff email", "269 staged anchors point to live; seven team emails use staging domain", "Deployment dependency plus direct contact defect", "Confirm rewrite policy; restore production email destinations", "Zero unintended cross-environment destinations after cutover"],
  ["P1", "Metadata, headings, and schema differ", `${samePathTitleChanges} titles differ among ${samePathMatches.length} same-path pairs; 94 post H1s absent`, "Repair to approved target state", "Apply template fixes, then page exceptions", "Approved title/H1/canonical/robots/schema values verified"],
  ["P1", "Arizona parent indexability differs", "Live parent is indexable/self-canonical/in sitemap; staged parent is noindex without canonical", "Migration decision required", "Approve parent-page role and implement", "Indexability/canonical/sitemap state matches approved architecture"],
];
summary.getRange("E9").write(actionRows);
summary.getRange("E9:J16").format = {
  font: { name: FONT, size: 10, color: COLORS.text },
  verticalAlignment: "center",
  wrapText: true,
  borders: { insideHorizontal: { style: "thin", color: COLORS.rule } },
};
summary.getRange("E9:J13").format.rowHeight = 58;
summary.getRange("E14:J16").format.rowHeight = 48;
summary.getRange("E9:E13").format = { fill: COLORS.redLight, font: { name: FONT, size: 10, bold: true, color: COLORS.red }, horizontalAlignment: "center", verticalAlignment: "center" };
summary.getRange("E14:E16").format = { fill: COLORS.amberLight, font: { name: FONT, size: 10, bold: true, color: COLORS.amber }, horizontalAlignment: "center", verticalAlignment: "center" };

summary.getRange("A22:J22").values = [["Important limitations", null, null, null, null, null, null, null, null, null]];
summary.getRange("A22:J22").format = { fill: COLORS.grayLight, font: { name: FONT, size: 10, bold: true, color: COLORS.navy } };
summary.getRange("A23:J25").values = [
  ["Public discovery cannot prove CMS-only URLs absent from both graphs; obtain a CMS export for a true backend reconciliation.", null, null, null, null, null, null, null, null, null],
  [`Rendered QA sampled each material template family; it was not a pixel-level visual review of all ${matches.length} mapped pairs.`, null, null, null, null, null, null, null, null, null],
  ["No form submission, CRM, notification-email, consent, analytics-event, call-routing, accessibility, performance, security, or legal-accuracy test was performed.", null, null, null, null, null, null, null, null, null],
];
summary.getRange("A23:J25").format = { font: { name: FONT, size: 10, italic: true, color: COLORS.gray }, verticalAlignment: "center" };
summary.getRange("A23:J25").format.rowHeight = 22;
const summaryWidths = [31, 18, 40, 3, 10, 30, 42, 28, 38, 43];
summaryWidths.forEach((width, index) => {
  const column = colName(index);
  summary.getRange(`${column}2:${column}25`).format.columnWidth = width;
});
summary.getRange("A2").format.font = { name: FONT, size: 16, bold: true, color: COLORS.navy };
summary.getRange("A3:J3").format.font = { name: FONT, size: 10, italic: true, color: COLORS.gray };

workbook.recalculate();

const summaryInspect = await workbook.inspect({
  kind: "table",
  range: "Summary!A1:J25",
  include: "values,formulas",
  tableMaxRows: 25,
  tableMaxCols: 10,
  maxChars: 8000,
});
const pageInspect = await workbook.inspect({
  kind: "table",
  range: "Page Comparison!A1:X10",
  include: "values,formulas",
  tableMaxRows: 10,
  tableMaxCols: 24,
  maxChars: 6000,
});
const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
  maxChars: 4000,
});

await fs.rm(previewDir, { recursive: true, force: true });
await fs.mkdir(previewDir, { recursive: true });
const renderRanges = {
  Summary: "A1:J25",
  "Page Comparison": "A1:X16",
  "Field Changes": "A1:G18",
  "URL Gaps": "A1:F20",
  "Broken Links": "A1:G18",
  Redirects: "A1:G18",
  "Cross-Environment": "A1:F18",
  "Orphan-Like": "A1:F18",
  "Rendered QA": "A1:F16",
  "URL Inventory": "A1:AC14",
  Methodology: "A1:D18",
};
const previewPaths = [];
for (const [sheetName, range] of Object.entries(renderRanges)) {
  const blob = await workbook.render({ sheetName, range, scale: 1, format: "png" });
  const previewPath = path.join(previewDir, `${sheetName.replaceAll(" ", "-").toLowerCase()}.png`);
  await fs.writeFile(previewPath, new Uint8Array(await blob.arrayBuffer()));
  previewPaths.push(previewPath);
}

await fs.mkdir(outputDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });

const savedWorkbook = await SpreadsheetFile.importXlsx(await FileBlob.load(outputPath));
const savedSummaryInspect = await savedWorkbook.inspect({
  kind: "table",
  range: "Summary!A8:C20",
  include: "values,formulas",
  tableMaxRows: 13,
  tableMaxCols: 3,
  maxChars: 4000,
});
const savedFormulaErrors = await savedWorkbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "saved-file formula error scan",
  maxChars: 4000,
});
const savedSummaryPreview = await savedWorkbook.render({
  sheetName: "Summary",
  range: "A1:J25",
  scale: 1,
  format: "png",
});
const savedSummaryPreviewPath = path.join(previewDir, "summary-saved-file.png");
await fs.writeFile(
  savedSummaryPreviewPath,
  new Uint8Array(await savedSummaryPreview.arrayBuffer()),
);

console.log(JSON.stringify({
  outputPath,
  sheetRows: {
    pageComparison: pageComparisonRows.length,
    fieldChanges: fieldChangeRows.length,
    urlGaps: gapRows.length,
    brokenTargets: brokenRows.length,
    redirects: redirectRows.length,
    crossEnvironmentSources: crossEnvironmentRows.length,
    orphanLike: orphanRows.length,
    renderedQa: renderedQaRows.length,
    urlInventory: urlInventoryRows.length,
  },
  previews: previewPaths,
  summaryInspect: summaryInspect.ndjson,
  pageInspect: pageInspect.ndjson,
  formulaErrors: formulaErrors.ndjson,
  savedSummaryInspect: savedSummaryInspect.ndjson,
  savedFormulaErrors: savedFormulaErrors.ndjson,
  savedSummaryPreview: savedSummaryPreviewPath,
}, null, 2));
