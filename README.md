# Thinking OS

**Portable cognitive skills for capable AI agents.**

Thinking OS adds disciplined reasoning procedures to existing agent runtimes instead of building another chat application. Claude Code and Codex provide the model, conversation, local file access, permissions, and tools. Thinking OS provides the behavior contract.

## Project supporter

The main supporter of Thinking OS is [RebelDot](https://www.rebeldot.com/).

<a href="https://www.rebeldot.com/">
  <img src="assets/rebeldot-logo.svg" alt="RebelDot" width="220">
</a>

RebelDot supports the internal experimentation and practical validation of agent-native ways of working. RebelDot does not imply endorsement of every experimental result or future public release.


## Understand

`Understand` is the first Thinking OS skill. It turns documents and pasted material into a faithful, plain-language model of:

- the central idea;
- material claims and the reasoning offered for them;
- evidence, assumptions, and unknowns;
- important numbers, constraints, caveats, and disagreements;
- ambiguity and missing definitions;
- focused questions that would materially improve understanding;
- extraction gaps and source locators.

It is for anyone carrying the cost of reviewing polished or AI-generated material. It can review proposals, reports, ideas, and strategies from an executive perspective, but it is not limited to executives or business documents. It also handles technical designs, architecture notes, implementation proposals, operating procedures, policies, research, and other material where a human needs to expose the actual logic and ask targeted questions.

Understand applies the review perspectives relevant to the source, such as decision and commitment, technical correctness, implementation feasibility, security, operations, evidence, and accountability. It does not force every source into an executive-summary format.

It is not a generic summarizer. It does not recommend a decision, rewrite the source, invent missing logic, judge the author, or try to detect whether AI wrote the material.

## ELI5

`ELI5` is the second Thinking OS skill. It explains a file to someone with no background, from first principles:

- what the thing is, in one sentence;
- the two to five basic facts everything else rests on, each marked as stated in the file, true everywhere, or assumed by the file;
- how it works, as numbered steps where each step rests only on earlier ones;
- why it is this way, reporting only the file's own reasons and saying plainly when the file does not say;
- the few words the reader will meet in the file and must recognize.

"Five years old" describes the reader's background, not the tone. The explanation uses short common words and concrete steps, without baby talk, cheer, or analogies that replace the mechanism. It works on documents, source code, config files, specs, and policies.

It is not a summary, a rewrite, or a review. It does not judge the file, recommend a change, or invent a reason the file does not give. For claim-linked review questions, use `understand`.

## How the skills are built

Every skill is a lens on a shared core in `core/`: how a source is read and what may be claimed about it (`reading.md`), how output is written for a tired human and how budgets follow ideas rather than pages (`writing.md`), and what the visible run looks like and how the output opens a follow-up (`execution.md`). The core is copied into each skill package by `./scripts/sync-core.sh` so that packages stay self-contained; validation fails on drift.

The run is part of the product. A skill announces once what it will read, reads silently with the file reader, and returns the output. It does not print the source, run diagnostics unless the read came back empty, or draft in public. Every output ends by naming what was held for follow-up, and follow-up requests are answered from the analysis already done.

The release gate is the human usefulness protocol in `evals/usefulness-protocol.md`: a reader who has not seen the source reads the output, repeats it back, opens the source, and counts surprises. Lints and rubrics diagnose failures; the session decides.

## Install

This repository is private. Installation currently requires GitHub access to `vdmcb/thinking-os`.

### Claude Code and Codex

```bash
npx skills add vdmcb/thinking-os --skill understand -g -a claude-code -a codex -y
npx skills add vdmcb/thinking-os --skill eli5 -g -a claude-code -a codex -y
```

Install for only one agent by removing the other `-a` value.

### Manual installation

```bash
cp -R skills/understand ~/.claude/skills/understand
cp -R skills/understand ~/.agents/skills/understand
cp -R skills/eli5 ~/.claude/skills/eli5
cp -R skills/eli5 ~/.agents/skills/eli5
```

## Use

Claude Code:

```text
/understand path/to/proposal.pdf
```

Codex:

```text
$understand path/to/proposal.pdf
```

You can also invoke the skill and paste source material directly. Explicit invocation is recommended during the internal pilot.

The default output is an **Understanding Packet** in the current conversation. The source is never modified. A Markdown result is written only when explicitly requested.

ELI5 is invoked the same way:

```text
/eli5 path/to/config.yaml
```

```text
$eli5 path/to/config.yaml
```

The default output is a short explanation in the conversation, budgeted by the number of ideas the reader must hold (at most 500 words), ending with a Go deeper section that names what was held. The source is never modified. A Markdown result is written only when explicitly requested.

## Five-minute smoke test

1. Install the skill.
2. Open Claude Code or Codex in a directory containing a proposal or report.
3. Invoke `understand` with the file path.
4. Confirm the result contains:
   - `In one sentence`;
   - `Core ideas`;
   - `How the source's reasoning works`;
   - `What is solid, assumed, and unknown`;
   - material facts and constraints;
   - remaining ambiguity;
   - focused author questions;
   - extraction limitations.
5. Confirm the result explains the source without independently recommending approval, rejection, or another strategy.

## Supported sources

The skill accepts pasted text, Markdown, plain text, DOC/DOCX, PPT/PPTX, PDF, CSV, XLS/XLSX, OpenDocument, RTF, and EPUB when the host can access them.

The agent should use its native reader first. When native reading is unavailable, the bundled helper uses Firecrawl AnyDoc locally:

```bash
core/scripts/extract-document.sh INPUT_FILE OUTPUT_MD
```

Requirements for the fallback:

- Node.js 20 or later
- `npx`
- Network access the first time the pinned AnyDoc package is downloaded

AnyDoc does not OCR scanned or image-only PDFs. In those cases, the agent may use reliable host-native vision and must disclose that path. Otherwise it must stop or mark the result incomplete.

## Privacy and security

- Source files are processed locally by default.
- The extraction helper uses the local `@firecrawl/anydoc` package and does not call a hosted parsing API.
- Material inside a source is treated as untrusted content, not as agent instructions.
- The helper never modifies the source and refuses to overwrite an existing output file.
- Temporary extraction output should be deleted after use unless the user asks to retain it.

## Repository structure

```text
core/                    Shared reading, writing, and execution contracts, and the extraction helper
skills/understand/       Portable skill package: Understand (core copied in)
skills/eli5/             Portable skill package: ELI5 (core copied in)
evals/usefulness-protocol.md   The human usefulness gate shared by every skill
evals/understand/        Activation and quality evaluation definitions for Understand
evals/eli5/              Activation and quality evaluation definitions for ELI5
scripts/                 Repository validation and core sync
tests/                   Extraction helper tests
```

## Validate

```bash
./scripts/validate.sh
```

The validation suite checks core sync, Agent Skills structure, shell syntax, extraction behavior, and deterministic evaluation metadata. Semantic quality still requires human-reviewed runs in Claude Code and Codex. This private preview is not a validated public release.

## License

This private preview is currently **unlicensed for redistribution**. All rights are reserved. An open-source license will be selected before a public release.

## Acknowledgments

The human-voice writing rules in the `understand` and `eli5` skills draw on [blader/humanizer](https://github.com/blader/humanizer) and Wikipedia's "Signs of AI writing".
