# Host-generic on-demand suite

## Goal

Turn the on-demand `agy_tests/` suite into a host-generic suite that drives the installed CLI of any of the three hosts (Claude Code, Antigravity, Codex) against that host's installed plugin copy, the host chosen per run. Every test checks behaviour that is the same on every host, so the existing plugin-root resolution test and both agent-dispatch tests run and pass against all three hosts, with only the prerequisite check and the invocation differing per host. The suite's name and every reference to it (the `CLAUDE.md` command, `CONTRIBUTING.md`, the release pre-flight and its trigger paths) follow.

## Relevant starting state

### The `agy_tests/` suite

`agy_tests/` at the repository root holds `conftest.py` and two test modules with three tests, added by `milestone_47` and last changed by `milestone_54`. It sits outside `pyproject.toml`'s `testpaths = ["tests"]`, so `uv run pytest`, the 3.9 floor run, and CI's `drift-gate` job never reach it; it runs only as `uv run pytest agy_tests`. Every host-specific value is a module constant or a fixture bound to Antigravity: `BUILT_TREE` (`hosts/antigravity`), `PLUGIN_ROOT_TILDE` (`~/.gemini/config/plugins/cairn`), `PRINT_TIMEOUT`, the `plugin_root` fixture, and the `run_agy` fixture, whose command is always `agy -p <prompt> --dangerously-skip-permissions --print-timeout 20m` plus an optional `--output-format`, run with the user's real `HOME` at the account's default model and effort. Nothing selects a host: the suite reads no pytest option or environment variable and parametrizes no test.

### Prerequisite check

`conftest.py`'s `pytest_cmdline_main` hook runs three checks in order before any test: `agy` resolvable on `PATH`, a directory at the global plugin path, and that directory byte-identical to `hosts/antigravity/` file for file, a missing or extra file included. On the first failure it writes one line, `agy suite prerequisite missing: <reason and remedy>`, to stderr and returns exit code 1, with no per-test outcome and never a skip. The suite writes nothing to the installed copy; replacing it is left to the user.

### Seeding and the fixture project

`seeded_repo` copies `tests/fixtures/agy_project/` into a fresh directory under `tmp_path`, renames its `milestones.fixture/` container to `milestones/`, and makes one `git init` and seed commit, so each process starts from the same committed tree. The fixture holds only that container: a pointer-era `README.md` naming a current milestone, and `milestone_01_pocket-ledger-foundations/` with a filled `requirements.md` (headed `# Milestone 1: …`), three bare question blocks in `open_questions.xml`, and one task, `Add The Project README`, in `TASKS_TODO.md`; it carries no context file (`CLAUDE.md` or `AGENTS.md`) and no source. The container is tracked as `milestones.fixture/` so the milestones tool's discovery pattern does not list it in this repository, which `CLAUDE.md`'s milestones-tool invariant states by path, and `tests/test_milestones_tasks.py` uses `tests/fixtures/agy_project/…` strings as synthetic commit paths in three tests without reading the fixture.

### The plugin-root resolution test

`test_plugin_root_resolution.py` runs `/cairn:submit-task --milestone milestones/milestone_01_pocket-ledger-foundations/ <issue>` in one headless process with `--output-format stream-json` and reads the host's own tool-call records: `step_update` events, each tool step in its final `DONE` or `ERROR` state, and a closing `result` event with status `SUCCESS`. It asserts that no dispatch tool was used, that at least one `DONE` file read lies under `<expanded root>/shared/`, that every read attempted with a `~` path ended in `ERROR`, that a `DONE` shell call ran `task_list.py insert` under the root in its tilde or expanded form with output empty or `submission commit landed`, and that the seeded task list holds two sections. The tool names and parameters (`read_file`/`view_file` with `Path`/`AbsolutePath`, `run_command` with `CommandLine`, four dispatch tool names), the record shapes, the `Command exited with code` output wrapper, and the tilde pin are all Antigravity's; only the last assertion reads the repository instead of the host's records.

### The two agent-dispatch tests

