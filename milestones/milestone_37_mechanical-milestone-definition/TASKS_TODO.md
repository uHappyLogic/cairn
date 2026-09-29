# TASKS TODO

## Reword Documentation For Two Tools

Following the Documentation of two tools decision, replace every tool-count statement with count-free wording (`CLAUDE.md`'s "one stdlib-only Python tool", its sole-writer invariant, and its tests layout line, `CONTRIBUTING.md`'s "the one program", `README.md`'s account of who writes `open_questions.xml`, `docs/workflow.md`'s "exactly one writer" and define-step sentences, the `init-milestone-base-workflow` step 2 Python-check justification, and the like), reword the sole-writer rule so `define_milestone.py` creates the document and the open-question tool is its only writer after that, and name `define_milestone.py` only in the `CLAUDE.md` repository layout line and the `define-milestone-goal` entry of `docs/skill-reference.md`, which now describes the tool-driven definition. The invocation shape in `docs/ways-of-using-cairn.md`, the `discuss-milestone-goal` handoff, and `CONTRIBUTING.md`'s reservation step stay as they are, and a `{{PLUGIN_ROOT}}/…` reference must still name a file, never the `tools/` directory, or the build rejects it. Verified by `grep` finding no remaining `create` subcommand reference or single-tool count in the repository's prose, and by both host trees rebuilt so `uv run scripts/build_hosts.py --check` passes.

---
