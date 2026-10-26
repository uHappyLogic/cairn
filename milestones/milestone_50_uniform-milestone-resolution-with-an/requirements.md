# Milestone 50: Uniform milestone resolution with an override flag

## Goal

Every skill that operates on a milestone resolves it the same way: through the shared pointer procedure by default, or through one optional leading --milestone <milestone_id> flag that names a milestone directory and overrides the pointer. specify-milestone-starting-state loses its required positional id and joins the sixteen pointer-resolving skills under this rule, get-current-milestone.md gains the override as its one input, a named override that matches no milestone directory stops on an error line with no fallback to the pointer, an override is honoured even when the pointer reads none, and complete-all-tasks forwards the override to its dispatched agent. capture-milestone-principle-updates keeps its required positional id as the stated exception. The docs that spell the old argument (the skill-reference heading, the headless chain line and placeholder list in ways-of-using-cairn.md) are updated, and CLAUDE.md records the resolution rule as an invariant.

## Relevant starting state

## Decisions

## Out of Scope

