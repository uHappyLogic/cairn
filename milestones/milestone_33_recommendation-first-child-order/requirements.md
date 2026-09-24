# Milestone 33: Recommendation-first child order

## Goal

Change the open-question tool's canonical child order so that a block carrying a `<recommendation>` renders, after its `<question>`, its `<applied-principle>` and `<depends-on>` elements, then the `<recommendation>`, then the alternative the recommendation names, then the remaining alternatives in their existing relative order; a block without a recommendation keeps today's order. The reordering lives entirely in the tool's renderer, so it is deterministic and applied on every write, with no skill prose positioning elements. `sort` keeps ordering blocks only, and a block keeps its reordered alternatives after `strip --recommendation`.

## Relevant starting state

## Decisions

## Out of Scope

