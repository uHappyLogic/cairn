# TASKS TODO

## Rewire Answer Sweep Orchestrator

Rewire `answer-all-open-questions-with-recommendation` to gather and order its questions with one tool walk call, to run each pre-dispatch re-check as a `lift` call whose failure is the skip and whose printed text is the commit body, and to commit each answer's staged `open_questions.xml` and `requirements.md` under `Recommendation-answer: <Short Title>`, deleting the prose graph walk, origin promotion, and re-read rules the tool now owns while keeping strictly sequential dispatch and the one-commit-per-answer rule. Verified by the rendered skill and a passing host rebuild.

---

## Rewire Recommend Sweep Orchestrator

Rewire `recommend-all-open-questions` to gather in three tool calls — bare `list` (empty document stops the run), `list --unannotated` (empty means nothing to annotate), then `locate` over the surviving ids whose verbatim blocks are both the ranking input and the dispatch prompt — and to judge each return by the last-line `FAILED:` verdict alone before piping the whole message to `embed` through a quoted-delimiter heredoc, filling the one-slot repair template with the tool's `Error:` line, retaining one repair per question and the skip advisory. Delete the seven-test gate, its reason strings, and the whole-block-replacement `Edit`, state the hand-clear as `strip` followed by a re-run with no hand-edit exception, and commit `open_questions.xml` under `Recommendation-annotation:`; verified by the rendered skill and a passing host rebuild.

---

## Rewire Read-Only Question Consumers

Repoint every whole-set reader at `<MILESTONE_DIR>/open_questions.xml` read directly with the file-reading tool for reasoning only — the `recommend-open-question` agent's grounding, `core/shared/recommend-procedure.md`'s sibling read, `discuss-open-question`'s context step (its locate via the tool), `ask-in-milestone-context`, and `modify-milestone-goal`'s impact analysis — each carrying the one rule that every locate, list, or lift goes through the tool, and drop the agent's indentation and escaping rules that `embed` now normalizes while keeping its element rendering and two-test self-check. Verified by the rendered files naming no `requirements.md` question read and a passing host rebuild.

---

## Rewire Review Pass And Derive Precondition

Rewire `review-milestone-requirements` to author each new question with `add`, prune or dedup with bare `remove` (which strips dependents transitively), read `open_questions.xml` whole for reconciliation, report convergence as an empty `list`, and commit both `open_questions.xml` and `requirements.md` under `Requirements-review:`; rewire `derive-tasks` so its precondition is a `list` call whose non-empty output is the stop message's Short Titles. Verified by the rendered skills and a passing host rebuild.

---

## Repoint Capture Diff Reconstruction

Repoint `capture-milestone-principle-updates` so its answer-commit walk filters on `-- milestones/<milestone_id>/open_questions.xml`, each `git show` names both `open_questions.xml` and `requirements.md`, the removed lines of the `open_questions.xml` hunk feed the block reconstruction and the added lines of the `requirements.md` hunk fill the recorded decision, and the pre-split blockquote fallback is dropped since no compatibility with pre-split milestones is provided. Every other rule of the per-commit read stays uniform, verified by the rendered skill and a passing host rebuild.

---

## Sync CLAUDE.md Invariants To Tool

Rewrite `CLAUDE.md` for the split: the repository layout entries (add `core/tools/open_questions.py`, `tests/`, the CI pytest steps, and the four-directory host tree), the milestone file structure listing four files, and every invariant that spells out the boundary-line CLI, the five-entity rule, the seven-test gate, the whole-block-replacement embed, the prose graph walk, or the hand-edit hatch, so each states the tool's contract and the judgment the prose keeps instead. Verified by a `boundary-line`/`xmllint`/`awk` grep returning only historical mentions and by the file reading consistently against the rendered host trees.

---

## Sync README Docs And Contributing

Update `README.md` (Python 3.9+ prerequisite under `## Installation`, the four-file milestone list, the design-principle line for claim 11), both `scripts/hosts/<host>/README.md` templates (the same prerequisite), `docs/design-claims.md` claim 11, `docs/workflow.md`'s query-convention paragraph, the eight question-skill entries in `docs/skill-reference.md`, `CONTRIBUTING.md`'s Development section (the two pytest commands beside the build loop), and the repository's own `milestones/README.md` file description, stating that pre-split milestones get no migration. Verified by a rebuild with `uv run scripts/build_hosts.py --check` passing and no remaining boundary-line description in the docs.

---
