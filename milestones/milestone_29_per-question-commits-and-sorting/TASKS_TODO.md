# TASKS TODO

## Sync Docs Pages To New Granularity

Update `docs/skill-reference.md`'s `recommend-all-open-questions` entry (one `Recommendation-annotation: <Short Title>` commit per embedded question with the lifted line as its body, the end-of-run `sort` and `Question-ordering: <milestone_id>` commit on every run, the two success lines `Recommendations embedded.` / `Questions reordered.` and their selection rule) and `docs/workflow.md`'s `## How skills commit` granularity sentence so neither states that the sweep commits once at the end of the run, keeping every string in sync with `CLAUDE.md` and both host trees. Needed so the user-facing docs match the shipped behavior. Verified by a grep for `once at the end of the run` under `docs/` naming only `/derive-tasks`, by the new strings matching the rendered `hosts/*/skills/recommend-all-open-questions/SKILL.md` verbatim, and by `uv run scripts/build_hosts.py --check` passing.

---
