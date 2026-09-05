---
name: release-plugin
description: Cut a cairn plugin release for a given MAJOR.MINOR.PATCH version, running every pre-flight and version gate before anything is changed or published.
---

# release-plugin

Releases the cairn plugin at a maintainer-supplied `MAJOR.MINOR.PATCH` version. This
`SKILL.md` is the single place the release procedure is documented — no release prose lives
in `CLAUDE.md` or `README.md`. It is a maintainer-only, project-local skill: it lives under
`.claude/skills/`, outside the shipped `skills/` tree, so it is never transpiled into
`.agents/plugins/cairn/` and never reaches a consuming project.

The going-forward tag format is a bare `MAJOR.MINOR.PATCH`. The legacy `v.0.9.x` and
`v0.9.7` tags are never created, moved, or deleted by this skill.

Nothing is written, committed, pushed, tagged, or published until every gate below has
passed and the release notes have been composed. The pre-flight and version gates (steps 2
and 3) are hard stops: on failure, report the specific reason and exit, having changed
nothing. Never work around a gate, and never ask the maintainer to waive one.

## Usage

```
/release-plugin <MAJOR.MINOR.PATCH>
```

- `<MAJOR.MINOR.PATCH>`: the version literal to release, e.g. `1.0.0`. Bare — no `v`
  prefix, no suffix.

**Example:**
```
/release-plugin 1.0.0
```

Call the argument `<VERSION>` from here on.

## Workflow

### 1. Resolve the last release

The last release is the **nearest tag reachable from HEAD**:

```bash
git describe --tags --abbrev=0
```

Call the exact tag string it prints `<LAST_TAG>`. Use it literally wherever the release run
needs the previous release — the `<LAST_TAG>..HEAD` commit range and the compare-link
endpoint alike. Both are ancestry questions, so the mixed legacy tag formats do not matter
there and no version string is parsed for them; the one place `<LAST_TAG>` is read as a
version is the monotonicity check in step 3.

If the command fails (no tag is reachable from HEAD), stop and report that the last release
could not be resolved.

### 2. Pre-flight stops

Run all four checks. Each one blocks a route by which uncommitted or unmerged content could
reach a published tag, so any failure stops the run.

**a. The tracked working tree is clean.**

```bash
git status --porcelain --untracked-files=no
```

Any output means tracked modifications or staged changes are pending. Stop and report them.

**b. HEAD is on `main`.**

```bash
git rev-parse --abbrev-ref HEAD
```

Anything other than `main` — including a detached HEAD, which prints `HEAD` — stops the run.
Report the branch found.

**c. `main` is not behind `origin/main`.**

```bash
git fetch origin main
git rev-list --count main..origin/main
```

A non-zero count means `origin/main` carries commits `main` does not, so the release would
tag an outdated tree. Stop and report the count. Being *ahead* of `origin/main` is fine and
expected — those local commits are pushed later in the run.

**d. No untracked files under the transpiler's source paths.**

```bash
git ls-files --others --exclude-standard -- skills/ agents/ shared/
```

Any output means a source file that would belong in the release is not committed. Stop and
list the files. Untracked files **elsewhere** in the repo are tolerated and are not checked:
staging is path-scoped, so they cannot be picked up.

### 3. Validate the version argument

All three refusals are hard and pre-mutation. A bad version caught here costs an error
message; caught later it would cost reverting a pushed commit and deleting a published
release. A maintainer who genuinely needs a non-monotonic or backfill release tags manually,
outside this skill.

**a. The literal is well-formed.**

`<VERSION>` must match `^[0-9]+\.[0-9]+\.[0-9]+$` — exactly three dot-separated numeric
components, no `v` prefix, no pre-release or build suffix. Otherwise stop and report the
expected shape.

**b. The tag does not already exist.** Look the exact tag name up locally and on the remote:

```bash
git tag --list "<VERSION>"
git ls-remote --tags origin "refs/tags/<VERSION>"
```

Output from either means the tag is taken. Stop and report which side already has it. This
is an exact-name lookup, not a pattern search — a tag whose name merely contains `<VERSION>`
is not a match.

**c. The version is strictly greater than the last release.** Compare as a **numeric
tuple**, never by tag-name sort:

1. Normalize `<LAST_TAG>` to its numeric components: drop a leading `v` and any `.`
   immediately after it, so `v.0.9.6`, `v0.9.7`, and `0.9.9` all reduce to `0.9.6`, `0.9.7`,
   and `0.9.9`. If what remains is not three numeric components, stop and report that the
   last release could not be compared.
