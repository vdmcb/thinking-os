# ELI5 explanation format

One artifact: a short explanation the reader can repeat back. It ends on its last fact.

## Budget follows ideas

An idea is one thing the reader must hold: one basic fact, one step, or one term in the glossary. Count them before writing and pick the ceiling from the count, never from the length of the file.

| Ideas the reader must hold | Word ceiling |
| --- | --- |
| up to 9 | 250 words |
| up to 14 | 375 words |
| up to 19 | 500 words |

Structural caps: 2 to 5 basic facts, 3 to 8 steps, 0 to 6 terms. 500 words is the hard ceiling. Cut order when it does not fit: glossary terms, side paths inside steps, "What the file does not say", numbers off the main path. Never cut a basic fact, a main-path number, or a "the file does not say why". Never raise the ceiling silently.

## Status line

Only when you could not read the whole file, the explanation begins:

> **I could only read part of this.** <which part is missing and what the explanation therefore leaves out>

---

# The explanation

Four required sections, two optional, in this order. Headings exactly as written. No other headings, no tables, no diagrams, no glyphs.

## What this is

One or two sentences: the kind of thing the subject is and the one job it does. For a document that proposes or describes something, this is the thing, not the document, which is named in passing.

## The basic facts

Two to five bullets: the bedrock. Each bullet is one plain fact the subject rests on. Facts from the file carry no label. A fact the file did not need to state ends with "(general knowledge, not from the file)". A condition the file needs but never states ends with "(the file assumes this but does not say it)". A claim the file makes is not a basic fact.

## How it works

Numbered steps, one sentence each, three to eight, in an order where every step rests only on the basic facts and the steps before it. Follow the subject's main path from its input to its result. Side paths and options are held; mention that they exist only when leaving them out would mislead.

When the file does not describe how the subject works, this section is one or two sentences saying so and naming what the file gives instead. Do not narrate the document's structure to fill the section.

## Why it is this way

The file's stated reasons, as the file's reasons: "The file says retries are off for charges because a double charge is worse than a failed one." For each mechanism the reader will wonder about that the file leaves unexplained, write "The file does not say why". Never supply a reason.

## Words you will see

Optional. A lookup for when the reader opens the file: terms they will meet there and must recognize. One line per term: the term, a colon, then what it means in plain words. A term listed here is not used earlier in the explanation; if the explanation needs it, introduce it inline at first use and leave it out of the glossary. Skip the section when no term qualifies.

## What the file does not say

Optional. One or two sentences reporting an absence that a reader would reasonably expect and that matters to using the file. No judgment, no suggestion.

---

## Rules that bind every section

- **One idea per sentence.** Aim for under fifteen words. Never over twenty-five.
- **Common words.** Prefer the word a child knows. A technical word the reader will meet is introduced once with a concrete picture, then used.
- **No baby talk.** No exclamation marks; no pet names ("kiddo", "buddy"); no "imagine you have", "picture this", "think of it like a magic box"; no story frames ("once upon a time"); no rhetorical questions; no cheer ("cool, right?", "great job"); no "so basically".
- **Bold only in the status line.** Typography and voice rules are in [core/writing.md](core/writing.md).

## Optional saved artifact

When the user asks to save, write `<source base name> - ELI5.md` using the template in `assets/`. Never overwrite the source.
