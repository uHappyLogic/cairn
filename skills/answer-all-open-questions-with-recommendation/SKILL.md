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
into `## Decisions`, cascades to mooted siblings, and leaves that edit **staged but uncommitted**.
The orchestrator **commits that staged index itself** — once per successful agent return, before
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

### 1. Gather the recommendation-bearing questions once and order them by the dependency graph

Fetch the recommendation-bearing set with the line-oriented boundary-line CLI — do **not** read
the whole file to eyeball headers. Every `<open-question>` block lives under the single
`## Open questions` section of `<MILESTONE_DIR>/requirements.md`, so that section is the one
bounded region the CLI slices deterministically. Using `awk`/`sed`/`grep` keyed on the
`<open-question …>` opening and `</open-question>` closing **boundary lines** — never a real XML
processor (`xmllint`) — enumerate every block **in document order** (the order the CLI hands
them back is the order their blocks appear in the section, and the walk below relies on it) and
keep only those that **contain a `<recommendation>` element**, extracting each surviving block's
`id` (and `status`) by attribute-name-anchored regex like `id="([^"]*)"` (so extraction is
independent of attribute order). From each surviving block also extract the `question` value of
every self-closing `<depends-on question="…" option="…"/>` line it carries — the same
attribute-name-anchored regex, anchored on `question=`; the recommend sweep embeds one such line
per sibling recommendation this block's recommendation assumed. Read only the `question` value
here: the `option` value is what the recording core's cascade reconciles at answer time, and the
orchestrator never acts on it. Open and deferred blocks share one `<open-question …>` /
`</open-question>` boundary-token pair distinguished only by `status`, so the gather ignores type.
Recommendation-less blocks — those with **no `<recommendation>` element** — are **not gathered**:
annotating them is the recommend sweep's job (`/recommend-all-open-questions`), never this one's.
If no block carries a `<recommendation>` element, say so and stop.

Order the gathered list by **walking the dependency graph built over it** — never by a judgment
of which question is more significant. Build the graph from the gathered set alone: each gathered
block is a node, and each of its `<depends-on question="…">` values is an edge from that block to
the gathered block whose `id` case-folds equal to the value (both entity-unescaped, exactly as
step 2's re-check matches `id`). **Drop every edge whose target is not in the gathered set** — the
named block is absent from the document, or it is present but carries no `<recommendation>`
element and so was never gathered. This sweep will never answer such a target, so the edge carries
nothing to order against; dropping it is the whole treatment — never widen the gather to pull the
target in, and leave the `<depends-on>` line itself in the document for the recording core's
cascade. A question left with no resolvable edge after the drop is an ordinary origin.

Then walk the graph **by depth**, placing each question exactly once:

- **Origins first.** Every question with no resolvable edge is an origin. Place all origins, in
  **document order** among themselves.
- **Next depth.** Place every not-yet-placed question whose every resolvable edge points at a
  question already placed, again in document order among themselves. Repeat until every
  question is placed. Same-depth questions cannot depend on one another, so document order is
  the only tie-break needed and it is what the gather already yielded.
- **Stranded set.** If questions remain but none of them has all its targets placed — each waits
  on another of the remaining — the remainder is a `<depends-on>` cycle (reachable only through
  the recommend sweep's hand-clear escape hatch, when a regenerated block declares a dependency
  back on one of its former dependents). Promote the **document-order-first** remaining question
  to an origin: place it next, count it as placed, and continue the depth walk over the rest.
  Repeat the promotion each time the walk strands again. The cycle dissolves at the promoted
  question's answer, whose cascade reconciles every dependent that assumed its option.

The walk is **deterministic and total** for any graph shape, cycles included: it depends only on
the document's block order and the gathered `<depends-on>` values, places every gathered question
exactly once, and always terminates. Walking a target before its dependents is what lets each
answer's cascade settle the dependents in turn — removing the tag where the recorded option agrees
with what they assumed, stripping their embedded children where it does not. The ordering decides
only *which question goes first*, never *whether* a question gets answered: every gathered block
carries a recommendation, so every question that still carries one when its turn comes gets
recorded, and a dependent whose children a prior answer's cascade stripped is skipped by step 2's
re-check — that is the cascade doing its job, not a gap in the walk.

You walk this gathered, ordered list **exactly once** (step 2). **Do not wrap step 2 in an outer
re-gather loop** — there is no such loop, and adding one is a defect.

### 2. Walk the order once, dispatching the agent per surviving question

For each question in the gathered order:

**a. Re-check against the live document, and lift the commit body.** With the same line-oriented
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
`<open-question>` blocks (`status="open"` / `status="deferred"`) in `requirements.md` and via
re-running `/review-milestone-requirements`.
