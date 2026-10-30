# TASKS TODO

## Gate Query Over Started Milestones

Add the `gate MILESTONE_PATH` query to `core/tools/milestones.py`: it refuses a shallow repository (`git rev-parse --is-shallow-repository` printing `true`, naming `git fetch --unshallow`) and a path with no `milestones/` container, each on one `Error:` line with exit 1, and otherwise prints, one bare path per line, every other live milestone that is started (its `TASKS_TODO.md` modified after its creation, by the path-scoped `git log -1 --diff-filter=M` test) and whose scope equals, contains, or lies under the named milestone's scope, exiting 0 whether or not anything is printed. Pinned by tests in the `test_milestones_*` family covering overlap in both directions, disjoint packages, a defined-only milestone, and both refusals.

---

## Finish by Removing the Milestone Directory

Rename `core/skills/finish-current-milestone/` to `finish-milestone`, keeping its two checks and its `tasks` read, and make it commit through the commit tool's one command with the milestone directory as the removal and the context file as an ordinary path when edited, under `Milestone-finish: <path>` with the summary as body: the title read from the `requirements.md` heading with any legacy `Milestone <N>: ` prefix stripped, a blank line, then the 3–8 bullets, a trailing trailer block allowed. It writes nothing to `milestones/README.md` and touches no pointer; its six fixed-lines rows, its `docs/skill-reference.md` entry, and every reference to the old name follow, verified by the suite and a finish in a scratch repository whose `summary` then prints the body back.

---

## Retire Activation and Reduce the Bootstrap

Delete `core/skills/goto-next-milestone/` with its four fixed lines and its reference entry, and reduce `init-milestone-base-workflow` to the context file alone: it creates the file with a `## Milestone Workflow` section carrying the path-addressed guidance when the file is missing, appends the section when the file lacks it, leaves any present section exactly as it is, probes nothing, creates no `milestones/` scaffold, and commits only the context file subject-only under `Workflow-bootstrap: milestones`, its no-op lines reworded from the scaffold to the guidance. The git work-tree probe and the `python3 --version` check against 3.9 become the opening step of `define-milestone-goal`, run on every invocation before the definition tool and each stopping before any write on a fixed line moved from the bootstrap, with `README.md`'s prerequisite sentence naming `/define-milestone-goal` as the skill that checks them; verified by the suite, the fixed-lines test, and a bootstrap run on an empty project.

---

## Capture Takes a Milestone Path

Make `capture-milestone-principle-updates` take the milestone's repo-relative path, as the definition tool printed it, as its required positional argument, used verbatim in the repeat-capture grep, the path-scoped answer walk, and the `Principle-capture:` subject, and accepted when `<path>/requirements.md` is in the tree or a path-scoped `git log -1 --format=%h -- <path>/requirements.md` prints a hash, so a finished and removed milestone is harvestable; it parses no `--milestone`, and its two stop lines are reworded from id to path. Verified by the fixed-lines test and a capture run against a removed milestone in a scratch repository.

---

## Conversational Skills Read the Record

`discuss-milestone-goal` step 1 runs one fixed, unconditional `record .` call in place of its README history read, and `ask-in-milestone-context` loses its pointer-`none` fallback and its project-wide mode outright, resolving only through the shared procedure, and runs `record <PATH>` at its own discretion when a question concerns past work, scoped to the path the question concerns, the milestone's scope, or `.`, a finished milestone being answered from that project-wide read. Verified by the rebuilt trees and one run of each skill against this repository's record.

---

## Retire Current From Runtime Wording

Reword every frontmatter description reading "the current milestone" and every runtime prose mention of the current milestone under `core/` (about eighty, `alternatives-procedure.md` and `recommend-procedure.md` among them) to name the milestone the run was pointed at, each description staying one clause of 25 words or fewer, with the three `settings.toml` hands-on comments, `.github/ISSUE_TEMPLATE/proposal.yml`, `/release-plugin`, and the per-skill entries of `docs/skill-reference.md` following. Verified by the rebuilt trees, the suite, and a grep of the rendered trees finding no "current milestone".

---

## Migrate Milestones Into Finish Commits

