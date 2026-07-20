---
name: answer-open-question
description: Answer a named open question in the current milestone requirements document, recording the decision and its downstream implications and committing the manual-answer edit.
---

# answer-open-question

Resolves a named open or deferred question in the current milestone's `requirements.md` by recording the user's answer, propagating its implications through the document, and committing that edit on its own with the decision's rationale in the commit body — establishing the `Manual-answer:` commit the finish-time `/capture-milestone-principle-updates` skill later distills into reusable principles.

## Usage

```
/answer-open-question <Short Title>. <answer text>
```

The `<Short Title>` must match (case-insensitive, against the block's `id`) an existing `<open-question status="open|deferred">` block. The `.` character is the separator. Everything after the first `.` is the answer.

The answer text is recorded literally. The one reserved answer text is the retired sentinel `record the recommendation`: recording a question's embedded recommendation now lives in `/answer-open-question-with-recommendation`, so instead of recording that phrase this skill recognizes it, stops without recording, and redirects — see step 2.

**Example (literal answer):**
```
/answer-open-question Getting-started section order. Use approach B — open the "Draft the Getting Started section of the user guide" deliverable with the install-and-run walkthrough, then follow it with the conceptual overview, so a new reader reaches a working setup before the background material.
```

**Example (retired sentinel — redirected, records nothing):**
```
/answer-open-question Getting-started section order. record the recommendation
```

## Workflow

### 1. Parse the input

Split the skill args on the first `.` character:
- Before: the question **Short Title** (trim whitespace)
- After: the **answer text** (trim whitespace)

If no `.` is found, report a parse error and show the expected format.

### 2. Redirect guard for the retired sentinel

Compare the parsed answer text — **trimmed and lowercased** — against the retired sentinel `record the recommendation`, as an **exact whole-string match** (never a substring: an answer that merely *contains* those words is a literal answer, not the sentinel). This is a pure string comparison on the parsed text — no milestone resolution, no file read.

- **Exactly the sentinel — redirect and stop:** recording a question's embedded recommendation now lives in `/answer-open-question-with-recommendation`. **Stop without recording or committing anything** and print a redirect message telling the user to record the recommendation via `/answer-open-question-with-recommendation <Short Title>` instead (or to answer with literal text here via `/answer-open-question <Short Title>. <answer text>`). This is the skill's own clean no-commit stop — the same clean outcome the literal path gets from the shared procedure on a Short-Title mismatch.
- **Anything else — literal-answer path:** the parsed answer text *is* the `ANSWER`. Carry it straight into step 3.

### 3. Record the answer

Read and follow the shared answer-recording procedure at `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out every step **yourself, in this conversation**. Pass it the **Short Title** parsed in step 1 and the **answer text** resolved in step 2 as its `SHORT TITLE` and `ANSWER` inputs.

That procedure owns resolving the current milestone (the `<MILESTONE_DIR>` referenced below), locating the matching block, analysing the answer's implications, removing the block, folding the decision into `## Decisions`, and cascading to any entries the answer moots. Do not restate those steps here. If the Short Title matches no block, the procedure stops without changes and reports the mismatch — relay that to the user so they can retry.

### 4. Commit the manual answer

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out its steps yourself. Supply it these inputs, using the same `<MILESTONE_DIR>` resolved while recording:

- **PATHS** — this skill's own edit: `<MILESTONE_DIR>/requirements.md`.
- **SUBJECT** — exactly `Manual-answer: <Short Title>` (the answered question's handle), so `/capture-milestone-principle-updates` can collect these with `git log --grep='^Manual-answer: '`.
- **Body** — the decision's rationale — but record only rationale that genuinely exists in this conversation. Never prompt the user for a rationale and never fabricate one. When `/discuss-open-question` deliberation is in context, the body captures that reasoning. On a cold answer (no deliberation), the body is the literal answer text — recorded verbatim, including any inline "because" clause the user typed; when the answer states no reasoning, the body holds the bare decision. The answer string is itself the cold path's rationale affordance — add no separate rationale prompt.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit — do not restate those mechanics here. Its no-op guard also covers this skill's clean-stop cases: if step 3 stopped on a Short-Title mismatch, step 2's redirect guard fired on the retired sentinel, or step 1 hit a parse error, `requirements.md` is unchanged, so nothing is staged and nothing is committed.

### 5. Report findings

On the success path — the answer was recorded and committed — print exactly one fixed terse status line, carrying no identifier (no Short Title, no commit subject):

```
Answer recorded.
```

Do **not** re-narrate which question resolved or how the document changed (the resolved block, the decision folded into `## Decisions`, the cascading resolutions) — the committed diff and `git log` are the durable record of that. Alongside the terse line keep only the one piece of genuinely git-absent advisory output: any new open questions the answer may have introduced — surface these but do **not** add them to the document without user confirmation.

**No-op case:** if step 4's dirty-own-path guard fired — nothing was committed because `requirements.md` was unchanged (a step 1 parse error, the step 2 retired-sentinel redirect, or a step 3 Short-Title mismatch) — do **not** print the terse success line. Instead print a single line stating that nothing was recorded and briefly why, since git holds no durable record of a no-op.

## Rules

- Parse on the **first** `.` only — Short Title before, answer text after.
- The answer text is recorded literally. The retired sentinel `record the recommendation` — matched as an **exact whole-string** comparison after trim + lowercase, **never a substring** — is the one reserved exception: it is not recorded but redirects to `/answer-open-question-with-recommendation` and stops (step 2). Any other answer text is a literal answer and takes the unchanged literal path.
- The redirect guard records nothing and does no file I/O — it is a pure string comparison on the parsed answer text (no milestone resolution, no reading `requirements.md`). Recording a question's embedded recommendation belongs to `/answer-open-question-with-recommendation`, not this skill.
- The recording mechanism lives **only** in `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`; never duplicate or restate its locate / analyse / remove / fold / cascade steps here.
- Commit via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, supplying only the path `<MILESTONE_DIR>/requirements.md` and the subject `Manual-answer: <Short Title>`; never restate its path-scoped-staging, no-op-guard, or subject-convention mechanics here.
- The manual-answer commit carries the rationale in its **body**. The shared procedure's dirty-own-path no-op guard subsumes the old "commit only if recorded" conditional: a parse error, a Short-Title mismatch, or the step 2 redirect guard leaves `requirements.md` unchanged, so nothing is committed.
