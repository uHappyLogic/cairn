# TASKS DONE

## Switch Antigravity Plugin Root To Global Path

Change `plugin_root` in `scripts/hosts/antigravity/settings.toml` from `.agents/plugins/cairn` to the tilde literal `~/.gemini/config/plugins/cairn`, the form the host's own plugin guide writes the path, reword the comment above it (which now says the plugin loads relative to the consuming workspace), and rebuild the host trees so every rendered read path and `python3` command in `hosts/antigravity/` names the global path. `core/`, the dispatch prompts, and the agent files stay unchanged and the runner gets no resolution rule. Verified when `uv run scripts/build_hosts.py --check` passes on the committed trees and no file under `hosts/antigravity/` still carries `.agents/plugins/cairn`.

**Verified:**

- `plugin_root` in `scripts/hosts/antigravity/settings.toml` reads `"~/.gemini/config/plugins/cairn"`, the tilde literal.
- The comment above `plugin_root` no longer says the plugin loads relative to the consuming workspace; it describes the fixed global-install path in the host guide's tilde form.
- `uv run scripts/build_hosts.py` rebuilt the trees: every rendered read path and `python3` command in `hosts/antigravity/` (29 files, 92 references, agents included) names `~/.gemini/config/plugins/cairn`.
- `core/`, the Claude Code and Codex definitions and trees, the dispatch-prompt slots, and the agent sources are unchanged, and the runner gets no resolution rule.
- `uv run scripts/build_hosts.py --check` passes on the rebuilt trees.
- No file under `hosts/antigravity/` rendered from `core/` still carries `.agents/plugins/cairn`; the only remaining occurrences are in `hosts/antigravity/README.md`, rendered from the README template's install section, which the "Rewrite Antigravity Installation Section For Global Install" task rewrites.

---

## Add Write-Tools Frontmatter Slot To Agents

Place one named slot placeholder inside the frontmatter of both `core/agents/*.md` files, positioned so an empty value leaves no blank frontmatter line; the Antigravity definition's value file holds `enable_write_tools: true`, the Claude Code and Codex definitions declare the slot with an empty value file, and each definition's `[slots]` table carries the slot's comment. No build code, schema, or `strip_frontmatter_keys` list changes, and `color` stays the one structural exception. Verified when the rebuilt `hosts/antigravity/agents/*.md` frontmatter carries `enable_write_tools: true`, the other two trees' agent frontmatter is unchanged, and `--check` plus the pinned pytest pass.

**Verified:**

- Both `core/agents/*.md` files carry the `{{AGENT_WRITE_TOOLS}}` placeholder inside their frontmatter, at the start of the closing `---` line, so an empty value adds no frontmatter line.
- `scripts/hosts/antigravity/slots/AGENT_WRITE_TOOLS.md` holds `enable_write_tools: true`; the Claude Code and Codex definitions declare the slot with an empty value file.
- Each definition's `[slots]` table carries an `AGENT_WRITE_TOOLS` entry with its comment above it.
- `scripts/build_hosts.py` is unchanged, every `strip_frontmatter_keys` list is unchanged, and `color` stays the one stripped key.
- The rebuilt `hosts/antigravity/agents/*.md` frontmatter carries `enable_write_tools: true`, and the Claude Code and Codex trees' agent files are byte-unchanged (git diff touches only the two Antigravity agents).
- `uv run scripts/build_hosts.py --check` passes and `uv run pytest` passes (684 passed).

---

## Add Declared Agent Frontmatter Keys Check

Give every host definition one new settings key in the shared `SETTINGS_SCHEMA` naming the frontmatter keys and values each rendered agent file must carry (`enable_write_tools = true` for Antigravity, empty for Claude Code and Codex), and add to `check_host_tree` one generic check, mirroring `stripped-key-present`, that fails `--check` when a rendered agent lacks a declared key or carries a different value. Document the key and the check in the build's module docstring and declare the key in `tests/test_build_rendering.py`'s synthetic definitions, since the shared key set is required of every definition. Verified when `--check` passes on the committed trees, fails when the Antigravity slot value is temporarily emptied, and the pinned pytest passes.

**Verified:**

- `SETTINGS_SCHEMA` in `scripts/build_hosts.py` carries the new shared key `required_agent_frontmatter` (a dict), loaded onto `HostDefinition` and validated by the loader (each key a frontmatter key name, each value a string, boolean, integer, or float).
- `scripts/hosts/antigravity/settings.toml` declares `required_agent_frontmatter = { enable_write_tools = true }`; the Claude Code and Codex definitions declare it empty (`{}`), each with a comment above the key.
- `check_host_tree` has one generic check, `declared-key-mismatch`, mirroring `stripped-key-present`, that fails when a rendered `agents/<name>.md` frontmatter lacks a declared key or carries a different value (type included).
- The build's module docstring documents the `required_agent_frontmatter` key and lists the `declared-key-mismatch` check in the check set.
- Both synthetic definitions in `tests/test_build_rendering.py` declare `required_agent_frontmatter = {}`.
- `uv run scripts/build_hosts.py --check` passes on the committed trees.
- With `scripts/hosts/antigravity/slots/AGENT_WRITE_TOOLS.md` temporarily emptied, `--check` exits 1 with `declared-key-mismatch` on both Antigravity agents (a value of the string `"true"` fails the same way); restored, `--check` passes again.
- `uv run pytest` passes (684 passed).

---

## Rewrite Antigravity Installation Section For Global Install

