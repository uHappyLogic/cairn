---
name: modify-milestone-goal
description: Revise the `## Goal` of the current milestone's requirements.md when a discussion reveals the goal itself — not just an open question — needs to change. Use when the user wants to reshape, broaden, narrow, or correct the objective of an already-defined milestone (e.g. "the goal should also cover X", "drop Y from the goal", "the goal is really about Z"). This is the only skill that mutates an existing milestone's Goal; it edits the Goal section only and surfaces — never auto-cascades — the downstream impact. It is offered by /discuss-open-question when a deliberation concludes the goal must shift, and is also directly invocable.
---

# modify-milestone-goal

Replaces the `## Goal` of the current milestone's `requirements.md` with a revised goal statement, then surfaces what the change may have invalidated downstream — leaving those follow-up edits to the user.

This is the only skill that edits the Goal of an *already-defined* milestone. `define-milestone-goal` writes the Goal once at creation; `discuss-milestone-goal` only shapes a goal conversationally before creation. When a milestone is live and its objective needs to move, this is the skill that records it. It is deliberately invisible to `answer-open-question` — recording a decision and reshaping the milestone's objective are different acts, and the autonomous answer/principle path must never reach goal mutation.

## Usage

```
/modify-milestone-goal <new or revised goal text>
```

- `<new or revised goal text>`: either a complete replacement goal statement, or a described change to fold into the existing one (e.g. "also support offline playback"). If it is a delta, integrate it against the current Goal rather than discarding what is still true.

**Example:**
```
/modify-milestone-goal Broaden the shooting mechanic so the player can fire at any enemy in line of sight, not only enemies on the same spline segment.
```

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded path.

### 1. Read the current Goal

Read `<MILESTONE_DIR>/requirements.md` and locate the `## Goal` section. Show the user the current goal text so the change is reviewable against what it replaces.

### 2. Determine the revised Goal

From the argument, settle on the new Goal prose:

- If the argument is a full replacement, use it (lightly cleaned for clarity).
- If it is a delta ("also…", "drop…", "really about…"), integrate it with the existing Goal so the result is a single coherent statement, preserving the parts still true.

If the intended change is genuinely ambiguous, state the revised wording you propose and confirm it with the user before writing. The Goal is the root of the whole requirements tree — getting its wording right matters more than acting fast.

### 3. Analyse the impact (before editing)

Reason about what the new goal may have invalidated. Do **not** write this analysis into the document and do **not** edit those sections — this is to inform what you surface in step 5:

- Which `## Decisions` entries the new goal contradicts, moots, or leaves dangling.
- Which open or `Deferred` questions it newly settles, newly opens, or makes irrelevant.
- Which `## Out of Scope` entries the new goal now pulls back in (or pushes out).
- If `TASKS_TODO.md` / `TASKS_DONE.md` already hold tasks, which derived or completed tasks the new goal strands, contradicts, or leaves unaddressed.

### 4. Edit only the Goal

Replace the body of the `## Goal` section with the revised goal text. Touch nothing else — not `## Decisions`, not the questions, not `## Out of Scope`, not the task lists. A single targeted edit, not a rewrite of the file.

### 5. Commit the goal revision

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: `<MILESTONE_DIR>/requirements.md` (the file whose `## Goal` section it just revised).
- **SUBJECT** — `Goal-revision: <milestone_id>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit — do not restate those mechanics here.

### 6. Confirm

On the success path — the commit in step 5 recorded the revised goal — print exactly one fixed terse status line and nothing else:

```
Goal revised.
```

Do not add the before → after goal text, the downstream-impact analysis from step 3, the milestone id, or a next-step pointer; the committed diff and git log are the durable record. (The step-3 analysis still runs — it informs your own reasoning — but it is no longer printed.)

If instead the step-5 dirty-own-path guard fired (the `## Goal` section was unchanged, so nothing was committed), do not print the terse line — print a single concise line stating that nothing changed and briefly why, e.g. `No change — the revised goal matched the existing one; nothing committed.`

## Rules

- Edit **only** the `## Goal` section. This skill never records decisions, answers questions, edits Out-of-Scope, or touches the task lists.
- **Surface, never cascade.** The downstream consequences of a goal change are for the user to resolve (via `/review-milestone-requirements` and the answer/task skills) — never auto-apply them. The blast radius of a goal change is too large to fold in silently.
- A goal change is not an answering decision and produces no reusable answering principle — this skill never feeds into principle capture.
- Confirm the revised wording with the user when the intended change is ambiguous; the Goal is load-bearing.
