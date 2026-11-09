# Host-generic on-demand suite

## Goal

Turn the on-demand `agy_tests/` suite into a host-generic suite that drives the installed CLI of any of the three hosts (Claude Code, Antigravity, Codex) against that host's installed plugin copy, the host chosen per run. Every test checks behaviour that is the same on every host, so the existing plugin-root resolution test and both agent-dispatch tests run and pass against all three hosts, with only the prerequisite check and the invocation differing per host. The suite's name and every reference to it (the `CLAUDE.md` command, `CONTRIBUTING.md`, the release pre-flight and its trigger paths) follow.

## Relevant starting state

## Decisions

## Out of Scope

