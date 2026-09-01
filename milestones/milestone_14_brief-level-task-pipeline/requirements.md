# Milestone 14: Brief-level task pipeline

## Goal

Flatten the task pipeline to brief-level tasks: derive-tasks writes its ordered briefs directly into TASKS_TODO.md (same ## heading + --- section format, brief-level detail only — no Provides/Notes/Success sections), retiring the submit-task agent and the per-brief dispatch loop. shared/complete-procedure.md is reworked to derive each task's acceptance bar itself from the task description plus requirements.md, and to resolve cross-task references by reading prior tasks' live deliverables (tasks run in order). The user-facing submit-task skill is leaned down to author the same brief-level format, keeping all tasks in TASKS_TODO.md at one consistent altitude; CLAUDE.md invariants and README.md are reconciled to the flattened design.

## Relevant starting state

## Decisions

## Out of Scope

