---
name: answer-open-question
description: Answer a named open question in the current milestone requirements document, updating the document to reflect the decision and its downstream implications.
---

# answer-open-question

Resolves a named open question or deferred entry in the current milestone's `requirements.md` by recording the user's answer and propagating its implications through the document — then chains into `try-capture-answer-principle` so a reusable rule behind the call can be learned for future autonomous sweeps.

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

That procedure owns resolving the current milestone, locating the matching block, analysing the answer's implications, removing the block, folding the decision into `## Implementation decisions`, and cascading to any entries the answer moots. Do not restate those steps here. If the Short Title matches no entry, the procedure stops without changes and reports the mismatch — relay that to the user so they can retry.

### 3. Report findings

After the procedure finishes, briefly state:
- Which question was resolved and how the document changed (resolved block, implementation-decision updates, cascading resolutions).
- Any new open questions the answer may have introduced — surface these but do **not** add them to the document without user confirmation.

### 4. Capture any reusable principle

After recording, **always** invoke `/try-capture-answer-principle` with no argument. This chain-off is **unconditional** — `answer-open-question` does not judge whether the decision generalizes. Capture runs inline in this same conversation, where the full deliberation is in context; it anchors on the answer just recorded, analyses whether a reusable answering principle lies behind it, and exits quietly on its own when nothing generalizes. So the chain is always taken; the decision about whether a principle is worth recording belongs entirely to capture.

## Rules

- Parse on the **first** `.` only — Short Title before, answer text after.
- The recording mechanism lives **only** in `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`; never duplicate or restate its locate / analyse / remove / fold / cascade steps here.
- Always chain into `/try-capture-answer-principle` after recording — unconditionally, never gated on your own judgment of whether the decision is reusable.
- Do not commit. Leave the document (and any principle-store) changes staged for the user to review.
