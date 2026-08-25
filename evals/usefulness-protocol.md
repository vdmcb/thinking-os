# Human usefulness protocol

The only measurement that tests what Thinking OS claims: a reader who has not seen the source, given the skill's output, can say what the source is and how it works, and is not surprised when they then open it. Style lints and contract literals are proxies. This is the gate.

## Session

One reader, one source, one skill output. The reader has not seen the source and has no more background than the skill's target reader.

1. **Read.** The reader reads the output once, at their own pace. Record the time.
2. **Repeat back.** Without looking at the output, the reader says, in their own words:
   - for `eli5`: what the thing is, what it rests on, how it works, and why;
   - for `understand`: what the source asks for, what the case rests on, the three weakest points, and which of the questions they would send first.
   Record the account verbatim or as close as practical.
3. **Open the source.** The reader reads or skims the source with the output beside it, for at most twice the time spent in step 1.
4. **Count surprises.** A surprise is anything in the source that changes what the reader thought after step 2: a fact they had wrong, a mechanism they had missed, a number they did not know mattered, a reason they thought was the file's and was not. Classify each:
   - **material:** it changes the account from step 2;
   - **minor:** the account stands, they would have liked to know.
5. **Ask the follow-up.** The reader asks one question the output made them want to ask. Record whether the skill's follow-up answer came from the held analysis without re-reading, and whether the answer resolved it.
6. **Judge the run.** The reader, or a second person, reads the transcript of the run. Record whether anything in it needed decoding: printed source text, diagnostics, retries, drafts.

## Record

Use `evals/usefulness-record.md`. Records with real sources stay in `evals/<skill>/runs/`, which is ignored by git. Commit a record only if the source is synthetic or cleared.

## Gate

Before a release tag, each skill needs at least five sessions on distinct real sources, across at least two readers, with:

- no session with more than one material surprise;
- every follow-up answered from the held analysis;
- no run that needed decoding.

A session that fails the gate is a defect to fix in the skill, then rerun on a fresh source. Sessions that pass on a rerun of the same source do not count.
