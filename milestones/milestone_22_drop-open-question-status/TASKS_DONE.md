# TASKS DONE


## Review Skill Authors Status-Free Blocks

Rewrite step 3 of `skills/review-milestone-requirements/SKILL.md` so every finding it surfaces is authored as one ordinary three-line block whose opening tag is exactly `<open-question id="Short Title">`, deleting the "it's fine to leave some decisions to settle while doing the work" sentence, the Blocking/Deferred categories, the "do not mark something blocking if a reasonable, low-risk-to-reverse choice exists" rule, and the deferred template with no reworded threshold or pointer in their place. The shape rules state the single-physical-line opening tag plainly, dropping the id-first ordering clause and `status` from the entity-escaping rule, because the sweep and answer skills match against exactly this shape. Verified by reading the step and finding one template, no triage, and no mention of `status`.

**Verified:**

- The opening paragraph of `skills/review-milestone-requirements/SKILL.md` no longer carries the "it's fine to leave some decisions to settle while doing the work if they're better solved there" sentence; it ends at "ready enough for the work to begin."
- Step 3 contains no **Blocking** or **Deferred** category, no "Categorise each new finding" instruction, no "do not mark something blocking if a reasonable, low-risk-to-reverse choice exists" rule, and no reworded don't-raise threshold or pointer sentence in their place.
- Step 3 renders exactly one three-line template, whose opening tag is exactly `<open-question id="Short Title">`; the deferred template is gone.
- The shape rules state the single-physical-line opening tag plainly as `<open-question id="…">` carrying the double-quoted `id` attribute, with no id-first ordering clause, and the entity-escaping rule names only the `id` attribute value.
- `grep -n status` over step 3 (from `### 3.` to `### 4.`) returns nothing; the file's remaining `status`/`deferred` hits sit only in step 1 and step 5, which the sibling task "Review Skill Convergence On Any Block" owns.
- Step 3's "only annotate gaps relative to what is already written" rule survives as the pass's altitude guard.

---

## Review Skill Convergence On Any Block

Update the step 1 inventory and the step 5 report of `skills/review-milestone-requirements/SKILL.md` so the still-open list names every remaining `<open-question>` block and the convergence verdict is "ready for `/derive-tasks` only when no `<open-question>` block remains", removing the deferred carry-forward clause. This is needed because the derive-tasks precondition it mirrors no longer passes any block through. Verified by grepping the file for `status=` and `deferred` and finding nothing.

**Verified:**

- Step 1's inventory bullet in `skills/review-milestone-requirements/SKILL.md` names the `<open-question>` blocks present under `## Open questions` with no `status="open"`/`status="deferred"` qualifier.
- Step 5's "What's still open" item lists every remaining `<open-question>` block by Short Title (`id`).
- Step 5's convergence rule reads that `/derive-tasks` requires no `<open-question>` block remains, its two sub-bullets branch on any block remaining vs. none, the deferred carry-forward clause and the "noting any deferred blocks" wording are gone, and no retirement note was added in their place.
- `grep -i -E 'status=|deferred'` over the file returns nothing; the only surviving `status` hit is the "terse status line" wording in step 5.
- The diff touches only step 1's bullet and step 5's four report lines; steps 0, 2, 3, 4, the no-op paragraph, and the frontmatter are unchanged.

---
