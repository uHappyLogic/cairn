# Milestone 29: Per-question recommendation commits and question sorting

## Goal

Change the recommend sweep's commit granularity from one commit per run to one commit per embedded question, mirroring the answer sweep: after each successful `embed`, the orchestrator commits `open_questions.xml` path-scoped under `Recommendation-annotation: <Short Title>` with the lifted recommendation line as the body, and a skipped question commits nothing. Add a `sort` subcommand to `open_questions.py` that rewrites the document with the annotated blocks first in `walk`'s order (origins, then dependents by depth, same-depth ties and un-annotated blocks in stable prior document order) and every `<recommendation>`-less block last, reusing the walk algorithm so `walk` is by construction the annotated prefix of `list` on a sorted document; the serializer itself keeps writing blocks in their existing order, so no other write reorders anything. The recommend sweep runs `sort` once after its last dispatch and commits the reorder as its own `Question-ordering: <milestone_id>` commit behind the dirty-own-path guard, so a human reviewing the document reads the questions whose answers cannot be nullified by a dependency first.

## Relevant starting state

## Decisions

## Out of Scope

