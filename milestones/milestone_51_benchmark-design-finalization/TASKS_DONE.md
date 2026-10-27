# TASKS DONE

## Finish Stops On Standing Open Questions

Make `finish-current-milestone` stop, writing and committing nothing, when the milestone's `open_questions.xml` still holds any question block, checked through the open-question tool's `list` call, whatever `TASKS_DONE.md` holds, with no check on completed tasks and no override flag, so a milestone whose derivation was refused on standing questions can no longer be closed empty while a decision-only milestone that answered everything still closes. Change it under `core/`, rebuild the hosts, and verify with `uv run scripts/build_hosts.py --check` and both pytest runs green.

**Verified:**

- `core/skills/finish-current-milestone/SKILL.md` step 3 runs `python3 {{PLUGIN_ROOT}}/tools/open_questions.py list <MILESTONE_DIR>` before the `TASKS_TODO.md` check and before any write (steps 5-8), and on any printed line stops immediately, writing and committing nothing, with the fixed `Cannot finish the milestone: the following open questions must be resolved first:` line and the printed Short Titles as bullets; a failing call prints its `Error:` line and stops; the `list` call is the whole check, never a read of `open_questions.xml`
- The stop applies whatever `TASKS_DONE.md` holds; the skill adds no check on completed tasks and no override flag (the only `--milestone` flag remains the milestone-selection one), so an empty `list` with an empty `TASKS_TODO.md` proceeds to finish a decision-only milestone
- The skill's intro states that it verifies no open question stands, and `docs/skill-reference.md`'s finish entry describes the new stop
- `uv run scripts/build_hosts.py` rebuilt the three host trees, each rendering the `list` call with its own plugin root, and `uv run scripts/build_hosts.py --check` passes
- `uv run pytest` passes (891 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (887 passed, 1 skipped)

---
