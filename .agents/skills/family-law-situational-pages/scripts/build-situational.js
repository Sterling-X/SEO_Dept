#!/usr/bin/env node
/**
 * LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL
 *
 * Manifest-driven DOCX generator for the demonstrated FL-M008 High-Conflict
 * Divorce Situational route. This is not the Core Hub template. It reuses only
 * generic docx-js mechanics and pinned dependency versions proven locally.
 *
 * Usage: node scripts/build-situational.js <input.json> <output.docx>
 */

const fs = require("fs");
const path = require("path");
const {
  AlignmentType,
  BorderStyle,
  Document,
  ExternalHyperlink,
  Footer,
  Header,
  HeadingLevel,
  LevelFormat,
  Packer,
  PageNumber,
  Paragraph,
  ShadingType,
  TextRun,
  convertInchesToTwip,
} = require("docx");

const [inputArg, outputArg] = process.argv.slice(2);
if (!inputArg || !outputArg) {
  console.error("Usage: node scripts/build-situational.js <input.json> <output.docx>");
  process.exit(2);
}

const inputPath = path.resolve(inputArg);
const outputPath = path.resolve(outputArg);
const skillRoot = path.resolve(__dirname, "..");
const repoRoot = path.resolve(skillRoot, "../../..");
const architecturePath = path.join(repoRoot, "context/architecture/Family_Law_StructureV2.html");

function fail(messages) {
  for (const message of messages) console.error(`ERROR: ${message}`);
  process.exit(1);
}

function readJson(filename) {
  try {
    return JSON.parse(fs.readFileSync(filename, "utf8"));
  } catch (error) {
    fail([`Cannot read JSON ${filename}: ${error.message}`]);
  }
}

function loadArchitecture() {
  let html;
  try {
    html = fs.readFileSync(architecturePath, "utf8");
  } catch (error) {
    fail([`Cannot read governing V2 architecture at ${architecturePath}: ${error.message}`]);
  }
  const match = html.match(/const compact = (\{.*?\});\s*\n/s);
  if (!match) fail(["Cannot locate embedded V2 compact data."]);
  const compact = JSON.parse(match[1]);
  const read = (key, index) => index === -1 || index == null ? null : compact.d[key][index];
  const nodes = compact.n.map((tuple, index) => ({
    index,
    id: tuple[0],
    name: tuple[1],
    parent: tuple[2],
    pageType: read("pageType", tuple[7]),
    nodeClass: read("nodeClass", tuple[8]),
    publishability: read("publishability", tuple[9]),
    path: tuple[10],
    role: read("contentRole", tuple[11]),
    intent: read("intent", tuple[12]),
    requiredness: read("requiredness", tuple[13]),
    priority: read("priorityTier", tuple[14]),
    wave: read("productionWave", tuple[15]),
    decision: read("decisionState", tuple[16]),
    gate: read("governanceGate", tuple[17]),
    briefType: read("briefType", tuple[18]),
    wordTarget: read("wordCountTarget", tuple[19]),
    faqModule: read("faqModule", tuple[20]),
    primaryCta: read("primaryCta", tuple[21]),
  }));
  const edges = compact.e.map((tuple, index) => ({
    index,
    id: `CL-${String(index + 1).padStart(5, "0")}`,
    source: tuple[0],
    target: tuple[1],
    type: read("relationshipType", tuple[2]),
    status: read("relationshipStatus", tuple[4]),
    provenance: read("relationshipProvenance", tuple[5]),
  }));
  return { nodes, edges };
}

function validHttpUrl(value) {
  try {
    const parsed = new URL(value);
    return parsed.protocol === "https:" || parsed.protocol === "http:";
  } catch {
    return false;
  }
}

function validIsoDate(value) {
  return /^\d{4}-\d{2}-\d{2}$/.test(String(value || ""))
    && !Number.isNaN(Date.parse(`${value}T00:00:00Z`));
}

