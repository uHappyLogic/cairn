# TASKS TODO

## Describe Undermined-Pick Clearing In Docs

Update the `docs/skill-reference.md` entries for `/answer-open-question`, `/answer-open-question-with-alternative`, and `/modify-milestone-goal`, and the design text of claims 6 and 16 in `docs/design-claims.md`, to describe the new behaviour: a hand answer names the standing picks it undermines and `remove` reconciles them with the tagged dependents in one write, strip on doubt covering that judgment, and a goal revision clears the picks it undermines with one non-transitive `strip --recommendation`, so the `/modify-milestone-goal` entry no longer says it edits the Goal and nothing else. Verified by reading each changed passage against the Decisions.

---

## Update CLAUDE.md Invariants For Undermined Picks

Revise the invariants in `CLAUDE.md` that this milestone changes, with their rationale: "One reconciliation engine, strip on doubt" gains the runner-named undermined dependents that ride the same `remove` write (judged in the composing hand-answer procedure so the core stays a pass-through recorder, no exemption when the answer matches the answered block's own pick, an unknown name refused but a pick-less one accepted, still no console advisory), and the `modify-milestone-goal` bullet and its line in the skill list record that a revision now clears the picks it undermines with one non-transitive `strip --recommendation` committed with the goal edit. Verified by reading the bullets against the Decisions and, as the milestone's closing check, by `uv run scripts/build_hosts.py --check`, `uv run pytest`, and `uv run --no-project --python 3.9 --with pytest pytest` all passing.

---

