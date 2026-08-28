# Audit prompt

Give this prompt to an independent agent together with the complete source and the draft output. The agent must not have written the draft. If no agent is available, run the same prompt yourself as a distinct pass after rereading the source in full.

Fill `SOURCE` with the file path or the full extracted text and `DRAFT` with the complete draft, including the stance line, the three answers, and the three follow-up questions.

```text
You are an adversarial fact-checker. SOURCE is ground truth: <path or text>. DRAFT is the text under audit: <draft>.

Read the whole SOURCE before you start. Then, for every number, quoted phrase, comparative, and factual statement in the DRAFT, classify it as one of:

SUPPORTED: verbatim in the source, or an exact arithmetic restatement of visible source figures.
UNSUPPORTED: absent from the source, or contradicting it.
STRETCH: an inference the source does not state; a dropped qualifier such as about, roughly, partly, only, directly, in practice, typical; or a dropped scope word such as which environment, population, model, batch, condition, or period the figure applies to.
MISQUOTE: quotation marks around words that are not verbatim. Collapse whitespace and HTML entities before matching; anything else counts as a misquote.

Then run these checks separately:

DIRECTION: for every figure that sits next to a verb (closes, accounts for, causes, improves, worsens, ahead, behind, replaces, reduces, increases), confirm the verb and its direction match the source. A correct figure with the wrong verb is an error.

NOT STATED: for every "Not stated", "Not measured", or "Unresolved" in the DRAFT, confirm the source is in fact silent. For every place the DRAFT says the source cannot answer a question, check whether the source gives a partial answer (mostly, partly, in one environment) that the DRAFT overstated as silence.

CAVEATS: for every item the DRAFT tells the reader to stop, start, drop, release, or fund, check whether the source attaches a caveat or condition that the DRAFT omitted.

STATUS: for every "current", "deployed", "live", "in production", "released", "runs", "powers", or bare present tense that implies an item is in use, confirm the source states that status for that item. Check the other direction too: a deployment the source states must not read as a proposal, and the source's hedge ("is piloting", "plans to") must survive.

RECOMMENDATIONS: for every action the DRAFT presents as required, confirm the source does not merely recommend, propose, or suggest it.

QUESTIONS: for the three answered questions, does the source actually bear on each question as asked, or does the question presuppose something the source does not say? For the three follow-up questions, is each one about a specific claim, figure, or term in the source; not already answered by the source; not a repeat of an answered question; and not a disguised recommendation?

ADJECTIVES: list every evaluative adjective or adverb in the DRAFT answers (invalid, proven, fine, strong, weak, clearly, significant, and the like). The stance label is allowed. The source's own measured comparatives are allowed. Blunt wording inside the questions is allowed.

Return only the following, nothing else. Do not summarise the source.

1. UNSUPPORTED: each item with the draft wording and what the source says.
2. MISQUOTE: each item with the draft quote and the source wording.
3. STRETCH: each item with the dropped qualifier or scope word.
4. DIRECTION: each error with the source verb.
5. NOT STATED: each overstatement of silence.
6. CAVEATS: each omitted condition.
7. STATUS: each deployment or adoption status the source does not state, upgraded or downgraded.
8. RECOMMENDATIONS: each source recommendation the DRAFT presents as required.
9. QUESTIONS: each unfair or duplicated question.
10. ADJECTIVES: the list.
11. COUNTS: per answer (stance, A1, A2, A3, follow-ups), claims checked and claims supported.

Be strict. Prefer a false alarm to a missed error.
```

## After the audit

Fix every item in categories 1 through 10. Re-check every quoted phrase by searching the whitespace-collapsed source. Then run the audit again on the corrected draft. Stop when a round returns no items in categories 1 through 9; category 10 items must be removed, quoted, or attributed.

Print the `Audited:` line in the output only with the counts from the final round.
