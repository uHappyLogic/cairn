# TASKS TODO

## Milestone Definition Creates Three Files

Make the milestone-definition tool create three files — `open_questions.xml`, `requirements.md`, and `TASKS_TODO.md` — dropping `TASKS_DONE.md` from its template constants, `milestone_files`, docstring, and `--help`, and from `tests/test_define_output.py` and `tests/test_define_cleanup.py` (whose failure injected on the done file moves to another file), and bring every skill that names the file set to three: `define-milestone-goal`, `init-milestone-base-workflow`'s `milestones/README.md` template and its context-file `## Milestone Workflow` block, and `modify-milestone-goal`'s stranded-tasks sentence, with the define entry of `docs/skill-reference.md`. Needed because a completed task's record is now its commit, so no milestone starts with a done file. Verified by both pytest runs passing, no `TASKS_DONE` left in those files, and a rebuilt `hosts/` tree passing `--check`.

---

## Fixed-Line Readers Switch To Tasks Query

Replace the `TASKS_DONE.md` read of `finish-current-milestone` (step 2, the summary bullets drawn from it, and the wording of its open-question stop), `derive-tasks` (the coverage matrix's already-satisfied check), and `submit-task` (its triage read) with one fixed call of the milestones tool, `tasks` on `<MILESTONE_DIR>` with the body flag, unconditionally at the step that read the file, and have each treat a failed call (the tool refusing, or git unavailable) as one stop with the tool's `Error:` line quoted verbatim below a fixed line of its own — `Cannot finish the milestone: the completed-task read failed.`, `Cannot derive tasks: the completed-task read failed.`, and a new line in `submit-task`'s `Task not submitted — …` family — writing and committing nothing, an empty milestone being no failure, and the three lines joining the `## Fixed console lines` table of `docs/skill-reference.md`. Verified by `tests/test_fixed_console_lines.py` passing in both pytest runs, no `TASKS_DONE` left in the three skills, and a rebuilt `hosts/` tree passing `--check`.

---

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
