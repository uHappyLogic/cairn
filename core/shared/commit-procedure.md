# Commit procedure (shared core)

This is the single source of truth for the skill-layer commit step: recording one pass's
own changes as a single path-scoped git commit, for every committing skill that references
it. The caller resolves the inputs below and wraps the result; this file describes only the
commit work itself, which is one call to the plugin's commit tool.

## Inputs

This procedure records one commit given four inputs the caller supplies, the last two
optional, every one already resolved:

- **PATHS** — the explicit set of file paths this pass created or edited (its *own* paths).
  The caller decides this set **without content inspection** — it names the paths it
  touched (recording them as it edits, or knowing them structurally), never diffing the
  tree to discover what to include. The commit records exactly these paths, and the
  REMOVALS below, and no others. PATHS may be empty only when REMOVALS names a path.
- **SUBJECT** — the resolved one-line commit subject for this pass, in the house
  `<Marker>: <descriptor>` shape.
- **BODY** (optional) — zero or more body lines for this pass's commit, supplied by the
  caller already resolved as the text it wants recorded under SUBJECT. What a body holds,
  and whether a pass carries one at all, is the caller's decision and never this
  procedure's: it forwards the lines it is given to git and composes, prompts for, and
  inspects nothing. A caller that supplies no BODY gets a subject-only commit.
- **REMOVALS** (optional) — the paths this pass removes from the project, each a file or a
  directory removed whole, named exactly as the caller resolved it. The commit removes each
  and records its removal beside PATHS. A caller that supplies no REMOVALS removes nothing.

## Procedure

Run this one command as the step's one git tool call, with SUBJECT and BODY as given,
every path of REMOVALS written out in full after its own `--remove`, and every path of PATHS
written out on the command line after `--` as its own argument, none held in a shell
variable:

```
python3 {{PLUGIN_ROOT}}/tools/commit.py --subject "<SUBJECT>" --body "<BODY>" --remove <REMOVAL> -- <PATHS>
```

When the caller supplies no BODY, leave out `--body "<BODY>"`, and the commit is
subject-only. Write one `--remove <REMOVAL>` for each path of REMOVALS, and none when the
caller supplies no REMOVALS; when PATHS is empty, leave out `-- <PATHS>`. The tool runs the
dirty-own-path guard over PATHS and REMOVALS, removes each path of REMOVALS from the index
and the working tree with `git rm -r` (which refuses a file holding an uncommitted change, so
no uncommitted work is discarded), stages exactly PATHS, and commits them with PATHS and
REMOVALS as the commit's pathspec, so nothing outside them is committed whatever else the
index holds, repeating a git write another process's lock refused before passing git's
message on. Run no git command of your own beside it: no status check, no `git add` (never
`git add -A`), no `git rm` or other removal, no `git commit`, and no `--allow-empty`.

Read the outcome from what the tool prints:

- **Nothing** — the commit landed.
- **Exactly the line `Nothing committed — none of the paths changed.`** on stdout — none of
  PATHS or REMOVALS changed, so nothing was removed, staged, or committed and git history is
  untouched. This line is the no-op the caller reports: it chooses its own no-op line on
  reading it.
- **One `Error: <reason>` line** on stderr — nothing was committed, and the line, which
  carries git's own message when a git command failed, is passed on to the caller as the
  step's failure.
