# TASKS TODO

## Add Declared Agent Frontmatter Keys Check

Give every host definition one new settings key in the shared `SETTINGS_SCHEMA` naming the frontmatter keys and values each rendered agent file must carry (`enable_write_tools = true` for Antigravity, empty for Claude Code and Codex), and add to `check_host_tree` one generic check, mirroring `stripped-key-present`, that fails `--check` when a rendered agent lacks a declared key or carries a different value. Document the key and the check in the build's module docstring and declare the key in `tests/test_build_rendering.py`'s synthetic definitions, since the shared key set is required of every definition. Verified when `--check` passes on the committed trees, fails when the Antigravity slot value is temporarily emptied, and the pinned pytest passes.

---

## Rewrite Antigravity Installation Section For Global Install

In the README template under `scripts/hosts/antigravity/` and the root `README.md` section that carries it word for word, change the extract commands and prose to install into `~/.gemini/config/plugins/cairn`, and correct the template's opening sentence that describes extraction into a workspace's `.agents/plugins/cairn/`. Follow the extract command with one identical sentence stating that Antigravity discovers a new plugin directory only on startup, so a running agy session must be restarted after the extract (first install only, no re-extract advice, no listing or verification command), and add a short note for projects that extracted cairn under an earlier release: the literal command removing the project's `.agents/plugins/cairn/` directory with one clause on why (the old copy is discovered beside the global one and predates the subagents' write and shell tools), saying nothing about how the host ranks or merges the two copies. Verified when the two installation sections are identical, the rebuilt `hosts/antigravity/README.md` carries the template, and `--check` passes.

---

## Correct Remaining Stale Antigravity Path Mentions

Correct the two tracked, non-historical statements outside the install sections and the host definition that still name the workspace-local plugin path or say the plugin loads from the working directory: the `--add-dir` bullet in `docs/ways-of-using-cairn.md`, and the Antigravity manifest location in `.github/ISSUE_TEMPLATE/bug.yml`, which becomes `~/.gemini/config/plugins/cairn/plugin.json`. `CHANGELOG.md` entries and finished milestones' files stay as written. Verified when a `git grep` for `.agents/plugins/cairn` outside `hosts/`, `milestones/`, and `CHANGELOG.md` finds only the removal command the install sections carry.

---

## Commit The Agy Suite Fixture Project

Add one committed directory under `tests/fixtures/` holding a small project tree: `milestones/README.md` with its `Current milestone:` pointer, one milestone directory with `requirements.md`, an `open_questions.xml` holding a few bare blocks in the tool's canonical form, and the two task files carrying the one trivial task the direct dispatches need. The fixture is what each agy process is seeded from, so it depends on no plugin tool being correct. Verified when, on a copy, the open-question tool's `list` prints the blocks' Short Titles and the task-list tool's `move` accepts the trivial task.

---

## Scaffold The Agy Suite Outside Testpaths

Create the suite's own directory at the repository root (for example `agy_tests/`) with a `conftest.py` holding its fixtures: one up-front prerequisite check that stops the whole run before any test with a non-zero exit and one line naming the missing prerequisite (agy resolvable on `PATH`, the global copy present at `~/.gemini/config/plugins/cairn`, and that copy byte-identical with the repository's `hosts/antigravity/` tree, naming the remedy of re-extracting or copying the built tree), never skipping and treating every prerequisite the same way; a seeded-repository fixture that copies the fixture project to a fresh temporary directory and runs `git init` and an initial commit there for every agy process; and a launcher running `agy -p` with `--dangerously-skip-permissions`, no `--model` and no `--effort`, and one fixed `--print-timeout` value chosen by the suite, enforcing no wall-clock limit of its own, holding no model id, and writing nothing to the user's installation. `testpaths = ["tests"]`, `pyproject.toml`, and the CI workflow stay unchanged, with no marker, `addopts`, naming convention, or environment variable involved. Verified when `uv run pytest` and the 3.9 floor run collect nothing from the directory, `uv run pytest agy_tests` reaches it, and a hidden prerequisite produces exactly the one-line stop with no per-test outcome.

---

## Add The Plugin-Root Resolution Test

Add the suite's resolution test: one dispatch-free headless agy process in a seeded repository whose printed output asserts separately that the orchestrator read a shared procedure at the global `~/.gemini/config/plugins/cairn` path and ran a `python3` tool command there, which also pins whether the host's file-reading tool takes the tilde path. No dispatched agent's resolution is asserted by this test. Verified by `uv run pytest agy_tests` passing against the installed copy after it has been refreshed from the rebuilt `hosts/antigravity/` tree, an explicit act outside the suite.

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
