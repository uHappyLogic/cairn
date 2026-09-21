# TASKS TODO

## Tool Sort Subcommand With Tests

Add a `sort MILESTONE_DIR` subcommand to `core/tools/open_questions.py` — registered through `add_subcommand` and listed in the module docstring's `Subcommands:` — that rewrites the document with the `<recommendation>`-bearing blocks first in exactly `walk_order`'s order (origins, then dependents by depth, same-depth ties in prior document order) and every `<recommendation>`-less block last in stable prior document order, reusing `walk_order` rather than reimplementing it, printing nothing on success and one `Error:` line with the document unchanged on failure; `render_document` and every other subcommand keep writing blocks in their existing order. Needed so `walk` is by construction the annotated prefix of `list` on a sorted document. Verified by a new `tests/test_sort.py` (annotated prefix equals `walk`'s print, un-annotated blocks last in prior order, `sort` idempotent and the identity on an already-sorted document such as the `annotated` fixture, silent success, `Error:` on a missing document) passing under both `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest`, and by a rebuild with `uv run scripts/build_hosts.py --check` passing with the tool rendered byte-identical.

---

## Recommend Sweep Per-Question Commits

Change `core/skills/recommend-all-open-questions/SKILL.md` so that after each silent `embed` in step 3 the orchestrator runs the tool's `lift <MILESTONE_DIR> "<Short Title>"` and commits through `{{PLUGIN_ROOT}}/shared/commit-procedure.md` with PATHS `<MILESTONE_DIR>/open_questions.xml`, SUBJECT `Recommendation-annotation: <Short Title>`, and BODY the lifted "`<option>` — `<rationale>`" line, before the next dispatch, while a skipped question commits nothing and the once-per-run `Recommendation-annotation: <milestone_id>` commit of step 4 and its "never inside the dispatch loop" wording are removed. Needed so the sweep's granularity mirrors the answer sweep's one commit per question. Verified by reading the skill against `answer-all-open-questions-with-recommendation`'s step 2 for the same lift-then-commit shape, and by a rebuild with `uv run scripts/build_hosts.py --check` passing.

---

## Recommend Sweep Sort Step And Report Lines

Give `core/skills/recommend-all-open-questions/SKILL.md` a fixed end-of-run step, reached on every run that found questions (an empty `list --unannotated` print and an all-skipped dispatch loop both fall through to it instead of exiting to the no-op line), that runs the tool's `sort <MILESTONE_DIR>` once after the last dispatch and commits the reorder through the shared procedure with PATHS `<MILESTONE_DIR>/open_questions.xml`, SUBJECT `Question-ordering: <milestone_id>`, and no BODY, the dirty-own-path guard being the sort's only no-op test; then rewrite the report step to pick its line by what the run committed in strict order — an embed wrote: `Recommendations embedded.`; else the sort committed: `Questions reordered.`; else the distinct no-op line with its reason — with the still-skipped advisory printed alongside whichever line is chosen. Needed so a reader of the document meets the questions whose answers no dependency can nullify first, and so every terse line stays true to the git log. Verified by reading the skill for the three-way selection rule and the fall-through, and by a rebuild with `uv run scripts/build_hosts.py --check` passing.

---

## Sync CLAUDE.md To New Granularity

Update `CLAUDE.md` so every surface that states the old rule matches the rendered skill and tool: the layout entries for `core/tools/open_questions.py` (add `sort`), `core/shared/commit-procedure.md` (the optional BODY input), and `tests/` (add `test_sort.py`); the pipeline line and the `recommend-all-open-questions` invariant (per-question `Recommendation-annotation: <Short Title>` commits with the lifted body, the end-of-run `sort` and its `Question-ordering: <milestone_id>` commit on every run, the narrowed "annotated nothing and moved nothing commits nothing" invariant); the commit-convention invariant (the per-skill subject list, the orchestrator-granularity sentence, the new `Question-ordering:` marker); and the terse-reporting invariant's stated carve-out for this one skill's two success lines and their selection rule. Needed because CLAUDE.md is the editor-facing home of these rules and currently states once-per-run. Verified by greps for `Recommendation-annotation: <milestone_id>`, `once at the end of the run`, `Questions reordered.`, and `sort` returning only the intended lines and by the file reading consistently against the rendered host trees.

---

## Sync Docs Pages To New Granularity

Update `docs/skill-reference.md`'s `recommend-all-open-questions` entry (one `Recommendation-annotation: <Short Title>` commit per embedded question with the lifted line as its body, the end-of-run `sort` and `Question-ordering: <milestone_id>` commit on every run, the two success lines `Recommendations embedded.` / `Questions reordered.` and their selection rule) and `docs/workflow.md`'s `## How skills commit` granularity sentence so neither states that the sweep commits once at the end of the run, keeping every string in sync with `CLAUDE.md` and both host trees. Needed so the user-facing docs match the shipped behavior. Verified by a grep for `once at the end of the run` under `docs/` naming only `/derive-tasks`, by the new strings matching the rendered `hosts/*/skills/recommend-all-open-questions/SKILL.md` verbatim, and by `uv run scripts/build_hosts.py --check` passing.

---
