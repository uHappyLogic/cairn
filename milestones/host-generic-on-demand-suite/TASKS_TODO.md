# TASKS TODO

## Split The Release Pre-Flight Check Per Host

Rewrite check g of `.claude/skills/release-plugin/SKILL.md`, and the pre-flight's opening sentence that names what it guards, so the check keeps one trigger set per host, that host's definition directory (`scripts/hosts/claude/`, `scripts/hosts/antigravity/`, or `scripts/hosts/codex/`) plus the host-neutral paths `core/agents/*.md`, `scripts/build_hosts.py`, and the suite's directory, diffs each set against `<LAST_TAG>..HEAD`, and runs `uv run pytest host_tests --host <host>` only against the hosts whose set printed anything, so a host-neutral change runs all three and a change to one host's definition runs that host alone, a non-zero exit or the `host suite prerequisite missing:` line still stopping the release. The check guards only Antigravity's integration today, and a release must not ship any host's integration that host's installed CLI no longer runs. It is verified by running the three diffs against the last release tag and confirming the hosts they select, and by the check's commands running as written.

---
