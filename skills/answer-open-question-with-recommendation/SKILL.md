---
name: answer-open-question-with-recommendation
description: Record an open question's embedded recommendation as that question's answer in the current milestone's requirements.md.
model: opus
---

# answer-open-question-with-recommendation

Records one open question's **embedded recommendation** as its answer **inline, in the
current conversation** — never in a subagent — so the recording reasoning (which block was
resolved, what decision was folded in, what cascaded) stays in context for follow-up.

To record **every** recommendation-bearing question unattended instead, use
`/answer-all-open-questions-with-recommendation`.

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
**yourself, in this conversation**. Pass it the `<Short Title>` from the invocation as its
`SHORT TITLE` input. That procedure owns the find-milestone → locate → lift → delegate work,
composing over `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`, which owns the
locate/analyse/remove/fold/cascade recording.

Do **not** spawn the `answer-open-question-with-recommendation` agent.

The shared procedure resolves `<MILESTONE_DIR>` in its step 1 — hold that value; you need it
for the commit below.

**Clean-stop-and-point:** if the shared procedure hits its no-`<recommendation>`-element /
missing-block guard (no block matches the Short Title, or the matched block carries no
`<recommendation>` element), it stops without changing anything. Relay that to the user
and point them to run `/recommend-all-open-questions` first (so the question gets an embedded
recommendation), or to record a literal answer via `/answer-open-question <Short Title>. <answer text>`.
Commit nothing — go no further.

### 2. Commit the recommendation answer

Read and follow the shared commit procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you
need to resolve the path), carrying out its steps yourself. Supply it these inputs, using the
same `<MILESTONE_DIR>` the shared recording procedure resolved:

- **PATHS** — this skill's own edit: `<MILESTONE_DIR>/requirements.md`.
- **SUBJECT** — exactly `Recommendation-answer: <Short Title>` (the answered question's
  handle). This distinct subject does **not** match `/capture-milestone-principle-updates`'s
  `^Manual-answer:` grep, so capture never harvests it.
- **Body** — the lifted recommendation content (the `<option>` — `<rationale>` answer text,
  derived from the block's `<recommendation>` element — its `option` attribute recombined with
  the element's text, with XML entities un-escaped) — the answer that was recorded.

That procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.
Its no-op guard also covers this skill's clean-stop case: if step 1 hit its
no-`<recommendation>`-element / missing-block guard, `requirements.md` is unchanged, so
nothing is staged and nothing is committed.

### 3. Report findings

On the success path — the recommendation was recorded and committed — print exactly one fixed
terse status line, carrying no identifier (no Short Title, no commit subject):

```
Answer recorded.
```

Do **not** re-narrate which question resolved or how the document changed (the resolved block,
the decision folded into `## Decisions`, the cascading resolutions). Alongside the terse line
keep only the one piece of genuinely git-absent advisory output: any new open questions the
recorded decision may have introduced — surface these but do **not** add them to the document
without user confirmation.

**No-op case:** if step 2's dirty-own-path guard fired — nothing was committed because
`requirements.md` was unchanged (step 1's no-`<recommendation>`-element / missing-block clean
stop) — do **not** print the terse success line. Instead print a single line stating that
nothing was recorded and briefly why.

Then stay available: the user may now ask follow-up questions or request adjustments, with
the full recording context still in hand.
