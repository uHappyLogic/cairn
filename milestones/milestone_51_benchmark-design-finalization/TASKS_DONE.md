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
