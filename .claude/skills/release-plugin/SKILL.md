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

Every step below runs **before** anything is written, committed, pushed, tagged, or
published. Each is a hard stop: on failure, report the specific reason and exit, having
changed nothing. Never work around a stop, and never ask the maintainer to waive one.

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
