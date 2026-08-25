# The run and the follow-up

The user sees the run as well as the output: every command, every printed result, every retry. For tools whose purpose is reducing cognitive load, a confusing run is a failed output even when the text is good. And understanding is rarely finished in one turn, so every skill holds more than it shows and answers from it on request.

## The visible run

The ideal run has two visible parts: one line saying what is about to happen, then the answer. Everything between them is silent reading.

- **Announce once.** One sentence before reading: what will be read and how. No narration after that until the answer.
- **Read with the file reader.** Never print the source or an extracted copy to the terminal. `pdftotext` writes a file; the file reader reads it.
- **One extraction command at most.** No `pdfinfo`, page counts, image listings, or other diagnostics unless the read itself came back empty or visibly broken. Completeness is checked by reading.
- **No scratch drafts.** Draft in your head to the budget and return the text once. No drafts on disk, no lints or word counts on them, no iterating in public.
- **No tooling detours.** If a command fails for an environment reason (a shadowed binary, a missing tool), switch once and silently to the alternative.
- **Keep the extraction for the session.** Extracted text lives in the session's temporary directory, never in the user's project, so follow-ups can cite locations without re-reading. Delete it when the user asks or when saving output.
- **Fail plainly.** When the source cannot be read, one message: what was tried, what failed, what is needed. Then stop.

Test for the run: someone reading the transcript afterwards sees what was read and the answer, and nothing they have to decode.

## Held layers

The held material is analyzed at full precision and released on request. Each skill defines its held layers in its output format and decides whether the output points to them: a review brief ends with a held line naming what can be asked for; a plain explanation ends on its last fact and answers when asked. A pointer, where used, names what was held for this source in one to three lines, never boilerplate.

Follow-up requests are part of the skill. When the reader asks for a held layer, a deeper cut of one step or claim, or the numbers behind a sentence, answer from the analysis already done, under the same contract and voice rules, without re-reading the source unless the request needs content that was not analyzed.
