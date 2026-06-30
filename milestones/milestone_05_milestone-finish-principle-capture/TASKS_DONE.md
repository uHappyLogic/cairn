# TASKS DONE

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

