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

## Rewire Three Answer Skills Onto Commit Procedure

Bring the three already-committing answer-recording skills — `answer-open-question`, `answer-open-question-with-recommendation` (the **skill**, not its agent), and `answer-open-question-with-alternative` — onto this milestone's shared skill-layer commit convention **without changing their observable behavior**. Each already commits its own path-scoped `requirements.md` edit today with its commit mechanics restated inline; re-express each skill's commit step as a reference to the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) instead of spelling out the path-scoped staging, subject, and no-op logic in-skill, and drop the prose that frames these skills as the documented committing "exception" — under the new layer rule every file-changing skill commits, so they are the norm, not exceptions.

Each skill keeps its existing subject exactly as-is (`Manual-answer: <Short Title>` / `Recommendation-answer: <Short Title>` / `Alternative-answer: <Short Title>` — all already conforming `<Marker>: <descriptor>` instances), its path-scoped staging of `<MILESTONE_DIR>/requirements.md`, and its commit body exactly as they are, and comes under the uniform dirty-own-path no-op guard (which subsumes each skill's existing "commit only if the answer was actually recorded" conditional — a clean-stop leaves the path unchanged, so nothing is committed, preserving today's behavior). The skills supply only their already-resolved path (`<MILESTONE_DIR>/requirements.md`) and their resolved subject to the shared procedure.

**Notes:**
- Unlike the two sibling grouping tasks (which turn non-committers into committers), these three **already commit** — so this is a re-expression onto the shared procedure, not a behavior change. Subjects, path scope, and bodies must come out byte-for-byte equivalent; only the restated mechanics move to the reference and the "exception" framing is removed.
- Each of the three files carries the exception framing in **two** places that both must go: the Workflow commit step ("This is a deliberate, documented exception to the project's 'individual skills never commit' rule…" / "Committing here is a deliberate, documented exception…") **and** the trailing `## Rules` bullet restating it. Remove the exception framing from both, in all three files.
- Reference the shared procedure via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic in these skills.
- Scope is the three `SKILL.md` files only. The `answer-open-question-with-recommendation` **agent** is out of scope (its commit moving up to the orchestrator is a separate concern), and so is any re-sync of the committing-vs-staging prose in `CLAUDE.md` / `README.md`.
- Leave every existing clean-stop guard untouched: `answer-open-question`'s retired-sentinel redirect and Short-Title mismatch, the recommendation skill's no-`<recommendation>`-element / missing-block stop, and the alternative skill's missing-question / no-alternatives / non-matching-id stops. Each already commits nothing on a clean stop, which is exactly what the dirty-own-path guard also yields.

**Success:**
- Each of `skills/answer-open-question/SKILL.md`, `skills/answer-open-question-with-recommendation/SKILL.md`, and `skills/answer-open-question-with-alternative/SKILL.md` has its commit step reference `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` instead of restating path-scoped-staging / subject-convention / no-op-guard mechanics.
- The three commit subjects are unchanged and still exactly `Manual-answer: <Short Title>`, `Recommendation-answer: <Short Title>`, and `Alternative-answer: <Short Title>` respectively; each commit still stages only `<MILESTONE_DIR>/requirements.md` (never `git add -A`) and its body is unchanged.
- No "deliberate, documented exception", "individual skills never commit" exception framing, or equivalent "exception to the … rule" prose remains in any of the three files — in either the Workflow step or the `## Rules` section.
- Each skill's commit is brought under the dirty-own-path no-op guard (via the shared procedure), and its existing clean-stop guards are unchanged.
- The `answer-open-question-with-recommendation` agent file is not modified by this task.

---

