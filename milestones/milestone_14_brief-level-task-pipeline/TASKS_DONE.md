# TASKS DONE

## Slim Submit Procedure Into Shared Task Format

Replace `shared/submit-procedure.md` with `shared/task-format.md`, holding only the brief-level task template and its authoring guidelines. The milestone-resolution, context-loading, and POSITION-insertion steps drop out (the two authoring runners now handle those themselves), and the name describes the task format rather than a submit procedure. This is the shared source of truth both `derive-tasks` and the leaned-down `submit-task` skill will reference via `${CLAUDE_PLUGIN_ROOT}`, and that `shared/complete-procedure.md` parses.

**Provides:**
- `shared/task-format.md` — the shared brief-level task-format file, referenced via `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md`.
- The brief-level task template it defines: a `##` task-title heading, a 1–3 sentence description with the "how it would be verified" clause folded in as prose, and a trailing `---` separator — no `Provides`, `Notes`, or `Success` sections.
- The four carried-over authoring guidelines: atomic scope, no open decisions, quote numeric values from `requirements.md`, unique 4–8 word titles.

**Notes:**
- `shared/submit-procedure.md` is still referenced by `skills/submit-task/SKILL.md` and `agents/submit-task.md`; rewriting/retiring those referrers belongs to sibling tasks, so this task leaves them dangling.
- Keep the file execution-neutral in the established shared-file style — no commit steps, no `DONE`/`FAILED` return protocol, no ordering or positioning decisions.
- `scripts/migrate_skills_to_agy.py` copies only `agents/` and `skills/` into `.agents/plugins/cairn/`; `shared/` has no generated twin, so this rename needs no transpile re-run.

**Success:**
- `shared/task-format.md` exists and contains exactly two content areas: the brief-level task template and the four authoring guidelines.
- `shared/submit-procedure.md` no longer exists.
- The template in `shared/task-format.md` contains no `Provides`, `Notes`, or `Success` section and no other structured done-ness heading.
- The template specifies the `##` heading, the 1–3 sentence description, and the mandatory trailing `---` separator.
- `shared/task-format.md` contains no milestone-resolution, context-loading, or POSITION/insertion instructions.

---

