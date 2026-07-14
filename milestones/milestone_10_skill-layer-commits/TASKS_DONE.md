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

## Commit From The Task-Authoring Skills

Turn the two task-authoring-path committers — the `submit-task` **skill** (which authors and inserts inline) and the `derive-tasks` **orchestrator** — into committers under this milestone's skill-layer rule, and verify the `submit-task` **agent** stays non-committing. Both skills are currently **silent** about git (they just edit and hand back a dirty tree); each now ends by committing exactly its own change to the milestone's `TASKS_TODO.md`, path-scoped, under its own distinct function-derived subject prefix, referencing the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) rather than restating its logic.

The two skills commit at different points because they occupy different layers: the `submit-task` skill authors inline, so it commits its **own** path-scoped insertion into `<MILESTONE_DIR>/TASKS_TODO.md` at the end of its run; `derive-tasks` is an orchestrator, so it commits **once at the end of a run** — after all its sequential `submit-task` agents have returned (the milestone's stated per-run granularity for it) — covering the `TASKS_TODO.md` file it initialized and its agents appended into, under the uniform dirty-own-path no-op guard. The two subject prefixes must be distinct from each other (and from the other committing skills' prefixes), each derived from that skill's distinctive function in the `<Marker>: <descriptor>` house shape, and neither matching capture's `^Manual-answer:` grep. The `submit-task` agent and the execution-neutral `shared/submit-procedure.md` stay commit-free — under the layer rule agents never commit — so this task adds **no** commit language to either; it only confirms they gain none.

**Provides:**
- The `submit-task` skill now ends by committing its own path-scoped insertion into `<MILESTONE_DIR>/TASKS_TODO.md` under a distinct, function-derived `<Marker>: <descriptor>` subject prefix (clear of `^Manual-answer:`), via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- `derive-tasks` now ends by committing once per run — after its sequential `submit-task` agent loop returns — its path-scoped `<MILESTONE_DIR>/TASKS_TODO.md` under its own distinct, function-derived prefix (clear of `^Manual-answer:`), with the dirty-own-path no-op guard, via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.

**Notes:**
- `derive-tasks` commits **once per run, not once per agent** — the single commit sits after the whole sequential per-brief agent loop completes (it is the orchestrator committing its agents' appended work after they return), never inside the loop. This mirrors `complete-all-tasks` being the per-task committer while `derive-tasks` is the milestone's once-at-the-end committer.
- Both committers stage only `<MILESTONE_DIR>/TASKS_TODO.md`; the distinctness lives entirely in the two subject prefixes. Reference the shared procedure via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic — each supplies only the resolved path (`<MILESTONE_DIR>/TASKS_TODO.md`) and its resolved subject.
- The `submit-task` **agent** part is a boundary check, not an edit: `agents/submit-task.md` already carries "Do not commit," and the execution-neutral `shared/submit-procedure.md` must gain no commit language. Verify both remain commit-free; add nothing to either.

**Success:**
- `skills/submit-task/SKILL.md` ends with a commit step that references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` and stages only `<MILESTONE_DIR>/TASKS_TODO.md` (never `git add -A`).
- `skills/derive-tasks/SKILL.md` ends with a single commit step — placed after its sequential agent loop returns, committing exactly once per run — that references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, stages only `<MILESTONE_DIR>/TASKS_TODO.md` (never `git add -A`), and is under the dirty-own-path no-op guard.
- `agents/submit-task.md` and `shared/submit-procedure.md` contain no `git add`/`git commit`/commit-step language — both remain commit-free.
- The two commit subject prefixes are distinct from one another, each in `<Marker>: <descriptor>` shape, function-derived, and neither matches `^Manual-answer:`.

---

## Commit From The Complete-Task Skill

Turn the `complete-task` **skill** (the inline, user-facing single-task completion path) into a committer under this milestone's skill-layer rule. It currently ends by leaving the diff staged ("committing belongs to `/complete-all-tasks` alone"); replace that end-state with a commit step that references the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) rather than restating its logic. Per the *Completion commit path scope* decision in `requirements.md`, the skill commits the task's real change set — the exact set of paths the completer created or edited while carrying out the task (recorded as each edit is made, never derived by diffing) together with the milestone's two task-list files (the `TASKS_TODO.md` the task left and the `TASKS_DONE.md` it joined) — as one path-scoped commit (never `git add -A`), under its own distinct function-derived subject prefix, applying the uniform dirty-own-path no-op guard.

The execution-neutral `shared/complete-procedure.md` — run by both this skill and the `complete-task` agent — must stay commit-free: the commit itself lives only in this skill wrapper. If the record-paths-as-you-edit bookkeeping needs a home, place it so the shared procedure gains no commit language (recording paths as they are edited is not committing and not content inspection).

**Provides:**
- The `complete-task` skill now ends by committing its own path-scoped completion change set (the completer's recorded created/edited paths plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`) under a distinct, function-derived `<Marker>: <descriptor>` subject prefix (clear of `^Manual-answer:`), via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.

