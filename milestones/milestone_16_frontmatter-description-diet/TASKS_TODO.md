# TASKS TODO

## Falsification Pass Over Parallel Doc Surfaces

Run one bounded pass over `README.md`'s `## Skill reference` entries and `CLAUDE.md`'s per-skill workflow map, editing an entry only where a shortened description has made an existing claim demonstrably false, adding no new prose and doing no general tidying, since both surfaces are the intended homes for the mechanics and provenance deleted from descriptions. Verified by a recorded per-entry check of both surfaces against the rewritten descriptions that either lists each falsified claim and its correction or reports a no-op with nothing edited.

---

## Regenerate Antigravity Tree After Rewrites

Run `uv run scripts/migrate_skills_to_agy.py` exactly once, after every description rewrite has landed, to regenerate the checked-in Antigravity tree at `.agents/plugins/cairn/` so the description savings reach that surface, touching no transpiler source. Verified when the transpiler exits cleanly without exercising its re-quoting fallback, a whole-set check confirms all 24 descriptions are 25 words or fewer with no semicolon or colon and every raw frontmatter loads under `yaml.safe_load` unquoted, and the regenerated tree's descriptions match the source files.

---
