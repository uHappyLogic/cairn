# TASKS DONE

## Retire Try-Capture-Answer-Principle Skill

Delete the now-superseded `skills/try-capture-answer-principle/` directory and scrub its remaining live cross-references so nothing dangles a pointer at the deleted skill. Capture has moved to the finish-time `/capture-milestone-principle-updates` skill, so the on-demand capture skill and every live mention of it outside the doc-sync surface and the frozen records must go. Per the "Bad-principle correction path" decision, this reference cleanup is `/derive-tasks` work.

**Notes:**
- **Scope of edits — three live surfaces only:**
  1. Delete the entire `skills/try-capture-answer-principle/` directory (its `SKILL.md` and the dir).
  2. `milestones/answer_decision_principles.md` header: the sentence currently reading the file is "written **only** by `try-capture-answer-principle`" must name the new sole writer `capture-milestone-principle-updates` (exact name, authored by the "Author Capture-Milestone-Principle-Updates Skill" task) instead.
  3. `skills/try-answer-all-questions-by-principle/SKILL.md` and `skills/modify-milestone-goal/SKILL.md`: scrub every live mention of `try-capture-answer-principle`. The `try-answer-all-questions-by-principle` file has **multiple** references (its `description` frontmatter, body prose, and the "Never chain to `/try-capture-answer-principle`" invariant) — all must go, not just the invariant line. Preserve each invariant's meaning without naming a deleted skill: the sweep still never feeds its auto-answers into principle capture (its answers were already derived from a confirmed principle); `modify-milestone-goal` still records no answering principle from a goal change.
- **Do NOT touch these surfaces** (each owned elsewhere): `skills/answer-open-question/SKILL.md` (its capture-chain refs are removed by the earlier "Commit Manual Answers, Drop Capture Chain" task — leave whatever it did); `skills/reject-auto-answer/SKILL.md` (deleted wholesale by its own retirement task — its references go with it); `CLAUDE.md` and `README.md` (the single downstream doc-sync task owns all of those, including the coupled README Mermaid graph and the no-commit-invariant prose); this milestone's own `milestones/milestone_05_*/requirements.md`.
- **Do NOT rewrite frozen historical records:** leave the `milestones/README.md` history untouched and the `milestone_02`/`03`/`04` `requirements.md` + `TASKS_DONE.md` files untouched — they record what happened.
- When removing a token from a sentence the milestone has also invalidated, keep the *edited* sentence locally true — e.g. a clause listing `answer-open-question` as a skill that "leaves its edits staged" or a "taught via `answer-open-question` → `try-capture-answer-principle`" path is now stale; rephrase or pick a still-valid example for the sentence you are editing. Do **not** expand this into a staleness audit of the whole file or touch the global no-commit-invariant prose — that lives with the doc-sync task.
- This skill does not commit; leave all changes staged.

**Success:**
- `skills/try-capture-answer-principle/` no longer exists (directory and `SKILL.md` gone).
- `grep -rn "try-capture-answer-principle" skills/ milestones/answer_decision_principles.md` returns no hits **except** inside `skills/reject-auto-answer/` (handled by its own retirement task).
- The header of `milestones/answer_decision_principles.md` names `capture-milestone-principle-updates` as the file's sole writer.
- `skills/try-answer-all-questions-by-principle/SKILL.md` and `skills/modify-milestone-goal/SKILL.md` contain no occurrence of `try-capture-answer-principle`, and each still states its surviving invariant (sweep never captures its auto-answers / goal change yields no answering principle) without naming a deleted skill.
- `git diff` shows `CLAUDE.md`, `README.md`, `milestones/README.md`, and every `milestone_02`/`03`/`04` `requirements.md` and `TASKS_DONE.md` unchanged by this task.

---

## Commit Manual Answers, Drop Capture Chain

Make the `/answer-open-question` skill wrapper (`skills/answer-open-question/SKILL.md`) commit its own manual-answer edit instead of leaving it staged, and sever its unconditional chain into `/try-capture-answer-principle`. After the shared answer-recording procedure folds the decision into `## Decisions`, the skill stages only its own `requirements.md` edit and commits it with a recognizable subject and the rationale in the body — establishing the `Manual-answer:` commit convention that the later finish-time capture skill walks. Only the skill wrapper changes; `shared/answer-procedure.md` is not touched.

