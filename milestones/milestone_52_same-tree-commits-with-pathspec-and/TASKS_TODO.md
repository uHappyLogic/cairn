# TASKS TODO

## Route The Batch Calls Through The Tool

Replace the inlined guard, `git add`, and `git commit` in the three question-document batch calls — the answer sweep's batched call in both its question and conflict sections, the recommendation pass's batch call for its annotation and ordering commits, and the alternatives pass's batch call — with the commit tool's command, each call capturing the tool's stdout and echoing its own landed-commit marker only when that capture is empty, with their prose and reporting steps following. These calls are where a completion agent's staged files could ride into a question commit, which the pathspec now prevents. Verified by `tests/test_sweep_batched_call.py` passing against the changed call under both interpreters and the rebuilt host trees passing `--check`.

---

## Route The Task-File Writer Calls Through The Tool

Replace the inlined guard, `git add`, and `git commit` in the inline `complete-task` skill's, `submit-task`'s, and `derive-tasks`' fixed calls with the commit tool's command chained behind their task-list tool call, each capturing the tool's stdout and echoing its landed-commit marker only when that capture is empty, with their prose following. Each task-file commit then carries exactly its own paths and survives another run's lock. Verified by the three rendered calls running as shown against a scratch repository and the rebuilt host trees passing `--check`.

---

## Test The Lock Retry Through One Fixed Call

Add one test that extracts the inline `complete-task` skill's fixed call from the rendered Claude Code tree — the one fixed call the parallel test leaves unrun — and runs it in a `tmp_path` repository in two cases: holding `.git/index.lock` and releasing it within the retry window, asserting the commit landed with only its own paths; and creating the lock and never removing it, asserting the call ends within a time limit a little above the retry bound, passes on git's `Unable to create '…/.git/index.lock'` message, and lands no commit. This is the milestone's deterministic proof of the retry, which the parallel test is not relied on for and which no other fixed call is run against a lock for. Verified by the test passing under both interpreters on the conftest git fixtures.

---

## Extend The Resumption Rule To Live Work

Rewrite the opening of step 3 of `core/shared/complete-procedure.md` so uncommitted changes in the tree are named as either a previous run's partial work or another run's live work, with the runner continuing from what bears on its task and leaving the rest untouched in both cases. Several `complete-all-tasks` runs may now share one working tree, so the rule must cover work that is in progress rather than abandoned. Verified by the rebuilt host trees passing `--check` with both runners' files still pointing at the unchanged step.

---

## Completion Agent Writes Its Path File

Change `core/agents/complete-task.md` so it takes a third prompt line, `Scratch directory: <scratch dir>`, stages nothing, and runs step 5 as one fixed shell call chaining the task-list tool's `move` with the write of the task's whole change set — the recorded created and edited paths plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`, one path per line — to a file of one fixed name per run inside that scratch directory, behind the move's `&&`, with its return protocol reworded to match. The orchestrator commits each task from that file, so the agent's return becomes a file as the alternatives agent's already is. Verified by `agy_tests/test_subagent_write_tools.py` updated to the three-line prompt and to the landed path file as its pass signal, and the rebuilt host trees passing `--check`.

---

## Orchestrator Commits Each Task From The Path File

Change `core/skills/complete-all-tasks/SKILL.md` and the three hosts' `COMPLETE_TASK_DISPATCH` slot values so the run creates its scratch directory once with `mktemp -d`, passes it on every dispatch as the fixed `Scratch directory:` prompt line, and replaces step 2c's whole-index guard and commit with one fixed call that commits through the commit tool with the agent's path file as its only pathspec and then moves that file into a `processed` subdirectory of the scratch directory under a name the call makes unique, deleting nothing; an absent or empty file after a `DONE` commits nothing, ends the run on a new fixed identifier-free stop line with the task name and whether the file was absent or empty below it, and the `Task run committed nothing — no task staged a change.` condition, its line, and its table row are retired so a run whose tasks all returned `DONE` always ends on `All tasks completed.`. Verified by the new stop line's row in `docs/skill-reference.md`'s fixed-lines table and the retired row gone with `tests/test_fixed_console_lines.py` passing, the rebuilt host trees passing `--check`, and the on-demand agy suite run for the Antigravity slot change.

---

## Add The Parallel Two-Milestone Completion Test

Add one test that extracts the completion agent's step-5 fixed call and the orchestrator's commit-from-file call from the rendered Claude Code tree and, for each of two fixture milestones seeded into one `tmp_path` repository through the conftest factory, makes the task's edits, runs the agent's call with that milestone's recorded paths substituted, then runs the orchestrator's call on the path file it left behind, running the two milestones' agent-then-orchestrator sequences concurrently and asserting each `Task-completion:` commit carries only its own paths; it writes no path file of its own and runs no inline `complete-task` call. It is the milestone's one simple proof that two runs can share a tree without one's files riding into the other's commit. Verified by the test passing under both interpreters.

---

## Update The Committing Invariants In CLAUDE.md

Revise the CLAUDE.md invariants to the mechanism as it now stands: the committing invariant places the commit mechanics in the commit tool rather than in `commit-procedure.md` and describes the orchestrator's commit-from-file in place of the index its agent staged, the rule that a tool touches no git is scoped to the document writers, the shell-literal invariant's sentence setting a commit tool aside is reworded, the return-contract and dispatch-prompt invariants record the completion agent's path file and the scratch directory passed on every dispatch, and the `tests/` layout line names the moved git fixtures and the two new tests. The invariants are where the rationale for these decisions lives, so a later editor must not restore the staging contract or the whole-index commit. Verified by reading each named invariant against the runtime files and tests it describes.

---

## Update The Docs For Same-Tree Commits

Update `docs/workflow.md`'s `## How skills commit`, the `complete-all-tasks` and `complete-task` entries of `docs/skill-reference.md`, `docs/design-claims.md`, and `docs/ways-of-using-cairn.md` to record the pathspec, the retry, and the commit-from-file mechanism, rewording design claim 12 from a clean tree after each skill to per-commit hygiene while claim 9 stays as written, and stating that the existing "Preparing the next milestone while the current one runs" chain no longer leaks a completion agent's files into the answer sweep's or an annotating pass's commit, with two `complete-all-tasks` runs sharing one tree left unstated and no new chain added. The docs cover only the same-tree concurrency they already describe. Verified by no doc still saying an agent stages or an orchestrator commits the staged index, and `tests/test_fixed_console_lines.py` passing.

---