**Notes:**
- The staged path set is the completer's created/edited paths (recorded as each edit happens — not chosen by diffing the tree) plus the two task-list files `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`; this matches the *Completion commit path scope* decision's "record paths as each edit is made" wording exactly.
- Keep `shared/complete-procedure.md` commit-free — it must not gain `git add`/`git commit`/commit-step language, because the `complete-task` agent also runs it and agents never commit. Wherever the record-paths bookkeeping lands, phrase it as commit-free recording (recording is not committing), and put the commit only in this skill's `SKILL.md`.
- Remove the trailing leave-staged prose in **both** places it appears: the Workflow "Hand back for review" step ("Leave the changes staged, not committed — committing belongs to `/complete-all-tasks` alone…") **and** the `## Rules` bullet ("Do not commit. Leave the changes staged for the user to review and commit."), so no residual instruction contradicts the new commit step.
- A failed or abandoned completion must commit nothing — this is exactly what the shared procedure's dirty-own-path no-op guard yields (a no-match clean stop leaves the tree unchanged, so nothing is staged or committed). Do not restate the guard; reference the shared commit procedure.
- Reference the shared procedure via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic — the skill supplies only the resolved path set and its resolved subject.
- Scope is `skills/complete-task/SKILL.md` (and, if needed, a commit-free bookkeeping note) only. The other half of the *Completion commit path scope* decision — the `complete-all-tasks` orchestrator committing its `complete-task` agent's per-task path set — is a separate concern and not part of this task.

**Success:**
- `skills/complete-task/SKILL.md` ends with a commit step that references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- That commit stages the completer's recorded created/edited paths plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`, and never uses `git add -A`.
- The commit subject is a function-derived `<Marker>: <descriptor>` prefix that does not match `^Manual-answer:`.
- No "Do not commit", "leave staged", "leave the changes staged", or "committing belongs to `/complete-all-tasks`" prose remains anywhere in `skills/complete-task/SKILL.md` (neither the Workflow step nor `## Rules`).
- `shared/complete-procedure.md` contains no `git add`/`git commit`/commit-step language — it remains commit-free.
- A failed or abandoned completion commits nothing (the dirty-own-path no-op guard from the shared procedure).

---


## Commit Per Task From Complete-All-Tasks Orchestrator

Complete the *Completion commit path scope* decision's orchestrator half (the sibling of the *Commit From The Complete-Task Skill* task, which handled the inline path): make the `complete-all-tasks` orchestrator commit its `complete-task` agent's real per-task change set, and give the agent the path-recording/hand-back contract that feeds it. The `complete-task` **agent** stays a non-committer (agents never commit under the layer rule); what it gains is: it records the exact set of paths it created or edited while carrying out its task — recorded as each edit is made, never by diffing or content inspection — and either stages that explicit path set itself or returns the path list to the orchestrator, in both cases alongside the milestone's two task-list files (`<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`), so the orchestrator's commit can stay path-scoped.

The `complete-all-tasks` orchestrator keeps its existing **per-task** commit granularity (one commit after each successful agent return, unchanged) but replaces its step-2c body: drop `git add -A` in favour of committing that explicit per-task path set, and drop the bare task-heading subject in favour of a function-derived `<Marker>: <descriptor>` subject prefix (clear of `^Manual-answer:`), with the task heading moving into the commit body. Reference the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) for the path-scoped-staging, subject-convention, and no-op-guard mechanics rather than restating them.

