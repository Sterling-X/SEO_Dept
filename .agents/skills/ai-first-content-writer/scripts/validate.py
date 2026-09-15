#!/usr/bin/env python3
"""Pre-delivery validator for AI-first articles.

Enforces the ai-first-content-writer quality gate. Exits 1 on any hard failure.
"""
import json, re, sys

# Configured per-article from content.json meta
CORE = None
PRIMARY = None

AI_TELLS = [
    "it's important to note", "it is important to note", "in today's world",
    "navigating the complexities", "delve into", "tapestry", "testament to",
    "in conclusion", "it's worth noting", "at the end of the day",
    "when it comes to", "landscape of", "ever-evolving", "robust solution",
    "unlock the", "game-changer", "rest assured", "look no further",
]
TAG_ON = [
    "see our", "learn more at", "click here", "for more on this, see",
    "read more", "check out our", "visit our", "for more information, see",
]
GENERIC_ANCHORS = {"click here", "learn more", "this page", "here", "read more", "more"}

fails, warns = [], []


CITE_FRAGMENT = re.compile(r"^\s*([A-Z][\w.]*\.?\s+){0,4}[\d()./:a-z-]*\.?\s*(\[\d+\])?\s*$")


def sentences(text):
    """Split into real sentences. A trailing statute cite ("Wis. Stat. sec. 767.41(6)(a) [5]")
    is an attribution fragment, not a sentence, so it is not counted."""
    t = re.sub(r"\b(sec|Stat|Wis|approx|No|vs)\.", r"\1<DOT>", text)
    parts = [s.replace("<DOT>", ".") for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]
    return [p for p in parts if not CITE_FRAGMENT.match(p)]


