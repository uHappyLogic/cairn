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

## Write Pre-Split Case Conversion Script

Write the one throwaway conversion script under `temp/` that prepares a scratch clone of a milestone predating `open_questions.xml`: it creates the empty document in the milestone directory, turns every question of the open-questions section of `requirements.md` into a bare block through the tool's `add` (the historical Short Title and question text only), deletes that section, and commits the converted state inside the clone. The re-run check needs it so pre-split and post-split cases run through the unchanged alternatives pass alike and count in one tally. It is verified by running it in a scratch clone checked out at a pre-split commit and confirming the tool's `list` prints that milestone's questions, the section is gone from `requirements.md`, and the source repository is untouched.

**Verified:**

- The script exists as `temp/convert_presplit_case.py` under the gitignored `temp/` (`git check-ignore` names the `temp/` rule), taking the scratch clone and the milestone directory as arguments, so `git status` shows nothing new to commit from it.
- It creates `open_questions.xml` holding the empty canonical document (`<open-questions/>` and a newline), then adds each historical question as a bare block through `open_questions.py add` of the rebuilt `hosts/claude` tree, passing only the historical Short Title and the question text on stdin; no historical alternative or recommendation enters the document.
- It reads both historical question layouts: XML blocks inside the `## Open questions` section (with or without the retired `status` attribute) and the older Markdown blockquotes opening `**Open question — <Title>:**` or `**Deferred — <Title>:**`, including those the oldest layout kept inline in other sections, whose alternatives and recommendation would otherwise stay readable in `requirements.md`.
- It deletes the `## Open questions` section and every question blockquote from `requirements.md`, then commits exactly `open_questions.xml` and `requirements.md` inside the clone under a `Pre-split conversion: <milestone directory>` subject.
- Run in scratch clones under the system temp directory checked out at the parents of three pre-split answer commits (one per layout: XML section, blockquote section, inline blockquotes with no section), the tool's `list` printed each milestone's historical questions in document order, the answered question among them; `requirements.md` held no `## Open questions` heading, question block, or question blockquote afterwards, the rest of the file unchanged; each clone's tree was clean with the conversion commit on top.
- Its parser, run over the pre-split parent `requirements.md` of every pre-split case the re-run check can draw from, found at least one question in each, found the answered question's Short Title in each, and left no question marker behind.
- It refuses a work tree outside the system temp directory (tried on a source repository: it stopped on its `Error:` line), a dirty tree, and a milestone that already has `open_questions.xml`; the source repositories' `HEAD` and status were identical before and after the runs, and every scratch clone was deleted.

---

## Fix Re-Run Cases And Control Sample

Fix, in an uncommitted manifest under `temp/`, the cases the re-run check will use: all 20 historical cases rated strong candidates (16 where the answer took a direction no option represented, 4 where it took a combination on an axis the set never laid out) and a control sample of eight to ten refinement overrides picked by a stratified seeded draw, with the grouping features (source project, how many alternatives the historical set held, and whether its judged verdict flagged near-duplicates) fixed before the draw and the seed fixed before any run. Fixing the selection first keeps it independent of every run's outcome. It is verified by the manifest holding exactly those counts with every group represented and by the draw reproducing under its recorded seed, with nothing from the benchmark data entering a committed file.

**Verified:**

- An uncommitted manifest exists under `temp/` (`temp/rerun-check/manifest.json`, written by `temp/rerun-check/draw_cases.py`), and `git status` shows nothing new to commit from it because `temp/` is gitignored.
- The manifest holds exactly 20 re-run cases, all the strong candidates and nothing else: 16 where the answer took a direction no option represented and 4 where it took a combination on an axis the set never laid out.
- The manifest holds a control sample of 10 refinement overrides, within the eight-to-ten bound, drawn from the 65 deduplicated refinement overrides.
- The grouping features (source project, size of the historical alternative set, and the judged near-duplicate flag) and their bins are fixed as constants in the draw script before the draw, yielding 9 non-empty groups, and every group is represented by at least one drawn control case.
- The seed is recorded in the manifest before any run, and re-running the draw in verify mode under that seed reproduces the recorded re-run and control selection exactly, under both the system `python3` and Python 3.9.
- Every selected case resolves read-only to an answer commit and its parent in its source repository, with its milestone directory and pre-split status recorded; no source repository was written to.
- No committed file carries any case, project, question, or commit detail from the benchmark data; the only committed change is this task-list move with aggregate counts.

---

## Run Paired Alternatives Re-Run Check

Run the one-off check over the fixed re-run and control cases: each case in a scratch clone outside this working copy at the parent of its answer commit (converted first where pre-split), the alternatives pass run back to back under the unchanged `alternatives-procedure.md` from the commit before the rewrite and under the new rules, both with `--model "opus"` at `--effort high`, and a separate blind judge agent deciding recovery of the missing direction and both control tests for each rule version's set. The change counts as verified when the new rules recover the missing direction in at least 5 more of the 20 re-run cases than the baseline, net of the paired cases they win minus those they lose, and fail no more control cases than the baseline; on a shortfall, revise the enumeration wording once and re-run the check, and record the aggregate shortfall if it persists. It is verified by the recovered-direction counts, the baseline counts, the margin, and the control outcomes recorded as aggregates only in this task's `**Verified:**` bullets, with every clone deleted, the source repositories only read, and no benchmark or private-project information in any committed artifact.

**Verified:**

