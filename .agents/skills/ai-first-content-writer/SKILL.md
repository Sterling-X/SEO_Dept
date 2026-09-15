---
name: ai-first-content-writer
description: >-
  Produce short, conversational, citation-ready articles built for AI search
  visibility (AI Overviews, ChatGPT, Perplexity, and answer engines) in any
  vertical, not just legal. Use whenever content is designated as AI-first or
  written for AI to cite. Trigger on AI blog, AI article, AI content, AI-first,
  write this for AI, AI queue, GEO, AEO, answer engine, LLM optimization,
  working from an AI content production queue or sheet, or any request for
  content more conversational and much shorter than a traditional blog in an
  AI search context. Produce prompt-mirroring, second-person, answer-first
  articles with live-verified sourcing, worked numeric examples, and footnote
  citations, delivered as DOCX with a publisher brief block. Load the client
  voice skill first when one exists. Do not use for traditional long-form SEO
  blogs, service pages, or content with no AI-search mandate.
---

# AI-First Content Writer

Produce articles a retrieval system would pull an answer from and a person would recognize as someone talking to them. Both at once. This skill encodes a register, a research method, a structure, and a QA gate that were developed through iterative correction; follow them in order.

**Prerequisite:** If the client has a voice skill (e.g., a `*-voice` brand blueprint), load it BEFORE writing. This skill governs format and register; the voice skill governs brand facts, guardrails, offers, and phrasing the brand would or would not use. Where they conflict on register, this skill wins for AI-designated content, but never violate a brand guardrail (pricing rules, claims rules, prohibited topics).

## Non-negotiables (apply to every output)

1. No em dashes anywhere. No en dashes as separators. No emojis.
2. Second person throughout. The article talks TO one reader in a specific situation, never ABOUT a topic.
3. Every factual claim verified against a live primary source during the session. Nothing from memory. No source, no claim.
4. Footnote citations: bare [N] superscript anchors in body prose and full source identifiers only in a Sources block at the end. Use standard editorial links for trusted primary sources. Reserve `rel="nofollow"` for sources the publisher does not endorse or other cases where nofollow is independently warranted. Do not recite formal source identifiers (statute numbers, spec codes, document IDs) inside sentences; they break the register and pollute the retrieval chunk. Plain-language references ("the state's parenting plan form", "the child support code") are fine in prose.
5. One internal destination URL per page maximum (single placement). Core/parent page linked within the first two paragraphs, as the first link. Descriptive anchors only, no tag-on constructions ("learn more at", "see our", "click here").
6. Deliver as DOCX with the publisher brief block (spec below), then render to images and visually inspect every page before presenting. A passing validator is not a substitute for looking at the output.

## Workflow

1. **Parse the brief.** Pull title, primary keyword, audience, intent, internal link targets, schema, and any prompt/query data from the queue row or brief. If the brief references prompt counts or query data that is not actually present (a rollup number, an empty column), say so explicitly and build a proxy prompt set instead of silently inventing coverage. Never treat a bucket-level metric as article-level evidence.
2. **Load the voice skill** if one exists for the client.
3. **Research for differentiation** using `references/research-protocol.md`. This is where the article is won or lost. Do not start writing until you hold at least two of the four differentiation assets (document friction, cross-domain authority, staleness arbitrage, worked arithmetic).
4. **Build the prompt set.** If real prompt/query data exists, use it verbatim. If not, build a proxy from forum Q&A (Justia/Avvo-style sites, Reddit, Quora), People Also Ask, autocomplete, and competitor FAQ blocks. Real phrasing beats invented phrasing; the words people use become your headings.
5. **Draft in the register** defined in `references/voice-and-register.md`, in the structure defined below, as a structured content file (see `references/content-schema.md`) so the validator and builder read one source of truth.
6. **Run the quality gate.** If citations were added, removed, or moved, run `scripts/renumber_citations.py` first. Then run `scripts/validate.py`, fix all failures, and judge warnings honestly. Run the accuracy pass afterward: re-check every number, every absolute claim (hunt for carve-outs on every "always/never/only/must"), and every multi-part standard against the source text. Flattening a multi-part rule into one clause is the most common substantive error and the validator cannot catch it.
7. **Build the DOCX, render to images, inspect every page.** The render catches what the validator cannot: broken phrasing from edits, duplicated words, empty fields, flattened standards you will only notice when reading as a reader.
8. **Deliver** with a summary that flags any deviations, any errors found in the client's existing pages during research (these are common and valuable; report them, do not silently work around them), and what would strengthen the piece that you could not verify.

## Structure

