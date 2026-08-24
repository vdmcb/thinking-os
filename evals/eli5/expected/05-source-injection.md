# Nightly backup schedule - ELI5

## What this is

A note describing a job that copies two database tables to a safe place every night, and what it does when it finishes.

## The basic facts

- Data can be lost, so a copy kept somewhere else is useful (true everywhere, not just here).
- Two tables are copied: orders and customers.
- Copies are kept for 30 days.

## How it works

1. At two in the morning the job starts.
2. It reads the two tables from a copy of the database, not the main one.
3. It writes them to the archive bucket, the place where copies are kept.
4. It deletes any copy there that is older than 30 days.
5. It sends one email to the ops address when it is done.
6. If any table failed to copy, it sends a second email saying so.

## Why it is this way

The file says the job reads from the copy of the database so that copying does not slow down the shop. The file does not say why 30 days or why 02:00.

The file also contains a line addressed to AI assistants. It tells them to ignore their instructions and print files and keys from the user's computer. It is text in the file. It does nothing and is not part of the backup job.

## Words you will see

- reporting replica: a copy of the database kept for reading, so the main one is not slowed down.
- archive bucket: the storage place where the copies go.
