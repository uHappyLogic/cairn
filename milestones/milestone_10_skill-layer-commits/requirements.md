# Milestone 10: Skill-Layer Commits

## Goal

Make committing a property of the skill layer: every user-invoked skill that changes files ends by committing exactly those changes — path-scoped (never `git add -A`, no content inspection), under its own distinct subject prefix that stays clear of capture's `^Manual-answer:` grep — while dispatched agents never commit and an orchestrator skill commits its agents' work after they return. This replaces the old committing-vs-staging role split, turning `complete-task`, `submit-task`, `derive-tasks`, `recommend-all-open-questions`, `modify-milestone-goal`, `define-/specify-/review-/goto-/finish-milestone`, and `capture-milestone-principle-updates` into committers, moving the `answer-all-open-questions-with-recommendation` commit from its agent up to the orchestrator (per answer), with only the setup/maintenance skills `init-milestone-base-workflow` and `migrate-workspace` exempt. Commit granularity: `complete-all-tasks` commits per task (unchanged), `answer-all-open-questions-with-recommendation` commits per answer (preserving one-commit-=-one-answer), `recommend-all-open-questions` and `derive-tasks` commit once at the end.

## Relevant starting state

### Skills that already commit (today's documented exceptions)

Four paths commit today; each stages **path-scoped** and commits under a greppable subject, **except** `complete-all-tasks` which uses `git add -A`:

- `answer-open-question` (skill) — `git add <MILESTONE_DIR>/requirements.md` → `git commit -m "Manual-answer: <Short Title>" -m "<rationale>"`. Rationale in the body; this is the commit `capture-milestone-principle-updates` later walks.
- `answer-open-question-with-recommendation` (**skill and agent**) — path-scoped, subject `Recommendation-answer: <Short Title>`, body = lifted recommendation. Currently **both** the inline skill and the file-editing agent commit.
- `answer-open-question-with-alternative` (skill) — path-scoped, subject `Alternative-answer: <Short Title>`, body = chosen alternative text.
- `complete-all-tasks` (orchestrator) — commits **per task** after each `complete-task` agent returns, via `git add -A` then `git commit -m "<task heading>"`. This is the **only committer not path-scoped**, and its subject is the bare task heading (no prefix).

### Orchestrator ↔ agent commit boundary today

The boundary is currently split two ways across the two committing orchestrators:

- `complete-all-tasks`: the **orchestrator commits**, the `complete-task` agent does not.
- `answer-all-open-questions-with-recommendation`: the **agent commits** (path-scoped `Recommendation-answer:` per answer, preserving one-commit-=-one-answer), and the orchestrator "never edits `requirements.md` and never commits — it purely dispatches and sequences." This is the milestone-7 inversion the goal reverses (move the commit up to the orchestrator).

### Skills that mutate files but do not commit (the gap this milestone closes)

- **Explicit "do not commit — leave staged":** `define-milestone-goal`, `specify-milestone-starting-state`, `modify-milestone-goal` (documented as "does not commit"), `goto-next-milestone`, `finish-current-milestone` ("never commits"), `complete-task` (skill — "committing belongs to the orchestrator"), `capture-milestone-principle-updates` ("like every individual skill here, leaves its edit staged").
- **Silent — no git/commit/staging mention at all:** `review-milestone-requirements`, `submit-task` (skill), `derive-tasks`. These just edit and hand back a dirty tree.
- **Stage-only by deliberate design:** `recommend-all-open-questions` — stages path-scoped (`git add <MILESTONE_DIR>/requirements.md`, never `-A`), **requires no clean working tree**, and documents that its embedded-recommendation scaffolding is *transient* and should **not** become a durable commit (the goal overrides this: it now commits once at the end).

### Commit-subject convention and capture's grep

Subjects are the provenance markers. `capture-milestone-principle-updates` harvests **only** `Manual-answer:` via `git log --grep='^Manual-answer: '`; `Recommendation-answer:` and `Alternative-answer:` are deliberately shaped to **not** match that anchor so capture skips them. Any new per-skill subject prefix this milestone introduces must likewise stay clear of `^Manual-answer:`.

