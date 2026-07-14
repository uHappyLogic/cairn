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