`test_subagent_write_tools.py` starts one headless process per agent whose prompt tells it to call `invoke_subagent` with the agent's bare name as `TypeName`, a `Role`, and the real dispatch prompt (the Short Title or task name, then the `Milestone directory:` and `Scratch directory:` lines), the scratch directory created by the test. The pass signal is files read from disk. For the alternatives agent: `<scratch>/Data file format.xml` holding only `<alternative>` elements, each with an `id`, an `advantage`, and a `drawback`, no `.xml.part` left behind, and a clean `git status`. For the completion agent: `README.md` with its heading, `TASKS_TODO.md` reduced to `# TASKS TODO`, exactly `body.txt` (only `- ` bullets) and `paths.txt` (the deliverable and the task list) in the scratch directory, nothing staged, and one commit. The stream-json output is read for one thing, that the process made exactly one dispatch of the named agent with that prompt (a `subagent` step's `type_name` and `initial_prompt`) and used none of five Antigravity write or shell tools itself.

### Host definitions: plugin root, install, and dispatch

| Host | Rendered plugin root | Plugin directory in the built tree | Documented install | Agent dispatch (slot values) |
|---|---|---|---|---|
| Claude Code | `${CLAUDE_PLUGIN_ROOT}`, which arrives in skill text already resolved to an absolute path | `hosts/claude/` | `/plugin marketplace add`, then `/plugin install cairn@cairn`; the monorepo's root `.claude-plugin/marketplace.json` is a directory marketplace pointing at `./hosts/claude` | `Agent` tool with `subagent_type` `cairn:<agent>` |
| Antigravity | the tilde literal `~/.gemini/config/plugins/cairn` | `hosts/antigravity/` | extract the release, or copy the built tree, into that fixed global path | `invoke_subagent` with `TypeName` the bare agent name |
| Codex | `${PLUGIN_ROOT}`, which the definition says the host resolves to the installed plugin's root | `hosts/codex/plugins/cairn/` (the tree root is a marketplace) | `codex plugin marketplace add`, then `codex plugin add cairn@cairn` | `spawn_agent` starting a generic subagent, with no registered agent name |

On Claude Code and Antigravity the dispatch prompt is the three-line prompt alone; on Codex the two `*_PROMPT_INSTRUCTIONS` slots open it with `Read and follow the agent instructions in ${PLUGIN_ROOT}/agents/<agent>.md.` Only Antigravity's install location is a fixed path recorded in the repository: the Claude Code and Codex definitions name no install path.

### Headless invocation and records per host

`docs/ways-of-using-cairn.md` documents one headless form per host: `claude -p "/cairn:<skill> …" --dangerously-skip-permissions`, `agy -p "/cairn:<skill> …" --dangerously-skip-permissions`, and `codex exec '$cairn:<skill> …' --dangerously-bypass-approvals-and-sandbox`. Each installed CLI's help lists a machine-readable output mode, `--output-format stream-json` on `claude` (with `--print`) and on `agy`, and `--json` (JSONL events) on `codex exec`; only `agy`'s help lists a time limit for a print run (`--print-timeout`). The suite parses `agy`'s records only, and the repository holds no parser for or description of the `claude` or `codex` event records. No automated test drives `claude` or `codex`: their dispatch behaviour is recorded only in the dated hands-on blocks heading each `settings.toml` (Claude Code 2026-10-18 with its dispatch points carried forward from 2026-10-13, Codex 2026-10-13 under `codex exec` and the workspace-write sandbox), while Antigravity's block cites the suite itself for its 2026-10-26 re-check.

### Installed CLIs and plugin copies on the maintainer's machine

Checked 2026-11-09: `claude` 2.1.319, `agy` 1.4.11, and `codex-cli` 0.159.3 are all on `PATH`. `claude plugin list` reports `cairn@cairn` 1.9.0 as read from this checkout's `hosts/claude` through the directory marketplace, while `~/.claude/plugins/cache/cairn/cairn/` also holds versioned copies (1.0.0 to 1.9.0). `agy plugin list` reports cairn 1.9.0 at the global path, whose files differ from the committed `hosts/antigravity/` (it still holds `shared/get-current-milestone.md` and lacks `shared/resolve-milestone.md`), so the suite's third prerequisite does not hold as things stand. `codex plugin list` reports `cairn@cairn` installed at 1.7.6 from the local marketplace at `hosts/codex`, its files copied to `~/.codex/plugins/cache/cairn/cairn/1.7.6/`, a tree older than `hosts/codex/plugins/cairn/`.

