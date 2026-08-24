# ELI5 explanation format

One artifact: a short explanation the reader can repeat back. Hard ceiling **400 words**.

## Word budgets

Ceilings, not targets. Pick the tier from how many ideas the reader must hold, never from file length.

| Source | Ceiling |
| --- | --- |
| One mechanism or short file | 150 words |
| A file with one main path and a few options | 250 words |
| A file with several parts that depend on each other | 400 words |

If the explanation does not fit, cut side paths and options before cutting bedrock or steps. Never raise the ceiling silently.

## Status line

Only when you could not read the whole file, the explanation begins:

> **I could only read part of this.** <which part is missing and what the explanation therefore leaves out>

---

# The explanation

Four required sections, two optional, in this order. Headings exactly as written, sentence case. No other headings, no tables, no diagrams, no glyphs.

## What this is

One or two sentences. The kind of thing and the one job it does. A stranger can now say what they are holding.

## The basic facts

Two to five short bullets: the bedrock from the first-principles procedure. Each bullet is one plain fact. Facts the file states carry no label. A fact that is generally true ends with "(true everywhere, not just here)". A fact the file needs but never states ends with "(the file assumes this but does not say it)".

## How it works

Numbered steps, one sentence each, in an order where every step rests only on the basic facts and the steps before it. Usually three to eight steps. Follow the file's main path from its input to its result. Mention that other paths exist only when leaving them out would mislead.

## Why it is this way

The file's stated reasons, as the file's reasons: "The file says retries are off for charges because a double charge is worse than a failed one." When the file gives no reason for a mechanism the reader will wonder about, write "The file does not say why" for that mechanism. Never supply a reason.

## Words you will see

Optional. Include only when the reader will open the file and meet a term they must recognize. One line per term: the term, a colon, then what it means in plain words. Skip the section when no term qualifies. Never define a term the reader will not meet.

## What the file does not say

Optional. Include only when a reader would reasonably expect something the file leaves out and its absence matters to using the file. One or two sentences. This reports an absence; it does not judge it or suggest what should be there.

---

## Rules that bind every section

- **One idea per sentence.** Aim for under fifteen words. Never over twenty-five.
- **Common words.** Prefer the word a child knows. When a technical word is needed because the reader will meet it, introduce it once with a concrete picture, then use it.
- **No term before its introduction.** This applies across sections: a word introduced in "Words you will see" may not appear earlier without its plain meaning beside it.
- **Numbers stay exact**, with their unit and what they count.
- **Analogies** are allowed after the plain statement, never instead of it, and always say where they stop matching in the same sentence or the next.
- **No judgment, no advice, no fix.**
- **No baby talk.** No exclamation marks, no pet names, no "imagine", no story frame, no rhetorical questions, no cheer.

## Typography

- Never em-dashes or en-dashes, including ranges: "3-5". Use a comma, colon, period, or parentheses.
- No emoji, no decorative symbols.
- Bold only in the status line. Never for emphasis.
- Straight quotes.

The full writing rules live in [human-voice.md](human-voice.md). Load them before drafting.

## Optional saved artifact

When the user asks to save, write `<source base name> - ELI5.md`. Never overwrite the source.

## Before returning: the repeat-back pass

Reread once as the reader, then:

- for each paragraph, confirm the reader could say it back after one read;
- confirm no term appears before it is introduced;
- confirm every step rests on an earlier step or a basic fact;
- confirm every "why" is the file's or says the file does not say;
- confirm every number matches the file exactly;
- cut every sentence that adds no fact the reader needs;
- recount the words;
- run the [human-voice.md](human-voice.md) check.
