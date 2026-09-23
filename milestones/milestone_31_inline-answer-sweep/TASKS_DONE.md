# TASKS DONE

## Answer Procedures Take Milestone Directory

Remove the find-milestone step from `core/shared/answer-procedure.md` and `core/shared/answer-with-recommendation-procedure.md`, making `MILESTONE_DIR` a required caller-supplied input that the outer procedure hands on to the recording core with no branch on whether it was supplied, and rewrite each opening paragraph's consumer sentence to the inline skill plus inline sweep shape with no agent named. The milestone needs it so every answer runner resolves the directory once and every `lift`, `locate`, `remove`, and commit in a run uses the directory it walked. Verified by neither file referencing `get-current-milestone.md`, both listing `MILESTONE_DIR` among their inputs, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

**Verified:**

- `core/shared/answer-procedure.md` has no find-milestone step and does not reference `get-current-milestone.md`; its steps run 1. Locate through 5. Cascade with every internal step cross-reference renumbered to match.
- `core/shared/answer-with-recommendation-procedure.md` has no find-milestone step and does not reference `get-current-milestone.md`; its steps run 1. Lift and 2. Delegate, and its step 2 hands the given `MILESTONE_DIR` to the recording core with no branch on whether it was supplied.
- Both files list `MILESTONE_DIR` among their inputs as a required, caller-resolved directory the procedure never looks up itself.
- Each opening paragraph's consumer sentence names the inline skill plus the inline answer sweep, and neither file names an agent, an orchestrator, or isolated execution.
- The rebuilt `hosts/claude/shared/` and `hosts/antigravity/shared/` copies of both procedures carry the change, and `uv run scripts/build_hosts.py --check` passes.

---

## Answer Runners Resolve Milestone Once

Make `answer-open-question`, `answer-open-question-with-alternative`, and the single-question `answer-open-question-with-recommendation` skill each resolve `<MILESTONE_DIR>` exactly once through `shared/get-current-milestone.md` and pass it to the shared procedure as its `MILESTONE_DIR` input, dropping the prose that says the procedure resolves the milestone itself or harmlessly re-resolves it. The milestone needs it because the procedures no longer look the milestone up. Verified by each of the three skills holding one resolution step before delegating and naming `MILESTONE_DIR` among the inputs it hands over, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

**Verified:**

- `core/skills/answer-open-question/SKILL.md` holds exactly one resolution step, `### 3. Find the current milestone`, following `shared/get-current-milestone.md`, placed after the parse and sentinel-redirect steps (which stay resolution-free) and before `### 4. Record the answer` delegates to `answer-procedure.md`; every later step cross-reference is renumbered to match.
- `core/skills/answer-open-question-with-alternative/SKILL.md` keeps its single `### 1. Find the current milestone` step before the lift and delegation.
- `core/skills/answer-open-question-with-recommendation/SKILL.md` gains exactly one resolution step, `### 1. Find the current milestone`, before `### 2` delegates to `answer-with-recommendation-procedure.md`; every later step cross-reference is renumbered to match.
- Each of the three skills names `MILESTONE_DIR` among the inputs it hands to its shared procedure, passing the directory its own resolution step produced, and its commit step uses that same directory.
- None of the three skills says the shared procedure resolves the milestone itself or harmlessly re-resolves it: the "owns resolving the current milestone", "its own step 1 re-resolves … harmless", "The procedure resolves the current milestone itself", "find-milestone → lift → delegate", and "resolves `<MILESTONE_DIR>` in its step 1" wording is gone.
- The rebuilt `hosts/claude/` and `hosts/antigravity/` copies of the three skills carry the change, and `uv run scripts/build_hosts.py --check` passes.

---

## Rewrite Sweep As Inline Skill

