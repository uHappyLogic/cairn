---
name: release-plugin
description: Cut a cairn plugin release for a given MAJOR.MINOR.PATCH version, running every pre-flight and version gate before anything is changed or published.
---

# release-plugin

Releases the cairn plugin at a maintainer-supplied `MAJOR.MINOR.PATCH` version. This
`SKILL.md` is the single place the release procedure is documented — no release prose lives
in `CLAUDE.md` or `README.md`. It is a maintainer-only, project-local skill: it lives under
`.claude/skills/`, outside `core/`, so no host build renders it into a `hosts/<host>/` tree
and it never reaches a consuming project.

Every tag and release is a bare `MAJOR.MINOR.PATCH`, with no `v` prefix anywhere in the
history — the legacy `v.0.9.x` and `v0.9.7` tags were renamed to their bare form on
2026-09-07, and no `v`-prefixed tag remains on either side.

Nothing is written, committed, pushed, tagged, or published until every gate below has
passed and the release notes have been composed. The pre-flight and version gates (steps 2
and 3) are hard stops: on failure, report the specific reason and exit, having changed
nothing. Never work around a gate, and never ask the maintainer to waive one.

The release notes live in the repository: the `Release: <VERSION>` commit prepends them to
`CHANGELOG.md` as the entry `## <VERSION> — <YYYY-MM-DD>`, and from that commit on the
committed entry — extracted from `HEAD:CHANGELOG.md` by the rule step 7 states — is the one
source of the notes: step 7 shows it (and, while the commit is still unpushed, revises it in
place at the maintainer's request by amending that commit) and step 8 publishes it to the
monorepo release and every distribution release, so the changelog and the three release pages
carry identical text by construction.

**Resuming an interrupted release.** Re-running with the same version after a failed run is
the whole recovery story — there is no rollback of already-published refs and no hand-run
recovery command. A resumption is detected once, up front:

```bash
git log -1 --format='%s' HEAD
```

If that prints exactly `Release: <VERSION>`, this version's release commit is already
recorded and the run is a **resumption**. When it is, step 1 excludes `<VERSION>` from the
last-release lookup, step 3b tolerates a tag that points at HEAD, step 3c requires the
`CHANGELOG.md` entry it would otherwise forbid, and steps 5 and 6 are skipped whole — the
notes step 5 would compose and the commit step 6 would produce already exist, as the entry in
`HEAD:CHANGELOG.md`, and steps 7 and 8 read that entry exactly as they do on a fresh run.
Every other step runs unchanged, and step 8's per-artifact checks pick the run up from the
first step that did not complete.

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

Run all six checks. Each one blocks a route by which the release would tag something other
than a fresh build of committed `core/`, or publish into a place that does not exist, so any
failure stops the run. None of them writes anything.

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

**d. No untracked files under the host build's source paths.**

```bash
git ls-files --others --exclude-standard -- core/ scripts/hosts/
```

Any output means a source file the host build would read — a `core/` file, or a host
definition's settings or template under `scripts/hosts/<host>/` — is not committed, so the
trees it renders would not be reproducible from `main`. Stop and list the files. Untracked
files **elsewhere** in the repo are tolerated and are not checked: staging is path-scoped, so
they cannot be picked up.

**e. The committed host trees are a fresh build of `core/`.**

```bash
uv run scripts/build_hosts.py --check
```

This renders every host from `core/` through its `scripts/hosts/<host>/` definition into a
temporary directory at the current `VERSION`, runs the build's full validation set on the
render, and compares it byte-for-byte against the committed `hosts/<host>/` trees. It writes
nothing. A non-zero exit stops the run: report the script's output, which lists every
differing path (or every failing file and check, when validation rather than the comparison
failed). The remedy is the maintainer's, outside this skill — rebuild with
`uv run scripts/build_hosts.py`, commit that sync as its own standalone commit, never folded
into the release, and re-run `/release-plugin <VERSION>`. This gate is what lets step 6 change
only version slots: once the committed trees match a fresh build at the old version, the only
thing a rebuild at the new version can change is the version literal in each rendered manifest
and README.

**f. Every host's distribution repository exists.** List the host definitions — one
directory per host, in definition order:

```bash
ls -1 scripts/hosts/
```

Call each directory name `<host>`. Its distribution repository is `uHappyLogic/cairn-<host>`,
derived from the definition directory name by that fixed convention and nothing else — no
settings file names it. For every `<host>`, check that the repository exists:

```bash
gh repo view uHappyLogic/cairn-<host> --json nameWithOwner
```

A zero exit means it exists; move to the next host. A non-zero exit (`Could not resolve to a
Repository`) means it is missing. Once every host has been checked, if any is missing, stop
and print — for each missing host, with `<host>` filled in — exactly these two commands, in
this order, and **never run them**:

```bash
gh repo create uHappyLogic/cairn-<host> --public \
  --description "Distribution of the Cairn plugin for <host>, published verbatim by each release of uHappyLogic/cairn. Report issues there."
gh repo edit uHappyLogic/cairn-<host> \
  --add-topic cairn --add-topic <host> --add-topic plugin \
  --enable-issues=false --enable-wiki=false --enable-projects=false
```

The `create` is public, carries a description, and is deliberately empty — no `--license`,
`--add-readme`, or `--gitignore` — so the first publish into it becomes the repository's root
commit rather than a child of an initial README; the `LICENSE` file the published tree
carries is the license. The `edit` adds the topics and disables issues, wiki, and projects so
feedback routes to `uHappyLogic/cairn`. Provisioning a public repository is a deliberate,
irreversible act that belongs to the maintainer: this skill publishes into what already
exists and stops on anything else, so it prints the commands and exits with nothing changed.

### 3. Validate the version argument

All four refusals are hard and pre-mutation. A bad version caught here costs an error
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

**c. The changelog carries the version's entry exactly when the run is a resumption.** Count
the entry headings for `<VERSION>` in the committed changelog — the tracked tree is clean by
step 2a, so `HEAD:CHANGELOG.md` is the working file:

```bash
git show HEAD:CHANGELOG.md | awk -v v='<VERSION>' '$1 == "##" && $2 == v { n++ } END { print n + 0 }'
```

A heading counts when its first field is `##` and its second is exactly `<VERSION>` — the
`## <VERSION> — <YYYY-MM-DD>` form step 6c writes — so this is an exact-name count, and a
heading merely containing `<VERSION>` is not a match. The required count is one check that
flips on resumption:

- On a **fresh run** it must be `0`. A `1` or more means an entry for `<VERSION>` was already
  committed without this run's `Release: <VERSION>` commit being at HEAD — a stale unpublished
  Release commit buried below HEAD, or a hand-written entry — and a run that continued would
  prepend a duplicate in a commit that then succeeds. Stop and report the count, naming the
  commit the heading last changed in (`git log -1 --format='%h %s' -S'## <VERSION> — ' -- CHANGELOG.md`).
- On a **resumption** it must be exactly `1`: the entry the `Release: <VERSION>` commit at HEAD
  prepended, which steps 7 and 8 read back. A `0` means the commit at HEAD carries no entry
  (it was made by hand, or before the changelog existed), and `2` or more means a duplicate;
  either stops the run, reporting the count.

If `git show` itself fails, `CHANGELOG.md` is not a tracked file at HEAD: stop and report it —
the release prepends to that file and never creates it.

**d. The version is strictly greater than the last release.** Compare as a **numeric
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
the release body in context. Call the finished text `<RELEASE_BODY>`; step 6 writes it into
`CHANGELOG.md` as the `<VERSION>` entry and commits it, and from that commit on the committed
entry — not this draft — is what steps 7 and 8 show and publish.

**Skip this whole step on a resumption.** The notes it would compose are already committed:
the `Release: <VERSION>` commit at HEAD carries them as the `CHANGELOG.md` entry step 3c
counted, and step 7 reads that entry back. Recomposing would produce a second condensed
rewrite that could hand a distribution release notes differing from a monorepo release an
earlier run already created; reading the entry back cannot. The cross-check in (c) and the
empty-range confirmation in (d) are therefore not re-run on a resumption — the committed
entry is the evidence they passed. Carry `<VERSION>` and `<LAST_TAG>` straight into step 7.

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
   `### Changes since <LAST_TAG>` section — at `###`, like every section in (e), and a short
   bulleted summary of the user-facing changes under the same rewrite discipline as (e)
   below — then the Full Changelog link from (f).
3. Show the maintainer that full body and ask whether to release with it.
4. Proceed only on an **explicit** affirmative answer. Anything else — a refusal, a question,
   an ambiguous reply — stops the run with nothing changed.

An empty range is the only path that reaches the rest of the release without history-entry
sections, and it never takes itself silently.

**e. Compose one section per finished milestone.** Otherwise, for each milestone on the
(agreed) list, **highest number first**, read its `### Milestone <N> — <Title>` entry in
`milestones/README.md` and rewrite it into:

```markdown
### <Title> (milestone <N>)

- <condensed user-facing change>
- <condensed user-facing change>
```

`<Title>` is the heading's title text; `<N>` is the milestone number as the heading writes it.

Every section heading in the body is `###` — one level below the `## <VERSION> — <YYYY-MM-DD>`
heading step 6c puts over the body in `CHANGELOG.md`, so the sections nest under their
release. The body must contain **no line beginning `## `**: the next such line is what ends
the entry under step 7's extraction rule, so a `##` inside the body would cut the published
notes short.

The bullets are **condensed rewrites, never verbatim copies**. Keep what a consumer of the
plugin would notice — what the release now does, what changed for them, what was added,
renamed, or retired. Cut milestone-internal process detail: task counts, per-task ledgers,
audit passes, re-audit verdicts, which sweep touched which file, and how the work was
verified. Where several history bullets describe one user-facing change, merge them into one.
This is the shape every sectioned release page from `0.9.8` on and its `CHANGELOG.md` entry
already carry, and matching it keeps the release series consistent.

**f. Close with the compare link.** The last line of `<RELEASE_BODY>` is always:

```markdown
**Full Changelog**: https://github.com/uHappyLogic/cairn/compare/<LAST_TAG>...<VERSION>
```

`<LAST_TAG>` is used literally, whatever its format; `<VERSION>` is the tag this run creates.

### 6. Apply the version, rebuild the host trees, and record the release commit

Everything so far has been read-only. This step is where the run first writes, and it
produces **exactly one commit** — the complete, self-consistent state the tag will point at.
Run it unattended: nothing here pauses for the maintainer.

**Skip this whole step on a resumption.** The `Release: <VERSION>` commit at HEAD is the
commit this step produces: the version script and the rebuild would rewrite the same
values, the changelog already carries the entry step 3c counted, and the commit would find
nothing staged. Carry `<VERSION>` and `<LAST_TAG>` straight into step 7, which reads the
notes from that commit.

**a. Write the version into its source of truth and every mirrored surface.**

```bash
uv run scripts/set_version.py <VERSION>
```

The script takes the bare literal and writes it into the four surfaces it owns — `VERSION`,
the single source of truth, and the three mirrors kept in lockstep with it,
`.claude-plugin/marketplace.json`, `pyproject.toml`, and `uv.lock` — leaving every file
untouched if any one of them fails. A non-zero exit stops the release; report what the script
printed. The script never touches git, `gh`, or anything under `hosts/`: every host manifest
is rendered from `VERSION` by the build in (b), never written here.

**b. Rebuild the host trees.**

```bash
uv run scripts/build_hosts.py
```

This renders every host from `core/` through its `scripts/hosts/<host>/` definition into
`hosts/<host>/`, filling each manifest and README template's version slot from the `VERSION`
just written, and swaps the trees in only after every host passes the build's validation set.
Order matters: the rebuild must follow (a), or the rendered trees carry the previous version.
A non-zero exit stops the release; report what the script printed — nothing under `hosts/`
was written.

Because step 2e proved the committed trees already matched a fresh build of `core/` at the
previous version, this rebuild can change only the version literal in each rendered manifest
and README: the Release commit changes version slots and the `CHANGELOG.md` entry (c) adds,
and nothing else, by construction. There is no drift to inspect, report, or absorb here —
anything the rebuild changed beyond the version slots would have stopped the run in
pre-flight.

**c. Prepend the changelog entry, then stage exactly the written paths.** The entry is the
`## <VERSION> — <YYYY-MM-DD>` heading over `<RELEASE_BODY>` verbatim, and it goes below the
changelog's title, above every earlier release:

```markdown
## <VERSION> — <YYYY-MM-DD>

<RELEASE_BODY>

```

The date is today's UTC calendar date, `date -u +%Y-%m-%d` — the clock the backfilled
headings took from each release's `publishedAt` — and the separator is an em dash (`—`,
U+2014) with one space on each side, as every existing heading has it. Insert those lines —
the heading, one blank line, the body's lines exactly as composed, one blank line — immediately
**above the first line of `CHANGELOG.md` that begins `## `**, which is `<LAST_TAG>`'s heading.
That slot sits below the `# Changelog` title and its one-line verbatim note, which are never
touched, and it is the file's only write: no Unreleased section is filled, no reference-link
list is updated, and no earlier entry is edited.

