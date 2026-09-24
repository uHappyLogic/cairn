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
