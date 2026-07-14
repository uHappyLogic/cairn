# TASKS DONE

## Terse Reporting: Milestone-Lifecycle Skills

Cut the success-path reporting of the four milestone-lifecycle skills — `define-milestone-goal`, `specify-milestone-starting-state`, `goto-next-milestone`, and `modify-milestone-goal` — to a single fixed terse status line, removing each one's prose summary and next-step handoff pointer. Each also gains a distinct one-line no-op message for when its commit's dirty-own-path guard fires. This applies the milestone's terse-reporting decisions to this group of `SKILL.md` files.

**Notes:**
- Terse line shape (per the "Terse status line shape" decision): a fixed sentence carrying no identifier — no milestone id, count, or commit subject. Concrete choices to use: `define-milestone-goal` step 6 → "Milestone defined."; `specify-milestone-starting-state` step 7 → "Starting state recorded."; `goto-next-milestone` step 5 → "Milestone activated."; `modify-milestone-goal` step 6 → "Goal revised." Delete the prose-summary bullets and the "Suggest the next step" / "Recommended next step" handoff pointer from each of these success steps.
- No-op case (per the "No-op pass reporting" decision): when the shared commit procedure's dirty-own-path guard fires (the pass changed no files, so nothing was committed), the step must instead print a concise one-line message stating that nothing changed and briefly why — distinct from the terse success line, because git holds no durable record of a no-op.
- Boundary — leave every failure/clean-stop message untouched: `define-milestone-goal` step 3's conflict stop; `specify-milestone-starting-state` step 1's not-found stop and step 3's `/init` suggestion; `goto-next-milestone` steps 1–2's prerequisite / "none" / candidate-selection stops. Only the final success-report step of each skill changes.
- `modify-milestone-goal` step 6 currently also surfaces a before→after and a downstream-impact analysis; it collapses fully to the terse line too. This skill is deliberately not among the ones the "Non-redundant advisory output" decision keeps advisory output for (those are `review-milestone-requirements`, `derive-tasks`, and the answer skills — all outside this task). Its "surface, never cascade" analysis body (steps 3–5) and its Rules stay unchanged; only the step-6 output collapses.
- No file-writing or commit behavior changes; edit each `SKILL.md` inline (no shared reporting-convention file is introduced).

**Success:**
- In each of the four `SKILL.md` files, the final `## Workflow` step's success path instructs printing exactly one fixed terse status line with no identifier and no next-step/handoff pointer.
- Each of those four final steps also instructs a distinct one-line no-op message, triggered when the dirty-own-path guard fires, that states nothing changed and briefly why.
- The strings "Suggest the next step" and "Recommended next step", and the per-item prose-summary bullets, no longer appear in those four success steps.
- `define-milestone-goal` step 3, `specify-milestone-starting-state` steps 1 and 3, and `goto-next-milestone` steps 1–2 retain their existing failure/clean-stop wording unchanged; every file-creation/edit and commit step across the four skills is unchanged.
- No new file is created under `shared/`.

---

## Terse Reporting: Answer Skills

Cut the success-path reporting of the three answer skills — `answer-open-question`, `answer-open-question-with-recommendation`, and `answer-open-question-with-alternative` — to a single fixed terse status line, removing the prose re-narration of which question resolved, how the document changed, and cascade details. Per the milestone's "Non-redundant advisory output" decision, keep the one piece of genuinely git-absent advisory output — the note about newly-exposed open questions — alongside the terse line. Each step also gains a distinct one-line no-op message for when its commit's dirty-own-path guard fires. This applies the milestone's terse-reporting decisions to the answer-skill group of `SKILL.md` files.

**Notes:**
- The final reporting step in each skill: `answer-open-question` step 5 "Report findings", `answer-open-question-with-recommendation` step 3 "Report findings", `answer-open-question-with-alternative` step 6 "Report findings". Only these steps change.
- Terse line shape (per the "Terse status line shape" decision): a fixed sentence carrying no identifier — no Short Title, no commit subject. A concrete choice to use across all three: "Answer recorded." Delete the "which question was resolved and how the document changed (resolved block, decision folded into `## Decisions`, cascading resolutions)" re-narration bullet — and, for `answer-open-question-with-alternative`, also the "which alternative you recorded (id + how it read)" clause — since the committed diff and git log are the durable record of that.
- Non-redundant advisory (per the "Non-redundant advisory output" decision): retain each step's "Any new open questions the recorded decision may have introduced — surface these but do **not** add them to the document without user confirmation" note beside the terse line. This is decision-critical information the commit never captured, so it stays. The two `with-…` skills' trailing "Then stay available…" follow-up sentence also stays (it is not diff re-narration).
- No-op case (per the "No-op pass reporting" decision): when the shared commit procedure's dirty-own-path guard fires (the pass changed no files, so nothing was committed), the step must instead print a concise one-line message stating that nothing changed and briefly why — distinct from the terse success line, because git holds no durable record of a no-op. For these skills the guard fires on the clean-stop cases each already documents (Short-Title mismatch, missing `<recommendation>`/`<alternative>` element, the retired-sentinel redirect, a parse error).
- Boundary — leave every failure/clean-stop message untouched: `answer-open-question`'s step 1 parse-error message, its step 2 retired-sentinel redirect guard pointing at `/answer-open-question-with-recommendation`, and its step 3 Short-Title-mismatch relay; `answer-open-question-with-recommendation`'s step 1 no-`<recommendation>`-element / missing-block clean-stop-and-point; `answer-open-question-with-alternative`'s step 2 guard (no matching question id, no `<alternative>` elements, no matching alternative id, each listing the available ids). Every skill's `## Rules` section is also unchanged.
- No file-writing or commit behavior changes; edit each `SKILL.md` inline (no shared reporting-convention file is introduced).