function countWords(text) {
  return (String(text || "").match(/[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*/g) || []).length;
}

function runText(run) {
  return String(run?.text || "");
}

function blockText(block) {
  if (["h2", "h3"].includes(block.type)) return String(block.text || "");
  if (block.type === "p") return (block.runs || []).map(runText).join("");
  if (["ul", "ol"].includes(block.type)) {
    return (block.items || []).map((item) => (item.runs || []).map(runText).join("")).join(" ");
  }
  return "";
}

function sentenceCount(text) {
  const matches = String(text || "").match(/(?:[.!?](?:[\"')\]]+)?)(?=\s|$)/g);
  return matches ? matches.length : (String(text || "").trim() ? 1 : 0);
}

const data = readJson(inputPath);
const architecture = loadArchitecture();
const nodeById = new Map(architecture.nodes.map((node) => [node.id, node]));
const edgeById = new Map(architecture.edges.map((edge) => [edge.id, edge]));
const errors = [];

if (data.schema_version !== 2) errors.push("schema_version must be 2.");
if (data.workflow !== "situational-fl-m008-local-replacement") {
  errors.push('workflow must be "situational-fl-m008-local-replacement".');
}
if (!data.meta || typeof data.meta !== "object") errors.push("meta is required.");
if (!Array.isArray(data.content)) errors.push("content must be an array.");
if (!Array.isArray(data.link_manifest)) errors.push("link_manifest must be an array.");
if (!Array.isArray(data.sources)) errors.push("sources must be an array, even when empty.");
if (errors.length) fail(errors);

const meta = data.meta;
const synthetic = meta.synthetic_fixture === true;
const sourceNode = nodeById.get(meta.architecture_node_id);
if (!sourceNode) {
  errors.push(`Unknown V2 architecture node: ${meta.architecture_node_id || "(missing)"}.`);
} else {
  const requiredMatches = [
    ["architecture_node_id", "FL-M008", meta.architecture_node_id],
    ["v2_reference_path", sourceNode.path, meta.v2_reference_path],
    ["v2_page_type", sourceNode.pageType, meta.v2_page_type],
    ["v2_role", sourceNode.role, meta.v2_role],
    ["v2_brief_type", sourceNode.briefType, meta.v2_brief_type],
    ["v2_word_count_target", sourceNode.wordTarget, meta.v2_word_count_target],
  ];
  for (const [field, expected, actual] of requiredMatches) {
    if (actual !== expected) errors.push(`meta.${field} must match V2 exactly: ${expected}.`);
  }
  if (sourceNode.pageType !== "Practice-Area Situational Page" || sourceNode.role !== "Situational") {
    errors.push(`${sourceNode.id} is not the required Situational page type and role.`);
  }
  if (sourceNode.nodeClass !== "Canonical Page" || sourceNode.publishability !== "Publishable") {
    errors.push(`${sourceNode.id} is not a publishable canonical node.`);
  }
  if (sourceNode.gate !== "PASS — CANONICAL") errors.push(`${sourceNode.id} gate must be PASS — CANONICAL.`);
}

for (const field of [
  "title_tag",
  "meta_description",
  "cms_title",
  "social_title",
  "social_description",
  "h1",
  "client_url",
  "canonical_url",
  "url_retention_decision",
  "robots",
  "media_note",
  "situational_purpose",
]) {
  if (!String(meta[field] || "").trim()) errors.push(`meta.${field} is required.`);
}
if (!/high[- ]conflict divorce/i.test(String(meta.h1 || ""))) {
  errors.push("meta.h1 must identify High-Conflict Divorce.");
}
if (String(meta.title_tag || "").length > 65) errors.push("meta.title_tag must not exceed 65 characters.");
if (String(meta.meta_description || "").length > 165) errors.push("meta.meta_description must not exceed 165 characters.");
if (/\bdraft\b/i.test(String(meta.title_tag || ""))) errors.push("meta.title_tag must not contain Draft.");

const clientUrl = validHttpUrl(meta.client_url) ? new URL(meta.client_url) : null;
if (!clientUrl) {
  errors.push("meta.client_url must be an HTTP(S) URL.");
} else if (clientUrl.search || clientUrl.hash) {
  errors.push("meta.client_url must not contain a query or fragment.");
}
const canonicalUrl = validHttpUrl(meta.canonical_url) ? new URL(meta.canonical_url) : null;
if (!canonicalUrl) {
  errors.push("meta.canonical_url must be an HTTP(S) URL.");
} else if (canonicalUrl.search || canonicalUrl.hash) {
  errors.push("meta.canonical_url must not contain a query or fragment.");
}
if (meta.url_retention_decision === "retain-existing" && meta.canonical_url !== meta.client_url) {
  errors.push("A retain-existing decision requires canonical_url to equal client_url exactly.");
}

const requiredExcludedIntents = new Set(["general-divorce-hub", "contested-divorce-procedure"]);
const excludedIntents = new Set(meta.excluded_intents || []);
for (const intent of requiredExcludedIntents) {
  if (!excludedIntents.has(intent)) errors.push(`meta.excluded_intents must include ${intent}.`);
}

if (synthetic) {
  if (!clientUrl || clientUrl.hostname !== "example.com") errors.push("Synthetic fixtures must use example.com.");
  if (meta.voice_source !== "synthetic-fixture") errors.push('Synthetic fixtures must set voice_source to "synthetic-fixture".');
  if (data.sources.length) errors.push("Synthetic fixtures must not include sources or citation runs.");
  if (data.link_inventory?.status !== "synthetic-fixture") {
    errors.push('Synthetic fixtures must set link_inventory.status to "synthetic-fixture".');
  }
} else {
  for (const field of ["firm_name", "jurisdiction", "voice_source"]) {
    if (!String(meta[field] || "").trim()) errors.push(`meta.${field} is required for production output.`);
  }
  if (meta.client_url_status !== 200 || meta.client_url_redirects !== 0) {
    errors.push("Production client URL evidence must record a direct 200 with zero redirects.");
  }
  if (!validIsoDate(meta.client_url_verified_on) || !String(meta.client_url_evidence || "").trim()) {
    errors.push("Production client URL evidence requires an ISO date and non-empty evidence note.");
  }
  if (data.link_inventory?.status !== "reviewed" || !validIsoDate(data.link_inventory?.reviewed_on)
      || !String(data.link_inventory?.evidence || "").trim()) {
    errors.push("Production output requires a reviewed, dated link inventory with evidence, including when no links activate.");
  }
  if (data.sources.length < 1) errors.push("Production legal copy requires at least one verified official source.");
}

const expectedFilename = synthetic
  ? /^synthetic-high-conflict-divorce-situational\.docx$/
  : /^[a-z0-9]+(?:-[a-z0-9]+)*-high-conflict-divorce-situational\.docx$/;
if (!expectedFilename.test(path.basename(outputPath))) {
  errors.push(`Output filename does not match the ${synthetic ? "synthetic" : "production"} FL-M008 naming contract.`);
}

const linkById = new Map();
const linkUrls = new Set();
const supportedAuthorities = new Set([
  "v2-explicit-relationship",
  "skill-parent-navigation",
  "skill-process-bridge",
  "consultation-cta",
]);
const authorityCounts = new Map([...supportedAuthorities].map((authority) => [authority, 0]));
const hasOwn = (object, field) => Object.prototype.hasOwnProperty.call(object, field);

function validateV2Target(link, target) {
  if (!target) return;
  if (target.nodeClass !== "Canonical Page" || target.publishability !== "Publishable") {
    errors.push(`${link.id}: target ${target.id} is not a publishable canonical page.`);
  }
  if (/^(?:HOLD|BLOCK) —/.test(target.gate || "")) {
    errors.push(`${link.id}: target ${target.id} cannot activate while its V2 gate is ${target.gate}.`);
  } else if (target.gate !== "PASS — CANONICAL") {
    if (link.target_gate_approval !== "approved" || !String(link.target_gate_evidence || "").trim()) {
      errors.push(`${link.id}: target ${target.id} needs documented approval for gate ${target.gate}.`);
    }
  }
  if (link.v2_reference_path !== target.path) {
    errors.push(`${link.id}: v2_reference_path must match target V2 path ${target.path}.`);
  }
}

for (const link of data.link_manifest) {
  if (!link.id || linkById.has(link.id)) {
    errors.push(`Every link_manifest entry needs a unique id; problem at ${link.id || "(missing)"}.`);
    continue;
  }
  linkById.set(link.id, link);
  if (!sourceNode || link.source_node_id !== sourceNode.id) {
    errors.push(`${link.id}: source_node_id must be FL-M008.`);
  }
  const authority = link.supporting_authority;
  if (!supportedAuthorities.has(authority)) {
    errors.push(`${link.id}: supporting_authority must be one of ${[...supportedAuthorities].join(", ")}.`);
  } else {
    authorityCounts.set(authority, authorityCounts.get(authority) + 1);
  }

  if (authority === "consultation-cta") {
    if (link.destination_kind !== "consultation-contact") {
      errors.push(`${link.id}: consultation-cta must set destination_kind to consultation-contact.`);
    }
    for (const field of ["target_node_id", "v2_reference_path", "v2_edge_id"]) {
      if (hasOwn(link, field)) errors.push(`${link.id}: consultation-cta must omit ${field}; it is not a V2 relationship.`);
    }
  } else if (supportedAuthorities.has(authority)) {
    const target = nodeById.get(link.target_node_id);
    if (!target) {
      errors.push(`${link.id}: unknown V2 target ${link.target_node_id || "(missing)"}.`);
    } else {
      if (authority === "v2-explicit-relationship") {
        const edge = edgeById.get(link.v2_edge_id);
        if (!edge || !sourceNode || edge.source !== sourceNode.index || edge.target !== target.index) {
          errors.push(`${link.id}: ${link.v2_edge_id || "(missing edge)"} is not an exact outgoing V2 relationship from FL-M008 to ${target.id}.`);
        }
      }
      if (authority === "skill-parent-navigation") {
        if (hasOwn(link, "v2_edge_id")) {
          errors.push(`${link.id}: skill-parent-navigation must omit v2_edge_id; its direction is required by the Situational skill, not a V2 edge.`);
        }
        if (!sourceNode || target.index !== sourceNode.parent
            || target.pageType !== "Core Practice-Area Hub" || target.role !== "Hub") {
          const parentId = sourceNode ? architecture.nodes[sourceNode.parent]?.id : "the V2 parent";
          errors.push(`${link.id}: skill-parent-navigation must target the actual V2 parent ${parentId || "(missing)"}.`);
        }
      }
      if (authority === "skill-process-bridge") {
        if (hasOwn(link, "v2_edge_id")) {
          errors.push(`${link.id}: skill-process-bridge must omit v2_edge_id; its direction is required by the Situational skill, not a V2 edge.`);
        }
        if (!sourceNode || target.id !== "FL-M004" || target.parent !== sourceNode.parent
            || target.pageType !== "Practice-Area Procedural Page" || target.role !== "Core Procedure") {
          errors.push(`${link.id}: skill-process-bridge must target FL-M004 under the same parent with V2 page type Practice-Area Procedural Page and role Core Procedure.`);
        }
      }
      validateV2Target(link, target);
    }
  }
  if (!validHttpUrl(link.client_url)) {
    errors.push(`${link.id}: client_url must be HTTP(S).`);
  } else {
    const parsed = new URL(link.client_url);
    if (clientUrl && parsed.hostname !== clientUrl.hostname) errors.push(`${link.id}: client_url must use the client domain.`);
    if (parsed.search || parsed.hash) errors.push(`${link.id}: client_url must not contain a query or fragment.`);
  }
  if (linkUrls.has(link.client_url)) errors.push(`${link.id}: duplicate client destination URL.`);
  linkUrls.add(link.client_url);
  if (link.client_url_status !== 200 || link.client_url_redirects !== 0 || link.destination_fit !== "verified") {
    errors.push(`${link.id}: destination must be a verified right-service direct 200 with zero redirects.`);
  }
  if (!validIsoDate(link.client_url_verified_on) || !String(link.client_url_evidence || "").trim()) {
    errors.push(`${link.id}: destination evidence requires an ISO date and non-empty note.`);
  }
  if (!String(link.anchor || "").trim() || !String(link.placement || "").trim()) {
    errors.push(`${link.id}: anchor and placement are required.`);
  }
}

for (const authority of ["skill-parent-navigation", "skill-process-bridge", "consultation-cta"]) {
  const count = authorityCounts.get(authority);
  if (count !== 1) errors.push(`FL-M008 requires exactly one ${authority} link; found ${count}.`);
}

const sourceById = new Map();
for (const source of data.sources) {
  if (!Number.isInteger(source.id) || sourceById.has(source.id)) {
    errors.push(`Every source needs a unique integer id; problem at ${source.id ?? "(missing)"}.`);
    continue;
  }
  sourceById.set(source.id, source);
  if (!String(source.label || "").trim() || !validHttpUrl(source.url)) {
    errors.push(`Source ${source.id}: label and HTTP(S) URL are required.`);
  }
  if (!synthetic) {
    if (source.authority !== "official-primary" || source.status !== 200
        || !validIsoDate(source.verified_on) || !String(source.verification_evidence || "").trim()) {
      errors.push(`Source ${source.id}: production sources require official-primary, status 200, an ISO verification date, and evidence.`);
    }
  }
}
if (data.sources.length > 6) errors.push("No more than six sources are allowed for this Situational route.");

if (data.content.length < 3 || data.content[0]?.type !== "p" || data.content[1]?.type !== "p") {
  errors.push("The first two content blocks must be answer-first paragraphs.");
}
if (!/high[- ]conflict/i.test(blockText(data.content[0] || {}))) {
  errors.push("The first opening paragraph must directly identify the high-conflict situation.");
}

const h2Blocks = data.content.filter((block) => block.type === "h2");
if (h2Blocks.length < 5) errors.push("At least five H2 sections are required for FL-M008.");
const h2Roles = new Map();
for (const block of h2Blocks) {
  if (!String(block.text || "").trim()) errors.push("Every H2 needs text.");
  if (block.role) {
    if (h2Roles.has(block.role)) errors.push(`H2 role ${block.role} appears more than once.`);
    h2Roles.set(block.role, block);
  }
}
for (const role of ["scenario", "strategy", "firm-help", "cta"]) {
  if (!h2Roles.has(role)) errors.push(`Required H2 role ${role} is missing.`);
}
if (h2Blocks.at(-1)?.role !== "cta") errors.push("The final consumer-copy H2 must have role cta.");

const allowedBlocks = new Set(["p", "h2", "h3", "ul", "ol"]);
const allowedRuns = new Set(["text", "strong", "internal_link", "citation"]);
const usedLinkIds = [];
const usedLinkBlocks = new Map();
const usedSourceIds = [];
for (const [blockIndex, block] of data.content.entries()) {
  if (!allowedBlocks.has(block.type)) {
    errors.push(`content[${blockIndex}] has unsupported type ${block.type || "(missing)"}.`);
    continue;
  }
  let runGroups = [];
  if (block.type === "p") runGroups = [block.runs];
  if (["ul", "ol"].includes(block.type)) {
    if (!Array.isArray(block.items) || !block.items.length) errors.push(`content[${blockIndex}] list must contain items.`);
    runGroups = (block.items || []).map((item) => item.runs);
  }
  if (block.type === "p" && sentenceCount(blockText(block)) > 3) {
    errors.push(`content[${blockIndex}] exceeds the three-sentence paragraph limit.`);
  }
  for (const runs of runGroups) {
    if (!Array.isArray(runs) || !runs.length) {
      errors.push(`content[${blockIndex}] has an empty run collection.`);
      continue;
    }
    for (const run of runs) {
      if (!allowedRuns.has(run.type)) errors.push(`content[${blockIndex}] has unsupported run type ${run.type || "(missing)"}.`);
      if (!runText(run)) errors.push(`content[${blockIndex}] contains an empty run.`);
      if (run.type === "internal_link") {
        usedLinkIds.push(run.link_id);
        if (!usedLinkBlocks.has(run.link_id)) usedLinkBlocks.set(run.link_id, []);
        usedLinkBlocks.get(run.link_id).push(blockIndex);
        const link = linkById.get(run.link_id);
        if (!link) errors.push(`content[${blockIndex}] references unknown link ${run.link_id || "(missing)"}.`);
        else if (run.text !== link.anchor) errors.push(`${run.link_id}: run text must match manifested anchor exactly.`);
      }
      if (run.type === "citation") {
        usedSourceIds.push(run.source_id);
        if (!sourceById.has(run.source_id)) errors.push(`content[${blockIndex}] references unknown source ${run.source_id}.`);
        if (run.text !== `[${run.source_id}]`) errors.push(`Source ${run.source_id}: citation text must be [${run.source_id}].`);
      }
    }
  }
}

for (const link of data.link_manifest) {
  const uses = usedLinkIds.filter((id) => id === link.id).length;
  if (uses !== 1) errors.push(`${link.id}: internal link must appear exactly once in content; found ${uses}.`);
}
const ctaBlockIndex = data.content.findIndex((block) => block.type === "h2" && block.role === "cta");
for (const link of data.link_manifest.filter((item) => item.supporting_authority === "consultation-cta")) {
  const blocks = usedLinkBlocks.get(link.id) || [];
  if (blocks.length === 1 && blocks[0] <= ctaBlockIndex) {
    errors.push(`${link.id}: consultation CTA must appear after the final role=cta H2.`);
  }
}
for (const id of usedLinkIds) {
  if (usedLinkIds.filter((item) => item === id).length > 1) errors.push(`${id}: duplicate internal-link placement.`);
}
for (const source of data.sources) {
  const uses = usedSourceIds.filter((id) => id === source.id).length;
  if (uses !== 1) errors.push(`Source ${source.id}: body citation must appear exactly once; found ${uses}.`);
}

const consumerText = data.content.map(blockText).join(" ");
const wordCount = countWords(consumerText);
if (wordCount < 1100 || wordCount > 1700) {
  errors.push(`Consumer copy must contain 1,100–1,700 words; found ${wordCount}.`);
}
if (/\u2014/.test(consumerText)) errors.push("Consumer copy contains an em dash.");
if (/[•●▪◦]/.test(consumerText)) errors.push("Consumer copy contains a Unicode bullet; use list blocks.");
if (/\[(?:LOCAL DETAIL|INSERT|TODO|TBD)[^\]]*\]/i.test(consumerText)) errors.push("Consumer copy contains an unresolved placeholder.");

const fullReviewText = [
  meta.title_tag,
  meta.meta_description,
  meta.cms_title,
  meta.social_title,
  meta.social_description,
  meta.h1,
  meta.media_note,
  consumerText,
].join(" ");
for (const term of data.quality_contract?.forbidden_terms || []) {
  if (term && fullReviewText.toLowerCase().includes(String(term).toLowerCase())) {
    errors.push(`Forbidden content term remains: ${term}.`);
  }
}
if (errors.length) fail(errors);

const BLUE = "17365D";
const BLUE_LIGHT = "EAF0F6";
const GOLD = "C99B42";
const GRAY = "5F6B76";
const TEXT = "202B35";

function textRun(text, options = {}) {
  return new TextRun({ text, font: "Arial", size: 24, color: TEXT, ...options });
}

function makeRuns(runs) {
  return runs.map((run) => {
    if (run.type === "text") return textRun(run.text);
    if (run.type === "strong") return textRun(run.text, { bold: true });
    if (run.type === "internal_link") {
      const link = linkById.get(run.link_id);
      return new ExternalHyperlink({
        link: link.client_url,
        children: [textRun(run.text, { bold: true, color: "2E5090", underline: {} })],
      });
    }
    if (run.type === "citation") {
      const source = sourceById.get(run.source_id);
      return new ExternalHyperlink({
        link: source.url,
        children: [textRun(run.text, { color: GRAY, superscript: true, size: 18 })],
      });
    }
    throw new Error(`Unsupported run type: ${run.type}`);
  });
}

const children = [];
children.push(new Paragraph({
  style: "ArtifactLabel",
  children: [new TextRun({ text: "PROPOSED REPLACEMENT DRAFT  |  NOT PUBLISHED", bold: true, font: "Arial", size: 18, color: "FFFFFF" })],
  shading: { type: ShadingType.CLEAR, fill: BLUE },
  border: { bottom: { color: GOLD, style: BorderStyle.SINGLE, size: 14, space: 1 } },
}));
children.push(new Paragraph({ style: "MetadataHeading", children: [textRun("Proposed metadata", { bold: true, color: BLUE, size: 26 })] }));
for (const [label, value] of [
  ["Retained implementation URL", meta.client_url],
  ["Canonical URL", meta.canonical_url],
  ["Title tag", meta.title_tag],
  ["Meta description", meta.meta_description],
  ["CMS page title", meta.cms_title],
  ["Open Graph / Twitter title", meta.social_title],
  ["Open Graph / Twitter description", meta.social_description],
  ["H1", meta.h1],
  ["Robots", meta.robots],
  ["Media note", meta.media_note],
  ["Architecture", `FL-M008 | Situational | ${meta.v2_reference_path}`],
]) {
  children.push(new Paragraph({
    style: "MetadataLine",
    children: [textRun(`${label}: `, { bold: true, color: BLUE, size: 20 }), textRun(value, { size: 20, color: GRAY })],
  }));
}
children.push(new Paragraph({ text: "" }));
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [textRun(meta.h1, { bold: true, color: BLUE, size: 36 })] }));

let listIndex = 0;
for (const block of data.content) {
  if (block.type === "p") {
    children.push(new Paragraph({ children: makeRuns(block.runs), style: "Normal" }));
  } else if (block.type === "h2") {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [textRun(block.text, { bold: true, color: BLUE, size: 30 })] }));
  } else if (block.type === "h3") {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: [textRun(block.text, { bold: true, color: BLUE, size: 26 })] }));
  } else if (["ul", "ol"].includes(block.type)) {
    const reference = block.type === "ul" ? "situational-bullets" : "situational-numbers";
    for (const item of block.items) {
      children.push(new Paragraph({
        children: makeRuns(item.runs),
        numbering: { reference, level: 0, instance: listIndex },
        style: "Normal",
      }));
    }
    listIndex += 1;
  }
}

