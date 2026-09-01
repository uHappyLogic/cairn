# TASKS DONE

## Slim Submit Procedure Into Shared Task Format

Replace `shared/submit-procedure.md` with `shared/task-format.md`, holding only the brief-level task template and its authoring guidelines. The milestone-resolution, context-loading, and POSITION-insertion steps drop out (the two authoring runners now handle those themselves), and the name describes the task format rather than a submit procedure. This is the shared source of truth both `derive-tasks` and the leaned-down `submit-task` skill will reference via `${CLAUDE_PLUGIN_ROOT}`, and that `shared/complete-procedure.md` parses.

**Provides:**
- `shared/task-format.md` — the shared brief-level task-format file, referenced via `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md`.
- The brief-level task template it defines: a `##` task-title heading, a 1–3 sentence description with the "how it would be verified" clause folded in as prose, and a trailing `---` separator — no `Provides`, `Notes`, or `Success` sections.
- The four carried-over authoring guidelines: atomic scope, no open decisions, quote numeric values from `requirements.md`, unique 4–8 word titles.

**Notes:**
- `shared/submit-procedure.md` is still referenced by `skills/submit-task/SKILL.md` and `agents/submit-task.md`; rewriting/retiring those referrers belongs to sibling tasks, so this task leaves them dangling.
- Keep the file execution-neutral in the established shared-file style — no commit steps, no `DONE`/`FAILED` return protocol, no ordering or positioning decisions.
- `scripts/migrate_skills_to_agy.py` copies only `agents/` and `skills/` into `.agents/plugins/cairn/`; `shared/` has no generated twin, so this rename needs no transpile re-run.

**Success:**
- `shared/task-format.md` exists and contains exactly two content areas: the brief-level task template and the four authoring guidelines.
- `shared/submit-procedure.md` no longer exists.
- The template in `shared/task-format.md` contains no `Provides`, `Notes`, or `Success` section and no other structured done-ness heading.
- The template specifies the `##` heading, the 1–3 sentence description, and the mandatory trailing `---` separator.
- `shared/task-format.md` contains no milestone-resolution, context-loading, or POSITION/insertion instructions.

---

## Rewrite Derive-Tasks To Write Briefs Directly

Rewrite `skills/derive-tasks/SKILL.md` so it writes its ordered briefs into `<MILESTONE_DIR>/TASKS_TODO.md` itself in the brief-level format defined by `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md`, retiring the per-brief `submit-task` agent dispatch loop and every reference to that agent and to `POSITION: append`. The skill keeps everything else it owns — decomposition, the requirement→task coverage matrix, dependency ordering, plan presentation, the coverage advisory, the terse success line, and its once-at-end-of-run commit. This is what makes `derive-tasks` the single writer on the derivation path, at one consistent altitude with the leaned-down `submit-task` skill.

**Provides:**
- `skills/derive-tasks/SKILL.md` as the sole author of `TASKS_TODO.md` on the derivation path, writing brief-level sections per `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md` with no delegation step.
- Its precondition step keyed on `<open-question>` XML blocks, with `status="open"` blocks blocking derivation.
- `agents/submit-task.md` left with no remaining caller, so a sibling task can retire it.

**Notes:**
- The stale `> **Open question` scan in step 2 predates the milestone-9 XML format; the current form is an `<open-question id="..." status="open|deferred">` block, and only `status="open"` blocks block derivation — `status="deferred"` blocks may carry forward.
- The agent is named in the YAML frontmatter `description` as well as in the body prose (the delegation rationale, the `complete-all-tasks` mirror analogy, step 7, and two Rules bullets); the frontmatter must keep both `name` and `description` keys, since `scripts/migrate_skills_to_agy.py` hard-errors without them.
- Step 6's initialize-to-a-bare-`# TASKS TODO`-header move is still worth keeping — it is what makes the once-at-end path-scoped commit and its dirty-own-path no-op guard behave — but its "so the agent has an empty file to append into" rationale goes.
- Re-running the transpilation script to regenerate `.agents/plugins/cairn/` is a milestone-wide sweep, not part of this task.

**Success:**
- `skills/derive-tasks/SKILL.md` contains no occurrence of `submit-task`, `POSITION`, or `subagent_type`, and no agent-dispatch step.
- It references `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md` as the format for the task sections it writes.
- Its precondition step scans for `<open-question` blocks rather than `> **Open question`.
- It still contains the decomposition step, the requirement→task traceability matrix, the dependency-ordering step, the plan-presentation step, the untraceable-requirement coverage advisory, the terse `Tasks derived.` success line, its no-op message, and the commit step supplying `<MILESTONE_DIR>/TASKS_TODO.md` and `Task-derivation: <milestone_id>` to `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`.
- Its YAML frontmatter still carries `name` and `description`, and the `description` no longer mentions delegating authoring to the agent.

---

## Retire The Submit-Task Agent

Delete `agents/submit-task.md`, the bulk per-brief authoring subagent. Its sole caller was the `derive-tasks` dispatch loop, which "Rewrite Derive-Tasks To Write Briefs Directly" removes, so no consumer remains once that task lands. Only the root source file goes here; the generated twin and the `CLAUDE.md`/`README.md` prose are reconciled by later sibling tasks.

**Provides:**
- The absence of `agents/submit-task.md` — later tasks (the Antigravity transpile re-run and the documentation reconciliation) assume the root source file is already gone.
- `agents/complete-task.md` as the only remaining skill+agent pair in the plugin, which the documentation tasks describe.

**Notes:**
- The checked-in generated twin `.agents/plugins/cairn/agents/submit-task.md` is regenerated (rmtree-and-copy of `agents/`) by `scripts/migrate_skills_to_agy.py`; do **not** hand-edit or delete the generated tree here — a later task re-runs the script for the whole milestone.
- `CLAUDE.md` and `README.md` still describe the agent (layout entry, the "submit-task exists as both skill and agent" invariant, the `derive-tasks` skill-reference line). Leave them — later sibling tasks own that reconciliation.
- Two residual agent references live under `skills/` and are dangling pointers to the deleted file once this task lands; remove exactly those passages and nothing else, leaving the rest of each file to its own sibling task: `skills/submit-task/SKILL.md` (the "for bulk authoring, `derive-tasks` instead spawns the `submit-task` **agent**" paragraph and the two "never spawn / never delegate to the `submit-task` agent" prohibitions), and `skills/answer-open-question-with-recommendation/SKILL.md` (the "like `complete-task`/`submit-task`" SKILL+AGENT-pair analogy, which must drop `submit-task` since only `complete-task` remains such a pair).
- `shared/submit-procedure.md` — whose header names the agent as one of its two runners — is already gone by this point, replaced by `shared/task-format.md` in an earlier task.
- Legitimate references to the user-facing `/submit-task` **skill** (in `discuss-new-task`, `ask-in-milestone-context`, and the skill's own body) stay; only agent references are being retired.

**Success:**
- `agents/submit-task.md` does not exist.
- No file under `skills/` or `shared/` contains the string `subagent_type` paired with `submit-task`.
- No file under `skills/` or `shared/` refers to a `submit-task` agent — no "`submit-task` agent" phrase, no spawn/delegate-to-the-agent prohibition, and no listing of `submit-task` as a skill+agent pair.
- `agents/` contains only `complete-task.md`, `recommend-open-question.md`, and `answer-open-question-with-recommendation.md`.

---
