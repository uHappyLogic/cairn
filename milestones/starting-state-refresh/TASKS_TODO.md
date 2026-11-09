# TASKS TODO

## Live Query Filtered by Milestone Path

Give the `live` query of `core/tools/milestones.py` an optional MILESTONE_PATH: with it the query lists, in its unchanged three-field line, every other live milestone, started or defined, whose scope equals, contains, or lies under the named milestone's, the named one left out as `gate` leaves it out, reading the path lexically as `gate` reads its argument and refusing on one `Error:` line a path that names no directory directly inside a `milestones/` container; with no argument it prints what it prints today. It is the starting-state procedure's in-flight read, the started field and the scope filter in one call. Pinned by tests beside `tests/test_milestones_live.py` covering overlap in both directions, a disjoint scope, a defined and a started sibling both listed, the refusal, and the unchanged no-argument print, with the host trees rebuilt.

---

## Milestones Query Milestone-Path Form and Bound

Give the `milestones` query of `core/tools/milestones.py` two additions that leave `milestones PATH` reading as it does today: a milestone-path form, a flag taking a MILESTONE_PATH in place of the positional PATH, read lexically and refused as `gate` refuses a path that names no directory directly inside a `milestones/` container, whose print is the overview `milestones <scope>` gives for that milestone's scope; and an optional `--last N` that keeps every live line and only the N newest finished lines by finish timestamp. Without `--last` the query prints what it prints today, so `record`, `/release-plugin`, and every other reader are unchanged. Pinned by tests beside `tests/test_milestones_milestones.py` covering the form against the equivalent scope call, its refusal, the bound keeping every live line, and the unbounded print unchanged, with the host trees rebuilt.

---

## Write the Starting-State Procedure

Write `core/shared/starting-state-procedure.md`, the one commit-free shape of a first run and a refresh that three runners will follow: it opens with `since <MILESTONE_DIR>` and its three outcomes (no line is a first run, the anchor alone means the ground has not moved and nothing is explored, anything more is a refresh), explores the scope and then the adjacent material the goal reaches, reads the record in two tiers with no verified bar (the `milestones` overview in its milestone-path form, then `summary` or `show` for each milestone whose line bears on the goal, never `tasks --with-body`), reads what is in flight through `live <MILESTONE_DIR>` with each started milestone's decisions and remaining tasks read as prose, and edits `## Relevant starting state` in place, leaving byte-identical every subsection whose facts still hold. After the edit it names, from a whole read of `open_questions.xml`, the standing picks the changed facts undermine by the two tests `modify-milestone-goal` applies, doubt stripping, and clears them with one `strip --recommendation` call, corrected against the `Error:` line and re-run once on a failure; it owns two fixed stop lines, each with the `Error:` line verbatim beneath it, one for any failed milestones-tool call, stopping before any edit, pick clearing, or commit, and one for a second pick-clearing failure, the edit left uncommitted, and it states the repeated exploration of a refresh that changed nothing as an accepted cost. Verified by the rebuilt host trees, the two stop lines' new rows in the `## Fixed console lines` table of `docs/skill-reference.md` passing `tests/test_fixed_console_lines.py`, and a read of the procedure against the decisions under `### The starting-state procedure`.

---

## Starting-State Skill Follows the Procedure

Rewrite `core/skills/specify-milestone-starting-state/SKILL.md` to follow `starting-state-procedure.md` for a first run and a refresh alike, so it no longer assumes an empty section, and to commit `requirements.md`, together with `open_questions.xml` when the procedure cleared a pick, under `Starting-state: <MILESTONE_DIR>`. Its two fixed lines stay as they are, it gains one fixed no-op line of its own, printed with nothing explored when `since` prints the anchor alone, and it stops on the procedure's two lines as the procedure states them. Verified by the rebuilt host trees, the new no-op line's row in the `## Fixed console lines` table passing `tests/test_fixed_console_lines.py`, and a read of the rendered skill against each of the three `since` outcomes.

---

## Review Pass Reads the Milestones Overview

