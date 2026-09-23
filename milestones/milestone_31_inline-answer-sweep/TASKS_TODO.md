# TASKS TODO

## Answer Runners Resolve Milestone Once

Make `answer-open-question`, `answer-open-question-with-alternative`, and the single-question `answer-open-question-with-recommendation` skill each resolve `<MILESTONE_DIR>` exactly once through `shared/get-current-milestone.md` and pass it to the shared procedure as its `MILESTONE_DIR` input, dropping the prose that says the procedure resolves the milestone itself or harmlessly re-resolves it. The milestone needs it because the procedures no longer look the milestone up. Verified by each of the three skills holding one resolution step before delegating and naming `MILESTONE_DIR` among the inputs it hands over, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

---

## Rewrite Sweep As Inline Skill

Rewrite `core/skills/answer-all-open-questions-with-recommendation/SKILL.md` as an inline single-writer skill that dispatches no agent: it resolves `<MILESTONE_DIR>` once, gathers its order with one `walk` call, reads `open_questions.xml` and `requirements.md` whole once for reasoning only, then per question follows `shared/answer-with-recommendation-procedure.md` from its lift step (the lift's failure is the silent skip, its print the commit body) and commits each answer through `shared/commit-procedure.md` under the unchanged `Recommendation-answer: <Short Title>` subject, exactly as the Decisions on whole-set context read, sweep lift reuse, and skipped-question reporting state. It records every pick as given and never judges it, stops the whole run on a tool failure after a fold with the Short Title and the tool's `Error:` line quoted verbatim and no rollback, and closes with one end-of-run `walk` as a completeness check, reporting `Recommendations recorded.` or one distinct no-op line beside only two advisories: the contradiction pairs noticed at fold time (answered Short Title and conflicting Decisions heading) and any id the final `walk` printed as an anomaly, with no new-question advisory and no skipped question named. Verified by the skill text naming no agent, its frontmatter description staying within 25 words, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

---

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