2. Split both `<VERSION>` and the normalized `<LAST_TAG>` on `.` and compare
   `(major, minor, patch)` as integers, most significant first.

`<VERSION>` must be strictly greater. Equal or lower stops the run, reporting both versions.

### 4. Carry the resolved values forward

With every gate passed, the run holds two resolved values — `<VERSION>`, the validated
version literal to release, and `<LAST_TAG>`, the last release anchor — and proceeds to the
rest of the release with them.

### 5. Compose the release notes

This step still mutates nothing: it reads the range, cross-checks its two sides, and builds
the release body in context. Call the finished text `<RELEASE_BODY>`; the later steps commit,
tag, and publish with it.

**a. Gather the finished milestones from the commit range.**

Each finished milestone lands in exactly one `Milestone-finish: milestone_<NN>_<slug>` commit
touching `milestones/README.md`:

```bash
git log --grep='^Milestone-finish: ' --format='%s' <LAST_TAG>..HEAD -- milestones/README.md
```

From each subject take `<NN>` — the milestone number, read as an integer so `06` and `6` are
the same milestone. Call this set the **commit side**.

**b. Gather the history entries added over the same range.** The tracked tree is clean by
step 2b, so the working file is HEAD:

```bash
diff <(git show <LAST_TAG>:milestones/README.md | grep '^### Milestone ' | sort) \
     <(grep '^### Milestone ' milestones/README.md | sort)
```

Every heading present at HEAD but not at `<LAST_TAG>` — the `>` lines — is an added entry.
Take its number from `### Milestone <N> — <Title>`, again as an integer. Call this set the
**history side**. A heading that exists at both ends but was reworded shows up as added here;
the cross-check below is what turns that into a visible stop rather than a silent
mis-numbering.

**c. Cross-check the two sides.** They must name exactly the same set of milestone numbers.
Any disagreement, in **either** direction, stops the run:

- a milestone number on the commit side with no matching history entry — a
  `/finish-current-milestone` whose `milestones/README.md` entry is missing or renumbered;
- a milestone number on the history side with no matching finish commit — a history entry
  added by hand, or a finish commit outside the range.

On any mismatch, print **both sides** — the commit-side subjects and the history-side
headings, with the unmatched numbers called out — state that nothing was changed, and exit.
The maintainer fixes the source and re-runs. The release is the one irreversible artifact in
the run, so a false stop costs a single `milestones/README.md` edit and a re-run.

**d. Empty range.** When both sides are empty — no `Milestone-finish:` commit in the range
and no history entry added — no milestone was finished since `<LAST_TAG>`. That is ambiguous
between a forgotten `/finish-current-milestone` and a deliberate version-only patch release,
and only the maintainer can tell the two apart, so:

1. State plainly that no milestone was finished since `<LAST_TAG>`.
2. Build **commit-range-derived notes** in place of the usual history-entry sections: read
   the range's commits (`git log --format='%s' <LAST_TAG>..HEAD`, reading bodies where a
   subject is not self-explanatory) and condense them into a single
   `## Changes since <LAST_TAG>` section — a short bulleted summary of the user-facing
   changes, under the same rewrite discipline as (e) below — then the Full Changelog link
   from (f).
3. Show the maintainer that full body and ask whether to release with it.
4. Proceed only on an **explicit** affirmative answer. Anything else — a refusal, a question,
   an ambiguous reply — stops the run with nothing changed.

An empty range is the only path that reaches the rest of the release without history-entry
sections, and it never takes itself silently.

**e. Compose one section per finished milestone.** Otherwise, for each milestone on the
(agreed) list, **highest number first**, read its `### Milestone <N> — <Title>` entry in
`milestones/README.md` and rewrite it into:

```markdown
## <Title> (milestone <N>)

- <condensed user-facing change>
- <condensed user-facing change>
```

`<Title>` is the heading's title text; `<N>` is the milestone number as the heading writes it.

The bullets are **condensed rewrites, never verbatim copies**. Keep what a consumer of the
plugin would notice — what the release now does, what changed for them, what was added,
renamed, or retired. Cut milestone-internal process detail: task counts, per-task ledgers,
audit passes, re-audit verdicts, which sweep touched which file, and how the work was
verified. Where several history bullets describe one user-facing change, merge them into one.
This is the shape the published `0.9.8` and `0.9.9` bodies already set, and matching it keeps
the release series consistent.

**f. Close with the compare link.** The last line of `<RELEASE_BODY>` is always:

```markdown
**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/<LAST_TAG>...<VERSION>
```

`<LAST_TAG>` is used literally, whatever its format; `<VERSION>` is the tag this run creates.