Then confirm the write with `git diff --numstat -- CHANGELOG.md` and `grep -n '^## ' CHANGELOG.md`:
the diff shows added lines only (`0` deletions), and the first two `## ` lines are the new
heading and then `<LAST_TAG>`'s. Anything else — a deletion, the entry landing anywhere but
first, a second `<VERSION>` heading — means the prepend went wrong: stop and report, with
nothing committed.

Now stage the written paths. Name them explicitly — the four surfaces the version script
writes, the changelog, and the rebuilt trees:

```bash
git add -- \
  VERSION \
  pyproject.toml \
  uv.lock \
  .claude-plugin/marketplace.json \
  CHANGELOG.md \
  hosts/
```

**Never `git add -A`** and never `git add .`. A path-scoped `git add` records additions,
modifications, and removals under those paths, so a rebuild that drops a rendered file is
staged too. Nothing else in the repo may enter the release commit.

**d. Commit once.** The subject is exactly:

```
Release: <VERSION>
```

with `<VERSION>` the bare literal, and the body following the repository's commit conventions.
One release is one commit — never split the version bump and the rebuild, and never amend a
later step into it. The run's **only amend** is step 7's revision of the notes: a
`git commit --amend --no-edit` over `git add -- CHANGELOG.md` alone, made only while this
commit is still unpushed, which changes the changelog entry and leaves this subject untouched.