**Provides:**
- The `complete-all-tasks` orchestrator now commits each completed task's explicit path set (the agent's recorded created/edited paths plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`) path-scoped, per task, under a distinct function-derived `<Marker>: <descriptor>` subject prefix (clear of `^Manual-answer:`) with the task heading in the commit body, via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- The `complete-task` agent now carries a path-recording/hand-back contract: it records the paths it created/edited (as each edit is made, no diffing) and either stages that explicit set itself or returns it to the orchestrator, alongside the two task-list files — while still never committing.

**Notes:**
- The agent's path-recording bookkeeping is the **same recorded path set** the inline `complete-task` skill uses in the *Commit From The Complete-Task Skill* task; place this task's agent-side wording consistently with wherever that sibling task homed the bookkeeping. `shared/complete-procedure.md` must stay execution-neutral and commit-free — recording paths as they are edited is not committing and not content inspection, so it may live in the shared procedure or the agent wrapper, but no `git add`/`git commit`/commit-step language may enter the shared procedure. The commit lives only in the orchestrator.
- The orchestrator commit stays **per task** (inside the loop, after each agent's success return) — this is not the once-at-the-end granularity `derive-tasks` uses. Only the staging mechanism (explicit path set, no `git add -A`) and the subject (function-derived prefix + heading-in-body) change; the after-each-success timing is unchanged.
- The orchestrator's new subject prefix is function-derived and must be distinct from the other committing skills' prefixes and clear of `^Manual-answer:`; the task's `##` heading text that was the old subject now goes into the commit body.
- Reference `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` for the commit mechanics; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic — the orchestrator supplies only the resolved per-task path set and its resolved subject.
- Scope is `skills/complete-all-tasks/SKILL.md` and `agents/complete-task.md`. Leave the orchestrator's existing loop structure (re-read top task, spawn agent, stop-on-FAILED, never-complete-directly) intact; only step 2c's staging/commit body and the surrounding commit prose change.

**Success:**
- `skills/complete-all-tasks/SKILL.md` no longer contains `git add -A` and no longer uses the bare task heading as the commit subject; its per-task commit step stages the explicit per-task path set and references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- The orchestrator commits once after each successful task (granularity unchanged), under a function-derived `<Marker>: <descriptor>` subject prefix that does not match `^Manual-answer:`, with the task heading in the commit body.
- `agents/complete-task.md` carries the path-recording/hand-back contract (record created/edited paths as edited — no diffing/content inspection — and stage-or-return them alongside the two task-list files) and still states the agent does not commit.
- `shared/complete-procedure.md` contains no `git add`/`git commit`/commit-step language — it remains commit-free and execution-neutral.

---

## Commit From The Recommend Sweep Orchestrator

Turn the `recommend-all-open-questions` orchestrator into a committer under this milestone's skill-layer rule, at the milestone's stated granularity for it: **once at the end of the sweep**. It currently ends by staging path-scoped but deliberately **not** committing (its step 5 "Stage the edit (do not commit)" and its final `## Rules` "Mutate but do not commit" bullet); replace that end-state with a single commit step — after all its per-question subagents have returned and their sub-elements are embedded — that commits exactly its own path-scoped edit to `<MILESTONE_DIR>/requirements.md`, under its own distinct function-derived subject prefix, referencing the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) rather than restating its logic, all under the uniform dirty-own-path no-op guard so a sweep that annotated nothing (every block already carried a `<recommendation>` element) stages and commits nothing.

This also requires rewriting the now-overridden rationale prose that frames the embedded-recommendation scaffolding as *transient* and asserts the durable git record is only the eventual `Recommendation-answer:` commit — under the new rule the annotation sweep records its own commit, so that framing (the intro paragraph "The durable git record is the eventual `Recommendation-answer:` commit … transient scaffolding …" and its echo in the old step 5) must go. The subject prefix is derived from this skill's distinctive recommend-sweep function in the `<Marker>: <descriptor>` house shape, must be distinct from the other committing skills' prefixes, and must not match capture's `^Manual-answer:` grep. The skill supplies only its resolved path (`<MILESTONE_DIR>/requirements.md`) and its resolved subject to the shared procedure.

Every other deliberate property of the sweep is untouched: it stays the sole-mutator whole-block-replacement embedder, idempotently skips blocks already carrying a `<recommendation>` element, keeps **no clean-working-tree precondition**, stays argument-free, and its dispatched `recommend-open-question` subagents stay read-only and non-committing.

**Provides:**
- `recommend-all-open-questions` now ends by committing once per sweep — after its per-question subagent dispatches return and their sub-elements are embedded — its path-scoped `<MILESTONE_DIR>/requirements.md` under a distinct, function-derived `<Marker>: <descriptor>` subject prefix (clear of `^Manual-answer:`), with the dirty-own-path no-op guard, via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.

