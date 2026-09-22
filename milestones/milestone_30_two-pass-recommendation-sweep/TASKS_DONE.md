# TASKS DONE

## Tool Partial Strip Flag

Add a `--recommendation` mode to the `strip` subcommand of `core/tools/open_questions.py` that clears only the `<recommendation>`, `<depends-on>`, and `<applied-principle>` children of each named block and leaves its `<alternative>` children standing, implemented as the one shared per-block primitive the cascade will reuse, while bare `strip` keeps clearing every child. The milestone needs it as the cheap revision hatch of the inline recommendation pass. Verified by `tests/test_strip.py` pinning both forms under both pytest runs with the existing strip-to-bare tests left true.

**Verified:**

- `strip <MILESTONE_DIR> --recommendation <SHORT_TITLE>...` deletes only the `<recommendation>`, `<depends-on>`, and `<applied-principle>` children of each named block and leaves its `<alternative>` children standing verbatim, touching no other block and no `<depends-on>` tag naming it; the flag is accepted before or after the titles and before the directory
- Bare `strip` still deletes every child but `<question>`; every pre-existing strip-to-bare test in `tests/test_strip.py` passes unchanged, and `remove`'s cascade still calls the full `strip_question` (the narrowed cascade is the next task's)
- The partial strip is one named per-block primitive, `strip_recommendation(question)`, returning whether it deleted anything, and `strip_question` composes over it, so the cascade can reuse it with a one-call swap
- A block with nothing the mode would delete (alternatives-only or bare) triggers no write — document bytes, inode, and mtime unchanged — and an unknown id is refused with the usual one `Error:` line listing the document's ids, document unchanged
- `tests/test_strip.py` pins both forms (17 new `--recommendation` tests beside the existing ones); `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both pass, 364 tests each
- Host trees rebuilt with `uv run scripts/build_hosts.py`; `hosts/claude/tools/open_questions.py` and `hosts/antigravity/tools/open_questions.py` are byte-identical to `core/tools/open_questions.py` and `uv run scripts/build_hosts.py --check` passes

---
## Tool Narrowed Answer Cascade

Change `remove` so every option-less removal and every disagreeing dependent takes the partial strip — clearing the `<recommendation>`, `<depends-on>`, and `<applied-principle>` children but keeping the `<alternative>` children — transitively over dependents of stripped blocks as today. That keeps the parallel pass's alternatives across answers, so an override costs only a re-run of the recommendation pass. Verified by `tests/test_remove.py` re-pinned to the kept-alternatives outcome and both pytest runs passing.

**Verified:**

- `remove_question` passes every option-less and every disagreeing dependent to `strip_recommendation` instead of `strip_question`, transitively over `dependents_of` each stripped block exactly as before, so a stripped dependent keeps its `<alternative>` children verbatim and loses only its `<recommendation>`, `<depends-on>`, and `<applied-principle>` children — never again reading as bare
- Agreeing dependents still lose only the tag, no `<depends-on>` tag is left naming a removed or stripped block, every surviving block's alternatives are unchanged by any removal (pinned over the annotated fixture and the seven-block dependency web with every option), and an `--option` naming none of the removed block's alternatives is still refused with the document unchanged
- The tool's module usage text, the `remove_question` docstring, and the `remove` parser help state the narrowed contract ("stripped as by strip --recommendation, keeping its <alternative> elements"); no runtime prose file changed, that being the later prose task's
- `tests/test_remove.py` is re-pinned to the kept-alternatives outcome: the strip-to-bare helper and every `is_bare`/bare-block assertion on a stripped dependent are replaced by the `pick_stripped`, `stripped`, and `stripped_lines` helpers, the dangling-tag tests detect a stripped block by its lost `<recommendation>`, and two new tests pin that a cascade strip keeps the alternatives line-for-line and never produces the bare block
- `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both pass, 365 tests each
- Host trees rebuilt with `uv run scripts/build_hosts.py`; `hosts/claude/tools/open_questions.py` and `hosts/antigravity/tools/open_questions.py` are byte-identical to `core/tools/open_questions.py` and `uv run scripts/build_hosts.py --check` passes

---
## Tool List Alternatives Filters

Retire `list --unannotated` and give `list` two symmetric filters, `--without-alternatives` (blocks carrying no `<alternative>` children) and `--without-recommendation` (today's `--unannotated` meaning), re-pointing the five test files that spell the old flag (`test_list.py`, `test_sort.py`, `test_walk.py`, `test_embed.py`, `test_strip.py`). The alternatives pass dispatches on the first filter, the recommendation pass stops on it and skips on the second. Verified by both pytest runs passing with no `--unannotated` left under `core/tools/` or `tests/`.

**Verified:**

- `list <MILESTONE_DIR> --without-alternatives` prints only the blocks carrying no `<alternative>` child and `list <MILESTONE_DIR> --without-recommendation` only the blocks carrying no `<recommendation>` child (today's `--unannotated` meaning, unchanged); either flag is accepted before or after the directory, both together print only the blocks carrying neither, and a block whose recommendation alone was stripped (`strip --recommendation`) prints under the second filter and not the first
- `--unannotated` is retired: argparse rejects it as an unrecognized argument with exit 2, and grep finds no `--unannotated` under `core/tools/` or `tests/`
- The five test files that spelled the old flag (`test_list.py`, `test_sort.py`, `test_walk.py`, `test_embed.py`, `test_strip.py`) are re-pointed to `--without-recommendation`, and `tests/test_list.py` pins both filters (each alone over the annotated, bare, entities, and empty fixtures, both together, the partially-stripped block, and the document left unchanged)
- The tool's module usage text and the `list` parser help name both flags and state that a block prints under both only when it carries neither
- `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest` both pass, 371 tests each
- Host trees rebuilt with `uv run scripts/build_hosts.py`; `hosts/claude/tools/open_questions.py` and `hosts/antigravity/tools/open_questions.py` are byte-identical to `core/tools/open_questions.py` and `uv run scripts/build_hosts.py --check` passes

---
