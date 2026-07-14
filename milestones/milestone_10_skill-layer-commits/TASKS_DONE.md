# TASKS DONE

## Author Shared Skill-Layer Commit Procedure

Create the single execution-neutral source of truth for the skill-layer commit step — a new file under `shared/` that every committing skill and committing orchestrator will reference via `${CLAUDE_PLUGIN_ROOT}` (never restate), exactly as `complete-task`/`submit-task`/`answer-open-question-with-recommendation` reference their shared procedures today. It is the foundational artifact of this milestone: every later task points downstream skills at this convention rather than duplicating it.

The document must state all four elements of the milestone's committing model as decided in `requirements.md`:

- **Path-scoped staging** — stage only explicitly named paths, never `git add -A`, and decide the path set without content inspection (no diffing to choose what to include).
- **Commit-subject convention** — each committing skill's subject prefix is derived systematically from its distinctive function in the established `<Marker>: <descriptor>` house shape (the `-answer:` family being one instance), with every prefix staying clear of capture's `^Manual-answer:` grep by construction — no ad-hoc per-skill list, no grandfathered exceptions.
- **Dirty-own-path no-op guard** — after a pass, if the skill's own paths did not actually change, stage nothing, commit nothing, report the no-op, and return cleanly (no `--allow-empty`).
- **Layer rule** — user-invoked skills that change files commit; dispatched agents never commit; an orchestrator skill commits its agents' work after they return.

The document takes resolved inputs (the path set and the subject) and holds only the commit logic — no arg-parsing, no skill-specific behavior — mirroring how `shared/answer-procedure.md` is execution-neutral while its wrappers own arg-parsing and committing.

**Provides:**
- `shared/commit-procedure.md` — the execution-neutral shared commit core referenced by every committing skill/orchestrator via `${CLAUDE_PLUGIN_ROOT}`. Its input contract is a resolved path set plus a resolved commit subject; it defines path-scoped staging, the `<Marker>: <descriptor>` subject convention (all prefixes clear of `^Manual-answer:`), the dirty-own-path no-op guard, and the skills-commit/agents-never-commit/orchestrator-commits-after-return layer rule.

**Notes:**
- This is authoring one new Markdown file only — it wires no existing skill onto the procedure (each committer's rewiring is a later task) and changes no other file. It must be written so downstream skills can reference it without restating any of it, following the plugin's `shared/ = single source of truth across ≥2 runners` convention.
- Keep it execution-neutral in the plugin's established sense: it must not mention arg-parsing, the `DONE`/`FAILED` agent return protocol, `<MILESTONE_DIR>` resolution, or any per-skill subject — those belong to the wrapping skills/agents/orchestrators. The layer rule is stated as a rule the wrappers follow, not as behavior this file executes.
- The no-op guard is deliberately `--allow-empty`-free; state the guard as check-own-paths-then-skip, matching the `No-op pass commit` decision in `requirements.md`.

**Success:**
- `shared/commit-procedure.md` exists.
- Its content states all four elements: path-scoped staging (never `git add -A`, no content inspection), the systematic `<Marker>: <descriptor>` subject convention that stays clear of `^Manual-answer:`, the dirty-own-path no-op guard (no `--allow-empty`), and the skills-commit / agents-never-commit / orchestrator-commits-after-return layer rule.
- The document is execution-neutral: it references no specific skill's arguments or subject prefix and describes no arg-parsing, and it is phrased so a skill can reference it via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` without restating its steps.

---

## Commit From Three Milestone-Lifecycle Skills

Turn the three simple single-edit milestone-lifecycle skills — `define-milestone-goal`, `specify-milestone-starting-state`, and `goto-next-milestone` — into committers under this milestone's skill-layer rule. Each currently ends with the instruction "Do not commit — leave staging to the user"; replace that end-state with a commit step that references the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) rather than restating its logic. Each skill ends its pass by committing exactly the file(s) it changed, path-scoped, under its own distinct function-derived subject prefix, applying the uniform dirty-own-path no-op guard.

Each skill has a different own-path set to stage: `define-milestone-goal` creates and commits the new milestone directory's three files (`requirements.md`, `TASKS_TODO.md`, `TASKS_DONE.md`); `specify-milestone-starting-state` commits the milestone's `requirements.md`; `goto-next-milestone` commits `milestones/README.md`. The three subject prefixes must be distinct from one another, each derived from that skill's distinctive function in the `<Marker>: <descriptor>` house shape, and none may match capture's `^Manual-answer:` grep.

**Provides:**
- `define-milestone-goal`, `specify-milestone-starting-state`, and `goto-next-milestone` each now end by committing their own path-scoped change set under a distinct, function-derived `<Marker>: <descriptor>` subject prefix (all clear of `^Manual-answer:`), via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.

**Notes:**
- These are per-skill wirings, not one copy-pasted block: each skill's staged path set differs (a fresh directory of three files, a single `requirements.md`, or `milestones/README.md`), so the resolved path set handed to the shared procedure is authored per skill.
- The commit step replaces the existing trailing "Do not commit — leave staging to the user" Rule in each of the three files — remove that line (and any other leave-staged/do-not-commit prose) so no residual "leave staging to the user" instruction contradicts the new commit step.
- Reference the shared procedure via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic in these skills — the skill supplies only the resolved path set and the resolved subject.

**Success:**
- Each of `skills/define-milestone-goal/SKILL.md`, `skills/specify-milestone-starting-state/SKILL.md`, and `skills/goto-next-milestone/SKILL.md` ends with a commit step that references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- No "Do not commit", "leave staging to the user", or other leave-staged/do-not-commit prose remains in any of the three files.
- The three commit subject prefixes are distinct from one another, each in `<Marker>: <descriptor>` shape, function-derived, and none matches `^Manual-answer:`.
- Each skill's commit stages only its own edited path(s) (the new milestone directory's files / the milestone `requirements.md` / `milestones/README.md`) and never uses `git add -A`.

