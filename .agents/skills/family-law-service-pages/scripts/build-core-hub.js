#!/usr/bin/env node
/**
 * LOCAL REPLACEMENT: Core Practice-Area Hub DOCX generator.
 *
 * The original transfer did not contain a Core Hub template or generator.
 * This implementation is grounded in this skill's SKILL.md and the governing
 * Family Law Architecture V2 artifact. It does not generate or verify prose.
 *
 * Usage: node build-core-hub.js <input.json> <output.docx>
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
  console.error("Usage: node build-core-hub.js <input.json> <output.docx>");
  process.exit(2);
}

const inputPath = path.resolve(inputArg);
const outputPath = path.resolve(outputArg);
const repoRoot = path.resolve(__dirname, "../../../..");
const architecturePath = path.join(
  repoRoot,
  "context/architecture/Family_Law_StructureV2.html",
);

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
  const read = (key, index) => compact.d[key][index];
  const nodes = compact.n.map((tuple, index) => ({
    index,
    id: tuple[0],
    name: tuple[1],
    parent: tuple[2],
    pageType: read("pageType", tuple[7]),
    nodeClass: read("nodeClass", tuple[8]),
    publishability: read("publishability", tuple[9]),
    path: tuple[10],
    requiredness: read("requiredness", tuple[13]),
    decision: read("decisionState", tuple[16]),
    gate: read("governanceGate", tuple[17]),
  }));
  const relationships = compact.e.map((tuple) => ({
    source: tuple[0],
    target: tuple[1],
    type: read("relationshipType", tuple[2]),
    occurrences: tuple[3],
    status: read("relationshipStatus", tuple[4]),
    provenance: read("relationshipProvenance", tuple[5]),
    notes: read("relationshipNotes", tuple[6]),
  }));
  return { nodes, relationships };
}

function textOfRuns(runs) {
  return (runs || []).map((run) => run.text || "").join("");
}

function textOfBlock(block) {
  if (["h1", "h2", "h3"].includes(block.type)) return block.text || "";
  if (block.type === "p") return textOfRuns(block.runs);
  if (["ul", "ol"].includes(block.type)) {
    return (block.items || []).map((item) => textOfRuns(item.runs)).join(" ");
  }
  return "";
}

function countWords(text) {
  return (text.match(/[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*/g) || []).length;
}

function validHttpUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" || url.protocol === "http:";
  } catch {
    return false;
  }
}

const data = readJson(inputPath);
const architecture = loadArchitecture();
const nodeById = new Map(architecture.nodes.map((node) => [node.id, node]));
const errors = [];

if (data.schema_version !== 1) errors.push("schema_version must be 1.");
if (data.workflow !== "core-hub") errors.push('workflow must be "core-hub".');
if (!data.meta || typeof data.meta !== "object") errors.push("meta is required.");
if (!Array.isArray(data.content)) errors.push("content must be an array.");
if (!Array.isArray(data.link_manifest)) errors.push("link_manifest must be an array.");
if (!Array.isArray(data.sources)) errors.push("sources must be an array, even when empty.");
if (errors.length) fail(errors);

const meta = data.meta;
const synthetic = meta.synthetic_fixture === true;
const hub = nodeById.get(meta.architecture_node_id);
if (!hub) {
  errors.push(`Unknown V2 architecture node: ${meta.architecture_node_id || "(missing)"}.`);
} else {
  if (hub.pageType !== "Core Practice-Area Hub") {
    errors.push(`${hub.id} is ${hub.pageType}, not a Core Practice-Area Hub.`);
  }
  if (hub.nodeClass !== "Canonical Page" || hub.publishability !== "Publishable") {
    errors.push(`${hub.id} is not a publishable canonical page.`);
  }
  if (meta.canonical_path !== hub.path) {
    errors.push(`canonical_path must match V2 exactly: ${hub.path}.`);
  }
  if (hub.gate === "HOLD — ARCHITECTURE REVIEW" || hub.gate === "BLOCK — NON-PUBLISHABLE") {
    errors.push(`${hub.id} cannot proceed while its V2 gate is ${hub.gate}.`);
  }
  if (hub.gate !== "PASS — CANONICAL") {
    if (meta.gate_approval !== "approved" || !String(meta.gate_evidence || "").trim()) {
      errors.push(`${hub.id} requires gate_approval "approved" and non-empty gate_evidence for ${hub.gate}.`);
    }
  }
}