Then confirm the staging was complete: `git status --porcelain --untracked-files=no` must be
empty. Any tracked change left behind means a written path was missed; stop and report it
rather than tagging a partial state. The tag is not created here — the run holds `<VERSION>`
and `<LAST_TAG>` and carries them into the publish step, and the notes now live in the commit
as the `CHANGELOG.md` entry step 7 reads back; `<RELEASE_BODY>` is not carried past this
point.

### 7. Confirm before publishing

This is the run's **single pause**. Everything before it is local work a `git reset` undoes;
everything after it is public and permanent. The pause asks one question; a revision of the
notes answers it by amending the still-unpushed release commit and asking again, so the run
leaves this step only by publishing or by stopping.

**Extract the entry.** The release notes are the `<VERSION>` entry of the committed changelog,
read from `HEAD:CHANGELOG.md` — never from context, and the same way on a fresh run and a
resumption. The entry is **the lines under the `## <VERSION> — <YYYY-MM-DD>` heading, up to
the next `##` heading, blank lines trimmed**: every line after the heading line and before the
next line beginning `## ` (or the end of the file where the entry is the last), with the blank
lines at the start and end of that range dropped and the blank lines inside it kept. Extract it
with exactly this command, whose heading match is the same exact second-field test as step 3c:

```bash
git show HEAD:CHANGELOG.md | awk -v v='<VERSION>' '
  /^## / { if (found) exit; found = ($2 == v); next }
  found  { lines[++n] = $0 }
  END {
    s = 1; e = n
    while (s <= e && lines[s] == "") s++
    while (e >= s && lines[e] == "") e--
    for (i = s; i <= e; i++) print lines[i]
  }'
```

