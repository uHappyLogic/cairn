---
name: migrate-milestones
description: Upgrade a pointer-era project by re-finishing each milestone its README history records as a finish commit, then removing the README.
---

# migrate-milestones

Moves a project's record of finished milestones out of `milestones/README.md`, where the
retired pointer workflow kept it, and into git, in the form `/finish-milestone` now writes. It
walks the README's `## Milestone History` entries oldest first and, for each whose directory
still stands, makes exactly the commit the new finish would make, without finish's two checks,
since the history entry is the done fact: the milestone's directory removed, the subject
`Milestone-finish: <path>`, and as body the title from that directory's `requirements.md`
heading, a blank line, and the entry's bullets verbatim, the commit carrying the original
finish date as its author date. The plugin's milestones tool then reads every migrated
milestone as it reads a natively finished one: `milestones .` lists it with its finish date, and
`summary` and `record` print its entry back. One commit per milestone keeps the revert path:
reverting one migration commit restores that milestone's directory, and a later run migrates it
again. A closing commit then removes `milestones/README.md` and a live milestone's
`TASKS_DONE.md` when one is present, and rewrites the `## Milestone Workflow` section of `AGENTS.md` to the
path-addressed guidance.

It rewrites no existing commit, so the verified bars of tasks completed before completed tasks
moved into commits are not carried over: they stay in each finished milestone's
`TASKS_DONE.md`, which leaves the tree with its directory and stands at that finish commit's
parent, while those tasks' `Task-completion:` commits carry no bar. A live milestone stays where
it is, under its numbered name, and the principle store
`milestones/answer_decision_principles.md` is untouched.

It is upgrade scaffolding, run **once per project by a person**: it belongs to no chain, nothing
dispatches it, and it asks one confirmation before its first commit. Every commit it makes is a
call to the plugin's commit tool, each path-scoped to what it removes or rewrites, and it runs no
git write of its own. Every tool call it makes, those inside step 1's call included, is written
out in full as the fenced block shows it, never through a variable, alias, or function of your
own defined to stand for the command or any part of it.

## Usage

```
/migrate-milestones
```

No arguments. Run it from the workspace root of the project to upgrade.

## Workflow

### 1. Read the plan in one fixed shell call

Run this one fixed shell call from the workspace root, written out in full exactly as shown,
with only `<mode>` replaced by `plan`:

```
mode='<mode>'
tab="$(printf '\t')"
if [ ! -f milestones/README.md ]; then
  echo 'no readme'
elif [ "$(git rev-parse --is-shallow-repository)" = true ]; then
  echo 'shallow clone'
else
  awk '
    /^## / { history = ($0 == "## Milestone History"); next }
    history && index($0, "### Milestone ") == 1 {
      rest = substr($0, 15)
      cut = index(rest, " — ")
      if (cut > 1 && substr(rest, 1, cut - 1) ~ /^[0-9]+$/) entry[++count] = (substr(rest, 1, cut - 1) + 0) "\t" substr(rest, cut + length(" — "))
    }
    END { while (count > 0) print entry[count--] }
  ' milestones/README.md | while IFS="$tab" read -r number title; do
    dir="$(git ls-files -- milestones | awk -F / -v number="$number" 'NF > 2 { split($2, part, "_"); if (part[1] == "milestone" && part[2] ~ /^[0-9]+$/ && part[2] + 0 == number) { print "milestones/" $2 "/"; exit } }')"
    if [ -z "$dir" ]; then
      finished="$(git log --format=%s | awk -v number="$number" 'index($0, "Milestone-finish: milestones/milestone_") == 1 { name = substr($0, 19); if (split(name, part, "/") == 3 && part[3] == "" && split(part[2], word, "_") > 1 && word[2] ~ /^[0-9]+$/ && word[2] + 0 == number) { print name; exit } }')"
      if [ -n "$finished" ]; then
        printf 'migrated\t%s\t%s\t%s\n' "$number" "$finished" "$title"
      else
        printf 'absent\t%s\t%s\n' "$number" "$title"
      fi
    else
      id="${dir%/}"
      date="$(git log --format='%aI%x09%s' | awk -F '\t' -v id="Milestone-finish: ${id#milestones/}" -v path="Milestone-finish: $dir" '$2 == id || $2 == path { print $1; exit }')"
      if [ -z "$date" ]; then
        date="$(git log -1 --format=%aI -- "$dir")"
      fi
      if [ "$mode" = plan ]; then
        printf 'finish\t%s\t%s\t%s\t%s\n' "$number" "$dir" "$date" "$title"
      else
        heading="$(awk 'index($0, "# ") == 1 { line = substr($0, 3); gsub(/[ \t\r]+/, " ", line); sub(/^ /, "", line); sub(/ $/, "", line); sub(/^Milestone [0-9]+: /, "", line); print line; exit }' "${dir}requirements.md")"
        bullets="$(awk -v number="$number" '
          /^## / { history = ($0 == "## Milestone History"); entry = 0; next }
          history && index($0, "### ") == 1 {
            rest = substr($0, 15)
            cut = index(rest, " — ")
            entry = (index($0, "### Milestone ") == 1 && cut > 1 && substr(rest, 1, cut - 1) ~ /^[0-9]+$/ && substr(rest, 1, cut - 1) + 0 == number)
            next
          }
          entry && (seen || /[^ \t]/) { seen = 1; print }
        ' milestones/README.md)"
        if out="$(python3 ~/.gemini/config/plugins/cairn/tools/commit.py --subject "Milestone-finish: $dir" --body "${heading:-$title}

$bullets" --date "$date" --remove "$dir")" && [ -z "$out" ]; then
          printf 'finished\t%s\n' "$dir"
        else
          [ -z "$out" ] || printf '%s\n' "$out"
          printf 'stopped at\t%s\n' "$dir"
          break
        fi
      fi
    fi
  done
  if [ "$mode" = plan ]; then
    printf 'remove\t%s\n' milestones/README.md
    git ls-files -- milestones | awk -F / '
      FNR == NR {
        if (/^## /) history = ($0 == "## Milestone History")
        else if (history && index($0, "### Milestone ") == 1) {
          rest = substr($0, 15)
          cut = index(rest, " — ")
          if (cut > 1 && substr(rest, 1, cut - 1) ~ /^[0-9]+$/) done[substr(rest, 1, cut - 1) + 0] = 1
        }
        next
      }
      NF == 3 && $3 == "TASKS_DONE.md" { split($2, part, "_"); if (!(part[1] == "milestone" && part[2] ~ /^[0-9]+$/ && (part[2] + 0) in done)) print "remove\t" $0 }
    ' milestones/README.md -
  fi
fi
```

