# TASKS DONE

## Version Script Writes Every Version Surface

Add a version script under `scripts/` that takes one bare `MAJOR.MINOR.PATCH` literal as its argument, refuses anything else, and writes it into `.claude-plugin/plugin.json`, a new `version` field on the single `plugins[]` entry in `.claude-plugin/marketplace.json`, and `pyproject.toml` (moving `cairn-tooling` off its independent `0.1.0`), keeping the matching `cairn-tooling` version line in `uv.lock` in step; it never touches the generated `.agents/plugins/cairn/plugin.json`, git, or `gh`. The milestone needs one command that bumps every source version literal so a release leaves no per-file judgement call. Verified by running it with a test version, confirming exactly those files changed with the literal in each, and reverting.

**Verified:**

- `scripts/set_version.py` exists under `scripts/` and runs as `uv run scripts/set_version.py <version>`.
- It accepts exactly one bare `MAJOR.MINOR.PATCH` literal and refuses anything else with a non-zero exit and no file change: zero arguments, two arguments, `v1.2.3`, `1.2`, `1.2.3.4`, `1.2.3-rc1`, `abc`, and `01.2.3` all stopped with an error and left the tree clean.
- A run with test version `9.9.9` wrote `"version": "9.9.9"` into `.claude-plugin/plugin.json`.
- The same run added `"version": "9.9.9"` to the single `plugins[]` entry in `.claude-plugin/marketplace.json`, which carried no version field before.
- The same run moved `pyproject.toml`'s `[project]` version off `0.1.0` to `version = "9.9.9"`.
- The same run kept `uv.lock`'s `cairn-tooling` `[[package]]` version in step at `version = "9.9.9"`.
- `git status --porcelain` after that run listed exactly those four files as modified (plus the new untracked script), each `git diff` hunk touching only its version line, and `git status --porcelain .agents/` was empty, so the generated `.agents/plugins/cairn/plugin.json` was not touched.
- The script invokes no git and no `gh`: it imports only `json`, `os`, `re`, and `sys`, with no `subprocess` or `os.system` use, and the only `.agents`/git/gh mentions in the file are in its docstring.
- A second identical run left the same four modified files and nothing further, and a run from a directory without the surfaces failed before writing anything, leaving all files unchanged.
- Reverting the four files with `git checkout --` restored `0.9.9`/`0.1.0` and left the working tree carrying only the new script.

---

## Transpiler Copies Plugin Version Into Manifest

Change `scripts/migrate_skills_to_agy.py` so the manifest dict it writes to `.agents/plugins/cairn/plugin.json` carries a `version` key read from `.claude-plugin/plugin.json` at generation time, so the generated tree is correct on every regeneration path including a bare standalone `uv run scripts/migrate_skills_to_agy.py`. The milestone needs the generated manifest to carry a version while keeping the source manifest the single source of truth. Verified by regenerating the tree and confirming the generated manifest's `version` equals the source manifest's `0.9.9`, with no other generated file changing.

**Verified:**

- `scripts/migrate_skills_to_agy.py` reads `.claude-plugin/plugin.json` at generation time and copies its `version` value into the dict it writes to `.agents/plugins/cairn/plugin.json`.
- No version literal is hard-coded in the transpiler: a repo-root grep for `[0-9]+\.[0-9]+\.[0-9]+` over the script returns nothing, so the source manifest is the sole source.
- A bare `uv run scripts/migrate_skills_to_agy.py` from the repository root produced a generated manifest whose `version` is `"0.9.9"`, equal to the source manifest's value.
- The generated manifest keeps its existing `$schema`, `name`, and `description` keys unchanged: `git diff` on it shows only the added `version` line.
- After that regeneration `git status --porcelain` listed `.agents/plugins/cairn/plugin.json` as the only changed generated file (alongside the edited script), and a second run added no further changes.
- A source manifest that is missing, unreadable, or carries no `version` value stops the run with a clear error and a non-zero exit before any generated manifest is written, rather than emitting a version-less manifest.
- Pointing the script at a source manifest carrying `3.4.5` produced a generated manifest with `"version": "3.4.5"`, confirming the value is read per run rather than fixed.

---

## Release Skill Pre-Flight And Version Gates

