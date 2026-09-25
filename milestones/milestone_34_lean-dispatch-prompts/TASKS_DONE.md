# TASKS DONE

## Add the Question-Text List Flag

Give `list` in `core/tools/open_questions.py` a `--with-question` flag that prints each block on one line in document order as the un-escaped id, a single tab, then the un-escaped question text, changing only the line shape so it composes with `--without-alternatives` and `--without-recommendation` exactly as they select today, with no new refusal path. The docstring's `Subcommands:` section, the argparse help, and the output contract each state the tab separator, and `tests/test_list.py` gains tests asserting a literal tab, un-escaped values via the `entities` fixture, and the flag crossed with each filter alone and together. Verified by `uv run pytest` and the 3.9 floor run both passing and `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

**Verified:**

- `list --with-question` prints each selected block as the un-escaped id, one literal tab, then the un-escaped question text, one per line in document order (`tests/test_list.py` asserts the shape on the `annotated` and `bare` fixtures and un-escaped values on the `entities` fixture); without the flag the output is the bare id list as before, every existing `list` test still passing.
- The flag composes with `--without-alternatives` and `--without-recommendation`, alone and together, the filters selecting exactly the blocks they select without it, including a block whose recommendation alone was stripped; the diff adds no `ToolError`, so no new refusal path exists.
- The tab separator is stated at all three contract sites: the docstring's `Subcommands:` entry for `list`, the docstring's output contract, and the argparse `--with-question` help shown by `list --help`.
- `tests/test_list.py` gained tests asserting a literal tab (and no space beside it), un-escaped values via the `entities` fixture, the flag crossed with each filter alone and with both together, the empty-document and fully-annotated cases, the document left unchanged, and the in-process `main` path.
- `uv run pytest` passed (447 tests), the 3.9 floor run `uv run --no-project --python 3.9 --with pytest pytest` passed (447 tests), and `uv run scripts/build_hosts.py --check` passed after rebuilding `hosts/claude/` and `hosts/antigravity/`.

---
