# Commit procedure (shared core)

This is the single source of truth for the skill-layer commit step: recording one pass's
own changes as a single path-scoped git commit. It is referenced (never restated) via
`${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` by every committing skill and every
committing orchestrator, exactly as the other `shared/` procedures are referenced by their
wrappers.

The wrappers add their own framing (where the paths and subject come from, how the outcome
is signalled, any follow-up). This file describes only the commit work itself — guard,
stage, commit — and says nothing about how callers resolve their inputs or wrap the result.

## Inputs

This procedure records one commit given two inputs the caller supplies, both already
resolved:

- **PATHS** — the explicit set of file paths this pass created or edited (its *own* paths).
  The caller decides this set **without content inspection** — it names the paths it
  touched (recording them as it edits, or knowing them structurally), never diffing the
  tree to discover what to include. This procedure stages exactly these paths and no
  others.
- **SUBJECT** — the resolved one-line commit subject for this pass (see *The subject
  convention* below for the shape the caller's subject must take).

Deciding the path set and deriving the subject are the caller's job; staging exactly those
paths, guarding the no-op case, and committing under that subject are this procedure's job.

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

## The subject convention

Every committing skill's SUBJECT follows the established `<Marker>: <descriptor>` house
shape — a distinctive marker prefix, a colon and space, then a short descriptor. The marker
is **derived systematically from that skill's distinctive function**, not drawn from an
ad-hoc per-skill list and with no grandfathered exceptions: the marker names what the pass
did, so the git log reads as self-describing provenance and every prefix is greppable.

Every such marker must stay clear of capture's `^Manual-answer:` grep **by construction** —
only genuinely user-deliberated manual answers carry a marker beginning `Manual-answer:`, so
capture harvests only those and skips every other committing skill's commits without any
change to its grep. The `-answer:` family is one instance of this shape; a skill deriving a
new marker picks one that names its function and does not collide with `^Manual-answer:`.

Deriving the actual marker for a given pass is the caller's job — it hands this procedure the
already-resolved SUBJECT.

## The layer rule

Committing is a property of the **skill layer**. This is the rule the wrappers follow when
deciding whether to run this procedure at all; this procedure itself just executes a commit
when it is called.

- **User-invoked skills that change files commit.** A file-changing skill ends its pass by
  running this procedure over its own path set.
- **Dispatched agents never commit.** An agent runs its work in isolation and hands its
  result (and, where relevant, the paths it touched) back to its caller; it never runs this
  procedure.
- **An orchestrator skill commits its agents' work after they return.** The orchestrator
  dispatches its agents, and once they return it runs this procedure over the resulting path
  set — at the orchestrator's own commit granularity (per dispatched unit or once at the end
  of the run, as that orchestrator decides).

## Rules

- Stage only the given PATHS, explicitly named — never `git add -A`, never a tree-wide or
  content-driven selection.
- The path set is decided by the caller without content inspection; the no-op guard's status
  check is scoped to the already-given paths, not a diff to choose them.
- On a no-op pass (no own path changed) stage nothing and commit nothing — no `--allow-empty`
  empty commit.
- The SUBJECT is `<Marker>: <descriptor>` with a function-derived marker that stays clear of
  `^Manual-answer:` by construction.
- This file holds only the commit logic. Resolving `<MILESTONE_DIR>`, parsing arguments,
  deriving the subject, signalling any return protocol, and following up are the wrappers'
  job — never restate them here.
