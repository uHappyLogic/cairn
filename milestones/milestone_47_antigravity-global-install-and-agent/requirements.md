# Milestone 47: Antigravity global install and agent tools

## Goal

Fix the two Antigravity runtime failures reported in `temp/agy_runtime_issues_report.md`: grant write and shell tool access (`enable_write_tools: true`) to the `provide-alternatives-to-open-question` and `complete-task` subagents in the Antigravity host tree, and standardize Antigravity on the global `~/.gemini/config/plugins/cairn` installation path across `plugin_root`, the rendered host tree, and the installation documentation. Add a repeatable, on-demand test suite that drives the real `agy` CLI to verify global plugin-root resolution and subagent write/shell tool execution, kept out of the default `pytest` and CI runs so it executes only when requested or when the Antigravity host integration changes.

## Relevant starting state

### Antigravity host definition

`scripts/hosts/antigravity/settings.toml` declares `plugin_root = ".agents/plugins/cairn"`, the one host whose plugin-root literal is a path rather than a runtime variable (Claude Code renders `${CLAUDE_PLUGIN_ROOT}`, Codex `${PLUGIN_ROOT}` under `plugin_dir = "plugins/cairn"`), with `plugin_dir = ""`, `strip_frontmatter_keys = ["color"]`, and eight file-backed slots under `slots/`, none of which names a plugin path. Its header comment holds the host's one hands-on check, dated 2026-10-13 against `agy` 1.3.4 and run from a workspace holding the tree at that workspace-relative path; the block states that Antigravity defines no plugin-root variable, and a global install was not part of the check. The definition's templates are `README.md`, `CONTRIBUTING.md`, `plugin.json`, and `.github/workflows/traffic-badges.yml`; the README template's `### Antigravity` section is a `mkdir -p .agents/plugins/cairn` followed by a `curl | tar` extract into it, and the root `README.md` carries that section word for word. No tracked file mentions `~/.gemini`.

### Rendered Antigravity tree and the build's checks

`hosts/antigravity/` is pure build output in which 30 files carry the literal `.agents/plugins/cairn` in 96 places (every SKILL.md but `discuss-milestone-goal`, six shared procedures, both agents, and the README), each either a path to read or a `python3 .agents/plugins/cairn/tools/<tool>.py` command. Both rendered agents carry a two-key frontmatter (`name`, `description`): `color` is the only key the build touches, through the strip-keys setting, and no setting adds a frontmatter key per host. `scripts/build_hosts.py` validates every tree with `dangling-plugin-root` (each `<plugin_root>/path` must name a file resolved against `plugin_dir`, matched through `re.escape(plugin_root)`, so any literal works), `foreign-plugin-root` (no other host's literal in the tree, exempting hosts that share one literal), `stripped-key-present`, `frontmatter-missing/invalid/keys` (YAML-loadable, `name` and `description` present), and `unfilled-placeholder`. `tests/test_build_rendering.py` covers rendering through a synthetic definition in-process under the pinned interpreter only, not the check set.

### Installed `agy` and the global plugin copy

`agy` 1.4.0 is at `~/.local/bin/agy`, and `~/.gemini/config/plugins/cairn/` is a byte-identical copy of `hosts/antigravity/` at 1.8.5. `agy plugin list --json` reports it enabled with `"source": "antigravity"`, 22 skills, and 2 agents at that path; `agy plugin validate --strict --json` reports zero findings; `agy agents` lists `complete-task` and `provide-alternatives-to-open-question`; `~/.gemini/config/config.json` holds an empty `plugins` map. The CLI's built-in `plugin` guide names `~/.gemini/config/plugins/<name>/` as where a plugin is created and `.agents/plugins/` as a project customization root, states that a new plugin directory is discovered only on startup, and limits `agy plugin install <target>` to Agent Marketplace entries. The binary's subagent schema carries `enable_write_tools` ("Set true to equip the subagent with tools to create and edit files, and run commands."), and the binary carries a `${PLUGIN_ROOT}` string in MCP and hook configuration context, with no substitution into skill text documented in the built-in guides or verified. Headless runs take `agy -p "<prompt>"` with `--dangerously-skip-permissions`, `--output-format text|json|stream-json`, `--print-timeout`, `--mode`, `--model`, `--effort`, and `--add-dir`.

### The observed failure

`temp/agy_runtime_issues_report.md` (dated 2026-10-17, under the gitignored `temp/`) records a `/cairn:provide-alternatives-to-all-open-questions` run in `/Users/lucask/workspace/kinga_page` against the global copy: all 11 dispatched subagents ended `FAILED:` for want of shell and write tools, and the orchestrator's `.agents/plugins/cairn/...` reads and commands failed with no such file. The subagent transcript under `~/.gemini/antigravity-cli/brain/613286ca-…` shows only `view_file` and `send_message` calls, and the orchestrator transcripts show the skill loaded from the absolute path `/Users/lucask/.gemini/config/plugins/cairn/skills/<skill>/SKILL.md`, so the plugin's real location reaches the orchestrator through its skill metadata but not the dispatched agent, whose prompt carries only the Short Title, the milestone directory, and the scratch directory. The report names the task-list tool `tasks_todo.py`; the shipped tool is `tools/task_list.py`.

### Test suite and CI

`tests/` is one flat pytest suite under `pyproject.toml`'s `testpaths = ["tests"]` and `pythonpath = ["core/tools"]`, with no markers or `addopts`, run twice (the pinned 3.13 interpreter and the 3.9 floor through `uv run --no-project`); `tests/conftest.py` drives each tool as a subprocess over fixtures under `tests/fixtures/`. `tests/test_build_rendering.py` is the only conditional module, skipping itself at module level below 3.11. `.github/workflows/drift-gate.yml` is one `ubuntu-latest` job with no path filter running `--check` and then both pytest runs; it installs only `uv` and no host CLI. No test drives any host binary, no `evals/` directory exists, and the `dev` dependency group holds pytest alone. `.gitignore` covers `temp/`, `__pycache__/`, and `.pytest_cache/`.

### Constraints the repository already records

`CLAUDE.md` holds the invariants this goal touches: runtime files name no host and carry no editor-facing prose, a host's hands-on check lives only in the dated block of its `settings.toml` header, host wording differences reach `core/` only as named slots declared by every definition, a dispatch prompt carries only what the orchestrator holds and the agent cannot fetch itself, and rendered shell commands are written literally with the runner-variable ban scoped by origin so a host-provided plugin-root reference falls outside it.

## Decisions

### Antigravity host tree

- **Plugin root is the tilde literal.** `plugin_root` in `scripts/hosts/antigravity/settings.toml` becomes `~/.gemini/config/plugins/cairn`, the form the host's own plugin guide writes the path, so every rendered read path and `python3` command in the Antigravity tree names that tilde path. The literal is fixed at build time; `core/`, the dispatch prompts, and the agent files are unchanged, and the runner gets no resolution rule. Whether the host's file-reading tool takes a tilde path is left to the suite's resolution test to pin.
- **The write-tools key reaches the agents through a frontmatter slot.** A named slot placeholder sits inside the frontmatter of both `core/agents/*.md` files; the Antigravity definition's value file holds `enable_write_tools: true`, and the Claude Code and Codex definitions declare the slot with an empty value file, placed so an empty value leaves no blank frontmatter line. No build code, schema, or `strip_frontmatter_keys` list changes, `color` stays the one structural exception, and the rendered frontmatter is validated by the existing YAML checks.

## Out of Scope

