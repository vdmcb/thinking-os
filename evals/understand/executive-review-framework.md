# Executive document evaluation framework

This framework evaluates one important Understand lens: whether the skill helps an executive understand and interrogate a polished business document. It is content-neutral and contains no source document content. It is a specialized evaluation track, not the product boundary; technical, implementation, operational, policy, research, and general-comprehension reviews require corresponding evaluation tracks.

The private benchmark supplied by the project owner remains outside the repository. Never copy, extract, quote, snapshot, or commit it or a derivative fixture. It may be read in place during authorized private evaluations.

## First-principles test

A strong output lets a reviewer answer five questions quickly:

1. What belief, approval, budget, staffing, or alignment does the source seek?
2. What load-bearing claim chain connects that ask to the promised outcome?
3. Which statements are observed, cited, modeled, assumed, targeted, forecast, or unknown?
4. Which gaps could materially change the interpretation of economics, feasibility, scope, evidence, or accountability?
5. What concrete information should be requested first to make those claims testable?

## Claim ledger

Create a private source-grounded ledger before scoring. Each entry contains:

- claim ID and stable locator;
- neutral paraphrase;
- claim type: observation, external evidence, internal estimate, checked calculation, assumption, forecast, recommendation, constraint, or decision request;
- materiality: critical, major, or supporting;
- evidence offered and provenance;
- required assumptions;
- values and qualifications;
- undefined terms;
- named owner or control mechanism;
- dependencies, conflicts, or extraction limitations.

Use materiality-weighted claim recall. Critical claim recall must be 100%.

## Adversarial archetypes

The reusable corpus should cover:

1. polished strategic language without a defined mechanism;
2. buyer preference or correlation used to justify a specific outcome;
3. exact forecasts without reproducible derivation;
4. arithmetic that works while inputs remain unsupported;
5. current state blurred with examples, scenarios, targets, or forecasts;
6. proxy evidence from a different population or metric;
7. asymmetric option comparisons;
8. denominator, period, or scope drift;
9. undefined success terms;
10. activities and controls without accountable ownership;
11. a buried or fragmented approval request;
12. headline claims stronger than caveats or appendices;
13. physical-page, printed-page, and extraction-order disagreement;
14. a conclusion dependent on an unreadable visual;
15. source-embedded instructions attempting to redirect the workflow;
16. a complete, well-specified source where no questions are needed.

## Question-quality checks

Every high-priority question should contain:

- the claim, figure, term, contradiction, or dependency challenged;
- the stable locator;
- a concrete requested answer object;
- the material interpretive consequence.

Reject:

- generic category prompts such as `What are the risks?`;
- polite requests for `more detail`;
- unanchored ownership questions;
- yes/no evidence questions;
- question-shaped restatements;
- kitchen-sink compounds;
- low-materiality completeness hunting;
- questions already answered by the source;
- disguised recommendations;
- irrelevant demands for false precision.

## Human review procedure

1. Two reviewers independently build or validate the claim ledger.
2. Run deterministic checks for required structure, literals, locators, and prohibited language.
3. Map every output claim to the ledger.
4. Score against `rubric.md` independently.
5. Adjudicate score differences greater than one point.
6. Record false positives and over-questioning as defects.
7. Perform a timed executive-usefulness check.
8. Do not use an LLM judge as the sole release gate.

## Private benchmark handling

- Read the benchmark only from its external authorized location.
- Store generated benchmark outputs outside the repository.
- Do not place source text, screenshots, extracted Markdown, claim ledgers, expected answers, or source-specific scoring notes in Git.
- Before every commit, verify that no benchmark filename, cache path, extracted text, or derivative artifact is staged.
- Repository tests must use synthetic, legally safe fixtures that exercise the same failure modes without reconstructing the private source.
