# TASKS TODO

## Describe The Host Suite In Contributor Docs

Rewrite the descriptions of the suite, which after the rename still describe an Antigravity-only suite, to match the host-generic one: `CONTRIBUTING.md`'s suite paragraph gives the `--host` choice, each host's prerequisite stop with its remedy (bringing the installed copy up to date by hand with that host's documented install), and one trigger set per host, that host's definition directory (`scripts/hosts/claude/`, `scripts/hosts/antigravity/`, or `scripts/hosts/codex/`) plus the host-neutral paths `core/agents/*.md`, `scripts/build_hosts.py`, and the suite's directory, asking for a run against each host whose set the change touches, and `CLAUDE.md`'s command and layout lines describe a suite that drives the chosen host's installed CLI against that host's installed plugin copy. It is verified by reading each statement against the suite's conftest and by the command the two files give running as written.

---

## Split The Release Pre-Flight Check Per Host

Rewrite check g of `.claude/skills/release-plugin/SKILL.md`, and the pre-flight's opening sentence that names what it guards, so the check keeps one trigger set per host, that host's definition directory (`scripts/hosts/claude/`, `scripts/hosts/antigravity/`, or `scripts/hosts/codex/`) plus the host-neutral paths `core/agents/*.md`, `scripts/build_hosts.py`, and the suite's directory, diffs each set against `<LAST_TAG>..HEAD`, and runs `uv run pytest host_tests --host <host>` only against the hosts whose set printed anything, so a host-neutral change runs all three and a change to one host's definition runs that host alone, a non-zero exit or the `host suite prerequisite missing:` line still stopping the release. The check guards only Antigravity's integration today, and a release must not ship any host's integration that host's installed CLI no longer runs. It is verified by running the three diffs against the last release tag and confirming the hosts they select, and by the check's commands running as written.

---
