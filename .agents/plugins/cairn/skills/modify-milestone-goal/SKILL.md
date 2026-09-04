---
name: modify-milestone-goal
description: Revise the Goal section of the current milestone's requirements.md when the objective itself needs to be reshaped, broadened, narrowed, or corrected.
---

# modify-milestone-goal

Replaces the `## Goal` of the current milestone's `requirements.md` with a revised goal statement, then surfaces what the change may have invalidated downstream — leaving those follow-up edits to the user. It is the only skill that edits the Goal of an *already-defined* milestone.

## Usage

```
/modify-milestone-goal <new or revised goal text>
```

- `<new or revised goal text>`: either a complete replacement goal statement, or a described change to fold into the existing one (e.g. "also cover a quick-reference section"). If it is a delta, integrate it against the current Goal rather than discarding what is still true.

**Example:**
```
/modify-milestone-goal Broaden the getting-started guide to walk a new user through their first week, not only their first session.
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

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.

### 6. Confirm

On the success path — the commit in step 5 recorded the revised goal — print exactly one fixed terse status line and nothing else:

```
Goal revised.
```

Do not add the before → after goal text, the downstream-impact analysis from step 3, the milestone id, or a next-step pointer. (The step-3 analysis still runs — it informs your own reasoning — but is not printed.)

If instead the step-5 dirty-own-path guard fired (the `## Goal` section was unchanged, so nothing was committed), do not print the terse line — print a single concise line stating that nothing changed and briefly why, e.g. `No change — the revised goal matched the existing one; nothing committed.`
