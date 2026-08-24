# Finding the bedrock

An explanation anchored in first principles starts from the smallest true things and builds up. This reference says how to find those things and how to build from them without inventing.

## What bedrock is

A bedrock fact is one that:

- cannot be broken into smaller facts without losing meaning;
- something in the file stands on, so that if it were false the file would be pointless or wrong;
- a reader with no background can accept on first read.

Bedrock is usually one of three kinds:

- **A fact about the world.** Computers lose connections. Memory is limited. Money left in an account grows when the bank adds to it.
- **A constraint.** The whole request must finish within ten seconds. The cache holds at most twenty items. Only the payroll team may see this table.
- **A goal.** Do not charge a card twice. Answer faster the second time. Catch a broken build before it is merged.

## Finding it: take apart, sort, keep

**Take apart.** Read the file and ask of its main mechanism: what has to be true for this to make sense? Write each answer down. Then ask of each answer: what has to be true for that? Stop when the next answer is something the reader already knows, or when the file gives nothing further.

**Sort.** Mark each fact:

- stated in the file;
- true everywhere, not just here;
- assumed by the file but never stated.

Facts the file states carry no label. The other two get their label in the output, in plain words.

**Keep.** Two to five facts. Drop any fact that nothing in the file stands on. Drop any fact that is only a restatement of another. If more than five remain, the file has more than one main path; pick the path the file itself treats as primary and mention that other paths exist.

## Building up

Order the steps so that each one rests only on the bedrock and the steps before it. The test for each step is: which earlier fact does this stand on? If the answer is "none yet", the step is out of order or a bedrock fact is missing.

Write each step as one plain sentence. A step that needs two sentences is usually two steps.

The build is finished when the reader can follow the file's main path from its input to its result. It is not finished when every line of the file has been mentioned.

## What first principles do not mean

- Not "explain the physics of everything". Bedrock is the smallest fact the file needs, not the smallest fact that exists. A retry policy rests on "connections fail sometimes", not on how networks work.
- Not "add what the author should have said". A missing reason stays missing. Write that the file does not say why.
- Not "reason by analogy". An analogy can illustrate a step after the step is stated plainly. It cannot be the step.

## Two worked examples

**A retry policy.** The file says: try again twice after a failure, wait one second then two, do not retry most client errors, ten-second deadline overall. Bedrock: a request can fail for a moment and then work (true everywhere); a request that failed because it was wrong will fail the same way again (true everywhere); the whole thing must finish in ten seconds (stated). Build: send the request; if it fails for a passing reason, wait one second and try again; if that fails, wait two seconds and try a last time; if it fails because the request was wrong, stop at once; whatever happens, stop at ten seconds.

**A cache.** The file is a class that stores up to N items and drops the least recently used one when full. Bedrock: memory is limited (true everywhere); things asked for recently tend to be asked for again (the file assumes this but does not say it); the store may hold at most N items (stated). Build: when something is asked for, look in the store first; if it is there, hand it back and mark it as fresh; when something new is stored and the store is full, throw out the item nobody has touched for the longest time.
