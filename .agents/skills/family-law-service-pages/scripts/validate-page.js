#!/usr/bin/env node
/**
 * validate-page.js
 *
 * Pre-delivery scanner for family-law service pages produced as DOCX.
 * Enforces the hard rules in:
 *   - family-law-service-pages/SKILL.md (Internal Linking Rules)
 *   - family-law-red-team-qa-reviewer/SKILL.md (Failure modes)
 *   - Johnson Law Group production conventions (em-dash ban, banned AI-tells, North Star limit)
 *
 * Usage:
 *   node validate-page.js <path-to-docx>
 *
 * Exits 0 if all hard rules pass. Exits 1 with a written report if any fail.
 *
 * Requires: npm i adm-zip
 */

const fs = require('fs');
const path = require('path');
const AdmZip = require('adm-zip');

const docxPath = process.argv[2];
if (!docxPath) {
  console.error('Usage: node validate-page.js <path-to-docx>');
  process.exit(2);
}

// ---------- Load document XML ----------
const zip = new AdmZip(docxPath);
const documentXml = zip.readAsText('word/document.xml');
const relsXml = zip.readAsText('word/_rels/document.xml.rels');

if (!documentXml) {
  console.error('Could not read word/document.xml from', docxPath);
  process.exit(2);
}

// ---------- Extract plain text from document.xml ----------
// Joins all <w:t> runs in document order. Good enough for phrase scanning.
const textRuns = [...documentXml.matchAll(/<w:t[^>]*>([^<]*)<\/w:t>/g)].map(m => m[1]);
const fullText = textRuns.join('');

// ---------- Extract hyperlinks ----------
// Hyperlinks live in two forms:
//   1. <w:hyperlink r:id="rId7"> ... </w:hyperlink> referencing word/_rels/document.xml.rels
//   2. <w:hyperlink w:anchor="..."> internal anchors (we ignore these for URL-uniqueness)
const relsMap = {};
if (relsXml) {
  // Match every <Relationship .../> tag, then check it's a hyperlink and pull Id + Target.
  // Attribute order is not guaranteed, so we extract attrs individually.
  for (const m of relsXml.matchAll(/<Relationship\s+([^>]+?)\/>/g)) {
    const attrs = m[1];
    if (!/Type="[^"]*hyperlink"/i.test(attrs)) continue;
    const idMatch = attrs.match(/\bId="([^"]+)"/);
    const targetMatch = attrs.match(/\bTarget="([^"]+)"/);
    if (idMatch && targetMatch) {
      relsMap[idMatch[1]] = targetMatch[1];
    }
  }
}

// Pull each external hyperlink occurrence in document order.
// We need the (anchor text, URL) pair for each occurrence so we can detect duplicates AND
// count how many distinct anchor strings point to the same URL.
const hyperlinkBlocks = [...documentXml.matchAll(/<w:hyperlink\s+([^>]*?)>([\s\S]*?)<\/w:hyperlink>/g)];
const linkOccurrences = [];
for (const block of hyperlinkBlocks) {
  const attrs = block[1];
  const inner = block[2];
  const ridMatch = attrs.match(/r:id="([^"]+)"/);
  if (!ridMatch) continue; // internal anchor, not external link
  const rid = ridMatch[1];
  const anchor = [...inner.matchAll(/<w:t[^>]*>([^<]*)<\/w:t>/g)].map(m => m[1]).join('');
  const target = relsMap[rid];
  if (!target) continue;
  linkOccurrences.push({ anchor: anchor.trim(), url: target });
}

// ---------- Findings collector ----------
const findings = { hardFail: [], softWarn: [], info: [] };
const fail = (msg) => findings.hardFail.push(msg);
const warn = (msg) => findings.softWarn.push(msg);
const info = (msg) => findings.info.push(msg);

