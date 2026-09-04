# Milestone 17: Versioning And Release Tooling

## Goal

Put cairn's own versioning on a rail: add a version script under `scripts/` that writes a given `MAJOR.MINOR.PATCH` literal into every in-repo place a version belongs — auditing the repo first to decide that full set and adding a version to surfaces that carry none today, starting with the generated Antigravity manifest — and a maintainer-only release skill under `.claude/skills/` that takes the version as its argument, runs the script, regenerates the Antigravity tree, commits, pushes, tags, and creates the GitHub release with notes it composes from the changes since the last release (the `milestones/README.md` history entries added since the last release, cross-checked against the commit range). The script only edits files and never touches git or `gh`; the skill owns every git and `gh` step, refuses to run on a dirty working tree, and pushes any local commits before it pushes the tag. Neither artifact ships to consuming projects or falls under the plugin's runtime-layer skill invariants, the going-forward tag format is bare `MAJOR.MINOR.PATCH`, and the legacy `v.0.9.x` tags are left untouched.

## Relevant starting state

### Version-bearing surfaces

The only in-repo file that carries a plugin version today is `.claude-plugin/plugin.json` (`"version": "0.9.9"`). It was hand-aligned with the release tag in commit `503cb27` (`Manifest-version: align plugin.json with release tag 0.9.9`); before that it had read `1.0.0` since milestone 3 and never tracked releases. `.claude-plugin/marketplace.json` carries no version at all — its single `plugins[]` entry has only `name`, `source`, and `description`. `pyproject.toml` (`cairn-tooling`, `version = "0.1.0"`) versions the transpilation tooling, not the plugin, and has never moved. `README.md` embeds no version literal; its release badge (`img.shields.io/github/v/release/uHappyLogic/cairn?…&display_name=tag`) reads the latest GitHub release tag live. A repo-wide grep for `0.9.` and `"version"` outside `milestones/` and `.git/` hits only `plugin.json`.

### Generated Antigravity tree and transpiler

`scripts/migrate_skills_to_agy.py` is the only script under `scripts/`, run as `uv run scripts/migrate_skills_to_agy.py` (Python 3.13 via `.python-version`, `pyyaml` the sole dependency). On every run it **rewrites** `.agents/plugins/cairn/plugin.json` from a hard-coded dict — `$schema`, `name`, and `description: "Ported plugin for cairn"` — with no version key, so any version added to that manifest by hand is lost on the next regeneration; the version must come from the script itself. It also deletes and recopies `skills/` (skipping any directory whose name ends in `-workspace`), `agents/`, and `shared/` into the tree. The generated tree (32 files) is **checked in**, and the last two milestones each closed with a regeneration commit, so "regenerate the Antigravity tree" already has an established place in the finish ritual but no automation.

### Tags and GitHub releases

Ten tags exist across three formats: `v.0.9.0` through `v.0.9.6` (dotted legacy), `v0.9.7`, and bare `0.9.8` and `0.9.9` — the goal's bare `MAJOR.MINOR.PATCH` format is already in use for the last two. Each tag has a matching GitHub release on `uHappyLogic/cairn` (latest `0.9.9`, created 2026-09-04, not draft or prerelease). The `0.9.8` and `0.9.9` release bodies follow one hand-written shape: one `## <Milestone title> (milestone <N>)` section per milestone finished since the prior release, each a bulleted summary, closing with a `**Full Changelog**: …/compare/<prev>...<new>` link. Release `0.9.9` covered milestones 15 and 16 (80 commits from `0.9.8`); its bullets are condensed rewrites of the corresponding `milestones/README.md` history entries, not verbatim copies. `gh` 2.96.0 is installed and authenticated to `uHappyLogic` over SSH; the `origin` remote is `git@github.com:uHappyLogic/cairn.git`. There is no release automation: `.github/` holds only the README banner image, and no workflow files exist.

### Milestone history as release-note source

`milestones/README.md` carries a `## Milestone History` section with one `### Milestone <N> — <Title>` entry per finished milestone (newest first, bulleted), plus the `## Completed Milestones` table (`# | Title | Path`) that `finish-current-milestone` appends to. Each history entry lands in exactly one `Milestone-finish: milestone_<NN>_<slug>` commit touching `milestones/README.md`, so "history entries added since the last release" is recoverable as the `Milestone-finish:` commits in `<last-tag>..HEAD`, and cross-checkable by diffing the `### Milestone` headings of that file at the two ends of the range. Since `0.9.9` there are three commits and no finished milestone: the `Manifest-version:` bump plus milestone 17's definition and activation.

### Maintainer-only skill location

`.claude/` contains only `settings.json` (enabling the `skill-creator` plugin) and `settings.local.json`; there is no `.claude/skills/` directory, so the release skill will be the first project-local skill. The plugin's shipped skills all live under `skills/` (21 directories), which the transpiler copies into the Antigravity tree and which the `CLAUDE.md` runtime-layer invariants govern; `.claude/skills/` is outside both. `AGENTS.md` is a symlink to `CLAUDE.md`, so it needs no separate maintenance.

### Commit conventions relevant to the release path

Every committing skill stages path-scoped and commits under a `<Marker>: <descriptor>` subject via `shared/commit-procedure.md`, which also supplies the dirty-own-path no-op guard. The working tree is clean at `c91eb5a`, and the one prior version bump used the ad-hoc subject `Manifest-version:`. Commits authored through Claude carry a `Co-Authored-By:` trailer in the body.

## Decisions

## Out of Scope

