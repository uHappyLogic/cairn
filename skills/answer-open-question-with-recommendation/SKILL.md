---
name: answer-open-question-with-recommendation
description: Record one open question's embedded recommendation as its answer in the current milestone's requirements.md inline in this conversation, then commit that answer on its own. Use when the recommend sweep has annotated a question with a recommendation and you want to accept and record that recommendation as the decision for a single named question you want to stay available to discuss afterwards.
model: opus
---

# answer-open-question-with-recommendation

Records one open question's **embedded recommendation** as its answer **inline, in the
current conversation** — not in a subagent. Running inline is the whole point: the recording
reasoning (which block was resolved, what decision was folded in, what cascaded) stays in
context, so you can follow up right after — ask why the recommendation read that way, tweak
the recorded decision, or answer the next question — without the context being thrown away.

This is the single-question, inline twin of the `answer-open-question-with-recommendation`
agent, completing the SKILL + AGENT pair (like `complete-task`/`submit-task`). For sweeping
**every** open question that carries an embedded recommendation unattended, use
`/answer-all-open-questions-with-recommendation` instead — that orchestrator dispatches the
file-editing agent per question and each dispatch commits its own answer.

## Invocation

```
/answer-open-question-with-recommendation <Short Title>
```

`<Short Title>` must match (case-insensitive, against the block's `id`) an existing
`<open-question status="open|deferred">` block that the `/recommend-all-open-questions` sweep
has already annotated with a `<recommendation>` element. The procedure resolves the current
milestone itself, so nothing needs to be looked up first.

## Workflow

### 1. Run the shared lift-then-delegate procedure inline

Read and follow the shared procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/answer-with-recommendation-procedure.md` (run
`echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out every step
**yourself, in this conversation**. It is the single source of truth for the
find-milestone → locate → lift → delegate work (it composes over
`${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`, which owns the
locate/analyse/remove/fold/cascade recording). Pass it the `<Short Title>` from the
invocation as its `SHORT TITLE` input. Do not restate its lift/record/cascade steps here.

Do **not** spawn the `answer-open-question-with-recommendation` agent — that would discard
the recording context this skill exists to keep. (The shared file is the single source of
truth, so the work is identical either way; only the context differs.)

The shared procedure resolves `<MILESTONE_DIR>` in its step 1 — hold that value; you need it
for the commit below.

**Clean-stop-and-point:** if the shared procedure hits its no-`<recommendation>`-element /
missing-block guard (no block matches the Short Title, or the matched block carries no
`<recommendation>` element), it stops without changing anything. Relay that to the user
and point them to run `/recommend-all-open-questions` first (so the question gets an embedded
recommendation), or to record a literal answer via `/answer-open-question <Short Title>. <answer text>`.
Commit nothing — go no further.

### 2. Commit the recommendation answer

**Only if step 1 actually recorded the answer** — i.e. the shared procedure folded a decision
into `## Decisions` rather than stopping on its no-`<recommendation>`-element / missing-block
guard — commit the edit. If it stopped without changes, there is nothing to commit; do not
run these commands.

Stage **only** this skill's own `requirements.md` edit — path-scoped, never `git add -A` —
and commit it on its own, using the same `<MILESTONE_DIR>` the shared procedure resolved:

```
git add <MILESTONE_DIR>/requirements.md
git commit -m "Recommendation-answer: <Short Title>" -m "<lifted recommendation content>"
```

- **Subject:** exactly `Recommendation-answer: <Short Title>` (the answered question's
  handle). This distinct subject keeps the commit out of finish-time
  `/capture-milestone-principle-updates`: a recommendation-derived answer's body is a
  pre-computed recommendation, not user-deliberated reasoning, so capture never harvests it.
- **Body:** the lifted recommendation content (the `<option>` — `<rationale>` answer text,
  derived from the block's `<recommendation>` element — its `option` attribute recombined with
  the element's text, with XML entities un-escaped) — the answer that was recorded.

Committing here is a deliberate, documented exception to the project's "individual skills
never commit" rule — the standalone `answer-open-question-with-recommendation` skill records
a decision, so it commits its decision atomically with a greppable subject, exactly as
`answer-open-question` does. Staging path-scoped keeps the commit touching only
`requirements.md` and never sweeps in unrelated working-tree changes.

### 3. Report findings

After committing, briefly state:
- Which question was resolved and how the document changed (resolved block, decision folded
  into `## Decisions`, cascading resolutions).
- Any new open questions the recorded decision may have introduced — surface these but do
  **not** add them to the document without user confirmation.

Then stay available: the user may now ask follow-up questions or request adjustments, with
the full recording context still in hand.

## Rules

- Run the shared procedure **inline** — never delegate this skill to the
  `answer-open-question-with-recommendation` agent. (The shared file is the single source of
  truth, so the work is identical either way; only the context differs.)
- The lift/record/cascade mechanism lives **only** in the shared procedures
  (`${CLAUDE_PLUGIN_ROOT}/shared/answer-with-recommendation-procedure.md` composing over
  `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`); never duplicate or restate lifting the
  `<recommendation>` element, folding into `## Decisions`, or cascading here.
- Commit **only** when step 1 actually recorded the answer; the shared procedure's
  no-`<recommendation>`-element / missing-block clean stop produces no change and no commit.
- Stage path-scoped — `git add <MILESTONE_DIR>/requirements.md`, never `git add -A` — so the
  commit touches only `requirements.md`.
- The commit carries the lifted recommendation content in its **body** and the subject
  `Recommendation-answer: <Short Title>`. Committing here is a deliberate, documented exception
  to the "individual skills never commit" rule.
