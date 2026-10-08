# TASKS TODO

## Record Batch Rationale in CLAUDE.md Invariants

Update the `CLAUDE.md` invariants that describe the alternatives pass (the two-annotating-passes bullet, element rendering, committing as a skill-layer property, shell commands written literally, success-path reporting, dispatched-agent return contracts, the dispatch-prompt rule, and the host-wording-slots bullet) so they state the batch form: one `mktemp -d` run directory, the agent's one scratch file as the sole exception to its read-only contract, `DONE` or `FAILED:` as its only final message, a temporary name renamed into place, a fixed scan moving every piped file aside, one commit per question landed in batches once per run or once per wake-up by host, repairs sent together, re-waits without limit, nothing deleted, the end-of-run `list --without-alternatives` advisory, the three-value prompt, and `ALTERNATIVES_CONCURRENCY` governing return collection with the Antigravity value identical to the Claude Code one. Each bullet carries the rationale a later editor must not undo (why a return no longer travels through the orchestrator's context twice, why the final message is a token rather than a path, why no `DONE` is cross-checked against the scan, why no delete command enters the runner's prose, and why the retired per-return pipeline must not be restored), and the result is verified by reading each edited bullet against the milestone's decisions; the file renders into no host tree, so no rebuild is needed.

---

## Describe Batched Pass in Docs

Update `docs/skill-reference.md`'s entries for `provide-alternatives-to-all-open-questions` and the `provide-alternatives-to-open-question` subagent, claims 13, 15, and 18 of `docs/design-claims.md`, and the two passages of `docs/workflow.md` that describe the pass, so they describe the scratch-file return (the agent writes one file outside the repository and ends with `DONE` or `FAILED:`, and the orchestrator gets nothing but that token), the batch embed-and-commit (one fixed scan per batch call, one commit per question, once per run where the host waits once and once per wake-up where it does not), the repair rounds, the no-annotation-landed advisory, and the untouched scratch directory, leaving `docs/ways-of-using-cairn.md` as it is. Verified by reading each edited passage against the milestone's decisions and the rewritten skill and agent files.

---
