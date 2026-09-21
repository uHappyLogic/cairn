---
name: answer-all-open-questions-with-recommendation
description: Record the embedded recommendation as the answer for every question in the current milestone's requirements that carries one.
---

# answer-all-open-questions-with-recommendation

This is the batch path that records every open question's **embedded recommendation** as its
answer. The recommend sweep (`/recommend-all-open-questions`) annotates each question by embedding
a `<recommendation>` element in its `<open-question>` block in the current milestone's
`open_questions.xml`; this skill gathers the blocks that carry one and, for each, dispatches the
file-editing `answer-open-question-with-recommendation` agent to lift that recommendation and
record it — the decision lands under `## Decisions` of `requirements.md` and the answered block
leaves `open_questions.xml` — leaving recommendation-less blocks untouched (annotating them is the
recommend sweep's job, not this one's). It requires **no** clean-working-tree precondition.

It is an **orchestrator**. It does not record answers itself: for each recommendation-bearing
question it dispatches the agent, which lifts the `<recommendation>` element, folds the decision
into `## Decisions`, cascades to mooted siblings, and leaves those two edits **staged but
uncommitted**. The orchestrator **commits that staged index itself** — once per successful agent
return, before dispatching the next. Because every dispatch mutates the same two files,
`open_questions.xml` and `requirements.md`, the dispatches run **strictly sequentially, never in
parallel**. Every read this skill makes of `open_questions.xml` is a call to the plugin's
open-question tool — the `walk` in step 1 and the `lift` in step 2 — and it never reads or edits
that document itself.

## Usage

```
/answer-all-open-questions-with-recommendation
```

Takes no arguments — it sweeps every `<open-question>` block in the current milestone's
`open_questions.xml` that contains a `<recommendation>` element.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Gather the questions in dispatch order with one call

Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py walk <MILESTONE_DIR>
```

It prints the dispatch order: one line per `<open-question>` block that carries a
`<recommendation>` element, the block's `id` (its Short Title) bare, each block placed after every
printed block its `<depends-on>` tags name. That one call is the whole gather and the whole ordering —
never read `open_questions.xml` to gather or to order. Recommendation-less blocks are not printed:
annotating them is the recommend sweep's job (`/recommend-all-open-questions`), never this one's.

If the call prints nothing, no block carries a `<recommendation>` element: say so and stop. If it
fails, its one `Error: <reason>` line on stderr is the report: print it and stop.

You walk this printed order **exactly once** (step 2). **Do not wrap step 2 in an outer re-gather
loop** — there is no such loop, and adding one is a defect.

### 2. Walk the order once, dispatching the agent per surviving question

For each Short Title in the gathered order:

**a. Re-check with one `lift` call, and hold its print as the commit body.** Run

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py lift <MILESTONE_DIR> "<Short Title>"
```

If the call fails — one `Error:` line on stderr, exit 1 — **skip this question** and move on to
the next: an earlier answer's cascade has removed the block or stripped its embedded children, and
a stripped block is the recommend sweep's to regenerate, not this sweep's to answer. The failing
call is the re-check and the skip in one; do not read the document to confirm it.

If the call succeeds, it prints one line, "`<option>` — `<rationale>`" — the same answer text the
agent records. **Hold that line as this question's commit body** for **c**: the agent hands nothing
back, and once it has recorded the answer the block is gone, so this call is the only place to lift
it.

**b. Dispatch the file-editing agent.** Use the `Agent` tool with `subagent_type` set to the
namespaced registry name of the `answer-open-question-with-recommendation` agent under this
plugin's namespace, `cairn:answer-open-question-with-recommendation` — one dispatch per question.
Pass it the question's **Short Title** in the prompt:

```
Record the embedded recommendation for this open question as its answer.

Short Title: <Short Title>
```

Wait for the agent to return before dispatching the next one. **Dispatch strictly sequentially —
never in parallel**: every dispatch lifts, records, and cascades against the same
`open_questions.xml` and `requirements.md`, and you commit each answer between dispatches.

**c. Handle the agent's return.** The agent returns `DONE` or `FAILED: <reason>`:

- **`DONE`** — the agent recorded the answer and left its two edits,
  `<MILESTONE_DIR>/open_questions.xml` and `<MILESTONE_DIR>/requirements.md`, **staged but
  uncommitted**, returning no payload. **Commit that staged index now, before dispatching the next
  question** — stage nothing yourself (the agent already staged both paths by name, so never
  `git add` and never `git add -A`):
  - **No-op guard** — check whether anything is actually staged (for example
    `git diff --cached --quiet`). If nothing is, this answer produced no committable change: commit
    nothing, create no empty commit, and continue to the next question.
  - **Commit** — commit the staged index under exactly the subject
    `Recommendation-answer: <Short Title>` (the answered question's handle), with the line the
    `lift` call printed in **a** as the commit **body** — `git commit -m "<subject>" -m "<body>"`
    with no pathspec, since the staged index is exactly this answer's two edits.

  Commit once per answer — the per-answer granularity is the point. Then continue to the next
  question.
- **`FAILED: <reason>`** — stop the loop, report the question's Short Title and the failure
  reason, and stop. Do not commit anything for this question and do not dispatch any further
  questions. Treat it as a real failure to report-and-stop on, not a benign skip. **Never record
  the answer yourself as a fallback** — the agent owns all mutation.
- If the agent returns without an explicit `DONE` or `FAILED` status (returned early, produced no
  output, or gave an ambiguous result), treat it as `FAILED`: report what was returned, stop the
  loop, and do not dispatch further.

### 3. Report

On the success path, when the gathered order is exhausted, print exactly one fixed terse status
line for the whole run — `Recommendations recorded.` — and nothing more: no count of how many
recommendations were recorded and no pointer to review the commits.

If the sweep recorded nothing (no recommendation-bearing questions, or every one skipped, so nothing
was committed this run), do not print the terse success line; instead say so in one sentence — this
is the distinct one-line no-op message, kept separate from the terse success line.

Do **not** enumerate the untouched (recommendation-less) questions: they remain visible as
`<open-question>` blocks in `open_questions.xml` and via re-running
`/review-milestone-requirements`.