Run as `plan`, the call writes nothing. When `milestones/README.md` does not exist it prints
`no readme` alone, and when `git rev-parse --is-shallow-repository` prints `true` it prints
`shallow clone` alone: a shallow clone's truncated log could hold neither an original finish
commit nor the newest commit that changed a directory, so no date the plan printed could be
trusted.

Otherwise it reads the `### Milestone <N> — <Title>` entries under `## Milestone History` and
takes them **oldest first**, the reverse of the README's order, since every finish prepended its
entry, so the commits land in the order the milestones finished. For each entry it looks for the
directory under `milestones/` whose `milestone_<number>_<slug>` name carries the entry's number,
leading zeros ignored, among the directories the git index tracks a file under, and prints one
tab-separated line:

- **`finish`, the number, the directory, the date, and the title** — the directory stands, so the
  entry is migrated now, even when a migration of it was made and reverted before. The directory
  is printed as the milestone's path, trailing slash included. The date is the author date, in
  git's ISO form, of the newest commit whose subject is exactly `Milestone-finish:` followed by
  the directory's name (the original finish) or by its path (an earlier migration since
  reverted, which carried the same date), and, when no such commit exists, of the newest commit
  that changed the directory.
- **`migrated`, the number, the path, and the title** — the directory is gone and a
  `Milestone-finish:` subject in the log names a `milestones/milestone_<number>_<slug>/` path
  carrying the entry's number: the entry was migrated by an earlier run and is skipped.
- **`absent`, the number, and the title** — the directory is gone and no such subject exists.

The title on each line is the README entry's. Last come the closing commit's removals, one
`remove` line each: `milestones/README.md`, then every `TASKS_DONE.md` the index tracks directly
inside a directory under `milestones/` whose name carries no history entry's number — a live
milestone's.

