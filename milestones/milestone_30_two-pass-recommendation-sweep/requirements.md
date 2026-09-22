# Milestone 30: Two-pass recommendation sweep

## Goal

Split the recommend sweep in two: a new `/provide-alternatives-to-all-open-questions` skill dispatches a renamed alternatives-only agent in parallel, one per question lacking alternatives, embedding and committing each return as it lands, while `/recommend-all-open-questions` becomes an inline skill that dispatches no agents, stops when any question lacks alternatives, reasons over the whole question set at once to embed a `<recommendation>` and its `<depends-on>` declarations per block against frozen alternatives, and commits once per run with its reasoning in the commit body before the end-of-run sort. Narrow every option-less removal and every disagreeing dependent in the tool's cascade so it clears only the `<recommendation>`, `<depends-on>`, and `<applied-principle>` children and keeps the `<alternative>` children, transitively as today, so an override needs only a re-run of the recommendation pass; the tool gains the partial strip, a `list` filter for blocks without alternatives, and a two-shape `embed`. `/discuss-open-question` works on a question in any state, reusing embedded alternatives when present and producing both halves when bare, and the pipeline docs, skill reference, workflow diagrams, headless chains, and CLAUDE.md invariants are updated to the two-pass shape.

## Relevant starting state

## Decisions

## Out of Scope

