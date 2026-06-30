---
name: answer-open-question
description: Answer a named open question in the current milestone requirements document, recording the decision and its downstream implications and committing the manual-answer edit.
---

# answer-open-question

Resolves a named open question or deferred entry in the current milestone's `requirements.md` by recording the user's answer, propagating its implications through the document, and committing that edit on its own with the decision's rationale in the commit body — establishing the `Manual-answer:` commit the finish-time `/capture-milestone-principle-updates` skill later distills into reusable principles.

## Usage

```
/answer-open-question <Short Title>. <answer text>
```

The `<Short Title>` must match (case-insensitive) the title of an existing `Open question` or `Deferred` entry. The `.` character is the separator. Everything after the first `.` is the answer.

**Example:**
```
/answer-open-question Arc drive technique. Use approach B — two Cinemachine virtual cameras per rail axis, blended by Cinemachine's built-in blend system. RailCameraSnapper will activate the appropriate virtual camera on rail switch rather than calling ForceCameraPosition.
```

## Workflow

### 1. Parse the input

Split the skill args on the first `.` character:
- Before: the question **Short Title** (trim whitespace)
- After: the **answer text** (trim whitespace)

If no `.` is found, report a parse error and show the expected format.

### 2. Record the answer

Read and follow the shared answer-recording procedure at `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out every step **yourself, in this conversation**. Pass it the **Short Title** and **answer text** parsed in step 1 as its `SHORT TITLE` and `ANSWER` inputs.

That procedure owns resolving the current milestone (the `<MILESTONE_DIR>` referenced below), locating the matching block, analysing the answer's implications, removing the block, folding the decision into `## Decisions`, and cascading to any entries the answer moots. Do not restate those steps here. If the Short Title matches no entry, the procedure stops without changes and reports the mismatch — relay that to the user so they can retry.

### 3. Commit the manual answer

**Only if step 2 actually recorded the answer** — i.e. the shared procedure folded a decision into `## Decisions` rather than stopping on a Short-Title mismatch — commit the edit. If the procedure stopped without changes (or step 1 hit a parse error), there is nothing to commit; do not run these commands.

Stage **only** this skill's own `requirements.md` edit — path-scoped, never `git add -A` — and commit it on its own, using the same `<MILESTONE_DIR>` step 2 resolved:

```
git add <MILESTONE_DIR>/requirements.md
git commit -m "Manual-answer: <Short Title>" -m "<rationale / decision body>"
```

- **Subject:** exactly `Manual-answer: <Short Title>` (the answered question's handle), mirroring the sweep's `Principle-based-answer: <Short Title>` so `/capture-milestone-principle-updates` can collect these with `git log --grep='^Manual-answer: '`.
- **Body:** the decision's rationale — but record only rationale that genuinely exists in this conversation. Never prompt the user for a rationale and never fabricate one. When `/discuss-open-question` deliberation is in context, the body captures that reasoning. On a cold answer (no deliberation), the body is the answer text recorded verbatim, including any inline "because" clause the user typed; when the answer states no reasoning, the body holds the bare decision. The answer string is itself the cold path's rationale affordance — add no separate rationale prompt.
- **No `Answer-Principle:` trailer.** That trailer is the sweep's signature; its absence is what marks this commit as a manual answer rather than an auto-answer.

This is a deliberate, documented exception to the project's "individual skills never commit" rule: `answer-open-question` commits exactly its own path-scoped manual-answer edit so that finish-time principle capture has a clean, greppable commit to walk. Staging path-scoped keeps the commit touching only `requirements.md` and never sweeps in unrelated working-tree changes, which also preserves the sweep's clean-tree precondition.

### 4. Report findings

After committing, briefly state:
- Which question was resolved and how the document changed (resolved block, decision folded into `## Decisions`, cascading resolutions).
- Any new open questions the answer may have introduced — surface these but do **not** add them to the document without user confirmation.

## Rules

- Parse on the **first** `.` only — Short Title before, answer text after.
- The recording mechanism lives **only** in `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`; never duplicate or restate its locate / analyse / remove / fold / cascade steps here.
- Commit **only** when step 2 actually recorded the answer; a parse error or a Short-Title mismatch produces no commit.
- Stage path-scoped — `git add <MILESTONE_DIR>/requirements.md`, never `git add -A` — so the commit touches only `requirements.md`.
- The manual-answer commit carries the rationale in its **body** and **no** `Answer-Principle:` trailer. Committing here is a deliberate, documented exception to the "individual skills never commit" rule.
