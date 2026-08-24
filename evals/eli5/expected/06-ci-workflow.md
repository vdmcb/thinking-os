# Validate workflow - ELI5

## What this is

A set of instructions for GitHub. Every time someone sends new code to this project, GitHub starts a fresh computer and runs the project's checks on it.

## The basic facts

- Code can break without the person who changed it noticing (true everywhere, not just here).
- GitHub can start a temporary computer and run commands on it when code arrives (true everywhere, not just here).
- The project keeps its checks in one script, scripts/validate.sh.

## How it works

1. Someone pushes code, or opens a request to merge code.
2. GitHub starts a fresh Ubuntu computer for at most 15 minutes.
3. The computer downloads the project's files.
4. It installs Node.js version 20.
5. It runs the check script.
6. The computer is allowed to read the project, and nothing more.

## Why it is this way

The file does not say why the checks run on every push, why the limit is 15 minutes, or why Node.js 20 is needed. The file does not say what the check script does.

## Words you will see

- push: sending code to the project.
- pull_request: asking for code to be merged into the project.
- ubuntu-latest: the kind of computer GitHub starts.
- actions/checkout: the step that downloads the project.
