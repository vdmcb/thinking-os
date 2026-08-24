# Retry policy for the payments client - ELI5

## What this is

A short rule for a program that talks to a payment service. It says what to do when a request to that service fails.

## The basic facts

- A request can fail for a moment and then work if sent again (true everywhere, not just here).
- A request that was wrong will fail the same way every time it is sent (true everywhere, not just here).
- The whole attempt, waits included, must finish within ten seconds.
- Charging a card twice is worse than not charging it at all.

## How it works

1. The program sends the request.
2. If it fails, the program waits one second and sends it again.
3. If that fails too, it waits two seconds and sends it a last time, so three tries at most.
4. If the answer says the request itself was wrong (a code from 400 to 499), the program stops at once instead of trying again.
5. Two of those codes, 408 and 429, are the exception: they are treated as passing failures and retried.
6. Whatever happens, the program stops when ten seconds have passed.
7. For one request, the one that charges a card, the program never retries.

## Why it is this way

The file says the charge request is never retried because a double charge is worse than a failed one. The file does not say why 408 and 429 are retried when the other codes are not.

## Words you will see

- HTTP 400-499: answer codes that mean the request itself had a mistake in it.
- POST /charges: the request that takes money from a card.
