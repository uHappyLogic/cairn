# TASKS TODO

## Rewrite Layout Documentation And Stale References

Rewrite the `## Repository layout` block, the `## Development` section, and every invariant in `CLAUDE.md` that references runtime files by root `skills/`, `agents/`, or `shared/` paths, `${CLAUDE_PLUGIN_ROOT}`, the transpiler, or `.agents/plugins/cairn/` so they describe `core/` with `{{PLUGIN_ROOT}}`, the `scripts/hosts/<host>/` definitions, `scripts/build_hosts.py` with its `--check` mode, the committed `hosts/<host>/` trees, the root `VERSION` file, and the two distribution repositories, and rewrite the Development section of `README.md` likewise; in the same edit delete the four stale `migrate-workspace` references (the `README.md` commit-exemption sentence, the two `CLAUDE.md` exemption mentions, and the whole Migration-catalog invariant bullet). Verified when a grep of both files finds no `migrate-workspace`, `migrate_skills_to_agy`, or `.agents/plugins` mention outside historical milestone records and every path the two documents name exists in the repository.

---

## Cut Over To Generated Claude Tree

Repoint the root `.claude-plugin/marketplace.json` entry's `source` from `"."` to `"./hosts/claude"` (the monorepo keeps this hand-held marketplace, still named `cairn`), and in the same change delete the root `skills/`, `agents/`, `shared/`, and `.agents/` trees, the root `.claude-plugin/plugin.json` whose content now lives in the Claude host template, and `scripts/migrate_skills_to_agy.py` outright with no deprecation shim or alias, updating the `pyproject.toml` description that still names the transpiler. This is deliberately the last task, because the running plugin resolves its shared procedures from the root trees until it lands. Verified when `uv run scripts/build_hosts.py --check` still passes, `git ls-files` lists none of the removed paths, and the marketplace entry resolves to `hosts/claude/.claude-plugin/plugin.json`.

---
