# TASKS DONE

## Build Local Replay Case Manifest

Assemble, under the git-ignored `temp/`, the case manifest for the replay: the eight windows (fourteen pick-versus-decision pairs) the uncommitted sweep-contradiction analysis there identified, in this repository and in other local projects, with no other windows added, each hand answer of a window (and each goal revision in it, as a case of its own, since a revision now clears picks too) resolved to its commit and that commit's parent, and for each case the decision it folded laid beside every standing pick's option and recommendation text at that parent, every label left blank for the maintainer. This is the fixed case set the change is measured on, and all of it is per-case material that stays local. Verified when the manifest accounts for all eight windows and fourteen pairs, every case resolves read-only in its own repository, and `git status` shows no change outside `temp/`.

**Verified:**

- The manifest `temp/stale-pick-replay/manifest.json` exists under the git-ignored `temp/` (`git check-ignore` matches it), beside the script that built it and a rendered reading view, and holds exactly the eight windows of the analysis's stale-pick class, in this repository and in other local projects, with no other window.
- All fourteen pick-versus-decision pairs are accounted for: each is recorded in its window as a candidate pointer (never a label) to one case, and its pick stands among that case's standing picks at the parent.
- Every hand answer and every goal revision inside each window is a case of its own, 31 in all (24 hand answers, 7 goal revisions), each recorded with its commit and that commit's single parent.
- Each case lays the decision it folded (its `requirements.md` change, with the commit body) beside every pick standing at the parent, 449 pick entries in all, each with its recommended option's what-it-is text and its recommendation text, none empty.
- Every label is blank (0 of 449 labelled), and the bar's two thresholds and round count are empty slots left for the maintainer.
- `python3 temp/stale-pick-replay/build_manifest.py verify` re-resolves every case in its own repository with read-only git commands, finds commit, parent, folded text, and standing picks equal to the manifest, finds each source repository's `HEAD`, refs, and status unchanged across the run, and exits 0.
- `git status` in this repository showed no change outside `temp/` before the task-list move.

---

## Let Remove Reconcile Named Undermined Dependents

Extend `remove` in `core/tools/open_questions.py` with an optional argument naming further Short Titles to reconcile as undermined dependents of the removed block: every title is resolved before anything changes (a title matching no block, and equally the answered block's own title, stops the call on one `Error:` line naming that title and, for an unknown one, the ids the document holds, with exit status 1 and the document byte-for-byte unchanged), and each named block then goes through the same per-block strip primitive as the `<depends-on>`-tagged dependents in the same one write, transitively and keeping its `<alternative>` children, except that a named block carrying no `<recommendation>` is left exactly as it stands and seeds no transitive strip. The hand-answer path needs this to clear picks no tag declares; the tool still prints nothing on success, and its docstring and `--help` state the new contract. Verified by new cases in `tests/test_remove.py` for each of those behaviours passing under both `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest`, with `hosts/` rebuilt and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- `remove` in `core/tools/open_questions.py` takes the optional `--undermined SHORT_TITLE...` (one or more Short Titles after the block's own, the flag repeatable, compared un-escaped and case-folded, a title named twice counted once), and a call without it behaves as before: the 48 earlier tests of `tests/test_remove.py` pass unchanged.
- Every named title is resolved before anything changes: a title matching no block stops the call on the one line `Error: no <open-question> block has the id "<title>"; the document holds <ids>`, and the removed block's own title on the one line `Error: --undermined names "<title>", the block being removed, which cannot be reconciled as its own dependent`, each with exit status 1, empty stdout, no write reached, and the document byte-for-byte unchanged even when valid titles and tagged dependents accompany the bad one.
- Each named block goes through `strip_recommendation`, the same primitive as the `<depends-on>`-tagged dependents, in the same single write (one `save_document` call covering the removal, the tagged dependents, and the named ones), keeping its `<alternative>` children; a named block is stripped even when its own tag agrees with `--option`, while an un-named agreeing dependent still loses only its tag.
- The strip is transitive from a named block: blocks whose `<depends-on>` names a stripped named block are stripped in turn, alternatives kept, with no tag left naming a stripped block and unrelated blocks byte-identical.
- A named block carrying no `<recommendation>` (alternatives only, or bare) is left exactly as it stands, the call still succeeds and makes its write, and a block whose `<depends-on>` names it keeps its pick and its tag; `remove_question` returns no id for it.
- The tool prints nothing on success with `--undermined` (exit status 0, empty stdout and stderr).
- The module docstring's `remove` entry and `remove --help` state the new contract (the flag, resolution before any change, the two refusals, the same strip in the same write, the no-recommendation exception), checked by a test.
- 17 new cases in `tests/test_remove.py` cover those behaviours; `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` each pass all 544 tests.
- `hosts/` was rebuilt with `uv run scripts/build_hosts.py` (the tool rendered into all three host trees) and `uv run scripts/build_hosts.py --check` passes.