Create the maintainer-only skill at `.claude/skills/release-plugin/SKILL.md`, invoked as `/release-plugin <MAJOR.MINOR.PATCH>`, whose opening steps resolve the last release as the nearest tag reachable from HEAD via `git describe --tags --abbrev=0`, apply the four hard pre-flight stops (tracked working tree clean, HEAD on `main`, `main` not behind `origin/main` after a fetch, no untracked files under `skills/`, `agents/`, or `shared/`), and hard-refuse the version argument when it is malformed, when its tag already exists locally or remotely, or when it is not strictly greater than the last release compared as a numeric tuple. The milestone needs every route by which a bad version or unmerged content could reach a published tag closed before anything mutates, and this skill's `SKILL.md` is the only place the release procedure is documented. Verified by reviewing the skill against the recorded decisions and running its check commands against the live repo to confirm they resolve `0.9.9` and pass or stop as expected.

**Verified:**

- `.claude/skills/release-plugin/SKILL.md` exists as the sole documented home of the release procedure, with no release paragraph added to `CLAUDE.md` or `README.md`.
- It carries YAML frontmatter that loads under `yaml.safe_load` with an unquoted `name: release-plugin` and a single-sentence 22-word `description` free of colons and semicolons.
- It documents the invocation `/release-plugin <MAJOR.MINOR.PATCH>` with a bare, unprefixed version literal as the sole argument.
- Its step 1 resolves the last release as the nearest tag reachable from HEAD via `git describe --tags --abbrev=0`, used literally for the `<LAST_TAG>..HEAD` range and the compare-link endpoint; run live it resolves `0.9.9`.
- Its step 2 applies the four hard pre-flight stops — tracked working tree clean (`git status --porcelain --untracked-files=no`), HEAD on `main` (`git rev-parse --abbrev-ref HEAD`), `main` not behind `origin/main` after `git fetch origin main` (`git rev-list --count main..origin/main`), and no untracked files under `skills/`, `agents/`, `shared/` (`git ls-files --others --exclude-standard`), tolerating untracked files elsewhere; all four pass against the live repo (empty, `main`, `0`, empty).
- Its step 3 hard-refuses a malformed version literal against `^[0-9]+\.[0-9]+\.[0-9]+$`, which accepts `1.0.0` and rejects `v1.0.0` when run live.
- Its step 3 hard-refuses a version whose tag already exists by exact-name lookup locally (`git tag --list`) and remotely (`git ls-remote --tags origin refs/tags/<VERSION>`); run live both return `0.9.9` and neither returns `1.0.0`.
- Its step 3 hard-refuses a version not strictly greater than the last release, comparing `(major, minor, patch)` as integers after normalizing a legacy `v`/`v.` prefix off `<LAST_TAG>`, never by tag-name sort.
- Every gate runs pre-mutation and each failure stops the run reporting the specific reason while changing nothing, and legacy `v.0.9.x` tags are never touched.

---

## Release Notes From Milestone History

Extend the release skill with a note-composition step that gathers the `Milestone-finish:` commits in `<last-tag>..HEAD`, cross-checks them against the `### Milestone` headings added to `milestones/README.md` over that range, stops and prints both sides on any mismatch in either direction, and on an empty range shows commit-range-derived notes and proceeds only on explicit maintainer confirmation; otherwise it rewrites each milestone's history bullets into one condensed `## <Title> (milestone <N>)` section per milestone, closing with a `**Full Changelog**` compare link from the last tag to the new version. The milestone needs release notes composed from the history entries and matched to the shape of the published `0.9.8` and `0.9.9` bodies. Verified by reviewing the step against the recorded decisions and walking it against the live `0.9.9..HEAD` range, which must take the empty-range path.

**Verified:**

- `.claude/skills/release-plugin/SKILL.md` gains a note-composition step (step 5) that runs before any mutating step and remains the sole documented home of the release procedure, with no release prose added to `CLAUDE.md` or `README.md`.
- Step 5a gathers the finished milestones from `git log --grep='^Milestone-finish: ' --format='%s' <LAST_TAG>..HEAD -- milestones/README.md`, reading each subject's `milestone_<NN>_` number as an integer.
- Step 5b gathers the `### Milestone` headings added to `milestones/README.md` over the same range by diffing the sorted heading lists at `<LAST_TAG>` and HEAD, taking the added (`>`) lines' numbers as integers.
- Step 5c requires the two sides to name the same set of milestone numbers and stops on a mismatch in either direction — a finish commit with no history entry, or a history entry with no finish commit — printing both sides and changing nothing.
- Step 5d handles the empty range by stating plainly that no milestone was finished since `<LAST_TAG>`, building commit-range-derived notes (a single `## Changes since <LAST_TAG>` section plus the compare link) from `git log --format='%s' <LAST_TAG>..HEAD`, showing that full body, and proceeding only on an explicit affirmative answer.
- Step 5e composes one `## <Title> (milestone <N>)` section per finished milestone, highest number first, as condensed rewrites of the history bullets rather than verbatim copies, cutting milestone-internal process detail — the shape the published `0.9.8` and `0.9.9` bodies set.
- Step 5f closes `<RELEASE_BODY>` with `**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/<LAST_TAG>...<VERSION>`, using `<LAST_TAG>` literally whatever its format.
- Walked live against `0.9.9..HEAD`: the commit side is empty and the heading diff is empty, so both sides agree and the run takes the empty-range path of step 5d, as the task requires.
- Sanity-walked the non-empty case against `0.9.8..0.9.9`: the commit side returns milestones 16 and 15 and the heading diff returns exactly those two added entries, so the cross-check matches and the highest-number-first ordering reproduces the published `0.9.9` body's section order.
- The step is read-only — every command it names is a `git log`, `git show`, `grep`, or `diff` — and `git status --porcelain` after the walk listed only the edited `SKILL.md`.
- The skill's frontmatter still loads under `yaml.safe_load` with an unquoted 22-word `description`, and the file stays under `.claude/skills/`, outside the transpiled `skills/` tree.

