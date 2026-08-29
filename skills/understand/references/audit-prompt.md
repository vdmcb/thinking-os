# Audit prompt

Give this prompt to an independent agent together with the internal evidence packet and the draft output. The agent must not have written the draft. Do not give it the original asset, a path to the asset, or extraction and rendering tools. If no agent is available, run the same prompt yourself as a distinct comparison using the same packet.

Fill `EVIDENCE_PACKET` with the claims, exact figures and phrases, qualifiers, locators, value statuses, visual facts, source inventory, and coverage gaps captured during the one source-read pass. Fill `DRAFT` with the complete draft, including the stance line, the three answers, and the three follow-up questions.

```text
You are an adversarial fact-checker. EVIDENCE_PACKET is the complete evidence available for this audit: <packet>. DRAFT is the text under audit: <draft>.

Do not open, extract, render, or request the original asset. Do not use outside knowledge to fill a gap. Compare the whole DRAFT with the whole EVIDENCE_PACKET. For every number, quoted phrase, comparative, and factual statement in the DRAFT, classify it as one of:

SUPPORTED: recorded verbatim in the evidence packet, or an exact arithmetic restatement of figures recorded there.
UNVERIFIABLE: absent from the evidence packet. It may or may not appear in the original asset; the audit must not reopen the asset to find out.
UNSUPPORTED: contradicted by the evidence packet.
STRETCH: an inference the evidence packet does not support; a dropped qualifier such as about, roughly, partly, only, directly, in practice, typical; or a dropped scope word such as which environment, population, model, batch, condition, or period the figure applies to.
MISQUOTE: quotation marks around words that are not verbatim. Collapse whitespace and HTML entities before matching; anything else counts as a misquote.

Then run these checks separately:

DIRECTION: for every figure that sits next to a verb (closes, accounts for, causes, improves, worsens, ahead, behind, replaces, reduces, increases), confirm the verb and its direction match the evidence packet. A correct figure with the wrong verb is an error.

NOT STATED: for every "Not stated", "Not measured", or "Unresolved" in the DRAFT, confirm the evidence packet records that absence or unresolved status. If the packet has no finding either way, mark the draft statement UNVERIFIABLE. For every place the DRAFT says the source cannot answer a question, check whether the packet records a partial answer (mostly, partly, in one environment) that the DRAFT overstated as silence.

CAVEATS: for every item the DRAFT tells the reader to stop, start, drop, release, or fund, check whether the evidence packet records a caveat or condition that the DRAFT omitted.

STATUS: for every "current", "deployed", "live", "in production", "released", "runs", "powers", or bare present tense that implies an item is in use, confirm the evidence packet records that status for that item. Check the other direction too: a recorded deployment must not read as a proposal, and a recorded hedge ("is piloting", "plans to") must survive.

RECOMMENDATIONS: for every action the DRAFT presents as required, confirm the evidence packet does not record it merely as recommended, proposed, or suggested.

QUESTIONS: for the three answered questions, does the evidence packet bear on each question as asked, or does the question presuppose something the packet does not support? For the three follow-up questions, is each one about a specific recorded claim, figure, term, or gap; not already answered in the packet; not a repeat of an answered question; and not a disguised recommendation? A closing sentence that asks for the owner's plan and deadline when the evidence does not exist is the format's permitted fallback, not a recommendation.

ADJECTIVES: list every evaluative adjective or adverb in the DRAFT answers (invalid, proven, fine, strong, weak, clearly, significant, and the like). The stance label is allowed. The source's own measured comparatives are allowed. Blunt wording inside the questions is allowed.

Return only the following, nothing else. Do not summarise the source.

1. UNSUPPORTED OR UNVERIFIABLE: each item with the draft wording and what the evidence packet says, or the packet gap.
2. MISQUOTE: each item with the draft quote and the evidence-packet wording.
3. STRETCH: each item with the dropped qualifier or scope word.
4. DIRECTION: each error with the verb recorded in the evidence packet.
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

Fix every item in categories 1 through 10 using only the same evidence packet. Re-check every quoted phrase against its whitespace-collapsed exact phrase in the packet. Never reopen or re-extract the original asset between rounds. Then run the audit again on the corrected draft and the unchanged packet. Stop when a round returns no items in categories 1 through 9, or after the third round. Run at most three rounds. In the third round resolve every remaining item by deletion or downgrade only (cut the sentence, or replace the claim with "Not stated"); do not re-source or rewrite. The output ships only when the final round reports zero items in categories 1 and 2, and the `Audited:` line carries that round's counts; count every `UNVERIFIABLE` item as unsupported in that line. Never run a fourth round. Category 10 items must be removed, quoted, or attributed.

Print the `Audited:` line in the output only with the counts from the final round.
