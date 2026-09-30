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

## Add One-Axis Rule To Question Authoring

Add to step 3 of `core/skills/review-milestone-requirements/SKILL.md` a third requirement on the question text — each question asks one choice, with no test named for detecting a second axis — plus the named exception that choices in one gap that constrain each other, so that not every pairing is viable, are authored as a single multi-axis question. This prevents upstream the set growth the new enumeration rules would otherwise produce on compound questions. It is verified by reading step 3 against the two Question authoring decisions with step 2's tidy-only boundary untouched, and by `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

**Verified:**

- `core/skills/review-milestone-requirements/SKILL.md` step 3's question-text requirement now carries a third requirement: each question asks one choice, and a gap holding two choices becomes two questions, one per choice.
- The same passage names the exception from the second Question authoring decision: choices in one gap that constrain each other, so that not every pairing is viable, are authored as a single multi-axis question asking both choices at once.
- The added wording names no test for detecting a second axis, matching the first Question authoring decision; the detection tests are left to the `temp/` idea document.
- Step 2 (prune, dedup, flag-on-doubt, and the never-record boundary) is unchanged: the diff under `core/` is one line, inside step 3.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/` and `hosts/antigravity/`, and `uv run scripts/build_hosts.py --check` passes.

---

## Verify One-Axis Rule With Compound Fixture

Build the small throwaway fixture milestone under `temp/` whose `requirements.md` deliberately leaves a gap holding one independent pair of axes and one coupled pair, and run `review-milestone-requirements` against it in a scratch working copy with the rebuilt plugin tree, to check the one-axis rule and its exception as authored. The run passes when it authors one question per axis for the independent pair and a single multi-axis question for the coupled pair; if it does not, revise the failing step-3 wording once (never the fixture), re-run the fixture with one run, and record any remaining shortfall while keeping the best wording. It is verified by the question set the final run authored, described in this task's record.

**Verified:**

- A throwaway fixture milestone exists under the gitignored `temp/one-axis-fixture/`: a small synthetic project whose `requirements.md` leaves one gap holding an independent pair of choices (the export file format and whether the export includes archived notes) and one gap holding a coupled pair (the on-disk storage format and the sync transport, where one pairing of the four is not viable). Nothing in it comes from the benchmark data.
- `review-milestone-requirements` ran once against the fixture in a fresh scratch git working copy under the system temp directory, headless with `--model "fable" --effort high`, with the rebuilt `hosts/claude` tree loaded through `--plugin-dir` and the installed copy of the plugin disabled; the run's init record lists the plugin at `hosts/claude` and its tool calls read only that tree.
- For the independent pair the run authored one question per axis: a question on the export file format and a separate question on whether archived notes are included.
- For the coupled pair the run authored a single multi-axis question asking both the storage format and the sync transport at once, naming why they constrain each other and that not every pairing is viable.
- Every other question the run authored (storage location, note ids across devices, sync destination setup, sync conflict behaviour) asks one choice.
- The first run passed, so the step-3 wording was not revised and no re-run was needed; there is no shortfall to record.
- The scratch working copy was deleted after its question set was read, and this repository's tracked tree is unchanged by the run: the fixture, its run script, and the run transcript stay under the gitignored `temp/`.

---
