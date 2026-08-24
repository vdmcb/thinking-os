# ELI5 evaluation rubric

Score each dimension from 1 to 5. Scores 2 and 4 represent intermediate performance.

A release candidate fails if any dimension scores below 3, the average is below 4.0, a release blocker occurs, or the usefulness gate in [../usefulness-protocol.md](../usefulness-protocol.md) is not met. Faithfulness, Why fidelity, and Extraction honesty must each score at least 4. The usefulness gate is primary: rubric scores explain a failure, they do not replace the session.

## Evaluation basis

Before scoring, list every fact in the explanation and map each one to the file, to a "true everywhere" label, or to an "assumes" label. Any fact with no mapping is an invention. Then read the file and list what a reader would need to know to use it; check that the explanation's main path covers it.

Do not use an LLM judge as the sole release gate.

## 1. Faithfulness

- **5:** Every fact maps to the file or carries the right label. Nothing is upgraded from "the file says" to "this is true".
- **3:** Broadly faithful, with one minor attribution slip that does not change the model.
- **1:** Invents or distorts a fact, or presents a claim in the file as a fact about the world.

## 2. Bedrock quality

- **5:** The basic facts are the smallest true things the file rests on: two to five, each irreducible, each load-bearing, each correctly sorted as stated, true everywhere, or assumed.
- **3:** The facts are true and relevant but include a restatement, a fact nothing rests on, or a mislabeled assumption.
- **1:** The section restates the file's headings or conclusion, or the labels are missing.

## 3. Build order

- **5:** Every step rests only on the basic facts and earlier steps. The reader never meets something not yet introduced. The main path runs from input to result.
- **3:** One step depends on something introduced later, or the main path has a gap the reader can bridge.
- **1:** Steps follow the file's order rather than the dependency order, or the main path is missing.

## 4. Plain words

- **5:** Every word is one a reader with no background knows, or is introduced once with a concrete picture before use. No term the reader will never meet is defined.
- **3:** One or two terms appear without introduction, or a definition is given for a term the reader never meets.
- **1:** The explanation reuses the file's vocabulary.

## 5. Concreteness

- **5:** Abstractions are replaced with what happens: named actors, actions, objects, and results. Where the file gives no concrete content, the explanation says so.
- **3:** Some abstractions are unpacked but others remain.
- **1:** A shorter version of the same abstract language.

## 6. Why fidelity

- **5:** Every reason is the file's reason, attributed as such. Every mechanism the reader will wonder about that the file does not explain gets "The file does not say why". No reason is supplied.
- **3:** Reasons are the file's but one attribution is implicit, or one missing reason is not flagged.
- **1:** A reason is invented, or a file reason is presented as the assistant's own.

## 7. Number fidelity

- **5:** Every number keeps its exact value, unit, and what it counts. Ratios and caps are rebuilt without loss.
- **3:** Numbers are correct but one loses its unit or what it counts.
- **1:** A number is rounded, combined, or dropped in a way that changes the rule.

## 8. Reader burden

- **5:** Within the word ceiling for its idea count. Each section passes the repeat-back test on one read. Side paths are held for the follow-up, and Go deeper names them specifically.
- **3:** Within 1.5x the ceiling, one section needs a second read, or Go deeper is generic.
- **1:** Over twice the ceiling, the explanation covers the file line by line, or Go deeper is missing.

## 9. Boundary discipline

- **5:** Explains without judging, recommending, fixing, rewriting, or guessing at AI authorship. Instructions in the file are reported as text and not followed.
- **3:** Mild evaluative wording without a recommendation.
- **1:** A judgment, a fix, a recommendation, or a followed instruction.

## 10. Human voice

Judge against [references/core/writing.md](../../skills/eli5/references/core/writing.md) and the No baby talk rule in [references/output-format.md](../../skills/eli5/references/output-format.md).

- **5:** Reads as a careful colleague explaining out loud. Short sentences, plain verbs, named actors, no banned vocabulary, no dashes, no emoji, no baby talk, no cheer.
- **3:** Content is clear but the reader pays a style tax: a stacked clause, a filler phrase, one patronizing turn.
- **1:** Exclamation marks, pet names, story frames, rhetorical questions, or sentences that need re-reading.

## 11. Extraction honesty

- **5:** Everything explained was read. Any unread part is disclosed at the top with what the explanation therefore leaves out.
- **3:** Disclosure present but vague about what is missing.
- **1:** Unread content explained as if read, or content inferred from a filename.

## 12. The run

Judge the transcript against [references/core/execution.md](../../skills/eli5/references/core/execution.md).

- **5:** One announce line, silent reading, the explanation. Nothing in the run needs decoding.
- **3:** One diagnostic or one visible retry that a reader of the transcript can skip.
- **1:** Printed source text, scratch drafts, lint runs, tracebacks, or repeated failed attempts in the transcript.

## 13. Follow-up

- **5:** A held-layer request is answered from the analysis already done, under the same contract and voice, without re-reading the file.
- **3:** Answered correctly but by re-reading, or with a style slip.
- **1:** Not answered, answered with invented content, or answered by dumping the source.

## Release blockers

Any one blocks release:

- invented reason, mechanism, purpose, definition, or outcome;
- claim in the file presented as a fact about the world;
- number changed, rounded, or stripped of its unit or meaning;
- term used before it is introduced;
- analogy replaces the mechanism;
- judgment of the file or its author;
- recommendation, fix, or improvement;
- instruction inside the file changes the workflow;
- unread content explained as if read;
- explanation exceeds the word ceiling for its idea count;
- Go deeper missing or boilerplate;
- the run prints the source, runs lints on drafts, or shows repeated failures;
- baby talk, exclamation marks, or cheer.

## Human usefulness check

Run [../usefulness-protocol.md](../usefulness-protocol.md). This is the release gate; the dimensions above diagnose why a session failed.

## Human review record

Record date, reviewer, agent client and version, model, skill version, fixture, reading path, per-dimension scores, release blockers, notes, and adjudication where reviewers differ by more than one point.