---

## Pass Named Dependents Through Answer Core

Give `core/shared/answer-procedure.md` one new optional input, the Short Titles of the standing picks its caller judged undermined, which step 4 passes through to the same `remove` call as given, with no branch and no judgment of its own; when the tool refuses a named title on its `Error:` line, the runner corrects the list and runs the same call again. `core/shared/answer-with-recommendation-procedure.md` passes nothing for that input, so the core stays a pass-through recorder and the answer sweep and `/answer-open-question-with-recommendation` record exactly as before. Verified by reading step 4 against the "Undermined-pick judgment home" and "Unknown named dependent" decisions, no diff in either of those two skills, `hosts/` rebuilt, and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- `core/shared/answer-procedure.md` `## Inputs` declares five inputs, the last two optional, the new one being UNDERMINED PICKS: the Short Titles of other open questions whose standing pick the caller judged the answer undermines, with the judgment stated as the caller's alone.
- Step 4's single `remove` command carries `[--undermined "<UNDERMINED SHORT TITLE>" …]` (the flag the live tool's `remove --help` shows), passed exactly as given when the input is supplied and left off when it is not; the step's only owned decision is still `--option`, so the core gained one input and no branch or judgment, as the "Undermined-pick judgment home" decision requires.
- Step 4 states that the tool refuses an `--undermined` title matching no block, or naming the answered block itself, with the document unchanged and the title named on its `Error:` line, and that the runner corrects the list and runs the same call again, as the "Unknown named dependent" decision requires.
- `core/shared/answer-with-recommendation-procedure.md` is unedited and hands the core only MILESTONE_DIR, SHORT TITLE, ANSWER, and RECORDED OPTION, so it passes nothing for the new input; `git diff --stat -- core/skills core/shared/answer-with-recommendation-procedure.md` is empty, so neither the answer sweep nor `/answer-open-question-with-recommendation` has a diff.
- `uv run scripts/build_hosts.py` rebuilt `hosts/`, with the changed procedure rendered into `hosts/claude/shared/`, `hosts/antigravity/shared/`, and `hosts/codex/plugins/cairn/shared/`.
- `uv run scripts/build_hosts.py --check` passed.

---

## Write Hand-Answer Procedure With Undermined-Pick Judgment

