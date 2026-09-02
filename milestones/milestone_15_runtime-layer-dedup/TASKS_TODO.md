# TASKS TODO

## Extend Transpile Script And Regenerate Tree

Extend `scripts/migrate_skills_to_agy.py` with a wholesale copy of `shared/` into `.agents/plugins/cairn/`, in the shape of the existing `agents/` copytree, so every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a present file, then run `uv run scripts/migrate_skills_to_agy.py` once the re-audit loop has closed so the checked-in tree reflects the final deduplicated layer; rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text to an Antigravity-resolvable path stays out of scope and is recorded as a follow-up in this task's `TASKS_DONE.md` entry. Verified by inspecting the regenerated file list for the 7 `shared/` files and by confirming every generated `SKILL.md` and agent file is byte-identical to its source.

---