Call what it prints `<ENTRY>`. It is exactly the body between the heading's blank line and the
blank line before `<LAST_TAG>`'s heading. On a fresh run's **first** extraction it is
`<RELEASE_BODY>` as step 6c wrote it, now read back from the commit rather than from context;
if the two differ, the 6c write went wrong — stop and report it, the commit still being local.
(After a revision below, `<ENTRY>` is the revised entry and `<RELEASE_BODY>` is no longer its
reference.) An empty `<ENTRY>` (the heading absent, or nothing under it) is likewise a stop:
step 3c counted exactly one such heading, so this cannot happen without the changelog having
changed since.

Show the maintainer both facts they need in order to veto or revise:

1. `<VERSION>` — the version about to be tagged and released.
2. `<ENTRY>` — the **full** committed entry, verbatim, exactly as step 8c will publish it.
   Never a summary, an excerpt, or a description of it.

Then ask whether to publish. The answer takes one of three forms:

- **Publish** — an **explicit** affirmative. Proceed to step 8.
- **Revise** — a stated change to the entry's text, or word that the maintainer has already
  edited the entry by hand in the working `CHANGELOG.md`. Take the revision path below; it
  ends by showing the entry again and asking again.
- **Anything else** — a refusal, a question, an ambiguous reply — stops the run here with
  nothing pushed. Say that the release commit stays at HEAD — unpushed and revertible, unless
  an earlier run already pushed it — and that re-running `/release-plugin <VERSION>` resumes
  from this point.

