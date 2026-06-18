---
name: migrate-workspace
description: Manually upgrade an existing consuming workspace's milestones/ artifacts (every requirements.md plus milestones/README.md, history included) to Cairn's current conventions. Run it after updating the plugin to bring a project that adopted an earlier version in step with later structural changes. Idempotent — detects each retired pattern wherever it appears and rewrites in place, so a partially-migrated or already-current workspace is a no-op.
---

# migrate-workspace

Upgrades the **data artifacts of a consuming workspace** — the `milestones/` tree a
project generated while using Cairn — to the plugin's current conventions. When a
later version of Cairn changes the shape of those artifacts (a renamed heading, a
reworded structural blurb), this skill is the standing mechanism that brings an
already-adopted workspace in step.

It is the **inverse** of the plugin's own refactors: those rename the plugin's source
(skills, agents, shared procedures); a consumer holds no copies of that source, only
the generated `milestones/` tree. So the migration surface is exactly:

- every `requirements.md` under `milestones/` — **including historical and completed
  milestone directories**, not just the active one, and
- `milestones/README.md`.

Nothing else in a consuming workspace is a Cairn-owned artifact, so nothing else is
touched.

## Usage

```
/migrate-workspace
```

No arguments. Run it from the root of the consuming workspace (the directory that
contains `milestones/`). Each migration in the catalog below is applied by detection,
so running it on an up-to-date or partially-migrated workspace is safe — it changes
only what still carries a retired pattern.

## Migration catalog (the extension point)

This catalog is the skill's single source of registered migrations. **Each future
milestone that changes a workspace artifact appends one entry here**; the workflow
below applies whatever the catalog contains, so the procedure never changes — only
this list grows.

The **destination** of every migration is whatever the **live templates emit**, not a
string frozen into this file:

- `define-milestone-goal`'s `requirements.md` template — currently the headings
  `## Relevant starting state` and `## Decisions`.
- `init-milestone-base-workflow`'s `milestones/README.md` blurb — currently the line
  `- \`requirements.md\` — goal, relevant starting state, decisions, open questions`.

Treat those templates as the authority for the target state. If a template later
changes, update the matching catalog entry's "Rewrite to" so the destination tracks it;
the retired-pattern detection below is what each entry adds on top.

Each entry is line-anchored on purpose: it matches a **structural heading or blurb
line**, never an incidental prose mention of the same words. A milestone's Goal or
decision text that happens to say "implementation" is left untouched.

### Catalog fields

Every entry declares:

- **Targets** — which files it scans (a glob under `milestones/`).
- **Detect** — the retired line, anchored so only the structural line matches.
- **Rewrite to** — the current line, per the live template named above.

### Registered migrations

**M1 — Starting-state heading**
- Targets: every `milestones/**/requirements.md`.
- Detect: a line equal to `## Relevant implementation state`.
- Rewrite to: `## Relevant starting state`.

**M2 — Decisions heading**
- Targets: every `milestones/**/requirements.md`.
- Detect: a line equal to `## Implementation decisions`.
- Rewrite to: `## Decisions`.

**M3 — README structural blurb**
- Targets: `milestones/README.md`.
- Detect: within the `requirements.md` bullet of the "Each milestone … contains"
  blurb, the fragment `relevant implementation state, implementation decisions`.
- Rewrite to: `relevant starting state, decisions` (leaving the rest of the bullet —
  `goal, … , open questions` — intact).

## Workflow

### 1. Locate the workspace artifacts

Confirm a `milestones/` directory exists at the current root. If it does not, stop and
report that this does not look like a Cairn workspace (nothing to migrate).

Enumerate the migration targets:

- All `requirements.md` files under `milestones/` at any depth — use
  `find milestones -name requirements.md` (or `git grep`-friendly equivalents). This
  **must** include completed/historical milestone directories; do not filter to the
  current one.
- `milestones/README.md`, if present.

### 2. Apply every catalog migration by detection

For each registered migration, in catalog order, scan its Targets and rewrite each
**detected** line in place:

- Match the **Detect** pattern line-anchored — a whole structural heading line, or the
  specific README blurb fragment. Never do a free substring replace that could catch
  prose.
- Where detected, replace with **Rewrite to**.
- Where not detected (already migrated, or never present), do nothing for that file —
  this is what makes the skill idempotent without any version stamp.

Apply migrations against the live file contents so each runs on the result of the
previous one.

### 3. Report

Summarize, per migration:

- Which files were rewritten and how many lines changed.
- Which targets were already current (no change).

If nothing changed anywhere, say so explicitly — the workspace was already up to date
(or already migrated).

## Verifying a migration

After running, the workspace should satisfy:

- `git grep -i "implementation state"` and `git grep -i "implementation decisions"`
  under `milestones/` return **zero** hits (the retired structural phrases are gone).
- Each `requirements.md` heading matches the current `define-milestone-goal` template
  (`## Relevant starting state`, `## Decisions`), in historical/completed directories
  as well as the active one.
- The `milestones/README.md` blurb line reads
  `… goal, relevant starting state, decisions, open questions`.
- A second consecutive run reports no changes (idempotent).

## Adding a future migration

When a later milestone changes a workspace artifact:

1. Add one entry to **Registered migrations** with its `Targets`, `Detect`
   (line-anchored on the retired structural line), and `Rewrite to` (pointing at the
   live template that now defines the destination).
2. Do **not** touch the workflow — it already applies whatever the catalog holds.
3. Keep detection structural: migrate heading/blurb lines, never incidental prose that
   merely mentions the same words.

## Rules

- Operate **only** on the consuming workspace's `milestones/` artifacts —
  `requirements.md` files and `milestones/README.md`. Never edit plugin source.
- Migrate **all** milestone directories, completed history included — a consumer needs
  its whole history normalized.
- Detect, don't assume: rewrite a retired pattern only where it actually appears, so
  re-runs and partial states are no-ops.
- Keep edits line-anchored to structural headings/blurbs; never rewrite prose that
  incidentally contains a retired word.
- Do not commit — leave the migrated files staged for the user to review.
