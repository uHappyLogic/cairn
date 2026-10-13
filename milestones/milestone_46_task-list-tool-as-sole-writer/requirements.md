# Milestone 46: Task-list tool as sole writer

## Goal

Add a stdlib-only Python 3.9+ task-list tool under `core/tools/` that becomes the only writer of a milestone's `TASKS_TODO.md` and `TASKS_DONE.md` once `define_milestone.py` has created them: it moves one task section TODO→DONE with its `**Verified:**` bar read from stdin for the completion procedure, inserts a positioned section for `submit-task`, and initializes and appends sections for `derive-tasks`, so the `##`/`---` parsing and the Verified rendering leave runtime prose for a tested tool and the ad-hoc move scripts are retired. Every runner that writes a task file chains the tool call with the git step it owns in one shell call, the `complete-task` agent its path-scoped `git add` and the inline runners their commit procedure, so the completion tail becomes one turn. The tool touches no git, reads of the task files stay as they are, and the milestone ships the tool, its tests under both interpreters, the updated prose, docs, and `CLAUDE.md` invariants, and the rebuilt host trees passing `--check`.

## Relevant starting state

## Decisions

## Out of Scope

