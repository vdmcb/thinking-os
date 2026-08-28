# Understand output format

Understand produces a compact default answer and holds a detailed reference analysis for requests that need it.

## Default answer

Plain text with one Markdown section header. Hard ceiling: **600 words**, including the follow-up questions. Use fewer words when the source is simple.

```text
Status: Incomplete. <Only when a material extraction gap exists; name the gap and affected conclusion.>

Stance: <Positive / Negative / Mixed> on <named object>. <One sentence when needed to distinguish material dimensions.>
Q1: <State question in the stakeholder's words>
A: <Source-grounded answer>
Q2: <Decision question in the stakeholder's words>
A: <Source-grounded answer; attribute any recommendation to the source>
Q3: <Resource or first-change question in the stakeholder's words>
A: <Source-grounded answer; state what is not specified>

## Follow-up questions

1. <Most consequential unanswered, source-specific question>
2. <Second>
3. <Third>

Audited: <N> claims checked, 0 unsupported, 0 misquotes.
Held: <source-specific reference analysis, arithmetic, evidence, or page map available for follow-up>. Ask for any of them.
```

Print the audit line only when it is true. Always end with one held line naming specific material already analyzed for this source. Do not add a title, preamble, conclusion, table, first-principles section, or generic summary.

### Stance

The stance is scoped and evidentiary. It may characterize reported performance, evidence, readiness, completeness, or the source's proposal as defined. It does not approve, reject, rank, fund, release, or otherwise make the user's decision.

Good:

- `Mixed on release readiness: positive on the measured pipeline repair, negative on live validation.`
- `Positive on the migration case as presented; implementation cost and schedule are not stated.`

Bad:

- `Positive.`
- `Approve the migration.`
- `This is clearly the right strategy.`

### Q1: state

Ask the question that establishes the current condition: whether the result is good or bad, working or broken, supported or unsupported, ready or incomplete. Answer with the strongest source-grounded evidence and its scope. Include what the source measured and what it did not.

### Q2: decision

Ask what decision the source changes. Use the source's actual decision when one exists. If the source cannot settle the question, say what it supports and what remains unresolved. A source recommendation stays attributed.

### Q3: resources

Ask what begins, stops, changes first, or requires people, money, time, ownership, capacity, deployment, or another commitment. Include the source's caveats. Use `Not stated` for missing cost, timeline, owner, or release status.

### Follow-up questions

The header is exactly **Follow-up questions**. Include exactly three numbered questions.

These are not alternate summaries of Q1-Q3. They identify the next three unknowns a stakeholder should resolve after reading the answers. Order them by how much the response could change interpretation or action.

Silently confirm that each question has:

- **Claim challenged:** the exact source-specific claim, number, conflict, term, or dependency;
- **Source:** a stable locator when available;
- **Pushback:** the missing or inadequate evidence, definition, bridge, or commitment;
- **Why the answer matters:** the interpretation that could change;
- **Answer required:** a concrete, inspectable response.

Publish only the natural-language question. Do not print those field labels.

Apply three tests:

1. **Evidence-first:** ask for the real-world fact that would settle the issue before asking for an audit of inputs.
2. **Responsiveness:** if vague prose could appear responsive, request a more inspectable answer.
3. **Genericity:** remove the source-specific nouns and numbers. If the question still fits most documents, rewrite it.

Questions are one or two sentences, with the locator at the end. A third sentence is allowed only for the fallback: if the evidence does not exist, ask for the owner's plan and deadline to obtain it. Never propose the plan.

## Optional reference analysis

Produce this only when the user asks for the full analysis, evidence ledger, calculations, or detailed gaps. Keep it compact and table-first.

- **The ask:** purpose, requested response, claimed outcome, horizon, explicit decision, implied commitments, and unresolved authorization boundaries.
- **Load-bearing reasoning:** each material claim chain, source-stated mechanism, evidence, required assumptions, unresolved items, value status, and locator.
- **Evidence strength and applicability:** provenance, population, period, sample, exclusions, metric definition, exact proposition supported, and whether external citations were checked.
- **Numbers and internal consistency:** material values with unit, denominator, period, population, scenario, transparent calculations, missing formulas, and unreconciled model bridges.
- **Material unknowns:** ordered by consequence without repeating the default follow-up questions.
- **Other important context:** caveats, dissent, alternatives, and conflicts outside the main claim chain.
- **Extraction limitations:** reading path, coverage, unreadable content, OCR or vision use, locator scheme, and affected conclusions.

## Writing and typography

- One idea per sentence.
- Use plain verbs and concrete actors.
- Use straight quotes.
- Do not use em dashes, en dashes, emoji, decorative symbols, or ASCII diagrams outside quoted source text.
- Do not personify a document.
- Do not repeat the same fact or gap across answers and follow-ups.
- Preserve source shorthand only after introducing it in plain language.

Load [core/writing.md](core/writing.md) before drafting.

## Saved output

When the user asks to save the result, write `<source base name> - Understood.md`. Append the reference analysis only if requested. Never overwrite the source.

## Final compression pass

Before returning:

- confirm the stance has a named scope;
- confirm Q1, Q2, and Q3 serve state, decision, and resource roles;
- remove any sentence that does not change understanding;
- confirm all facts, numbers, and causal directions against the source;
- confirm exactly three follow-up questions remain;
- confirm every follow-up passes the evidence-first, responsiveness, and genericity tests;
- confirm no follow-up repeats an answered question;
- confirm the final held line names source-specific material already analyzed;
- confirm the answer is within 600 words;
- run the core writing check.
