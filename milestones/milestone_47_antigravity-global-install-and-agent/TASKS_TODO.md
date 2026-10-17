# TASKS TODO

## Add The Agy Suite Run Trigger

Over one shared narrow path set (`scripts/hosts/antigravity/`, `core/agents/*.md`, `scripts/build_hosts.py`, and the suite's own directory), add a sentence to `CONTRIBUTING.md`'s `## Development` section requiring an agy suite run (`uv run pytest agy_tests`) before committing a change to those paths, and a new pre-flight check in `.claude/skills/release-plugin/SKILL.md` that runs the suite when any of those paths changed since `<LAST_TAG>` and stops the release on a failure, costing nothing when none changed and staying within the pre-flight's no-write rule because the suite writes nothing to the installation. Verified by reading both edits against the path set and by the pre-flight's check count and wording staying consistent.

---

## Rewrite The Antigravity Hands-On Check Block

Run the hands-on check against the installed agy 1.4.0 and rewrite the dated block in the header of `scripts/hosts/antigravity/settings.toml` as that new check, naming the global `~/.gemini/config/plugins/cairn` path as the install checked, the `enable_write_tools` check on both agents, and the points the 2026-10-13 run sourced (dispatch, waiting, continuing an agent, context file), each re-checked or carried forward. It stays the one record of what was checked, carries no reference to the agy suite, and the `CLAUDE.md` invariant stays as worded. Verified when the block names every point and no suite and `--check` still passes.

---
