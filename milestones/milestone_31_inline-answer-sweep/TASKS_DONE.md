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