- Every case ran in a scratch clone under the system temp directory holding only the history up to the parent of its answer commit (a fetch of that one commit, so the answer and everything after it were absent); pre-split cases were converted there by `temp/convert_presplit_case.py`, and post-split cases had the case question emptied with the tool's bare `strip` and committed inside the clone.
- The baseline ran on the `hosts/claude` tree of the commit before the rewrite (the task-derivation commit preceding `Task-completion: Rewrite Alternatives Procedure Enumeration Step`), whose only differences from the new tree are the enumeration files; the new rules ran on this working copy's rebuilt `hosts/claude`. Each version's tree was loaded explicitly with the installed copy of the plugin disabled.
- On each case the per-question `cairn:provide-alternatives-to-open-question` agent ran with the pass's exact two-value dispatch prompt, its return judged by the pass's pipeline (last-line verdict, `embed --alternatives`, one repair by continuing the same session); every one of the 120 runs across both rounds embedded a set, 9 of them after their single repair.
- All 20 re-run cases and all 10 control cases ran under both rule versions back to back with `--model "opus"` at `--effort high`, and every run's init record names the same model release.
- A separate blind judge agent, run headless per brief in a fresh context with no tools and one fixed instruction set, judged each set from only the historical answer, the recorded missing direction or the refined listed option, and that one set, under shuffled opaque brief ids with the version key held apart.
- First round: the new rules recovered the missing direction in 10 of 20 re-run cases and the baseline in 12 of 20 (new-only 1, baseline-only 3, net margin -2 against the bar of 5); control failures were 1 of 10 for the new rules (direction lost) and 0 of 10 for the baseline. The check fell short.
- The enumeration wording was revised once in `core/shared/alternatives-procedure.md` step 2: every axis gains a none position (not having the element, keeping it as it stands, removing it outright, or leaving it unenforced), values are taken from the underlying decision rather than the wording's list, a degree axis keeps a middle of the range that trades differently from both ends, and the covering test names the none position and requires each viable combination to be one option.
- Second round, the whole paired check re-run on the revised wording: the new rules recovered the missing direction in 11 of 20 re-run cases and the baseline in 13 of 20 (new-only 1, baseline-only 3, net margin -2 against the bar of 5); control failures were 0 of 10 for the new rules and 1 of 10 for the baseline (direction lost). The control comparison passed; the recovery margin did not.
- The shortfall persists after the single revision round and is recorded here: the change is not verified by the re-run check, whose margin stayed at -2 in both rounds. The milestone keeps the revised wording as the best it has, since it matched the first round's margin and met the control comparison, which the first wording missed.
- Every scratch clone was deleted once its set was read; the source repositories were only read (fetched from), their `HEAD`, refs, and status unchanged by the runs apart from an unrelated commit the user made in one of them during the check.
- All run material (scripts, transcripts, sets, briefs, and verdicts) stays under the gitignored `temp/rerun-check/`; the only committed changes are the revised wording, its rebuilt host copies, and this task-list move with aggregate counts, and none of them carries a case, project, question, or answer detail from the benchmark data.
- `uv run scripts/build_hosts.py --check` passes on the rebuilt `hosts/claude/` and `hosts/antigravity/` trees.

---

## State New Rules In Skill Reference And Claims

Update `docs/skill-reference.md` to state the enumeration rules briefly in the `discuss-open-question`, `provide-alternatives-to-all-open-questions`, and alternatives-subagent entries and the one-axis rule in the `review-milestone-requirements` entry, and rewrite claim 4's Design in `docs/design-claims.md` to say the alternatives are distinct and cover the decision, with no count and its Metric line left as it is. Both pages otherwise still describe the retired count guideline. It is verified by reading those entries against the final runtime wording, finding no count guideline for alternatives left in either page, and confirming `docs/workflow.md` is unedited.

**Verified:**

- The `discuss-open-question` entry of `docs/skill-reference.md` no longer says "2–4": a bare block's alternatives are enumerated through `alternatives-procedure.md`, stated briefly as axes named first, each option a position on them, the set distinct (every two options differ in substance on an axis) and covering (the underlying decision rather than the question's wording, not doing the thing included where honestly viable), with no count guideline.
- The `provide-alternatives-to-all-open-questions` entry states the same rules briefly as the ones every subagent enumerates under, with the set's size following from its axes and their viable combinations, and says the orchestrator itself states and checks none of them, matching the orchestrator's SKILL.md.
- The `provide-alternatives-to-open-question` (subagent) entry states the rules as `alternatives-procedure.md` step 2 now words them: axes first (approaches, degrees or values where the trade-off changes, premises the wording assumes, a none position on every axis), not doing the thing weighed on every question with postponing as one form of it, options as positions on every axis with every combination weighed and each viable one described, no sibling-owned axis varied and such a dependence named as a condition in the drawback, the distinct and covering tests, no count guideline, and a what-it-is text holding only the option's axis positions.
- The `review-milestone-requirements` entry states the one-axis rule as step 3 words it: each question asks one choice, a gap holding two becomes two questions, choices that constrain each other so not every pairing is viable are one multi-axis question, and no detection test is prescribed.
- Claim 4's Design in `docs/design-claims.md` says the alternatives are distinct and cover the decision (each two different in substance, covering the full decision and not only the question's words, including not doing the thing where possible), carries no count, and keeps its one-advantage-one-drawback, recommendation, and citation sentences; its Metric line is byte-for-byte unchanged.
- A search of both pages for `2–4`, `2 to 4`, `two to four`, and `typically` finds no count guideline for alternatives, and neither page carries any figure or detail from the benchmark data.
- `git diff --quiet docs/workflow.md` succeeds, so `docs/workflow.md` is unedited, and `CLAUDE.md` is untouched.

---
