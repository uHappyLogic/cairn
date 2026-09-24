# TASKS DONE

## Recommendation-First Renderer Child Order

Change `_question_lines` in `core/tools/open_questions.py` so a block carrying a `<recommendation>` renders, after its `<question>`, its `<applied-principle>` and `<depends-on>` elements, then the `<recommendation>`, then the one alternative the recommendation's option names, then the remaining alternatives in their existing relative order, while a block without a recommendation keeps today's order and an option naming none of the block's alternative ids promotes nothing (the recommendation half still renders first). The move is renderer-only and deterministic on every write: `sort` keeps ordering whole blocks only, `strip --recommendation` keeps the alternatives in their now-reordered list order, the parser still accepts any child order so an old-order document converts lazily on its next write, and no conversion subcommand is added. Verified by the existing suite still passing except the tests that pin the old order, and by rendering a recommendation-bearing block and observing the new order.

**Verified:**

- `_question_lines` in `core/tools/open_questions.py` renders a block carrying a `<recommendation>` as `<question>`, its `<applied-principle>` elements, its `<depends-on>` elements, the `<recommendation>`, the one alternative whose id the option names (matched with the tool's `id_key`), then the remaining alternatives in their existing relative order — observed by `locate` on a block whose option `c` named the third alternative `C`, printing `C`, `A`, `B` after the recommendation half.
- A block without a `<recommendation>` keeps today's order (`<question>`, the alternatives, `<applied-principle>`, `<depends-on>`) — observed on a block with alternatives `M`, `N` and a stray `<applied-principle>`.
- A recommendation whose option names none of the block's alternative ids still renders the recommendation half first and promotes nothing, with no write failure — observed on a block with option `Nope` over `X`, `Y`.
- The change is renderer-only: the parser still accepts any child order (an old-order document loads, `walk` leaves it byte-identical, and `sort` with no block moved writes nothing, the file comparing equal after the run), and it converts on the next writer save (`add` rewrote an old-order block recommendation-first with its named alternative promoted); no conversion subcommand was added.
- `strip --recommendation` on a block saved in the new order keeps its alternatives in their reordered list order (`B`, `A`).
- `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both report 400 passed, 27 failed, and every failure pins the old order: with the `annotated` and `entities` golden fixtures re-rendered through the tool in a scratch copy, only 6 remain, each a literal expected block in `tests/test_embed.py` or `tests/test_format.py` that places the alternatives before the recommendation half (realigned by the later test task).

---

## Update Canonical-Form Contract Text

Reword the canonical-form statement in the module docstring (the `--help` text) and the `embed` help of `core/tools/open_questions.py` so they state the new order once: a recommendation-bearing block groups its children as `<question>`, `<applied-principle>`, `<depends-on>`, `<recommendation>`, the named alternative, then the rest in relative order, and a block without a recommendation keeps `<question>`, the `<alternative>` elements, `<applied-principle>`, `<depends-on>`. This is the one place child order is stated, so the wording must cover the unmatched-option case (no promotion). Verified by `--help` output reading correctly and `tests/test_contract.py` passing.

**Verified:**

- The canonical-form bullet of the module docstring in `core/tools/open_questions.py` states the order once: a block carrying a `<recommendation>` renders `<question>`, `<applied-principle>`, `<depends-on>`, `<recommendation>`, the one `<alternative>` the option names, then the other alternatives in their relative order; a block carrying none renders `<question>`, the alternatives in their relative order, `<applied-principle>`, `<depends-on>`.
- The same bullet covers the unmatched-option case: an option naming none of the alternatives promotes nothing, and the alternatives keep their relative order after the recommendation. It also states that the written order becomes the stored relative order, so a later `strip --recommendation` keeps it.
- The docstring's `embed` entry and the argparse `embed` help no longer restate an order. Each says the other half's elements stay as the block holds them and the whole block is written in the canonical child order stated in the module docstring's document format. The retired "grouped by kind in the canonical order" and "written grouped by kind" wording is gone.
- `python3 core/tools/open_questions.py --help` and `embed --help` read correctly and exit 0.
- `tests/test_contract.py` passes under both `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` (11 passed each). The full suite is unchanged from the previous task at 400 passed and 27 failed, and every failure pins the old child order.

---

## Realign Renderer Tests And Fixtures

Update `tests/test_format.py`'s `NON_CANONICAL`/`CANONICAL` pin and the `tests/fixtures/annotated/open_questions.xml` golden file to the new child order so the round-trip identity holds, and add tests covering promotion of the named alternative, the unmatched-option case rendering the recommendation half first with no promotion and no write failure, a block without a recommendation keeping today's order, an old-order document staying as written until a writer next saves it, `sort` writing nothing when no block moved even on an old-order document, and `strip --recommendation` keeping the reordered alternative order. Verified by `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both passing.

**Verified:**

- `tests/fixtures/annotated/open_questions.xml` and `tests/fixtures/entities/open_questions.xml` are re-rendered through the tool so every recommendation-bearing block reads `<question>`, `<applied-principle>`, `<depends-on>`, `<recommendation>`, then its alternatives (the named one already first in both); the golden round-trip identity holds for all four fixtures.
- `tests/test_format.py`'s `CANONICAL` pin renders `NON_CANONICAL` recommendation half first with the named alternative `Second` promoted ahead of `First`, and the five literal expected blocks in `tests/test_embed.py` that placed alternatives before the recommendation half are realigned to the new order.
- New tests cover promotion of the named alternative (`test_render_promotes_the_named_alternative_and_keeps_the_rest_in_relative_order`, `test_render_of_an_already_first_named_alternative_moves_only_the_recommendation_half`, and `test_embed_recommendation_promotes_the_named_alternative_and_keeps_the_set_frozen`).
- New tests cover the unmatched-option case rendering the recommendation half first with no promotion (`test_render_of_an_unmatched_option_puts_the_recommendation_half_first_and_promotes_nothing`) and with no write failure, since `add` saves such a document with exit 0 (`test_a_writer_saves_a_block_with_an_unmatched_option_without_failing`).
- A new test covers a block without a recommendation keeping today's order (`test_render_of_a_block_without_a_recommendation_keeps_the_alternatives_first`).
- A new test covers an old-order document staying byte-identical through `list`, `list --without-recommendation`, `walk`, `locate`, `lift`, and `sort`, then being rewritten recommendation-first with its named alternative promoted by the next `add` (`test_an_old_order_document_stays_as_written_until_a_writer_next_saves_it`).
- A new test covers `sort` writing nothing when no block moved on an old-order document: the bytes, inode, and mtime are unchanged, even though a re-render would differ (`test_sort_writes_nothing_when_no_block_moved_even_on_an_old_order_document`).
- A new test covers `strip --recommendation` keeping the reordered alternative order `C`, `A`, `B` in both the model and the file (`test_strip_recommendation_keeps_the_reordered_alternative_order`).
- `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both report 436 passed, 0 failed.

---

## Reword Alternatives-Untouched Contract Sites

Replace every claim that the recommendation pass or `embed --recommendation` leaves a block's `<alternative>` children untouched, in `core/skills/recommend-all-open-questions/SKILL.md`, `docs/skill-reference.md`, `docs/workflow.md`, and the `CLAUDE.md` invariants, with the frozen-set guarantee those files already use elsewhere: the pass never adds, drops, or edits an alternative, and none of these sites states child order. Confirm no skill prose positions elements itself and that the capture skill's element-agnostic reconstruction needs no change. Verified by grepping those files for the retired wording and finding none.

**Verified:**

- `core/skills/recommend-all-open-questions/SKILL.md` no longer says the pass "never touches a block's `<alternative>` children" (opening paragraph now: "never adds, drops, or edits a block's `<alternative>` — it only picks and orders") or that `embed --recommendation` leaves "its `<alternative>` children untouched" (the embed step now: "adding, dropping, and editing no `<alternative>`").
- `docs/skill-reference.md`'s recommendation-pass entry now says `embed --recommendation` writes the block "without adding, dropping, or editing an `<alternative>`", and `docs/workflow.md` now says `embed --recommendation` "never adds, drops, or edits an `<alternative>`".
- The `CLAUDE.md` invariants carry no alternatives-untouched claim (their only `<alternative>` statements are the cascade never clearing one and a stripped dependent keeping its alternatives, both still true), so no edit was needed there.
- None of the reworded sentences states child order; the order stays stated only in the tool's module docstring and `--help`.
- No skill, shared procedure, or agent prose positions elements itself: every order mention defers to the tool's canonical form. `core/skills/capture-milestone-principle-updates/SKILL.md` reconstructs the answered block keyed on tags between its boundary lines and reads alternatives in document order as the options the user saw, which stays true under the new order, so it needs no change.
- Grepping the four files for `never touches` and `` `<alternative>` children untouched `` finds nothing; `uv run pytest` reports 436 passed.

---
