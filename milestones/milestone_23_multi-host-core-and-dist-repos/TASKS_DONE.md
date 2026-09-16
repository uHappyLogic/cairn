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

## Neutralize Host-Named Prose In Core

Reword the three prose sites in `core/` that name a host so they name capabilities and the plugin's own namespace instead: the `recommend-all-open-questions` repair step keyed on whether the host can continue a finished agent session versus cannot (no `SendMessage`, Claude Code, or Antigravity mention), the dispatch sites of the three orchestrators naming the agent's registry name under this plugin's namespace, and the `init-milestone-base-workflow` CLAUDE.md template addressing the coding agent working in the repository. The agents' Claude-only `color` frontmatter key stays in `core/`, since the Antigravity host definition strips it by data. Verified when a case-insensitive grep for `Claude Code`, `Antigravity`, and `SendMessage` under `core/` returns nothing and each reworded passage still states the same rule it did before.

**Verified:**

- `grep -rni 'claude code' core` returns nothing.
- `grep -rni 'antigravity' core` returns nothing.
- `grep -rni 'sendmessage' core` returns nothing.
- The `recommend-all-open-questions` repair step still states the same two-branch rule in the same order — continue the same agent session where the host can continue a finished agent session and the dispatch's handle is still held (a follow-up message addressed to the agent id the `Agent` tool returned), else one fresh `cairn:recommend-open-question` re-dispatch with the same prompt plus the corrective message as the fallback — keyed only on whether the host can continue a finished agent session versus cannot, naming no host and no host tool.
- The three orchestrators' dispatch sites (`complete-all-tasks` step 2b, `answer-all-open-questions-with-recommendation` step b, `recommend-all-open-questions` step 3) still direct the `Agent` tool with `subagent_type` set to the namespaced registry name of the agent under this plugin's namespace, each naming its literal (`cairn:complete-task`, `cairn:answer-open-question-with-recommendation`, `cairn:recommend-open-question`) with no host attribution, and the per-dispatch prompts are unchanged.
- The `init-milestone-base-workflow` CLAUDE.md template now opens "This file provides guidance to the coding agent working in this repository." with the rest of the template (the `## Milestone Workflow` paragraph) byte-for-byte unchanged.
- All three `core/agents/*.md` files still carry their `color` frontmatter key (`yellow`, `red`, `blue`).
- The change set is exactly the four files `core/skills/recommend-all-open-questions/SKILL.md`, `core/skills/answer-all-open-questions-with-recommendation/SKILL.md`, `core/skills/complete-all-tasks/SKILL.md`, and `core/skills/init-milestone-base-workflow/SKILL.md` (14 lines changed); the root `skills/`, `agents/`, `shared/`, and `.agents/` trees are untouched.
- Each touched file's frontmatter still loads under `yaml.safe_load` with `name` and `description` present and every description at or under 25 words (15, 18, 15, 21).

---

## Add Root VERSION File And Version Script

Create a root `VERSION` file holding the bare `1.4.0` literal and nothing else as the single source of truth for the plugin version, and rewrite `scripts/set_version.py <MAJOR.MINOR.PATCH>` to write `VERSION`, `pyproject.toml`, `uv.lock`, and the root `.claude-plugin/marketplace.json` entry in lockstep (all-or-nothing, as today), never writing any manifest under `hosts/` and no longer treating the root `.claude-plugin/plugin.json` as a surface. Verified by running the script with a throwaway version, confirming exactly those four files change and carry the literal, then restoring `1.4.0`.

**Verified:**

- A root `VERSION` file exists holding exactly the bare `1.4.0` literal on one newline-terminated line and nothing else: `cat -e VERSION` prints `1.4.0$` only and the file is 6 bytes.
- `scripts/set_version.py`'s write set (its `RENDERERS` tuple) names exactly four paths — `VERSION`, `.claude-plugin/marketplace.json`, `pyproject.toml`, `uv.lock` — with no path under `hosts/` and no `.claude-plugin/plugin.json`; the only `hosts/` and `plugin.json` mentions in the script are the docstring's "deliberately not written" statement.
- `uv run scripts/set_version.py 9.9.9` from the repository root exits 0, and `git status --porcelain` afterwards lists exactly those four files (`VERSION` new, the other three modified); `.claude-plugin/plugin.json` is untouched and still reads `1.4.0`.
- After that run each of the four carries `9.9.9` in its version slot and nothing else in them changed: `VERSION` is `9.9.9\n`, `marketplace.json`'s single `plugins[0].version` is `"9.9.9"` with name, source `"."`, and description intact, `pyproject.toml` `[project]` `version = "9.9.9"`, and `uv.lock`'s `cairn-tooling` block reads `version = "9.9.9"` with the `pyyaml` `6.0.3` line untouched — each tracked diff is exactly one line.
- All-or-nothing holds: with the last-rendered surface `uv.lock` moved away, `.venv/bin/python scripts/set_version.py 8.8.8` exits 1 with `uv.lock not found (run this script from the repository root)` and `No files were changed.`, and `VERSION`, `marketplace.json`, and `pyproject.toml` still read the pre-run `9.9.9`.
- `uv run scripts/set_version.py 1.4.0` restores the literal: `git diff --stat` over the three tracked surfaces is empty, `VERSION` is again `1.4.0\n`, and the working tree holds only the task's own change set (`scripts/set_version.py` modified, `VERSION` new).
- The invocation contract is unchanged — `uv run scripts/set_version.py MAJOR.MINOR.PATCH`; no argument, two arguments, and `v1.2.3` each exit 1 with the existing usage/format message and change nothing — and the docstring names the four surfaces, `VERSION` as the single source of truth the mirrored surfaces follow, and the never-written `hosts/<host>/` manifests (rendered by the host build from `VERSION`) and root `plugin.json`.

---