**Revise the entry.** The notes are the skill's own output, written into a commit the run
made, so a revision at the run's own review point is applied here rather than handed back to
the maintainer as a stop. It is the run's **only amend** (6d), and it is allowed only while the
release commit is still unpushed — check that first, before touching anything:

```bash
git fetch origin main
git merge-base --is-ancestor HEAD origin/main
```

A **non-zero** exit means `origin/main` does not carry HEAD: the commit is unpushed and may be
amended — continue. A **zero** exit means `origin/main` already carries the release commit — a
resumption past step 8a — so its notes are frozen: a pushed commit is never amended. **Stop and
report** that reason, with nothing changed, and say that re-running `/release-plugin <VERSION>`
resumes from this point with the notes as committed.

Then apply the revision to the `<VERSION>` entry — and only that entry — in the working
`CHANGELOG.md`: edit the entry's lines to carry the maintainer's stated change, keeping every
section at `###` and adding no line that begins `## ` (5e's rule — the next such line ends the
entry). An edit the maintainer already made by hand in the working file counts the same: take
the file as it stands and apply nothing. Either way, confirm the change stayed inside the entry
— everything outside it, the `## ` heading lines included, must still match HEAD:

```bash
diff <(git show HEAD:CHANGELOG.md | awk -v v='<VERSION>' '/^## / { skip = ($2 == v); print; next } !skip') \
     <(awk -v v='<VERSION>' '/^## / { skip = ($2 == v); print; next } !skip' CHANGELOG.md)
```

Any output means the revision reached outside the entry — another release's entry, the title
or its note, or the `<VERSION>` heading itself — or added a `## ` line inside it: stop and
report it, leaving the working change in place and the commit untouched. If instead the file is
unchanged from HEAD (`git diff --quiet HEAD -- CHANGELOG.md` exits 0), there is nothing to
amend: say so, then show the entry and ask again.

Then stage that one path and amend, keeping the message:

```bash
git add -- CHANGELOG.md
git commit --amend --no-edit
```

`git add -- CHANGELOG.md` is the amend's whole staging — never `git add -A`, and no other path,
so the amended commit still changes only version slots and the changelog entry. `--no-edit`
keeps the message as 6d wrote it, so the `Release: <VERSION>` subject a resumption keys on is
untouched; confirm that `git log -1 --format='%s' HEAD` still prints exactly `Release: <VERSION>`.

