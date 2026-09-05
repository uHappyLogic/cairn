# TASKS TODO

## Version Script Writes Every Version Surface

Add a version script under `scripts/` that takes one bare `MAJOR.MINOR.PATCH` literal as its argument, refuses anything else, and writes it into `.claude-plugin/plugin.json`, a new `version` field on the single `plugins[]` entry in `.claude-plugin/marketplace.json`, and `pyproject.toml` (moving `cairn-tooling` off its independent `0.1.0`), keeping the matching `cairn-tooling` version line in `uv.lock` in step; it never touches the generated `.agents/plugins/cairn/plugin.json`, git, or `gh`. The milestone needs one command that bumps every source version literal so a release leaves no per-file judgement call. Verified by running it with a test version, confirming exactly those files changed with the literal in each, and reverting.

---

## Transpiler Copies Plugin Version Into Manifest

Change `scripts/migrate_skills_to_agy.py` so the manifest dict it writes to `.agents/plugins/cairn/plugin.json` carries a `version` key read from `.claude-plugin/plugin.json` at generation time, so the generated tree is correct on every regeneration path including a bare standalone `uv run scripts/migrate_skills_to_agy.py`. The milestone needs the generated manifest to carry a version while keeping the source manifest the single source of truth. Verified by regenerating the tree and confirming the generated manifest's `version` equals the source manifest's `0.9.9`, with no other generated file changing.

---

## Release Skill Pre-Flight And Version Gates

Create the maintainer-only skill at `.claude/skills/release-plugin/SKILL.md`, invoked as `/release-plugin <MAJOR.MINOR.PATCH>`, whose opening steps resolve the last release as the nearest tag reachable from HEAD via `git describe --tags --abbrev=0`, apply the four hard pre-flight stops (tracked working tree clean, HEAD on `main`, `main` not behind `origin/main` after a fetch, no untracked files under `skills/`, `agents/`, or `shared/`), and hard-refuse the version argument when it is malformed, when its tag already exists locally or remotely, or when it is not strictly greater than the last release compared as a numeric tuple. The milestone needs every route by which a bad version or unmerged content could reach a published tag closed before anything mutates, and this skill's `SKILL.md` is the only place the release procedure is documented. Verified by reviewing the skill against the recorded decisions and running its check commands against the live repo to confirm they resolve `0.9.9` and pass or stop as expected.

---

## Release Notes From Milestone History

Extend the release skill with a note-composition step that gathers the `Milestone-finish:` commits in `<last-tag>..HEAD`, cross-checks them against the `### Milestone` headings added to `milestones/README.md` over that range, stops and prints both sides on any mismatch in either direction, and on an empty range shows commit-range-derived notes and proceeds only on explicit maintainer confirmation; otherwise it rewrites each milestone's history bullets into one condensed `## <Title> (milestone <N>)` section per milestone, closing with a `**Full Changelog**` compare link from the last tag to the new version. The milestone needs release notes composed from the history entries and matched to the shape of the published `0.9.8` and `0.9.9` bodies. Verified by reviewing the step against the recorded decisions and walking it against the live `0.9.9..HEAD` range, which must take the empty-range path.

---

## Release Skill Local Release Commit

Extend the release skill so that after the gates and note composition it runs the version script, regenerates the Antigravity tree, prints a one-line advisory naming how many files beyond `.agents/plugins/cairn/plugin.json` changed when the regeneration reveals drift, and records exactly one commit under `Release: MAJOR.MINOR.PATCH` staged path-scoped to the files the version script wrote plus `.agents/plugins/cairn/`, never `git add -A`. The milestone needs the release to be a single self-consistent commit the tag can point at, produced unattended. Verified by reviewing the step against the recorded decisions and confirming the named paths match the version script's and transpiler's live write sets.

---

## Release Skill Confirmation And Publish

Extend the release skill with the single pre-publish pause that shows the maintainer the version and the full composed release body, then on approval pushes `main`, pushes a bare `MAJOR.MINOR.PATCH` tag, and creates the GitHub release via `gh` with that body, each step check-then-do (`git rev-parse`, `git ls-remote --tags`, `gh release view`) so a re-run with the same version skips what already succeeded and stops on an artifact that exists but disagrees with the expected state; legacy `v.0.9.x` tags are never touched. The milestone needs one human veto point before anything becomes public and a re-run as the whole recovery story. Verified by reviewing the step against the recorded decisions and confirming each check command resolves correctly against the live `0.9.9` tag and release.

---
