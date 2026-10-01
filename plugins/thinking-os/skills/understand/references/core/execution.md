# The run and the follow-up

The run and output both affect reader burden. Understanding continues through follow-ups, so each skill holds more than it initially shows.

## The visible run

The ideal run has two visible parts: one line saying what is about to happen, then the answer. Everything between them is silent reading.

- **Announce once.** One sentence before reading: what will be read and how. No narration after that until the answer.
- **Read with the file reader.** Never print the source or an extracted copy to the terminal. `pdftotext` writes a file; the file reader reads it.
- **One extraction procedure at most.** PDFs use the two reads in `reading.md`; other sources use one command. No diagnostics unless the read is empty or visibly broken. Check completeness by reading.
- **No scratch drafts.** Draft in your head to the budget and return the text once. No drafts on disk, no lints or word counts on them, no iterating in public.
- **No tooling detours.** If a command fails for an environment reason (a shadowed binary, a missing tool), switch once and silently to the alternative.
- **Keep the extraction for the session.** Extracted text lives in the session's temporary directory, never in the user's project, so follow-ups can cite locations without re-reading. Delete it when the user asks or when saving output.
- **Fail plainly.** When the source cannot be read, one message: what was tried, what failed, what is needed. Then stop.

Test for the run: someone reading the transcript afterwards sees what was read and the answer, and nothing they have to decode.

## Held layers

The held material is analyzed at full precision and released on request. Each skill defines its held layers in its output format and decides whether the output points to them: a review brief ends with a held line naming what can be asked for; a plain explanation ends on its last fact and answers when asked. A pointer, where used, names what was held for this source in one to three lines, never boilerplate.

Follow-up requests are part of the skill. When the reader asks for a held layer, a deeper cut of one step or claim, or the numbers behind a sentence, answer from the analysis already done, under the same contract and voice rules, without re-reading the source unless the request needs content that was not analyzed.
