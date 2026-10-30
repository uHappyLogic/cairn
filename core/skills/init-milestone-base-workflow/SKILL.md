---
name: init-milestone-base-workflow
description: Bootstrap the milestone workflow in a project by ensuring {{CONTEXT_FILE}} carries the path-addressed milestone workflow guidance.
---

# init-milestone-base-workflow

Bootstraps the milestone-driven workflow inside a project. Its whole duty is `{{CONTEXT_FILE}}`: it ensures that file carries the `## Milestone Workflow` guidance, which tells anyone working in the project where milestones live and how each is named and finished. It probes nothing and creates no `milestones/` directory or other scaffold — `/define-milestone-goal` checks the workflow's runtime prerequisites each time it runs and creates a scope's `milestones/` container with the first milestone placed there. Run this **once** per project, before any other workflow skill.

This skill is additive and idempotent: it creates `{{CONTEXT_FILE}}` when it is missing and appends the section when the file lacks it, but never overwrites or rewrites content that is already there. It commits `{{CONTEXT_FILE}}` alone as one path-scoped commit.

## Usage

```
/init-milestone-base-workflow
```

No arguments.

## Workflow

### 1. Detect existing state

Check whether `{{CONTEXT_FILE}}` exists at the workspace root. If it does, read it and note whether it already contains a `## Milestone Workflow` section — any section under that heading, whatever its text says, an older one included.

If the section is present, the project is already bootstrapped: stop without changing anything and committing nothing, and print this one line and nothing else:

```
Workflow already bootstrapped — the guidance section is present.
```

### 2. Write the workflow guidance into {{CONTEXT_FILE}}

Write the `## Milestone Workflow` section exactly as `{{PLUGIN_ROOT}}/shared/workflow-guidance.md` states it, by the one of that file's first two cases that applies: **if `{{CONTEXT_FILE}}` does not exist**, create it with the minimal content shown there; **if it exists and lacks the section**, append the section to the end of the file, leaving every existing line untouched. Never its third case: a section already present ended the run in step 1, and this skill rewrites nothing.

### 3. Commit the bootstrap

Read and follow the shared commit procedure at `{{PLUGIN_ROOT}}/shared/commit-procedure.md`, running its one commit-tool command yourself as this step's one git tool call. Supply it these two inputs:

- **PATHS** — this skill's own change set: `{{CONTEXT_FILE}}` alone, which step 2 created or appended the section to.
- **SUBJECT** — `Workflow-bootstrap: milestones`.

Supply no BODY: the commit is subject-only. Hand the path over unchanged — uncommitted changes already present in `{{CONTEXT_FILE}}` before this run (for example a file just written by `/init`) are swept into this commit, with no status probe beforehand, no stop, no confirmation, no hunk-level staging, and no advisory.

The commit tool runs the dirty-own-path guard, the path-scoped staging, and the commit.

### 4. Confirm

On the success path — the commit in step 3 recorded the bootstrap — print exactly one fixed terse status line and nothing else:

```
Workflow bootstrapped.
```

Do not say whether the file was created or appended to, name the commit, or add any next-step or handoff pointer; the commit diff shows what was written.

If instead the step-3 commit tool printed `Nothing committed — none of the paths changed.` (the file already matched the last commit, so nothing was committed), do not print the terse line — print this one fixed line and nothing else:

```
Bootstrap committed nothing — the guidance already matched the last commit.
```
