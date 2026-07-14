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

