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
