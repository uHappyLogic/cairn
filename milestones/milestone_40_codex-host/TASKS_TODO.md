# TASKS TODO

## Verify Codex Install and Agent Dispatches

In a new minimal git repository in a temporary directory outside the cairn checkout, seeded without a model by running the milestone-definition tool and the open-question tool directly so it holds one milestone with one bare open question and one small task, run three live checks exactly once each: add the marketplace from the committed `hosts/codex/` directory and run `codex plugin add cairn@cairn`, then run one dispatch of each agent as a headless `codex exec` run with `--dangerously-bypass-approvals-and-sandbox`, calling Codex by its full path, the alternatives dispatch leaving alternatives embedded in the seed's question. The task passes only when all three pass: a free-tier quota stop leaves it open to resume at the first unrun check with earlier evidence kept as valid, and a result that contradicts a recorded decision is reported as a failure, never fixed or decided here. The three outcomes and the workspace's path are recorded in `TASKS_DONE.md`, the workspace is kept for the interactive check, and no seed or run script is kept.

---

## Confirm Maintainer Interactive Codex Check

The fourth live check is the maintainer's: in an interactive Codex session in the kept verification workspace, under the workspace-write sandbox with on-request approval, they run `$cairn:recommend-all-open-questions` and approve its git steps. This task passes only when the workspace shows that run, such as the `Recommendation-annotation:` commit the skill leaves in the workspace's git history, and the completer must never run the skill itself; without that evidence the task fails and stays open until the maintainer has run the check. On a pass it records the fourth outcome in `TASKS_DONE.md` and deletes the workspace.

---
