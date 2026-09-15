# Content Schema

All drafting happens in a single `content.json`. The validator, the citation renumberer, and the DOCX builder all read this one file, so the thing that gets QA'd is the thing that ships. Never hand-edit the DOCX.

```json
{
  "meta": {
    "queue": "Row ref | phase | any queue metadata",
    "title": "Article H1",
    "url": "https://client.com/target-slug/",
    "primary": "primary keyword phrase",
    "related": "comma-separated related keywords",
    "intent": "Stage | Audience | Format",
    "core": "Core page label | https://client.com/core-page/",
    "core_url": "https://client.com/core-page/",
    "links": "Label | URL -- Label | URL -- Label | URL",
    "schema": "BlogPosting + FAQPage",
    "differentiation": "The 2-4 assets and why they earn citations",
    "citation_note": "Style notes and any flagged deviations",
    "publisher": "[Publisher: use standard editorial links for trusted primary sources; add rel=\"nofollow\" only where independently warranted]",
    "brand": { "heading": "1B3A5C", "accent": "2E75B6", "link": "1155CC" }
  },
  "blocks": [
    { "t": "h1", "text": "..." },
    { "t": "h2", "text": "..." },
    { "t": "h3", "text": "..." },
    { "t": "p", "runs": [
        { "text": "plain text " },
        { "text": "anchor text", "link": "https://internal-target/" },
        { "text": "[1]", "cite": 1 }
    ]},
    { "t": "ul", "items": [
        "plain string item",
        { "runs": [ { "text": "rich item with a citation " }, { "text": "[2]", "cite": 2 } ] }
    ]},
    { "t": "ol", "items": [ "..." ] }
  ],
  "sources": [
    { "n": 1, "id": "Full formal identifier", "url": "https://absolute-source-url" }
  ]
}
```

Rules the tooling enforces or assumes:

- `meta.core_url` and `meta.primary` drive the validator's link-position and keyword checks. Set them; do not leave the calibration client's values.
- `meta.brand` colors are optional; the builder falls back to neutral defaults.
- Citation runs carry both the display text `[N]` and the machine field `cite: N`. After any insertion or reordering, run `scripts/renumber_citations.py` so numbering matches order of first appearance and Sources reorders to match.
- Every `cite` must resolve to a Sources entry and every Sources entry must be cited at least once. Reusing the same source number is allowed. Orphans in either direction are validator failures.
- The final block before Sources content is `{ "t": "h2", "text": "Sources" }`; the builder appends the sources list after it.
- Blocks map to published HTML one-to-one: h2/h3 hierarchy and the FAQ h3 block must survive into the CMS with FAQPage markup. The DOCX is a handoff format, not the artifact being optimized; offer HTML when the pipeline accepts it.

## Pipeline

```
draft content.json
python3 scripts/renumber_citations.py  # if citations were added, removed, or moved
python3 scripts/validate.py            # structure + register gate
node scripts/build_docx.js             # writes the DOCX
# render to PDF, rasterize, view every page, fix, repeat
```
