# TASKS TODO

## Recommend Sweep Sort Step And Report Lines

Give `core/skills/recommend-all-open-questions/SKILL.md` a fixed end-of-run step, reached on every run that found questions (an empty `list --unannotated` print and an all-skipped dispatch loop both fall through to it instead of exiting to the no-op line), that runs the tool's `sort <MILESTONE_DIR>` once after the last dispatch and commits the reorder through the shared procedure with PATHS `<MILESTONE_DIR>/open_questions.xml`, SUBJECT `Question-ordering: <milestone_id>`, and no BODY, the dirty-own-path guard being the sort's only no-op test; then rewrite the report step to pick its line by what the run committed in strict order — an embed wrote: `Recommendations embedded.`; else the sort committed: `Questions reordered.`; else the distinct no-op line with its reason — with the still-skipped advisory printed alongside whichever line is chosen. Needed so a reader of the document meets the questions whose answers no dependency can nullify first, and so every terse line stays true to the git log. Verified by reading the skill for the three-way selection rule and the fall-through, and by a rebuild with `uv run scripts/build_hosts.py --check` passing.

---

## Sync CLAUDE.md To New Granularity

Update `CLAUDE.md` so every surface that states the old rule matches the rendered skill and tool: the layout entries for `core/tools/open_questions.py` (add `sort`), `core/shared/commit-procedure.md` (the optional BODY input), and `tests/` (add `test_sort.py`); the pipeline line and the `recommend-all-open-questions` invariant (per-question `Recommendation-annotation: <Short Title>` commits with the lifted body, the end-of-run `sort` and its `Question-ordering: <milestone_id>` commit on every run, the narrowed "annotated nothing and moved nothing commits nothing" invariant); the commit-convention invariant (the per-skill subject list, the orchestrator-granularity sentence, the new `Question-ordering:` marker); and the terse-reporting invariant's stated carve-out for this one skill's two success lines and their selection rule. Needed because CLAUDE.md is the editor-facing home of these rules and currently states once-per-run. Verified by greps for `Recommendation-annotation: <milestone_id>`, `once at the end of the run`, `Questions reordered.`, and `sort` returning only the intended lines and by the file reading consistently against the rendered host trees.

---

## Sync Docs Pages To New Granularity

Update `docs/skill-reference.md`'s `recommend-all-open-questions` entry (one `Recommendation-annotation: <Short Title>` commit per embedded question with the lifted line as its body, the end-of-run `sort` and `Question-ordering: <milestone_id>` commit on every run, the two success lines `Recommendations embedded.` / `Questions reordered.` and their selection rule) and `docs/workflow.md`'s `## How skills commit` granularity sentence so neither states that the sweep commits once at the end of the run, keeping every string in sync with `CLAUDE.md` and both host trees. Needed so the user-facing docs match the shipped behavior. Verified by a grep for `once at the end of the run` under `docs/` naming only `/derive-tasks`, by the new strings matching the rendered `hosts/*/skills/recommend-all-open-questions/SKILL.md` verbatim, and by `uv run scripts/build_hosts.py --check` passing.

---
