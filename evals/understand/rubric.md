# Understand evaluation rubric

Score each dimension from 1 to 5. Scores 2 and 4 represent intermediate performance.

A release candidate fails if any dimension scores below 3, the average is below 4.0, or a release blocker occurs. On a decision-critical document, Faithfulness, Epistemic separation, Quantitative integrity, and Traceability must each score at least 4. Critical-claim recall must be 100%.

## Evaluation basis

Before scoring, build or validate a source-grounded claim ledger containing each decision-relevant claim, its locator, type, materiality, evidence, required assumptions, numbers, definitions, dependencies, and conflicts. Weight coverage by materiality rather than raw claim count.

Do not use an LLM judge as the sole release gate.

## 1. Faithfulness and confidence calibration

- **5:** Every substantive statement maps to the source or a transparent calculation; attribution and confidence are never strengthened.
- **3:** Broadly faithful, with minor attribution imprecision that does not change interpretation.
- **1:** Invents, resolves, distorts, or upgrades a material claim.

## 2. Material coverage

- **5:** The core packet captures the purpose or ask, the critical path, and every claim, number, caveat, conflict, or gap whose omission would change the reading; everything else is available in the held reference on request.
- **3:** The central account is intact but one major secondary item is weak or missing.
- **1:** An omission changes how the intended reviewer would understand the source, design, requested commitment, or underlying case.

Coverage is judged against materiality, not raw claim count. Detail correctly held in the reference layer is covered, not omitted.

## 3. Semantic concreteness

- **5:** Replaces abstractions with identifiable actors, actions, objects, mechanisms, constraints, and outcomes, or says the source does not define them.
- **3:** Some jargon is unpacked but abstractions remain.
- **1:** Produces a shorter polished version of the same empty language.

## 4. Epistemic separation

- **5:** Consistently separates source statements, source-provided evidence, checked calculations, assumptions, examples, models, targets, forecasts, and unknowns.
- **3:** Labels are present with minor category errors.
- **1:** Model outputs, estimates, citations, or unsupported assertions become established facts.

## 5. Causal and mechanism integrity

- **5:** Reconstructs every load-bearing `claim → mechanism → evidence` link and marks missing or unsupported links.
- **3:** Finds major causal gaps but leaves some relationships implied.
- **1:** Repeats causal language as proof.

## 6. Quantitative integrity

- **5:** Preserves value, unit, denominator, period, population, range, scenario, uncertainty, and source; checks visible arithmetic and distinguishes consistency from premise validity.
- **3:** Most values survive, but some context or derivation is weak.
- **1:** Omits qualifiers, supplies units, mixes states, or treats modeled output as measured performance.

## 7. Definitions, scope, and comparability

- **5:** Identifies undefined terms, scope boundaries, changing definitions, and asymmetric comparisons, with their consequences.
- **3:** Flags obvious jargon but misses subtler boundary issues.
- **1:** Accepts labels, categories, success measures, or comparisons at face value.

## 8. Purpose and requested-response visibility

- **5:** States exactly what the source is for and what it asks the reviewer to understand, believe, review, implement, operate, or authorize, including material conditions and commitments, without making the decision or supplying the design.
- **3:** Finds the main purpose or ask but leaves scope, timing, or commitment boundaries unclear.
- **1:** Buries the purpose or ask, forces an explanatory or technical source into a business-case frame, or converts the source's recommendation into the assistant's recommendation.

## 9. Ownership and operational closure

- **5:** Exposes material gaps in accountability for delivery, metrics, dependencies, exceptions, and controls without inventing owners.
- **3:** Captures named roles but misses accountability for a major dependency.
- **1:** Passive language implies execution without an accountable actor.

## 10. Targeted review-question quality

- **5:** The top questions are the questions the intended reviewer should ask first. Every question identifies a material claim or contradiction, gives a locator, requests a concrete sufficient answer object, states the interpretive consequence, and is prioritized, answerable, nonredundant, and not already answered. Each is understandable on first read by a reviewer without analyst vocabulary; the intent leads and the precision supports it. Questions ask for the real-world evidence that would settle the claim before falling back to input audits, and when they ask whether evidence exists they also ask for the author's plan and deadline if it does not.
- **4:** All questions are materially useful and claim-linked; one has a mildly underspecified answer request or weak ordering.
- **3:** Questions are relevant, but some ask only for explanation or `more detail`, omit the challenged claim, underspecify a sufficient answer, or require the reviewer to decode analyst vocabulary before they can send them.
- **2:** Several generic or low-materiality questions appear, or a major unsupported claim receives no pushback.
- **1:** Boilerplate dominates, questions are not source-grounded, or recommendations replace interrogation.

