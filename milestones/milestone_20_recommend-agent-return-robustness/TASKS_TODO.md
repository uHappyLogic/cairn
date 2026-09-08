# TASKS TODO

## Regenerate Antigravity Plugin Tree

Run `uv run scripts/migrate_skills_to_agy.py` so `.agents/plugins/cairn/` picks up the rewritten agent and sweep skill, confirming the transpiled skill reads the same two-branch repair prose and therefore takes the fresh re-dispatch branch where session continuation is unavailable. Verify with `diff -r` between the source and generated trees showing only the expected `${CLAUDE_PLUGIN_ROOT}` reference rewrites and dropped resolve hints.

---