**Success:**
- In each of the three `SKILL.md` files, the final reporting step's success path instructs printing exactly one fixed terse status line with no identifier, followed only by the newly-exposed-open-questions advisory note.
- The re-narration of the resolved block, the decision folded into `## Decisions`, and the cascading resolutions no longer appears in those three success steps; `answer-open-question-with-alternative`'s "which alternative you recorded" clause is likewise gone.
- Each of those three steps also instructs a distinct one-line no-op message, triggered when the dirty-own-path guard fires, that states nothing changed and briefly why.
- `answer-open-question` step 1's parse-error message, step 2's retired-sentinel redirect guard (still pointing at `/answer-open-question-with-recommendation`), and step 3's Short-Title-mismatch relay are unchanged; the missing-element and Short-Title clean stops in the other two skills are unchanged; every record/commit step and every `## Rules` section across the three skills is unchanged.
- No new file is created under `shared/`.

---

## Terse Reporting: Review-Milestone-Requirements

Cut the success-path reporting of `review-milestone-requirements` step 5 "Report convergence" to a single fixed terse status line, removing the "What changed this pass" prose re-narration and the handoff pointers to `/discuss-open-question` and `/answer-open-question`. Per the milestone's "Non-redundant advisory output" decision, keep the genuinely git-absent, decision-critical output — the convergence verdict (whether the document is ready for `/derive-tasks`) and the list of still-open questions — alongside the terse line. The step also gains a distinct one-line no-op message for when the step-4 commit's dirty-own-path guard fires. This applies the milestone's terse-reporting decisions to `review-milestone-requirements`, this skill's flagship no-op-pass case.

**Notes:**
- Only step 5 "Report convergence" changes. Terse line shape (per the "Terse status line shape" decision): a fixed sentence carrying no identifier — no milestone id, count, or commit subject; a concrete choice to use is "Requirements reviewed."
- Delete the "What changed this pass" bullet (blocks pruned with covering decision cited, repeats merged, new questions raised, "possibly resolved — confirm" flags) — that reshaping is exactly the committed diff the terse cut targets — and remove the "one-line nudge toward `/discuss-open-question` or `/answer-open-question`" handoff pointer from the "What's still open" bullet.
- Non-redundant advisory (per the "Non-redundant advisory output" decision): keep the still-open list (remaining `status="open"` blocks by Short Title / `id`) and keep the full **Convergence** verdict — the `no status="open"` blocks remaining → ready-for-`/derive-tasks` rule, and the deferred-blocks-may-carry-forward note. This is decision-critical state the commit never captures, so it stays beside the terse line.
- No-op case (per the "No-op pass reporting" decision): step 4 already documents this as "the milestone's flagship no-op-pass case" — when the step-4 dirty-own-path guard fires (a pass that reconciled, pruned, and surfaced nothing, so `requirements.md` is unchanged and nothing was committed), step 5 must instead print a concise one-line message stating that nothing changed and briefly why — distinct from the terse success line, because git holds no durable record of a no-op.
- Boundary — every document-editing step is untouched: step 2 (reconcile/prune/dedup), step 3 (surface new gaps / author `<open-question>` blocks), and step 4 (the commit and its shared-procedure reference) are unchanged, as is the `## Rules` section. Only step 5's console output changes.
- No file-writing or commit behavior changes; edit `skills/review-milestone-requirements/SKILL.md` inline (no shared reporting-convention file is introduced).

**Success:**
- `review-milestone-requirements` step 5's success path instructs printing exactly one fixed terse status line with no identifier, followed only by the still-open list and the convergence verdict; the "What changed this pass" bullet and the `/discuss-open-question` / `/answer-open-question` handoff pointers no longer appear in step 5.
- Step 5 also instructs a distinct one-line no-op message, triggered when the step-4 dirty-own-path guard fires, that states nothing changed and briefly why.
- Steps 0–4 and the `## Rules` section of `skills/review-milestone-requirements/SKILL.md` are unchanged — every reconcile, surface, prune, authoring, and commit instruction is byte-for-byte intact.
- No new file is created under `shared/`.

