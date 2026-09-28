---
name: init-milestone-base-workflow
description: Bootstrap the milestone workflow in a project by creating the milestones/ directory and milestones/README.md, and ensuring CLAUDE.md carries the workflow guidance.
---

# init-milestone-base-workflow

Bootstraps the milestone-driven workflow inside a project. It first checks that the workspace root lies inside a git work tree, then that a Python 3.9 or later interpreter answers as `python3` — the two runtime prerequisites of the workflow skills — and stops before writing anything when either check fails. It then creates the `milestones/` directory and `milestones/README.md` (with the grep-able `Current milestone:` pointer line), and ensures `CLAUDE.md` contains the `## Milestone Workflow` guidance. Run this **once** per project, before any other workflow skill.

This skill is additive and idempotent: it creates missing scaffolding and inserts missing sections into existing files, but never overwrites or rewrites content that is already there. It commits the files it created or edited as one path-scoped commit.

## Usage

```
/init-milestone-base-workflow
```

No arguments.

## Workflow

### 1. Check the git prerequisite

This skill and the workflow skills commit their own changes with git, so every project this skill bootstraps needs its workspace root inside a git work tree. Check it here, first, before the Python check and the state detection and on every invocation — a re-run on an already-bootstrapped project gets the same check.

Run `git rev-parse --is-inside-work-tree` once, in the workspace root. If it prints `true`, the check passes: continue to step 2. It passes anywhere inside a work tree — a subdirectory of a larger repository, or a freshly initialized repository with no commits yet — with no existing commit required, no match with the repository's top level required, and no advisory printed when the two differ.

Otherwise — the shell reports `git` as not found, or the probe prints `false` or fails with a not-a-repository error — **stop before any write**: create and edit nothing, prompt for nothing, and never run `git init` yourself. Print one full message that states, in order:

- **What it looked for** — a git work tree at the workspace root.
- **What it found** — that the `git` executable is missing, or that the directory is not a work tree.
- **The remedy** — install git when the executable is missing; otherwise run `git init` in the workspace root.
- **That a re-run completes the bootstrap** — once the remedy is applied, run `/init-milestone-base-workflow` again; it picks up with nothing to undo, since this stop wrote nothing.

This stop is separate from the Python check's: a project failing both learns about git here and about Python on the next run.

### 2. Check the Python prerequisite

The workflow skills drive the plugin's open-question tool as `python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py`, so every project this skill bootstraps needs a Python 3.9 or later interpreter reachable as `python3`. Check it here, after the git check, before the state detection and on every invocation — a re-run on an already-bootstrapped project gets the same check.

Run `python3 --version`. If it prints a version of 3.9 or later, the check passes: continue to step 3. Compare the version numerically, minor by minor — `3.10` and `3.13` are later than `3.9`, `3.8` is not.

Otherwise — `python3` is not found, or it reports a version below 3.9 — run `python --version` as well. Its result decides nothing about passing; it only makes the message below precise. Then **stop before any write**: create and edit nothing, and print one full message that states, in order:

- **What it looked for** — a Python 3.9 or later interpreter answering as `python3`, and failing that as `python`.
- **What it found** — for each of the two names, that it was not found or the exact version it reported.
- **The remedy** — when `python` reported 3.9 or later, that interpreter exists under the other name and must be exposed as `python3` (a `python3` symlink or alias on the PATH, or the platform's equivalent); otherwise install Python 3.9 or later so that `python3` resolves to it.
- **That a re-run completes the bootstrap** — once `python3 --version` reports 3.9 or later, run `/init-milestone-base-workflow` again; it picks up with nothing to undo, since this stop wrote nothing.

### 3. Detect existing state

Probe the workspace root in parallel and record what already exists:

- Does `milestones/` exist?
- Does `milestones/README.md` exist? If so, does it contain a `Current milestone:` line?
- Does `CLAUDE.md` exist? If so, read it and note whether it already contains a `## Milestone Workflow` section.

Use these findings to decide which steps below are no-ops. If **all** of the following are already present — `milestones/`, `milestones/README.md`, and a `Current milestone:` line in `milestones/README.md` — the project is already initialized: stop without changing anything and print this one line and nothing else:

```
Workflow already bootstrapped — nothing changed.
```

### 4. Create the milestones/ directory

If `milestones/` does not exist, create it. Create no `milestone_<N>_<slug>/` directory inside it — that is `/define-milestone-goal`'s job.

### 5. Create milestones/README.md

If `milestones/README.md` does **not** exist, create it with this exact structure:

```markdown
# Milestones

This file is the source of truth for which milestone is current.

Each milestone lives at `milestones/milestone_<N>_<slug>/` and contains:

- `requirements.md` — goal, relevant starting state, decisions, out of scope
- `open_questions.xml` — the open questions, one `<open-question>` block each under a single `<open-questions>` root, written only by the plugin's open-question tool
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks

## Current Milestone

Current milestone: none

## Milestone History

_No milestones completed yet._

## Completed Milestones

| # | Title | Path |
|---|-------|------|
```

If `milestones/README.md` **already exists**, do not overwrite it. Instead, ensure it contains a `## Current Milestone` section with a `Current milestone:` line; if either is missing, insert the section (with `Current milestone: none`) after the file's top-level heading, and leave the rest of the file untouched.

### 6. Ensure CLAUDE.md carries the workflow guidance

**If `CLAUDE.md` does not exist**, create it with this minimal content:

```markdown
# CLAUDE.md

This file provides guidance to the coding agent working in this repository.

## Milestone Workflow

This project uses the milestone-driven workflow. Each milestone lives at
`milestones/milestone_<N>_<slug>/` with `requirements.md`, `open_questions.xml`,
`TASKS_TODO.md`, and `TASKS_DONE.md`. `milestones/README.md` is the source of truth for
which milestone is current. Never advance the pointer without first running
`/finish-current-milestone`.
```

**If `CLAUDE.md` already exists**, update it without disturbing existing content:

- If it has **no** `## Milestone Workflow` section, append the `## Milestone Workflow` section (the paragraph shown above) to the end of the file.
- If the section already exists, leave it exactly as-is — do not rewrite or re-template it.

Never write a current-milestone pointer into `CLAUDE.md`; the pointer lives only in `milestones/README.md`. Never document the project's environment context in `CLAUDE.md` yourself either.

### 7. Commit the bootstrap

Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: **always** `milestones/README.md` (created or edited in step 5), and **additionally** `CLAUDE.md` **only on runs where step 6 created it or appended the `## Milestone Workflow` section to it**. When step 6 left an existing section as-is, `CLAUDE.md` is not in the set and the commit covers `milestones/README.md` alone. This conditional inclusion is keyed on whether this skill's step 6 made the edit — decided as the edit is (or is not) made, never by diffing or inspecting content.
- **SUBJECT** — `Workflow-bootstrap: milestones`.

Supply no BODY: the commit is subject-only. Hand the paths over unchanged — uncommitted changes already present in them before this run (for example a `CLAUDE.md` just written by `/init`) are swept into this commit, with no status probe beforehand, no stop, no confirmation, no hunk-level staging, and no advisory.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.

### 8. Confirm

On the success path — the commit in step 7 recorded the bootstrap — print exactly one fixed terse status line and nothing else:

```
Workflow bootstrapped.
```

Do not list which items were created or left untouched, the pointer's initial value, the commit, or any next-step or handoff pointer; the commit diff shows which files were created or appended to.

If instead the step-7 dirty-own-path guard fired (none of the paths changed, so nothing was committed), do not print the terse line — print a single concise line stating that nothing changed and briefly why, e.g. `No change — the scaffold was already committed; nothing committed.`
