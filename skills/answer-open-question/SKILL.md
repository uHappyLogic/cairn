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

The answer text is normally recorded literally. The one reserved exception is the sentinel `record the recommendation` (record-recommendation mode): instead of recording that phrase, the skill lifts the recommendation the `/recommend-all-open-questions` sweep embedded beneath the question header and records that — see step 2.

**Example (literal answer):**
```
/answer-open-question Arc drive technique. Use approach B — two Cinemachine virtual cameras per rail axis, blended by Cinemachine's built-in blend system. RailCameraSnapper will activate the appropriate virtual camera on rail switch rather than calling ForceCameraPosition.
```

**Example (record-recommendation mode):**
```
/answer-open-question Arc drive technique. record the recommendation
```

## Workflow

### 1. Parse the input

Split the skill args on the first `.` character:
- Before: the question **Short Title** (trim whitespace)
- After: the **answer text** (trim whitespace)

If no `.` is found, report a parse error and show the expected format.

### 2. Resolve the answer text (literal vs. record-recommendation)

Compare the parsed answer text — **trimmed and lowercased** — against the reserved sentinel `record the recommendation`, as an **exact whole-string match** (never a substring: an answer that merely *contains* those words is a literal answer, not the sentinel). This gate decides what the `ANSWER` for step 3 is:

- **Not the sentinel — literal-answer path (unchanged):** the parsed answer text *is* the `ANSWER`. Carry it straight into step 3.
- **Exactly the sentinel — record-recommendation mode:** do not record the phrase itself. Lift the recommendation the `/recommend-all-open-questions` sweep embedded beneath the question header and record *that* instead:
  1. Resolve `<MILESTONE_DIR>` by following `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` (never a hardcoded path).
  2. Read `<MILESTONE_DIR>/requirements.md` and find the contiguous `>`-prefixed blockquote run whose header — `> **Open question — <Short Title>:**` or `> **Deferred — <Short Title>:**` — matches the Short Title from step 1 (case-insensitive). Within that run, read the `> **Recommendation:** <chosen option> — <rationale>` anchor line embedded beneath the header.
  3. **No-embedded-recommendation guard:** if the block carries no `> **Recommendation:**` anchor (the recommend sweep never ran, or the question was added after it) — or if no block matches the Short Title at all — **stop without changing anything and commit nothing.** Report the situation and point the user to run `/recommend-all-open-questions` first, or to answer with literal text via `/answer-open-question <Short Title>. <answer text>`. (This is the skill's own clean no-commit stop — the same clean outcome the literal path gets from the shared procedure on a Short-Title mismatch.)
  4. Otherwise the `ANSWER` for step 3 is the anchor line's **content** — the `<chosen option> — <rationale>` text after the `> **Recommendation:** ` prefix, with the `>` and the `**Recommendation:**` label stripped — so what lands in `## Decisions` is clean prose, not blockquote markup.

Locating the block here and reading its anchor is *answer-derivation* — the wrapper's job — and is deliberately separate from the shared procedure's locate / analyse / remove / fold / cascade recording mechanism, which stays owned by `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` (step 3) and is not restated here. In sentinel mode the skill reads the block read-only to derive the answer; the shared procedure then re-locates and removes the whole run itself, unchanged.

### 3. Record the answer

Read and follow the shared answer-recording procedure at `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out every step **yourself, in this conversation**. Pass it the **Short Title** parsed in step 1 and the **answer text** resolved in step 2 as its `SHORT TITLE` and `ANSWER` inputs.

That procedure owns resolving the current milestone (the `<MILESTONE_DIR>` referenced below), locating the matching block, analysing the answer's implications, removing the block, folding the decision into `## Decisions`, and cascading to any entries the answer moots. Do not restate those steps here. If the Short Title matches no entry, the procedure stops without changes and reports the mismatch — relay that to the user so they can retry.

### 4. Commit the manual answer

**Only if step 3 actually recorded the answer** — i.e. the shared procedure folded a decision into `## Decisions` rather than stopping on a Short-Title mismatch — commit the edit. If the procedure stopped without changes, step 2's record-recommendation guard stopped (no embedded recommendation or no matching block), or step 1 hit a parse error, there is nothing to commit; do not run these commands.

Stage **only** this skill's own `requirements.md` edit — path-scoped, never `git add -A` — and commit it on its own, using the same `<MILESTONE_DIR>` resolved while recording:

```
git add <MILESTONE_DIR>/requirements.md
git commit -m "Manual-answer: <Short Title>" -m "<rationale / decision body>"
```

- **Subject:** exactly `Manual-answer: <Short Title>` (the answered question's handle), mirroring the sweep's `Principle-based-answer: <Short Title>` so `/capture-milestone-principle-updates` can collect these with `git log --grep='^Manual-answer: '`.
- **Body:** the decision's rationale — but record only rationale that genuinely exists in this conversation. Never prompt the user for a rationale and never fabricate one. When `/discuss-open-question` deliberation is in context, the body captures that reasoning. On a cold answer (no deliberation), the body is the answer text — the value resolved in step 2, i.e. the lifted `<chosen option> — <rationale>` in record-recommendation mode, never the sentinel phrase — recorded verbatim, including any inline "because" clause the user typed; when the answer states no reasoning, the body holds the bare decision. The answer string is itself the cold path's rationale affordance — add no separate rationale prompt.
- **No `Answer-Principle:` trailer.** That trailer is the sweep's signature; its absence is what marks this commit as a manual answer rather than an auto-answer.

This is a deliberate, documented exception to the project's "individual skills never commit" rule: `answer-open-question` commits exactly its own path-scoped manual-answer edit so that finish-time principle capture has a clean, greppable commit to walk. Staging path-scoped keeps the commit touching only `requirements.md` and never sweeps in unrelated working-tree changes, which also preserves the sweep's clean-tree precondition.

### 5. Report findings

After committing, briefly state:
- Which question was resolved and how the document changed (resolved block, decision folded into `## Decisions`, cascading resolutions).
- Any new open questions the answer may have introduced — surface these but do **not** add them to the document without user confirmation.

## Rules

- Parse on the **first** `.` only — Short Title before, answer text after.
- Record-recommendation mode is selected by the reserved sentinel answer text `record the recommendation`, matched as an **exact whole-string** comparison after trim + lowercase — **never a substring**. Any other answer text is a literal answer and takes the unchanged literal path.
- In record-recommendation mode the skill itself locates the targeted block and lifts its `> **Recommendation:** …` anchor content as the answer text passed to the shared procedure; if the block has no such anchor (or no block matches the Short Title), it stops without changes and commits nothing. This read-and-lift is answer-derivation, not the shared procedure's recording mechanism.
- The recording mechanism lives **only** in `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`; never duplicate or restate its locate / analyse / remove / fold / cascade steps here.
- Commit **only** when step 3 actually recorded the answer; a parse error, a Short-Title mismatch, or the record-recommendation no-anchor guard produces no commit.
- Stage path-scoped — `git add <MILESTONE_DIR>/requirements.md`, never `git add -A` — so the commit touches only `requirements.md`.
- The manual-answer commit carries the rationale in its **body** and **no** `Answer-Principle:` trailer. Committing here is a deliberate, documented exception to the "individual skills never commit" rule.
