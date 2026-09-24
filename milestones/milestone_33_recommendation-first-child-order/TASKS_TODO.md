# TASKS TODO

## Reword Alternatives-Untouched Contract Sites

Replace every claim that the recommendation pass or `embed --recommendation` leaves a block's `<alternative>` children untouched, in `core/skills/recommend-all-open-questions/SKILL.md`, `docs/skill-reference.md`, `docs/workflow.md`, and the `CLAUDE.md` invariants, with the frozen-set guarantee those files already use elsewhere: the pass never adds, drops, or edits an alternative, and none of these sites states child order. Confirm no skill prose positions elements itself and that the capture skill's element-agnostic reconstruction needs no change. Verified by grepping those files for the retired wording and finding none.

---

## Rebuild Host Trees After Renderer Change

Run `uv run scripts/build_hosts.py` so both `hosts/claude` and `hosts/antigravity` carry the changed tool source and skill prose, then confirm `uv run scripts/build_hosts.py --check` passes so `main` stays drift-free. Verified by the `--check` run exiting cleanly.

---
