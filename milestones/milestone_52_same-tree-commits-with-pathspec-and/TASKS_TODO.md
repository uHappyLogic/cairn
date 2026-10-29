# TASKS TODO

## Add The Parallel Two-Milestone Completion Test

Add one test that extracts the completion agent's step-5 fixed call and the orchestrator's commit-from-file call from the rendered Claude Code tree and, for each of two fixture milestones seeded into one `tmp_path` repository through the conftest factory, makes the task's edits, runs the agent's call with that milestone's recorded paths substituted, then runs the orchestrator's call on the path file it left behind, running the two milestones' agent-then-orchestrator sequences concurrently and asserting each `Task-completion:` commit carries only its own paths; it writes no path file of its own and runs no inline `complete-task` call. It is the milestone's one simple proof that two runs can share a tree without one's files riding into the other's commit. Verified by the test passing under both interpreters.

---

## Update The Committing Invariants In CLAUDE.md

Revise the CLAUDE.md invariants to the mechanism as it now stands: the committing invariant places the commit mechanics in the commit tool rather than in `commit-procedure.md` and describes the orchestrator's commit-from-file in place of the index its agent staged, the rule that a tool touches no git is scoped to the document writers, the shell-literal invariant's sentence setting a commit tool aside is reworded, the return-contract and dispatch-prompt invariants record the completion agent's path file and the scratch directory passed on every dispatch, and the `tests/` layout line names the moved git fixtures and the two new tests. The invariants are where the rationale for these decisions lives, so a later editor must not restore the staging contract or the whole-index commit. Verified by reading each named invariant against the runtime files and tests it describes.

---

## Update The Docs For Same-Tree Commits

Update `docs/workflow.md`'s `## How skills commit`, the `complete-all-tasks` and `complete-task` entries of `docs/skill-reference.md`, `docs/design-claims.md`, and `docs/ways-of-using-cairn.md` to record the pathspec, the retry, and the commit-from-file mechanism, rewording design claim 12 from a clean tree after each skill to per-commit hygiene while claim 9 stays as written, and stating that the existing "Preparing the next milestone while the current one runs" chain no longer leaks a completion agent's files into the answer sweep's or an annotating pass's commit, with two `complete-all-tasks` runs sharing one tree left unstated and no new chain added. The docs cover only the same-tree concurrency they already describe. Verified by no doc still saying an agent stages or an orchestrator commits the staged index, and `tests/test_fixed_console_lines.py` passing.

---
