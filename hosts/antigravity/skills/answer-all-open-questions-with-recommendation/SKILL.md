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

It runs **inline and dispatches no agent**: you are the single writer of this run, recording
every answer yourself, in this conversation, one question at a time in the order the tool gives
you, each answer committed before the next question is touched. You record **every pick as
given** and never judge it — a pick is never re-weighed, replaced, or skipped on its merits.
Every gather, order, re-check, and change of `open_questions.xml` is a call to the plugin's
open-question tool; the one whole read of the document with the file-reading tool (step 2) is
for reasoning only. It requires **no** clean-working-tree precondition: every commit is
path-scoped to the milestone's two files.

## Usage

```
/answer-all-open-questions-with-recommendation
```

Takes no arguments — it sweeps every `<open-question>` block in the current milestone's
`open_questions.xml` that contains a `<recommendation>` element.

## Workflow

### 0. Find the current milestone, once

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use
a hardcoded path. Resolve it **once per run** and hold it: every tool call, every recorded
answer, and every commit below uses this one directory, the one the run walked.

### 1. Gather the order with one `walk` call

Run

```
python3 .agents/plugins/cairn/tools/open_questions.py walk <MILESTONE_DIR>
```

It prints one line per `<open-question>` block that carries a `<recommendation>` element — the
block's `id` (its Short Title), bare — each block placed after every printed block its
`<depends-on>` tags name. That one call is the whole gather and the whole ordering: never read
`open_questions.xml` to gather or to order. Recommendation-less blocks are not printed.

If the call prints nothing, no block carries a `<recommendation>` element: print the no-op line
(step 5) and stop. If it fails, its one `Error: <reason>` line on stderr is the report: print it
and stop.

You walk this printed order **exactly once** (step 3). There is **no** outer re-gather loop:
recording only removes blocks or strips their picks, so the order never gains a question under
you.

### 2. Read the whole set once, for reasoning only

Read `<MILESTONE_DIR>/open_questions.xml` and `<MILESTONE_DIR>/requirements.md` **whole**,
once, with the file-reading tool. This snapshot gives every recording in step 3 its view of the
sibling questions and the decisions already recorded — the view the answer core's analyse step
and the contradiction advisory reason over — so no question pays for its own re-read.

The snapshot is context, never a source of truth for the loop. It never gathers, orders,
re-checks, or confirms a skip: the `walk` call gathered and ordered, and each question's `lift`
call (step 3a) is its re-check and its skip. Once a cascade lands, the snapshot is stale for
what it touched, so within step 3 the answer core's `locate` print of the block and the live
`requirements.md` take precedence over it.

### 3. Record each question in order, one commit per answer

For each Short Title in the gathered order, in turn:

**a. Record it through the shared procedure, from its lift step.** Read and follow
`.agents/plugins/cairn/shared/answer-with-recommendation-procedure.md`, carrying out its steps
yourself, with the `<MILESTONE_DIR>` from step 0 and this Short Title as its `MILESTONE_DIR` and
`SHORT TITLE` inputs. It lifts the block's recommendation with one `lift` call — the only lift
this question gets — and delegates the recording to
`.agents/plugins/cairn/shared/answer-procedure.md` (locate, analyse, fold, remove with the lifted
option passed verbatim, cascade).

- **The lift fails** — one `Error:` line, the procedure's no-recommendation guard stopping
  without changing anything: an earlier answer's cascade removed this block as moot or stripped
  its pick, and a stripped block is the recommendation pass's to re-pick. **Skip it silently**
  and move on to the next Short Title: report nothing, keep no record of it, and do not read the
  document to confirm it — the failing call is the re-check and the skip in one.
- **The lift succeeds** — it prints one line, "`<option>` — `<rationale>`". **Hold that line
  as this question's commit body** for **b**: once the answer is recorded the block is gone, so
  this print is the only place to take it from. Then carry the procedure through to its end.

In the answer core's analyse step you record the pick as given, whatever you conclude.
Its question of whether the answer contradicts or supersedes anything already written is the
one place this run notices a **contradiction**: when the pick runs against an entry in the live
`## Decisions` section at fold time — one that stood before the run or one this run recorded
earlier — record the pick anyway and hold the pair, this question's Short Title and the heading
of the `## Decisions` entry it conflicts with, for step 5. Never check a pick against another
block's standing recommendation the run has not yet reached. A new open question the decision
may raise is not reported and never added: it is the next `/review-milestone-requirements`
pass's to find.

**b. Commit this answer before the next question.** Read and follow the shared commit
procedure at `.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself,
with these three inputs:

- **PATHS** — `<MILESTONE_DIR>/open_questions.xml` and `<MILESTONE_DIR>/requirements.md`, the
  two files the recording changed.
- **SUBJECT** — exactly `Recommendation-answer: <Short Title>` (the answered question's
  handle), the subject that marks an accepted recommendation for
  `/capture-milestone-principle-updates`.
- **BODY** — the line the `lift` call printed in **a**, verbatim.

That procedure owns the path-scoped staging (never `git add -A`), the dirty-own-path no-op
guard, and the commit. Commit **once per answer**: one commit per recorded question is what
lets a single answer be reverted and re-answered on its own. Then continue with the next Short
Title.

**c. Stop the whole run on a tool failure after the fold.** When any tool call fails once this
question's decision has been folded into `requirements.md` — its `remove`, or a cascade
`remove` of a mooted entry — **stop the run at once**: report this question's Short Title with
the tool's `Error:` line quoted verbatim, commit nothing for it, and touch no further question.
Leave the question's uncommitted edits in the working tree exactly as they are — no rollback,
no snapshot restore, no skip-and-continue, and never a change to `open_questions.xml` outside
the tool to undo them. Every earlier answer is already committed, so what remains is the
recorded decision with its block still standing (or with a partial cascade): a resumable tree,
and stopping is what keeps that stranded fold out of the next answer's commit. The lifted
option is passed to `remove` verbatim and never corrected. A failure of any other tool call of
the procedure after a successful lift stops the run the same way.

### 4. Check completeness with one end-of-run `walk`

When the gathered order is exhausted, run the same call once more:

```
python3 .agents/plugins/cairn/tools/open_questions.py walk <MILESTONE_DIR>
```

A single pass either records a block or finds it removed or stripped by a cascade, so this
call is expected to print nothing. Any id it prints is an **anomaly** — a
recommendation-bearing block the run left unrecorded — held for step 5 as it was printed. This
check never records, lifts, or re-walks those ids, never names a skipped question, and reads no
document. If the call fails, hold its `Error:` line for step 5 in the same place.

### 5. Report

On the success path print exactly one fixed terse status line for the whole run, with no
identifier and no count:

```
Recommendations recorded.
```

when at least one answer was committed. When the run committed nothing — `walk` printed nothing
in step 1, or every question's lift failed — print instead one distinct line stating that
nothing was recorded and briefly why.

Beside that line print only these two advisories, each only when it fired, since git records
neither:

- **Contradictions** — one advisory naming each pair held in step 3a: the answered question's
  Short Title and the `## Decisions` heading it conflicts with, one pair per line. Nothing in
  the commit records which decision a folded answer conflicts with, and it is what a
  revert-then-re-answer needs.
- **Completeness anomaly** — each id the step-4 `walk` printed (or its `Error:` line), stated
  as a recommendation-bearing block the run left unrecorded.

Print nothing else: no skipped question is named, no new-question advisory is given, no
recommendation-less block is enumerated, and no recorded answer is re-narrated — the commits
are the record. On a step-3c stop, the stop report (the Short Title and the tool's `Error:`
line) replaces the status line, with any contradiction pairs already held printed beside it.
