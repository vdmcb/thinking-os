# Understanding Packet format

Understand produces two artifacts with different lives:

1. **The brief**, the default and usually the only output: a short memo a careful colleague might write, ending in the questions that drive understanding. Hard ceiling: **600 words**.
2. **The reference analysis**, the full evidentiary workup behind the brief. **Do not write it unless the user asks** ("show the numbers", "show the full analysis"). The analysis is still performed; it is held, not dumped.

## Word budgets for the brief

Ceilings, not targets. Pick the tier from decision complexity, never from page count: a fifty-page deck making one argument is a simple source.

| Source | Ceiling |
| --- | --- |
| Single claim or short document | 250 words |
| Standard proposal, plan, or study | 400 words |
| Complex, decision-critical, several independent claim chains | 600 words |

If material content cannot fit, cut elaboration and merge overlapping items. Never drop a caveat, and never raise the ceiling silently; when brevity and a material caveat genuinely conflict, keep the caveat and say in one line that the budget was exceeded for it.

## Status line

Only when extraction is materially incomplete, the brief begins:

> **Status: Incomplete.** <scope of the gap, affected claims, interpretive consequence>

Extraction honesty is never deferred to the reference layer.

---

# The brief

Two or three short paragraphs of plain prose, then the questions. No other headings, no diagrams, no tables, no glyphs.

**Paragraph one: what this is and what it asks.** The document, its author when named, the decision or belief it seeks, and the promised outcome with its headline numbers and page references inline.

**Paragraph two (and three when needed): what holds and what stands on assumptions.** This is the critical path from the analysis, expressed as prose. Say plainly which claims stand on their own and which stand on models, examples, or assertions, and what each weak point would change. Page references in parentheses. Rules:

- **Passed checks are silent.** Verification that confirms expectations earns no words. Only a failed check, a check that cannot be run, or an ungrounded input earns a sentence. Never write that the math checked out.
- **The materiality filter.** A weakness earns a sentence only if resolving it could change the reader's understanding. If it does not change the narrative, it is not worth mentioning; it stays in the held reference.
- **No inherited shorthand.** The reader may never open the source. The source's internal vocabulary gets one plain introduction before any use, or gets replaced with a description.
- **No document personification.** A deck does not count, believe, or assume. Write what the document presents, shows, or fails to show.
- Every weak point named here must have a matching question below. The order of the questions mirrors the order of the weak points; that is the mapping. At most, add a parenthetical "(question 2)" where the order alone is ambiguous. Never spend a sentence on the mapping: "Question 1 addresses this" is scaffolding, not information.
- Keep each paragraph under roughly 120 words. When a paragraph stacks a third finding, split it rather than densifying it.

## Questions for the author

The section header is exactly that. **3-5** numbered questions the reader can send unchanged; fewer when the source warrants, never padded. Order by how much the answer moves the interpretation.

Each question is one or two sentences, intent first, with its page reference in parentheses at the end; a third sentence is allowed only when the plan-fallback clause ("if not, what is your plan and by when?") needs one of its own. No labels, no bold, no metadata line. The supporting facts (the claim challenged, the source locator, why the answer matters, the concrete answer required) must all be identifiable inside the sentences themselves; they are authoring requirements, not printed fields. A drafting aid: silently confirm for each question that you could name its Claim challenged, Source, Pushback, Why the answer matters, and Answer required; then publish only the sentences.

Two generation rules, applied in order:

1. **Ask for the evidence, not the audit.** For each weak claim, first ask: what single real-world fact, if it exists, would settle this? A question like "are there customers behind the example already?" settles achievability and grounds the inputs in one ask. Fall back to input-tagging ("which of these numbers are contracted, measured, or assumed?") only when no single evidence object can settle the claim.
2. **Evidence, or the plan to get it.** When a question asks whether evidence exists, it also asks what the author will do, and by when, if it does not. Ask for the author's plan; never propose one.

Every question must: name the exact claim under pressure; carry its locator; request something concrete and inspectable; be understandable on first read by someone who has not read the source; not ask for facts already in the source; not disguise a recommendation. Apply the **genericity deletion test** (strip the source-specific nouns and numbers; if it still fits most documents, rewrite or drop it), the **responsiveness test** (if the author could answer in vague prose and appear responsive, demand a more inspectable object), and the **send test** (readable once, aloud, and explainable to a colleague). An extraction gap is never a question for the author.

If none are needed:

> No material follow-up questions are required to understand and test the source's stated case.

---

# The reference analysis (on request only)

When the user asks, produce any or all of the following, compressed and table-first, using the contract's full epistemic labels. The brief is a surface; the underlying analysis is always done at full precision.

- **The ask:** purpose and response sought; claimed outcome and horizon; the authorization perimeter, the explicit decision separated from implied commitments, unresolved dimensions marked (omit when the source seeks no authorization).
- **Load-bearing reasoning:** per claim chain: claim and role; stated mechanism or `Not explained`; evidence, its provenance, and the narrowest proposition it supports, with the inferential hops named; required assumptions; unresolved items; value status; locator.
- **Evidence strength and applicability:** one row per evidence item: provenance, population, period, sample and exclusions, metric definition, the exact proposition supported, whether external citations were independently checked. Citation presence is never verification.
- **Numbers and internal consistency:** material values with unit, denominator, period, population, scenario; a compact list of the checks performed; whether premises are supported (consistency is not premise validity); for a load-bearing forecast, whether the opening actual state traces through the volume, capacity, unit-value, timing, cost, and formula bridges to each terminal output, naming missing bridge elements without supplying them.
- **Material unknowns:** ordered by consequence, one line each, cross-referencing the brief's questions rather than restating them.
- **Other important context:** caveats, dissent, alternatives that matter but sit off the load-bearing chain.
- **Extraction limitations:** reading path, coverage, unreadable content and the claims depending on it, OCR or vision use, locator scheme, ordering or duplication artifacts. `None material` only after checking.

## Typography

Packets are read by tired humans. Write plain.

- Never em-dashes or en-dashes, including ranges: "3-5". Use a comma, colon, period, or parentheses.
- No emoji, no decorative symbols, no ASCII diagrams.
- Bold and italics only where they carry information the reader needs to find again. Never bold for emphasis alone.
- Prefer short sentences over stacked clauses.

The full writing rules live in [human-voice.md](human-voice.md). Load them before drafting; they are part of the output contract, not advice.

## Optional saved artifact

When the user asks to save, write `<source base name> - Simplified.md` (the brief; append the reference analysis only if they asked for it). Never overwrite the source.

## Before returning: the compression pass

Reread the brief once as the reader, then:

- cut every sentence that does not change what the reader understands or asks;
- confirm paragraph one alone says what the source is, what it wants, and its headline promise;
- confirm every weak point in the prose has a matching question, and no immaterial weakness survived the materiality filter;
- confirm nothing is stated twice, no passed check is narrated, no shorthand is unintroduced;
- scan for the known recurring offenders, which have each survived a draft before: "the book" or any source shorthand in paragraph one, "the deck counts" or any document-as-actor verb, and mapping sentences of the form "question N addresses this";
- recount the words after cutting; a draft that was over budget before the pass usually still is.
- confirm every question passes the genericity, responsiveness, and send tests;
- confirm the brief is within budget and no material caveat, number, conflict, or dissent was lost getting there;
- run the [human-voice.md](human-voice.md) check.
