# TASKS TODO

## Update README Recommend Sweep Entries

Revise the `README.md` skill-reference entries for `recommend-all-open-questions` and `recommend-open-question (subagent)` so they describe the extraction of the sub-element region, the single repair attempt (same-session re-emit or fresh re-dispatch) and the skip-with-advisory that follows only a second failure, and the agent's draft → self-check → emit return. Verify by reading the two entries against the finished skill and agent files for consistency.

---

## Regenerate Antigravity Plugin Tree

Run `uv run scripts/migrate_skills_to_agy.py` so `.agents/plugins/cairn/` picks up the rewritten agent and sweep skill, confirming the transpiled skill reads the same two-branch repair prose and therefore takes the fresh re-dispatch branch where session continuation is unavailable. Verify with `diff -r` between the source and generated trees showing only the expected `${CLAUDE_PLUGIN_ROOT}` reference rewrites and dropped resolve hints.

---
