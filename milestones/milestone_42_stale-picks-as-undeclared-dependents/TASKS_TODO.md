# TASKS TODO

## Route Both Hand-Answer Skills Through Procedure

Change `core/skills/answer-open-question/SKILL.md` and `core/skills/answer-open-question-with-alternative/SKILL.md` to follow the new shared hand-answer procedure in place of `answer-procedure.md` directly, the literal skill still passing no RECORDED OPTION and the alternative skill still passing its lifted id, so every hand answer runs the undermined-pick judgment. The alternative skill's "never read or edit it yourself" sentence and the literal skill's "every read and write of it in the core is a tool call" statement are reworded to the form the other inline skills carry (a whole read is for reasoning only, and every locate, list, lift, and write is a tool call), while each skill's reporting step and commit body stay as they stand, with nothing printed or recorded about any cleared pick. Verified by reading both skills against the "Undermined-pick judgment home", "Standing picks view", and "Cleared picks report" decisions, `hosts/` rebuilt, and `uv run scripts/build_hosts.py --check` passing.

---

## Clear Undermined Picks On Goal Revision

Extend `core/skills/modify-milestone-goal/SKILL.md` so that, in the same run as the goal edit, the skill names the standing picks its impact analysis judges the revision undermines (by the "Undermined pick test" decision's definition, read against the revised goal) from its existing whole read of `open_questions.xml`, and clears them with one `strip --recommendation` call over those Short Titles, keeping every `<alternative>`. The clearing is not transitive (a block whose `<depends-on>` names a cleared block keeps its pick and its tag), the tool is unchanged, and `open_questions.xml` joins `requirements.md` in the `Goal-revision:` commit, which closes the route by which a pick formed under the old goal reaches the answer sweep. Verified by reading the skill against the "Goal revision pick clearing" decision, its edit step and commit PATHS agreeing with it, `hosts/` rebuilt, and `uv run scripts/build_hosts.py --check` passing.

---

## Fix Hand Labels And Replay Result Bar

With the maintainer, inline and before any replay run, complete the local case manifest: the maintainer reads each case and labels every standing pick stale or unaffected by the "Undermined pick test" decision's definition, then sets the bar on both counts (an absolute threshold on stale picks cleared and one on unaffected picks left standing) together with the fixed number of revision-and-re-run rounds a shortfall buys, possibly none. No label or value comes from the runner or from any automated record (the historical sweep advisory and later history serve at most to point at candidates), and once written the labels are never changed. Verified when every standing pick of every case carries a label, both thresholds and the round count are written in the manifest, and `git status` shows no change outside `temp/`.

---

## Run Stale-Pick Replay And Record Aggregates

Replay every case of the labelled manifest with a runner kept outside the tracked files: a scratch clone of the case's own repository at the parent of its hand answer, the matching hand-answer skill (or `/modify-milestone-goal` for a goal-revision case) run headless against the rebuilt plugin tree, and each standing pick then counted against its fixed label as a stale pick cleared or an unaffected pick left standing, with no paired baseline run. The two totals are judged against the bar fixed beforehand; a shortfall on either count buys only the fixed number of revision-and-re-run rounds of the judgment prose set with the bar, after which the task completes with the change in place and the shortfall recorded. Done when both counts are measured over every case and recorded with the bar in this task's **Verified:** bullets as aggregate figures only (no repository or project name, question title, commit hash, or decision text), and `git status` shows no replay material among the tracked files.

---

## Describe Undermined-Pick Clearing In Docs

Update the `docs/skill-reference.md` entries for `/answer-open-question`, `/answer-open-question-with-alternative`, and `/modify-milestone-goal`, and the design text of claims 6 and 16 in `docs/design-claims.md`, to describe the new behaviour: a hand answer names the standing picks it undermines and `remove` reconciles them with the tagged dependents in one write, strip on doubt covering that judgment, and a goal revision clears the picks it undermines with one non-transitive `strip --recommendation`, so the `/modify-milestone-goal` entry no longer says it edits the Goal and nothing else. The text carries no figure from the replay, since no file outside the milestone directory may. Verified by reading each changed passage against the Decisions and finding no replay number under `docs/`.

---

## Update CLAUDE.md Invariants For Undermined Picks

Revise the invariants in `CLAUDE.md` that this milestone changes, with their rationale: "One reconciliation engine, strip on doubt" gains the runner-named undermined dependents that ride the same `remove` write (judged in the composing hand-answer procedure so the core stays a pass-through recorder, no exemption when the answer matches the answered block's own pick, an unknown name refused but a pick-less one accepted, still no console advisory), and the `modify-milestone-goal` bullet and its line in the skill list record that a revision now clears the picks it undermines with one non-transitive `strip --recommendation` committed with the goal edit. No figure from the replay is written. Verified by reading the bullets against the Decisions and, as the milestone's closing check, by `uv run scripts/build_hosts.py --check`, `uv run pytest`, and `uv run --no-project --python 3.9 --with pytest pytest` all passing.

---

