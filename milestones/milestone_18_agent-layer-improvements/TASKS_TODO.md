# TASKS TODO

## Pass Milestone Directory To Recommend Agent

Change the dispatch prompt in `skills/recommend-all-open-questions/SKILL.md` step 3 to carry the resolved `<MILESTONE_DIR>` alongside the Short Title and the question's full `<open-question>` block, dropping the "plus relevant surrounding requirements" clause so the orchestrator never reads the whole `requirements.md` to build context, and rewrite the Inputs section of `agents/recommend-open-question.md` to name `<MILESTONE_DIR>` as a prompt input the agent uses to read that milestone's `requirements.md` read-only for grounding, replacing the current instruction that it does not resolve the directory. This closes the contradiction where the agent is told not to resolve the directory while the shared recommend core it runs requires reading that milestone's `requirements.md`. Verified by reading both files to confirm the prompt template and the agent's Inputs section agree, and by regenerating the Antigravity tree with `uv run scripts/migrate_skills_to_agy.py` so `.agents/plugins/cairn/` stays byte-identical to the source.

---
