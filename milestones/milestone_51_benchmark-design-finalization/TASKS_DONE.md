# TASKS DONE

## Finish Stops On Standing Open Questions

Make `finish-current-milestone` stop, writing and committing nothing, when the milestone's `open_questions.xml` still holds any question block, checked through the open-question tool's `list` call, whatever `TASKS_DONE.md` holds, with no check on completed tasks and no override flag, so a milestone whose derivation was refused on standing questions can no longer be closed empty while a decision-only milestone that answered everything still closes. Change it under `core/`, rebuild the hosts, and verify with `uv run scripts/build_hosts.py --check` and both pytest runs green.

**Verified:**

- `core/skills/finish-current-milestone/SKILL.md` step 3 runs `python3 {{PLUGIN_ROOT}}/tools/open_questions.py list <MILESTONE_DIR>` before the `TASKS_TODO.md` check and before any write (steps 5-8), and on any printed line stops immediately, writing and committing nothing, with the fixed `Cannot finish the milestone: the following open questions must be resolved first:` line and the printed Short Titles as bullets; a failing call prints its `Error:` line and stops; the `list` call is the whole check, never a read of `open_questions.xml`
- The stop applies whatever `TASKS_DONE.md` holds; the skill adds no check on completed tasks and no override flag (the only `--milestone` flag remains the milestone-selection one), so an empty `list` with an empty `TASKS_TODO.md` proceeds to finish a decision-only milestone
- The skill's intro states that it verifies no open question stands, and `docs/skill-reference.md`'s finish entry describes the new stop
- `uv run scripts/build_hosts.py` rebuilt the three host trees, each rendering the `list` call with its own plugin root, and `uv run scripts/build_hosts.py --check` passes
- `uv run pytest` passes (891 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (887 passed, 1 skipped)

---

## Fix Every Skill's No-Op And Stop Lines

Give every skill a fixed, unique, identifier-free first line for each distinct no-op and precondition-stop condition, with variable detail allowed after it, as one plugin-wide convention extending the fixed-success-line invariant; list the lines in `docs/skill-reference.md`, extend the `CLAUDE.md` terse-reporting invariant to cover them, and add a pytest test that checks each listed line verbatim against the rendered skill files and that every line is unique. Verify by rebuilding the hosts and running `uv run scripts/build_hosts.py --check` and both pytest runs green with the new test passing.

**Verified:**

- Every no-op and stop condition each skill states, and each stop the shared milestone-resolution and completion procedures own, opens its report with one fixed, identifier-free line as the whole first line, its variable detail (the tool's `Error:` line verbatim, Short Titles, a remedy) on the lines below it, changed under `core/` in 19 skills and 2 shared procedures.
- `docs/skill-reference.md` gains a `## Fixed console lines` section whose table lists all 80 fixed lines (success, no-op, and stop) with source and kind, a shared-procedure stop listed once under its procedure and the shared `Answer recorded.` as one row naming its three skills.
- The `CLAUDE.md` terse-reporting invariant extends the fixed-line rule to every no-op and stop line as one plugin-wide convention, with its reason (no exit code, so a harness matches the final message), the listing, and the test; the milestone-resolution invariant's miss wording and the `tests/` layout entry match.
- `tests/test_fixed_console_lines.py` checks each listed line verbatim against the rendered source files of every host tree (claude, antigravity, codex), as a whole fenced-block line or a whole inline code span, checks that no line repeats and no line carries a placeholder, and failed on a mutated and on a duplicated row before passing (163 cases).
- `uv run scripts/build_hosts.py` rebuilt the three host trees and `uv run scripts/build_hosts.py --check` passes.
- `uv run pytest` passes (1054 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (1050 passed, 1 expected skip), the new test passing in both.

---

## Review Skill Prints Fixed Convergence Line

Give `review-milestone-requirements` a fixed, identifier-free convergence line, printed as its convergence verdict when its closing `list` is empty, as the exit signal the benchmark's bounded review loop matches in the invocation's final message, and spell the line in `docs/skill-reference.md` beside the skill's other fixed lines so the listed-line test pins it. Change it under `core/`, rebuild the hosts, and verify with `uv run scripts/build_hosts.py --check` and both pytest runs green.

**Verified:**

- `core/skills/review-milestone-requirements/SKILL.md` step 6 makes the convergence verdict, when the closing `list` prints nothing, exactly one fixed identifier-free line shown as a whole fenced-block line, `Requirements converged — ready for task derivation.`, printed on a reshaping pass and a no-op pass alike and never when `list` printed anything; the not-ready verdict is unchanged
- `docs/skill-reference.md`'s `## Fixed console lines` table lists the line in a `review-milestone-requirements` row of kind `verdict` beside the skill's success and no-op rows, the section's opening paragraph says it is the one listed line printed below a first line and matched as a review loop's exit signal, and the skill's own entry points at it
- `tests/test_fixed_console_lines.py` accepts the `verdict` kind and pins the line: it passes against all three rendered host trees and failed when the listed row was mutated, the uniqueness check passing with the line added
- The `CLAUDE.md` terse-reporting invariant states the convergence line, when it prints, and its reason (the bounded loop's exit signal), and names it as the table's one verdict line
- `uv run scripts/build_hosts.py` rebuilt the three host trees, each rendering the line in its `review-milestone-requirements/SKILL.md`, and `uv run scripts/build_hosts.py --check` passes
- `uv run pytest` passes (1056 passed) and `uv run --no-project --python 3.9 --with pytest pytest` passes (1052 passed, 1 skipped)

---

## Align Usage Docs With Model Strategy

Rewrite `docs/ways-of-using-cairn.md` to the draft's `models_strategy_1` allocation, the `sonnet` alias at `medium` for the init, define, goto, and finish lines, `fable` at `xhigh` for the starting-state, review, recommend, and derive lines, and `opus` at `high` for `complete-all-tasks`, with the alternatives, sweep, and hand-answer lines unchanged and every prose sentence that restates a section's settings rewritten to match, so the draft's "written from Cairn's own usage snippets" sentence becomes true. This is a docs-only change needing no host rebuild, verified by reading each chain line against the draft's table.

**Verified:**

- Every `claude` line of `init-milestone-base-workflow`, `define-milestone-goal`, `goto-next-milestone`, and `finish-current-milestone` in `docs/ways-of-using-cairn.md` carries `--model "sonnet" --effort medium`, matching the draft's Sonnet 5.5 / medium rows.
- Every `claude` line of `specify-milestone-starting-state`, `review-milestone-requirements` (the Starting a milestone line), `recommend-all-open-questions` (all four lines), and `derive-tasks` (all three lines) carries `--model "fable" --effort xhigh`, matching the draft's Fable 5.1 / xhigh rows.
- Every `complete-all-tasks` line (all four) carries `--model "opus" --effort high`, matching the draft's Opus 5.5 / high row.
- The alternatives lines (`opus` at `high`), the sweep lines and both hand-answer lines (`fable` at `high`) are unchanged and match the draft's rows; the `agy` review line and the stuck-milestone escalation review line (`opus` at `max`), which have no row in `models_strategy_1`, are left as they stood.
- Every prose sentence restating a section's settings (Starting a milestone, Answering the questions that matter to you, Running a mixed-agent requirements review, Putting more intelligence into a stuck milestone, Executing tasks) names the same model and effort as that section's lines, and the `--model` legend's alias examples now include `sonnet`, which `claude --help` lists.
- `ideas/benchmark_for_cairn.md` is untouched, its `models_strategy_1` table and "written from Cairn's own usage snippets" sentence standing as before; only `docs/ways-of-using-cairn.md` changed, no host was rebuilt, and `uv run scripts/build_hosts.py --check` passes.

---

## Draft Operator And Hidden Requirement Rules

Write into the draft's hidden-requirement and operator sections the bearing-question test (a one-line bearing scope beside each entry's statement, the topic or theme of the questions for prompt 1 and where a prepared set is stored or how it is carried to another computer for prompt 2, governing disclosure and the planned turn's "bears on" lines, a catch-all or off-scope question getting nothing beyond PROJECT.md), the reply-need classifier as a distinct tool-less model call under a fixed model and effort pair with its one stated rule, recorded verdict and one-clause reason, and tokens recorded beside the operator's apart from the totals, the operator's input of prompts 1 to n in phase n with phase n's hidden knowledge only, and the two-arm hidden-requirement pilot with its met-rate ceiling, hit-rate floor, and fix rules, each stated with the reason for the gap it resolves. Verify by reading the sections against the four decisions and gaps 3, 14, and 17 of the report.

**Verified:**

- The draft's "Hidden requirements" section carries an "A bearing scope" bullet stating that each entry has a one-line bearing scope beside its statement, versioned with the entry, naming the decisions a question must ask about to get the disclosure (prompt 1: the topic or theme of the questions; prompt 2: where a prepared set is stored or how it is carried to another computer). The harness inserts it with the statement into the operator's hidden knowledge, disclosure happens only on an in-scope question, a catch-all or off-scope question gets nothing beyond PROJECT.md, and the same scope governs the planned turn's "bears on" lines. The bullet states the catch-all and private-reading reason.
- Both project-section hidden-requirement entries carry a "Bearing scope:" sentence beside their statement. The operator's hidden-knowledge layer, the planned-turn sketch and its "answers only where the hidden knowledge decides" bullet, and the inputs bullet all apply the scope test, with no leftover "a question whose answer the statement changes" rule.
- The operator section holds a "The reply-need classifier" subsection: a distinct tool-less model call under a fixed model and effort pair versioned with the operator definition and recorded in the manifest (a `classifier` key). It reads only the final message, never the prompt or hidden knowledge, under one stated rule (asks, confirms, or offers a choice gets a reply; completion, stop, error, or a closing offer gets none). It outputs a verdict and a one-clause reason, and only a reply verdict invokes the operator. A no-reply verdict is not an operator turn and adds no attentive session. Every verdict and reason goes into the invocation's record file, and the classifier's tokens are recorded beside the operator's and kept out of the totals. The subsection states the reason for the separate call.
- The general guideline layer gives the operator prompts 1 to n in phase n, byte-identical from the versioned prompt texts the manifest records, at every reactive turn and at the planned turn, with earlier prompts marked as earlier requests and prompt n as the current one. Hidden knowledge stays phase n's only, and no versioning changes because a prompt-1 revision already invalidates both phases. The "prompt text as committed" sentence is gone, the phase-2 reason (a stakeholder who doesn't know the game they asked for) is stated, and the planned-turn input and the phase-2 operator sentence match.
- The "Hidden requirements" section holds a "The calibration pilot" subsection with two arms per prompt, each run a fixed small number of times under the strongest manual pair. The unasked arm runs manual_prompt with hidden knowledge withheld, under a met-rate ceiling. The asked arm gives a model the seed tree, the prompt, and one maintainer-written bearing question from the entry's scope, with no operator, under a hit-rate floor. A requirement passes only when both arms pass, a failed ceiling is fixed by weakening the evidence or the prompt's invitation, a failed floor by strengthening the evidence (each as a seed bump or prompt revision followed by another pilot), and pilot runs are never scored. The subsection states the reasons for the pilot and for two arms.
- The draft refers to the design-gaps report nowhere.

---

## Draft Left-Open And Implied List Split

Apply the overlap rules to both prompts' lists in the draft's project section: an item in both a left-open list and an implied list is split wherever a choice among ways remains, the implied line scoring only that some way through exists and the choice staying an unscored left-open item, and an item with no such choice goes to exactly one list by the stated test, implied when a quiz lacking it would be called broken or unfinished by any builder, left open when lacking it is a defensible product choice, with the verdict recorded per item and neither list thinned by a blanket rule, both rules stated in the text with gap 1's reason. Verify by checking that no item remains in both lists unsplit and that every moved item carries its verdict.

**Verified:**

- The "Implied requirements" bullet under "The axes" states both rules: an item in both lists is split wherever a choice remains among ways through its case (one no stated line already tests), the implied line scoring only that some way through exists and the choice staying an unscored left-open item, and an item with no such choice left goes to exactly one list by the stated test (implied when a host-run quiz lacking it would be called broken or unfinished by any builder, left open when lacking it is a defensible product choice); it says the verdict is recorded per item in the project section and that neither list is thinned by a blanket rule, and gives gap 1's reason (the item contradicted itself: called a decision, answered "your call", yet scored on one answer, so the axis rewarded more features, scored taste, and cost a minimal answer a line; and it read as tilting the axis toward Cairn), as the hidden requirement's one-list rule carried to the other two lists
- Prompt 1's lists record a verdict for each of the nine items that met: team names and keyboard control moved to the left-open list only, each with its line removed and its test verdict and reason stated; team counts, the tie, undoing an award, skipping a question, progress, a reload, and a shared place split, each implied line reworded to accept any way through and each left-open item reworded to the choice among ways
- Prompt 2's lists record a verdict for each of the six items that met (the editor's file, the built-in questions, choosing a set, answers off the big screen, answer validation, changing a set between questions), all split, each implied line reworded to accept any way through and each left-open item reworded to the choice among ways
- No left-open item of either prompt is scored on one of its answers by an implied line: every item still in both lists is split, prompt 1 now holds eleven implied lines and prompt 2 eleven
- The draft stays consistent with the lists: the phase-1 and phase-2 checklist counts read eleven implied lines for prompt 1, the "Open-ended beyond the flow" bullet names the post-split decisions, and the axis's way-through examples read "a resume or a warning before a reload"
- The draft refers to the design-gaps report nowhere, and only `ideas/benchmark_for_cairn.md` changed, with `uv run scripts/build_hosts.py --check` passing

---

## Draft Checklist Line Test Specifications

Write beside every test line in the draft's project section a short specification naming the case the test must drive the artifact into and the observable outcome it must assert, stated as an outcome rather than a means: prompt 1's six stated and thirteen implied lines, prompt 2's stated line and eleven implied lines, and prompt 2's carry-between-profiles hidden line, the award line's specification being award a point, take it back, and assert the score is back to its earlier value, with a confirmation that prevents the award counting as well. State that the specification is part of the checklist, still derived from the draft and nothing else, with each line keeping its id, and verify by counting the specified lines against those totals.

**Verified:**

- Every test line in the draft's project section carries a specification beside it, a `*Case:*` naming the case its test must drive the artifact into and an `*Assert:*` naming the observable outcome it must assert, each stated as an outcome that names no control or mechanism: prompt 1's six stated lines (newly listed under "Prompt 1: the game") and its implied lines, prompt 2's stated line (newly listed under "Prompt 2: the host's own questions") and its eleven implied lines, and prompt 2's carry-between-profiles hidden test line; prompt 1's animal reading line, not a test line, gets none
- Counting the specified lines gives 6 stated and 11 implied for prompt 1, 1 stated, 11 implied, and 1 hidden for prompt 2, 30 in all and none outside the project section; prompt 1's implied total is the live draft's eleven, the decision's thirteen having counted the team-names and keyboard lines that the earlier "Draft Left-Open And Implied List Split" task removed by its per-item verdicts, and the phase-1 and phase-2 checklist counts in the draft already read eleven
- The award line's specification is to award a question's point, take it back before the game moves on, and assert the team's score is back to its earlier value, a confirmation that keeps the award from counting, declined by the host, passing as well
- "The checklist and the rank" states that each test line carries the specification written beside it in the project section, stated as an outcome rather than a means so the any-way-through rule still holds, that the specification is part of the checklist, derived from the draft with its line and from nothing else, and that the line keeps its id (a specification is no line of its own, and a carried line takes its specification with it), with gap 7's reason (fresh tests per rating could test one line differently, a weak test passing on a control that exists); the rater's test-line bullet and "Fit with the run rules" point at the specification
- The draft refers to the design-gaps report nowhere, only `ideas/benchmark_for_cairn.md` changed, and `uv run scripts/build_hosts.py --check` passes

---
