# TASKS DONE

## Remove Pinned Model From Agent Frontmatter

Delete the `model: opus` frontmatter line from each of the three files under `agents/` (`complete-task.md`, `recommend-open-question.md`, `answer-open-question-with-recommendation.md`) so a dispatched agent inherits the session's model instead of forcing Opus, leaving `name`, `description`, and `color` untouched. Verified when none of the three source agent files carries a `model` key and the regenerated `.agents/plugins/cairn/agents/` tree is byte-identical to the source.

**Verified:**

- No `model` key remains in the frontmatter of any of the three source agent files: `grep -rn '^model:' agents/` returns nothing, and `yaml.safe_load` of each file's frontmatter yields exactly the keys `name`, `description`, `color`.
- The `name`, `description`, and `color` values are untouched in all three files (`complete-task` green, `answer-open-question-with-recommendation` green, `recommend-open-question` teal); `git diff --stat` shows exactly one deleted line and zero added lines per file.
- The Antigravity tree was regenerated with `uv run scripts/migrate_skills_to_agy.py` and `diff -r agents .agents/plugins/cairn/agents` exits 0 — the generated agent tree is byte-identical to the source.

---

## Remove Pinned Model From Skill Frontmatter

Delete the `model: opus` frontmatter line from the two skills that still carry it, `skills/answer-open-question-with-recommendation/SKILL.md` and `skills/answer-open-question-with-alternative/SKILL.md`, leaving `name` and `description` untouched, so that together with the agent task before it nothing in the plugin pins a model. Verified when a grep for a `model:` frontmatter line across `skills/` and `agents/` finds nothing and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

**Verified:**

- Neither source skill frontmatter carries a `model` key: `grep -rn '^model:' skills/ agents/` returns nothing, and `yaml.safe_load` of each of the two files' frontmatter yields exactly the keys `name`, `description`.
- The `name` and `description` values are untouched in both files; `git diff --numstat` shows exactly one deleted line and zero added lines per source file.
- Together with the completed agent task, nothing in the plugin pins a model: no file under `skills/` or `agents/` (or the generated `.agents/plugins/cairn/` tree) contains a `model:` frontmatter line.
- The Antigravity tree was regenerated with `uv run scripts/migrate_skills_to_agy.py` and `diff -r` of `skills`, `agents`, and `shared` against their `.agents/plugins/cairn/` counterparts each exits 0 — the generated tree is byte-identical to the source.

---
