# Answer-with-recommendation procedure (shared core)

This is the single source of truth for recording one open question's **embedded
recommendation** as its answer in the current milestone's `requirements.md`. It composes
over `shared/answer-procedure.md` (the recording core): it lifts the recommendation the
recommend sweep embedded beneath the question header, then delegates the actual recording
to that core unchanged. It is followed in two ways:

- **Inline**, by the `answer-open-question-with-recommendation` skill, which runs these
  steps directly in the user's conversation so the recording context survives for
  follow-up.
- **In isolation**, by the `answer-open-question-with-recommendation` agent, which runs the
  same steps in a throwaway subagent context for the
  `answer-all-open-questions-with-recommendation` sweep.

The wrappers add their own framing (where the title comes from, how the outcome is
signalled, committing, any follow-up). This file describes only the work itself — resolve,
locate, lift, delegate — and says nothing about how callers obtain their input or wrap the
result.

## Inputs

This procedure records one recommendation-derived answer given one input the caller
supplies:

- **SHORT TITLE** — the resolved handle of an existing `Open question` or `Deferred`
  entry to answer (case-insensitive). The caller has already obtained it; locating the
  matching block, lifting its recommendation, and delegating the recording are this
  procedure's job.

The ANSWER is **not** an input here — this procedure *derives* it by lifting the block's
embedded recommendation. That derived ANSWER, together with SHORT TITLE, is what it hands to
`shared/answer-procedure.md`.

## Procedure

### 1. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 2. Locate the question and its embedded recommendation

Read `<MILESTONE_DIR>/requirements.md`. Find the `Open question — <Short Title>` or
`Deferred — <Short Title>` entry whose title matches SHORT TITLE (case-insensitive). The
question is the contiguous run of `>`-prefixed lines beginning with that one-line header —
the header plus the recommendation sub-block the recommend sweep embedded beneath it (its
internal gaps rendered as empty `>` lines, bounded by the blank lines that separate
entries).

Within that run, find the anchor line of the exact form:

```
> **Recommendation:** <chosen option> — <one-line rationale>
```

**No-embedded-recommendation guard.** If no entry matches SHORT TITLE, or the matched entry
carries no `> **Recommendation:**` anchor line (the recommend sweep never annotated it, or
the question was added afterward), **stop without changing anything** and report why. This
mirrors `shared/answer-procedure.md`'s clean stop on a Short-Title mismatch: nothing is
recorded.

This locating is a **read** to derive the answer — it is not the recording core's own
locate/remove step, which runs later inside the delegated procedure.

### 3. Lift the anchor into ANSWER

Derive ANSWER from the matched anchor line by stripping the leading `> ` and the
`**Recommendation:**` label, leaving the `<chosen option> — <one-line rationale>` content
as the answer text.

### 4. Delegate to the recording core

Hand the resolved **SHORT TITLE** and the derived **ANSWER** to
`${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` and follow it unchanged. That procedure
owns the recording work (locate, analyse, remove, fold, cascade); this procedure only lifts
and delegates.

## Rules

- Title matching is case-insensitive.
- Derive ANSWER only from the block's `> **Recommendation:**` anchor — never from any other
  line of the sub-block, and never invent answer text.
- The no-embedded-recommendation guard is a clean stop: when no block matches or the matched
  block carries no anchor, change nothing and record nothing.
- Do not restate `shared/answer-procedure.md`'s locate/analyse/remove/fold/cascade steps —
  reference it and let it own the recording; this file's job is only lift-then-delegate.