// ---------- Locate Sources section in the document XML ----------
// Used to scope the Single-Placement Rule (statute body+Sources pairs are expected).
let sourcesXmlIdx = -1;
for (const m of documentXml.matchAll(/<w:t[^>]*>([^<]*)<\/w:t>/g)) {
  if (/^Sources\s*$/i.test(m[1])) {
    sourcesXmlIdx = m.index;
    break;
  }
}

// Tag each link occurrence with its location (body vs. sources)
const taggedOccurrences = [];
for (const block of hyperlinkBlocks) {
  const attrs = block[1];
  const inner = block[2];
  const ridMatch = attrs.match(/r:id="([^"]+)"/);
  if (!ridMatch) continue;
  const target = relsMap[ridMatch[1]];
  if (!target) continue;
  const anchor = [...inner.matchAll(/<w:t[^>]*>([^<]*)<\/w:t>/g)].map(m => m[1]).join('').trim();
  const inSources = sourcesXmlIdx >= 0 && block.index >= sourcesXmlIdx;
  taggedOccurrences.push({ anchor, url: target, inSources });
}

// ============================================================
// HARD RULE 1: Single-Placement Rule (internal links only)
// External statute citations are expected in body AND Sources; that pair is exempt.
// ============================================================
const bodyOnlyCounts = {};
for (const { url, inSources } of taggedOccurrences) {
  if (inSources) continue;
  bodyOnlyCounts[url] = (bodyOnlyCounts[url] || 0) + 1;
}
const duplicateUrls = Object.entries(bodyOnlyCounts).filter(([, n]) => n > 1);
if (duplicateUrls.length > 0) {
  fail(`Single-Placement Rule violated. ${duplicateUrls.length} URL${duplicateUrls.length > 1 ? 's' : ''} linked more than once in body content:`);
  for (const [url, n] of duplicateUrls) {
    fail(`  - ${url}  (linked ${n}x in body)`);
  }
}

// ============================================================
// HARD RULE 2: Banned Linking Patterns
// "See our X" / "Learn more at" / "Click here" / "see [Firm]" / "see our [topic] page"
// ============================================================
// Look for tag-on patterns appearing within ~80 chars BEFORE a hyperlink anchor.
// We scan the source XML between hyperlinks, looking at the trailing text of the
// preceding paragraph for tag-on phrases.
const tagOnPatterns = [
  /\bsee\s+our\b[^.]{0,40}$/i,
  /\bsee\s+(?:our\s+)?(?:page|pages)\s+on\b[^.]{0,40}$/i,
  /\blearn\s+more\s+(?:at|about)\b[^.]{0,40}$/i,
  /\bclick\s+here\b[^.]{0,40}$/i,
  /\bfor\s+more(?:\s+on)?,?\s+see\b[^.]{0,40}$/i,
  /\bfor\s+deeper\s+guidance[^.]{0,80}$/i
];

