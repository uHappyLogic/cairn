---
name: define-milestone-goal
description: Create a new milestone directory with initialized requirements.md (Goal filled from the provided description) and empty TASKS files.
---

# define-milestone-goal

Creates a new milestone directory under `milestones/` with a `requirements.md` pre-filled with the goal, plus empty `TASKS_TODO.md` and `TASKS_DONE.md`. Does not populate the remaining sections — those are filled by subsequent skills (`/specify-milestone-starting-state`, `/highlight-milestone-requirements-open-questions`, etc.).

## Usage

```
/define-milestone-goal <overall_goal_description>
```

- `<overall_goal_description>`: a clear description of what the milestone should accomplish. Use `/discuss-milestone-goal` first if the goal is still vague.

**Example:**
```
/define-milestone-goal add a shooting mechanic where the player fires a single projectile at enemies on the same spline segment
```

## Workflow

### 1. Determine the milestone number

Scan the `milestones/` directory for subdirectories whose names match the pattern `milestone_<NN>_*` (e.g. `milestone_01_public-release-prep`). For each matching directory, extract the numeric prefix and parse it as an integer, stripping any leading zeros (`01` → `1`, `09` → `9`). Take the maximum integer found and add 1 to get the next milestone number. Format the result zero-padded to two digits (e.g. `1` → `01`, `9` → `09`, `10` → `10`).

If `milestones/` contains no matching directories (cold start), treat the maximum as `0`, so the first milestone number is `1`, formatted `01`.

Do not read the milestone number from `CLAUDE.md` or from `milestones/README.md`'s pointer — the scan is the sole source.

### 2. Derive the milestone slug

Convert `<overall_goal_description>` to a short kebab-case slug (3–5 words max) that captures the essence of the goal. The full directory name is `milestone_<NN>_<slug>` where `<NN>` is the zero-padded two-digit number from step 1.

**Example:** "add a shooting mechanic where the player fires a single projectile" → `milestone_12_player-shooting` (if the next number happens to be 12)

### 3. Check for conflicts

Verify that `milestones/milestone_<NN>_<slug>/` does not already exist. If a milestone with that number exists under any slug, stop and report the conflict.

### 4. Create the milestone directory

Create `milestones/milestone_<NN>_<slug>/` with three files. Use the zero-padded `<NN>` in the directory name and the integer (leading zeros stripped) `<N>` in the `requirements.md` heading.

**`requirements.md`:**
```markdown
# Milestone <N>: <title>

## Goal

<overall_goal_description>

## Relevant starting state

## Implementation decisions

## Out of Scope

```

**`TASKS_TODO.md`:**
```markdown
# TASKS TODO

```

**`TASKS_DONE.md`:**
```markdown
# TASKS DONE

```

### 5. Confirm

Report:
- New milestone directory created: `milestones/milestone_<NN>_<slug>/`
- The goal written into `requirements.md`
- Suggest the next step: `/specify-milestone-starting-state milestone_<NN>_<slug>` to fill in the starting state section.

## Rules

- Do not update `CLAUDE.md` or `milestones/README.md` — those are only updated when the milestone becomes the *current* active milestone via `/goto-next-milestone`.
- Do not populate `## Relevant starting state`, `## Implementation decisions`, or `## Out of Scope` — leave them empty for later skills.
- Do not assign the milestone as current — defining a milestone does not activate it.
- Never overwrite an existing milestone directory.
- Do not commit — leave staging to the user.
