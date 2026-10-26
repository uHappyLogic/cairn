# Milestone 7: Golden sweep fixture

## Goal

Record every walked pick of the document beside this file in one batched call, one commit per answer.

## Relevant starting state

The cache sits in front of a slow store, and a read of that store can fail.

## Decisions

### Storage

- **One store.** Every cache entry lives in a single store beside the project.

### Cache size

The cache holds at most 100 entries at a time.

### Memory budget

- **Entry cap.** The cache holds at most 500 entries, so a full scan stays fast.
- **No disk spill.** An entry that does not fit in the cache is never written to disk.

## Out of Scope

- Anything the sweep does not record.