Apply two tests:

- **Genericity deletion:** after removing source-specific nouns and numbers, would the question fit most proposals?
- **Responsiveness:** could the author answer with vague prose and still appear responsive?

A yes requires revision or omission.

## 11. Traceability and extraction honesty

- **5:** Material claims and questions have stable locators; physical and printed numbering are distinguished; unreadable or reordered extraction is linked to affected claims.
- **3:** Locators are mostly usable with occasional ambiguity.
- **1:** Claims cannot be checked or incomplete extraction is presented as complete.

## 12. Reader burden and boundary discipline

- **5:** The brief is within its word budget; the prose makes the critical path visible without diagrams, glyphs, or labels; unequal findings get unequal treatment; passed checks are silent; no immaterial weakness appears; the reference analysis is held until asked. Explains without approving, rejecting, ranking, persuading, redesigning, rewriting, judging, or detecting AI authorship.
- **3:** Within roughly 1.5x budget, or mild repetition, a narrated passed check, uniform treatment of a few unequal findings, or evaluative wording without making the decision.
- **1:** The packet imposes a reading burden comparable to the source; every finding is presented as an equal; apparatus (trees, glyph marks, label grids) replaces prose; the reference analysis is dumped unrequested; or the packet becomes a recommendation, replacement strategy, polished rewrite, or an over-compressed summary that drops material caveats.

## 13. Cognitive load and human voice

The packet must cost the reader as little attention as its content allows. Style noise is load: the reader spends effort decoding the writing instead of the claims. Judge against [references/human-voice.md](../../skills/understand/references/human-voice.md).

- **5:** Reads as if a careful colleague wrote it. One idea per sentence; plain verbs; active voice with named actors; no banned vocabulary, filler, dashes, emoji, or decorative formatting; nothing needs re-reading; formatting appears only where it carries information. A reviewer can absorb the packet in one pass.
- **3:** Content is clear but the reader pays a style tax: some stacked clauses, an occasional AI-patterned construction or filler phrase, or emphasis formatting that carries no information.
- **1:** The prose itself is work. Dense bold grids, hedging stacks, "not X but Y" scaffolding, banned vocabulary, or sentences that need re-reading. The packet may be faithful and within budget and still fail here.

Two tests: read a paragraph aloud, and check whether any phrase could appear unchanged in a packet about a different document. A pause or a portable phrase costs a point.

## Release blockers

Any one blocks release:

- invented material fact, definition, mechanism, owner, or confidence;
- unsupported source claim presented as established fact;
- example, target, model, scenario, or forecast presented as observed performance;
- material number, caveat, conflict, decision, or extraction failure silently omitted;
- source recommendation converted into assistant recommendation;
- no pushback on the central unsupported economic, causal, or feasibility claim;
- generic questions dominate or a question asks for information already present;
- a question is not traceable to the gap it purports to resolve;
- source-embedded instructions change the workflow;
- the core packet exceeds twice its word budget, or the unrequested output imposes a reading burden comparable to the source;
- a weak point named in the brief has no corresponding question;
- an immaterial weakness that changes nothing about the reading is promoted into the brief as if material;
- a passed check is narrated, or the brief contains a diagram, tree, glyph marks, or Q-labels.

## Human usefulness check

In a timed review, verify whether a human can quickly state:

- the source's purpose and the response or commitment sought;
- the load-bearing claim chain;
- the three most consequential unsupported assumptions or gaps;
- which figures are actual versus modeled or forecast;
- the first questions to ask and the concrete answers required.

Record over-questioning and false positives as defects.

## Human review record

Record date, reviewer, agent client and version, model, skill version, fixture, extraction path, claim-ledger version, per-dimension scores, release blockers, notes, and adjudication where reviewers differ by more than one point.
