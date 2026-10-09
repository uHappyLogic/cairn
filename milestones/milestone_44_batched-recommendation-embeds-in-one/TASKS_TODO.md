# TASKS TODO

## Describe Batched Recommendation Call in Docs

Update the `recommend-all-open-questions` entry of `docs/skill-reference.md`, the two `docs/workflow.md` passages that describe the pass (the convergence-loop paragraph and "How skills commit"), and claims 13, 14, and 15 of `docs/design-claims.md` so they describe the batched form: one fixed shell call per batch that runs each picked block's own `embed --recommendation` process and `lift`, commits `open_questions.xml` under `Recommendation-annotation: <milestone_id>` with the lifted lines as body once per batch call rather than once per run, then sorts and commits the reorder under `Question-ordering: <milestone_id>` behind the dirty-own-path guard, with a refused block printing its own paired `Error:` line while the rest land, at most one corrected re-send of the refused blocks and then a skip reported with the remedy of re-running the pass, and the status line read from the call's marker lines. Verified by reading each edited passage against the milestone's `## Decisions` and the rewritten skill with no contradiction, `docs/ways-of-using-cairn.md` unchanged, and `uv run scripts/build_hosts.py --check` passing.

---