Add `core/skills/migrate-milestones/`, a person-run skill in no chain that walks the README's `## Milestone History` entries oldest first and, for each whose directory still stands, makes through the commit tool the finish commit the new finish would make: the directory removed with `--remove`, the subject `Milestone-finish: <path>`, the body the title from that directory's `requirements.md` heading, a blank line, and the entry's bullets, and `--date` carrying the original finish commit's `%aI` author date, or the newest commit that changed the directory when no finish commit exists, while an entry whose directory is gone with a path-form finish subject in the log is skipped as migrated. Before its first commit it stops on a shallow repository or on any entry with no directory, listing them, then prints its whole plan and asks once, a rejection ending on one fixed no-op line with nothing changed; its closing commit removes `milestones/README.md` and a live milestone's `TASKS_DONE.md` if present and rewrites the context file's `## Milestone Workflow` section to the bootstrap's new guidance, and a project without the README is told so on one fixed line. Verified by the fixed-lines test and a run against a pointer-era scratch repository whose `milestones .` then lists every entry with its original date.

---

## Release Notes From the Milestones Tool

Rewrite steps 5a–5e of `.claude/skills/release-plugin/SKILL.md` to read the record through the milestones tool rather than a `git log` of its own: `milestones .` supplies the finished milestones with their finish dates, the skill keeps those finished after the last tag's date, and `summary` on each supplies the title line and bullets of its `###` section, with the README cross-check dropped and steps 3c and 7 unchanged. Verified by reading both queries against a scratch repository holding finish-shaped commits on either side of a tag.

---

## Docs and Invariants Follow the Path Form

Rewrite the documentation to the path-addressed shape: every chain in `docs/ways-of-using-cairn.md` carries `--milestone <path>` from the definition line's printed path, with the activation line gone, the definition line taking `--at`, and finish described as removal; `docs/workflow.md`'s stages, diagram labels, and committing paragraph; `docs/design-claims.md` claims 9 and 10; `README.md`'s how-it-works and self-dogfooding paragraphs; `CONTRIBUTING.md`'s contributor flow, where the maintainer reserves with `/define-milestone-goal --at <scope>` on `main`, the contributor branches from that commit and runs the pipeline with `--milestone <path>`, and the goto step and the pointer conditions on reserving and merging go, the pull request template's milestone field naming the reserved path; `ideas/benchmark_for_cairn.md`'s bootstrap and activation lines; and `CLAUDE.md`'s layout, skill list, file-structure, and invariant sections, retiring the pointer, goto, and finish-precedes-goto invariants, rewriting the pre-split and pre-flip notes for what the migration leaves in history, and describing resolution, definition, finish, the commit tool's two new inputs, the tool's queries, and the migration as landed, while leaving its `## Milestone Workflow` tail for the migration's closing commit. Verified by the fixed-lines test, `--check`, and a read-through finding no pointer, activation, or README-history reference outside recorded history.

---

## Gate the Four Task Writers

Add one shared procedure under `core/shared/` stating the `gate` call, what a held scope means, and its one fixed stop line with the holder paths beneath it, and reference it as a separate step before the fixed write call in `derive-tasks` and `submit-task`, before each dispatch in `complete-all-tasks`, and after the procedure's step 1 in the `complete-task` skill, each runner stopping when the captured print is non-empty, with the write calls, `complete-procedure.md`, and the agent unchanged and design claim 9, the fixed-lines table, and `CLAUDE.md` gaining the gate in place of the pointer. This task stands last among the implementation tasks; it is verified by the fixed-lines test, the rebuilt trees, and a refused task entry in a scratch repository holding two started milestones in one container.

---

## Revise the Draft After Migration

Revise "Carrying it out" in `ideas/milestones_addressed_by_path.md` so its step 3 records what landed as the sections for steps 1 and 2 do, marking it done and noting what it found for step 4 (the `live` filter, the record's missing bars, what the migration and the gate met on this repository), its date line extended. Its precondition is that this repository's own `/migrate-milestones` run has landed, so `milestones/README.md` is gone: it is completed alone, in a fresh session after that run, by the inline `/complete-task --milestone <path>`, and `/finish-milestone --milestone <path>` follows it; verified by a read of the revised section against the milestone's commits.

---
