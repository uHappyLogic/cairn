# TASKS TODO

## Select The Host With A Required Option

Register a pytest command-line option `--host` in the suite's conftest taking exactly one of `claude`, `antigravity`, or `codex` per run, with no default, read in the existing `pytest_cmdline_main` hook before the prerequisite checks, which then cover only the named host; a run that names no host, or an unknown value, stops there before any test with one prerequisite-style stderr line listing the three accepted values and a non-zero exit, never a skip. Give each host one entry in the suite's Python for the values only the suite needs, and read the values a host definition already declares (its name, its built tree, and `plugin_dir`) from `scripts/hosts/<host>/settings.toml` with `tomllib`, leaving the build and the definitions' key set unchanged. It is verified by a run without `--host` and a run with an unknown value each printing that one line and exiting non-zero with no test outcome, and by a run with `--host antigravity` going on to Antigravity's prerequisite checks and no other host's.

---

## Check The Chosen Host's Installed Copy

Make the prerequisite check, for the chosen host only, find that host's CLI on `PATH`, ask the CLI where the installed copy is, and require that copy to match the host's plugin directory in the committed built tree file for file, a missing or extra file included: for Claude Code the `cairn@cairn` entry of `claude plugin list --json` for the scope that applies to a repository outside any recorded project, its `readFromFolder` when set and otherwise its `installPath`, against `hosts/claude/`; for Codex `~/.codex/plugins/cache/cairn/cairn/<version>/`, built from the installed `cairn@cairn` version in `codex plugin list --json`, against `hosts/codex/plugins/cairn/`; and for Antigravity `~/.gemini/config/plugins/cairn` against `hosts/antigravity/`. A missing CLI, a CLI reporting no install, or a mismatch stops the run before any test on the one prerequisite line, which carries that host's own remedy by its documented install (copying the built tree or extracting the release for Antigravity, re-running `codex plugin marketplace add` and `codex plugin add cairn@cairn` for Codex, refreshing the directory-marketplace install for Claude Code), and the suite still writes nothing to any installation. It is verified by running the check against each of the three hosts on this machine and confirming, for each, that the path it compares is the copy that host's CLI reports and that its outcome, a pass or the stop line with its remedy, matches whether that copy equals the built tree.

---

## Bound Every Headless Run By One Timeout

Replace the `run_agy` fixture with one shared run fixture that starts the chosen host's headless command from its entry and passes a timeout of 20 minutes, one value for every host, to the subprocess it starts, so a run that exceeds it is killed, its whole process group with it, and fails its test; `--print-timeout` is dropped from the `agy` command line, which makes the suite's limit the only bound on every host. It is verified by a run made to outlast a shortened limit being killed with every process of its group and failing its test, and by the `agy` command the fixture composes carrying no `--print-timeout`.

---

## Pass The Suite On Antigravity Through Host Entries

Rework the plugin-root resolution test and both agent-dispatch tests so every assertion on the host's tool-call records and each dispatching process's prompt goes through the chosen host's entry (a record parser for that host's shape with its own read, shell, dispatch, and write tool names and its way of telling a completed call from a failed one, and the wording that names its dispatch mechanism), with Antigravity's existing parsing and `invoke_subagent` prompt becoming its entry and the tilde-pin assertion removed outright, with no replacement assertion and no host-specific branch, while every other record assertion and the file pass signals stay. Start by refreshing the installed copy at `~/.gemini/config/plugins/cairn` from the built `hosts/antigravity/` tree, have `uv run pytest host_tests --host antigravity` pass all three tests with none marked or skipped, then add one re-check sentence (the date, the installed `agy` version, that the check ran by the host suite and under which invocation, the points it covered) after the 2026-10-26 sentence of the hands-on block in `scripts/hosts/antigravity/settings.toml`, the rest of the block standing. A failure caused by the plugin's Antigravity integration rather than by the suite is not fixed in this task: stop and report the defect, which lands as its own task of this milestone.

