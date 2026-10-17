# TASKS TODO

## Switch The Write-Tool Grant To A Tools List

Replace the Antigravity `AGENT_WRITE_TOOLS` slot value, the `enable_write_tools: true` line the installed agy ignores in an agent file's frontmatter, with a `tools:` list naming the host's file-writing and command-running tools as its `define_subagent` tool materializes them for a write-enabled subagent (`write_to_file`, `replace_file_content`, `multi_replace_file_content`, and `run_command` among them), keeping the Claude Code and Codex values empty, and extend `required_agent_frontmatter` with the build's `declared-key-mismatch` check so the Antigravity definition pins that list value. Rebuild `hosts/`, refresh the installed copy at `~/.gemini/config/plugins/cairn` from the rebuilt tree, and confirm with one headless `agy -p` dispatch of each plugin agent that it now holds write and shell tools, so the subagent probe can pass against the installed copy. Verified when `--check` and both pytest runs pass, both rendered Antigravity agents carry the `tools:` list and no `enable_write_tools` key, and the installed copy is byte-identical with `hosts/antigravity/`.

---

## Add The Subagent Write-Tool Probe

Add tests whose headless `agy -p` prompts dispatch each plugin agent directly, bypassing the orchestrator skills: `provide-alternatives-to-open-question` with a fixture Short Title, the seeded milestone directory, and a scratch directory the suite created, and `complete-task` with the heading of the fixture's trivial task. The pass signal is the files each agent lands, the scratch file holding `<alternative>` elements and the task's section moved from `TASKS_TODO.md` into `TASKS_DONE.md` by the task-list tool with the two paths staged, with no final message or transcript record read and no trivial write-and-run task replacing an agent's real contract. Verified by `uv run pytest agy_tests` passing against the refreshed installed copy.

---

## Add The Agy Suite Run Trigger

Over one shared narrow path set (`scripts/hosts/antigravity/`, `core/agents/*.md`, `scripts/build_hosts.py`, and the suite's own directory), add a sentence to `CONTRIBUTING.md`'s `## Development` section requiring an agy suite run (`uv run pytest agy_tests`) before committing a change to those paths, and a new pre-flight check in `.claude/skills/release-plugin/SKILL.md` that runs the suite when any of those paths changed since `<LAST_TAG>` and stops the release on a failure, costing nothing when none changed and staying within the pre-flight's no-write rule because the suite writes nothing to the installation. Verified by reading both edits against the path set and by the pre-flight's check count and wording staying consistent.

---

## Rewrite The Antigravity Hands-On Check Block

Run the hands-on check against the installed agy 1.4.0 and rewrite the dated block in the header of `scripts/hosts/antigravity/settings.toml` as that new check, naming the global `~/.gemini/config/plugins/cairn` path as the install checked, the `enable_write_tools` check on both agents, and the points the 2026-10-13 run sourced (dispatch, waiting, continuing an agent, context file), each re-checked or carried forward. It stays the one record of what was checked, carries no reference to the agy suite, and the `CLAUDE.md` invariant stays as worded. Verified when the block names every point and no suite and `--check` still passes.

---
