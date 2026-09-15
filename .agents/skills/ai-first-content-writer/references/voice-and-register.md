# Voice and Register

This is the part that took three attempts to get right. Read the autopsy first, because the failure modes are more instructive than the rules.

## The autopsy: why two versions failed

**v1 failed as an encyclopedia.** Formal register, statutory paraphrase, zero contractions, every section opening with a definitional statement. "A long-distance parenting plan in Wisconsin trades frequency for duration." Sharp-sounding agency copy that no human has ever said to another human. It was also undifferentiated: a tight restatement of the primary sources, which gives an AI system nothing it cannot get from the sources directly.

**v2 failed as a casual encyclopedia.** Contractions added, sentences shortened, register still expository. "Wisconsin has two child support formulas. Which one applies turns on whether both parents have at least 92 overnights." Grammatically casual, structurally a lecture. The lesson: conversational is a stance problem, not a word-choice problem. Decorating expository prose with contractions produces a blog that thinks it is a conversation.

**v3 worked because the stance changed.** Same facts, different addressee. "This is the one that costs people money, and it almost always comes up too late. Land at 91 and it's a flat 17 percent. Land at 93 and the court can use the shared formula." That is one side of a conversation with a specific person at a specific moment.

## The stance test

For every sentence, ask: is this ABOUT a topic, or TO a person?

- ABOUT: "Wisconsin sets no travel-cost formula. It requires specificity."
- TO: "There's no formula. That's exactly why it turns into a fight."

- ABOUT: "Form FA-4147V is the proposed parenting plan Wisconsin parents file."
- TO: "When you sit down with Wisconsin's parenting plan form, you'll hit a two-week grid. Don't try to force your schedule into it."

- ABOUT: "Electronic communication may only supplement placement."
- TO: "No, and it's worth being blunt, because people get talked into it."

If a paragraph fails the test, do not lightly edit it. Rewrite it from the reader's position: what are they holding, what are they afraid of, what are they about to do wrong.

## The out-loud test

Read the sentence aloud. If a knowledgeable friend would not say it across a table, it does not go in. This kills formal transitions ("Furthermore," "It is important to note"), nominalizations ("the allocation of transportation costs" becomes "who pays for the flights"), and passive constructions where an actor exists.

## Measured cadence targets

These numbers come from analyzing the final approved calibration article. Treat them as targets with tolerance, not laws.

| Property | Target | Calibration value |
|---|---|---|
| Median sentence length | 9-12 words | 10 |
| Mean sentence length | 11-14 words | 12.4 |
| Sentences under 8 words | 25-35 percent | 32 percent |
| Sentences over 25 words | under 10 percent | 7 percent |
| Deliberate fragments per 1,000 words | 10-16 | 14 |
| Sentences per paragraph | 1-3, mean ~2.4 | 2.4 |
| Words per paragraph | mean ~30, max 60 | 31 mean, 58 max |
| One-sentence paragraphs | ~20-25 percent of paragraphs | 23 percent |
| Contractions | at least 1 per 35 words | 1 per 28 |
| Second-person pronouns | at least 1 per 30 words | 1 per 23 |
| Sentences opening with So/And/But/Then/Because | 10-18 percent | 15 percent |
| Question-formatted headings | 60-70 percent | 68 percent |

## Moves that create the register

**Fragments for emphasis, placed where the reader needs to stop.** "One number: 100 driving miles." "The flights. The overnight count." "Days, not weeks." Use them at section openings and after a heavy fact. More than about one per 70 words starts to read as affect.

**Open mid-conversation.** The first sentence of the article assumes the situation is already happening: "So one of you is moving, or already has." Never open with a definition, a statistic about the industry, or "If you're reading this."

**Stakes before mechanics.** Lead a section with what it costs to get this wrong ("This is the one that costs people money, and it almost always comes up too late"), then the rule.

**Concrete over categorical.** "Halfway between Green Bay and Dallas is a gas station in Missouri" beats "midpoint exchanges may be impractical over long distances." "Punch both addresses into your phone" beats "consult a mapping application." One vivid specific per section, minimum.

**Blunt verdicts on yes/no questions.** "No. And you should hear that clearly, because people get talked into it." Then the rule, then the qualifier. Never open a yes/no answer with background.

**The reader's future arguments.** Name the fight before it happens: "Parents argue about this later far more often than they expect to." "Split evenly becomes an argument every March."

**Direct instruction is allowed.** "Write in an airport." "Add them." "Don't be the parent who moves without doing this properly." The reader came for direction; give it.

## Banned patterns

- Em dashes, en dashes as separators, emojis (global rule).
- AI-tell phrases: "it's important to note", "navigating the complexities", "in today's world", "delve", "landscape of", "when it comes to", "at the end of the day", "rest assured", "look no further", "in conclusion", "robust", "unlock", "game-changer".
- Formal source identifiers inside prose. "Wis. Stat. sec. 767.481(1)(a)" mid-sentence breaks the register; the [N] anchor carries it.
- Rhetorical throat-clearing before answers ("Great question", "Let's break it down", "The short answer is that it depends").
- FAQ answers that restate a body section.
- Perfectly uniform sentence lengths. If every sentence is 12-16 words, the piece reads machine-made regardless of word choice. Vary hard: fragments against occasional 30-word sentences.

## Register vs. brand voice

The client voice skill controls what the brand says (claims, offers, prohibited topics, brand phrases). This register controls how the piece talks. For AI-designated content, this register applies even when the brand's traditional content is formal; the brand shows up in the facts, the guardrails, and the closing paragraphs, not in stiffening the prose. If a brand guardrail genuinely conflicts (e.g., the brand prohibits second person), stop and flag it rather than silently choosing.
