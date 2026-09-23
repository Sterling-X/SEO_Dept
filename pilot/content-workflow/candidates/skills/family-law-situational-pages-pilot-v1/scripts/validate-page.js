#!/usr/bin/env node
/**
 * LOCAL REPLACEMENT / NOT RECOVERED ORIGINAL
 *
 * Page-level pre-delivery scanner for the demonstrated FL-M008 Situational
 * workflow. It does not reuse the Core page contract and keeps explicit V2,
 * skill navigation, and consultation-CTA authority distinct.
 *
 * Usage: node scripts/validate-page.js <page.docx> --manifest <input.json>
 *
 * PILOT CANDIDATE v1. Baseline: .agents/skills/family-law-situational-pages/scripts/validate-page.js
 * (hash in ../pilot-manifest.json). Added: broader placeholder grammar, plain-text citation-marker
 * detection, first-appearance citation order, Sources-row id/label/URL parity with the manifest.
 */
const PLACEHOLDER_PATTERNS = [
  /\[(?!\d+\])[^\]\n]{1,120}\]/,
  /\{\{[^}\n]{0,120}\}\}/,
  /<<[^>\n]{0,120}>>/,
  /\b(?:TODO|TBD|FIXME|XXX|PLACEHOLDER)\b/,
  /\bTK\b/,
  /lorem ipsum/i,
];
function findPlaceholder(text) {
  for (const pattern of PLACEHOLDER_PATTERNS) {
    const match = String(text || "").match(pattern);
    if (match) return match[0];
  }
  return null;
}

const fs = require("fs");
const path = require("path");
const AdmZip = require("adm-zip");

const args = process.argv.slice(2);
const docxArg = args[0];
const manifestIndex = args.indexOf("--manifest");
const manifestArg = manifestIndex >= 0 ? args[manifestIndex + 1] : null;
if (!docxArg || !manifestArg) {
  console.error("Usage: node scripts/validate-page.js <page.docx> --manifest <input.json>");
  process.exit(2);
}

const docxPath = path.resolve(docxArg);
const manifestPath = path.resolve(manifestArg);
let manifest;
try {
  manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
} catch (error) {
  console.error(`ERROR: Cannot read manifest ${manifestPath}: ${error.message}`);
  process.exit(2);
}
if (manifest.schema_version !== 2 || manifest.workflow !== "situational-fl-m008-local-replacement") {
  console.error("ERROR: Manifest is not the scoped FL-M008 local replacement contract.");
  process.exit(2);
}

let zip;
try {
  zip = new AdmZip(docxPath);
} catch (error) {
  console.error(`ERROR: Cannot open DOCX ${docxPath}: ${error.message}`);
  process.exit(2);
}
const documentXml = zip.readAsText("word/document.xml");
const relsXml = zip.readAsText("word/_rels/document.xml.rels");
if (!documentXml || !relsXml) {
  console.error("ERROR: DOCX is missing document.xml or document.xml.rels.");
  process.exit(2);
}

function decodeXml(value) {
  return String(value || "")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, "&");
}

function textFromXml(xml) {
  return [...String(xml || "").matchAll(/<w:t[^>]*>([\s\S]*?)<\/w:t>/g)]
    .map((match) => decodeXml(match[1]))
    .join("");
}

