# TASKS TODO

## Describe Batched Pass in Docs

Update `docs/skill-reference.md`'s entries for `provide-alternatives-to-all-open-questions` and the `provide-alternatives-to-open-question` subagent, claims 13, 15, and 18 of `docs/design-claims.md`, and the two passages of `docs/workflow.md` that describe the pass, so they describe the scratch-file return (the agent writes one file outside the repository and ends with `DONE` or `FAILED:`, and the orchestrator gets nothing but that token), the batch embed-and-commit (one fixed scan per batch call, one commit per question, once per run where the host waits once and once per wake-up where it does not), the repair rounds, the no-annotation-landed advisory, and the untouched scratch directory, leaving `docs/ways-of-using-cairn.md` as it is. Verified by reading each edited passage against the milestone's decisions and the rewritten skill and agent files.

---
