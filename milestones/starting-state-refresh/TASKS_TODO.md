# TASKS TODO

## Docs and Invariants Describe the Refresh

Bring `docs/workflow.md`, `docs/skill-reference.md`, and `CLAUDE.md` in line with the starting state as landed: the workflow page's starting-state and task-entry stages and its committing paragraph (a refresh committed under `Starting-state:` by the skill or, as a commit of its own, by a task-entry writer; the gate checked twice; an unchanged refresh repeated as an accepted cost), the skill-reference entries of `specify-milestone-starting-state`, `review-milestone-requirements`, `derive-tasks`, and `submit-task`, and `CLAUDE.md`'s layout, pipeline listing, and invariants. The milestones-tool invariant is rewritten for `since`, `show`, the milestone-path forms of `live` and `milestones`, `--last`, the content read from a commit, and `gate` and `since` as the two queries that check for a shallow clone; the scope-gate invariant for the two gate positions in the task-entry writers; and one new invariant records the starting state's rationale (the anchor found by subject and path, the refresh as a premise change with its pick clearing, the writers refreshing instead of stopping, no state for an unchanged refresh, the verified bars left unread). Verified by `uv run scripts/build_hosts.py --check`, both pytest runs, and a read-through finding no statement that `live` takes no argument, that only `gate` checks for a shallow clone, or that the tool has six queries.

---

## Benchmark Draft Follows the Refresh

Update `ideas/benchmark_for_cairn.md` for the refresh while keeping both cairn deliveries' one starting-state line in place and their lists unchanged: the chain text gains one statement of why, that the line already stands where the ways-of-using rule puts the refresh, directly ahead of the first review pass, and that in a single-milestone run nothing outside the milestone's directory lands between it and derivation, so a second line would end on the no-op line every time. The expected lines "Detecting a stop" gives the starting-state line take the new no-op line as the `## Fixed console lines` table of `docs/skill-reference.md` spells it. Verified by a read of the draft against the Benchmark chains decision, the two delivery lists unchanged in the diff and the no-op line matching its table row character for character.

---

## Revise the Draft After Step Four

Revise "Carrying it out" in `ideas/milestones_addressed_by_path.md` so its step 4, "The starting state", is headed done and records what landed as the sections for steps 1 to 3 do (the task count against the about nine planned, where the milestone grew, and where the Proposed shape now differs from what landed), and so it notes what this milestone found for step 5, "The record in the completion procedure", with the draft's date line extended. It stands last, after the acceptance runs, so the record it reads is complete; verified by a read of the revised section against this milestone's decisions and its `Task-completion:` commits as `tasks <MILESTONE_DIR> --with-body` prints them.

---
