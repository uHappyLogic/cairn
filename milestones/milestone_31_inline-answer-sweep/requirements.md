# Milestone 31: Inline answer sweep

## Goal

Make `/answer-all-open-questions-with-recommendation` an inline single-writer skill that dispatches no agent: it gathers the dispatch order with one `walk` call, reads the question set once for context, then for each question in that order runs the shared answer-with-recommendation procedure itself (lift as the re-check, locate, fold, remove with the lifted option, cascade) and commits that answer through the shared commit procedure under the unchanged `Recommendation-answer: <Short Title>` subject with the lifted line as body, one commit per answer, unattended. It records every surviving pick as given and never judges picks; a contradiction it happens to notice is reported once alongside the terse status line while the run proceeds. The end-of-run check is the cheap one: `walk` prints nothing beyond the blocks the cascades stripped, reported as the existing still-skipped advisory, with no document re-read. The `answer-open-question-with-recommendation` agent is deleted as its only consumer goes inline; the single-question skill, the shared procedures' contracts, and the capture path stay untouched, and the CLAUDE.md invariants, skill reference, workflow, design claims, headless chains, and both host trees are updated to the two-agent, inline-sweep shape.

## Relevant starting state

## Decisions

## Out of Scope

