# TASKS TODO

## Add Definition Tool Test Suite

Add flat per-concern test files under `tests/` for `define_milestone.py`, one per concern named in the Test suite extension decision (numbering and padding, slug derivation, conflicts, failure cleanup, output and exit contract), plus the parity test from the Creating open_questions.xml decision that the written document parses with `open_questions.load_document` and equals `render_document(Document())`. Extend `conftest.py` with a second pinned tool path, a `run_define` subprocess fixture beside `run_tool`, and a helper that builds milestone-root layouts under `tmp_path`, changing no `pyproject.toml` setting. Verified by both suite runs passing, `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest`, with no `__pycache__` left under `core/tools/`.

---

## Rewrite Define Skill Around Tool

Rewrite `core/skills/define-milestone-goal/SKILL.md` so its single `<overall_goal_description>` argument stays and the model's only work is choosing the title, running `python3 {{PLUGIN_ROOT}}/tools/define_milestone.py --title` with the goal text on stdin as a quoted heredoc, handing the tool's two printed lines unchanged to the commit procedure as PATHS (the directory) and SUBJECT, and printing `Milestone defined.` or the distinct no-change line, while a failure quotes the tool's `Error:` line or the shell's missing-interpreter line verbatim and stops. The number, slug, and conflict steps are gone, the skill names the four files the tool creates and states none of their contents, and its frontmatter description stays one clause of 25 words or fewer. Verified by rebuilding both host trees so `uv run scripts/build_hosts.py --check` passes and by one run of the rewritten steps in a throwaway git repository that ends in a `Milestone-definition:` commit holding exactly the four files.

---

## Remove Create From Open-Question Tool

Remove the `create` subcommand from `core/tools/open_questions.py` (`cmd_create`, its parser registration, and its docstring entry) so the tool works only on documents that already exist, and reword the module docstring's sole-writer claim so `define_milestone.py` creates the document and this tool is its only writer after that. Delete `tests/test_create.py`, keeping only its check that the `empty` fixture is what the serializer renders for no questions, and rewrite the `tests/test_contract.py` cases that drive `create` against a surviving subcommand. Verified by both suite runs passing, `python3 core/tools/open_questions.py --help` no longer listing `create`, and both host trees rebuilt so `--check` passes.

---

## Reword Documentation For Two Tools

Following the Documentation of two tools decision, replace every tool-count statement with count-free wording (`CLAUDE.md`'s "one stdlib-only Python tool", its sole-writer invariant, and its tests layout line, `CONTRIBUTING.md`'s "the one program", `README.md`'s account of who writes `open_questions.xml`, `docs/workflow.md`'s "exactly one writer" and define-step sentences, the `init-milestone-base-workflow` step 2 Python-check justification, and the like), reword the sole-writer rule so `define_milestone.py` creates the document and the open-question tool is its only writer after that, and name `define_milestone.py` only in the `CLAUDE.md` repository layout line and the `define-milestone-goal` entry of `docs/skill-reference.md`, which now describes the tool-driven definition. The invocation shape in `docs/ways-of-using-cairn.md`, the `discuss-milestone-goal` handoff, and `CONTRIBUTING.md`'s reservation step stay as they are, and a `{{PLUGIN_ROOT}}/…` reference must still name a file, never the `tools/` directory, or the build rejects it. Verified by `grep` finding no remaining `create` subcommand reference or single-tool count in the repository's prose, and by both host trees rebuilt so `uv run scripts/build_hosts.py --check` passes.

---
