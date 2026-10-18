---
name: answer-all-open-questions-with-recommendation
description: Record the embedded recommendation as the answer for every question in the current milestone that carries one, reasoning over the whole set inline.
---

# answer-all-open-questions-with-recommendation

This is the batch path that records every open question's **embedded recommendation** as its
answer, unattended. The recommendation pass (`/recommend-all-open-questions`) annotates each
question by embedding a `<recommendation>` element in its `<open-question>` block in the current
milestone's `open_questions.xml`; this skill walks the blocks that carry one and records each
pick — the decision lands under `## Decisions` of `requirements.md` and the answered block leaves
`open_questions.xml` — one commit per answer, leaving recommendation-less blocks untouched
(annotating them is the recommendation pass's job, not this one's).

It runs **inline and dispatches no agent**: you are the single writer of this run, composing
every answer yourself, in this conversation, and recording the whole run in **one fixed
batched shell call** (step 3) that takes the questions in the order the tool gives you and
commits each answer before the next question is touched. You record **every pick as given**
and never judge it — a pick is never re-weighed, replaced, or skipped on its merits.
Every gather, order, view, re-check, and change of `open_questions.xml` is a call to the
plugin's open-question tool, every change of `requirements.md` is a call to its fold tool, and
this run edits neither document by hand; `open_questions.xml` is never read with the
file-reading tool: the gather, the order, and the view of it are one fixed shell call (step 1).
Every tool call the run makes — this skill's own, those inside step 1's loop and step 3's
sections included — is written out in full as its fenced block shows it, never through a
variable, alias, or function of your own defined to stand for the command or any part of it.
`requirements.md` is read whole once with the file-reading tool, in the same turn as step 1's
call (step 2), for reasoning only. It requires **no** clean working tree beyond the milestone's
two files: step 3's call stops before any write while either of them holds a change, and every
commit is path-scoped to them, so a dirty tree elsewhere stays out of it.

## Usage

```
/answer-all-open-questions-with-recommendation
```

Takes no arguments — it sweeps every `<open-question>` block in the current milestone's
`open_questions.xml` that contains a `<recommendation>` element.

## Workflow

### 0. Find the current milestone, once

Follow `${PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use
a hardcoded path. Resolve it **once per run** and hold it: every tool call, every recorded
answer, and every commit below uses this one directory, the one the run walked.

### 1. Gather, order, and view the questions in one fixed shell call

Run this one fixed shell call, written out in full exactly as shown, with only
`<MILESTONE_DIR>` replaced:

```
python3 ${PLUGIN_ROOT}/tools/open_questions.py list --with-question <MILESTONE_DIR> &&
python3 ${PLUGIN_ROOT}/tools/open_questions.py walk <MILESTONE_DIR> | while IFS= read -r id; do
  printf '%s\n' "$id"
  if pick="$(python3 ${PLUGIN_ROOT}/tools/open_questions.py lift <MILESTONE_DIR> "$id" 2>&1)"; then
    printf '%s\n' "$pick"
    python3 ${PLUGIN_ROOT}/tools/open_questions.py lift --alternative "${pick%% — *}" <MILESTONE_DIR> "$id"
  else
    printf '%s\n' "$pick"
  fi
done
```

Its `list --with-question` prints every `<open-question>` block in document order, one line
each: the block's `id` (its Short Title), a tab, and its `<question>` text —
recommendation-less blocks included. Its `walk` then yields the `id` of every block that
carries a `<recommendation>` element, each placed after every yielded block its `<depends-on>`
tags name, and for each one in that order the loop prints three lines: the `id`, bare; the
block's lifted line, "`<option>` — `<rationale>`"; and the picked alternative's line,
"`<option>` — `<what-it-is>`", lifted with the option taken from the held line as its text
before the first spaced em dash. A walked `id` whose lift fails is followed by that lift's
`Error:` line in place of the pick and by no alternative line: it has no pick to record and
gets no section in step 3's call. `id` and `pick` are each one quoted value per walked
question, set and used within this one call, never a tool command or a path list.

That one call is the whole gather, the whole ordering, and the whole view of the question
document: never read `open_questions.xml` with the file-reading tool, to gather, to order, or
to reason over. The walked ids, in the order printed, are the run's order; a block printed only
in the tab-separated lines carries no `<recommendation>` and is left untouched.

If the call prints no walked id — nothing after the tab-separated lines, or nothing at all — no
block carries a `<recommendation>` element: print the no-op line (step 4) and stop. If it
prints an `Error: <reason>` line that follows no walked id, the gather itself failed and that
line is the report: print it and stop.

You walk this printed order **exactly once** (step 3), and this call is never run again to
re-check a question or confirm a skip: each section's own `lift` in step 3's call is its
question's re-check and its skip. There is **no** outer re-gather loop: recording only removes
blocks or strips their picks, so the order never gains a question under you.

### 2. Read `requirements.md` whole, in the same turn as step 1's call

Read `<MILESTONE_DIR>/requirements.md` **whole**, once, with the file-reading tool, never
through shell output. Neither this read nor step 1's call needs the other's output, so send
the two in the same turn, as two independent tool calls.

This read and step 1's print are the context every section of step 3 is composed from — the
decisions already recorded and their `###` subsections, and each question's text and pick — so
no question pays for its own re-read. Write each question's decision from its question text,
its lifted line, and its picked alternative's what-it-is line, as the view printed them.

