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
