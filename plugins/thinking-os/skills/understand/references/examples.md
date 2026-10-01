# Examples and anti-examples

These examples demonstrate behavior, not fixed wording.

## Example 1: proposal with weak support

### Source excerpt

> Our AI-native transformation layer will unlock operational leverage across the enterprise. A six-person team can deliver the platform in two quarters, reducing processing costs by 40% and creating a durable strategic moat.

### Good output shape

```text
Stance: Negative on evidentiary readiness. The staffing, schedule, and savings are source claims without a visible mechanism or supporting measurement.
Q1: How well supported is the promised 40% processing-cost reduction?
A: The excerpt states the reduction but gives no current cost baseline, included process, calculation, or observed result.
Q2: Does the excerpt support committing to the proposed platform?
A: It defines the desired commitment as six people for two quarters but does not establish that this team and schedule can deliver the undefined platform or savings.
Q3: What would the commitment require?
A: Six people for two quarters. Cost, role mix, scope, dependencies, and ownership are not stated.

## Follow-up questions

1. Which current processing-cost baseline and calculation produce the 40% reduction?
2. What functions are included in the "platform," and which six roles deliver them within two quarters?
3. What observable condition would make the claimed strategic advantage durable rather than reproducible by competitors?

Held: the claim chain behind the six-person, two-quarter plan, the evidence gap behind the 40% reduction, and the strategic-advantage premise. Ask for any of them.
```

Why it works: the stance is scoped, the three answers preserve the source's silence, each follow-up requests something specific, and the held line names the deeper analysis available on request.

### Bad output

> The company should start with a smaller pilot because the proposed transformation is too ambitious.

Why it fails: it introduces a recommendation and judgment instead of explaining the source.

## Example 2: clear technical material

### Source excerpt

> Requests are retried twice after the initial attempt, with exponential delays of one and two seconds. HTTP 400-499 responses are not retried except 408 and 429. The total request deadline is ten seconds.

### Good handling

- The state answer says a request can run at most three times.
- It preserves one-second and two-second delays, 408 and 429 exceptions, and the shared ten-second deadline.
- The decision answer explains the policy as written without recommending a change.
- The resource answer says implementation ownership and monitoring are not stated if those points matter to the user's context.
- Follow-ups target only real semantic boundaries, such as whether backoff time counts toward the ten-second deadline and what happens when that deadline expires.

Why it works: every threshold and exception survives, and the required follow-ups deepen understanding without inventing a defect.

## Example 3: caveat changes the headline

### Source excerpt

> The pilot increased conversion from 8% to 12%. The treatment group contained 220 existing customers selected by account managers. New customers and self-serve accounts were excluded.

### Good handling

The state answer reports a four-percentage-point increase over the pilot period among 220 account-manager-selected existing customers. It does not call the increase causal or generalize it to new and self-serve customers. The decision answer says the source does not establish a broader rollout effect. Follow-ups ask for a control comparison, selection criteria, and evidence from the excluded populations.

Why it works: the qualification is retained because it materially limits interpretation.

## Example 4: ambiguous spreadsheet metric

### Extracted cells

```text
Sheet: Forecast
B2: Revenue | C2: 1.4 | D2: 2.1
B3: Growth  | C3: 18  | D3: 24
```

### Good handling

The state answer says the sheet displays revenue values 1.4 and 2.1 and growth values 18 and 24, but does not expose currency, scale, percentage signs, periods, or what columns C and D represent. The follow-ups ask for those exact definitions and the formulas behind the displayed values.

### Bad output

> Revenue grows from $1.4M to $2.1M while growth rises from 18% to 24%.

Why it fails: currency, scale, percentage units, time periods, and direction were invented.

## Example 5: partially unreadable source

### Situation

Pages 1-8 of a 12-page PDF contain readable text. Pages 9-12 are image-only appendices referenced by the financial conclusion, and no reliable vision capability is available.

### Correct behavior

Begin with `Status: Incomplete.` State that the main text was read but the appendices supporting the financial conclusion were not. Do not assign a confident stance to that conclusion. Identify pages 9-12 as the missing scope, and make any affected follow-up question an extraction limitation rather than imagined author silence.

## Anti-patterns

### Generic summary

> The document outlines an innovative strategy designed to improve efficiency and drive growth.

Fails because it reproduces abstraction without concrete actors, mechanisms, evidence, constraints, or a scoped stance.

### Bare stance

> Stance: Positive.

Fails because it hides what is positive and on what evidence.

### Synonym replacement

> "Operational leverage" means "better operational efficiency."

Fails because it replaces jargon with another abstraction rather than explaining what changes in work, cost, throughput, or responsibility.

### Invented completion

> The six-person team is sufficient because modern agent frameworks reduce development time.

Fails unless the source supplies that mechanism and evidence.

### Boilerplate follow-ups

> What are the next steps? Who are the stakeholders? What are the risks?

Fails because the questions are not tied to a source-specific claim or unknown.

### Repeated questions

> Q2: Should we release?
>
> Follow-up question 1: Should we release?

Fails because follow-ups must advance beyond the three answered stakeholder questions.

### Author judgment

> The writer is hiding weak thinking behind AI-generated corporate language.

Fails because Understand evaluates source support, not the author or authorship method.