`mode`, `tab`, and every value the loop sets (`number`, `title`, `dir`, `id`, `date`,
`finished`, and in step 3's run `heading`, `bullets`, and `out`) are each one quoted value per
call or per entry, set and used within this one call, never a tool command or a path list.

Read the print in this order, each case ending the run:

- **`no readme`** — the project has nothing to migrate. Print this one fixed no-op line and
  nothing else, having changed nothing:

  ```
  Nothing to migrate — the project has no milestones/README.md.
  ```

- **`shallow clone`** — stop without changing anything: print the fixed line
  `Migration stopped — the repository is a shallow clone.` first, then below it the remedy: run
  `git fetch --unshallow`, then re-run `/migrate-milestones`.
- **Any `absent` line** — stop without changing anything: print the fixed line
  `Migration stopped — some history entries have no directory.` first, then below it one line
  per `absent` line, its number and title as `<N> — <Title>`, and then the remedy: restore each
  directory from the history where it once stood, or edit its entry out of
  `milestones/README.md` by hand, then re-run `/migrate-milestones`. No absent entry is ever
  migrated.

### 2. Print the plan and ask once

Print the whole plan from step 1's lines, in their order: every `finish` line's directory, date,
and title, each the commit step 3 makes — the directory it removes and the author date it
carries; then, when there are any, the `migrated` lines' paths as already migrated and skipped;
then what the closing commit does — removes each path a `remove` line names, and rewrites the
`## Milestone Workflow` section of `AGENTS.md`. A plan with no `finish` line is still a
plan: its closing commit is the whole migration.

Then ask **once** whether to proceed. The answer accepts or rejects the plan whole: no entry is
edited out of it and nothing in it is re-ordered. An explicit acceptance runs steps 3 to 5 with
no further prompt. Anything else ends the run with no file changed and no commit made: print this
one fixed no-op line and nothing else:

```
Nothing migrated — the plan was declined.
```

### 3. Finish every entry in step 1's call

Run step 1's call again from the workspace root, written out in full exactly as shown there,
with `<mode>` replaced by `commit`. It walks the same entries in the same order and prints the
same `migrated` and `absent` lines, but for each directory that stands, in place of its
`finish` line, it makes that entry's finish commit and prints its outcome.

Each commit is the one command of the shared commit procedure at
`~/.gemini/config/plugins/cairn/shared/commit-procedure.md`, the plugin's commit tool, with the directory as
its one removal, `Milestone-finish: <path>` as its subject, `<path>` being the directory's path
with its trailing slash, and the date step 1 printed as `--date`, which sets the author date
only, the committer date staying the time the commit is made. Its body is the milestone's record in the
shape `/finish-milestone` writes: on the first line the title from the text of the first `# `
heading of the directory's `requirements.md`, whitespace folded and any legacy
`Milestone <N>: ` prefix stripped — the README entry's title only when that heading holds
nothing — then one blank line, then the entry's lines below its heading, verbatim, its outer
blank lines trimmed: its bullets. The tool runs the dirty-own-path guard, removes the
directory's tracked files with `git rm -r`, which refuses a file holding an uncommitted change,
and commits the removal with the directory as the commit's pathspec, so nothing else the index
holds rides in it.

What the call prints for each directory that stands:

- **`finished`, a tab, and the path** — its commit landed.
- **`stopped at`, a tab, and the path**, beside the commit tool's `Error:` line printed just
  before it (or the line the tool printed when it committed nothing) — no commit was made for
  it, and the call ended there: no later entry was touched. Every earlier entry's commit stands,
  so a re-run reads them as migrated and resumes at this one. Stop: print the fixed line
  `Migration stopped — a finish commit could not be made.` first, then below it the path paired
  with that line, quoted verbatim, and the remedy: resolve what the line names (a file holding an
  uncommitted change, for instance), then re-run `/migrate-milestones`. The closing commit is
  not made.

An `absent` line here, an entry whose directory left the tree after step 1 read it, stops the
run once the call ends, on step 1's absent-entry line, list, and remedy: every finish commit the
call made stands, and the closing commit is not made.

### 4. Rewrite the guidance section

Read `AGENTS.md` at the workspace root and rewrite its `## Milestone Workflow` section to
the path-addressed guidance, exactly as `~/.gemini/config/plugins/cairn/shared/workflow-guidance.md` states the
section, by whichever of that file's cases applies: a section present, the pointer-era one or
any other, is replaced whole, a file lacking the section has it appended, and a missing file is
created. Change nothing else in the file.

### 5. Make the closing commit

Read and follow the shared commit procedure at `~/.gemini/config/plugins/cairn/shared/commit-procedure.md`,
running its one commit-tool command yourself as this step's one git tool call. Supply it these
three inputs:

- **REMOVALS** — every path a `remove` line of step 1's print named, `milestones/README.md`
  first, each written out in full after its own `--remove`.
- **PATHS** — `AGENTS.md`, which step 4 rewrote.
- **SUBJECT** — `Workflow-migration: milestones`.

Supply no BODY: the commit is subject-only.

If the commit tool prints an `Error:` line, stop: print the fixed line
`Migration stopped — the closing commit could not be made.` first, then that `Error:` line
verbatim below it, and the remedy: resolve what it names, then re-run `/migrate-milestones`,
which reads every entry as migrated and plans the closing commit alone. Every finish commit of
step 3 stands.

### 6. Report

On the success path — the closing commit landed — print exactly one fixed terse status line and
nothing else:

```
Milestones migrated.
```

Do not list the migrated milestones, count them, name the commits, or add any next-step
pointer: the commits are the record.
