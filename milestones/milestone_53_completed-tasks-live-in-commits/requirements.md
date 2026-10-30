# Milestone 53: Completed tasks live in commits

## Goal

Make a completed task's whole record its `Task-completion:` commit, as "Carrying it out › 2. Completed tasks live in commits" of `ideas/milestones_addressed_by_path.md` proposes, delivering that step whole and nothing of step 3. `TASKS_DONE.md` goes: the task-list tool's `move` becomes `remove`, which removes one section and renders no bar and ignores a `TASKS_DONE.md` standing beside the list, the milestone-definition tool creates three files, and the verified bar becomes the body of the task's commit, written by the inline `complete-task` skill as its own commit's body and by the `complete-task` agent as a second fixed-name file beside `paths.txt` that the orchestrator's existing commit-from-file call passes as the body and moves into `processed` with it. The read-only milestones tool, `core/tools/milestones.py`, is born with `tasks PATH` in the draft's general form as its only query and everything a first query fixes, its read-only git contract, line shape, `Error:` line, tests on the shared git fixtures, and parity test; every reader of `TASKS_DONE.md` (`finish-current-milestone`, `derive-tasks`, `ask-in-milestone-context`, `submit-task`, `discuss-new-task`) reads `tasks` instead, every remaining mention of the file in runtime files, templates, docs, and tests goes, and the invariants, the fixed-call and parallel tests, and the rebuilt hosts follow. The milestone's last task revises the draft's Carrying it out, rewriting step 2 as a done section recording what landed and revising step 3 with whatever this milestone discovered; the pointer, `milestones/README.md`, finish's README entry, and the commit tool's contract are untouched.

## Relevant starting state

## Decisions

## Out of Scope