if (meta.page_type !== "Core Practice-Area Hub") {
  errors.push('meta.page_type must be "Core Practice-Area Hub".');
}
if (!String(meta.title || "").trim()) errors.push("meta.title is required.");
const siteUrl = validHttpUrl(meta.site_origin) ? new URL(meta.site_origin) : null;
if (!siteUrl) {
  errors.push("meta.site_origin must be an HTTP(S) origin.");
} else if (siteUrl.pathname !== "/" || siteUrl.search || siteUrl.hash) {
  errors.push("meta.site_origin must contain only the scheme and host.");
}
if (synthetic) {
  if (siteUrl && siteUrl.hostname !== "example.com") {
    errors.push("Synthetic fixtures must use the reserved example.com origin.");
  }
  if (meta.firm_name || meta.jurisdiction) {
    errors.push("Synthetic fixtures must omit firm_name and jurisdiction rather than invent facts.");
  }
  if (data.sources.length !== 0) errors.push("Synthetic fixtures must not contain sources or citation runs.");
  if (meta.voice_source !== "synthetic-fixture") {
    errors.push('Synthetic fixtures must set voice_source to "synthetic-fixture".');
  }
  if (data.link_inventory?.status !== "synthetic-fixture") {
    errors.push('Synthetic fixtures must set link_inventory.status to "synthetic-fixture".');
  }
} else {
  for (const key of ["firm_name", "jurisdiction", "voice_source"]) {
    if (!String(meta[key] || "").trim()) errors.push(`meta.${key} is required for production output.`);
  }
  if (data.link_inventory?.status !== "reviewed" || !String(data.link_inventory?.evidence || "").trim()) {
    errors.push("Production output requires a reviewed link_inventory with evidence.");
  }
  if (hub && hub.requiredness !== "Required") {
    if (meta.activation_approval !== "approved" || !String(meta.activation_evidence || "").trim()) {
      errors.push(`${hub.id} is ${hub.requiredness}; production output requires activation_approval "approved" and activation_evidence.`);
    }
  }
}

const expectedName = synthetic
  ? /^synthetic-[a-z0-9]+(?:-[a-z0-9]+)*-core\.docx$/
  : /^[a-z0-9]+(?:-[a-z0-9]+)*-[a-z0-9]+(?:-[a-z0-9]+)*-core\.docx$/;
if (!expectedName.test(path.basename(outputPath))) {
  errors.push(`Output filename does not match the ${synthetic ? "synthetic fixture" : "production"} Core pattern.`);
}

