# TASKS TODO

## Remove Create From Open-Question Tool

Remove the `create` subcommand from `core/tools/open_questions.py` (`cmd_create`, its parser registration, and its docstring entry) so the tool works only on documents that already exist, and reword the module docstring's sole-writer claim so `define_milestone.py` creates the document and this tool is its only writer after that. Delete `tests/test_create.py`, keeping only its check that the `empty` fixture is what the serializer renders for no questions, and rewrite the `tests/test_contract.py` cases that drive `create` against a surviving subcommand. Verified by both suite runs passing, `python3 core/tools/open_questions.py --help` no longer listing `create`, and both host trees rebuilt so `--check` passes.

---

## Reword Documentation For Two Tools

Following the Documentation of two tools decision, replace every tool-count statement with count-free wording (`CLAUDE.md`'s "one stdlib-only Python tool", its sole-writer invariant, and its tests layout line, `CONTRIBUTING.md`'s "the one program", `README.md`'s account of who writes `open_questions.xml`, `docs/workflow.md`'s "exactly one writer" and define-step sentences, the `init-milestone-base-workflow` step 2 Python-check justification, and the like), reword the sole-writer rule so `define_milestone.py` creates the document and the open-question tool is its only writer after that, and name `define_milestone.py` only in the `CLAUDE.md` repository layout line and the `define-milestone-goal` entry of `docs/skill-reference.md`, which now describes the tool-driven definition. The invocation shape in `docs/ways-of-using-cairn.md`, the `discuss-milestone-goal` handoff, and `CONTRIBUTING.md`'s reservation step stay as they are, and a `{{PLUGIN_ROOT}}/…` reference must still name a file, never the `tools/` directory, or the build rejects it. Verified by `grep` finding no remaining `create` subcommand reference or single-tool count in the repository's prose, and by both host trees rebuilt so `uv run scripts/build_hosts.py --check` passes.

---
