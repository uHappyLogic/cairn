# Get Current Milestone (shared snippet)

This is the single source of truth for resolving `<MILESTONE_DIR>` from the
current-milestone pointer.

## How to read the pointer

1. In the workspace root `milestones/README.md`, find the one line whose prefix
   is `Current milestone:` (case-sensitive; the colon is load-bearing — this
   unique prefix is what distinguishes the machine pointer line from the section
   heading `## Current Milestone`).

2. Examine the value after the prefix:

   - If the value is the bare token `none` (no backticks) — `Current milestone: none`
     — there is no active milestone. Stop and report accordingly; do not attempt to
     read a milestone directory.

   - Otherwise the value is a backtick-quoted path, e.g.
     `` Current milestone: `milestones/milestone_01_public-release-prep/` ``.
     Extract the path inside the backticks; that path is `<MILESTONE_DIR>`.

3. Use `<MILESTONE_DIR>` as the prefix for all milestone-relative file reads
   (e.g. `<MILESTONE_DIR>/TASKS_TODO.md`, `<MILESTONE_DIR>/requirements.md`).
