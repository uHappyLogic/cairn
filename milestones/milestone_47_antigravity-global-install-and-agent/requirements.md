# Milestone 47: Antigravity global install and agent tools

## Goal

Fix the two Antigravity runtime failures reported in `temp/agy_runtime_issues_report.md`: grant write and shell tool access (`enable_write_tools: true`) to the `provide-alternatives-to-open-question` and `complete-task` subagents in the Antigravity host tree, and standardize Antigravity on the global `~/.gemini/config/plugins/cairn` installation path across `plugin_root`, the rendered host tree, and the installation documentation. Add a repeatable, on-demand test suite that drives the real `agy` CLI to verify global plugin-root resolution and subagent write/shell tool execution, kept out of the default `pytest` and CI runs so it executes only when requested or when the Antigravity host integration changes.

## Relevant starting state

## Decisions

## Out of Scope

