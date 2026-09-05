# TASKS TODO

## Release Skill Local Release Commit

Extend the release skill so that after the gates and note composition it runs the version script, regenerates the Antigravity tree, prints a one-line advisory naming how many files beyond `.agents/plugins/cairn/plugin.json` changed when the regeneration reveals drift, and records exactly one commit under `Release: MAJOR.MINOR.PATCH` staged path-scoped to the files the version script wrote plus `.agents/plugins/cairn/`, never `git add -A`. The milestone needs the release to be a single self-consistent commit the tag can point at, produced unattended. Verified by reviewing the step against the recorded decisions and confirming the named paths match the version script's and transpiler's live write sets.

---

## Release Skill Confirmation And Publish

Extend the release skill with the single pre-publish pause that shows the maintainer the version and the full composed release body, then on approval pushes `main`, pushes a bare `MAJOR.MINOR.PATCH` tag, and creates the GitHub release via `gh` with that body, each step check-then-do (`git rev-parse`, `git ls-remote --tags`, `gh release view`) so a re-run with the same version skips what already succeeded and stops on an artifact that exists but disagrees with the expected state; legacy `v.0.9.x` tags are never touched. The milestone needs one human veto point before anything becomes public and a re-run as the whole recovery story. Verified by reviewing the step against the recorded decisions and confirming each check command resolves correctly against the live `0.9.9` tag and release.

---
