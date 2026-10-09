# Milestone 44: Batched recommendation embeds in one shell call

## Goal

The recommendation pass's post-decision mechanics become one fixed shell call, shown in full in `recommend-all-open-questions` and run exactly as shown: for every picked block it runs the existing `embed --recommendation` heredoc followed by that block's `lift`, then commits `open_questions.xml` once under `Recommendation-annotation: <milestone_id>` with the lifted lines captured as the body, then sorts the document and commits the reorder behind the dirty-path guard. Each `embed` stays its own process, so every valid block is written and each refused block prints its own `Error:` line while the rest land and commit; the runner corrects only the refused blocks and re-sends them in one more call of the same shape, which commits and sorts again, so a run commits once per batch call rather than once per run. The open-question tool is not required to change, but a tool change that shortens the call (a multi-block `embed --recommendation` that prints the lifted line per accepted block) is in scope if it earns its place. `CLAUDE.md`, `docs/`, and the rebuilt host trees restate the pass accordingly.

Out of scope: the alternatives pass, the answer sweep, a task-list tool for the completion move, and any change to how picks are formed.

## Relevant starting state

## Decisions

## Out of Scope