Give `core/skills/review-milestone-requirements/SKILL.md` one fixed milestones-tool call at its inventory step, run on every pass and read beside the two documents: the `milestones` overview in its milestone-path form for `<MILESTONE_DIR>` with `--last` written as the literal 10, a listed milestone getting a deeper read through `summary` or `show` only where the pass judges its line to bear on a gap or a pair of decisions. A failed call, meaning any non-zero exit, stops the pass at that step before any prune, dedup, new block, or note deletion: the report opens with one new fixed, identifier-free stop line with the `Error:` line verbatim beneath it, no commit is made, and neither the still-open list nor the convergence verdict is printed. Verified by the rebuilt host trees, the stop line's new row in the `## Fixed console lines` table passing `tests/test_fixed_console_lines.py`, and the rendered call run as written against this repository.

---

## Review Pass Weighs Decisions Against Facts

Add one bullet to the gap-surfacing step of `core/skills/review-milestone-requirements/SKILL.md`: a recorded decision resting on a `## Relevant starting state` fact that no longer holds becomes an ordinary open question, authored like any other gap and never under the conflict questions' fixed opening phrase, since there is no second entry to rewrite, so that its answer supersedes or confirms the decision through the answer core's existing rewrite rule. This is the one place a starting-state refresh's changed facts are weighed against the decisions, the refresh itself rewriting none. Verified by the rebuilt host trees and a read of the rendered step showing the bullet beside its four existing questions with the `## Decisions` consistency step unchanged.

---

## Derive-Tasks Gates First and Refreshes

Make `core/skills/derive-tasks/SKILL.md` follow `check-scope-gate.md` twice, each time as its own step: at the front, directly after resolution and before everything else, and again directly ahead of the fixed write call, which stays gate-free, a run deriving no brief skipping the second check as it skips the write. Between the first gate and its reads it runs `since <MILESTONE_DIR> --milestones`: on no output or the anchor alone it explores nothing, prints nothing about the starting state, and goes on with the section as it stands, and on any line beyond the anchor it follows `starting-state-procedure.md` in place and commits the refreshed section, with `open_questions.xml` when a pick was cleared, under `Starting-state: <MILESTONE_DIR>` as a commit of its own that prints no line, before it reads the documents it decomposes. A failed `since` call, or either stop of the procedure, stops the whole run under the procedure's line with no task-list write and no task commit, and a refresh commit that landed before a closed second gate stays committed; verified by the rebuilt host trees, `tests/test_fixed_console_lines.py`, and a read of the rendered skill for each `since --milestones` outcome and both gate positions.

---

## Submit-Task Gates First and Refreshes

Make `core/skills/submit-task/SKILL.md` follow `check-scope-gate.md` twice, each time as its own step: at the front, directly after resolution and before its reads and authoring, and again directly ahead of its fixed insert-and-commit call, which stays gate-free. Between the first gate and its reads it runs `since <MILESTONE_DIR> --milestones`: on no output or the anchor alone it explores nothing, prints nothing about the starting state, and goes on, and on any line beyond the anchor it follows `starting-state-procedure.md` in place, its pick judgment live here since standing picks may exist, and commits the refreshed section, with `open_questions.xml` when a pick was cleared, under `Starting-state: <MILESTONE_DIR>` as a commit of its own that prints no line, before it authors. A failed `since` call, or either stop of the procedure, stops the whole run under the procedure's line with no insert and no task commit, and a refresh commit that landed before a closed second gate stays committed; verified by the rebuilt host trees, `tests/test_fixed_console_lines.py`, and a read of the rendered skill for each `since --milestones` outcome and both gate positions.

---

## Host Test for the Derive-Tasks Refresh

Add one test to `host_tests/` that runs a single headless `/cairn:derive-tasks --milestone …` on the first fixture milestone and asserts, from the seeded repository's git log, that a `Starting-state:` commit lands before the `Task-derivation:` commit, naming no host so it runs unchanged under `--host claude`, `--host antigravity`, and `--host codex`. Test-side code local to the new test, beside the unchanged `seeded_repo`, builds the history on top of the seed through the plugin's commit tool in this order: the first milestone's `Starting-state: <path>` commit, then a second, overlapping milestone's files added, its `Task-completion:` commits, and its `Milestone-finish: <path>` commit removing its directory, the first milestone left with no open question so the derivation's precondition holds. Its passing runs belong to the acceptance task; here it is verified by building that history in a scratch directory and reading it through the milestones tool (`gate` on the first milestone printing nothing, `since --milestones` printing lines beyond the anchor), with the other host tests and the shared seed unchanged in the diff.