const linkById = new Map();
const manifestedTargetUrls = new Set();
for (const link of data.link_manifest) {
  if (!link.id || linkById.has(link.id)) {
    errors.push(`Every link_manifest entry needs a unique id; problem at ${link.id || "(missing)"}.`);
    continue;
  }
  linkById.set(link.id, link);
  if (manifestedTargetUrls.has(link.target_url)) {
    errors.push(`${link.id}: target_url duplicates another manifest entry; one destination may appear only once.`);
  }
  manifestedTargetUrls.add(link.target_url);
  const target = nodeById.get(link.target_node_id);
  if (!hub || link.source_node_id !== hub.id) {
    errors.push(`${link.id}: source_node_id must be the selected hub ${hub?.id || "(unknown)"}.`);
  }
  if (!target) {
    errors.push(`${link.id}: unknown V2 target ${link.target_node_id || "(missing)"}.`);
    continue;
  }
  if (target.nodeClass !== "Canonical Page" || target.publishability !== "Publishable") {
    errors.push(`${link.id}: V2 target ${target.id} is not a publishable canonical page.`);
  }
  if (/^(?:HOLD|BLOCK) —/.test(target.gate || "")) {
    errors.push(`${link.id}: V2 target ${target.id} cannot be linked while its gate is ${target.gate}.`);
  } else if (target.gate !== "PASS — CANONICAL") {
    if (link.target_gate_approval !== "approved" || !String(link.target_gate_evidence || "").trim()) {
      errors.push(
        `${link.id}: V2 target ${target.id} requires target_gate_approval "approved" `
        + `and target_gate_evidence for ${target.gate}.`,
      );
    }
  }
  if (!target.path) errors.push(`${link.id}: V2 target ${target.id} has no resolved URL path.`);
  if (link.target_path !== target.path) errors.push(`${link.id}: target_path must match V2 exactly: ${target.path}.`);
  if (!validHttpUrl(link.target_url)) {
    errors.push(`${link.id}: target_url must be an HTTP(S) URL.`);
  } else {
    const targetUrl = new URL(link.target_url);
    if (targetUrl.pathname !== target.path || targetUrl.search || targetUrl.hash) {
      errors.push(`${link.id}: target_url must match V2 target path ${target.path} without a query or fragment.`);
    }
    if (siteUrl && targetUrl.origin !== siteUrl.origin) {
      errors.push(`${link.id}: internal target origin must match meta.site_origin ${siteUrl.origin}.`);
    }
  }
  const candidates = architecture.relationships.filter(
    (relationship) => relationship.source === hub?.index && relationship.target === target.index,
  );
  const relationship = candidates.find((candidate) => candidate.type === link.relationship_type);
  if (!relationship) {
    errors.push(`${link.id}: no directional V2 ${link.relationship_type || "(missing type)"} relationship ${hub?.id} → ${target.id}.`);
  } else if (relationship.status === "Non-linkable structural target — no URL") {
    errors.push(`${link.id}: V2 marks the relationship target non-linkable.`);
  }
  if (!String(link.inclusion_reason || "").trim()) errors.push(`${link.id}: inclusion_reason is required.`);
  if (synthetic) {
    if (link.publication_state !== "synthetic-fixture") {
      errors.push(`${link.id}: synthetic links must use publication_state "synthetic-fixture".`);
    }
  } else if (link.publication_state !== "published" || !String(link.publication_evidence || "").trim()) {
    errors.push(`${link.id}: production links require published state and publication_evidence.`);
  }
}

const sourceById = new Map();
for (const source of data.sources) {
  if (!source.id || sourceById.has(source.id)) {
    errors.push(`Every source needs a unique id; problem at ${source.id || "(missing)"}.`);
    continue;
  }
  sourceById.set(source.id, source);
  if (!String(source.identifier || "").trim()) errors.push(`${source.id}: source identifier is required.`);
  if (!validHttpUrl(source.url)) errors.push(`${source.id}: source URL must be HTTP(S).`);
}
if (data.sources.length > 8) errors.push("Core Hub source count exceeds the imported skill's maximum of 8.");
const sourceNumberById = new Map(data.sources.map((source, index) => [source.id, index + 1]));

const allowedTypes = new Set(["h1", "h2", "h3", "p", "ul", "ol"]);
let h1Count = 0;
let currentHeadingLevel = 0;
const linkUse = new Map([...linkById.keys()].map((id) => [id, 0]));
const citationUse = new Map([...sourceById.keys()].map((id) => [id, 0]));
const roles = new Map();
const localDetailPattern = /\[LOCAL DETAIL:\s*[^\]\s][^\]]*\]/g;