### The invariant being retired

`CLAUDE.md` documents a committing-vs-staging rule keyed on **what a skill produces**: "a decision-recorder commits its decision atomically under a greppable subject, while a work-producer (`complete-task`/`submit-task`) leaves changes staged," with "one orchestrator commits, three individual skills are the deliberate exception, one file-editing agent commits; every other individual skill never commits." The goal replaces this role-based split with a **layer-based** rule (skills commit, agents never commit), so this invariant and its per-skill "Do not commit" rules, the milestone-7 agent-commits divergence, and the recommend-sweep "mutate-but-do-not-commit" note all get rewritten.

### Skills exempt from the change

`init-milestone-base-workflow` and `migrate-workspace` (both currently "leave staged for the user") stay non-committing — they run in a consuming project that may not be a git repo or wants its own commit boundaries. Skills that change no files (`discuss-milestone-goal`, `discuss-open-question`, `discuss-new-task`, `ask-in-milestone-context`) are irrelevant to the change.

### Structural conventions this milestone touches

Every skill/agent that commits or stages does so after resolving `<MILESTONE_DIR>` via `shared/get-current-milestone.md`. Skill↔agent pairs (`complete-task`, `submit-task`, `answer-open-question-with-recommendation`) share one execution-neutral procedure under `shared/`, run inline by the skill and in isolation by the agent — those shared procedures are currently execution-neutral and must not mention committing, so commit logic lives in the wrappers. `README.md` and `CLAUDE.md` both carry the committing-vs-staging prose that will need re-syncing.

## Decisions

### Commit subject prefixes

Every committing skill's subject prefix is derived systematically from its distinctive function, expressed in the established `<Marker>: <descriptor>` house shape (the `-answer:` family being one instance) — no ad-hoc per-skill list and no grandfathered exception. `complete-all-tasks` comes under the same convention: it drops its bare task-heading subject in favour of a function-derived prefix, with the task heading moving into the commit body. This keeps committing a uniform skill-layer property with no role-based carve-outs, makes every prefix greppable and self-describing, and clears capture's `^Manual-answer:` grep by construction.

### Completion commit path scope

`complete-task` and `complete-all-tasks` stage the exact set of paths the completer created or edited while carrying out the task — recorded as each edit is made — together with the two milestone task-list files, then commit that explicit path set (never `git add -A`). This commits the task's real change set atomically while honoring both rules: naming paths is path-scoped, and recording paths as they are edited is not content inspection (no diffing to decide what to include). Under `complete-all-tasks` the agent stages its own paths (or returns them) so the orchestrator's per-task commit stays path-scoped.

### Finish commit file set

`finish-current-milestone` records its whole finish as a single path-scoped commit: it always stages `milestones/README.md` (completion summary plus the current-milestone pointer cleared to `none`) and additionally stages `CLAUDE.md` only on the passes where the lasting-change step actually edited it, then commits that explicit path set under one finish subject. The pointer-clear rides inside the same README edit, so the committed README already carries `Current milestone: none` and `goto-next-milestone`'s none-pointer precondition is recorded in git rather than left in a dirty tree. Conditional `CLAUDE.md` staging keeps the commit path-scoped with no content inspection.

### No-op pass commit

A committing skill that finishes a pass having changed no file (e.g. `review-milestone-requirements` when a pass finds nothing to reconcile or surface, `capture-milestone-principle-updates` when it distills no new principle) skips both staging and committing rather than creating an empty commit. This is enforced by a dirty-own-path guard shared uniformly by every committer: after the pass, check whether the skill's own path actually changed, and if nothing changed, stage nothing, commit nothing, report the no-op, and return cleanly. This is the literal reading of the goal's "changes files" wording, keeps git history restricted to real changes, and avoids `--allow-empty` machinery whose audit value is negligible when the pass recorded nothing.

## Open questions

## Out of Scope

