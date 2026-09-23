# TASKS TODO

## Delete The Recording Agent

Delete `core/agents/answer-open-question-with-recommendation.md` and remove the last runtime mention of that agent, the single-question skill's line telling the runner not to spawn it, so no runtime file names an agent that does not exist. The milestone needs it because the inline sweep was the agent's only consumer. Verified by both `hosts/claude/agents/` and `hosts/antigravity/agents/` holding exactly `complete-task.md` and `provide-alternatives-to-open-question.md` after `uv run scripts/build_hosts.py`, no file under `core/` naming the deleted agent, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

---

## Sync CLAUDE.md To Inline Sweep

Update `CLAUDE.md` to the two-agent, inline-sweep shape: the layout table and pipeline listing name two dispatched subagents and no agent for the sweep, the "Mutation-in-agent inversion" invariant is deleted, the answer-sweep invariant describes only the inline shape with no retirement clause, the committing and dispatched-agent-return invariants no longer have the sweep commit an agent's staged index, and the success-path reporting invariant's advisory list gains the sweep's completeness anomaly beside the still-skipped questions the two annotating passes still report. The milestone needs it so the rationale layer matches the runtime it governs. Verified by `CLAUDE.md` naming the deleted agent nowhere and every invariant sentence about the sweep agreeing with the rewritten skill.

---

## Sync Docs Pages To Inline Sweep

Update `docs/skill-reference.md` (rewrite the sweep entry to the inline shape and delete the agent entry), `docs/workflow.md` (the commit paragraph and the phase narrative that have the sweep commit an agent's staged index), and `docs/design-claims.md` (the claims describing subagent context and the skill-agent split) so each describes the inline sweep and the two remaining agents. The milestone needs it so the reader-facing documentation matches the runtime. Verified by no page under `docs/` naming the deleted agent or describing the sweep as an orchestrator over an agent, and every design claim still reading true of the two-agent shape.

---

## Headless Chains Move Sweep To Fable

Move all four `/cairn:answer-all-open-questions-with-recommendation` lines in `docs/ways-of-using-cairn.md` (the mixed-agent review chain, the executing-tasks chain, and both lines of the stuck-milestone chain) from `--model "opus"` at `--effort high` or `xhigh` to `--model "fable" --effort high`, the same settings as the recommend line, and rewrite each affected way's settings sentence to say so. This is the last task of the milestone, and the confirming run is the next milestone's first inline answer sweep on this repository at those settings. Verified by the page holding exactly four sweep lines, every one at `--model "fable" --effort high`, no sweep line on `opus`, and each settings sentence matching its chain.

---