for (const [index, block] of data.content.entries()) {
  if (!allowedTypes.has(block.type)) {
    errors.push(`content[${index}] has unsupported type ${block.type}.`);
    continue;
  }
  if (["h1", "h2", "h3"].includes(block.type)) {
    if (!String(block.text || "").trim()) errors.push(`content[${index}] heading text is required.`);
    const level = Number(block.type.slice(1));
    if (level === 1) h1Count += 1;
    if (currentHeadingLevel && level > currentHeadingLevel + 1) {
      errors.push(`content[${index}] skips from H${currentHeadingLevel} to H${level}.`);
    }
    currentHeadingLevel = level;
    if (block.role) {
      if (roles.has(block.role)) errors.push(`Heading role ${block.role} appears more than once.`);
      roles.set(block.role, index);
    }
    continue;
  }
  const items = block.type === "p" ? [{ runs: block.runs }] : block.items;
  if (!Array.isArray(items) || items.length === 0) errors.push(`content[${index}] must contain content.`);
  for (const item of items || []) {
    if (!Array.isArray(item.runs) || item.runs.length === 0) {
      errors.push(`content[${index}] has an item without runs.`);
      continue;
    }
    if (!textOfRuns(item.runs).trim()) {
      errors.push(`content[${index}] contains an empty paragraph or list item.`);
    }
    for (const run of item.runs) {
      if (!String(run.text || "").length) errors.push(`content[${index}] contains an empty run.`);
      if (run.link_id && run.citation_id) errors.push(`content[${index}] run cannot be both link and citation.`);
      if (run.link_id) {
        if (!linkById.has(run.link_id)) errors.push(`content[${index}] uses unknown link_id ${run.link_id}.`);
        else linkUse.set(run.link_id, linkUse.get(run.link_id) + 1);
      }
      if (run.citation_id) {
        if (!sourceById.has(run.citation_id)) errors.push(`content[${index}] uses unknown citation_id ${run.citation_id}.`);
        else {
          citationUse.set(run.citation_id, citationUse.get(run.citation_id) + 1);
          const expectedMarker = `[${sourceNumberById.get(run.citation_id)}]`;
          if (run.text !== expectedMarker) {
            errors.push(`content[${index}] citation ${run.citation_id} must use marker ${expectedMarker}.`);
          }
        }
      }
      const runText = String(run.text || "");
      if (/\[LOCAL DETAIL/i.test(runText)) {
        const validMarkers = runText.match(localDetailPattern) || [];
        const unmatched = runText.replace(localDetailPattern, "");
        if (validMarkers.length === 0 || /\[LOCAL DETAIL/i.test(unmatched)) {
          errors.push(
            `content[${index}] has a malformed local-detail marker; use [LOCAL DETAIL: description].`,
          );
        }
        if (run.bold !== true) {
          errors.push(`content[${index}] local-detail markers must be bold runs.`);
        }
        if (run.link_id || run.citation_id) {
          errors.push(`content[${index}] local-detail markers cannot also be links or citations.`);
        }
      }
    }
  }
}

if (h1Count !== 1) errors.push(`Core output requires exactly one H1; found ${h1Count}.`);
if (data.content[0]?.type !== "h1") errors.push("The first content block must be the H1.");
if (data.content[0]?.text !== meta.title) errors.push("The H1 must exactly match meta.title.");
if (data.content[1]?.type !== "p" || data.content[2]?.type !== "p") {
  errors.push("The H1 must be followed by two opening paragraphs.");
}
for (const role of ["firm-help", "faq", "cta"]) {
  if (!roles.has(role)) errors.push(`Required H2 role is missing: ${role}.`);
  else if (data.content[roles.get(role)]?.type !== "h2") errors.push(`Role ${role} must be assigned to an H2.`);
}
if (roles.has("firm-help") && roles.has("faq") && roles.has("cta")) {
  if (!(roles.get("firm-help") < roles.get("faq") && roles.get("faq") < roles.get("cta"))) {
    errors.push("Required H2 roles must appear in firm-help, FAQ, then CTA order.");
  }
}
for (const role of ["firm-help", "faq", "cta"]) {
  if (!roles.has(role)) continue;
  const start = roles.get(role);
  const nextH2 = data.content.findIndex((block, index) => index > start && block.type === "h2");
  const end = nextH2 === -1 ? data.content.length : nextH2;
  const hasBody = data.content.slice(start + 1, end).some(
    (block) => ["p", "ul", "ol"].includes(block.type) && textOfBlock(block).trim(),
  );
  if (!hasBody) errors.push(`Required ${role} section must contain body content.`);
}
if (roles.has("faq")) {
  const faqIndex = roles.get("faq");
  const nextH2 = data.content.findIndex((block, index) => index > faqIndex && block.type === "h2");
  const faqEnd = nextH2 === -1 ? data.content.length : nextH2;
  if (!data.content.slice(faqIndex + 1, faqEnd).some((block) => block.type === "h3")) {
    errors.push("The Hub FAQ block needs at least one H3 question.");
  }
  const faqBlocks = data.content.slice(faqIndex + 1, faqEnd);
  for (const [position, block] of faqBlocks.entries()) {
    if (block.type !== "h3") continue;
    const answerEndOffset = faqBlocks.findIndex(
      (candidate, candidateIndex) => candidateIndex > position && ["h2", "h3"].includes(candidate.type),
    );
    const answerEnd = answerEndOffset === -1 ? faqBlocks.length : answerEndOffset;
    const hasAnswer = faqBlocks.slice(position + 1, answerEnd).some(
      (candidate) => ["p", "ul", "ol"].includes(candidate.type) && textOfBlock(candidate).trim(),
    );
    if (!hasAnswer) errors.push(`FAQ question must contain a body answer: ${block.text || "(untitled)"}.`);
  }
}
for (const [id, count] of linkUse) {
  if (count !== 1) errors.push(`Manifested internal link ${id} must appear exactly once; found ${count}.`);
}
for (const [id, count] of citationUse) {
  if (count !== 1) errors.push(`Source ${id} must have exactly one in-body citation marker; found ${count}.`);
}

const fullText = data.content.map(textOfBlock).join(" ");
const wordCount = countWords(fullText);
if (wordCount < 1800 || wordCount > 2600) {
  errors.push(`V2 Core Hub word target is 1,800–2,600; content has ${wordCount} words.`);
}
if (errors.length) fail(errors);

const COLORS = {
  navy: "1F2A44",
  blue: "2E5090",
  gray: "666666",
  light: "EEF2F7",
  border: "CBD5E1",
};

function renderRuns(runs) {
  return runs.map((run) => {
    const options = {
      text: run.text,
      font: "Arial",
      size: 24,
      bold: run.bold === true,
      italics: run.italics === true,
    };
    if (run.link_id) {
      return new ExternalHyperlink({
        link: linkById.get(run.link_id).target_url,
        children: [new TextRun({ ...options, bold: true, color: COLORS.blue, underline: { type: "single", color: COLORS.blue } })],
      });
    }
    if (run.citation_id) {
      return new ExternalHyperlink({
        link: sourceById.get(run.citation_id).url,
        children: [new TextRun({ ...options, size: 18, color: COLORS.gray, superScript: true })],
      });
    }
    return new TextRun(options);
  });
}

function bodyParagraph(runs, extra = {}) {
  return new Paragraph({
    spacing: { before: 120, after: 120, line: 300 },
    widowControl: true,
    children: renderRuns(runs),
    ...extra,
  });
}

const children = [];
if (synthetic) {
  children.push(new Paragraph({
    spacing: { after: 180 },
    shading: { type: ShadingType.CLEAR, fill: "FFF4CC", color: "auto" },
    border: {
      top: { style: BorderStyle.SINGLE, size: 8, color: "C69214" },
      bottom: { style: BorderStyle.SINGLE, size: 8, color: "C69214" },
      left: { style: BorderStyle.SINGLE, size: 8, color: "C69214" },
      right: { style: BorderStyle.SINGLE, size: 8, color: "C69214" },
    },
    children: [new TextRun({
      text: "SYNTHETIC WORKFLOW FIXTURE • NOT CLIENT CONTENT • NOT FOR PUBLICATION",
      font: "Arial",
      size: 20,
      bold: true,
      color: "6B4F00",
    })],
  }));
}

for (const block of data.content) {
  if (block.type === "h1") {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_1,
      keepNext: true,
      children: [new TextRun({ text: block.text, font: "Arial", size: 36, bold: true, color: COLORS.navy })],
    }));
  } else if (block.type === "h2") {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_2,
      keepNext: true,
      children: [new TextRun({ text: block.text, font: "Arial", size: 30, bold: true, color: COLORS.navy })],
    }));
  } else if (block.type === "h3") {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_3,
      keepNext: true,
      children: [new TextRun({ text: block.text, font: "Arial", size: 26, bold: true, color: COLORS.blue })],
    }));
  } else if (block.type === "p") {
    children.push(bodyParagraph(block.runs));
  } else {
    const reference = block.type === "ul" ? "core-bullets" : "core-numbers";
    for (const item of block.items) {
      children.push(bodyParagraph(item.runs, {
        numbering: { reference, level: 0 },
        keepNext: false,
      }));
    }
  }
}

