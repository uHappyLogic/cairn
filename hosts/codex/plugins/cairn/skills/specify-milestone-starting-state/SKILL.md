---
name: specify-milestone-starting-state
description: Analyze the project's existing state and fill the "Relevant starting state" section of a milestone's requirements.md with context that supports future decisions.
---

# specify-milestone-starting-state

Writes the `## Relevant starting state` section of the named milestone's `requirements.md` through the shared starting-state procedure: on a first run it writes the empty section into existence, and on a re-run after the ground moved it refreshes the filled section in place. The output is reference material — not decisions — to ground the `## Decisions` conversation that follows.

## Usage

```
/specify-milestone-starting-state --milestone <path>
```

The required leading `--milestone <path>` names the milestone by its repo-relative path, exactly as the definition tool printed it, trailing slash included, e.g. `milestones/user-guide/`.

**Example:**
```
/specify-milestone-starting-state --milestone milestones/user-guide/
```

## Workflow

### 1. Find the milestone

Follow `${PLUGIN_ROOT}/shared/resolve-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded path.

### 2. Write the starting state

Read and follow the shared starting-state procedure at `${PLUGIN_ROOT}/shared/starting-state-procedure.md`, with `<MILESTONE_DIR>` as its input. It serves a first run and a refresh alike, so take the section as it finds it, empty or filled. Its step 1 decides which run this is, and the procedure then ends in exactly one of three ways:

- **The anchor alone** — its step 1 found the ground unmoved, so it explored, edited, and cleared nothing. Make no commit and skip to step 4.
- **A stop** — it stopped on one of its two fixed lines, `Starting state stopped — a milestones-tool read failed.` or `Starting state stopped — clearing the undermined picks failed.`, with the detail the procedure gives beneath it. That report, as the procedure states it, is this skill's whole report: make no commit, print nothing further, and end the run.
- **The change handed back** — it ran through its step 7, with `requirements.md` edited or left as it stood, and `open_questions.xml` changed exactly when its step 6 cleared a pick. Go on to step 3.

### 3. Commit the starting state

Read and follow the shared commit procedure at `${PLUGIN_ROOT}/shared/commit-procedure.md`, running its one commit-tool command yourself as this step's one git tool call. Supply it these two inputs:

- **PATHS** — this skill's own change set: `<MILESTONE_DIR>/requirements.md` (the file whose `## Relevant starting state` section the procedure wrote), and `<MILESTONE_DIR>/open_questions.xml` beside it only when the procedure's step 6 cleared a pick, so a refresh and the picks it cleared are one commit.
- **SUBJECT** — `Starting-state: <MILESTONE_DIR>`, the milestone path exactly as resolved, trailing slash included.

The commit tool runs the dirty-own-path guard, the path-scoped staging, and the commit.

### 4. Confirm

On the success path — the commit in step 3 recorded the written or refreshed starting state — print exactly one fixed terse status line and nothing else:

```
Starting state recorded.
```

Do not add the milestone path, the count of systems documented, the picks the procedure cleared, or a next-step pointer.

If instead the step-3 commit tool printed `Nothing committed — none of the paths changed.` (the procedure explored and left `requirements.md` as it stood, so nothing was committed), do not print the terse line — print this one fixed line and nothing else:

```
Starting state unchanged — nothing committed.
```

If the procedure ended on the anchor alone in step 2 (the ground had not moved, so nothing was explored and nothing was committed), print this one fixed line and nothing else:

```
Starting state current — the ground has not moved since it was recorded.
```