**Notes:**
- The commit is **once at the end of the sweep**, not per question — it mirrors `derive-tasks` being the milestone's once-at-the-end committer (contrast `complete-all-tasks`'s per-task and `answer-all-open-questions-with-recommendation`'s per-answer granularities). The recommend sweep records **no decisions and triggers no cascades**, so the once-at-the-end model needs none of the per-question re-check/gather-order machinery a decision-recording sweep uses; only the trailing stage-and-stop becomes a stage-and-commit.
- The old step 5 heading is "### 5. Stage the edit (do not commit)" and its body ends "**do not commit** … the durable git record is the eventual `Recommendation-answer:` commit, not the transient recommendation scaffolding." — replace the whole step with the commit step. The trailing `## Rules` bullet begins "**Mutate but do not commit**: stage path-scoped `git add <MILESTONE_DIR>/requirements.md` only … and stop. Require **no** clean working tree." — rewrite it to a commit rule while preserving its "no clean working tree" clause.
- The **no-clean-working-tree** property is retained, but its *stated reason* changes: the intro bullet "**No clean-working-tree precondition.** … this skill commits nothing, so it needs no clean tree." currently justifies it by "commits nothing," which is no longer true. Keep the property, drop/rewrite the now-false "commits nothing" justification (the once-at-the-end single commit needs no one-commit-per-answer discipline, so it still needs no clean tree).
- Reference the shared procedure via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic — the skill supplies only the resolved path (`<MILESTONE_DIR>/requirements.md`) and its resolved subject.
- Scope is `skills/recommend-all-open-questions/SKILL.md` only. The `recommend-open-question` agent stays read-only and non-committing — add no commit language to it. Re-syncing the committing-vs-staging prose in `CLAUDE.md` / `README.md` is a separate concern, not part of this task.

**Success:**
- `skills/recommend-all-open-questions/SKILL.md` ends with a single commit step — placed after its per-question subagent dispatches return, committing exactly once per sweep — that references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, stages only `<MILESTONE_DIR>/requirements.md` (never `git add -A`), and is under the dirty-own-path no-op guard.
- A no-op sweep (every gathered block already contained a `<recommendation>` element, so nothing was annotated) stages nothing and commits nothing.
- The stale "transient scaffolding" / "the durable git record is the eventual `Recommendation-answer:` commit" / "do not commit" rationale is gone from the file (both the intro paragraph and the old step 5), and no "Mutate but do not commit" or "leave the staged edit for the user" prose remains.
- The commit subject is a function-derived `<Marker>: <descriptor>` prefix, distinct from the other committing skills' prefixes and not matching `^Manual-answer:`.
- The sweep's other properties are unchanged: sole-mutator whole-block-replacement embedding, idempotent skip of already-`<recommendation>`-bearing blocks, no clean-working-tree precondition, argument-free; and `agents/recommend-open-question.md` gains no commit language (stays read-only, non-committing).

---

## Move Recommendation-Answer Sweep Commit To Orchestrator

Reverse the milestone-7 inversion in the `answer-all-open-questions-with-recommendation` sweep so it obeys this milestone's layer rule (agents never commit; an orchestrator commits its agents' work after they return). Today the dispatched `answer-open-question-with-recommendation` **agent** records *and* commits each answer, while the orchestrator "never edits `requirements.md` and never commits." Move the commit **up from the agent to the orchestrator**, per answer, preserving one-commit-=-one-answer.

The **agent** (`agents/answer-open-question-with-recommendation.md`) still runs `${CLAUDE_PLUGIN_ROOT}/shared/answer-with-recommendation-procedure.md` to record one question's answer in `<MILESTONE_DIR>/requirements.md`, but no longer stages or commits: its `Commit your own answer` section is removed, and it hands the recorded-but-uncommitted edit back — its `DONE`/`FAILED` protocol adjusted so `DONE` means "recorded, not committed" (its failure path still leaves the working tree exactly as it found it, committing nothing).

