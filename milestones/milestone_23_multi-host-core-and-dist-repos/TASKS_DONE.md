# TASKS DONE


## Create Host-Neutral Core Tree

Copy the root `skills/`, `agents/`, and `shared/` trees into a new `core/` directory (leaving the root trees in place until the final cutover task, because the running plugin still resolves its shared procedures from them), replacing every `${CLAUDE_PLUGIN_ROOT}` with the neutral placeholder `{{PLUGIN_ROOT}}` and deleting all 24 occurrences of the ``(run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path)`` resolve hint across the 18 files that carry it. This is the host-neutral source every host build renders from. Verified when `core/` holds the same file set as the three root trees, a grep finds no `CLAUDE_PLUGIN_ROOT` and no `echo` hint under `core/`, and every `{{PLUGIN_ROOT}}/shared/<name>.md` reference names a file present in `core/shared/`.

**Verified:**

- `core/` holds exactly the same file set as the three root trees: `diff` of the sorted relative paths under root `skills/`, `agents/`, `shared/` against those under `core/` is empty — 31 files (21 `skills/<name>/SKILL.md`, 3 `agents/*.md`, 7 `shared/*.md`), with `core/` containing only `agents`, `shared`, and `skills` at its top level.
- The root `skills/`, `agents/`, and `shared/` trees are left in place and unmodified: `git status --porcelain -- skills agents shared` is empty; the only working-tree change is the new untracked `core/`.
- `grep -rn 'CLAUDE_PLUGIN_ROOT' core` returns nothing.
- `grep -rn 'echo' core` returns nothing — the resolve hint was the only `echo` in the root trees, so this confirms all 24 hint occurrences across the 18 carrying files are deleted, the line-wrapped ones included (deleted with the transpiler's whitespace-tolerant `RESOLVE_HINT_RE`, which joins the surrounding sentence cleanly).
- `{{PLUGIN_ROOT}}` appears exactly 45 times under `core/`, one per root `${CLAUDE_PLUGIN_ROOT}` occurrence, and no other `{{` token exists anywhere under `core/`.
- Every distinct `{{PLUGIN_ROOT}}/shared/<name>.md` reference under `core/` (answer-procedure, answer-with-recommendation-procedure, commit-procedure, complete-procedure, get-current-milestone, recommend-procedure, task-format) names a file present in `core/shared/`.
- Each `core/` file differs from its root counterpart only by those two rewrites: re-applying `scripts/migrate_skills_to_agy.py`'s `RESOLVE_HINT_RE` deletion and the literal `${CLAUDE_PLUGIN_ROOT}` → `{{PLUGIN_ROOT}}` substitution to every root file reproduces the corresponding `core/` file byte-for-byte (31 checked, 0 mismatches), and every `core/` skill and agent frontmatter still `yaml.safe_load`s with `name` and `description` present (24/24).

---
