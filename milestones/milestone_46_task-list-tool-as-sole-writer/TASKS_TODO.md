# TASKS TODO

## Describe Task-List Tool In Docs

Update the documentation surfaces for the tool: `docs/skill-reference.md`'s `derive-tasks`, `submit-task`, `complete-task`, and `complete-all-tasks` entries and the `define-milestone-goal` entry's note that the task files are the task-list tool's from creation on, `docs/workflow.md`'s derive and completion narrative and its committing paragraph (the chained calls), `docs/design-claims.md` claim 7 (the Verified bar rendered by the tool) and claim 11 (the task files tool-written beside `open_questions.xml`, with the `tests/` metric covering the new tool), `README.md`'s task-file bullets, `milestones/README.md`'s file list and the matching template in `core/skills/init-milestone-base-workflow/SKILL.md`, and `CONTRIBUTING.md` and the host README templates under `scripts/hosts/` confirmed to need no edit under their count-free tool wording, naming no host in any rendered file. Verified by `grep` showing no doc still describing the move as `Read`/`Edit` or the submit fallback as an append, by each touched claim's design and metric matching the landed tool and tests, and by the rebuild so `uv run scripts/build_hosts.py --check` passes.

---