---

## Terse Reporting: Task And Principle-Capture Skills

Cut the success-path reporting of the three task-level and principle-capture skills — `submit-task`, `complete-task`, and `capture-milestone-principle-updates` — to a single fixed terse status line, removing the prose summary of what was authored/completed/distilled and every next-step/follow-up pointer. Each step also gains (or, for `capture`, keeps) a distinct one-line no-op message for when its commit's dirty-own-path guard fires. This applies the milestone's terse-reporting decisions to the task-level/capture group of `SKILL.md` files; the same-named dispatched agents under `agents/` (which return structured `DONE`/`FAILED` to an orchestrator, not console output) are out of scope.

**Notes:**
- The final reporting step in each skill: `submit-task` step 6 "Confirm", `complete-task` step 3 "Hand back", `capture-milestone-principle-updates` step 6 "Report". Only these steps change.
- Terse line shape (per the "Terse status line shape" decision): a fixed sentence carrying no identifier — no task title, no principle Short Title, no commit subject. Concrete choices to use: `submit-task` → "Task submitted."; `complete-task` → "Task completed."; `capture-milestone-principle-updates` → "Principles captured." Delete the prose summaries: `submit-task`'s task-title-and-insert-position line; `complete-task`'s "summarize what you completed, how you verified it, and the commit you made"; `capture`'s per-principle Short-Title + add/revision recap. Delete the follow-up pointers too: `capture`'s "now available to the recommendation advisor (`/discuss-open-question` and `/recommend-all-open-questions`)" pointer.
- These three skills are **not** among the ones the "Non-redundant advisory output" decision keeps advisory output for (those are `review-milestone-requirements`, `derive-tasks`, and the answer skills — all outside this task), so their success paths collapse fully to the terse line. In particular: `submit-task`'s success-path "if the atomic-scope rule left a second buildable piece unauthored, mention it and offer to queue it" clause and its "stay available…" invitation, and `complete-task`'s "stay available…" invitation, are part of the success narration that collapses — none is a preserved advisory. (The context-stays-for-follow-up behavior is unchanged; only the printed sentence goes.)
- No-op case (per the "No-op pass reporting" decision): when the shared commit procedure's dirty-own-path guard fires (the pass changed no files, so nothing was committed), the step must print a concise one-line message stating that nothing changed and briefly why — distinct from the terse success line, because git holds no durable record of a no-op. For `capture` this is its **existing** single-line "nothing to distill" report (the empty commit range / none-generalize / user-declined-every-candidate convergence at step 6); keep it as the distinct one-line no-op message rather than collapsing it into "Principles captured." For `submit-task` and `complete-task` the guard fires on the defensive no-file-change case each already documents (a completion abandoned before it touched any file; an insert that authored nothing).
- Interactive mid-workflow conversation is not success reporting and is untouched: `capture`'s step 4 phase-2 per-candidate revise-vs-add confirmation dialogue with the user (including any optional up-front pool preview) stays exactly as is — only the final step-6 report goes terse.
- Boundary — leave every failure/clean-stop message untouched: `submit-task` step 2's duplicate stop and out-of-scope redirect, and step 6's "could not author a concrete task — suggest `/discuss-new-task`" fallback; `complete-task` step 1's no-matching-task stop that lists the available `##` headings; `capture` step 1's pointer-resolution, step 2's empty-range exit, and step 3's none-generalize exit as preconditions. Every skill's `## Rules` section is also unchanged.
- No file-writing or commit behavior changes; edit each `SKILL.md` inline (no shared reporting-convention file is introduced).

**Success:**
- In each of the three `SKILL.md` files, the final reporting step's success path instructs printing exactly one fixed terse status line with no identifier and no next-step/follow-up pointer.
- The per-item prose summaries no longer appear on those success paths: `submit-task`'s task-title-and-position line and its atomic-scope-leftover offer; `complete-task`'s what/how/commit summary; `capture`'s per-principle add/revision recap and its recommendation-advisor pointer.
- Each of the three steps instructs a distinct one-line no-op message, triggered when the dirty-own-path guard fires, that states nothing changed and briefly why; for `capture` this is its existing single-line "nothing to distill" report, kept distinct and not collapsed into the terse success line.
- Failure/clean-stop wording is unchanged: `submit-task` step 2's triage stops and step 6's "could not author / suggest `/discuss-new-task`" fallback; `complete-task` step 1's no-matching-task stop; `capture` steps 1–3's preconditions; and `capture` step 4's interactive revise-vs-add dialogue.
- Every file-creation/edit and commit step across the three skills is unchanged, and no new file is created under `shared/`.

---

