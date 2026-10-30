# TASKS TODO

## Update The Docs For Same-Tree Commits

Update `docs/workflow.md`'s `## How skills commit`, the `complete-all-tasks` and `complete-task` entries of `docs/skill-reference.md`, `docs/design-claims.md`, and `docs/ways-of-using-cairn.md` to record the pathspec, the retry, and the commit-from-file mechanism, rewording design claim 12 from a clean tree after each skill to per-commit hygiene while claim 9 stays as written, and stating that the existing "Preparing the next milestone while the current one runs" chain no longer leaks a completion agent's files into the answer sweep's or an annotating pass's commit, with two `complete-all-tasks` runs sharing one tree left unstated and no new chain added. The docs cover only the same-tree concurrency they already describe. Verified by no doc still saying an agent stages or an orchestrator commits the staged index, and `tests/test_fixed_console_lines.py` passing.

---
