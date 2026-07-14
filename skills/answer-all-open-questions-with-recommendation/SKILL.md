---
name: answer-all-open-questions-with-recommendation
description: Autonomously sweep the current milestone's requirements for open and deferred questions that already carry an embedded recommendation and record each one's recommendation as its answer — by dispatching the file-editing answer-open-question-with-recommendation agent once per question, strictly sequentially, and committing each answer itself after the agent returns. Use this after a recommend sweep has annotated the questions (via /recommend-all-open-questions) and you want every recommendation-bearing question recorded at once without answering each by hand. Trigger it whenever the user says things like "answer all the recommendations", "record every embedded recommendation", "run the recommendation-answer sweep", "sweep the recommendations", or "accept all the recommended answers". Recommendation-less questions are the recommend sweep's job and are left untouched.
---

# answer-all-open-questions-with-recommendation

This is the batch path that records every open question's **embedded recommendation** as its
answer. The recommend sweep (`/recommend-all-open-questions`) annotates each question by embedding
a `<recommendation>` element in its `<open-question>` block; this skill re-checks the current
milestone's questions and, for each block that contains such an element, dispatches the file-editing
`answer-open-question-with-recommendation` agent to lift that recommendation and record it —
leaving recommendation-less blocks untouched (annotating them is the recommend sweep's job,
not this one's).

It is an **orchestrator**. It does not record answers itself: for each recommendation-bearing
question it dispatches the `answer-open-question-with-recommendation` agent, which lifts the
`<recommendation>` element, folds the decision into `## Decisions`, cascades to mooted siblings, and
hands the recorded-but-**uncommitted** edit back. Following this milestone's layer rule (dispatched
agents never commit; an orchestrator commits its agents' work after they return), the orchestrator
**commits each answer itself** — once per successful agent return, before dispatching the next.

The reasoning here is **pre-computed** — the recommendation already exists in the question
block — so there is no candidate elimination worth isolating. What a per-question agent isolates
instead is the **mutation**: each dispatch is a **file-editing** agent, keeping the expensive
per-question edit out of the orchestrator's context; the agent records, and the orchestrator commits
what it recorded. Because every dispatch mutates the same `requirements.md`, the dispatches run
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
before the questions that depend on them. This ordering is a proxy for *cascade-parent-first*:
answering a foundational question may moot its dependents via cascade before they are ever
dispatched, which is the safe direction for cascades.

The ordering is a **sequencing heuristic only** — it decides *which question goes first*, never
*whether* a question gets answered. Every gathered block carries a recommendation, so every
surviving question gets recorded; ordering never reintroduces judgment.

You walk this gathered, ordered list **exactly once** (step 2). A single ordered pass terminates
the sweep: recording only ever *removes* questions (cascades moot them) and nothing adds
questions mid-sweep, so the set shrinks monotonically to a fixed point. **Do not wrap step 2 in
an outer re-gather loop** — there is no such loop, and adding one is a defect.

### 2. Walk the order once, dispatching the agent per surviving question

For each question in the gathered order:

**a. Re-check against the live document.** With the same line-oriented boundary-line CLI, confirm
the block whose `id` case-folds equal to this question's Short Title **still exists and still
contains a `<recommendation>` element**. A prior answer's cascade may have already removed the
block; if it is gone — or its `<recommendation>` element is gone — **skip it** and move on. This is
a cheap deterministic locate/extract check keyed on the boundary lines, not a whole-document read.
The gathered list is an *ordering, not a work snapshot* — this cheap live re-check is what keeps
the sweep correct as cascades fire, and it earns its keep by avoiding a whole agent spin-up on an
already-mooted block. The agent's own `shared/answer-procedure.md` step-2 stop-on-missing-block
stays as a backstop.

**b. Dispatch the file-editing agent.** Use the `Agent` tool with
`subagent_type: "answer-open-question-with-recommendation"`, one dispatch per question. Pass it
the question's **Short Title** in the prompt:

```
Record the embedded recommendation for this open question as its answer.

Short Title: <Short Title>
```

Wait for the agent to return before dispatching the next one. **Dispatch strictly sequentially —
never in parallel.** Every dispatch lifts, records, and cascades against the same
`requirements.md`, and you commit each answer between dispatches, so two dispatches in flight at
once would corrupt each other's edits. This serialized dispatch is the load-bearing reason this
sweep cannot parallelize.

The agent owns **all** document mutation but does **not** commit — it records the answer and hands
the recorded-but-uncommitted edit back. You commit it (step 2c) before dispatching the next
question, so one commit = one answer.

**c. Handle the agent's return.** The agent returns `DONE` or `FAILED: <reason>`:

- **`DONE`** — the agent recorded the answer, leaving the `requirements.md` edit uncommitted, and
  handed back the **lifted recommendation content** (the `<option>` — `<rationale>` answer text).
  **Commit this answer now, before dispatching the next question**, by reading and following the
  shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run
  `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path). Supply it these inputs, using the
  `<MILESTONE_DIR>` resolved in step 0:
  - **PATHS** — this answer's only edit: `<MILESTONE_DIR>/requirements.md` (never `git add -A`).
  - **SUBJECT** — exactly `Recommendation-answer: <Short Title>` (the answered question's handle).
    This distinct subject keeps the commit out of finish-time
    `/capture-milestone-principle-updates`: a recommendation-derived answer's body is a
    pre-computed recommendation, not user-deliberated reasoning, so capture never harvests it.
  - **Body** — the lifted recommendation content the agent handed back (the recorded answer). The
    orchestrator does not re-derive the lift — it uses what the agent returned.

  The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit
  itself; do not restate those mechanics here. Commit once per answer — the per-answer granularity
  is the point. Then continue to the next question.
- **`FAILED: <reason>`** — stop the loop, report the question's Short Title and the failure
  reason, and stop. Do not commit anything for this question and do not dispatch any further
  questions. A `FAILED` here means the agent's no-`<recommendation>`-element / missing-block clean
  stop (or another error) fired — but the gather step already filtered to blocks containing a
  `<recommendation>` element and step 2a re-checked immediately before dispatch, so a `FAILED`
  signals a genuine should-not-happen inconsistency (a block that raced away between the re-check
  and the dispatch, or an internal error). Treat it as a real failure to report-and-stop on, not a
  benign skip. **Never record the answer yourself as a fallback** — the agent owns all mutation.
- If the agent returns without an explicit `DONE` or `FAILED` status (returned early, produced no
  output, or gave an ambiguous result), treat it as `FAILED`: report what was returned, stop the
  loop, and do not dispatch further.

### 3. Report

When the gathered order is exhausted, report once how many recommendations were recorded and
direct the user to review the commits — each recorded answer landed on its own
`Recommendation-answer: <Short Title>` commit, individually reversible. If the sweep recorded
nothing (no recommendation-bearing questions), say so in one sentence.

Do **not** enumerate the untouched (recommendation-less) questions: they remain visible as
`<open-question>` blocks (`status="open"` / `status="deferred"`) in `requirements.md` and via
re-running `/review-milestone-requirements`, so listing them here would just duplicate the live
document.

## Rules

- Gather **only** blocks that contain a `<recommendation>` element — recommendation-less blocks
  are the recommend sweep's job and are never gathered here.
- Walk the gathered order **once**, with a per-question live re-check + skip via the boundary-line
  CLI. There is **no** outer re-gather loop.
- Dispatch the `answer-open-question-with-recommendation` agent **strictly sequentially — never
  in parallel** — waiting for each to return, then committing its answer, before dispatching the
  next, because every dispatch mutates the same `requirements.md`.
- The **agent** owns all document mutation but does **not** commit; the **orchestrator commits
  each answer** after the agent returns (one commit = one answer, subject
  `Recommendation-answer: <Short Title>`, the lifted recommendation content in the body), per the
  shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` — supplying only
  the path `<MILESTONE_DIR>/requirements.md` and the resolved subject, never restating its
  path-scoped-staging, no-op-guard, or subject-convention mechanics. This follows the usual
  orchestrator-commits arrangement (as in `/complete-all-tasks`): the orchestrator, not the agent,
  owns the commit.
- This sweep needs **no** clean-working-tree precondition: the commit stages path-scoped
  (`git add <MILESTONE_DIR>/requirements.md`, never `git add -A`), so a dirty tree cannot
  contaminate it.
- On an agent `FAILED: <reason>` (or any missing/ambiguous return), stop the loop immediately,
  commit nothing for that question, and report which question failed and why. **Never record an
  answer directly here, even as a fallback when a dispatch fails.**
