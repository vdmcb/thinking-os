# Finding the bedrock

An explanation anchored in first principles starts from the smallest true things the subject rests on and builds up. This reference gives the tests and worked examples; the procedure itself is in SKILL.md step 4.

## What bedrock is

A bedrock fact:

- cannot be broken into smaller facts without losing meaning;
- has something in the file standing on it, so that if it were false the file would be pointless or wrong;
- can be accepted by a reader with no background on first read.

Three kinds: a **fact about the world** (computers lose connections; memory is limited; a company that loses customers loses money), a **constraint** (the whole request must finish within ten seconds; the store holds at most twenty items), a **goal** (do not charge a card twice; answer faster the second time; catch a broken build before it is merged).

Three sources, and the label each carries in the output: stated in the file (no label); general knowledge, not from the file; assumed by the file but never stated.

## Tests

- **Is it smaller?** If the fact can be split into two facts the file needs separately, split it.
- **Does anything stand on it?** Name the step or claim that would fall if it were false. If nothing would, drop it.
- **Is it a claim?** A claim is something the file asserts and asks the reader to accept (a saving, a result, a market size). It is not bedrock. What the claim rests on may be: the goal it serves, the world fact it needs.
- **More than five?** The subject has more than one main path. Take the one the file treats as primary and hold the others.

## Building up

Order the steps so that each rests only on the bedrock and the steps before it. For each step ask: which earlier fact does this stand on? "None yet" means the step is out of order or a bedrock fact is missing. One sentence per step; a step that needs two is two steps. The build is finished when the reader can follow the main path from input to result, not when every line of the file has been mentioned.

## What first principles do not mean

- Not "explain the physics of everything". Bedrock is the smallest fact the file needs, not the smallest fact that exists. A retry policy rests on "connections fail sometimes", not on how networks work.
- Not "add what the author should have said". A missing reason stays missing.
- Not "reason by analogy". An analogy can illustrate a step after the step is stated plainly. It cannot be the step.

## Worked examples

**A mechanism (retry policy).** The file: try again twice after a failure, wait one then two seconds, do not retry most client errors, ten-second deadline. Subject: the retry rule. Bedrock: a request can fail for a moment and then work (general knowledge); a request with a mistake in it fails the same way each time (general knowledge); the whole thing must finish in ten seconds (in the file). Build: send; on a passing failure wait one second and resend; on a second failure wait two seconds and send a last time; on a client mistake stop at once; stop at ten seconds regardless.

**Code (a cache class).** The file: a class holding up to N items, dropping the least recently used when full. Subject: the class. Bedrock: memory is limited (general knowledge); the store may hold at most N items (in the file); things asked for recently tend to be asked for again (assumed, not said). Build: on a request, look in the store; if present, return it and mark it fresh; on a store when full, drop the item untouched longest.

**A proposal (a slide deck asking for money).** The file: a deck proposing a new service, with a team, a price, and a projected result. Subject: the proposed service, not the deck. Bedrock: the company earns money today by selling hours, so it grows only by hiring (in the file); a business that charges a fixed fee earns whether or not it works more hours (general knowledge); the deck says buyers want a predictable bill (in the file, a claim the deck cites a survey for). "How it works" describes how the service would run: who is sold to, what is set up, what is charged. The projected result is a number on the main path and enters with its label as the deck's projection. If the deck gives no mechanism between the plan and the result, the steps say so in one sentence rather than describing the slides.

**A config (a CI workflow).** The file: a YAML file that runs a check script on every push. Subject: the file. Bedrock: code can break without the author noticing (general knowledge); the host can start a fresh machine and run commands when code arrives (general knowledge); the checks live in one script (in the file). Build: code arrives; a machine starts; it fetches the project; it installs what the file names; it runs the script. The file's choices (machine type, time limit, tool version) are numbers on the main path; their reasons are absent, and the Why section says so.
