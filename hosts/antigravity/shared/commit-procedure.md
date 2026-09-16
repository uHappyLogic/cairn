# Commit procedure (shared core)

This is the single source of truth for the skill-layer commit step: recording one pass's
own changes as a single path-scoped git commit, for every committing skill and orchestrator
that references it. The caller resolves the two inputs below and wraps the result; this file
describes only the commit work itself — guard, stage, commit.

## Inputs

This procedure records one commit given two inputs the caller supplies, both already
resolved:

- **PATHS** — the explicit set of file paths this pass created or edited (its *own* paths).
  The caller decides this set **without content inspection** — it names the paths it
  touched (recording them as it edits, or knowing them structurally), never diffing the
  tree to discover what to include. This procedure stages exactly these paths and no
  others.
- **SUBJECT** — the resolved one-line commit subject for this pass, in the house
  `<Marker>: <descriptor>` shape.

## Procedure

### 1. Dirty-own-path no-op guard

Before staging anything, check whether any of the PATHS actually changed in the working
tree (for example `git status --porcelain -- <PATHS>` — a status check scoped to the given
paths, which is *not* content inspection to decide the path set; the set is already given).

If none of the PATHS changed, this pass produced no real change: **stage nothing, commit
nothing, report the no-op, and return cleanly.** Do not create an empty commit — there is
no `--allow-empty` here; a pass that recorded nothing leaves git history untouched.

Only when at least one of the PATHS changed do you proceed to stage and commit.

### 2. Stage the own paths (path-scoped)

Stage exactly the PATHS and nothing else — `git add <PATHS>`, naming each path explicitly.

**Never `git add -A`** and never stage by any tree-wide or content-driven selection. Staging
is path-scoped by construction: the caller named the paths, so a dirty tree elsewhere cannot
contaminate this commit.

### 3. Commit under the resolved subject

Commit the staged paths under SUBJECT — `git commit -m "<SUBJECT>"` (plus any body lines the
caller supplies). Nothing outside the PATHS is committed.