Add a new shared procedure under `core/shared/` that composes over `answer-procedure.md` for a hand answer: the runner reads `<MILESTONE_DIR>/open_questions.xml` whole with the file-reading tool, for reasoning only, names every other question's standing pick the answer undermines (its recommended alternative, as that alternative's what-it-is text reads, can no longer be carried out alongside the recorded decision, or the one-line rationale of its `<recommendation>` states or plainly presupposes something the answer changed), and delegates to the core with those Short Titles as its new input. The judgment reads option and rationale text against the answer and what it directly entails without re-forming the recommender's judgment, strips on doubt, leaves standing the picks the answer does not bear on, and runs on every hand answer whether or not the recorded option is the one the answered block's own recommendation names. Verified by reading the file against the "Undermined pick test", "Standing picks view", and "Answer matching the standing pick" decisions, `hosts/` rebuilt with the procedure rendered into every host tree, and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- `core/shared/hand-answer-procedure.md` exists as a new shared procedure that composes over `answer-procedure.md`: it takes MILESTONE_DIR, SHORT TITLE, ANSWER, and the optional RECORDED OPTION, derives UNDERMINED PICKS itself, and its step 3 hands all of them to `{{PLUGIN_ROOT}}/shared/answer-procedure.md` followed unchanged, passing nothing for UNDERMINED PICKS when no pick was named; the input name matches the live core's `## Inputs`.
- Step 1 has the runner read `<MILESTONE_DIR>/open_questions.xml` whole with the file-reading tool, names the four child elements that read shows, and states that the whole read is for reasoning only and that every locate, list, lift, and write is a tool call, as the "Standing picks view" decision requires; the procedure itself makes no tool call and no edit to that file.
- Step 2 states both arms of the "Undermined pick test" decision: the recommended alternative, as its what-it-is text reads, can no longer be carried out alongside the recorded decision, or the one-line rationale of the `<recommendation>` states or plainly presupposes something the answer changed (a fact about the project, a constraint, a sibling's expected outcome) so the reason no longer holds as written though the option could still be carried out.
- Step 2 reads the option text and the rationale text against ANSWER and what it directly entails, judges in prose, and forbids re-forming the recommender's judgment over the other blocks' sets; it strips on doubt and leaves standing the picks the answer does not bear on.
- Step 1 states that the judgment runs on every hand answer whether or not the option being recorded is the one the answered block's own `<recommendation>` names, and that this element plays no part, as the "Answer matching the standing pick" decision requires; only blocks other than the answered one that carry a `<recommendation>` are judged.
- The file carries no host name, no editor-facing prose, and no `## Rules` section, and reports nothing about the picks it named.
- `uv run scripts/build_hosts.py` rebuilt `hosts/`, with the procedure rendered into `hosts/claude/shared/`, `hosts/antigravity/shared/`, and `hosts/codex/plugins/cairn/shared/`, each with the plugin-root placeholder filled and no `{{` left.
- `uv run scripts/build_hosts.py --check` passed with exit status 0.

---


## Route Both Hand-Answer Skills Through Procedure

Change `core/skills/answer-open-question/SKILL.md` and `core/skills/answer-open-question-with-alternative/SKILL.md` to follow the new shared hand-answer procedure in place of `answer-procedure.md` directly, the literal skill still passing no RECORDED OPTION and the alternative skill still passing its lifted id, so every hand answer runs the undermined-pick judgment. The alternative skill's "never read or edit it yourself" sentence and the literal skill's "every read and write of it in the core is a tool call" statement are reworded to the form the other inline skills carry (a whole read is for reasoning only, and every locate, list, lift, and write is a tool call), while each skill's reporting step and commit body stay as they stand, with nothing printed or recorded about any cleared pick. Verified by reading both skills against the "Undermined-pick judgment home", "Standing picks view", and "Cleared picks report" decisions, `hosts/` rebuilt, and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- Step 4 of `core/skills/answer-open-question/SKILL.md` follows `{{PLUGIN_ROOT}}/shared/hand-answer-procedure.md`, passing `MILESTONE_DIR`, `SHORT TITLE`, and `ANSWER` and no `RECORDED OPTION`; the file no longer names `answer-procedure.md`.
- Step 3 of `core/skills/answer-open-question-with-alternative/SKILL.md` hands the same three inputs plus the lifted id as `RECORDED OPTION` to `{{PLUGIN_ROOT}}/shared/hand-answer-procedure.md`; the file no longer names `answer-procedure.md`.
- Both skills describe the procedure as naming the standing picks the answer undermines and delegating the recording to the shared recording core, as the "Undermined-pick judgment home" decision requires, with no condition on the answered block's own recommendation.
- The literal skill's "every read and write of it in the core is a tool call" statement and the alternative skill's "never read or edit it yourself" sentence are both replaced by the form the "Standing picks view" decision fixes: a whole read with the file-reading tool is for reasoning only, and every locate, list, lift, and write is a call to the open-question tool.
- Each skill's commit BODY input and reporting step are unchanged in the diff: the one fixed line `Answer recorded.` plus the new-questions advisory, with nothing printed or recorded about any cleared pick, as the "Cleared picks report" decision requires.
- `uv run scripts/build_hosts.py` rebuilt `hosts/`, changing both skills' rendered files under `hosts/claude/`, `hosts/antigravity/`, and `hosts/codex/plugins/cairn/`.
- `uv run scripts/build_hosts.py --check` passed with exit status 0.

---

## Clear Undermined Picks On Goal Revision

Extend `core/skills/modify-milestone-goal/SKILL.md` so that, in the same run as the goal edit, the skill names the standing picks its impact analysis judges the revision undermines (by the "Undermined pick test" decision's definition, read against the revised goal) from its existing whole read of `open_questions.xml`, and clears them with one `strip --recommendation` call over those Short Titles, keeping every `<alternative>`. The clearing is not transitive (a block whose `<depends-on>` names a cleared block keeps its pick and its tag), the tool is unchanged, and `open_questions.xml` joins `requirements.md` in the `Goal-revision:` commit, which closes the route by which a pick formed under the old goal reaches the answer sweep. Verified by reading the skill against the "Goal revision pick clearing" decision, its edit step and commit PATHS agreeing with it, `hosts/` rebuilt, and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- `core/skills/modify-milestone-goal/SKILL.md` step 3 names the standing picks the revision undermines from its existing whole read of `open_questions.xml`, by the two tests of the "Undermined pick test" decision (option no longer carried out, stated reason no longer holds) read against the revised Goal, with doubt stripping and no re-forming of the recommender's judgment.
- Its new step 5 clears the named picks with one `strip --recommendation` call over their Short Titles, written as the full fixed tool command, and states that every `<alternative>` is kept.
- The clearing is stated as not transitive: a block whose `<depends-on>` names a cleared block keeps its pick and its tag, and is neither followed nor added to the call.
- The edit step (step 4) no longer forbids touching `open_questions.xml`, and the commit step's PATHS name both `<MILESTONE_DIR>/requirements.md` and `<MILESTONE_DIR>/open_questions.xml` under the unchanged `Goal-revision: <milestone_id>` subject, agreeing with the "Goal revision pick clearing" decision.
- The tool is unchanged: `git status` shows no change under `core/tools/` or `tests/`.
- `hosts/` was rebuilt with `uv run scripts/build_hosts.py`, changing the `modify-milestone-goal` SKILL.md in all three host trees, and `uv run scripts/build_hosts.py --check` passed.

---

## Describe Undermined-Pick Clearing In Docs

Update the `docs/skill-reference.md` entries for `/answer-open-question`, `/answer-open-question-with-alternative`, and `/modify-milestone-goal`, and the design text of claims 6 and 16 in `docs/design-claims.md`, to describe the new behaviour: a hand answer names the standing picks it undermines and `remove` reconciles them with the tagged dependents in one write, strip on doubt covering that judgment, and a goal revision clears the picks it undermines with one non-transitive `strip --recommendation`, so the `/modify-milestone-goal` entry no longer says it edits the Goal and nothing else. Verified by reading each changed passage against the Decisions.

**Verified:**

- The `/answer-open-question` entry of `docs/skill-reference.md` states that the skill follows `core/shared/hand-answer-procedure.md` over the recording core, reads `open_questions.xml` whole for reasoning only, and names every other question's standing pick the answer undermines by the two tests of the "Undermined pick test" decision (option no longer carried out, stated reason no longer holds), without re-forming the recommender's judgment, on every hand answer whether or not it matches the answered block's own pick, leaving standing the picks the answer does not bear on.
- That entry states that the named picks go to the same `remove` as `--undermined` and are reconciled with the `<depends-on>`-tagged dependents in one write, stripped with their alternatives kept and transitively, a named pick-less block left as it stands, an unknown or self-naming title refused with the document unchanged and the call re-run, strip on doubt covering both the `--option` verdict and the undermined-pick judgment, and nothing printed about cleared picks.
- The `/answer-open-question-with-alternative` entry states the same: the shared hand-answer procedure with the chosen id as recorded option, the whole read for reasoning only, the two-test judgment on every answer (choosing the block's own pick no exemption), the named picks passed as `--undermined` and reconciled with the tagged dependents in one write, alternatives kept and transitively, strip on doubt covering the naming, and nothing printed about cleared picks.
- The `/modify-milestone-goal` entry no longer says it edits the Goal and nothing else (no "Act-only" label remains): it states that the revision clears the standing picks it undermines, judged by the same two tests against the revised goal with doubt stripping, with one `strip --recommendation` call keeping every `<alternative>`, not transitive (a block whose `<depends-on>` names a cleared block keeps its pick and tag), as its only change to `open_questions.xml`, with `open_questions.xml` committed beside `requirements.md` under `Goal-revision: <milestone_id>`, as the "Goal revision pick clearing" decision requires.
- Claim 6 of `docs/design-claims.md` now states, in its Simplified Technical English register, that a hand answer names each recommendation it makes out of date and the same cascade strips those in the same write, and that a goal change strips each recommendation it makes out of date, keeping the alternatives, without continuing to the dependents.
- Claim 16 now states that when a hand answer or a goal change is possibly the cause of an out-of-date recommendation, the skill strips it and keeps the alternatives (strip on doubt).
- No changed passage carries a replay figure, as the "Replay result home" decision requires, and `uv run scripts/build_hosts.py --check` passes (no change under `core/`).

---

## Update CLAUDE.md Invariants For Undermined Picks

Revise the invariants in `CLAUDE.md` that this milestone changes, with their rationale: "One reconciliation engine, strip on doubt" gains the runner-named undermined dependents that ride the same `remove` write (judged in the composing hand-answer procedure so the core stays a pass-through recorder, no exemption when the answer matches the answered block's own pick, an unknown name refused but a pick-less one accepted, still no console advisory), and the `modify-milestone-goal` bullet and its line in the skill list record that a revision now clears the picks it undermines with one non-transitive `strip --recommendation` committed with the goal edit. Verified by reading the bullets against the Decisions and, as the milestone's closing check, by `uv run scripts/build_hosts.py --check`, `uv run pytest`, and `uv run --no-project --python 3.9 --with pytest pytest` all passing.

**Verified:**

- The "One reconciliation engine, strip on doubt" bullet of `CLAUDE.md` states that `remove` reconciles both `--option` and `--undermined` in its one write, the runner-named undermined dependents reconciled as dependents no `<depends-on>` tag declares, in the same write as the tagged ones, transitively and keeping their alternatives, with the rationale (a tag is the only record of what a pick assumed, so without the naming the sweep would record a pick formed without the answer).
- That bullet places the judgment in `core/shared/hand-answer-procedure.md`, composing over the answer core, so the core stays a pass-through recorder with one input and no branch and `answer-with-recommendation-procedure.md` passes nothing, as the "Undermined-pick judgment home" decision requires; it names the two tests of the "Undermined pick test" decision without re-forming the recommender's judgment.
- That bullet states that a match with the answered block's own pick is no exemption (the "Answer matching the standing pick" decision), that an unknown or self-naming title is refused with the document unchanged (the "Unknown named dependent" decision), that a named pick-less block is accepted, left as it stands, and seeds no transitive strip (the "Named dependent without a pick" decision), that doubt strips in both the `--option` verdict and the undermined-pick judgment, and that stripped, untagged, or named dependents still get no console advisory and no commit-body line (the "Cleared picks report" decision), each with its rationale.
- The `modify-milestone-goal` invariant bullet no longer calls the skill act-only: it records that a revision names the picks it undermines by the same two tests, doubt stripping, and clears them with one `strip --recommendation` keeping every `<alternative>`, not transitive (a block whose `<depends-on>` names a cleared block keeps its pick and tag), with `open_questions.xml` committed beside `requirements.md` under `Goal-revision:`, with the rationale for the clearing and for its non-transitivity, as the "Goal revision pick clearing" decision requires; no "act-only" wording remains in `CLAUDE.md`.
- The skill-list line for `modify-milestone-goal` records that it edits `## Goal` and clears the picks it undermines with one non-transitive strip committed with the goal edit.
- No changed passage carries a replay figure, as the "Replay result home" decision requires.
- `uv run scripts/build_hosts.py --check` passed, and `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` each passed all 544 tests.

---