function countWords(text) {
  return (String(text || "").match(/[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*/g) || []).length;
}

function sentenceCount(text) {
  const matches = String(text || "").match(/(?:[.!?](?:[\"')\]]+)?)(?=\s|$)/g);
  return matches ? matches.length : (String(text || "").trim() ? 1 : 0);
}

const findings = { hard: [], warnings: [], facts: [] };
const fail = (message) => findings.hard.push(message);
const warn = (message) => findings.warnings.push(message);
const fact = (message) => findings.facts.push(message);

const relsMap = new Map();
for (const match of relsXml.matchAll(/<Relationship\s+([^>]+?)\/>/g)) {
  const attributes = match[1];
  if (!/Type="[^"]*\/hyperlink"/i.test(attributes)) continue;
  const id = attributes.match(/\bId="([^"]+)"/)?.[1];
  const target = attributes.match(/\bTarget="([^"]+)"/)?.[1];
  if (id && target) relsMap.set(id, decodeXml(target));
}

let sourcesXmlIndex = -1;
for (const match of documentXml.matchAll(/<w:t[^>]*>([\s\S]*?)<\/w:t>/g)) {
  if (/^Sources\s*$/i.test(decodeXml(match[1]))) {
    sourcesXmlIndex = match.index;
    break;
  }
}
if (sourcesXmlIndex < 0) fail("Sources heading was not found.");

const linkOccurrences = [];
for (const match of documentXml.matchAll(/<w:hyperlink\s+([^>]*?)>([\s\S]*?)<\/w:hyperlink>/g)) {
  const rid = match[1].match(/r:id="([^"]+)"/)?.[1];
  if (!rid) continue;
  const url = relsMap.get(rid);
  if (!url) {
    fail(`Hyperlink ${rid} has no external relationship target.`);
    continue;
  }
  linkOccurrences.push({
    anchor: textFromXml(match[2]).trim(),
    url,
    inSources: sourcesXmlIndex >= 0 && match.index >= sourcesXmlIndex,
    index: match.index,
  });
}

const supportedAuthorities = new Set([
  "v2-explicit-relationship",
  "skill-parent-navigation",
  "skill-process-bridge",
  "consultation-cta",
]);
const authorityCounts = new Map([...supportedAuthorities].map((authority) => [authority, 0]));
for (const link of manifest.link_manifest || []) {
  if (!supportedAuthorities.has(link.supporting_authority)) {
    fail(`${link.id || "(missing link id)"}: unknown or missing supporting_authority.`);
    continue;
  }
  authorityCounts.set(link.supporting_authority, authorityCounts.get(link.supporting_authority) + 1);
}
for (const authority of ["skill-parent-navigation", "skill-process-bridge", "consultation-cta"]) {
  const count = authorityCounts.get(authority);
  if (count !== 1) fail(`FL-M008 requires exactly one ${authority} link; found ${count}.`);
}

const expectedInternal = new Map((manifest.link_manifest || []).map((link) => [link.client_url, link]));
const expectedSources = new Map((manifest.sources || []).map((source) => [source.url, source]));
const expectedUrls = new Set([...expectedInternal.keys(), ...expectedSources.keys()]);
for (const occurrence of linkOccurrences) {
  if (!expectedUrls.has(occurrence.url)) fail(`Unexpected hyperlink target in DOCX: ${occurrence.url}`);
}
for (const [url, link] of expectedInternal) {
  const uses = linkOccurrences.filter((item) => item.url === url);
  if (uses.length !== 1) fail(`${link.id}: internal destination must appear exactly once; found ${uses.length}.`);
  if (uses[0]?.inSources) fail(`${link.id}: internal destination appears in Sources instead of consumer copy.`);
  if (uses[0] && uses[0].anchor !== link.anchor) fail(`${link.id}: visible anchor does not match the manifest.`);
}
for (const [url, source] of expectedSources) {
  const bodyUses = linkOccurrences.filter((item) => item.url === url && !item.inSources);
  const sourceUses = linkOccurrences.filter((item) => item.url === url && item.inSources);
  if (bodyUses.length !== 1 || sourceUses.length !== 1) {
    fail(`Source ${source.id}: expected one body citation and one Sources hyperlink; found body=${bodyUses.length}, sources=${sourceUses.length}.`);
  }
  if (bodyUses[0] && bodyUses[0].anchor !== `[${source.id}]`) fail(`Source ${source.id}: body marker must be [${source.id}].`);
  if (sourceUses[0] && sourceUses[0].anchor !== source.url) fail(`Source ${source.id}: Sources hyperlink must display the full URL.`);
}
fact(`${expectedInternal.size} manifested internal link(s).`);
fact(`Link authority counts: ${[...authorityCounts].map(([authority, count]) => `${authority}=${count}`).join(", ")}.`);
fact(`${expectedSources.size} manifested official source(s).`);

const paragraphs = [...documentXml.matchAll(/<w:p(?:\s[^>]*)?>([\s\S]*?)<\/w:p>/g)].map((match) => {
  const inner = match[1];
  return {
    index: match.index,
    text: textFromXml(inner).trim(),
    style: inner.match(/<w:pStyle[^>]*w:val="([^"]+)"/)?.[1] || "Normal",
    isList: /<w:numPr>/.test(inner),
  };
});
const h1Position = paragraphs.findIndex((paragraph) => paragraph.style === "Heading1");
const sourcesPosition = paragraphs.findIndex((paragraph) => paragraph.style === "Heading2" && paragraph.text === "Sources");
if (h1Position < 0) fail("Styled H1 was not found.");
if (sourcesPosition < 0) fail("Styled Sources H2 was not found.");
const ctaHeadingText = (manifest.content || []).find((block) => block.type === "h2" && block.role === "cta")?.text;
const ctaHeading = paragraphs.find((paragraph) => paragraph.style === "Heading2" && paragraph.text === ctaHeadingText);
const ctaLink = (manifest.link_manifest || []).find((link) => link.supporting_authority === "consultation-cta");
const ctaOccurrence = ctaLink
  ? linkOccurrences.find((occurrence) => occurrence.url === ctaLink.client_url)
  : null;
if (!ctaHeading) fail("The final role=cta H2 from the manifest was not found in the DOCX.");
if (ctaLink && ctaOccurrence && ctaHeading
    && !(ctaOccurrence.index > ctaHeading.index && ctaOccurrence.index < sourcesXmlIndex)) {
  fail(`${ctaLink.id}: consultation CTA must appear after the final role=cta H2 and before Sources.`);
}
const consumerParagraphs = h1Position >= 0 && sourcesPosition > h1Position
  ? paragraphs.slice(h1Position + 1, sourcesPosition)
  : [];
const consumerText = consumerParagraphs.map((paragraph) => paragraph.text).join(" ");
const wordCount = countWords(consumerText);
fact(`${wordCount} consumer-copy words.`);

// Citation markers as visible text (hyperlinked or not) must match the manifest sources.
const normalizeText = (value) => String(value || "").replace(/\s+/g, " ").trim().normalize("NFC");
const expectedSourceIds = (manifest.sources || []).map((source) => Number(source.id));
const consumerMarkerIds = [...consumerText.matchAll(/\[(\d+)\]/g)].map((match) => Number(match[1]));
const firstSeenIds = [];
for (const id of consumerMarkerIds) if (!firstSeenIds.includes(id)) firstSeenIds.push(id);
if (firstSeenIds.join(",") !== expectedSourceIds.join(",")) {
  fail(`Citation markers by first appearance [${firstSeenIds.join(", ")}] do not match manifest source order [${expectedSourceIds.join(", ")}].`);
}
for (const id of new Set(consumerMarkerIds)) {
  const uses = consumerMarkerIds.filter((item) => item === id).length;
  if (uses !== 1) fail(`Citation marker [${id}] appears ${uses} times in consumer copy; each source is cited exactly once.`);
}
const hyperlinkedMarkers = linkOccurrences.filter((item) => !item.inSources && /^\[\d+\]$/.test(item.anchor)).length;
if (hyperlinkedMarkers !== consumerMarkerIds.length) {
  fail(`${consumerMarkerIds.length - hyperlinkedMarkers} citation marker(s) appear as plain text without a hyperlink.`);
}
if (expectedSourceIds.length) {
  const sourceRows = paragraphs.filter((paragraph) => paragraph.index > sourcesXmlIndex && paragraph.text).map((paragraph) => paragraph.text);
  const parsedRows = sourceRows.map((text) => text.match(/^\[(\d+)\]\s*(.*?)\s*\|\s*(\S+)\s*$/));
  if (parsedRows.some((row) => !row)) fail("A Sources row does not follow the [n] label | URL format.");
  const rowIds = parsedRows.filter(Boolean).map((row) => Number(row[1]));
  if (rowIds.join(",") !== expectedSourceIds.join(",")) fail(`Sources rows [${rowIds.join(", ")}] do not match manifest source ids [${expectedSourceIds.join(", ")}].`);
  for (const row of parsedRows.filter(Boolean)) {
    const source = (manifest.sources || []).find((item) => Number(item.id) === Number(row[1]));
    if (!source) continue;
    if (normalizeText(row[2]) !== normalizeText(source.label)) fail(`Sources [${row[1]}] label does not match the manifest label.`);
    if (row[3] !== source.url) fail(`Sources [${row[1]}] URL text does not match the manifest URL.`);
  }
}
if (wordCount < 1100 || wordCount > 1700) fail(`Consumer copy must contain 1,100–1,700 words; found ${wordCount}.`);

const openingParagraphs = consumerParagraphs.filter((paragraph) => paragraph.text).slice(0, 2);
if (openingParagraphs.length !== 2 || openingParagraphs.some((paragraph) => paragraph.style !== "Normal" || paragraph.isList)) {
  fail("The first two elements after H1 must be non-list body paragraphs.");
}
if (openingParagraphs[0] && !/high[- ]conflict/i.test(openingParagraphs[0].text)) {
  fail("The first paragraph does not directly identify the high-conflict situation.");
}

for (const paragraph of consumerParagraphs) {
  if (!paragraph.text || paragraph.style.startsWith("Heading") || paragraph.isList) continue;
  const sentences = sentenceCount(paragraph.text);
  if (sentences > 3) fail(`Paragraph exceeds three sentences (${sentences}): ${paragraph.text.slice(0, 90)}...`);
}

// Join paragraphs with newlines so word-boundary checks (placeholder words) do not see runs fused together.
const fullText = paragraphs.map((paragraph) => paragraph.text).join("\n");
if (fullText.includes("\u2014")) fail("Em dash detected.");
if (/[●▪◦]/.test(fullText)) fail("Unicode bullet character detected in visible content.");
const placeholderHit = findPlaceholder(fullText);
if (placeholderHit) fail(`Unresolved placeholder detected: ${placeholderHit}`);

const meta = manifest.meta || {};
if (/\bdraft\b/i.test(String(meta.title_tag || ""))) fail("Proposed title tag contains Draft.");
for (const phrase of [
  "navigating the complexities",
  "it is important to note",
  "it's important to note",
  "in today's world",
  "delve into",
  "tailored solutions",
]) {
  if (consumerText.toLowerCase().includes(phrase)) fail(`Banned generic phrase detected: ${phrase}.`);
}
for (const term of manifest.quality_contract?.forbidden_terms || []) {
  if (term && [
    meta.title_tag,
    meta.meta_description,
    meta.cms_title,
    meta.social_title,
    meta.social_description,
    meta.h1,
    meta.media_note,
    consumerText,
  ].join(" ").toLowerCase().includes(String(term).toLowerCase())) {
    fail(`Manifested forbidden term detected: ${term}.`);
  }
}

const tagOnPatterns = [
  /\bsee\s+our\b[^.]{0,50}$/i,
  /\blearn\s+more\s+(?:at|about)\b[^.]{0,50}$/i,
  /\bclick\s+here\b[^.]{0,50}$/i,
  /\bfor\s+more(?:\s+on)?,?\s+see\b[^.]{0,50}$/i,
];
for (const occurrence of linkOccurrences.filter((item) => !item.inSources && expectedInternal.has(item.url))) {
  const previous = paragraphs.filter((paragraph) => paragraph.index <= occurrence.index).at(-1);
  const anchorPosition = previous?.text.indexOf(occurrence.anchor) ?? -1;
  const leadIn = anchorPosition >= 0 ? previous.text.slice(0, anchorPosition).slice(-120) : "";
  if (tagOnPatterns.some((pattern) => pattern.test(leadIn))) {
    fail(`Banned tag-on link language precedes ${occurrence.anchor}.`);
  }
  if (/^(?:click here|this page|learn more|here)$/i.test(occurrence.anchor) || /^https?:\/\//i.test(occurrence.anchor)) {
    fail(`Generic or bare-URL anchor detected: ${occurrence.anchor}.`);
  }
}

const sourceHeadingCount = paragraphs.filter((paragraph) => paragraph.style === "Heading2" && paragraph.text === "Sources").length;
if (sourceHeadingCount !== 1) fail(`Sources H2 must appear once; found ${sourceHeadingCount}.`);
const h2s = paragraphs.filter((paragraph) => paragraph.style === "Heading2").map((paragraph) => paragraph.text);
if (h2s.at(-1) !== "Sources") fail("Sources is not the final H2.");

console.log(`FL-M008 page-level validation: ${docxPath}`);
for (const item of findings.facts) console.log(`INFO: ${item}`);
for (const item of findings.warnings) console.log(`WARNING: ${item}`);
for (const item of findings.hard) console.log(`ERROR: ${item}`);
if (findings.hard.length) {
  console.log(`FAIL: ${findings.hard.length} hard finding(s).`);
  process.exit(1);
}
console.log("PASS: FL-M008 page-level checks passed for the tested local contract.");
