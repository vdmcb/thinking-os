# Retry policy for the payments client

Requests are retried twice after the initial attempt, with exponential delays of one and two seconds. HTTP 400-499 responses are not retried except 408 and 429. The total request deadline is ten seconds, including waits.

Retries are disabled for `POST /charges` because a duplicate charge is worse than a failed one.
