---
name: answer-all-open-questions-with-recommendation
description: Autonomously sweep the current milestone's requirements for open and deferred questions that already carry an embedded recommendation and record each one's recommendation as its answer — by dispatching the file-editing answer-open-question-with-recommendation agent once per question, strictly sequentially, one commit per answer. Use this after a recommend sweep has annotated the questions (via /recommend-all-open-questions) and you want every recommendation-bearing question recorded at once without answering each by hand. Trigger it whenever the user says things like "answer all the recommendations", "record every embedded recommendation", "run the recommendation-answer sweep", "sweep the recommendations", or "accept all the recommended answers". Recommendation-less questions are the recommend sweep's job and are left untouched.
---

# answer-all-open-questions-with-recommendation

This is the batch path that records every open question's **embedded recommendation** as its
answer. The recommend sweep (`/recommend-all-open-questions`) annotates each question with an
`> **Recommendation:**` anchor; this skill re-reads the current milestone's questions and, for
each one that carries such an anchor, dispatches the file-editing
`answer-open-question-with-recommendation` agent to lift that recommendation and record it —
leaving recommendation-less questions untouched (annotating them is the recommend sweep's job,
not this one's).

It is a pure **orchestrator**. It does not record answers itself: for each recommendation-bearing
question it dispatches the `answer-open-question-with-recommendation` agent, which lifts the
anchor, folds the decision into `## Decisions`, cascades to mooted siblings, and **commits its
own answer**. The orchestrator owns only gathering, ordering, and sequencing the dispatches — it
**never edits `requirements.md` and never commits**.

The reasoning here is **pre-computed** — the recommendation already exists in the question
block — so there is no candidate elimination worth isolating. What a per-question agent isolates
instead is the **mutation**: each dispatch is a **file-editing** agent that owns its own commit,
keeping the expensive per-question edit out of the orchestrator's context. Because every dispatch
mutates the same `requirements.md`, the dispatches run **strictly sequentially, never in parallel**.

## Usage

```
/answer-all-open-questions-with-recommendation
```

Takes no arguments — it sweeps every `Open question` / `Deferred` entry in the current
milestone's `requirements.md` that carries an embedded `> **Recommendation:**` anchor.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Gather and order the recommendation-bearing questions once

Read `<MILESTONE_DIR>/requirements.md` in full. Gather every `Open question — <Short Title>` and
`Deferred — <Short Title>` entry **that carries an embedded `> **Recommendation:**` anchor** in
its blockquote run. Recommendation-less questions are **not gathered** — annotating them is the
recommend sweep's job (`/recommend-all-open-questions`), never this one's. If no gathered
question carries a recommendation, say so and stop.

Order the gathered list **loosely most-significant → least** — answer foundational questions
before the questions that depend on them. This ordering is a proxy for *cascade-parent-first*:
answering a foundational question may moot its dependents via cascade before they are ever
dispatched, which is the safe direction for cascades.

The ordering is a **sequencing heuristic only** — it decides *which question goes first*, never
*whether* a question gets answered. Every gathered question carries a recommendation, so every
surviving question gets recorded; ordering never reintroduces judgment.

You walk this gathered, ordered list **exactly once** (step 2). A single ordered pass terminates
the sweep: recording only ever *removes* questions (cascades moot them) and nothing adds
questions mid-sweep, so the set shrinks monotonically to a fixed point. **Do not wrap step 2 in
an outer re-gather loop** — there is no such loop, and adding one is a defect.

### 2. Walk the order once, dispatching the agent per surviving question

For each question in the gathered order:

**a. Re-check against the live document.** Re-read `<MILESTONE_DIR>/requirements.md` and confirm
the question's block still exists and still carries its `> **Recommendation:**` anchor. A prior
answer's cascade may have already removed it; if it is gone, **skip it** and move on. The
gathered list is an *ordering, not a work snapshot* — this cheap live re-read is what keeps the
sweep correct as cascades fire, and it earns its keep by avoiding a whole agent spin-up on an
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
never in parallel.** Every dispatch lifts, records, cascades, and commits against the same
`requirements.md`, so two dispatches in flight at once would corrupt each other's edits and
commits. This serialized dispatch is the load-bearing reason this sweep cannot parallelize.

The agent owns **all** document mutation and its own path-scoped commit (one commit = one answer,
subject `Recommendation-answer: <Short Title>`). The orchestrator neither edits `requirements.md`
nor commits.

**c. Handle the agent's return.** The agent returns `DONE` or `FAILED: <reason>`:

- **`DONE`** — the agent recorded the answer and committed it under
  `Recommendation-answer: <Short Title>`. Continue to the next question.
- **`FAILED: <reason>`** — stop the loop, report the question's Short Title and the failure
  reason, and stop. Do not dispatch any further questions. A `FAILED` here means the agent's
  no-anchor / missing-block clean stop (or another error) fired — but the gather step already
  filtered to questions carrying an embedded recommendation and step 2a re-checked immediately
  before dispatch, so a `FAILED` signals a genuine should-not-happen inconsistency (a block that
  raced away between the re-check and the dispatch, or an internal error). Treat it as a real
  failure to report-and-stop on, not a benign skip. **Never record the answer yourself as a
  fallback** — the agent owns all mutation and the commit.
- If the agent returns without an explicit `DONE` or `FAILED` status (returned early, produced no
  output, or gave an ambiguous result), treat it as `FAILED`: report what was returned, stop the
  loop, and do not dispatch further.

### 3. Report

When the gathered order is exhausted, report once how many recommendations were recorded and
direct the user to review the commits — each recorded answer landed on its own
`Recommendation-answer: <Short Title>` commit, individually reversible. If the sweep recorded
nothing (no recommendation-bearing questions), say so in one sentence.

Do **not** enumerate the untouched (recommendation-less) questions: they remain visible as
`Open question` / `Deferred` blocks in `requirements.md` and via re-running
`/review-milestone-requirements`, so listing them here would just duplicate the live document.

## Rules

- Gather **only** questions that carry an embedded `> **Recommendation:**` anchor —
  recommendation-less questions are the recommend sweep's job and are never gathered here.
- Walk the gathered order **once**, with a per-question live re-read + skip. There is **no** outer
  re-gather loop.
- Dispatch the `answer-open-question-with-recommendation` agent **strictly sequentially — never
  in parallel** — waiting for each to return before dispatching the next, because every dispatch
  mutates the same `requirements.md`.
- The **agent** owns all document mutation and its own path-scoped commit (one commit = one
  answer, subject `Recommendation-answer: <Short Title>`). The orchestrator **never edits
  `requirements.md` and never commits** — it purely dispatches and sequences. This inverts the
  usual orchestrator-commits arrangement (as in `/complete-all-tasks`, whose orchestrator owns the
  commit): here the per-question agent, not this orchestrator, owns it.
- This sweep needs **no** clean-working-tree precondition: the agent stages path-scoped
  (`git add <MILESTONE_DIR>/requirements.md`, never `git add -A`), so a dirty tree cannot
  contaminate its commit.
- On an agent `FAILED: <reason>` (or any missing/ambiguous return), stop the loop immediately and
  report which question failed and why. **Never record an answer directly here, even as a
  fallback when a dispatch fails.**
