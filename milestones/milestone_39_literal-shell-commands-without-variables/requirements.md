# Milestone 39: Literal shell commands without variables

## Goal

Stop Cairn runs from failing where a shell does not split an unquoted variable into words. Add a shell-neutral prose rule at the two provoking sites: `core/shared/commit-procedure.md` names each path literally in both the dirty-own-path check and the `git add`, never through a shell variable; and the multi-call open-question tool sites (`review-milestone-requirements`, the two annotating passes, the answer sweep, and `answer-procedure.md`) write the full fixed command on every call, never through a variable, alias, or function. The rationale is recorded in the `CLAUDE.md` invariants. Done when `hosts/` is rebuilt, `--check` passes, and both pytest runs pass. A structural fix, such as a commit tool, is out of scope.

## Relevant starting state

## Decisions

## Out of Scope

