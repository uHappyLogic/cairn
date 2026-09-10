# Milestone 21: Recommendation Dependency Graph

## Goal

Make `recommend-all-open-questions` dispatch sequentially in most-significant-first order, embedding each result before the next dispatch, so every recommendation may build on sibling recommendations already embedded and must declare each such use as a `<depends-on question="Short Title" option="Option"/>` child of its block, pointing only at still-open siblings. Extend the shared answer procedure's cascade so that recording an answer either removes the dependents' matching tags when the recorded option agrees with what they assumed, or strips the dependents' embedded children transitively when it disagrees (an exact id comparison for alternative and recommendation answers, a judgment of whether the recorded answer invalidates the assumed option for manual answers), leaving those blocks for the next recommend sweep to regenerate; the answer sweep walks the dependency graph from its origins. Retires the recommendation-independence invariant.

## Relevant starting state

## Decisions

## Out of Scope

