# Milestone 19: Principle Capture By Milestone

## Goal

Rework `capture-milestone-principle-updates` into an argument-driven harvester: it requires a milestone id, drops the last-completed-row resolution, and infers that milestone's decision history itself from the answer commits on its `requirements.md` across all three provenances (`Manual-answer:`, `Alternative-answer:`, `Recommendation-answer:`), reconstructing from each commit's diff the recommendation and cited principles the user saw against the answer they recorded. Manual and alternative answers are the override signal: at capture time the skill asks the user why the alternative was preferred (offering its own best guess) and distills from those overrides the compact, intuitive guideline the recommender lacked, so future recommendations are accepted more often and manual or alternative answers become rarer. The store may shrink as well as grow: current reasoning takes precedence over an existing entry it contradicts, with capture pruning, merging, or generalizing entries, salvaging what it can from a decommissioned rule, and keeping each entry as short as it can be while still reading as an intuitive rule.

## Relevant starting state

## Decisions

## Out of Scope