The **orchestrator** (`skills/answer-all-open-questions-with-recommendation/SKILL.md`) commits after each successful agent `DONE` return, before dispatching the next agent (still strictly sequential, because cascades mutate the shared document): path-scoped to `<MILESTONE_DIR>/requirements.md` (never `git add -A`), keeping the existing `Recommendation-answer: <Short Title>` subject with the lifted recommendation rationale in the commit body, referencing `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) for the mechanics rather than restating them.

**Provides:**
- Under `answer-all-open-questions-with-recommendation`, the **orchestrator commits per answer** (path-scoped `<MILESTONE_DIR>/requirements.md`, subject `Recommendation-answer: <Short Title>`, lifted recommendation rationale in the body, via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`) and the dispatched `answer-open-question-with-recommendation` **agent no longer commits** — it records the answer and returns `DONE` (with the lifted recommendation content for the commit body) / `FAILED` around an uncommitted edit.

**Notes:**
- This is the per-answer-granularity sibling of the *Commit Per Task From Complete-All-Tasks Orchestrator* task (which does the same orchestrator-commits move at per-task granularity). The commit stays **per answer** — inside the loop, after each successful agent `DONE`, before the next dispatch — not once-at-the-end; one-commit-=-one-answer is preserved.
- The orchestrator's commit body must carry the **lifted recommendation rationale**, which the agent computes (the `<option>` — `<rationale>` text lifted from the block's `<recommendation>` element). So the agent's adjusted `DONE` return must hand that recorded answer content back to the orchestrator for the commit body — the orchestrator does not re-derive the lift. This is the hand-back contract that replaces the agent's own commit.
- The subject stays exactly `Recommendation-answer: <Short Title>` — an already-conforming `<Marker>: <descriptor>` instance that stays clear of capture's `^Manual-answer:` grep; this task introduces **no** new prefix. Reference the shared commit procedure for path-scoped staging / no-op guard mechanics; do not restate them.
- Rewrite the prose in **both** components that documents the old agent-commits divergence: the orchestrator's intro paragraphs and its `## Rules` "the agent owns all mutation and its own path-scoped commit … The orchestrator never edits `requirements.md` and never commits … This inverts the usual orchestrator-commits arrangement" bullet must flip to orchestrator-commits; the agent's "Commit your own answer" section and the commit references in its return-protocol prose must go.
- The two shared procedures `shared/answer-with-recommendation-procedure.md` and `shared/answer-procedure.md` are execution-neutral and already commit-free — they must stay that way; add no commit language to either.
- The single-question `answer-open-question-with-recommendation` **skill** keeps committing inline and is **not** modified by this task. Re-syncing the committing-vs-staging / milestone-7-inversion prose in `CLAUDE.md` and `README.md` is a separate concern, not part of this task.

