---
name: answer-all-open-questions-with-recommendation
description: Record the embedded recommendation as the answer for every question in the current milestone's requirements that carries one.
---

# answer-all-open-questions-with-recommendation

This is the batch path that records every open question's **embedded recommendation** as its
answer. The recommend sweep (`/recommend-all-open-questions`) annotates each question by embedding
a `<recommendation>` element in its `<open-question>` block; this skill re-checks the current
milestone's questions and, for each block that contains such an element, dispatches the
file-editing `answer-open-question-with-recommendation` agent to lift that recommendation and
record it — leaving recommendation-less blocks untouched (annotating them is the recommend sweep's
job, not this one's). It requires **no** clean-working-tree precondition.

It is an **orchestrator**. It does not record answers itself: for each recommendation-bearing
question it dispatches the agent, which lifts the `<recommendation>` element, folds the decision
into `## Decisions`, cascades to mooted siblings, and leaves that edit **staged but uncommitted**.
The orchestrator **commits that staged index itself** — once per successful agent return, before
dispatching the next. Because every dispatch mutates the same `requirements.md`, the dispatches run
**strictly sequentially, never in parallel**.

## Usage

```
/answer-all-open-questions-with-recommendation
```

Takes no arguments — it sweeps every `<open-question>` block in the current milestone's
`requirements.md` that contains a `<recommendation>` element.

## Workflow

### 0. Find the current milestone

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Gather the recommendation-bearing questions in dispatch order with one call

Run

```
python3 .agents/plugins/cairn/tools/open_questions.py walk <MILESTONE_DIR>
```

Its output is the gathered order: one line per `<open-question>` block that carries a
`<recommendation>` element, the block's `id` (its Short Title) printed bare, already in dispatch
order. The tool gathers those blocks in document order, treats each block's
`<depends-on question="…">` value as an edge to the gathered block that id names — an edge naming
a block that is absent or carries no `<recommendation>` is dropped, because this sweep never
answers that block and the tag stays in the document for the recording core's cascade — and
places every target before its dependents, same-depth ties in document order, breaking a
`<depends-on>` cycle by promoting its document-order-first block to an origin. Recommendation-less
blocks are not printed: annotating them is the recommend sweep's job
(`/recommend-all-open-questions`), never this one's. Walking a target before its dependents is what
lets each answer's cascade settle the dependents in turn — the tag removed where the recorded option
agrees with what they assumed, their embedded children stripped where it does not — and a dependent
so stripped is skipped by step 2's re-check: that is the cascade doing its job, not a gap in the
order.

If the call prints nothing, no block carries a `<recommendation>` element: say so and stop. If it
fails, its one `Error: <reason>` line on stderr is the report: print it and stop.

You walk this printed order **exactly once** (step 2). **Do not wrap step 2 in an outer re-gather
loop** — there is no such loop, and adding one is a defect.

### 2. Walk the order once, dispatching the agent per surviving question

For each question in the gathered order:

**a. Re-check against the live document, and lift the commit body.** With the line-oriented
boundary-line CLI, confirm the block whose `id` case-folds equal to this question's Short Title
**still exists and still contains a `<recommendation>` element**. A prior answer's cascade may have
already removed the block; if it is gone — or its `<recommendation>` element is gone — **skip it**
and move on. This is a cheap deterministic locate/extract check keyed on the boundary lines, not a
whole-document read.

From that same surviving block, **lift the recommendation text now**, while it is still in the
document: recombine the `<recommendation>` element's `option` attribute value with the element's
text as `<option> — <rationale>`, un-escaping XML entities — the same answer form the agent records.
Hold it for this question's commit body in **c**; the agent hands nothing back, and after it runs
the block is gone, so lifting it here is the only chance.

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
`requirements.md`, and you commit each answer between dispatches.

**c. Handle the agent's return.** The agent returns `DONE` or `FAILED: <reason>`:

- **`DONE`** — the agent recorded the answer and left its `requirements.md` edit **staged but
  uncommitted**, returning no payload. **Commit that staged index now, before dispatching the next
  question** — stage nothing yourself (the agent already staged path-scoped, so never `git add` and
  never `git add -A`):
  - **No-op guard** — check whether anything is actually staged (for example
    `git diff --cached --quiet`). If nothing is, this answer produced no committable change: commit
    nothing, create no empty commit, and continue to the next question.
  - **Commit** — commit the staged index under exactly the subject
    `Recommendation-answer: <Short Title>` (the answered question's handle), with the recommendation
    text you lifted in **a** as the commit **body** — `git commit -m "<subject>" -m "<body>"` with no
    pathspec, since the staged index is exactly this answer's edit.

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

If the sweep recorded nothing (no recommendation-bearing questions, so nothing was committed this
run), do not print the terse success line; instead say so in one sentence — this is the distinct
one-line no-op message, kept separate from the terse success line.

Do **not** enumerate the untouched (recommendation-less) questions: they remain visible as
`<open-question>` blocks in `requirements.md` and via re-running
`/review-milestone-requirements`.
