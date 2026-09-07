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

Every tag and release is a bare `MAJOR.MINOR.PATCH`, with no `v` prefix anywhere in the
history — the legacy `v.0.9.x` and `v0.9.7` tags were renamed to their bare form on
2026-09-07, and no `v`-prefixed tag remains on either side.

Nothing is written, committed, pushed, tagged, or published until every gate below has
passed and the release notes have been composed. The pre-flight and version gates (steps 2
and 3) are hard stops: on failure, report the specific reason and exit, having changed
nothing. Never work around a gate, and never ask the maintainer to waive one.

**Resuming an interrupted release.** Re-running with the same version after a failed run is
the whole recovery story — there is no rollback of already-published refs and no hand-run
recovery command. A resumption is detected once, up front:

```bash
git log -1 --format='%s' HEAD
```

If that prints exactly `Release: <VERSION>`, this version's release commit is already
recorded and the run is a **resumption**. When it is, step 1 excludes `<VERSION>` from the
last-release lookup, step 3b tolerates a tag that points at HEAD, and step 6 is skipped whole
— the commit it would produce already exists. Every other step runs unchanged, and step 8's
per-artifact checks pick the run up from the first step that did not complete.

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
endpoint alike. Both are ancestry questions and parse no version string; the one place
`<LAST_TAG>` is read as a version is the monotonicity check in step 3.

If the command fails (no tag is reachable from HEAD), stop and report that the last release
could not be resolved.

On a **resumption**, exclude this run's own tag so the anchor stays the *previous* release:

```bash
git describe --tags --abbrev=0 --exclude=<VERSION>
```

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

**Resumption exception.** On a resumption the tag may already exist because an earlier run
pushed it before failing. A tag on either side that resolves to HEAD is that tag: leave it,
continue, and let step 8b re-check it. A tag resolving to any other commit is a genuine
collision and stops the run as above.

**c. The version is strictly greater than the last release.** Compare as a **numeric
tuple**, never by tag-name sort:

1. Confirm `<LAST_TAG>` is three numeric components — every tag is bare
   `MAJOR.MINOR.PATCH`, so it needs no normalization. If it is not, stop and report that
   the last release could not be compared.
2. Split both `<VERSION>` and `<LAST_TAG>` on `.` and compare `(major, minor, patch)` as
   integers, most significant first.

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

### 6. Apply the version, regenerate, and record the release commit

Everything so far has been read-only. This step is where the run first writes, and it
produces **exactly one commit** — the complete, self-consistent state the tag will point at.
Run it unattended: nothing here pauses for the maintainer.

**Skip this whole step on a resumption.** The `Release: <VERSION>` commit at HEAD is the
commit this step produces: the version script and the regeneration would rewrite the same
values, and the commit would find nothing staged. Carry `<VERSION>`, `<LAST_TAG>`, and
`<RELEASE_BODY>` straight into step 7.

**a. Write the version into every source surface.**

```bash
uv run scripts/set_version.py <VERSION>
```

The script takes the bare literal and writes it into the four source surfaces it owns —
`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `pyproject.toml`, and
`uv.lock` — leaving every file untouched if any one of them fails. A non-zero exit stops the
release; report what the script printed. The script never touches git, `gh`, or anything
under `.agents/`.

**b. Regenerate the Antigravity tree.**

```bash
uv run scripts/migrate_skills_to_agy.py
```

This rewrites `.agents/plugins/cairn/` from `skills/`, `agents/`, and `shared/`, and copies
the version just written into `.claude-plugin/plugin.json` through to the generated
`.agents/plugins/cairn/plugin.json`. Order matters: the regeneration must follow (a), or the
generated manifest carries the previous version. A non-zero exit stops the release.

**c. Report generated-tree drift, then proceed.**

In the ordinary case the regeneration changes only the generated manifest's version line.
When it changes more, a runtime edit reached `main` without being regenerated. Count the
generated files that changed beyond the manifest:

```bash
git status --porcelain --untracked-files=all -- .agents/plugins/cairn/ \
  | grep -v '\.agents/plugins/cairn/plugin\.json$'
```

If that produces output, print a **one-line advisory** naming the drift and how many files it
covers, for example:

```
Generated tree drift: 3 files beyond .agents/plugins/cairn/plugin.json changed on regeneration; absorbed into the release commit.
```

Then **proceed**. This is an advisory, never a stop and never a review prompt: the generated
tree is a pure deterministic derivative of already-committed sources, so the regeneration can
only produce what those sources say, and step 2a's clean tree makes the whole diff
self-generated. The advisory carries the one fact the commit alone would not surface.

**d. Stage exactly the written paths.** Name them explicitly — the four surfaces the version
script writes plus the regenerated tree:

```bash
git add -- \
  .claude-plugin/plugin.json \
  .claude-plugin/marketplace.json \
  pyproject.toml \
  uv.lock \
  .agents/plugins/cairn/