**Success:**
- `agents/answer-open-question-with-recommendation.md` contains no `git add`/`git commit`/staging language; its `DONE` return wraps a recorded-but-uncommitted edit (and carries back the lifted recommendation content for the orchestrator's commit body), and its `FAILED` path leaves the working tree exactly as it found it (commits nothing).
- `skills/answer-all-open-questions-with-recommendation/SKILL.md` commits once per successful agent `DONE` — before dispatching the next agent — staging only `<MILESTONE_DIR>/requirements.md` (never `git add -A`), under subject `Recommendation-answer: <Short Title>` with the lifted recommendation rationale in the body, referencing `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- The sweep's strictly-sequential dispatch and its per-question re-read/skip sequencing (step 2a live re-check, single gathered ordered pass, no outer re-gather loop) are unchanged.
- No "the agent … commits" / "the orchestrator never edits `requirements.md` and never commits" / "inverts the usual orchestrator-commits arrangement" divergence prose remains in either the orchestrator or the agent file.
- `shared/answer-with-recommendation-procedure.md` and `shared/answer-procedure.md` contain no `git add`/`git commit`/commit-step language — both remain commit-free.
- `skills/answer-open-question-with-recommendation/SKILL.md` (the single-question skill) is not modified by this task.

---

## Commit From The Finish-Milestone Skill

Turn `finish-current-milestone` into a committer under this milestone's skill-layer rule, per the *Finish commit file set* decision in `requirements.md`. It currently ends "never commits" (its step 8 recommendation prose and its trailing `## Rules` bullet both say so, leaving a dirty tree); replace that end-state with a single commit step — after the summary is written, the pointer is cleared, and the optional `CLAUDE.md` update has run — that records the whole finish as one path-scoped commit, referencing the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) rather than restating its logic. Its recommend-never-auto-run of `/capture-milestone-principle-updates` and every other property of the finish flow are unchanged.

The staged path set is authored per the decision: **always** `milestones/README.md` (which carries both the completion summary and the current-milestone pointer cleared to `none` in the same edit) and **additionally** the workspace `CLAUDE.md` **only on passes where step 7 actually edited it** — conditional staging keyed on whether-the-skill-edited-it, which is not content inspection. Because the pointer-clear rides inside the same README edit, the committed README already carries `Current milestone: none`, so `goto-next-milestone`'s none-pointer precondition is recorded in git rather than left in a dirty tree. The skill commits that explicit path set (never `git add -A`) under one distinct function-derived `<Marker>: <descriptor>` subject prefix that stays clear of capture's `^Manual-answer:` grep, applying the uniform dirty-own-path no-op guard.

**Provides:**
- `finish-current-milestone` now ends by committing its whole finish as one path-scoped commit — always staging `milestones/README.md` and conditionally staging `CLAUDE.md` (only when step 7 edited it) — under a distinct, function-derived `<Marker>: <descriptor>` subject prefix (clear of `^Manual-answer:`), via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.

**Notes:**
- The conditional `CLAUDE.md` staging is decided by **whether this skill's step 7 edited it**, recorded as the edit is (or is not) made — not by diffing or inspecting content. On a pass that skips step 7 entirely, `CLAUDE.md` is not staged and the commit covers `milestones/README.md` alone.
- The commit subject is one finish prefix in the `<Marker>: <descriptor>` house shape, function-derived from this skill's distinctive milestone-finish role, distinct from the other committing skills' prefixes, and must not match `^Manual-answer:`.
- Remove the "never commits" prose from both the step 8 recommendation text and the trailing `## Rules` bullet ("it never invokes it and never commits"), and any other leave-staged/do-not-commit wording, so no residual instruction contradicts the new commit step. Keep the recommend-but-never-auto-run of `/capture-milestone-principle-updates` intact — only the "never commits" clause changes.
- Reference the shared procedure via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic — the skill supplies only the resolved path set (README always, `CLAUDE.md` conditionally) and its resolved subject.
- Scope is `skills/finish-current-milestone/SKILL.md` only. Re-syncing the committing-vs-staging prose in `CLAUDE.md` / `README.md` is a separate concern, not part of this task.

**Success:**
- `skills/finish-current-milestone/SKILL.md` ends with a single commit step that references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- That commit always stages `milestones/README.md` and stages `CLAUDE.md` only on passes where step 7 edited it, and never uses `git add -A`.
- The committed `milestones/README.md` carries both the completion summary and `Current milestone: none` (the pointer-clear rides inside the same README edit), so `goto-next-milestone`'s none-pointer precondition is recorded in git.
- No "never commits", "leave staged", or other leave-staged/do-not-commit prose remains anywhere in the file (neither step 8 nor `## Rules`); the recommend-but-never-auto-run of `/capture-milestone-principle-updates` is preserved.
- The commit subject is a function-derived `<Marker>: <descriptor>` prefix, distinct from the other committing skills' prefixes and not matching `^Manual-answer:`.

---

## Commit From The Principle-Capture Skill

Turn `capture-milestone-principle-updates` — the finish-time skill that is the sole writer of the project-wide principle store `milestones/answer_decision_principles.md` — into a committer under this milestone's skill-layer rule, per the *No-op pass commit* decision in `requirements.md`. It currently ends "does not commit — leaves its edit staged" (its intro note and its trailing `## Rules` bullet both say so, handing back a dirty tree); replace that end-state with a commit step — after the confirmed revise-vs-add edits to the store have been applied — that records its own edit to `milestones/answer_decision_principles.md` as one path-scoped commit, referencing the shared commit procedure (see the *Author Shared Skill-Layer Commit Procedure* task's Provides) rather than restating its logic. This skill is the milestone's second named no-op case (alongside `review-milestone-requirements`): a pass that distills no new principle — the empty commit range, or in-range commits that none generalize — leaves the store untouched, so under the uniform dirty-own-path guard it stages nothing and commits nothing, reporting the no-op as it already does.

Everything else about the skill is unchanged: it still runs after `/finish-current-milestone` has cleared the pointer to `none`, still resolves `<MILESTONE_DIR>` from the last row of the `## Completed Milestones` table in `milestones/README.md` (not via `shared/get-current-milestone.md`), still walks that milestone's answers with the path-scoped `git log --grep='^Manual-answer: '`, and still runs its internal cross-candidate dedup and strongest-first per-candidate revise-vs-add confirmation against the live store. The staged path is the single fixed-path store `milestones/answer_decision_principles.md` (a `milestones/`-root artifact, not under `<MILESTONE_DIR>`). The subject is one prefix in the `<Marker>: <descriptor>` house shape, function-derived from this skill's distinctive principle-capture role, distinct from the other committing skills' prefixes, and must not match capture's own `^Manual-answer:` grep.