### 3. Record every question in one batched shell call

**a. Compose each question's section.** For every walked `id` step 1 printed with a pick, in
the printed order, decide three values before writing the call:

- **The decision** — the statement folded under `## Decisions`, written by the rules
  `${PLUGIN_ROOT}/shared/answer-procedure.md` sets in its fold step (step 3) for what a
  decision says and the shape its entry takes in the subsection it lands in. To decide what it
  says, ask only the first two questions of that procedure's analyse step (step 2) — whether
  the pick resolves the question completely, and what constraint it imposes — and record the
  pick as given whatever you conclude. Its other two questions are not this run's: the run
  carries no cascade, so an entry a decision moots stays in the document for the next
  `/review-milestone-requirements` pass to clean up or flag, and it forms no contradiction
  judgment, since that pass's `## Decisions` consistency step is where a conflicting pair is
  noticed. A new open question the decision may raise is not reported and never added: it is
  that pass's to find. That procedure's tool steps are never followed: this call runs the fold,
  the removal, and the commit.
- **The heading** — the `###` subsection under `## Decisions` the decision lands in, the one
  that fits it among those step 2's read shows, or a new heading where none fits; the fold
  tool folds into the subsection whose heading matches after whitespace and case folding, and
  creates a new heading's subsection at the end of `## Decisions`.
- **The option** — the text of the question's lifted line before its first spaced em dash (the
  whole line when there is none), copied from step 1's print as a literal: the option reaches
  `remove` as an exact id, never derived in the call and never corrected.

**b. Run the call.** Run this one fixed shell call, written out in full exactly as shown, with
only `<MILESTONE_DIR>` and each question section's `<Short Title>`, `<Heading>`, decision, and
`<Option>` replaced:

```
if [ -n "$(git status --porcelain -- <MILESTONE_DIR>/open_questions.xml <MILESTONE_DIR>/requirements.md)" ]; then
  echo 'dirty before start'
  git status --porcelain -- <MILESTONE_DIR>/open_questions.xml <MILESTONE_DIR>/requirements.md
  false
fi &&
if pick="$(python3 ${PLUGIN_ROOT}/tools/open_questions.py lift <MILESTONE_DIR> "<Short Title>" 2>/dev/null)"; then
  python3 ${PLUGIN_ROOT}/tools/requirements.py fold <MILESTONE_DIR> --section "<Heading>" <<'EOF' &&
<the decision>
EOF
  python3 ${PLUGIN_ROOT}/tools/open_questions.py remove <MILESTONE_DIR> "<Short Title>" --option "<Option>" &&
  if [ -n "$(git status --porcelain -- <MILESTONE_DIR>/open_questions.xml <MILESTONE_DIR>/requirements.md)" ]; then
    git add <MILESTONE_DIR>/open_questions.xml <MILESTONE_DIR>/requirements.md && git commit -q -m "Recommendation-answer: <Short Title>" -m "$pick" && echo 'answer commit landed'
  fi ||
  { printf 'stopped at\t%s\n' "<Short Title>"; false; }
fi &&
echo 'completeness walk' &&
python3 ${PLUGIN_ROOT}/tools/open_questions.py walk <MILESTONE_DIR>
```