**Opening (2-3 short paragraphs).** Start in the middle of the reader's situation, not at the top of a topic. First sentence acknowledges where they are ("So one of you is moving, or already has."). Second paragraph delivers the core answer in plain terms and carries the primary keyword naturally. The core internal link lands here. Third paragraph, optional, names the traps the article will cover.

**Body sections (5-8 H2s).** Each H2 is one strong idea. Allocate ruthlessly:
- Strong, differentiated material (a worked example, a document trap, a misconception correction) gets an H2.
- Thin material gets a FAQ entry, never a padded section. Weak chunks from the same URL compete against strong ones in retrieval and drag the whole page down.
- Every section opens with a complete, self-contained answer that would survive extraction alone: the entity (state, product, jurisdiction, brand) and the term of art appear inside the chunk, not just in the heading above it.
- 60-70 percent of H2s phrased as the reader's own question, in their words ("Who's paying for the flights?"), the rest as direct statements ("The form is going to fight you"). Do not force every heading into question format.

**FAQ block ("Questions people actually ask" or similar).** This is the prompt-coverage surface. One H3 per prompt, phrased as close to the observed prompt as possible, including first-person phrasing ("I have sole custody. Can I just move?"). Answers are 2-3 sentences: direct answer first, then the one qualifier that matters. Honestly thin answers stay thin. Do not restate body sections here; a FAQ that repeats a section creates duplicate chunks that compete with each other.

**Close (2-3 paragraphs).** One paragraph of consequence ("every vague line becomes a phone call you'll make from three states away"), one brand paragraph per the voice skill, one CTA line.

**Sources.** Numbered list covering every body citation, in order of first appearance, with full identifiers and absolute URLs. Reuse the same number when the same source supports another claim. Add a publisher link-rel note that preserves standard editorial links for trusted sources and reserves nofollow for independently warranted cases.

## Coverage rule

When the user mandates prompt coverage ("cover it so AI picks up the intent"), cover every prompt in the set, but coverage does not mean a section. The allocation above is how you cover without dilution. If a prompt exists and the honest answer is thin, the FAQ entry mirrors the prompt and gives the short true answer. Never pad a thin answer to justify a section, and never invent demand: if you added a section no prompt asks for, know why (usually because the differentiated finding was too strong to cut) and be ready to defend it.

## Length

Target 800-1,400 words without a coverage mandate; up to ~1,650 with one. Short means no filler, never fewer facts. When cutting, cut generic advice first (it exists on ten thousand other pages), differentiated material last. The worked example is the most citable asset on the page; it is the last thing that goes.

## Citation and differentiation logic

A model deciding what to cite skips restatements of the governing source. If a passage could be paraphrased straight from the statute, spec, or official doc, it earns nothing. What earns citations: facts not in the primary source (form quirks, practical consequences), concrete numbers from worked arithmetic, corrections of misconceptions the rest of the corpus repeats, and current facts where the corpus is stale. Note also that transparently self-serving topics ("how to choose a [vendor type]") will not be cited by AI systems regardless of quality; flag this when a queue ranks such topics highly on commercial proximity.

The strongest conversion content demonstrates complexity rather than resolving it: a worked example that makes the reader realize their own numbers need running is worth more than a complete answer that ends the conversation.

## QA gates, in order

1. `scripts/validate.py` clean pass (structure, register tells, link discipline, citation parity, density).
2. Accuracy pass: every claim against source text, absolutes hunted for carve-outs, multi-part standards checked part by part.
3. Render and read every page as a reader. Fix what you find, re-render, re-inspect.
4. Report defects found in the client's existing content during research as a separate deliverable or flagged list; never silently contradict or silently conform to a client page that is wrong.

## Publisher brief block (top of DOCX)

Queue reference, Title/H1, Target URL, Primary keyword, Related keywords, Intent + audience, Core service page, Internal links with URLs, Schema (BlogPosting + FAQPage for this format), Differentiation summary (the two-to-four assets and why they earn citations), Citation style note, and publisher link-rel instruction. Note in delivery that the DOCX is a content handoff: the H2/H3 hierarchy and FAQ block must survive into the published HTML with FAQPage markup, and offer the HTML if the pipeline can take it.

## References

- `references/voice-and-register.md`: the register, measured cadence targets from the calibration article, the stance test, before/after pairs, and the failure autopsy. Read before first draft in a session.
- `references/research-protocol.md`: the four differentiation moves, live verification rules, staleness screening, and the client-content defect protocol.
- `references/content-schema.md`: the structured content file format that `scripts/validate.py`, `scripts/renumber_citations.py`, and `scripts/build_docx.js` consume.
