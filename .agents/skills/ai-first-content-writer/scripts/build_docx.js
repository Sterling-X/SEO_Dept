const fs = require('fs');
function loadDocx() {
  try {
    return require('docx');
  } catch (error) {
    const runtimeModules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
    if (runtimeModules) {
      return require(require.resolve('docx', { paths: [runtimeModules] }));
    }
    throw new Error('The docx package is required. Set CODEX_PRIMARY_RUNTIME_NODE_MODULES or install docx.');
  }
}

const {
  Document, Packer, Paragraph, TextRun, ExternalHyperlink,
  HeadingLevel, AlignmentType, BorderStyle, LevelFormat, convertInchesToTwip
} = loadDocx();

const data = JSON.parse(fs.readFileSync('content.json', 'utf8'));
const brand = (data.meta && data.meta.brand) || {};
const NAVY = brand.heading || '1F2937', BLUE = brand.accent || '374151',
      GRAY = '767676', LINK = brand.link || '1155CC';
const srcMap = Object.fromEntries(data.sources.map(s => [s.n, s.url]));

const metaLine = (label, value) => new Paragraph({
  spacing: { after: 40 },
  children: [
    new TextRun({ text: `${label}: `, bold: true, size: 15, color: GRAY, font: 'Arial' }),
    new TextRun({ text: value, size: 15, color: GRAY, font: 'Arial' })
  ]
});

const divider = () => new Paragraph({
  spacing: { before: 140, after: 260 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'CCCCCC', space: 1 } },
  children: [new TextRun({ text: '', size: 2 })]
});

// Convert a run spec into docx children (plain text, internal link, or citation link)
function renderRuns(runs) {
  const out = [];
  for (const r of runs) {
    if (r.link) {
      out.push(new ExternalHyperlink({
        link: r.link,
        children: [new TextRun({
          text: r.text, font: 'Arial', size: 22,
          color: LINK, underline: { type: 'single', color: LINK }
        })]
      }));
    } else if (r.cite) {
      out.push(new ExternalHyperlink({
        link: srcMap[r.cite],
        children: [new TextRun({
          text: r.text, font: 'Arial', size: 22, superScript: true,
          color: LINK, underline: { type: 'single', color: LINK }
        })]
      }));
    } else {
      out.push(new TextRun({ text: r.text, font: 'Arial', size: 22 }));
    }
  }
  return out;
}

const children = [];

// ---------- Meta block ----------
children.push(new Paragraph({
  spacing: { after: 100 },
  children: [new TextRun({
    text: 'CONTENT BRIEF / PUBLISHER NOTES', bold: true, size: 16,
    color: GRAY, font: 'Arial', characterSpacing: 20
  })]
}));
const m = data.meta;
const metaKeys = [
  ['Queue','queue'], ['Title / H1','title'], ['Target URL','url'],
  ['Primary keyword','primary'], ['Related keywords','related'], ['Intent','intent'],
  ['Core service page','core'], ['Internal links','links'], ['Schema','schema'],
  ['Differentiation','differentiation'], ['Citation style','citation_note'],
  ['Publisher','publisher']
];
for (const [label, key] of metaKeys) {
  if (m[key] && String(m[key]).trim()) children.push(metaLine(label, m[key]));
}
children.push(divider());

// ---------- Body ----------
for (const b of data.blocks) {
  if (b.t === 'h1') {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 60, after: 220 },
      children: [new TextRun({ text: b.text, bold: true, size: 40, color: NAVY, font: 'Arial' })]
    }));
  } else if (b.t === 'h2') {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_2,
      spacing: { before: 320, after: 140 },
      children: [new TextRun({ text: b.text, bold: true, size: 28, color: NAVY, font: 'Arial' })]
    }));
  } else if (b.t === 'h3') {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_3,
      spacing: { before: 220, after: 100 },
      children: [new TextRun({ text: b.text, bold: true, size: 24, color: BLUE, font: 'Arial' })]
    }));
  } else if (b.t === 'p') {
    children.push(new Paragraph({
      spacing: { after: 180, line: 300 },
      children: renderRuns(b.runs)
    }));
  } else if (b.t === 'ul' || b.t === 'ol') {
    b.items.forEach(it => {
      const kids = (typeof it === 'string')
        ? [new TextRun({ text: it, font: 'Arial', size: 22 })]
        : renderRuns(it.runs);
      children.push(new Paragraph({
        numbering: { reference: b.t === 'ul' ? 'bullets' : 'numbers', level: 0 },
        spacing: { after: 90, line: 290 },
        children: kids
      }));
    });
  }
}

// ---------- Sources ----------
data.sources.forEach(s => {
  children.push(new Paragraph({
    spacing: { after: 90, line: 290 },
    indent: { left: convertInchesToTwip(0.3), hanging: convertInchesToTwip(0.3) },
    children: [
      new TextRun({ text: `[${s.n}] `, bold: true, font: 'Arial', size: 21 }),
      new TextRun({ text: `${s.id} | `, font: 'Arial', size: 21 }),
      new ExternalHyperlink({
        link: s.url,
        children: [new TextRun({
          text: s.url, font: 'Arial', size: 21,
          color: LINK, underline: { type: 'single', color: LINK }
        })]
      })
    ]
  }));
});
children.push(new Paragraph({
  spacing: { before: 160 },
  children: [new TextRun({
    text: '[Publisher: use standard editorial links for trusted primary sources; add rel="nofollow" only where independently warranted]',
    italics: true, size: 17, color: GRAY, font: 'Arial'
  })]
}));

const doc = new Document({
  numbering: {
    config: [
      {
        reference: 'bullets',
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: '\u2022',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.22) } } }
        }]
      },
      {
        reference: 'numbers',
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: '%1.',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.22) } } }
        }]
      }
    ]
  },
  styles: { default: { document: { run: { font: 'Arial', size: 22 } } } },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: {
          top: convertInchesToTwip(0.9), bottom: convertInchesToTwip(0.9),
          left: convertInchesToTwip(0.95), right: convertInchesToTwip(0.95)
        }
      }
    },
    children
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync((data.meta.outfile || 'article.docx'), buf);
  console.log('DOCX written');
});
