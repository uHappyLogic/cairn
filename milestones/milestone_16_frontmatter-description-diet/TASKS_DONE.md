# TASKS DONE

## Restructure Six Heaviest Skill Descriptions

Rewrite the frontmatter `description` of the six heaviest skills — `review-milestone-requirements`, `discuss-new-task`, `capture-milestone-principle-updates`, `recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, `modify-milestone-goal` — from scratch into a single independent clause of 25 words or fewer naming only what the skill does, deleting their trigger-phrase lists, mechanics, sequencing, design provenance, cross-skill references, and "Use when…" framing without preserving that content anywhere. These six carry the majority of the always-on description words and must be restructured rather than trimmed, and the `review-milestone-requirements` rewrite must also stop tripping the transpiler's re-quoting fallback. Verified when each of the six descriptions is 25 words or fewer, contains no semicolon or colon, keeps the `name` key and any `model` key untouched, and its raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted.

**Verified:**

- Each of the six rewritten descriptions (`review-milestone-requirements`, `discuss-new-task`, `capture-milestone-principle-updates`, `recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, `modify-milestone-goal`) is 25 words or fewer — 22, 22, 15, 18, 21, 21 respectively.
- Each of the six descriptions contains no semicolon and no colon.
- Each of the six is a single independent clause naming only what the skill does, with its trigger-phrase list, mechanics, sequencing, design provenance, cross-skill references, and "Use when…" framing deleted and preserved nowhere.
- Each file's `name` key is unchanged and none of the six carries a `model` key, so no `model` key was added or altered — the diff touches exactly one `description:` line per file.
- Each of the six files' raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted (plain scalar, no leading quote).
- `skills/review-milestone-requirements/SKILL.md` no longer trips the transpiler's re-quoting fallback — its raw frontmatter now parses under `yaml.safe_load` without the colon-space that previously raised.

---