```

**Never `git add -A`** and never `git add .`. A path-scoped `git add` records additions,
modifications, and removals under those paths, so a regeneration that deletes a generated
file is staged too. Nothing else in the repo may enter the release commit.

**e. Commit once.** The subject is exactly:

```
Release: <VERSION>
```

with `<VERSION>` the bare literal, and the body following the repository's commit conventions.
One release is one commit — never split the version bump and the regeneration, and never
amend a later step into it.

Then confirm the staging was complete: `git status --porcelain --untracked-files=no` must be
empty. Any tracked change left behind means a written path was missed; stop and report it
rather than tagging a partial state. The tag is not created here — the run holds `<VERSION>`,
`<LAST_TAG>`, and `<RELEASE_BODY>` and carries them into the publish step.

### 7. Confirm before publishing

This is the run's **single pause**. Everything before it is local work a `git reset` undoes;
everything after it is public and permanent. Show the maintainer both facts they need in
order to veto:

1. `<VERSION>` — the version about to be tagged and released.
2. `<RELEASE_BODY>` — the **full** composed body, verbatim, exactly as step 8c will publish
   it. Never a summary, an excerpt, or a description of it.

Then ask whether to publish, and proceed only on an **explicit** affirmative answer. Anything
else — a refusal, a question, an edit request, an ambiguous reply — stops the run here with
nothing pushed. Say that the release commit stays at HEAD, unpushed and revertible, and that
re-running `/release-plugin <VERSION>` resumes from this point.

Step 5d's empty-range question is a different one — whether commit-derived notes are an
acceptable substitute, asked before anything is written — so an empty-range run answers both.
This gate is the only pause between the release commit and publication, and it is never
skipped.

### 8. Publish: push `main`, push the tag, create the GitHub release

Three steps in this order: the branch must carry the commit before a tag can name it, and the
tag must exist on the remote before a release can attach to it.

Every one is **check-then-do** — query the artifact first, skip the step when it already
matches the expected state, and **stop and report** when it exists but disagrees with that
state rather than resuming past it. That is what makes a re-run with the same version resume
instead of duplicate: it picks up from the first step that did not complete. Never delete,
move, or force past an artifact to push a step through.

**a. Push `main`.** Check whether the release commit already landed:

```bash
git fetch origin main
git rev-parse origin/main
```

- Equal to `git rev-parse HEAD` → already pushed. Skip to (b).
- Not equal, and `git merge-base --is-ancestor origin/main HEAD` succeeds → `origin/main` is
  simply behind HEAD, the ordinary case. Push:

  ```bash
  git push origin main
  ```

- Not equal and that ancestry check fails → `origin/main` carries a commit HEAD does not;
  something was pushed since the step 2c pre-flight. **Stop and report**, naming both SHAs.
  Never force-push.

**b. Push the tag.** The tag is the bare `<VERSION>` literal — no `v` prefix, no suffix.
Check the remote by exact name:

```bash
git ls-remote --tags origin "refs/tags/<VERSION>"
```

- **No output** → the tag is not published. Create it on the release commit and push it:

  ```bash
  git tag <VERSION> HEAD
  git push origin "refs/tags/<VERSION>"
  ```

  The tag is lightweight, matching `0.9.8` and `0.9.9`. If a local tag of that name already
  exists (an earlier run created it, then failed before pushing), skip the `git tag` and push
  the existing one — but only once `git rev-parse <VERSION>` confirms it is HEAD; if it is
  not, stop and report.

- **Output whose SHA is `git rev-parse HEAD`** → already pushed. Skip to (c). (An annotated
  tag would also print a `refs/tags/<VERSION>^{}` line; that peeled line is the commit to
  compare.)
- **Output whose SHA is anything else** → the tag is published against a different commit.
  **Stop and report** both SHAs. Never move or delete a published tag, and never
  `git push --force` one.

**c. Create the GitHub release.** Check by exact tag name:

```bash
gh release view <VERSION> --repo uHappyLogic/cairn --json tagName,isDraft
```

- **Non-zero exit** (`release not found`) → not published. Write `<RELEASE_BODY>` to a
  temporary file so it survives verbatim, then create the release from it:

  ```bash
  gh release create <VERSION> --repo uHappyLogic/cairn \
    --title <VERSION> --verify-tag --notes-file <BODY_FILE>
  ```

  `--title` is the bare version, matching the published `0.9.8` and `0.9.9` releases;
  `--verify-tag` aborts if (b) did not land the tag. The release is neither a draft nor a
  prerelease — pass neither flag. Delete `<BODY_FILE>` afterwards.

- **JSON with `"tagName": "<VERSION>"` and `"isDraft": false`** → already published. Skip.
- **Any other existing release** — a draft, or one whose `tagName` differs → **stop and
  report** what was found. Never edit or delete a published release to make the run pass.

With (a), (b), and (c) each skipped or done, the release is live. Report its URL and stop:

```bash
gh release view <VERSION> --repo uHappyLogic/cairn --json url --jq .url
```
