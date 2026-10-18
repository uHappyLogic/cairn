# Milestone 7: Golden sweep fixture

## Goal

Record every walked pick of the document beside this file in one batched call, one commit per answer.

## Relevant starting state

The cache sits in front of a slow store, and a read of that store can fail.

## Decisions

### Storage

- **One store.** Every cache entry lives in a single store beside the project.

## Out of Scope

- Anything the sweep does not record.
