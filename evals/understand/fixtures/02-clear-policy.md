# Retry policy

A request is attempted once and may be retried twice. Retry delays are one second and two seconds. HTTP 400-499 responses are not retried, except 408 and 429. All attempts and delays share a ten-second request deadline. Network errors and HTTP 500-599 responses are retryable.
