# Milestone 17: Versioning And Release Tooling

## Goal

Put cairn's own versioning on a rail: add a version script under `scripts/` that writes a given `MAJOR.MINOR.PATCH` literal into every in-repo place a version belongs — auditing the repo first to decide that full set and adding a version to surfaces that carry none today, starting with the generated Antigravity manifest — and a maintainer-only release skill under `.claude/skills/` that takes the version as its argument, runs the script, regenerates the Antigravity tree, commits, pushes, tags, and creates the GitHub release with notes it composes from the changes since the last release (the `milestones/README.md` history entries added since the last release, cross-checked against the commit range). The script only edits files and never touches git or `gh`; the skill owns every git and `gh` step, refuses to run on a dirty working tree, and pushes any local commits before it pushes the tag. Neither artifact ships to consuming projects or falls under the plugin's runtime-layer skill invariants, the going-forward tag format is bare `MAJOR.MINOR.PATCH`, and the legacy `v.0.9.x` tags are left untouched.

## Relevant starting state

## Decisions

## Out of Scope

