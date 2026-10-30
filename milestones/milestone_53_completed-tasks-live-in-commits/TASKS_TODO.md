# TASKS TODO

## Conversational Readers Switch To Tasks Query

Replace the `TASKS_DONE.md` read of `ask-in-milestone-context` (its reads list, its "how did task X turn out?" guidance, and its live-deliverable-over-entry rule) and `discuss-new-task` (its triage read and its already-covered check) with the same fixed `tasks <MILESTONE_DIR>` call with the body flag the other readers run, at the step that read the file, and have each, on a failed call, tell the user in prose that the completed-task read failed, quoting the `Error:` line, and carry on from its other reads with no fixed line, keeping the conversational skills' exemption. Needed so every reader of completed work reads the commits once the done file is gone. Verified by no `TASKS_DONE` left in either skill, the fixed-lines test unchanged and passing, and a rebuilt `hosts/` tree passing `--check`.

---

## Update The Invariants In CLAUDE.md

Bring `CLAUDE.md` to the commit-borne record: the repository layout (the task-list and definition tool lines, the tests entry describing the fixed-call and parallel tests), the milestone file structure (three files), the task-list invariant (`remove` in place of `move`, no bar rendering, no two-file atomicity, the `TASKS_DONE.md` a pre-flip milestone keeps), the committing invariant's sentence naming the commit tool as the one tool that runs git (widened for the read-only milestones tool, the writers' rule unchanged), the return-contract and dispatch-prompt invariants (the body file beside `paths.txt`, the empty-bar guard), the task-altitude invariant (the bar recorded as the commit body), and the closing `## Milestone Workflow` block, recording the rationale of this milestone's `## Decisions` where a later editor might reverse them. Verified by a read of every changed invariant against the landed runtime files and tools and by no `TASKS_DONE` mention remaining in `CLAUDE.md` outside the pre-flip note.

---

## Update The Docs For Commit-Borne Records

Bring the docs, the landing page, and the pull request template to the commit-borne record: `docs/skill-reference.md`'s `complete-task`, `complete-all-tasks`, and finish entries (the bar as the `Task-completion:` body, the body file, the readers' `tasks` call), `docs/workflow.md`'s execution paragraph and a description of the milestones tool stating the shallow-clone limit, design claims 7 and 11 of `docs/design-claims.md`, `README.md`'s milestone-files list, and the `TASKS_DONE.md` checklist item of `.github/PULL_REQUEST_TEMPLATE.md` rewritten to the commit form beside its Milestone-finish item, while `ideas/benchmark_for_cairn.md`, `milestones/README.md`, and `CHANGELOG.md` stay as written. Verified by a repository-wide search finding `TASKS_DONE` only in those untouched records, the finished milestones' own directories, this milestone's requirements, and the design draft, and by `--check` passing.

---

## Revise The Draft's Carrying It Out

Revise `ideas/milestones_addressed_by_path.md`: rewrite "Carrying it out" step 2 as a done section recording what this milestone landed against its plan (the five readers, the body as the bar alone, the group-fed capture and the empty-bar guard, the `tasks` line shape, join, and empty-result rule, the task count), revise step 3 with whatever this milestone discovered that bears on the pointer's removal, and revise the "Limits to state up front" paragraph's shallow-clone sentence to the no-check stance in place of its stop line. It is the milestone's last task because it records the others. Verified by reading the revised sections against the landed runtime files and this milestone's `Task-completion:` log.

---
