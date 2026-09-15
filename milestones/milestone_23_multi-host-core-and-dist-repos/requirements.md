# Milestone 23: Multi-Host Core And Dist Repos

## Goal

Restructure cairn into a host-neutral `core/` (skills, agents, shared procedures, with a neutral plugin-root placeholder) from which a single build script generates every host plugin into a committed `hosts/<host>/` tree, starting with Claude Code and Antigravity, each from its own manifest template, rewrite rules, and validation, so that adding a host means adding a template rather than a transpiler; the root `skills/`, `agents/`, `shared/`, and `.agents/` trees are removed and the monorepo marketplace repointed at `./hosts/claude`. Extend the release procedure so each release also publishes every `hosts/<host>` tree into its own distribution repository (`cairn-claude`, `cairn-antigravity`) as one ordinary commit tagged with the release version, with no submodules and no hand-edits to those repos, and make `cairn-claude` the documented recommended install source.

## Relevant starting state

## Decisions

## Out of Scope

