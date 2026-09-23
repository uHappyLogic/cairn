---
name: answer-open-question-with-recommendation
description: Record an open question's embedded recommendation as that question's answer in the current milestone's requirements.md.
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
`<open-question>` block in `<MILESTONE_DIR>/open_questions.xml` that the
`/recommend-all-open-questions` sweep has already annotated with a `<recommendation>`
element. The skill resolves the current milestone itself, so nothing needs to be looked up
first.

## Workflow

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never
use a hardcoded path. Hold `<MILESTONE_DIR>` — you need it for the delegated recording and
the commit.

### 2. Run the shared lift-then-delegate procedure inline

Read and follow the shared procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/answer-with-recommendation-procedure.md`, carrying out every step
**yourself, in this conversation**. Pass it the `<MILESTONE_DIR>` from step 1 and the
`<Short Title>` from the invocation as its `MILESTONE_DIR` and `SHORT TITLE` inputs. That
procedure owns the lift → delegate work, composing over
`${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`, which owns the
locate/analyse/fold/remove/cascade recording; every read and write of `open_questions.xml`
in either is a call to the plugin's open-question tool.

Hold the one line the shared procedure's `lift` call prints, "`<option>` — `<rationale>`" —
it is the commit body below.

**Clean-stop-and-point:** if the shared procedure's `lift` call fails — the tool's `Error:`
line says no block has that id, or that the matched block carries no `<recommendation>`
element — it stops without changing anything. Relay that `Error:` line to the user and point
them to run `/recommend-all-open-questions` first (so the question gets an embedded
recommendation), or to record a literal answer via `/answer-open-question <Short Title>. <answer text>`.
Commit nothing — go no further.

### 3. Commit the recommendation answer

Read and follow the shared commit procedure at
`${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these three inputs, using the
`<MILESTONE_DIR>` from step 1:

- **PATHS** — this skill's own edits: `<MILESTONE_DIR>/open_questions.xml` and
  `<MILESTONE_DIR>/requirements.md`.
- **SUBJECT** — exactly `Recommendation-answer: <Short Title>` (the answered question's
  handle). This distinct subject marks an accepted recommendation: when
  `/capture-milestone-principle-updates` walks a milestone's answer commits across all three
  subjects, it reads this one as evidence about principles already in the store only, never as
  a source of new principles — those come from the `Manual-answer:` and `Alternative-answer:`
  override signals.
- **BODY** — the lifted recommendation: the "`<option>` — `<rationale>`" line the `lift` call
  printed in step 2, verbatim — the answer that was recorded.

That procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.
Its no-op guard also covers this skill's clean-stop case: if step 2 stopped on the `lift`
call's `Error:` line, neither file changed, so nothing is staged and nothing is committed.

### 4. Report findings

On the success path — the recommendation was recorded and committed — print exactly one fixed
terse status line, carrying no identifier (no Short Title, no commit subject):

```
Answer recorded.
```

Do **not** re-narrate which question resolved or how the documents changed (the removed block,
the decision folded into `## Decisions`, the cascading resolutions). Alongside the terse line
keep only the one piece of genuinely git-absent advisory output: any new open questions the
recorded decision may have introduced — surface these but do **not** add them to the document
without user confirmation.

**No-op case:** if step 3's dirty-own-path guard fired — nothing was committed because
neither file changed (step 2's clean stop on the `lift` call's `Error:` line) — do **not**
print the terse success line. Instead print a single line stating that nothing was recorded
and briefly why.

Then stay available: the user may now ask follow-up questions or request adjustments, with
the full recording context still in hand.
