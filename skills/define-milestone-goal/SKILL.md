---
name: define-milestone-goal
description: Create a new milestone directory with initialized requirements.md (Goal filled from the provided description) and empty TASKS files.
---

# define-milestone-goal

Creates a new milestone directory under `milestones/` with a `requirements.md` pre-filled with the goal, plus empty `TASKS_TODO.md` and `TASKS_DONE.md`. Does not populate the remaining sections — those are filled by subsequent skills (`/specify-milestone-starting-state`, `/review-milestone-requirements`, etc.). Defining a milestone does not activate it: this skill never updates `CLAUDE.md` or `milestones/README.md`, which change only when the milestone becomes the *current* active one via `/goto-next-milestone`.

## Usage

```
/define-milestone-goal <overall_goal_description>
```

- `<overall_goal_description>`: a clear description of what the milestone should accomplish. Use `/discuss-milestone-goal` first if the goal is still vague.

**Example:**
```
/define-milestone-goal add a getting-started guide that walks a new user through their first session
```

## Workflow

### 1. Determine the milestone number

Scan the `milestones/` directory for subdirectories whose names match the pattern `milestone_<NN>_*` (e.g. `milestone_01_public-release-prep`). For each matching directory, extract the numeric prefix and parse it as an integer, stripping any leading zeros (`01` → `1`, `09` → `9`). Take the maximum integer found and add 1 to get the next milestone number. Format the result zero-padded to two digits (e.g. `1` → `01`, `9` → `09`, `10` → `10`).

If `milestones/` contains no matching directories (cold start), treat the maximum as `0`, so the first milestone number is `1`, formatted `01`.

Do not read the milestone number from `CLAUDE.md` or from `milestones/README.md`'s pointer — the scan is the sole source.

### 2. Derive the milestone slug

Convert `<overall_goal_description>` to a short kebab-case slug (3–5 words max) that captures the essence of the goal. The full directory name is `milestone_<NN>_<slug>` where `<NN>` is the zero-padded two-digit number from step 1.

**Example:** "add a getting-started guide that walks a new user through their first session" → `milestone_12_getting-started-guide` (if the next number happens to be 12)

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

## Decisions

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

### 5. Commit the new milestone

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: the three files it just created — `milestones/milestone_<NN>_<slug>/requirements.md`, `milestones/milestone_<NN>_<slug>/TASKS_TODO.md`, and `milestones/milestone_<NN>_<slug>/TASKS_DONE.md`.
- **SUBJECT** — `Milestone-definition: milestone_<NN>_<slug>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.

### 6. Confirm

On the success path — the commit in step 5 recorded the new milestone — print exactly one fixed terse status line and nothing else:

```
Milestone defined.
```

Do not add the created directory path, the goal text, or a next-step pointer.

If instead the step-5 dirty-own-path guard fired (none of the three files changed, so nothing was committed), do not print the terse line — print a single concise line stating that nothing changed and briefly why, e.g. `No change — the milestone files already existed; nothing committed.`