Rewrite `core/skills/answer-all-open-questions-with-recommendation/SKILL.md` as an inline single-writer skill that dispatches no agent: it resolves `<MILESTONE_DIR>` once, gathers its order with one `walk` call, reads `open_questions.xml` and `requirements.md` whole once for reasoning only, then per question follows `shared/answer-with-recommendation-procedure.md` from its lift step (the lift's failure is the silent skip, its print the commit body) and commits each answer through `shared/commit-procedure.md` under the unchanged `Recommendation-answer: <Short Title>` subject, exactly as the Decisions on whole-set context read, sweep lift reuse, and skipped-question reporting state. It records every pick as given and never judges it, stops the whole run on a tool failure after a fold with the Short Title and the tool's `Error:` line quoted verbatim and no rollback, and closes with one end-of-run `walk` as a completeness check, reporting `Recommendations recorded.` or one distinct no-op line beside only two advisories: the contradiction pairs noticed at fold time (answered Short Title and conflicting Decisions heading) and any id the final `walk` printed as an anomaly, with no new-question advisory and no skipped question named. Verified by the skill text naming no agent, its frontmatter description staying within 25 words, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

**Verified:**

- `core/skills/answer-all-open-questions-with-recommendation/SKILL.md` describes an inline single-writer skill that dispatches no agent and names no agent: its only mention of the word is "dispatches no agent", and it has no `Agent` dispatch, no `DONE`/`FAILED` return handling, and no commit of a staged index.
- Step 0 resolves `<MILESTONE_DIR>` once per run through `shared/get-current-milestone.md` and holds it for every tool call, recording, and commit of the run.
- Step 1 gathers the whole order with one `walk` call, walked exactly once with no outer re-gather loop; an empty print goes to the no-op line and a failure prints the tool's `Error:` line and stops.
- Step 2 reads `open_questions.xml` and `requirements.md` whole once with the file-reading tool for reasoning only, and states the snapshot never gathers, orders, re-checks, or confirms a skip, with the `locate` print and live `requirements.md` taking precedence once cascades land.
- Step 3a follows `shared/answer-with-recommendation-procedure.md` from its lift step with `MILESTONE_DIR` and `SHORT TITLE`, runs no separate lift, treats the lift's failure as a silent skip with no record kept, and holds the lift's print as the commit body.
- Step 3a records every pick as given and never judges it, holds each contradiction noticed at fold time against the live `## Decisions` as a pair (answered Short Title, conflicting Decisions heading), never checks a pick against an unreached block's recommendation, and gives no new-question advisory.
- Step 3b commits each answer through `shared/commit-procedure.md` with PATHS the two milestone files, SUBJECT exactly `Recommendation-answer: <Short Title>`, and BODY the lifted line verbatim, once per answer before the next question.
- Step 3c stops the whole run on a tool failure after the fold, reporting the Short Title with the tool's `Error:` line quoted verbatim, leaving the uncommitted edits with no rollback, and never writing `open_questions.xml` outside the tool.
- Step 4 runs one end-of-run `walk` as a completeness check whose printed ids are an anomaly, never recording, lifting, or naming a skipped question and reading no document.
- Step 5 reports `Recommendations recorded.` or one distinct no-op line, beside only the contradiction-pairs advisory and the completeness anomaly, naming no skipped question and giving no new-question advisory.
- The frontmatter carries `name` and a one-clause `description` of 23 words with no colon or semicolon, loadable by `yaml.safe_load`.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/` and `hosts/antigravity/` copies of the skill, and `uv run scripts/build_hosts.py --check` passes.

---

## Delete The Recording Agent

Delete `core/agents/answer-open-question-with-recommendation.md` and remove the last runtime mention of that agent, the single-question skill's line telling the runner not to spawn it, so no runtime file names an agent that does not exist. The milestone needs it because the inline sweep was the agent's only consumer. Verified by both `hosts/claude/agents/` and `hosts/antigravity/agents/` holding exactly `complete-task.md` and `provide-alternatives-to-open-question.md` after `uv run scripts/build_hosts.py`, no file under `core/` naming the deleted agent, and `uv run scripts/build_hosts.py --check` passing with the rebuilt host trees committed.

**Verified:**

- `core/agents/answer-open-question-with-recommendation.md` is deleted; `core/agents/` holds only `complete-task.md` and `provide-alternatives-to-open-question.md`.
- The single-question skill's "Do **not** spawn the `answer-open-question-with-recommendation` agent." line is removed from `core/skills/answer-open-question-with-recommendation/SKILL.md`, and no file under `core/` names the deleted agent (remaining matches of the name are the same-named skill only).
- After `uv run scripts/build_hosts.py`, both `hosts/claude/agents/` and `hosts/antigravity/agents/` hold exactly `complete-task.md` and `provide-alternatives-to-open-question.md`.
- `uv run scripts/build_hosts.py --check` passes with the rebuilt host trees (agent deletions and the skill edit in both hosts) in the change set.

---

## Sync CLAUDE.md To Inline Sweep

Update `CLAUDE.md` to the two-agent, inline-sweep shape: the layout table and pipeline listing name two dispatched subagents and no agent for the sweep, the "Mutation-in-agent inversion" invariant is deleted, the answer-sweep invariant describes only the inline shape with no retirement clause, the committing and dispatched-agent-return invariants no longer have the sweep commit an agent's staged index, and the success-path reporting invariant's advisory list gains the sweep's completeness anomaly beside the still-skipped questions the two annotating passes still report. The milestone needs it so the rationale layer matches the runtime it governs. Verified by `CLAUDE.md` naming the deleted agent nowhere and every invariant sentence about the sweep agreeing with the rewritten skill.

**Verified:**

- The `CLAUDE.md` layout table's `core/agents/*.md` row names two dispatched subagents, `complete-task` and `provide-alternatives-to-open-question`, and no agent for the sweep.
- The pipeline listing describes `answer-open-question-with-recommendation` as recording one question's recommendation inline (no "agent for the sweep") and `answer-all-open-questions-with-recommendation` as an inline sweep in walk order dispatching no agent, one commit per answer.
- The "Mutation-in-agent inversion" invariant is deleted; its still-true composition rationale (lift in `answer-with-recommendation-procedure.md` over `answer-procedure.md`, inputs-as-given contract shared with literal `answer-open-question`) survives inside the answer-sweep invariant without naming an agent.
- The answer-sweep invariant describes only the inline shape (one `MILESTONE_DIR` resolution passed down, one `walk` walked once, whole-set read for reasoning only, strictly sequential recording from the procedure's lift step, lift failure as the silent skip, lift print as commit body, one commit per answer, every pick recorded as given, contradiction held and reported once, stop on a post-fold tool failure with a resumable tree, no re-gather loop, end-of-run `walk` as completeness check, new questions left to review), with no retirement clause and no mention of the deleted agent or an orchestrator.
- The committing invariant has only `complete-all-tasks` commit an agent's staged index and states the inline answer sweep commits each answer itself through the commit procedure.
- The dispatched-agent return contracts invariant names `complete-all-tasks` as the one other dispatch site and states the answer sweep dispatches nothing and has no return to judge.
- The success-path reporting invariant's advisory list names the still-skipped questions the two annotating passes report, beside the answer sweep's contradiction pairs and completeness anomaly.
- `grep` finds no mention of the deleted agent in `CLAUDE.md` (the one remaining `answer-open-question-with-recommendation` match is the pipeline's skill entry), and every sweep sentence agrees with the rewritten `core/skills/answer-all-open-questions-with-recommendation/SKILL.md`.
- `uv run scripts/build_hosts.py --check` passes.

---
