# Milestone 35: Committing Bootstrap

## Goal

Retire the bootstrap's non-committing exemption so that every file-changing Cairn skill commits its own paths and a headless chain leaves no uncommitted files behind. init-milestone-base-workflow gains a git work-tree prerequisite check beside its Python check, stopping before it writes anything when the project is not a git repository, and commits the files it created or edited (milestones/README.md, and CLAUDE.md when it touched it) through the shared commit procedure under its own function-derived subject. The invariant in CLAUDE.md, the exemption paragraph in docs/workflow.md, and the skill reference are updated to match. The benchmark harness side of G04 is out of scope.

## Relevant starting state

## Decisions

## Out of Scope