Now go back to **Extract the entry**: re-extract `<ENTRY>` from `HEAD:CHANGELOG.md` with the
same command, show `<VERSION>` and the full revised entry again, and ask again. Step 8 publishes
whatever HEAD records when the maintainer finally answers publish.

Step 5d's empty-range question is a different one — whether commit-derived notes are an
acceptable substitute, asked before anything is written — so an empty-range run answers both.
This gate is the only pause between the release commit and publication, and it is never
skipped.

### 8. Publish: push `main`, push the tag, create the GitHub release, publish the distribution repositories

Four steps in this order: the branch must carry the commit before a tag can name it, the tag
must exist on the remote before a release can attach to it, and the distribution publish runs
last because every distribution commit names the pushed source commit and the monorepo release
URL — nothing is created before what it names exists.

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

**c. Create the GitHub release.** First write `<ENTRY>` to a temporary file — call it
`<BODY_FILE>` — by running step 7's extraction again with its output redirected into the
file (`git show HEAD:CHANGELOG.md | awk … > <BODY_FILE>`), so the file is the committed entry
byte for byte rather than a transcription from context. Write it before the check below, not
inside the create branch: (c) and every host in (d) publish from this one file, so it must
exist even on a resumption that skips (c), and it is deleted only once step 8 is complete.
Then check by exact tag name:

```bash
gh release view <VERSION> --repo uHappyLogic/cairn --json tagName,isDraft
```

- **Non-zero exit** (`release not found`) → not published. Create the release from the file:

  ```bash
  gh release create <VERSION> --repo uHappyLogic/cairn \
    --title <VERSION> --verify-tag --notes-file <BODY_FILE>
  ```

  `--title` is the bare version, matching the published `0.9.8` and `0.9.9` releases;
  `--verify-tag` aborts if (b) did not land the tag. The release is neither a draft nor a
  prerelease — pass neither flag.

- **JSON with `"tagName": "<VERSION>"` and `"isDraft": false`** → already published. Skip.
- **Any other existing release** — a draft, or one whose `tagName` differs → **stop and
  report** what was found. Never edit or delete a published release to make the run pass.

**d. Publish each host's distribution repository.** Runs only once (a), (b), and (c) are each
skipped or done. List the host definitions in definition order, as step 2f did:

```bash
ls -1 scripts/hosts/
```

For each `<host>` in that order, the distribution repository is `uHappyLogic/cairn-<host>` and
its remote is `git@github.com:uHappyLogic/cairn-<host>.git` — the same SSH scheme as `origin`
— both derived from the directory name by that fixed convention and nothing else. Call that
URL `<REMOTE>`; every git command below names it directly, so no remote is added to the
monorepo's configuration. Each host is two check-then-do sub-steps in turn, its tag and then
its release, and the run moves to the next host only when both are skipped or done.

The tree to publish is the one the Release commit already stores for that host:

```bash
git rev-parse HEAD:hosts/<host>
```

Call it `<TREE>`, and call `git rev-parse HEAD` `<SHA>`. Publishing is plumbing over that
tree object — nothing is checked out or written on disk — so byte-identity between
`hosts/<host>/` at the Release commit and what the distribution repository carries is a
property of the object model, and step 2e's drift gate makes that tree a fresh build of
`core/`.

**i. The distribution tag.** Check the remote by exact name:

```bash
git ls-remote --tags <REMOTE> "refs/tags/<VERSION>"
```

