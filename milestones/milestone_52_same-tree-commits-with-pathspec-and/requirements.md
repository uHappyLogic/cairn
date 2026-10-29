# Milestone 52: Same-tree commits with pathspec and retry

## Goal

Make every skill-layer commit record exactly its own change set and survive another run's git lock, so several `complete-all-tasks` runs can share one working tree, as "Carrying it out › 1. Same-tree commits" of `ideas/milestones_addressed_by_path.md` proposes, plus the orchestrator's commit-from-file pulled forward from its second milestone. The commit procedure commits with its paths as the pathspec and repeats each failed git write a bounded number of times before passing git's message on, every call that inlines its three steps follows, and the completion agent stops staging and instead writes the paths it created or edited to a file in the run's scratch directory, which `complete-all-tasks` creates with `mktemp -d`, passes on every dispatch, and commits each task from in one call, its whole-index guard retired. The completion procedure's resumption rule names another run's live work beside a previous run's partial work; one simple test runs two milestones' tasks in parallel in one repository and asserts each commit carries only its own paths; the committing and return-contract invariants and the docs follow; the task-list tool, `TASKS_DONE.md`, the commit body, the milestones tool, and the pointer are untouched.

## Relevant starting state

## Decisions

## Out of Scope