In the README template under `scripts/hosts/antigravity/` and the root `README.md` section that carries it word for word, change the extract commands and prose to install into `~/.gemini/config/plugins/cairn`, and correct the template's opening sentence that describes extraction into a workspace's `.agents/plugins/cairn/`. Follow the extract command with one identical sentence stating that Antigravity discovers a new plugin directory only on startup, so a running agy session must be restarted after the extract (first install only, no re-extract advice, no listing or verification command), and add a short note for projects that extracted cairn under an earlier release: the literal command removing the project's `.agents/plugins/cairn/` directory with one clause on why (the old copy is discovered beside the global one and predates the subagents' write and shell tools), saying nothing about how the host ranks or merges the two copies. Verified when the two installation sections are identical, the rebuilt `hosts/antigravity/README.md` carries the template, and `--check` passes.

**Verified:**

- The `### Antigravity` sections of `scripts/hosts/antigravity/README.md` and the root `README.md` extract into `~/.gemini/config/plugins/cairn` (`mkdir -p` and `tar -C` both name that path), with prose naming it as the global path Antigravity loads the plugin from.
- The template's opening sentence describes extraction into the global `~/.gemini/config/plugins/cairn/` directory, no longer a workspace's `.agents/plugins/cairn/`.
- Directly after the extract command both sections carry the identical sentence "Antigravity discovers a new plugin directory only on startup, so restart any running `agy` session after the extract.", covering the first install only, with no re-extract advice and no listing or verification command.
- Both sections carry the identical earlier-release note with the literal `rm -rf .agents/plugins/cairn` command and one clause on why (discovered beside the global one, predates the subagents' write and shell tools), saying nothing about how the host ranks or merges the two copies.
- The two installation sections are identical in everything this task writes; the root section is an exact prefix of the template's, which alone keeps the release-pinning paragraph the root README dropped on purpose in commit 3b8f636.
- The rebuilt `hosts/antigravity/README.md` carries the template's section verbatim, and `uv run scripts/build_hosts.py --check` passes.

---

## Correct Remaining Stale Antigravity Path Mentions

Correct the two tracked, non-historical statements outside the install sections and the host definition that still name the workspace-local plugin path or say the plugin loads from the working directory: the `--add-dir` bullet in `docs/ways-of-using-cairn.md`, and the Antigravity manifest location in `.github/ISSUE_TEMPLATE/bug.yml`, which becomes `~/.gemini/config/plugins/cairn/plugin.json`. `CHANGELOG.md` entries and finished milestones' files stay as written. Verified when a `git grep` for `.agents/plugins/cairn` outside `hosts/`, `milestones/`, and `CHANGELOG.md` finds only the removal command the install sections carry.

**Verified:**

- The `--add-dir` bullet in `docs/ways-of-using-cairn.md` no longer says an `agy` run loads the plugin from its working directory; it keeps the working directory as the run's workspace and states the plugin loads from its installed location (on Antigravity the global `~/.gemini/config/plugins/cairn`), never from the working directory.
- The Cairn-version description in `.github/ISSUE_TEMPLATE/bug.yml` names the Antigravity manifest at `~/.gemini/config/plugins/cairn/plugin.json`, with the Claude Code and Codex manifest locations unchanged.
- `CHANGELOG.md` and every file under `milestones/` are unchanged.
- `git grep` for `.agents/plugins/cairn` outside `hosts/`, `milestones/`, and `CHANGELOG.md` finds only the `rm -rf .agents/plugins/cairn` removal command in the root `README.md` and `scripts/hosts/antigravity/README.md` install sections.
- No other file changed, and `uv run scripts/build_hosts.py --check` passes.

---

## Commit The Agy Suite Fixture Project

Add one committed directory under `tests/fixtures/` holding a small project tree: `milestones/README.md` with its `Current milestone:` pointer, one milestone directory with `requirements.md`, an `open_questions.xml` holding a few bare blocks in the tool's canonical form, and the two task files carrying the one trivial task the direct dispatches need. The fixture is what each agy process is seeded from, so it depends on no plugin tool being correct. Verified when, on a copy, the open-question tool's `list` prints the blocks' Short Titles and the task-list tool's `move` accepts the trivial task.

**Verified:**

- `tests/fixtures/agy_project/` holds `milestones/README.md` and one milestone directory `milestones/milestone_01_pocket-ledger-foundations/` with exactly `requirements.md`, `open_questions.xml`, `TASKS_TODO.md`, and `TASKS_DONE.md`, none of them ignored by git
- `milestones/README.md` carries the one `Current milestone:` line naming that milestone directory in backticks, in the bootstrap skill's template shape
- `requirements.md` carries the four prose headings the milestone-definition tool creates (Goal, Relevant starting state, Decisions, Out of Scope)
- `open_questions.xml` holds three bare blocks (`Data file format`, `Date input form`, `Summary period selection`) and is byte-identical to the open-question tool's own `add` rendering
- `TASKS_TODO.md` holds the one trivial task `Add The Project README` in the task-format shape and is byte-identical to the task-list tool's `initialize` rendering; `TASKS_DONE.md` is the empty canonical file
- On a copy, `python3 core/tools/open_questions.py list` exits 0 and prints exactly the three Short Titles, one per line
- On a copy, `python3 core/tools/task_list.py move … "Add The Project README"` exits 0 printing nothing, leaving the section under `**Verified:**` in the copy's `TASKS_DONE.md` and the copy's `TASKS_TODO.md` empty, with the committed fixture unchanged
- `tests/test_format.py` and `tests/test_sort.py` discover golden directories as those holding `open_questions.xml` directly, so the project tree is not collected as a golden document; `uv run pytest` (684 passed) and the 3.9 floor run (680 passed, 1 skipped) pass

---