**The question section** — the lines from `if pick=` through the column-0 `fi &&` that closes
it — is written once per question composed in **a**, every one in the one call however many
there are, with no cap and no splitting, in step 1's printed order and never reordered: `walk`
places each block after the blocks its `<depends-on>` tags name, so every commit that lands
records a pick whose assumed siblings are already recorded. Each copy carries that question's
Short Title in its four places, its heading after `--section`, its decision between the
`<<'EOF'` line and the `EOF` line (the delimiter is quoted so nothing inside is expanded; pick a
delimiter line the decision does not contain), and its option after `--option`. Every Short
Title, heading, and option is written inside double quotes, with any `"`, `$`, `` ` ``, or `\`
it holds escaped by a backslash. The lines before the first section and the lines from
`echo 'completeness walk'` to the end are written once.

The call's first lines are the **stranded-fold guard**: when either milestone file holds any
staged or unstaged change, whatever its origin — a fold a stopped run left uncommitted, or a
hand edit — the call prints `dirty before start` and the `git status --porcelain` lines beneath
it, then ends before any lift, fold, removal, or commit, so no leftover rides into an answer's
commit.

In each section the `lift` is the question's re-check against the live document, with only its
stderr silenced. When it fails — an earlier section's `remove` stripped this block's pick,
because its `<depends-on>` assumed an option other than the one recorded — the section does
nothing and prints nothing: that is the **silent skip**, kept in no record and confirmed by no
read, the stripped block being the recommendation pass's to re-pick. When it succeeds, its one
line, "`<option>` — `<rationale>`", is held in `pick` as the commit body, since once the answer
is recorded the block is gone. Then the fold tool splices the decision verbatim at the end of
the `<Heading>` subsection of `## Decisions`, so the recorded decision always lands before the
block is removed; `remove` deletes the block with `--option` naming the recorded option and, in
the same write, strips the pick of every block whose `<depends-on>` assumed another option of
it, keeping their alternatives; and the section carries out the three steps of the shared
commit procedure at `${PLUGIN_ROOT}/shared/commit-procedure.md` itself — its dirty-own-path
guard, the path-scoped `git add` of the two milestone files (never `git add -A`), and the
commit under `Recommendation-answer: <Short Title>` with the held line as its body through the
procedure's second `-m` form — with git's success output silenced and `answer commit landed`
printed once the commit has landed. One commit per answer is what lets a single answer be
reverted and re-answered on its own. `pick` is one quoted value per section, set at the
section's first line and used within it, never a tool command or a path list; no shell variable
carries anything from one section to the next.

A **stop**: when the fold, the `remove`, or a git step fails after a successful lift — the fold
tool refusing, `remove` refusing the option, git refusing the commit — the failing command's
own `Error:` line or git's message reaches the output unredirected, the section prints
`stopped at`, a tab, and the Short Title, and the call ends there: no later section and no
completeness walk runs. The tree is left exactly as it stands — no rollback, no restore, no
skip-and-continue, and never a change to `open_questions.xml` outside the tool — so every
earlier answer is committed and only this question is unfinished: clean when the fold was
refused, its decision folded and uncommitted with its block still standing when a later step
failed. That stop is what keeps a stranded fold out of the next answer's commit.

After the last section the call prints the fixed header line `completeness walk` and runs the
tool's `walk` once more as the completeness check. A single pass either records a block or
finds its pick stripped by an earlier section's `remove`, so this walk is expected to print
nothing; any id it prints is an **anomaly** — a recommendation-bearing block the run left
unrecorded. The check never records, lifts, or re-walks those ids and names no skipped
question.

What the call prints is the whole outcome:

- **`dirty before start`**, with `git status --porcelain` lines beneath it — nothing ran.
- **`answer commit landed`** — one per committed answer.
- **`stopped at`, a tab, and a Short Title**, beside the `Error:` line or git message printed
  just before it — the run stopped at that question.
- **`completeness walk`** — the call reached its end; every line after it is an id the walk
  printed, or its `Error:` line.

A skipped question prints nothing at all. Hold these lines for step 4.

### 4. Report

On the success path print exactly one fixed terse status line for the whole run, with no
identifier and no count, chosen by the call's markers:

```
Recommendations recorded.
```

when step 3's call printed at least one `answer commit landed`. When the run committed nothing
— step 1 printed no walked id, or the call reached its `completeness walk` line with no marker
before it because no section's lift succeeded — print instead one distinct line stating that
nothing was recorded and briefly why.

Beside that line print only the **completeness anomaly**, when it fired, since git records it
nowhere: each line the call printed after `completeness walk` (an id, or the walk's `Error:`
line), stated as a recommendation-bearing block the run left unrecorded.

Print nothing else: no skipped question is named, no contradiction or new-question advisory is
given, no recommendation-less block is enumerated, and no recorded answer is re-narrated — the
commits are the record.

Two stops replace the status line:

- **Dirty start** — the call printed `dirty before start`: report that the run recorded nothing
  because the milestone's own files already held changes, print the porcelain lines the call
  printed beneath it verbatim, and give the remedy — commit or discard those changes, then
  re-run this skill.
- **Stopped at a question** — the call printed `stopped at`, a tab, and a Short Title: report
  that Short Title paired with the `Error:` line or git message printed beside it, quoted
  verbatim, a multi-line git message whole. Every answer before it is committed; whatever this
  question left uncommitted in the two files stays as it is, and the next run's guard stops on
  it until it is committed or discarded.