if (data.sources.length > 0) {
  children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    keepNext: true,
    children: [new TextRun({ text: "Sources", font: "Arial", size: 30, bold: true, color: COLORS.navy })],
  }));
  data.sources.forEach((source, index) => {
    children.push(bodyParagraph([
      { text: `[${index + 1}] ${source.identifier} | `, bold: index === 0 },
    ], {
      indent: { left: convertInchesToTwip(0.3), hanging: convertInchesToTwip(0.3) },
      children: [
        new TextRun({ text: `[${index + 1}] ${source.identifier} | `, font: "Arial", size: 24 }),
        new ExternalHyperlink({
          link: source.url,
          children: [new TextRun({ text: source.url, font: "Arial", size: 24, color: COLORS.blue, underline: {} })],
        }),
      ],
    }));
  });
}

const headerText = synthetic ? "Synthetic Core Hub Fixture" : `${meta.firm_name} • ${hub.name}`;
const doc = new Document({
  creator: "Core Practice-Area Hub local workflow",
  title: meta.title,
  subject: synthetic ? "Synthetic mechanical fixture" : `${hub.name} Core Practice-Area Hub`,
  description: synthetic
    ? "Synthetic document used only to verify generation, validation, hyperlinks, and rendering."
    : "Generated Core Practice-Area Hub draft requiring editorial and legal review.",
  numbering: {
    config: [
      {
        reference: "core-bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 540, hanging: 260 } } },
        }],
      },
      {
        reference: "core-numbers",
        levels: [{
          level: 0,
          format: LevelFormat.DECIMAL,
          text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 540, hanging: 260 } } },
        }],
      },
    ],
  },
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 24, color: "111827" },
        paragraph: { spacing: { before: 120, after: 120, line: 300 } },
      },
      heading1: {
        run: { font: "Arial", size: 36, bold: true, color: COLORS.navy },
        paragraph: { spacing: { before: 240, after: 180 }, keepNext: true, outlineLevel: 0 },
      },
      heading2: {
        run: { font: "Arial", size: 30, bold: true, color: COLORS.navy },
        paragraph: { spacing: { before: 360, after: 140 }, keepNext: true, outlineLevel: 1 },
      },
      heading3: {
        run: { font: "Arial", size: 26, bold: true, color: COLORS.blue },
        paragraph: { spacing: { before: 280, after: 100 }, keepNext: true, outlineLevel: 2 },
      },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.border } },
          children: [new TextRun({ text: headerText, font: "Arial", size: 18, color: COLORS.gray })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", font: "Arial", size: 18, color: COLORS.gray }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: COLORS.gray }),
            new TextRun({ text: " of ", font: "Arial", size: 18, color: COLORS.gray }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: COLORS.gray }),
          ],
        })],
      }),
    },
    children,
  }],
});

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
Packer.toBuffer(doc)
  .then((buffer) => {
    fs.writeFileSync(outputPath, buffer);
    console.log(`DOCX written: ${outputPath}`);
    console.log(`V2 node: ${hub.id} (${hub.name}) • ${hub.gate}`);
    console.log(`Content words: ${wordCount} • manifested links: ${data.link_manifest.length} • sources: ${data.sources.length}`);
    console.log(synthetic ? "Scope: synthetic mechanics only." : "Scope: generation only; editorial and legal review remain required.");
  })
  .catch((error) => fail([`DOCX generation failed: ${error.message}`]));