### References to the suite by name

- `CLAUDE.md` (and `AGENTS.md`, its symlink): the Commands line `uv run pytest agy_tests`, the layout entry `agy_tests/`, and the milestones-tool invariant's sentence naming "the agy suite's fixture project", `tests/fixtures/agy_project/milestones.fixture/`, and `seeded_repo`.
- `CONTRIBUTING.md`, `## Development`: one paragraph giving the suite, its command, its prerequisite stop, and the path set whose change owes a run before committing: `scripts/hosts/antigravity/`, `core/agents/*.md`, `scripts/build_hosts.py`, and `agy_tests/`.
- `.claude/skills/release-plugin/SKILL.md`: the pre-flight's opening sentence (seven checks, one of them against shipping "an Antigravity host integration the installed `agy` no longer runs") and check **g**, which runs `git diff --name-only <LAST_TAG>..HEAD` over that same path set, runs `uv run pytest agy_tests` when it prints anything, and names the `agy suite prerequisite missing:` line.
- `scripts/hosts/antigravity/settings.toml`'s header comment ("by the agy suite"), and historical mentions in `CHANGELOG.md` (the 1.8.6 entry) and `ideas/milestones_addressed_by_path.md`.

The trigger path set names one host definition, Antigravity's, and neither of the other two.

### Sibling live milestone

`milestones/starting-state-refresh/` is live and `defined` in the same root scope. Its goal names "one test in the host-generic on-demand suite" that asserts a `derive-tasks` behaviour "on all three hosts", so it expects the suite this milestone delivers.

## Decisions

### Host selection and prerequisites

- **Host selection.** The suite's conftest registers a pytest command-line option, `--host`, taking exactly one of `claude`, `antigravity`, or `codex` per run, with no default. A run that names no host stops in the existing `pytest_cmdline_main` hook before any test, with one prerequisite-style stderr line listing the three accepted values and a non-zero exit, never a skip; an unknown value stops the same way. The option is read before the prerequisite checks, which cover only the named host.

- **Installed copy location.** Before any test the suite asks the chosen host's own CLI where the installed copy is, and takes no per-run value for it. For Claude Code it runs `claude plugin list --json` and takes the `cairn@cairn` entry for the scope that applies to a repository outside any recorded project: its `readFromFolder` when set, otherwise its `installPath`. For Codex it reads the installed `cairn@cairn` version from `codex plugin list --json` and builds `~/.codex/plugins/cache/cairn/cairn/<version>/` from it. Both read a JSON listing, never a text table. Where the CLI reports no install, the prerequisite check stops the run.

### The tests

- **Tilde pin dropped.** The plugin-root test's assertion that every read attempted with a `~` path ended in `ERROR` is removed outright, with no replacement assertion and no host-specific branch. The test keeps its host-neutral checks: the shared procedure reached at the expanded root, the `task_list.py insert` call under the root, and the two sections in the seeded list. Antigravity's tilde refusal stays recorded only in the dated hands-on block of `scripts/hosts/antigravity/settings.toml`, which no automated run re-checks.

- **Dispatch vehicle.** Each agent-dispatch test keeps a dispatching process of its own, with no orchestrator skill between it and the agent, and its prompt names the host's own dispatch mechanism, authored as one per-host value set: on Claude Code the `Agent` tool with `subagent_type` `cairn:<agent>`, on Antigravity `invoke_subagent` with the bare name as `TypeName`, as today, and on Codex `spawn_agent` starting a generic subagent. The prompt handed over is the host's real dispatch prompt: the three-line prompt alone on Claude Code and Antigravity, and on Codex that prompt opened by the line its `*_PROMPT_INSTRUCTIONS` slot renders, naming the agent file under the installed root. The pass signals stay the files the agent lands, unchanged.

## Out of Scope

