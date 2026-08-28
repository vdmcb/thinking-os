# Evaluation status

## v1.1.0 internal preview: shared core and the follow-up (foundation inherited by v2.1.0)

- The skill now sits on the shared core (`core/`): reading, writing, and execution contracts are copied into the package by `scripts/sync-core.sh` and drift-checked in CI. `references/human-voice.md` is replaced by `references/core/writing.md`; the question-phrasing rules moved to `references/question-language.md`. Behavior is unchanged.
- Execution contract (core/execution.md): one announce line, silent reading with the file reader, no diagnostics unless the read is empty, no scratch drafts.
- The brief ends with one held line naming what can be asked for (reference analysis, arithmetic behind a named number, evidence behind a named claim, page map). Exemplars 14 and 15 carry it.
- Human usefulness protocol (evals/usefulness-protocol.md) is now the release gate; rubric dimension 14 scores the run and the follow-up. Sessions are logged in evals/understand/usefulness-log.json. Usefulness sessions completed: 0 of 5.
- Steps 1 and 3 and the large-document procedure now delegate to core/reading.md; `references/large-documents.md` is removed. The description excludes plain explanation for a reader with no background (eli5), and three eli5-shaped prompts were added as negative activation cases. Cross-skill boundary cases live in evals/activation-crosscheck.json.
- Lint word lists come from core/lint.json plus this skill's additions. Always-loaded instruction text is 7,316 words, reported by the eli5 checker but not gated; reducing it is open work.

## v2.1.0 internal preview: three stakeholder questions, audited (format v4)

The default output is a scoped Positive, Negative, or Mixed stance on a named object; three answered questions labelled Q1 (state), Q2 (decision), and Q3 (resources or first change); a "Follow-up questions" header with exactly three numbered questions; and an "Audited:" line printed only when true. The 600-word ceiling stays. The Q-labels that v0.6.0 removed are back on purpose: in a blind trial on four documents (a performance report, a methodology paper, a migration proposal, and a product briefing; sources and outputs not committed), the three-question format was picked 4 of 4 over a question-first format and a Heilmeier catechism, and nothing in the trial showed the labels being read as fiscal quarters.

Changes in 2.1.0, each traced to a defect an independent auditor caught during the trial:

- The audit in step 9 is mandatory and uses an independent agent when the host has one (skills/understand/references/audit-prompt.md). A self-audit passed a correct figure with a reversed causal verb three times; the independent agent caught it.
- Three rules in step 7: no evaluative adjectives or adverbs (the stance carries the judgement); no "current", "deployed", or "in production" unless the source states it; "recommends" stays a recommendation, and every qualifier and scope word travels with its figure.
- PDFs are read twice, layout for locators and tables and raw for reading order, after the layout read interleaved a two-column paper mid-sentence. A visibly clipped source is disclosed in the stance line.
- Inside quotation marks the source's characters win; the dash lint in check-evals.py skips quoted spans.

Evaluation alignment:

- Exemplars 14 and 15 are the format references. Exemplars 01-13 remain contract-behavior references (labels, injection resistance, value-status conflicts).
- Deterministic lints for exemplars 14 and up: 600-word ceiling; "Stance:", "Q1:", "Q2:", "Q3:", and "## Follow-up questions" with exactly three numbered items; no analyst jargon in questions; no dashes outside quotes; no emoji, banned vocabulary, or dramatic-reveal phrases. expected-invariants.json (schema 8) separates the five default sections from the seven reference-analysis headers.
- Live trial of the 2.1.0 skill on the four documents above: completed; sources and outputs remain private and are not committed.
- Still model-judged: materiality of omissions, question fairness, adjective discipline, personification.

## v0.6.0 internal preview: the brief (format v3, superseded)

Format v3, shaped by an annotated review of five candidate structures on a live 31-page deck (artifact "Four Packet Shapes"). The default output is now a brief: two or three paragraphs of memo prose that carry the critical path, then "Questions for the author", under a 600-word hard ceiling. No claim-map diagram, no glyph marks, no Q-labels (they read as fiscal quarters), no printed question metadata. Rules added from the review: passed checks are silent; no inherited source shorthand; no document personification; no dramatic reveals; questions are evidence-first ("what real-world fact settles this?") and ask for the author's validation plan and deadline when the evidence does not exist yet.

Evaluation alignment for this direction:

- Exemplars 14 and 15 are the v3 references: 14 exercises compression of a long uniform source, 15 exercises evidence-first question generation. Exemplars 01-13 remain contract-behavior references (labels, injection resistance, value-status conflicts) and no longer exemplify output format.
- Deterministic lints in check-evals.py now enforce, for exemplars numbered 14 and up: the 600-word ceiling, the "Questions for the author" section, no analyst jargon in questions, no dashes, emoji, banned vocabulary, or dramatic-reveal phrases. All canary-tested.
- Rubric: dimension 12 scores the brief's shape (prose-carried critical path, silent checks, no apparatus); dimension 10 scores evidence-first and plan-or-evidence question quality; dimension 13 scores cognitive load and human voice.
- Still model-judged, not lint-checked: weak-point-to-question mapping, materiality of omissions, personification, and intent-first phrasing. These require the scored human rubric runs, which remain pending for v3.

## v0.4.0 internal preview — core-packet format

Format v2 ("core packet"): the default output is now a critical-path claim map with clear/potentially-unclear marks, a Where-it-can-break section, and 3–5 sendable questions, under a 900-word hard ceiling; the full evidentiary reference analysis is held and produced only on request. Driven by a live trial on a 50-page survey-report PDF where the v1 format produced a faithful but ~4,500-word packet that imposed a reading burden comparable to the source.

- Expected references 01–13 predate the core-packet format: they remain valid for their contract behaviors (epistemic labels, pushback shape, injection resistance) but do not exemplify the v2 structure. Case 14 is the first v2 exemplar and the first case that exercises compression at all (earlier fixtures max out at 224 words).
- Reading order for paginated sources now requires a page-preserving extraction; AnyDoc output carries no page boundaries and is demoted to prose fidelity only. A visually-encoded-content check (charts with detached value/label text objects) now triggers page rendering regardless of text-layer quality.
- Scored model-level rubric runs on the v2 format: pending.
- Cognitive load is now evaluated on two levels: rubric dimension 13 (sentence load, human voice, formatting-as-information; informed by Wikipedia's "Signs of AI writing" via blader/humanizer) and a deterministic lint in check-evals.py that fails CI on dashes, emoji, banned vocabulary, and filler phrases in any expected packet exemplar. Writing rules live in skills/understand/references/human-voice.md and are loaded before output.

## v0.3.0 internal preview

- Agent Skills structure validation: passing
- Claude Code and Codex clean-directory installation: passing
- Local AnyDoc extraction tests: passing for CSV, DOCX, PPTX, XLSX, and native-text PDF
- Failure tests: missing input, directories, unsupported extensions, existing output, path collision, malformed PDF, misleading extension, permission denial, and missing prerequisites
- Activation metadata: 15 positive and 12 negative cases, including executive, technical, implementation, and operational review prompts
- Human reference decompositions: 13 synthetic cases
- Live document trial: completed manually on an internal 31-page PDF without committing source material or output
- Automated model-level semantic gate: not implemented
- Claude Code authentication: available; scored model-level rubric run still pending
- Codex authentication: available; scored model-level rubric run still pending

This commit is an internal preview, not a validated public release. Do not create a release tag until authenticated Claude Code and Codex runs are scored against the rubric and release blockers.
