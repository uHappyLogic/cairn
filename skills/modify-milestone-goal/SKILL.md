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

### 5. Report and hand off

Briefly state:

- **Before → after** — the old goal and the new goal.
- **Downstream impact** — the specific Decisions, questions, Out-of-Scope entries, and (if tasks exist) tasks from step 3 that the change may have invalidated. Be concrete; name them.
- **Recommended next step** — re-run `/review-milestone-requirements` to reconcile the requirements against the new goal. If tasks were already derived, call out that they likely need revisiting before completion.

## Rules

- Edit **only** the `## Goal` section. This skill never records decisions, answers questions, edits Out-of-Scope, or touches the task lists.
- **Surface, never cascade.** The downstream consequences of a goal change are for the user to resolve (via `/review-milestone-requirements` and the answer/task skills) — never auto-apply them. The blast radius of a goal change is too large to fold in silently.
- Never chain into `/try-capture-answer-principle` — a goal change is not an answering decision and produces no reusable answering principle.
- Confirm the revised wording with the user when the intended change is ambiguous; the Goal is load-bearing.
- Do not commit — leave the change staged for the user to review.
