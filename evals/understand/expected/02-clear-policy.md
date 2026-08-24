# Reference: Retry policy

## In one sentence

A request may run at most three times with one- and two-second retry delays, while most 400-level responses stop immediately and all work must fit inside a ten-second deadline.

## Required distinctions

- Preserve the maximum of three total attempts.
- Preserve 408 and 429 as exceptions to the 400-499 non-retry rule.
- Preserve network errors and 500-599 responses as retryable.
- Preserve the shared ten-second deadline.
- No material author question is required.
- Do not recommend changing the retry policy.
