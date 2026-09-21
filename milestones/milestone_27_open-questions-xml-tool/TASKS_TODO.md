# TASKS TODO

## Repoint Capture Diff Reconstruction

Repoint `capture-milestone-principle-updates` so its answer-commit walk filters on `-- milestones/<milestone_id>/open_questions.xml`, each `git show` names both `open_questions.xml` and `requirements.md`, the removed lines of the `open_questions.xml` hunk feed the block reconstruction and the added lines of the `requirements.md` hunk fill the recorded decision, and the pre-split blockquote fallback is dropped since no compatibility with pre-split milestones is provided. Every other rule of the per-commit read stays uniform, verified by the rendered skill and a passing host rebuild.

---

## Sync CLAUDE.md Invariants To Tool

Rewrite `CLAUDE.md` for the split: the repository layout entries (add `core/tools/open_questions.py`, `tests/`, the CI pytest steps, and the four-directory host tree), the milestone file structure listing four files, and every invariant that spells out the boundary-line CLI, the five-entity rule, the seven-test gate, the whole-block-replacement embed, the prose graph walk, or the hand-edit hatch, so each states the tool's contract and the judgment the prose keeps instead. Verified by a `boundary-line`/`xmllint`/`awk` grep returning only historical mentions and by the file reading consistently against the rendered host trees.

---

## Sync README Docs And Contributing

Update `README.md` (Python 3.9+ prerequisite under `## Installation`, the four-file milestone list, the design-principle line for claim 11), both `scripts/hosts/<host>/README.md` templates (the same prerequisite), `docs/design-claims.md` claim 11, `docs/workflow.md`'s query-convention paragraph, the eight question-skill entries in `docs/skill-reference.md`, `CONTRIBUTING.md`'s Development section (the two pytest commands beside the build loop), and the repository's own `milestones/README.md` file description, stating that pre-split milestones get no migration. Verified by a rebuild with `uv run scripts/build_hosts.py --check` passing and no remaining boundary-line description in the docs.

---