**Provides:**
- The manual-answer commit convention that `/capture-milestone-principle-updates` (a later task) greps for: subject line exactly `Manual-answer: <Short Title>` (colon then space — it is matched by `git log --grep='^Manual-answer: '`), the decision rationale in the commit **body**, and **no** `Answer-Principle:` trailer (its absence is the discriminator between a manual answer and a sweep auto-answer that `reject-auto-answer`'s gate relies on).

**Notes:**
- Staging is path-scoped: `git add <MILESTONE_DIR>/requirements.md` only — never `git add -A` — so the commit touches only `requirements.md` and never sweeps in unrelated working-tree changes (per the "Answer commit scope" decision; this also preserves the sweep's clean-tree precondition).
- Cold-answer body rule (per "Cold-answer commit body"): record only rationale that genuinely exists in conversation context — never prompt the user for a rationale and never fabricate one. On a cold answer the body is the answer text recorded verbatim (including any inline "because" clause); when no reasoning was stated the body holds the bare decision. The answer string is itself the cold path's rationale affordance — do not add a separate rationale prompt.
- The commit fires only when the recording actually changed `requirements.md`. The existing no-op paths — a parse error (no `.` separator) and a Short-Title mismatch (the shared procedure stops without changes) — must still produce no commit.
- This skill committing is a deliberate, documented exception to the project's "individual skills never commit" invariant; note it as such in the skill text. Reconciling the CLAUDE.md / README invariant prose is a separate downstream doc-sync task — do not edit those here.
- Do not touch `shared/answer-procedure.md`: it is shared verbatim by the autonomous sweep and must stay commit-free.

**Success:**
- `skills/answer-open-question/SKILL.md` instructs a path-scoped `git add <MILESTONE_DIR>/requirements.md` (and explicitly not `git add -A`) followed by a commit whose subject is `Manual-answer: <Short Title>`, with the decision rationale in the commit body and no `Answer-Principle:` trailer.
- `skills/answer-open-question/SKILL.md` no longer contains any reference to `try-capture-answer-principle` or any "Capture any reusable principle" step, and no longer contains the "Do not commit / leave staged" rule; surrounding text reflects that the skill now commits.
- `git diff` shows `shared/answer-procedure.md` unchanged by this task.

---

## Author Capture-Milestone-Principle-Updates Skill

Author the new optional, finish-time skill `skills/capture-milestone-principle-updates/SKILL.md` that distills reusable answering principles from this milestone's `Manual-answer:` commits into the principle store. It is the milestone's central new artifact: it carries forward the retired `try-capture-answer-principle`'s principle-entry schema and revise-vs-add discipline, but wraps them in a batch two-phase flow over a finite, known-up-front commit set. It runs as an optional follow-up *after* `/finish-current-milestone` has already cleared the current-milestone pointer to `none`.

**Provides:**
- The slash command `/capture-milestone-principle-updates`, backed by `skills/capture-milestone-principle-updates/SKILL.md`. It is the **new sole writer** of the principle store `milestones/answer_decision_principles.md` (superseding the retired `try-capture-answer-principle`).
- It writes **only** `milestones/answer_decision_principles.md` and never touches any `requirements.md`. Like other individual skills it does **not** commit — it leaves its principle-store edit **staged** for the user.
- It carries forward the principle-entry schema verbatim: each entry is a `### <Short Title>` heading + a generalizable keep/eliminate directive in prose + an optional `*Origin: …*` line; **presence = confirmed**, there is no status field.

**Notes:**
- **`skill-creator` is the mandated authoring tool.** The milestone goal requires this skill be created via the `/skill-creator:skill-creator` skill — invoke it to scaffold and author `SKILL.md`; do not hand-write the skill outside that tool. State plainly in the skill text that this skill commits nothing and leaves its edit staged.
- **Target resolution (per "Finish-time recommendation"):** because the current-milestone pointer is already `none` when this skill runs, it must **not** resolve `<MILESTONE_DIR>` via `shared/get-current-milestone.md`. Instead it resolves `<MILESTONE_DIR>` from the **last row of the `## Completed Milestones` table** in `milestones/README.md` (the row `/finish-current-milestone` just appended), and feeds that same path into the commit walk.
- **Commit walk (per "Commit-walk boundary"):** `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md`. The path filter is itself the lower boundary (that file does not exist before the milestone was defined), so no milestone-start marker is needed. As a guard, exclude any matched commit carrying an `Answer-Principle:` trailer — those are sweep auto-answers, not manual answers.
- **Two-phase interaction model (per "Batch capture interaction model"):** (1) **Internal candidate elimination first** — extract candidate keep/eliminate directives from all in-range `Manual-answer` commit bodies, drop the non-generalizable ones, and cluster the surviving candidates **against each other** (cross-candidate dedup; the commit→principle mapping is many-to-many). (2) **Then strongest-first user confirmation against the live store** — present surviving candidates strongest-first; confirmation granularity is **per-candidate at write time** (never grouped-per-round): for each candidate run revise-vs-add by semantic overlap against the **live** store, take the user's add/revise/decline, write that one, then **re-scan** the remaining pool before the next (a write can turn a later candidate's "add" into a "revise"). It **may** optionally display the full surviving pool up front for context, but writes one candidate at a time.
- **Termination is deterministic:** the candidate pool is the finite, known-up-front set of in-range commits; the loop ends when every commit's rationale has been considered and every surviving candidate is resolved (add/revise/decline) with no pending merges.
- **Empty range is a normal exit, not a branch (per "Empty commit range"):** when the walk returns no qualifying commits, report a single line that there are no `Manual-answer` commits in range to distill, and exit writing/staging nothing. This is the **same** terminal "nothing captured" report the candidate-elimination flow produces when in-range commits exist but none generalize — the two converge on one report rather than a distinct empty-range branch.
- This task only authors the new skill. Retiring `try-capture-answer-principle` and reconciling the CLAUDE.md / README references (including the principle-store header's writer-attribution line) is downstream work — do not do it here.

**Success:**
- `skills/capture-milestone-principle-updates/SKILL.md` exists (authored via `/skill-creator:skill-creator`, per Notes).
- The skill resolves `<MILESTONE_DIR>` from the last row of the `## Completed Milestones` table in `milestones/README.md` (explicitly **not** via `shared/get-current-milestone.md`), and walks `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md`, excluding commits that carry an `Answer-Principle:` trailer.
- The skill text describes the two-phase flow: internal cross-candidate dedup, then strongest-first **per-candidate** revise-vs-add against the live store with a re-scan of the remaining pool after each write.
- The skill carries forward the `### <Short Title>` + prose keep/eliminate directive + optional `*Origin: …*` entry schema, with presence meaning confirmed and no status field.
- The skill treats an empty commit range as a single-line "nothing to distill" exit that converges with the "commits exist but none generalize" report, writing and staging nothing.
- The skill writes only `milestones/answer_decision_principles.md`, never touches any `requirements.md`, and does not commit (leaves its edit staged).

---

## Recommend Capture Skill At Finish

Update `/finish-current-milestone` (`skills/finish-current-milestone/SKILL.md`) so its step 8 ("Confirm") surfaces a recommendation to run the new `/capture-milestone-principle-updates` skill as an optional follow-up. Per the "Finish-time recommendation" decision, the recommendation is **RECOMMENDED, never auto-run**: step 8 only adds the suggestion text — the skill must not invoke the new skill and must not commit. The two next-step suggestions must be ordered `/capture-milestone-principle-updates` first (the milestone just closed) then `/define-milestone-goal` (the next one). No other step of the skill changes.

**Notes:**
- The recommendation belongs in **step 8** specifically, which already runs **after** the `## Completed Milestones` table-row append (step 5) and the pointer-clear to `none` (step 6) — so nothing moves; the change is purely adding the ordered suggestion to step 8. The reason it cannot fire earlier: `/capture-milestone-principle-updates` resolves its target `<MILESTONE_DIR>` from the **last row of the `## Completed Milestones` table**, which step 5 only just appended.
- Use a plain suggestion line worded as optional/recommended, e.g. "Optional: run `/capture-milestone-principle-updates` to distill reusable answering principles from this milestone's recorded decisions into the principle store."
- The brief names step 8 **and its Rules** as the affected surface. The Rules section (currently silent on the next-step suggestion) is the natural home for a guard such as "`/finish-current-milestone` only *suggests* `/capture-milestone-principle-updates` — it never invokes it and never commits." Add that guard rather than leaving the no-auto-run/no-commit constraint implicit.

**Success:**
- Step 8 of `skills/finish-current-milestone/SKILL.md` lists `/capture-milestone-principle-updates` (worded as optional/recommended) **before** `/define-milestone-goal` in its closing next-step suggestion.
- Step 8 contains no Skill/slash invocation that actually *runs* `/capture-milestone-principle-updates` and no `git commit` instruction — the change adds suggestion text only.
- The Rules section carries a guard stating `/finish-current-milestone` only suggests the new skill and never invokes it or commits.
- No step other than step 8 (and the Rules guard) is altered.

---

## Retire Reject-Auto-Answer Skill

Delete the now-retired `skills/reject-auto-answer/` directory and scrub its remaining live cross-references in other skill files so nothing dangles a pointer at the deleted skill. Per the "Bad-principle correction path" decision, `reject-auto-answer` is retired entirely with no dedicated replacement: correcting a bad auto-answer becomes the uniform "revert the auto-answer commit, then `/answer-open-question` to re-answer" flow, with the offending principle reconciled at milestone finish. This reference cleanup is `/derive-tasks` work.

**Notes:**
- **Scope of edits — one dir deleted, one file scrubbed:**
  1. Delete the entire `skills/reject-auto-answer/` directory (its `SKILL.md` and the dir; its own self-references go with it).
  2. `skills/try-answer-all-questions-by-principle/SKILL.md` has the two surviving live mentions (run `grep -rn "reject-auto-answer" skills/` to confirm). Both must go, but **preserve the still-true invariant prose** around each — the sweep still commits one auto-answer per commit and still prints `git log <BASE>..HEAD`, and each auto-answer is still individually traceable and revertible; only the pointer to the retired correction skill changes.
- **The line that points the user at `/reject-auto-answer` to undo a bad answer is a redirect, not a plain deletion.** Per the "Bad-principle correction path" decision, repoint it at the uniform replacement flow — revert the offending auto-answer commit, then run `/answer-open-question` to re-answer — so the "here's how to undo a bad answer" affordance survives the rename rather than silently vanishing. The other mention (the traceability/reversibility claim) stays true once the skill name is dropped.
- **Do NOT touch these surfaces** (each owned elsewhere): `skills/try-capture-answer-principle/SKILL.md` — that skill is deleted by its own "Retire Try-Capture-Answer-Principle Skill" task, sequenced **before** this one, so it should already be gone; do not recreate or edit it (if a mid-task grep still shows its refs, that is the prior task's domain, not a gap here). `CLAUDE.md` and `README.md` — the single downstream doc-sync task owns all of those, including the coupled README Mermaid graph and the no-commit-invariant prose. This milestone's own `milestones/milestone_05_*/requirements.md`.
- **Do NOT rewrite frozen historical records:** leave the `milestones/README.md` history untouched and the `milestone_02`/`03`/`04` `requirements.md` + `TASKS_DONE.md` files untouched — they record what happened.
- This skill does not commit; leave all changes staged.

**Success:**
- `skills/reject-auto-answer/` no longer exists (directory and `SKILL.md` gone).
- `grep -rn "reject-auto-answer" skills/` returns no hits.
- `skills/try-answer-all-questions-by-principle/SKILL.md` no longer names `reject-auto-answer`, yet still states the auto-answers are individually traceable/reversible and still tells the user how to undo a bad answer — now via the revert-then-`/answer-open-question` flow.
- `git diff` shows `CLAUDE.md`, `README.md`, `milestones/README.md`, this milestone's own `requirements.md`, and every `milestone_02`/`03`/`04` `requirements.md` and `TASKS_DONE.md` unchanged by this task.

---

## Sync CLAUDE.md And README To New Capture Model

Reconcile the two root documentation files — `CLAUDE.md` and root `README.md` — to the milestone's new reality, now that all the underlying skill changes are done by the earlier tasks. This is the **last** task and the **sole owner** of every `CLAUDE.md`/`README.md` edit in this milestone, so one completer holds the coupled README Mermaid graphs in view at once. The new reality to reflect: (a) `/answer-open-question` now commits its manual-answer edit (subject `Manual-answer: <Short Title>`, rationale in the body, no `Answer-Principle:` trailer) and no longer chains to capture; (b) a new skill `capture-milestone-principle-updates` exists — an optional finish-time skill, recommended by `/finish-current-milestone`, that distills principles from `Manual-answer:` commits into the principle store and is its new sole writer; (c) `try-capture-answer-principle` and `reject-auto-answer` are both retired (deleted), the latter's correction role replaced by the uniform "revert the auto-answer commit, then `/answer-open-question` to re-answer, principle reconciled at finish" flow.

**Notes:**
- **README is a grep-and-edit pass; CLAUDE.md requires rewriting invariant PROSE.** A grep-and-delete sweep of `CLAUDE.md` misses invariants that never name the retired skills — those must be located by meaning and rewritten, not just name-stripped.
- **README diagrams (per milestone 4, the README is six per-phase `flowchart TD` diagrams wired through shared `D0`–`D5` seam nodes):**
  - "Iterating milestone requirements" diagram: remove the `try-capture-answer-principle` node (`ITM5`) and the `reject-auto-answer` node (`ITM6`), and fix every edge that touched them so no dangling edges remain and the `D0`–`D5` seam wiring stays intact. Update that diagram's lead-in prose paragraph (it currently names both retired skills and the auto-capture chain).
  - "Ending a milestone" diagram: add a `capture-milestone-principle-updates` node (the optional finish-time follow-up `/finish-current-milestone` recommends), wired consistently with the existing seam/style conventions.
- **README `## Skill reference`:** delete the `### try-capture-answer-principle [...]` and `### reject-auto-answer [...]` subsections; add a new `### capture-milestone-principle-updates` subsection describing the finish-time distillation skill; update `### answer-open-question` (currently says it chains to `/try-capture-answer-principle`) to state it now records AND commits the answer and no longer chains to capture; and update the `### The answer-principle-learning loop` prose block (its "Manual teaching flow" and "Correction loop" bullets name the retired skills and the auto-chain) to the new model — manual answers are committed with rationale, principles are distilled at milestone finish by `capture-milestone-principle-updates`, correction is revert-then-re-answer.
- **CLAUDE.md `## Repository layout` + skills-overview/pipeline listing:** remove `try-capture-answer-principle` and `reject-auto-answer`; add `capture-milestone-principle-updates` (finish-time principle-distillation skill, new sole writer of the principle store, recommended by `finish-current-milestone`).
- **CLAUDE.md `## Invariants to preserve` — reconcile every invariant this milestone makes false (rewrite, do not merely name-strip):**
  - The "Two orchestrators commit; individual skills never commit" invariant is now FALSE for `answer-open-question` — rewrite it to record that `answer-open-question` is a deliberate, documented exception that commits exactly its own path-scoped `requirements.md` manual-answer edit (subject `Manual-answer: <Short Title>`, rationale in body, no `Answer-Principle:` trailer).
  - The invariant that `answer-open-question` unconditionally chains to `try-capture-answer-principle` — remove/replace it (the chain is severed; capture moved to finish time).
  - The entire `reject-auto-answer` invariant paragraph — remove it; where the "bad auto-answer" correction is described, replace with the revert-then-`/answer-open-question` flow with finish-time principle reconciliation.
  - Add invariant(s) for the new skill as warranted: it resolves `<MILESTONE_DIR>` from the last `## Completed Milestones` row (NOT `get-current-milestone`); path-scoped `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md` commit walk excluding `Answer-Principle:`-trailer commits; new sole writer of the principle store; recommended-not-auto-run at finish.
  - Update the principle-store sole-writer attribution wherever `CLAUDE.md` states it (now `capture-milestone-principle-updates`).
- **Frozen records and other files are off-limits:** do NOT edit `milestones/README.md` history, the `milestone_02`/`03`/`04` `requirements.md`/`TASKS_DONE.md`, this milestone's own `milestone_05` `requirements.md`, or any `skills/**/SKILL.md` or `shared/**` file — those are owned by the earlier tasks. This task edits only `CLAUDE.md` and root `README.md`.
- This skill does not commit; leave all changes staged.

**Success:**
- `grep -rn "try-capture-answer-principle\|reject-auto-answer" CLAUDE.md README.md` returns no hits.
- Both `CLAUDE.md` and `README.md` reference `capture-milestone-principle-updates`.
- The README's six `flowchart TD` diagrams have no dangling edges and the `D0`–`D5` seam chain is intact; the "Ending a milestone" diagram contains a `capture-milestone-principle-updates` node and the "Iterating milestone requirements" diagram no longer contains the `ITM5`/`ITM6` nodes.
- `CLAUDE.md`'s no-commit invariant and the chain-to-capture invariant are rewritten (not merely name-stripped), and the `reject-auto-answer` invariant paragraph is gone.
- The `answer-open-question` description in both `README.md` and `CLAUDE.md` states it commits its manual-answer edit and no longer chains to capture.
- `git diff` shows `milestones/README.md`, this milestone's own `requirements.md`, every `milestone_02`/`03`/`04` `requirements.md` and `TASKS_DONE.md`, and every `skills/**/SKILL.md` and `shared/**` file unchanged by this task.

---