def main():
    data = json.load(open("content.json"))
    global CORE, PRIMARY
    CORE = data["meta"].get("core_url") or ""
    PRIMARY = (data["meta"].get("primary") or "").lower()
    if not CORE or not PRIMARY:
        fails.append("meta.core_url and meta.primary must be set for this article.")
    blocks = data["blocks"]
    sources = data["sources"]

    # Flatten body text and collect structures
    body_text_parts, links, cites = [], [], []
    para_index = 0
    core_para = None
    first_link_url = None

    for b in blocks:
        if b["t"] in ("h1", "h2", "h3"):
            body_text_parts.append(b["text"])
        elif b["t"] in ("ul", "ol"):
            for it in b["items"]:
                if isinstance(it, dict):
                    body_text_parts.append("".join(r["text"] for r in it["runs"]))
                    for r in it["runs"]:
                        if "cite" in r:
                            cites.append(r["cite"])
                        if "link" in r:
                            links.append((r["link"], r["text"], para_index))
                else:
                    body_text_parts.append(it)
        elif b["t"] == "p":
            para_index += 1
            ptxt = "".join(r["text"] for r in b["runs"])
            body_text_parts.append(ptxt)
            for r in b["runs"]:
                if "link" in r:
                    links.append((r["link"], r["text"], para_index))
                    if first_link_url is None:
                        first_link_url = r["link"]
                    if r["link"] == CORE and core_para is None:
                        core_para = para_index
                if "cite" in r:
                    cites.append(r["cite"])
            # paragraph length discipline
            n = len(sentences(ptxt))
            w = len(ptxt.split())
            if n > 3 and w > 70:
                warns.append(f"Paragraph {para_index}: {n} sentences AND {w} words (dense): {ptxt[:70]}...")
            if w > 75:
                warns.append(f"Paragraph {para_index} is {w} words (dense, limit 75): {ptxt[:70]}...")

    full = "\n".join(body_text_parts)

    # 1. Em dashes / en dashes
    for ch, name in [("\u2014", "em dash"), ("\u2013", "en dash")]:
        if ch in full:
            for m in re.finditer(re.escape(ch), full):
                fails.append(f"{name} found: ...{full[max(0,m.start()-40):m.start()+40]}...")

    # 2. Emoji / non-ascii sweep
    allowed = {"\u2019", "\u201c", "\u201d", "\u2018"}
    bad = {c for c in full if ord(c) > 127} - allowed
    if bad:
        fails.append(f"Unexpected non-ASCII characters: {sorted(bad)}")

    # 3. AI tells
    low = full.lower()
    for t in AI_TELLS:
        if t in low:
            fails.append(f"AI tell phrase present: '{t}'")

    # 4. Tag-on link patterns
    for t in TAG_ON:
        if t in low:
            fails.append(f"Tag-on link pattern present: '{t}'")

    # 5. One internal destination, placed once
    urls = [u for u, _, _ in links]
    if len(links) > 1:
        fails.append(f"Found {len(links)} internal links; this format permits one core-page link.")
    dupes = {u for u in urls if urls.count(u) > 1}
    if dupes:
        fails.append(f"Duplicate internal destination URL(s): {dupes}")

    # 6. Generic anchor text + bare URLs
    for u, anchor, _ in links:
        if anchor.strip().lower() in GENERIC_ANCHORS:
            fails.append(f"Generic anchor text: '{anchor}'")
        if anchor.strip().startswith("http"):
            fails.append(f"Bare URL used as anchor: '{anchor}'")

    # 7. Core service page must be first internal link, within first two paragraphs
    if core_para is None:
        fails.append("Core service page link missing.")
    else:
        if core_para > 2:
            fails.append(f"Core service page link in paragraph {core_para}; must be in first two.")
        if first_link_url != CORE:
            fails.append(f"First internal link is {first_link_url}, must be the core service page.")

    # 8. Multi-link clusters in one paragraph
    from collections import Counter
    per_para = Counter(p for _, _, p in links)
    for p, c in per_para.items():
        if c > 1:
            fails.append(f"Paragraph {p} contains {c} internal links (max 1).")

    # 9. Citation parity and sequencing
    src_nums = [s["n"] for s in sources]
    first_seen = []
    for n in cites:
        if n not in first_seen:
            first_seen.append(n)
    if first_seen != list(range(1, len(first_seen) + 1)):
        fails.append(f"Body citations not numbered by order of first appearance: {cites}")
    if src_nums != list(range(1, len(src_nums) + 1)):
        fails.append(f"Sources not sequential from 1: {src_nums}")
    orphan_body = set(cites) - set(src_nums)
    orphan_src = set(src_nums) - set(cites)
    if orphan_body:
        fails.append(f"Body citations with no Sources entry: {sorted(orphan_body)}")
    if orphan_src:
        fails.append(f"Sources entries never cited in body: {sorted(orphan_src)}")

    # 10. Sources completeness
    for s in sources:
        if not s["url"].startswith("https://"):
            fails.append(f"Source [{s['n']}] URL not absolute https: {s['url']}")
        if len(s["id"].strip()) < 8:
            warns.append(f"Source [{s['n']}] identifier looks too thin to be a formal citation: {s['id']}")

    # 11. Primary keyword coverage
    kw_hits = low.count(PRIMARY)
    if kw_hits < 3:
        fails.append(f"Primary keyword '{PRIMARY}' appears {kw_hits} times (need 3+).")
    intro = "".join(
        "".join(r["text"] for r in b["runs"])
        for b in blocks if b["t"] == "p"
    )
    first_two = " ".join(
        "".join(r["text"] for r in b["runs"]) for b in blocks if b["t"] == "p"
    ).lower()
    if PRIMARY not in " ".join(first_two.split()[:120]):
        warns.append("Primary keyword not detected inside first ~120 words.")

    # 12. Heading question-format ratio (AI extractability)
    h2s = [
        b["text"] for b in blocks
        if b["t"] == "h2" and b["text"].strip().lower() != "sources"
    ]
    q = sum(1 for h in h2s if h.strip().endswith("?"))
    if q / max(len(h2s), 1) < 0.4:
        warns.append(f"Only {q}/{len(h2s)} H2s are question-formatted; AI retrieval prefers more.")

    # 13. Word count
    wc = len(full.split())
    if wc < 800:
        warns.append(f"Article is {wc} words; the normal floor is 800 unless the honest answer is unusually thin.")
    if wc > 1650:
        warns.append(f"Article is {wc} words; the normal ceiling is about 1,650 even with mandated prompt coverage.")

    print("=" * 64)
    print(f"Word count (body incl. headings/lists): {wc}")
    print(f"Internal links: {len(links)} | Unique: {len(set(urls))}")
    print(f"Body citations: {len(cites)} | Sources entries: {len(sources)}")
    print(f"H2 headings: {len(h2s)} | Question-formatted: {q}")
    print(f"Primary keyword hits: {kw_hits}")
    print("=" * 64)

    if warns:
        print("\nWARNINGS")
        for w in warns:
            print("  - " + w)
    if fails:
        print("\nFAILURES")
        for f in fails:
            print("  ! " + f)
        print("\nVALIDATOR: FAIL")
        return 1
    print("\nVALIDATOR: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
