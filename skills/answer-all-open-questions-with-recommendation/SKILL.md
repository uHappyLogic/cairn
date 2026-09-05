---
name: answer-all-open-questions-with-recommendation
description: Record the embedded recommendation as the answer for every open and deferred question in the current milestone's requirements that carries one.
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
into `## Decisions`, cascades to mooted siblings, and hands the recorded-but-**uncommitted** edit
back. The orchestrator **commits each answer itself** — once per successful agent return, before
dispatching the next. Because every dispatch mutates the same `requirements.md`, the dispatches run
**strictly sequentially, never in parallel**.

## Usage

```
/answer-all-open-questions-with-recommendation
```

Takes no arguments — it sweeps every `<open-question>` block (both `status="open"` and
`status="deferred"`) in the current milestone's `requirements.md` that contains a
`<recommendation>` element.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Gather and order the recommendation-bearing questions once

Fetch the recommendation-bearing set with the line-oriented boundary-line CLI — do **not** read
the whole file to eyeball headers. Every `<open-question>` block lives under the single
`## Open questions` section of `<MILESTONE_DIR>/requirements.md`, so that section is the one
bounded region the CLI slices deterministically. Using `awk`/`sed`/`grep` keyed on the
`<open-question …>` opening and `</open-question>` closing **boundary lines** — never a real XML
processor (`xmllint`) — enumerate every block and keep only those that **contain a
`<recommendation>` element**, extracting each surviving block's `id` (and `status`) by
attribute-name-anchored regex like `id="([^"]*)"` (so extraction is independent of attribute
order). Open and deferred blocks share one `<open-question …>` / `</open-question>` boundary-token
pair distinguished only by `status`, so the gather ignores type. Recommendation-less blocks —
those with **no `<recommendation>` element** — are **not gathered**: annotating them is the
recommend sweep's job (`/recommend-all-open-questions`), never this one's. If no block carries a
`<recommendation>` element, say so and stop.

Order the gathered list **loosely most-significant → least** — answer foundational questions
before the questions that depend on them. The ordering decides only *which question goes first*,
never *whether* a question gets answered: every gathered block carries a recommendation, so every
surviving question gets recorded.

You walk this gathered, ordered list **exactly once** (step 2). **Do not wrap step 2 in an outer
re-gather loop** — there is no such loop, and adding one is a defect.

### 2. Walk the order once, dispatching the agent per surviving question

For each question in the gathered order:

**a. Re-check against the live document.** With the same line-oriented boundary-line CLI, confirm
the block whose `id` case-folds equal to this question's Short Title **still exists and still
contains a `<recommendation>` element**. A prior answer's cascade may have already removed the
block; if it is gone — or its `<recommendation>` element is gone — **skip it** and move on. This is
a cheap deterministic locate/extract check keyed on the boundary lines, not a whole-document read.

**b. Dispatch the file-editing agent.** Use the `Agent` tool with `subagent_type` set to the
namespaced registry name of the `answer-open-question-with-recommendation` agent under this
plugin's namespace — Claude Code lists it as `cairn:answer-open-question-with-recommendation` —
one dispatch per question. Pass it the question's **Short Title** in the prompt:

```
Record the embedded recommendation for this open question as its answer.

Short Title: <Short Title>
```

Wait for the agent to return before dispatching the next one. **Dispatch strictly sequentially —
never in parallel**: every dispatch lifts, records, and cascades against the same
`requirements.md`, and you commit each answer between dispatches.

**c. Handle the agent's return.** The agent returns `DONE` or `FAILED: <reason>`:

- **`DONE`** — the agent recorded the answer, leaving the `requirements.md` edit uncommitted, and
  handed back the **lifted recommendation content** (the `<option>` — `<rationale>` answer text).
  **Commit this answer now, before dispatching the next question**, by reading and following the
  shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run
  `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path). Supply it these inputs, using the
  `<MILESTONE_DIR>` resolved in step 0:
  - **PATHS** — this answer's only edit: `<MILESTONE_DIR>/requirements.md` (never `git add -A`).
  - **SUBJECT** — exactly `Recommendation-answer: <Short Title>` (the answered question's handle).
  - **Body** — the lifted recommendation content the agent handed back (the recorded answer). The
    orchestrator does not re-derive the lift — it uses what the agent returned.

  The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit
  itself. Commit once per answer — the per-answer granularity is the point. Then continue to the
  next question.
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
`<open-question>` blocks (`status="open"` / `status="deferred"`) in `requirements.md` and via
re-running `/review-milestone-requirements`.