---

## Pass the Host Suite on Three Hosts

Refresh each host's installed plugin copy on this machine from the committed rebuilt tree by that host's documented install, then run the whole host suite, the refresh test included, as `uv run pytest host_tests --host claude`, `--host antigravity`, and `--host codex`, and have every test pass on all three with none marked or skipped. A host that fails is fixed in this task before it is done, the trees rebuilt, the copies refreshed again, and the suite re-run on every host the fix touches. It stands after every task that changes `core/` or `host_tests/`, and is verified by the three passing runs' summaries.

---

## Execution Chains Open With the Refresh

Rewrite the three chains of `docs/ways-of-using-cairn.md` that derive and complete tasks so each opens with the starting-state refresh line and one review pass and then carries exactly one alternatives line, one recommend line, and one sweep line, in that order and with nothing after the sweep, ahead of its derivation line: "Executing tasks" gains the alternatives and recommend lines ahead of its sweep, "Answering the questions that matter to you" an alternatives line after its hand-answer lines and ahead of its existing recommend line, and "Putting more intelligence into a stuck milestone" keeps its own alternatives, recommend, and sweep lines as that pass, each new line taking the model and effort settings the "Starting a milestone" chain gives it. The sentence under "Preparing another milestone while one runs" telling the operator to rerun the starting-state line goes, replaced by that rule, and the page states that a task-entry writer refreshes a stale state itself and that an exploration which changes nothing is repeated by the next run, an accepted cost. Verified by a read of each chain's fenced block and prose against the Execution chain lines decision, every changed line's skill name, flag, model, and effort matching the lines the page already carries.

---

## Docs and Invariants Describe the Refresh

Bring `docs/workflow.md`, `docs/skill-reference.md`, and `CLAUDE.md` in line with the starting state as landed: the workflow page's starting-state and task-entry stages and its committing paragraph (a refresh committed under `Starting-state:` by the skill or, as a commit of its own, by a task-entry writer; the gate checked twice; an unchanged refresh repeated as an accepted cost), the skill-reference entries of `specify-milestone-starting-state`, `review-milestone-requirements`, `derive-tasks`, and `submit-task`, and `CLAUDE.md`'s layout, pipeline listing, and invariants. The milestones-tool invariant is rewritten for `since`, `show`, the milestone-path forms of `live` and `milestones`, `--last`, the content read from a commit, and `gate` and `since` as the two queries that check for a shallow clone; the scope-gate invariant for the two gate positions in the task-entry writers; and one new invariant records the starting state's rationale (the anchor found by subject and path, the refresh as a premise change with its pick clearing, the writers refreshing instead of stopping, no state for an unchanged refresh, the verified bars left unread). Verified by `uv run scripts/build_hosts.py --check`, both pytest runs, and a read-through finding no statement that `live` takes no argument, that only `gate` checks for a shallow clone, or that the tool has six queries.

---

## Benchmark Draft Follows the Refresh

Update `ideas/benchmark_for_cairn.md` for the refresh while keeping both cairn deliveries' one starting-state line in place and their lists unchanged: the chain text gains one statement of why, that the line already stands where the ways-of-using rule puts the refresh, directly ahead of the first review pass, and that in a single-milestone run nothing outside the milestone's directory lands between it and derivation, so a second line would end on the no-op line every time. The expected lines "Detecting a stop" gives the starting-state line take the new no-op line as the `## Fixed console lines` table of `docs/skill-reference.md` spells it. Verified by a read of the draft against the Benchmark chains decision, the two delivery lists unchanged in the diff and the no-op line matching its table row character for character.

---

## Revise the Draft After Step Four

Revise "Carrying it out" in `ideas/milestones_addressed_by_path.md` so its step 4, "The starting state", is headed done and records what landed as the sections for steps 1 to 3 do (the task count against the about nine planned, where the milestone grew, and where the Proposed shape now differs from what landed), and so it notes what this milestone found for step 5, "The record in the completion procedure", with the draft's date line extended. It stands last, after the acceptance runs, so the record it reads is complete; verified by a read of the revised section against this milestone's decisions and its `Task-completion:` commits as `tasks <MILESTONE_DIR> --with-body` prints them.

---
