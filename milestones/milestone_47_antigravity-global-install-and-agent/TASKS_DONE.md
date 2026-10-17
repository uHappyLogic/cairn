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

## Scaffold The Agy Suite Outside Testpaths

Create the suite's own directory at the repository root (for example `agy_tests/`) with a `conftest.py` holding its fixtures: one up-front prerequisite check that stops the whole run before any test with a non-zero exit and one line naming the missing prerequisite (agy resolvable on `PATH`, the global copy present at `~/.gemini/config/plugins/cairn`, and that copy byte-identical with the repository's `hosts/antigravity/` tree, naming the remedy of re-extracting or copying the built tree), never skipping and treating every prerequisite the same way; a seeded-repository fixture that copies the fixture project to a fresh temporary directory and runs `git init` and an initial commit there for every agy process; and a launcher running `agy -p` with `--dangerously-skip-permissions`, no `--model` and no `--effort`, and one fixed `--print-timeout` value chosen by the suite, enforcing no wall-clock limit of its own, holding no model id, and writing nothing to the user's installation. `testpaths = ["tests"]`, `pyproject.toml`, and the CI workflow stay unchanged, with no marker, `addopts`, naming convention, or environment variable involved. Verified when `uv run pytest` and the 3.9 floor run collect nothing from the directory, `uv run pytest agy_tests` reaches it, and a hidden prerequisite produces exactly the one-line stop with no per-test outcome.

**Verified:**