children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [textRun("Sources", { bold: true, color: BLUE, size: 30 })] }));
if (!data.sources.length) {
  children.push(new Paragraph({ style: "Source", children: [new TextRun({ text: "Synthetic fixture: no sources.", font: "Arial", size: 24, color: GRAY })] }));
} else {
  for (const source of data.sources) {
    children.push(new Paragraph({
      style: "Source",
      children: [
        new TextRun({ text: `[${source.id}] ${source.label} | `, font: "Arial", size: 24, color: GRAY }),
        new ExternalHyperlink({
          link: source.url,
          children: [new TextRun({ text: source.url, font: "Arial", size: 24, color: "2E5090", underline: {} })],
        }),
      ],
    }));
  }
}

const document = new Document({
  creator: "Local FL-M008 Situational workflow replacement",
  title: meta.title_tag,
  subject: "Proposed replacement High-Conflict Divorce page",
  description: "Proposed replacement draft; not published.",
  styles: {
    default: {
      document: { run: { font: "Arial", size: 24, color: TEXT }, paragraph: { spacing: { after: 120, line: 300 } } },
      heading1: { run: { font: "Arial", size: 36, bold: true, color: BLUE }, paragraph: { spacing: { before: 240, after: 180 }, keepNext: true } },
      heading2: { run: { font: "Arial", size: 30, bold: true, color: BLUE }, paragraph: { spacing: { before: 360, after: 120 }, keepNext: true } },
      heading3: { run: { font: "Arial", size: 26, bold: true, color: BLUE }, paragraph: { spacing: { before: 280, after: 100 }, keepNext: true } },
    },
    paragraphStyles: [
      { id: "ArtifactLabel", name: "Artifact Label", basedOn: "Normal", quickFormat: true, run: { font: "Arial", size: 18, bold: true, color: "FFFFFF" }, paragraph: { spacing: { before: 0, after: 160 }, indent: { left: 160, right: 160 }, alignment: AlignmentType.CENTER } },
      { id: "MetadataHeading", name: "Metadata Heading", basedOn: "Normal", quickFormat: true, run: { font: "Arial", size: 26, bold: true, color: BLUE }, paragraph: { spacing: { before: 120, after: 80 }, keepNext: true } },
      { id: "MetadataLine", name: "Metadata Line", basedOn: "Normal", quickFormat: true, run: { font: "Arial", size: 20, color: GRAY }, paragraph: { spacing: { before: 20, after: 40 }, indent: { left: 160, right: 160 } }, shading: { type: ShadingType.CLEAR, fill: BLUE_LIGHT } },
      { id: "Source", name: "Source", basedOn: "Normal", quickFormat: true, run: { font: "Arial", size: 24, color: GRAY }, paragraph: { spacing: { before: 40, after: 80 } } },
    ],
  },
  numbering: {
    config: [
      { reference: "situational-bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "situational-numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: convertInchesToTwip(1), right: convertInchesToTwip(1), bottom: convertInchesToTwip(1), left: convertInchesToTwip(1) },
      },
    },
    headers: {
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: synthetic ? "SYNTHETIC FL-M008 TEST" : `${meta.firm_name}  |  PROPOSED REPLACEMENT`, font: "Arial", size: 16, color: GRAY })] })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Proposed draft  |  Page ", font: "Arial", size: 16, color: GRAY }), new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 16, color: GRAY })] })] }),
    },
    children,
  }],
});

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
Packer.toBuffer(document)
  .then((buffer) => fs.writeFileSync(outputPath, buffer))
  .then(() => console.log(`PASS: generated ${outputPath} (${wordCount} consumer-copy words; ${data.link_manifest.length} internal links; ${data.sources.length} sources).`))
  .catch((error) => fail([`DOCX generation failed: ${error.message}`]));