**Provides:**
- `capture-milestone-principle-updates` now ends by committing its own path-scoped edit to `milestones/answer_decision_principles.md` under a distinct, function-derived `<Marker>: <descriptor>` subject prefix (clear of `^Manual-answer:`), with the dirty-own-path no-op guard, via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; a pass that distills no new principle commits nothing.

**Notes:**
- This is the skill's named no-op case: the existing empty-commit-range exit and the "commits exist but none generalize" exit both leave the store unedited, so the commit step must sit behind the dirty-own-path guard — commit the store when a confirmed revise/add actually edited it, stage and commit nothing when the pass distilled none. The skill already reports "nothing to distill" on those exits; keep that report and simply commit nothing under it.
- Remove the "does not commit — leaves its edit staged" prose from **both** places it appears: the intro note ("Like every individual skill here it does **not** commit — it leaves its principle-store edit **staged** for the user to review.") and the trailing `## Rules` bullet ("**Do not commit.** Like every individual skill here, this leaves its edit to the principle store **staged** for the user to review."), plus the "edit is **staged, not committed**, for them to review" wording in the success-report step — so no residual leave-staged instruction contradicts the new commit step.
- The staged path is the fixed-path store `milestones/answer_decision_principles.md` itself — **not** any `<MILESTONE_DIR>` file — because this skill writes only that store. Reference the shared procedure via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`; do not restate its path-scoped-staging, subject-convention, or no-op-guard logic — the skill supplies only the resolved path (`milestones/answer_decision_principles.md`) and its resolved subject.
- Scope is `skills/capture-milestone-principle-updates/SKILL.md` only. Its milestone resolution (from the completed-milestones table), its `^Manual-answer:` harvest walk, and its dedup/revise-vs-add confirmation flow are all unchanged. Re-syncing the committing-vs-staging prose in `CLAUDE.md` / `README.md` is a separate concern, not part of this task.

**Success:**
- `skills/capture-milestone-principle-updates/SKILL.md` ends with a commit step that references `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` and stages only `milestones/answer_decision_principles.md` (never `git add -A`).
- A pass that distills no new principle (empty commit range, or in-range commits that none generalize — the store untouched) stages nothing and commits nothing (the dirty-own-path no-op guard), reporting the no-op as before.
- No "does not commit", "leaves its edit staged", "staged, not committed", or other leave-staged/do-not-commit prose remains anywhere in the file.
- The commit subject is a function-derived `<Marker>: <descriptor>` prefix, distinct from the other committing skills' prefixes and not matching `^Manual-answer:`.
- The skill's milestone resolution (from the `## Completed Milestones` table, not `shared/get-current-milestone.md`), its `^Manual-answer:` harvest walk, and its dedup/revise-vs-add confirmation flow are unchanged.

---

## Re-Sync CLAUDE.md And README.md To The Layer Rule

Re-sync the plugin's two documentation surfaces — the repository `CLAUDE.md` (its invariants section) and `README.md` (workflow documentation and per-skill reference) — to this milestone's layer-based commit rule, now that every skill/agent behavior change has landed. This task runs **last**: it documents the new committing model and retires every prose statement the earlier tasks made false, so that neither document contradicts the shipped behavior. It changes only documentation — no skill, agent, or `shared/` procedure is touched.

Retire everything the milestone obsoletes, in both documents at their respective altitudes:
- the role-based committing-vs-staging invariant ("a decision-recorder commits, a work-producer leaves changes staged"), including its "one orchestrator commits / three individual skills are the deliberate exception / one file-editing agent commits / every other individual skill never commits" counts and every per-skill "does not commit" / "leaves staged" / "leave staging to the user" rule for the now-converted skills;
- the milestone-7 agent-commits divergence documented for the `answer-all-open-questions-with-recommendation` sweep (the commit now lives in the orchestrator, per answer);
- the recommend sweep's "mutate-but-do-not-commit" / transient-scaffolding / "the durable git record is the eventual `Recommendation-answer:` commit" framing;
- the description of `complete-all-tasks` as committing via `git add -A` under a bare task-heading subject.