- `agy_tests/` exists at the repository root holding `conftest.py` alone, with no `__init__.py`, like `tests/`
- `conftest.py` holds one up-front check (a `pytest_cmdline_main` hook) that tests, in order, `agy` resolvable on `PATH`, the copy present at `~/.gemini/config/plugins/cairn`, and that copy byte-identical with `hosts/antigravity/` (every file path and its bytes); on the first missing one it writes one stderr line naming it (the identity line naming the first differing path and the remedy of re-extracting or copying the built tree) and returns exit code 1 before pytest configures its reporting, never skipping, each prerequisite through the same mechanism
- The `seeded_repo` fixture copies `tests/fixtures/agy_project` to a fresh directory under `tmp_path` on every call and runs `git init`, a local user identity, `git add -A`, and one initial commit there; two calls yield two distinct repositories, each with exactly one commit and a clean status
- The `run_agy` fixture runs exactly `agy -p <prompt> --dangerously-skip-permissions --print-timeout 20m` (plus `--output-format` only when asked), with no `--model`, no `--effort`, no `timeout=` of its own, no model id anywhere in the suite, and the user's real `HOME`; the suite only reads under the installed copy, and a smoke run of that exact flag set against the installed `agy` with stdin from `/dev/null` answered the prompt and exited 0
- `pyproject.toml` (`testpaths = ["tests"]`, no marker or `addopts`) and `.github/workflows/drift-gate.yml` are unchanged, and the suite relies on no naming convention or environment variable
- `uv run pytest` passes (684 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (680 passed, 1 skipped), both collecting zero items from `agy_tests/`
- `uv run pytest agy_tests` reaches the directory: in the current state (installed copy at release 1.8.5) its check stops the run on the README difference, and under a synthetic `HOME` holding an identical copy pytest proceeds to collection (0 items; 29 passed when `tests/test_sort.py` is named alongside) and a throwaway test file exercising both fixtures passed and was removed
- A hidden prerequisite (`agy` off `PATH`; no copy under an empty synthetic `HOME`; a copy differing by one byte) produces exactly one stderr line, empty stdout, and exit 1, with no per-test outcome even when `tests/test_sort.py` is named in the same run
- `uv run scripts/build_hosts.py --check` passes and the installed plugin copy is unchanged by the suite

---

## Add The Plugin-Root Resolution Test

Add the suite's resolution test: one dispatch-free headless agy process in a seeded repository whose printed output asserts separately that the orchestrator read a shared procedure at the global `~/.gemini/config/plugins/cairn` path and ran a `python3` tool command there, which also pins whether the host's file-reading tool takes the tilde path. No dispatched agent's resolution is asserted by this test. Verified by `uv run pytest agy_tests` passing against the installed copy after it has been refreshed from the rebuilt `hosts/antigravity/` tree, an explicit act outside the suite.

**Verified:**

- `agy_tests/test_plugin_root_resolution.py` holds the resolution test: one headless agy process per run, through the suite's `run_agy` launcher in a `seeded_repo` repository with `--output-format stream-json`, driving the dispatch-free `submit-task` skill and asserting that no agent-dispatch tool step (`invoke_subagent`, `define_subagent`, `manage_subagents`, `browser_subagent`) appears in its output
- From that process's printed output the test asserts separately that the orchestrator read a shared procedure at the global path (a DONE `view_file` step whose `AbsolutePath` lies under the expanded `~/.gemini/config/plugins/cairn/shared/`; the observed runs read `get-current-milestone.md` and `task-format.md`) and ran a `python3` tool command there (a DONE `run_command` step running `python3 ~/.gemini/config/plugins/cairn/tools/task_list.py insert …` in the tilde or expanded form, whose output is the chained call's `submission commit landed` or nothing, corroborated by the seeded `TASKS_TODO.md` gaining its second section)
- It pins the tilde handling: the host's `view_file` refuses a tilde path with "must be an absolute path" (observed in a smoke run), so the test asserts that every `view_file` call carrying a tilde path ended in ERROR and that the shared procedure was reached at the expanded absolute path, with the module docstring recording the pinned fact and that a DONE tilde read fails the test
- No dispatched agent's resolution is asserted; `agy_tests/conftest.py` gained only the `plugin_root` fixture returning the tilde literal and its expansion, the launcher unchanged (no `--model`, no `--effort`, the fixed `--print-timeout 20m`, no model id anywhere in the suite)
- `pyproject.toml` (`testpaths = ["tests"]`) and `.github/workflows/drift-gate.yml` are unchanged; `uv run pytest` passes (684 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (680 passed, 1 skipped), each collecting zero items from `agy_tests/`
- The installed copy at `~/.gemini/config/plugins/cairn` was refreshed from the rebuilt `hosts/antigravity/` tree as an explicit act outside the suite (the previous copy backed up first), after which `uv run pytest agy_tests` passes (1 passed in 59 s) and the copy is byte-identical with `hosts/antigravity/` afterwards, the suite having written nothing to it
- `uv run scripts/build_hosts.py --check` passes and only the two suite paths changed

---

## Switch The Write-Tool Grant To A Tools List

Replace the Antigravity `AGENT_WRITE_TOOLS` slot value, the `enable_write_tools: true` line the installed agy ignores in an agent file's frontmatter, with a `tools:` list naming the host's file-writing and command-running tools as its `define_subagent` tool materializes them for a write-enabled subagent (`write_to_file`, `replace_file_content`, `multi_replace_file_content`, and `run_command` among them), keeping the Claude Code and Codex values empty, and extend `required_agent_frontmatter` with the build's `declared-key-mismatch` check so the Antigravity definition pins that list value. Rebuild `hosts/`, refresh the installed copy at `~/.gemini/config/plugins/cairn` from the rebuilt tree, and confirm with one headless `agy -p` dispatch of each plugin agent that it now holds write and shell tools, so the subagent probe can pass against the installed copy. Verified when `--check` and both pytest runs pass, both rendered Antigravity agents carry the `tools:` list and no `enable_write_tools` key, and the installed copy is byte-identical with `hosts/antigravity/`.

**Verified:**

- `scripts/hosts/antigravity/slots/AGENT_WRITE_TOOLS.md` holds a `tools:` list naming exactly the twelve tools the installed agy's `define_subagent` materializes for a write-enabled subagent (`send_message`, `view_file`, `read_url_content`, `search_web`, `schedule`, `generate_image`, `multi_replace_file_content`, `replace_file_content`, `write_to_file`, `run_command`, `manage_task`, `notebook_edit`), pinned by having it define one throwaway subagent, in that order and layout, with no `enable_write_tools` line; the Claude Code and Codex value files stay empty
- `scripts/hosts/antigravity/settings.toml` declares `required_agent_frontmatter = { tools = [...] }` with that same list, with its comment and the `AGENT_WRITE_TOOLS` slot comment rewritten in mechanism terms and no version; the Claude Code and Codex definitions keep `{}`
- `scripts/build_hosts.py`'s loader accepts an array of non-empty strings as a `required_agent_frontmatter` value, `declared-key-mismatch` compares a declared array with the rendered list element by element in order, type included (`declared_value_matches`), and the module docstring documents the array form
- The rebuilt `hosts/antigravity/agents/*.md` frontmatters carry the `tools:` list and no `enable_write_tools` key; the Claude Code and Codex trees are byte-unchanged (only the two Antigravity agents changed under `hosts/`)
- `uv run scripts/build_hosts.py --check` passes; with `run_command` temporarily removed from the slot value it fails with `declared-key-mismatch` on both Antigravity agents, and passes again once the slot is restored byte-exact
- `uv run pytest` passes (684 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (680 passed, 1 skipped)
- The installed copy at `~/.gemini/config/plugins/cairn` was refreshed from the rebuilt tree (backed up first; only the two agent files changed) and is byte-identical with `hosts/antigravity/`, and `agy agents` still lists both plugin agents
- One headless `agy -p` dispatch of each plugin agent against the refreshed copy, with its real inputs in a seeded fixture copy, landed the files only write and shell tools can produce: the alternatives agent's `Data file format.xml` holding four `<alternative>` elements (its transcript shows `run_command` x3 and `write_to_file` x1), and the completion agent's `README.md` with the task moved into `TASKS_DONE.md` by the task-list tool and the three paths staged, nothing committed (its transcript shows `run_command` x2 and `write_to_file` x1)

---
