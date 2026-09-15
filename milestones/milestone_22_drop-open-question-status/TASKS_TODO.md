# TASKS TODO

## Regenerate Antigravity Tree Status Free

Run `uv run scripts/migrate_skills_to_agy.py` to regenerate `.agents/plugins/cairn/` from the swept `skills/`, `agents/`, and `shared/` so the generated tree carries no trace of the attribute, and use the same pass to confirm the whole sweep is grep-clean. Verified by grepping `skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, and `.agents/plugins/cairn/` for `status=`, `deferred`, and `Blocking` and finding only the capture skill's legacy blockquote note (and its generated copy), while "terse status line", `git status --porcelain`, "finish status", and the DONE/FAILED status wording survive untouched.

---