Document the new state (the four elements of the model as decided in `requirements.md` and codified in `shared/commit-procedure.md`): every user-invoked skill that changes files commits exactly those changes, path-scoped (never `git add -A`, no content inspection), under its own distinct function-derived `<Marker>: <descriptor>` subject prefix that stays clear of capture's `^Manual-answer:` grep; dispatched agents never commit; an orchestrator commits its agents' work after they return. State the commit granularity per orchestrator (`complete-all-tasks` per task with the task heading now in the commit body; the `answer-all-open-questions-with-recommendation` sweep per answer, committed by the orchestrator; `recommend-all-open-questions` and `derive-tasks` once at the end of a run), the uniform dirty-own-path no-op guard, and `shared/commit-procedure.md` as the single source of truth for the commit mechanics with the execution-neutral shared procedures (`answer-procedure.md`, `answer-with-recommendation-procedure.md`, `submit-procedure.md`, `complete-procedure.md`, `recommend-procedure.md`) staying commit-free. Name the two exemptions — `init-milestone-base-workflow` and `migrate-workspace` stay non-committing because a consuming project may not be a git repo or wants its own commit boundaries — and note the no-file-change conversational skills (`discuss-milestone-goal`, `discuss-open-question`, `discuss-new-task`, `ask-in-milestone-context`) are unaffected.

**Notes:**
- This is the milestone's documentation-truth task; its whole job is that no reader of either document is misled after the behavior changes. Every earlier task already deleted the stale prose *inside its own skill/agent files* — what survives, and what this task hunts, is the stale prose in the two top-level docs that describe those skills from the outside.
- Known stale passages to reconcile (verify against the live files, do not assume line numbers): in `CLAUDE.md`, the long committing-vs-staging invariant keyed on "what a skill produces" with its orchestrator/three-skills/one-agent counts, the `answer-all-open-questions-with-recommendation` "the agent commits — the orchestrator never commits" invariant, and the `recommend-all-open-questions` "mutate-but-do-not-commit" / transient-scaffolding invariant; in `README.md`, the per-skill reference entries that currently say `recommend-all-open-questions` "mutates but does not commit", the sweep agent "commits its own" answer while "the orchestrator itself never mutates or commits", `capture-milestone-principle-updates` / `modify-milestone-goal` / `complete-task` "leave staged / does not commit / never commits", `complete-all-tasks`'s commit description, and the "one of the three individual skills that deliberately commit" framing repeated across the three answer-skill entries.
- Keep every still-true statement intact — most importantly that `capture-milestone-principle-updates` harvests **only** `Manual-answer:` bodies via `git log --grep='^Manual-answer: '`, and that `Recommendation-answer:` / `Alternative-answer:` (and every new function-derived prefix) stay clear of that grep by construction. The subjects-are-provenance-markers convention survives; only the role-based committing/staging split is retired.
- Respect each document's altitude: `README.md` is user-facing narrative + per-skill reference (describe observable behavior — what commits, when, under what subject family); `CLAUDE.md` is the terse invariants list for a future editor (state the layer rule, the granularities, the no-op guard, the two exemptions, and the single-source-of-truth pointer to `shared/commit-procedure.md`). Do not copy `shared/commit-procedure.md`'s mechanics verbatim into either — reference the rule, do not restate the procedure.

**Success:**
- No prose in either `CLAUDE.md` or `README.md` contradicts the shipped behavior: no residual "leave staged" / "never commits" / "does not commit" / "git add -A" / "the agent commits" (for the recommendation sweep) claims remain about any of the converted skills or orchestrators.
- Both documents state, at their respective altitudes, the layer rule (file-changing skills commit path-scoped under a distinct function-derived `<Marker>: <descriptor>` subject clear of `^Manual-answer:`; agents never commit; orchestrators commit their agents' work after return), the per-orchestrator granularities, the dirty-own-path no-op guard, and `shared/commit-procedure.md` as the mechanics' single source of truth.
- Both documents name the two exemptions (`init-milestone-base-workflow`, `migrate-workspace`) with the reason (a consuming project may not be a git repo or wants its own commit boundaries), and identify the conversational no-file-change skills as unaffected.
- The still-true invariants survive verbatim in intent — capture harvesting only `Manual-answer:` bodies, and the non-manual answer subjects staying clear of that grep.
- No skill, agent, or `shared/` procedure file is modified by this task.

---
