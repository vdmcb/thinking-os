# Examples and anti-examples

These examples demonstrate behavior, not fixed wording.

## Example 1: Proposal with weak support

### Source excerpt

> Our AI-native transformation layer will unlock operational leverage across the enterprise. A six-person team can deliver the platform in two quarters, reducing processing costs by 40% and creating a durable strategic moat.

### Good decomposition

- **Claim:** A six-person team can build the proposed system in two quarters.
- **Why the source says it should be true:** Not explained.
- **Evidence offered:** None in the excerpt.
- **Assumptions:** Scope is stable; required data and integrations are available; the team has the necessary skills.
- **Unknowns:** What “platform” includes, how the 40% reduction was calculated, and what prevents competitors from reproducing it.
- **Source:** Provided excerpt.

A useful author question is: “Which current cost baseline and modeled changes produce the 40% reduction?” It matters because the claimed economic value depends on that calculation.

### Bad output

> The company should start with a smaller pilot because the proposed transformation is too ambitious.

Why it fails: it introduces a recommendation and judgment rather than explaining the source.

## Example 2: Clear technical material

### Source excerpt

> Requests are retried twice after the initial attempt, with exponential delays of one and two seconds. HTTP 400-499 responses are not retried except 408 and 429. The total request deadline is ten seconds.

### Good decomposition

- A request can run at most three times: the initial attempt plus two retries.
- Retry delays are one second and then two seconds.
- Most client errors stop immediately; 408 and 429 are exceptions.
- All attempts and delays must fit within the ten-second deadline.
- No material follow-up questions are required to understand the behavior.

Why it works: it preserves every threshold and exception without inventing design advice.

## Example 3: Caveat changes the headline

### Source excerpt

> The pilot increased conversion from 8% to 12%. The treatment group contained 220 existing customers selected by account managers. New customers and self-serve accounts were excluded.

### Good decomposition

The source reports a four-percentage-point conversion increase in a selected group of 220 existing customers. It does not establish that the effect generalizes to new or self-serve customers, and account-manager selection may have influenced the result.

Why it works: the qualification is retained because it materially limits interpretation.

## Example 4: Ambiguous spreadsheet metric

### Extracted cells

```text
Sheet: Forecast
B2: Revenue | C2: 1.4 | D2: 2.1
B3: Growth  | C3: 18  | D3: 24
```

### Good decomposition

The sheet appears to forecast revenue and growth but does not expose currency, scale, percentage signs, periods, or whether columns C and D represent scenarios or years. The numbers must be preserved as displayed but cannot be safely interpreted.

Useful question: “What units and periods apply to cells C2:D3?” This resolves whether `1.4`, `2.1`, `18`, and `24` represent money, percentages, counts, or another measure.

### Bad output

> Revenue grows from $1.4M to $2.1M while growth rises from 18% to 24%.

Why it fails: currency, scale, percentage units, and time periods were invented.

## Example 5: Partially unreadable source

### Situation

Pages 1-8 of a 12-page PDF contain readable text. Pages 9-12 are image-only appendices referenced by the financial conclusion, and no reliable vision capability is available.

### Correct behavior

Begin with an incomplete status. Explain that the main text was read but the appendices supporting the financial conclusion were not. Do not claim that the financial argument is supported. Identify pages 9-12 as the missing scope.

## Anti-patterns

### Generic summary

> The document outlines an innovative strategy designed to improve efficiency and drive growth.

Fails because it reproduces plausible abstraction without concrete actors, mechanisms, evidence, or constraints.

### Synonym replacement

> “Operational leverage” means “better operational efficiency.”

Fails because it replaces jargon with another abstraction rather than explaining what changes in work, cost, throughput, or responsibility.

### Invented completion

> The six-person team is sufficient because modern agent frameworks reduce development time.

Fails unless the source supplies that mechanism and evidence.

### Boilerplate questions

> What are the next steps? Who are the stakeholders? What are the risks?

Fails because the questions are not tied to a specific ambiguity in the source.

### Author judgment

> The writer is hiding weak thinking behind AI-generated corporate language.

Fails because Understand evaluates source support, not the author or authorship method.
