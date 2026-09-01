# TASKS TODO

## Regenerate The Antigravity Plugin Tree

Re-run the transpilation (`uv run scripts/migrate_skills_to_agy.py` from the repository root) once every source change of this milestone has landed — the shared format-file rename, the `derive-tasks` rewrite, the `submit-task` agent deletion, the `submit-task` skill lean-down, the completion-procedure rework, and the `CLAUDE.md`/`README.md` reconciliations — and check the regenerated `.agents/plugins/cairn/` tree in. The script rmtree-and-copies `agents/` wholesale, so the generated twin of the deleted `agents/submit-task.md` disappears on its own; this task is what makes the source retirement actually complete in the checked-in generated tree.

**Notes:**
- This task must run **last** in the milestone — it transcribes whatever the root sources say at the moment it runs, so any sibling task landing afterwards would leave the generated tree stale again.
- The script resolves `skills`, `agents`, and `.mcp.json` as **relative** paths, so it must be invoked from the repository root. There is no `.mcp.json` in this repo; the `No source MCP config found at .mcp.json` line it prints is expected output, not a failure.
- Skill directories whose name ends in `-workspace` are skipped by design, so `migrate-workspace` deliberately has no generated twin — its absence is not drift.
- The script may rewrite an unquoted YAML `description:` value into quoted form on its way out, so a generated `SKILL.md` can differ textually from its root source without that being drift.
- It exits 1 with a hard error if any `SKILL.md` is missing `name` or `description` in its frontmatter. If that fires, fix the **root** source file — never hand-edit anything under `.agents/`, which is generated output only.

**Success:**
- `uv run scripts/migrate_skills_to_agy.py` run from the repository root exits 0.
- `.agents/plugins/cairn/agents/submit-task.md` does not exist.
- `.agents/plugins/cairn/agents/` contains exactly one `.md` file per file in the root `agents/` directory, with matching names.
- `.agents/plugins/cairn/skills/` contains exactly one directory, each holding a `SKILL.md`, per root `skills/` subdirectory other than `migrate-workspace`.
- Running the script a second time immediately afterwards leaves `.agents/plugins/cairn/` unchanged (`git status --porcelain .agents/` reports nothing once the regenerated tree is committed).

---