---

## Pass The Suite On Claude Code

Add Claude Code's entry to the host suite: its headless command (`claude -p` with `--dangerously-skip-permissions` and `--output-format stream-json`), a parser for its stream-json records with its own read, shell, dispatch, and write tool names and its way of telling a completed call from a failed one, and a dispatching prompt that names the `Agent` tool with `subagent_type` `cairn:<agent>` and hands over the three-line dispatch prompt alone. Start by refreshing the directory-marketplace install so the prerequisite check passes, have `uv run pytest host_tests --host claude` pass all three tests with every record assertion kept and none marked or skipped, then append one re-check sentence (the date, the installed `claude` version, that the check ran by the host suite and under which invocation, the points it covered) to the hands-on block of `scripts/hosts/claude/settings.toml`, whose earlier text stands. A failure caused by the plugin's Claude Code integration rather than by the suite is not fixed in this task: stop and report the defect, which lands as its own task of this milestone.

---

## Pass The Suite On Codex

Add Codex's entry to the host suite: its headless command (`codex exec` with `--json` and, on every run, `--dangerously-bypass-approvals-and-sandbox`), a parser for its JSONL events with its own read, shell, dispatch, and write tool names and its way of telling a completed call from a failed one, and a dispatching prompt that names `spawn_agent` starting a generic subagent and hands over the three-line dispatch prompt opened by the line the host's `*_PROMPT_INSTRUCTIONS` slot renders, naming the agent file under the installed root. Start by refreshing the installed copy with `codex plugin marketplace add` and `codex plugin add cairn@cairn` so the prerequisite check passes, have `uv run pytest host_tests --host codex` pass all three tests with every record assertion kept and none marked or skipped, then append one re-check sentence (the date, the installed `codex-cli` version, that the check ran by the host suite and under which invocation, the points it covered) to the hands-on block of `scripts/hosts/codex/settings.toml`, whose earlier text stands. A failure caused by the plugin's Codex integration rather than by the suite is not fixed in this task: stop and report the defect, which lands as its own task of this milestone.

---

## Describe The Host Suite In Contributor Docs

Rewrite the descriptions of the suite, which after the rename still describe an Antigravity-only suite, to match the host-generic one: `CONTRIBUTING.md`'s suite paragraph gives the `--host` choice, each host's prerequisite stop with its remedy (bringing the installed copy up to date by hand with that host's documented install), and one trigger set per host, that host's definition directory (`scripts/hosts/claude/`, `scripts/hosts/antigravity/`, or `scripts/hosts/codex/`) plus the host-neutral paths `core/agents/*.md`, `scripts/build_hosts.py`, and the suite's directory, asking for a run against each host whose set the change touches, and `CLAUDE.md`'s command and layout lines describe a suite that drives the chosen host's installed CLI against that host's installed plugin copy. It is verified by reading each statement against the suite's conftest and by the command the two files give running as written.

---

## Split The Release Pre-Flight Check Per Host

Rewrite check g of `.claude/skills/release-plugin/SKILL.md`, and the pre-flight's opening sentence that names what it guards, so the check keeps one trigger set per host, that host's definition directory (`scripts/hosts/claude/`, `scripts/hosts/antigravity/`, or `scripts/hosts/codex/`) plus the host-neutral paths `core/agents/*.md`, `scripts/build_hosts.py`, and the suite's directory, diffs each set against `<LAST_TAG>..HEAD`, and runs `uv run pytest host_tests --host <host>` only against the hosts whose set printed anything, so a host-neutral change runs all three and a change to one host's definition runs that host alone, a non-zero exit or the `host suite prerequisite missing:` line still stopping the release. The check guards only Antigravity's integration today, and a release must not ship any host's integration that host's installed CLI no longer runs. It is verified by running the three diffs against the last release tag and confirming the hosts they select, and by the check's commands running as written.

---
