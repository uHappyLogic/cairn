# TASKS TODO

## Confirm Maintainer Interactive Codex Check

The fourth live check is the maintainer's: in an interactive Codex session in the kept verification workspace, under the workspace-write sandbox with on-request approval, they run `$cairn:recommend-all-open-questions` and approve its git steps. This task passes only when the workspace shows that run, such as the `Recommendation-annotation:` commit the skill leaves in the workspace's git history, and the completer must never run the skill itself; without that evidence the task fails and stays open until the maintainer has run the check. On a pass it records the fourth outcome in `TASKS_DONE.md` and deletes the workspace.

---
