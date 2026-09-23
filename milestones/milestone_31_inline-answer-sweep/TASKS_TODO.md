# TASKS TODO

## Sync Docs Pages To Inline Sweep

Update `docs/skill-reference.md` (rewrite the sweep entry to the inline shape and delete the agent entry), `docs/workflow.md` (the commit paragraph and the phase narrative that have the sweep commit an agent's staged index), and `docs/design-claims.md` (the claims describing subagent context and the skill-agent split) so each describes the inline sweep and the two remaining agents. The milestone needs it so the reader-facing documentation matches the runtime. Verified by no page under `docs/` naming the deleted agent or describing the sweep as an orchestrator over an agent, and every design claim still reading true of the two-agent shape.

---

## Headless Chains Move Sweep To Fable

Move all four `/cairn:answer-all-open-questions-with-recommendation` lines in `docs/ways-of-using-cairn.md` (the mixed-agent review chain, the executing-tasks chain, and both lines of the stuck-milestone chain) from `--model "opus"` at `--effort high` or `xhigh` to `--model "fable" --effort high`, the same settings as the recommend line, and rewrite each affected way's settings sentence to say so. This is the last task of the milestone, and the confirming run is the next milestone's first inline answer sweep on this repository at those settings. Verified by the page holding exactly four sweep lines, every one at `--model "fable" --effort high`, no sweep line on `opus`, and each settings sentence matching its chain.

---