---

## Commit From Two Requirements-Editing Skills

Turn the two requirements-editing skills — `review-milestone-requirements` and `modify-milestone-goal` — into committers under this milestone's skill-layer rule. Each ends its pass by committing exactly its own edit to the milestone's `requirements.md`, path-scoped, under its own distinct function-derived subject prefix, via the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) rather than restating its logic. `review-milestone-requirements` is the milestone's flagship no-op-pass case: a pass that reconciles, prunes, and surfaces nothing must stage nothing and commit nothing (the uniform dirty-own-path guard), reporting the no-op — while a pass that did reshape the questions section commits that reshaping. `modify-milestone-goal`'s documented "does not commit — leave staged" ending is replaced by the commit step; its act-only scope (edit `## Goal` only, surface but never cascade downstream impact) is unchanged.

Both skills stage the same own-path — the milestone's `requirements.md` — but must commit under two distinct subject prefixes, each derived from that skill's distinctive function in the `<Marker>: <descriptor>` house shape, and neither matching capture's `^Manual-answer:` grep.

**Provides:**
- `review-milestone-requirements` and `modify-milestone-goal` each now end by committing their own path-scoped edit to `<MILESTONE_DIR>/requirements.md` under a distinct, function-derived `<Marker>: <descriptor>` subject prefix (both clear of `^Manual-answer:`), via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; `review-milestone-requirements`'s no-op pass commits nothing.

**Notes:**
- `review-milestone-requirements` is where the no-op-pass decision most matters: its own reporting already says so when a pass finds nothing to reconcile and no new gaps, so the commit step must sit behind the dirty-own-path guard — commit the reshaped `requirements.md` when the pass changed it, stage and commit nothing when it did not.
- `modify-milestone-goal`'s trailing Rule is the exact line "Do not commit — leave the change staged for the user to review." — remove it (and any other leave-staged/do-not-commit prose) so no residual instruction contradicts the new commit step; leave the act-only "edit only `## Goal`" / "surface, never cascade" rules intact.
- Both skills edit only `requirements.md`, so the two staged path sets are identical; distinctness lives entirely in the two subject prefixes. Reference the shared procedure via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic — each skill supplies only the resolved path (`<MILESTONE_DIR>/requirements.md`) and its resolved subject.

**Success:**
- Each of `skills/review-milestone-requirements/SKILL.md` and `skills/modify-milestone-goal/SKILL.md` ends with a commit step that references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- `review-milestone-requirements`'s no-op pass path explicitly commits nothing (dirty-own-path guard), while a pass that reshaped the questions section commits `requirements.md`.
- No "does not commit", "leave staging to the user", "leave the change staged", or other leave-staged/do-not-commit prose remains in either file.
- The two commit subject prefixes are distinct from one another, each in `<Marker>: <descriptor>` shape, function-derived, and neither matches `^Manual-answer:`.
- Each skill's commit stages only its own edited path (`<MILESTONE_DIR>/requirements.md`) and never uses `git add -A`.

---

