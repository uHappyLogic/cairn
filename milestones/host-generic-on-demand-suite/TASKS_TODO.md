# TASKS TODO

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