// Walk hyperlink blocks; capture up to 120 chars of plain text immediately before each <w:hyperlink>
const linkPositions = [...documentXml.matchAll(/<w:hyperlink\s+[^>]*r:id="[^"]+"[^>]*>/g)];
// If the strict pattern matched none (e.g., r:id mid-attribute-list), fall back to permissive.
const linkPositionsFallback = linkPositions.length > 0
  ? linkPositions
  : [...documentXml.matchAll(/<w:hyperlink\s+[^>]*>/g)].filter(m => /r:id="/.test(m[0]));
for (const m of linkPositionsFallback) {
  const idx = m.index;
  const slice = documentXml.slice(Math.max(0, idx - 600), idx);
  const sliceText = [...slice.matchAll(/<w:t[^>]*>([^<]*)<\/w:t>/g)].map(x => x[1]).join('');
  const tail = sliceText.slice(-120);
  for (const pat of tagOnPatterns) {
    if (pat.test(tail)) {
      fail(`Banned linking pattern detected. Lead-in fails ("${tail.trim().slice(-80)}…"). Rewrite so the link is integrated into the sentence's noun phrase, not tagged on.`);
      break;
    }
  }
}

// Anchor text quality: bare URL or generic phrases (body content only)
const genericAnchors = ['click here', 'this page', 'learn more', 'here'];
for (const { anchor, url, inSources } of taggedOccurrences) {
  if (inSources) continue; // Sources entries may use URL-as-anchor by convention
  const a = anchor.toLowerCase().trim();
  if (genericAnchors.includes(a)) {
    fail(`Generic anchor text "${anchor}" → ${url}. Rewrite anchor to describe the linked topic.`);
  }
  if (/^https?:\/\//i.test(anchor)) {
    fail(`Bare URL used as anchor text in body: "${anchor}". Rewrite anchor to describe the linked topic.`);
  }
}

// ============================================================
// HARD RULE 3: Multi-link clusters in body
// Two or more hyperlinks within 200 chars of each other (excluding Sources / Related Topics modules).
// ============================================================
// Naive pass: look for hyperlink blocks separated by < 800 chars of XML AND no "Related" or "Sources" heading between them.
for (let i = 1; i < linkPositionsFallback.length; i++) {
  const prev = linkPositionsFallback[i - 1].index;
  const cur = linkPositionsFallback[i].index;
  const between = documentXml.slice(prev, cur);
  const hasModuleBoundary = /Related\s+(?:Family\s+Law\s+)?Topics|Related\s+Legal\s+Issues|Sources\b/i.test(between);
  if (cur - prev < 600 && !hasModuleBoundary) {
    // Check whether this cluster is in the Related Topics / Sources tail of the doc.
    const docTail = documentXml.slice(0, cur);
    const inAllowedModule = /Related\s+(?:Family\s+Law\s+)?Topics|Related\s+Legal\s+Issues|Sources\b/i.test(docTail.slice(-3000));
    if (!inAllowedModule) {
      warn(`Possible multi-link cluster: two hyperlinks within ${cur - prev} chars in body content. Confirm placement is intentional and that prose leads into each link.`);
    }
  }
}

// ============================================================
// HARD RULE 4: Em-dash ban
// ============================================================
const emDashCount = (fullText.match(/\u2014/g) || []).length;
if (emDashCount > 0) {
  fail(`Em dashes (\u2014) banned. Found ${emDashCount}. Replace with periods, commas, colons, parentheses, or restructured sentences.`);
}
const enDashInBody = (fullText.match(/\u2013/g) || []).length;
if (enDashInBody > 0) {
  warn(`En dashes (\u2013) found ${enDashInBody}. Acceptable in numeric ranges (e.g., 5–10 days), but check no en-dashes are used as em-dash substitutes.`);
}

// ============================================================
// HARD RULE 5: Banned AI-tell phrases
// ============================================================
const bannedPhrases = [
  { re: /\bnavigat(?:e|ing|es|ed)\b/i, label: 'navigate / navigating (as metaphor)' },
  { re: /\bdelve\s+into\b/i, label: 'delve into' },
  { re: /\bdive\s+deep\b/i, label: 'dive deep' },
  { re: /\bunpack(?:s|ing|ed)?\b/i, label: 'unpack (as verb)' },
  { re: /\bleverag(?:e|es|ing|ed)\b/i, label: 'leverage (as verb)' },
  { re: /\bin\s+today'?s\s+\w+\s+world\b/i, label: "in today's [X] world" },
  { re: /\bit'?s\s+not\s+just\s+\w+,?\s+it'?s\b/i, label: "It's not just X, it's Y" },
  { re: /\bit\s+is\s+not\s+just\s+\w+,?\s+it\s+is\b/i, label: "It is not just X, it is Y" }
];
for (const { re, label } of bannedPhrases) {
  if (re.test(fullText)) {
    fail(`Banned AI-tell phrase detected: "${label}". Rewrite.`);
  }
}

// ============================================================
// HARD RULE 6: "North Star" usage limit (Johnson Law Group convention)
// Single use, in firm description section. Script enforces the count only.
// ============================================================
const northStarCount = (fullText.match(/\bNorth Star\b/g) || []).length;
if (northStarCount > 1) {
  fail(`"North Star" used ${northStarCount} times. JLG convention: single use, in firm description section only.`);
} else if (northStarCount === 0) {
  info(`"North Star" not used. Acceptable for non-JLG firms or for procedural pages where the brand anchor is not required. If this is a JLG hub page, consider one mention in the firm section.`);
} else {
  info(`"North Star" usage: 1 (compliant).`);
}

// ============================================================
// HARD RULE 7: Citations referenced in body must match Sources entries
// ============================================================
const bodyCites = new Set([...fullText.matchAll(/\[(\d+)\]/g)].map(m => m[1]));
// crude detection: does the document have a Sources heading and entries [N]?
const sourcesIdx = fullText.search(/\bSources\b/);
let sourcesSection = '';
if (sourcesIdx >= 0) sourcesSection = fullText.slice(sourcesIdx);
const sourcesEntries = new Set([...sourcesSection.matchAll(/\[(\d+)\]/g)].map(m => m[1]));

// Body cites that aren't in sources, and sources entries that aren't cited in body
const bodyOnlyCites = new Set([...fullText.slice(0, sourcesIdx >= 0 ? sourcesIdx : fullText.length).matchAll(/\[(\d+)\]/g)].map(m => m[1]));
const orphanInBody = [...bodyOnlyCites].filter(n => !sourcesEntries.has(n));
const orphanInSources = [...sourcesEntries].filter(n => !bodyOnlyCites.has(n));
if (orphanInBody.length > 0) {
  fail(`Citation(s) referenced in body but missing from Sources: [${orphanInBody.join('], [')}]`);
}
if (orphanInSources.length > 0) {
  fail(`Citation(s) listed in Sources but never referenced in body: [${orphanInSources.join('], [')}]`);
}

// ============================================================
// Reporting
// ============================================================
console.log(`\n=== Pre-delivery validation: ${path.basename(docxPath)} ===\n`);

const bodyLinkCount = taggedOccurrences.filter(t => !t.inSources).length;
const sourcesLinkCount = taggedOccurrences.filter(t => t.inSources).length;
const uniqueBodyDests = new Set(taggedOccurrences.filter(t => !t.inSources).map(t => t.url)).size;
console.log(`Link inventory: ${taggedOccurrences.length} total (${bodyLinkCount} in body, ${sourcesLinkCount} in Sources). ${uniqueBodyDests} unique body destination${uniqueBodyDests === 1 ? '' : 's'}.`);
console.log(`Em dashes: ${emDashCount} | En dashes: ${enDashInBody}`);
console.log(`North Star count: ${northStarCount}`);
console.log(`Body cites: [${[...bodyOnlyCites].sort().join(', ')}]  Sources entries: [${[...sourcesEntries].sort().join(', ')}]`);
console.log(`Word count (body text): ${fullText.split(/\s+/).filter(Boolean).length}`);
console.log('');

if (findings.hardFail.length === 0 && findings.softWarn.length === 0) {
  console.log('PASS: All hard rules cleared. No warnings.');
  process.exit(0);
}

if (findings.hardFail.length > 0) {
  console.log(`HARD FAIL (${findings.hardFail.length}):`);
  for (const f of findings.hardFail) console.log('  ✗ ' + f);
  console.log('');
}

if (findings.softWarn.length > 0) {
  console.log(`WARNINGS (${findings.softWarn.length}):`);
  for (const w of findings.softWarn) console.log('  ⚠ ' + w);
  console.log('');
}

if (findings.info.length > 0) {
  console.log('INFO:');
  for (const i of findings.info) console.log('  • ' + i);
  console.log('');
}

process.exit(findings.hardFail.length > 0 ? 1 : 0);
