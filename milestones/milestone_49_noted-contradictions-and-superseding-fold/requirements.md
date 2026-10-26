# Milestone 49: Noted contradictions and superseding fold

## Goal

When a single-question answer skill's analyse step finds that the decision it records conflicts with a standing `## Decisions` entry, it saves the pair under a new `## Noted contradictions` section of `requirements.md`, where the next `/review-milestone-requirements` pass turns each note into one open question asking which entry stands and deletes the note; the answer sweep keeps forming no contradiction judgment of its own. Answering a conflict question rewrites the superseded entries instead of appending a correction: the fold tool gains a replace mode the sweep uses for such a question, and the single-question skills' Edit-based fold rewrites by rule, since bending an existing entry to match a recorded answer is permitted. `/derive-tasks` keeps its precondition and is never blocked by a noted contradiction; it gains only a tie-break rule that where two decisions cannot both hold, the later-recorded entry governs the brief and nothing is flagged.

## Relevant starting state

## Decisions

## Out of Scope

