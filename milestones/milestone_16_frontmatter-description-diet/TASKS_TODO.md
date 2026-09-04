# TASKS TODO

## Regenerate Antigravity Tree After Rewrites

Run `uv run scripts/migrate_skills_to_agy.py` exactly once, after every description rewrite has landed, to regenerate the checked-in Antigravity tree at `.agents/plugins/cairn/` so the description savings reach that surface, touching no transpiler source. Verified when the transpiler exits cleanly without exercising its re-quoting fallback, a whole-set check confirms all 24 descriptions are 25 words or fewer with no semicolon or colon and every raw frontmatter loads under `yaml.safe_load` unquoted, and the regenerated tree's descriptions match the source files.

---