---

## Release Skill Local Release Commit

Extend the release skill so that after the gates and note composition it runs the version script, regenerates the Antigravity tree, prints a one-line advisory naming how many files beyond `.agents/plugins/cairn/plugin.json` changed when the regeneration reveals drift, and records exactly one commit under `Release: MAJOR.MINOR.PATCH` staged path-scoped to the files the version script wrote plus `.agents/plugins/cairn/`, never `git add -A`. The milestone needs the release to be a single self-consistent commit the tag can point at, produced unattended. Verified by reviewing the step against the recorded decisions and confirming the named paths match the version script's and transpiler's live write sets.

**Verified:**

- `.claude/skills/release-plugin/SKILL.md` gains step 6, placed after the pre-flight/version gates (steps 2 and 3) and the note-composition step (step 5) and before any push, tag, or publish step, and remains the sole documented home of the release procedure — a grep of `CLAUDE.md` and `README.md` for `release-plugin` and `Release: ` returns nothing.
- Step 6a runs the version script as `uv run scripts/set_version.py <VERSION>` and stops the release on a non-zero exit; run live with test version `9.9.9` it wrote exactly the four surfaces it owns.
- Step 6b regenerates the Antigravity tree with `uv run scripts/migrate_skills_to_agy.py` and states the ordering constraint that it must follow 6a; run live after 6a the generated `.agents/plugins/cairn/plugin.json` carried `"version": "9.9.9"`, confirming the ordering is what makes the generated manifest correct.
- Step 6c counts the generated files changed beyond `.agents/plugins/cairn/plugin.json` with a `git status --porcelain --untracked-files=all -- .agents/plugins/cairn/` piped through a `grep -v` of that manifest path, and prints a one-line advisory naming the drift and the count when that produces output; run live after the regeneration it produced no lines, so the ordinary no-drift path prints nothing.
- Step 6c proceeds unconditionally after the advisory — it is explicitly never a stop and never a review prompt, and the full regeneration result is absorbed into the release commit.
- Step 6e records exactly one commit under the subject `Release: <VERSION>` with the bare literal, forbidding a split between the version bump and the regeneration and forbidding a later amend.
- Step 6d stages path-scoped by explicitly named paths and bans both `git add -A` and `git add .`; run live, `git add --` over the five named paths staged exactly those five and left an unrelated dirty file (`.claude/skills/release-plugin/SKILL.md`) unstaged.
- The four version-script paths named in 6d — `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `pyproject.toml`, `uv.lock` — match `scripts/set_version.py`'s live `RENDERERS` write set exactly, in the same order and with no path missing or extra.
- The fifth named path `.agents/plugins/cairn/` matches `scripts/migrate_skills_to_agy.py`'s live write set: every write it makes (the manifest, `mcp_config.json`, `skills/`, `agents/`, `shared/`) is under its `plugin_dir` of `.agents/plugins/cairn`.
- The claim in 6d that a path-scoped `git add` also records removals holds on the live git (2.50.1): in a scratch repo `git add -- d/` after deleting `d/y` staged `D d/y`.
- Step 6e's post-commit completeness check (`git status --porcelain --untracked-files=no` must be empty, otherwise stop) is present, and the step ends by carrying `<VERSION>`, `<LAST_TAG>`, and `<RELEASE_BODY>` forward without creating the tag.
- The skill's frontmatter still loads under `yaml.safe_load` with an unquoted `name: release-plugin` and a 22-word `description` free of colons and semicolons.
- The rehearsal was fully reverted: `git status --porcelain --untracked-files=all` afterwards lists only the edited `SKILL.md`, with `.claude-plugin/plugin.json` and the generated manifest both back at `0.9.9`.

---