- **No output** → this host is unpublished. Decide the parent first:

  ```bash
  git ls-remote --heads <REMOTE> refs/heads/main
  ```

  No output means the repository is still the empty one step 2f's creation command
  provides, so the commit has **no parent** — the first publish is a parentless root commit,
  and the push below makes `main` the default branch. Output means distribution `main`
  exists: fetch it into `FETCH_HEAD`, and only there —

  ```bash
  git fetch --no-tags <REMOTE> main
  ```

  — no remote-tracking ref is written, and `--no-tags` keeps the distribution tags, which
  share their names with the monorepo's own tags, out of the local tag namespace. A failing
  fetch is a stop, never a root commit: only the empty `--heads` query decides that.

  Then make the commit from `<TREE>` with `FETCH_HEAD` as its sole parent — drop
  `-p FETCH_HEAD` on a root commit — under subject `Release: <VERSION>` and a fixed
  provenance body:

  ```bash
  printf 'Release: <VERSION>\n\nSource: uHappyLogic/cairn@<SHA>\nPath: hosts/<host>/\nNotes: https://github.com/uHappyLogic/cairn/releases/tag/<VERSION>\n' \
    | git commit-tree <TREE> -p FETCH_HEAD -F -
  ```

  That message is the subject, a blank line, and exactly these three body lines, composed
  from values the run already holds — the source commit, the published path, and the
  monorepo release URL derived from `<VERSION>`:

  ```
  Source: uHappyLogic/cairn@<SHA>
  Path: hosts/<host>/
  Notes: https://github.com/uHappyLogic/cairn/releases/tag/<VERSION>
  ```

  It never carries the release notes; those live in the monorepo's `CHANGELOG.md` entry and
  on the GitHub releases. Call the commit id it prints `<COMMIT>` and land it with **one
  atomic push** to the branch and the tag:

  ```bash
  git push --atomic <REMOTE> "<COMMIT>:refs/heads/main" "<COMMIT>:refs/tags/<VERSION>"
  ```

  Atomic means both refs update or neither does, so a distribution tag exists exactly when
  distribution `main` carries the same commit and no half-published host can arise between
  re-runs. A rejected push — `non-fast-forward`, because `main` moved between the fetch and
  the push — lands nothing: **stop and report** it, and a re-run resumes from the fresh
  state.

- **Output** → the tag is published. Fetch its commit and compare trees:

  ```bash
  git fetch --no-tags <REMOTE> "refs/tags/<VERSION>"
  git rev-parse "FETCH_HEAD^{tree}"
  ```

  - Equal to `<TREE>` → already published, and — because step 2e proved `hosts/<host>/` a
    fresh build of `core/` — published correctly. Skip to (ii).
  - Anything else → the distribution tag names a different tree. **Stop and report** all
    three ids: the tag's tree, `<TREE>`, and the tag's commit SHA (the first column of the
    `ls-remote` line; an annotated tag would also print a `refs/tags/<VERSION>^{}` line,
    whose peeled SHA is the commit). Never move, delete, or force-push a published
    distribution tag — the same stop the monorepo tag gets in (b).

**ii. The distribution GitHub release.** Check by exact tag name on this host's repository:

```bash
gh release view <VERSION> --repo uHappyLogic/cairn-<host> --json tagName,isDraft
```

- **Non-zero exit** (`release not found`) → not published. Create it from the same
  `<BODY_FILE>` (c) wrote — the entry extracted from `HEAD:CHANGELOG.md` — so the changelog
  and the release pages carry identical notes by construction:

  ```bash
  gh release create <VERSION> --repo uHappyLogic/cairn-<host> \
    --title <VERSION> --verify-tag --notes-file <BODY_FILE>
  ```

  `--verify-tag` aborts if (i) did not land the tag; neither `--draft` nor `--prerelease`,
  as in (c). The notes are composed for the monorepo — their compare link points at
  `uHappyLogic/cairn` — and that is accepted; never edit them per host.

- **JSON with `"tagName": "<VERSION>"` and `"isDraft": false`** → already published. Skip.
- **Any other existing release** — a draft, or one whose `tagName` differs → **stop and
  report** what was found, exactly as in (c).

With (a) through (d) each skipped or done, the release is live everywhere. Delete
`<BODY_FILE>`, then report the release URLs — the monorepo's and one per host — and stop:

```bash
gh release view <VERSION> --repo uHappyLogic/cairn --json url --jq .url
gh release view <VERSION> --repo uHappyLogic/cairn-<host> --json url --jq .url
```
