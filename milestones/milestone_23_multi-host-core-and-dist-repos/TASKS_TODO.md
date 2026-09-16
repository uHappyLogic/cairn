# TASKS TODO

## Cut Over To Generated Claude Tree

Repoint the root `.claude-plugin/marketplace.json` entry's `source` from `"."` to `"./hosts/claude"` (the monorepo keeps this hand-held marketplace, still named `cairn`), and in the same change delete the root `skills/`, `agents/`, `shared/`, and `.agents/` trees, the root `.claude-plugin/plugin.json` whose content now lives in the Claude host template, and `scripts/migrate_skills_to_agy.py` outright with no deprecation shim or alias, updating the `pyproject.toml` description that still names the transpiler. This is deliberately the last task, because the running plugin resolves its shared procedures from the root trees until it lands. Verified when `uv run scripts/build_hosts.py --check` still passes, `git ls-files` lists none of the removed paths, and the marketplace entry resolves to `hosts/claude/.claude-plugin/plugin.json`.

---
