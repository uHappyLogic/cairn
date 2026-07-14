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

