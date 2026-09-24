# TASKS TODO

## Realign Renderer Tests And Fixtures

Update `tests/test_format.py`'s `NON_CANONICAL`/`CANONICAL` pin and the `tests/fixtures/annotated/open_questions.xml` golden file to the new child order so the round-trip identity holds, and add tests covering promotion of the named alternative, the unmatched-option case rendering the recommendation half first with no promotion and no write failure, a block without a recommendation keeping today's order, an old-order document staying as written until a writer next saves it, `sort` writing nothing when no block moved even on an old-order document, and `strip --recommendation` keeping the reordered alternative order. Verified by `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both passing.

---

## Reword Alternatives-Untouched Contract Sites

Replace every claim that the recommendation pass or `embed --recommendation` leaves a block's `<alternative>` children untouched, in `core/skills/recommend-all-open-questions/SKILL.md`, `docs/skill-reference.md`, `docs/workflow.md`, and the `CLAUDE.md` invariants, with the frozen-set guarantee those files already use elsewhere: the pass never adds, drops, or edits an alternative, and none of these sites states child order. Confirm no skill prose positions elements itself and that the capture skill's element-agnostic reconstruction needs no change. Verified by grepping those files for the retired wording and finding none.

---

## Rebuild Host Trees After Renderer Change

Run `uv run scripts/build_hosts.py` so both `hosts/claude` and `hosts/antigravity` carry the changed tool source and skill prose, then confirm `uv run scripts/build_hosts.py --check` passes so `main` stays drift-free. Verified by the `--check` run exiting cleanly.

---
