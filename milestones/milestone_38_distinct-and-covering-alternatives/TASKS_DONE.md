# TASKS DONE

## Rewrite Alternatives Procedure Enumeration Step

Rewrite step 2 of `core/shared/alternatives-procedure.md` under the milestone's Enumeration rules decisions: a mandatory axes-first move (premises and degree or parameter values treated as axes, every combination weighed in reasoning on a multi-axis question and each viable one described), distinctness and coverage as the tests the set must pass, the separate instruction to weigh not doing the thing (postponing folded into it as at most one option), the what-it-is field bounded by content instead of one sentence, the sibling-owned-axis condition in the drawback, and no count guideline. This is the milestone's core change, the rule set every later task verifies or documents. It is verified by reading the rewritten step against each Enumeration rules decision with step 1 and the no-preference rule intact, and by `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

**Verified:**

- Step 2 of `core/shared/alternatives-procedure.md` opens with a mandatory axes-first move: the axes of the underlying decision are named before any option is drafted, and the options are built as positions on them, as combinations weighed in reasoning with each viable one described on a multi-axis question.
- A degree or parameter value is treated as an axis whose values are the points where the key advantage or drawback genuinely changes, with same-trade-off values merged into one described by its range; each premise the wording takes for granted is an axis with accepting and rejecting as its values.
- Distinctness (every two options differ in substance on at least one axis) and coverage (the set covers the underlying decision, every viable position on every axis and the not-doing direction where viable) are stated as the two tests the set must pass.
- A separate instruction weighs not doing the thing on every question, listed only when honestly viable with no note that it was weighed, and postponing is folded into it as at most one option that says whether it means never or later.
- The what-it-is field holds only the option's position on each axis, with reasons for or against moved to the advantage and drawback fields and its length following from the positions, with no sentence limit.
- No option takes a position on a sibling-owned axis, and the drawback names any sibling-owned axis the option's viability depends on as a condition without naming the expected outcome.
- The step carries no count guideline: "typically two to four" and "one sentence" are gone and the set's size follows only from its axes and viable combinations.
- Step 1 and the opening statement that nothing in the procedure forms a preference are unchanged (the diff starts inside step 2).
- `uv run scripts/build_hosts.py --check` passes on the rebuilt `hosts/claude/` and `hosts/antigravity/` trees.

---

## Align Enumeration Restatements With Rewritten Procedure

Bring the two runtime restatements of step 2 into line with the rewritten procedure: `core/agents/provide-alternatives-to-open-question.md` stops calling the first field a sentence, and `core/skills/discuss-open-question/SKILL.md` step 3 drops its "2–4" count, each deferring to the procedure rather than restating its rules. Without this the subagent and the inline runner would still carry the retired count and length limits beside the new rules. It is verified by a search of `core/` finding no count guideline and no one-sentence limit on alternatives, and by `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

**Verified:**

- `core/agents/provide-alternatives-to-open-question.md` no longer calls the first field a sentence: its rendering step carries "the what-it-is text as the element's own text", and its self-check routes each bearing fact into whichever field the shared procedure gives it rather than restating the field rules.
- `core/skills/discuss-open-question/SKILL.md` step 3 no longer states "2–4": a bare block's options are enumerated "as that procedure lays them out", deferring to `alternatives-procedure.md` for the set's rules.
- A search of `core/` for count guidelines and one-sentence limits on alternatives (`2–4`, `two to four`, `2 to 4`, `typically two`, `what-it-is sentence`, `one sentence`) finds none applying to alternatives; the remaining hits are unrelated (the Short Title's 2–5 word handle and one-sentence restatements in other skills).
- `uv run scripts/build_hosts.py --check` passes on the rebuilt `hosts/claude/` and `hosts/antigravity/` trees.

---
