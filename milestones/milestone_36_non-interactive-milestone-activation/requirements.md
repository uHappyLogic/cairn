# Milestone 36: Non-interactive milestone activation

## Goal

`/goto-next-milestone` runs without asking anything. It activates the lowest-numbered milestone directory that isn't listed in `## Milestone History`. It stops only in two cases: the `Current milestone:` pointer doesn't read `none` (it tells you to run `/finish-current-milestone`), or no undone milestone exists (it tells you to run `/define-milestone-goal`). The single-candidate confirmation and the multiple-candidate choice are removed, the terse `Milestone activated.` line stays, and `docs/skill-reference.md`, `docs/ways-of-using-cairn.md` and the rebuilt host trees are updated to match.

## Relevant starting state

## Decisions

## Out of Scope

