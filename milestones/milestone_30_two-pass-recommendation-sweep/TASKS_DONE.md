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
