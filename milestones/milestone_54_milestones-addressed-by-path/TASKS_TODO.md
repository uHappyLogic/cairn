# TASKS TODO

## Docs and Invariants Follow the Path Form

Rewrite the documentation to the path-addressed shape: every chain in `docs/ways-of-using-cairn.md` carries `--milestone <path>` from the definition line's printed path, with the activation line gone, the definition line taking `--at`, and finish described as removal; `docs/workflow.md`'s stages, diagram labels, and committing paragraph; `docs/design-claims.md` claims 9 and 10; `README.md`'s how-it-works and self-dogfooding paragraphs; `CONTRIBUTING.md`'s contributor flow, where the maintainer reserves with `/define-milestone-goal --at <scope>` on `main`, the contributor branches from that commit and runs the pipeline with `--milestone <path>`, and the goto step and the pointer conditions on reserving and merging go, the pull request template's milestone field naming the reserved path; `ideas/benchmark_for_cairn.md`'s bootstrap and activation lines; and `CLAUDE.md`'s layout, skill list, file-structure, and invariant sections, retiring the pointer, goto, and finish-precedes-goto invariants, rewriting the pre-split and pre-flip notes for what the migration leaves in history, and describing resolution, definition, finish, the commit tool's two new inputs, the tool's queries, and the migration as landed, while leaving its `## Milestone Workflow` tail for the migration's closing commit. Verified by the fixed-lines test, `--check`, and a read-through finding no pointer, activation, or README-history reference outside recorded history.

---

## Gate the Four Task Writers

Add one shared procedure under `core/shared/` stating the `gate` call, what a held scope means, and its one fixed stop line with the holder paths beneath it, and reference it as a separate step before the fixed write call in `derive-tasks` and `submit-task`, before each dispatch in `complete-all-tasks`, and after the procedure's step 1 in the `complete-task` skill, each runner stopping when the captured print is non-empty, with the write calls, `complete-procedure.md`, and the agent unchanged and design claim 9, the fixed-lines table, and `CLAUDE.md` gaining the gate in place of the pointer. This task stands last among the implementation tasks; it is verified by the fixed-lines test, the rebuilt trees, and a refused task entry in a scratch repository holding two started milestones in one container.

---

## Revise the Draft After Migration

Revise "Carrying it out" in `ideas/milestones_addressed_by_path.md` so its step 3 records what landed as the sections for steps 1 and 2 do, marking it done and noting what it found for step 4 (the `live` filter, the record's missing bars, what the migration and the gate met on this repository), its date line extended. Its precondition is that this repository's own `/migrate-milestones` run has landed, so `milestones/README.md` is gone: it is completed alone, in a fresh session after that run, by the inline `/complete-task --milestone <path>`, and `/finish-milestone --milestone <path>` follows it; verified by a read of the revised section against the milestone's commits.

---
