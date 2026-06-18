# TASKS DONE

## Rename Answer-Sweep Orchestrator To Fan-Out Form

Rename the answer-sweep orchestrator skill `try-answer-questions-by-principle` → `try-answer-all-questions-by-principle` (the fan-out grammar `<verb>-all-<plural-object>` form, applied because this orchestrator shares the verb "answer" with its per-item worker) and update every cross-reference to the orchestrator's handle across the plugin. This is one of the milestone's order-free renames; the read-only candidate-elimination subagent `try-answer-question-by-principle` is deliberately NOT renamed.

**Provides:**
- The renamed orchestrator handle and skill directory `try-answer-all-questions-by-principle` (directory name IS the slash-command name), referenced by sibling rename tasks and the docs.

**Notes:**
- The orchestrator handle is the *plural* string `try-answer-questions-by-principle`; the subagent handle is the *singular* `try-answer-question-by-principle`. They are distinct strings — grep the plural form so the singular subagent is left untouched, including its dispatch string inside the orchestrator, which must stay exactly `try-answer-question-by-principle`.
- The live orchestrator-handle references are in: `skills/try-answer-questions-by-principle/SKILL.md` (its own self-references + the directory rename), `skills/reject-auto-answer/SKILL.md`, `skills/try-capture-answer-principle/SKILL.md`, `shared/answer-procedure.md`, `agents/try-answer-question-by-principle.md` (the subagent file names its parent orchestrator), `README.md` (Mermaid workflow node + per-skill reference-table row), `CLAUDE.md` (repository-layout + skills-overview + invariants mentions), and the single live header cross-reference line in `milestones/answer_decision_principles.md`.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` do NOT reference this handle, so no manifest edit is needed.
- Per the milestone's *Rename ordering* decision, this task syncs its own `README.md` and `CLAUDE.md` references rather than deferring to a trailing doc-sync pass.
- Do not edit frozen surfaces: historical milestone dirs (`milestone_01_*`, `milestone_02_*`), milestone_03's own `requirements.md`/`TASKS_*`, the history/completed sections of `milestones/README.md`, the `Origin:` provenance lines in `answer_decision_principles.md`, and `.claude/settings.local.json`.

**Success:**
- `git grep try-answer-questions-by-principle` over live plugin surfaces (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, `.claude-plugin/`, the live lines of `milestones/answer_decision_principles.md`) returns zero hits.
- Directory `skills/try-answer-all-questions-by-principle/` exists with its `SKILL.md`; the old `skills/try-answer-questions-by-principle/` directory no longer exists.
- The subagent handle `try-answer-question-by-principle` is unchanged everywhere it appeared (orchestrator dispatch string, `agents/try-answer-question-by-principle.md`, README, CLAUDE.md).
- The README Mermaid node + skill-table row and the CLAUDE.md invariants read coherently with the new `try-answer-all-questions-by-principle` handle.

---

## Rename Submit-Backlog-Task To Submit-Task

Drop the redundant `-backlog` segment from the single-task authoring machinery — which exists as BOTH a user-facing skill and an isolated bulk-authoring agent sharing one name — renaming `submit-backlog-task` → `submit-task` for the skill (`skills/submit-backlog-task/` directory, whose name IS the slash-command name) and the agent (`agents/submit-backlog-task.md`). Update the agent's dispatch type-string in the task-deriver orchestrator and every cross-reference across the plugin, and reword surrounding "backlog" prose around this handle to "task"/"the task list". This is one of the milestone's order-free renames (per *Task-collection noun*).

**Provides:**
- The renamed skill directory `skills/submit-task/` and agent file `agents/submit-task.md` (each name IS its handle), plus the agent dispatch type-string `submit-task`, referenced by sibling rename tasks and the docs.

**Notes:**
- An agent's filename doubles as its `subagent_type` dispatch string, so the dispatch call must read `subagent_type: "submit-task"` and match `agents/submit-task.md` exactly. That dispatch string lives in the task-deriver skill (currently `skills/populate-backlog/SKILL.md`, line ~93: `spawn the \`submit-backlog-task\` agent ... (subagent_type: "submit-backlog-task")`). This rename is order-free w.r.t. the `populate-backlog` → `derive-tasks` rename — `git grep` the dispatch string and update it wherever the deriver dir currently lives, regardless of its current name.
- The handle's live references are in: `skills/submit-backlog-task/SKILL.md` (its own self-references + the directory rename), the discuss-new-task skill (currently `skills/discuss-new-backlog-task/SKILL.md` — it hands off to this skill; its own `-backlog` rename is equally order-free, so grep the handle wherever that skill currently lives), the deriver skill's dispatch (above), `shared/submit-procedure.md`, `agents/submit-backlog-task.md` (the agent file + rename), `README.md` (Mermaid workflow node + per-skill reference-table rows for both skill AND agent), and `CLAUDE.md` (repository-layout, skills-overview, and invariants mentions — note CLAUDE.md describes this handle as *both* a skill and an agent).
- The shared file NAME stays `submit-procedure.md` (its rename is out of scope here) — only update mentions of the skill/agent *handle* inside it, including its own title line "Submit-backlog-task procedure".
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` do NOT reference this handle (verified by grep), so no manifest edit is needed.
- Per the milestone's *Rename ordering* decision, this task syncs its own `README.md` and `CLAUDE.md` references rather than deferring to a trailing doc-sync pass.
- Do not edit frozen surfaces: historical milestone dirs (`milestone_01_*`, `milestone_02_*`), milestone_03's own `requirements.md`/`TASKS_*`, the history/completed sections of `milestones/README.md`, the `Origin:` provenance lines in `answer_decision_principles.md`, and `.claude/settings.local.json`.

**Success:**
- `git grep submit-backlog-task` over live plugin surfaces (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, `.claude-plugin/`) returns zero hits.
- Directory `skills/submit-task/` exists with its `SKILL.md`, and `agents/submit-task.md` exists; the old `skills/submit-backlog-task/` directory and `agents/submit-backlog-task.md` no longer exist.
- The task-deriver orchestrator's dispatch call reads `subagent_type: "submit-task"` and resolves to `agents/submit-task.md`.
- The `discuss-new-backlog-task` handoff target, the `shared/submit-procedure.md` handle mentions, and the README Mermaid node + per-skill reference-table rows (skill and agent) + the CLAUDE.md layout/skills-overview/invariants mentions all read coherently with the new `submit-task` handle.

---

## Rename Populate-Backlog To Derive-Tasks

Fully rename the task-deriver skill `populate-backlog` → `derive-tasks` (the skill that decomposes `requirements.md` into a covered, dependency-ordered task list) and update every cross-reference to its handle across the plugin. Per the *Task-collection noun* decision this is a distinctive-function rename, **not** a `-backlog`-segment drop: "derive" names that the tasks logically follow from `requirements.md` with a proven requirement→task coverage matrix, and the object "tasks" keeps consistency with the `complete-task` / `submit-task` / `discuss-new-task` family. This is one of the milestone's order-free renames.

**Provides:**
- The renamed skill directory `skills/derive-tasks/` (directory name IS the slash-command name), referenced by sibling rename tasks and the docs.

**Notes:**
- This deriver spawns the single-task authoring worker agent. Do **not** touch that dispatch string or the worker handle — the worker rename is owned by the *Rename Submit-Backlog-Task To Submit-Task* task. Rename only THIS deriver's own handle. The two renames are order-free; on shared doc/`CLAUDE.md` lines that name **both** handles, change only `populate-backlog` → `derive-tasks` and leave the worker handle (`submit-backlog-task`/`submit-task`) exactly as you find it for its own task to settle.
- The live deriver-handle references are in: `skills/populate-backlog/SKILL.md` (frontmatter `name:`, the H1, the `/populate-backlog` usage line, the "Cannot populate backlog" / "re-run /populate-backlog" error prose, plus all other self-references and the directory rename), `shared/submit-procedure.md` (names `populate-backlog` as the bulk caller), `agents/submit-backlog-task.md` (its file's prose names `populate-backlog` as its caller — update the handle only, not the agent's own filename), `skills/submit-backlog-task/SKILL.md` (names `populate-backlog` as the bulk caller), `README.md` (the intro-prose "populate an ordered backlog" line, the Mermaid workflow node `/populate-backlog`, the "before the backlog can be populated" phrasing in the highlight reference, and the per-skill reference-table row `### populate-backlog`), and `CLAUDE.md` (repository-layout line, skills-overview line, and the several invariants mentions — note several co-name `submit-backlog-task` on the same line).
- Beyond exact-handle hits, grep prose in other skills that names this as a next step (e.g. the openings/closings of the answer/highlight family, `finish-current-milestone`) and reword "populate the backlog" / "before the backlog can be populated"-style phrasing to the `derive-tasks` vocabulary.
- Manifest waypoint: `.claude-plugin/plugin.json`'s description currently reads "…populate backlogs, implement tasks…". Retire the "populate backlogs" phrase toward the new vocabulary, but do **not** finalize the one-liner's wording — its final coherent form is owned by the execution-family rename task (it still names "implement tasks"); here just retire the dead phrase. `.claude-plugin/marketplace.json` does **not** reference this handle or the phrase (its description is "Milestone-driven development for any stack."), so no marketplace edit is needed.
- Per the milestone's *Rename ordering* decision, this task syncs its own `README.md` and `CLAUDE.md` references rather than deferring to a trailing doc-sync pass.
- Do not edit frozen surfaces: historical milestone dirs (`milestone_01_*`, `milestone_02_*`), milestone_03's own `requirements.md`/`TASKS_*`, the history/completed sections of `milestones/README.md`, the `Origin:` provenance lines in `answer_decision_principles.md`, and `.claude/settings.local.json`.

**Success:**
- `git grep populate-backlog` over live plugin surfaces (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, `.claude-plugin/`) returns zero hits.
- Directory `skills/derive-tasks/` exists with its `SKILL.md`; the old `skills/populate-backlog/` directory no longer exists.
- The single-task authoring worker's dispatch string inside the deriver skill is left untouched by this task (still exactly the handle the submit-task rename task owns).
- `.claude-plugin/plugin.json` no longer contains the phrase "populate backlogs".
- The README Mermaid node + per-skill reference-table row, the CLAUDE.md layout/skills-overview/invariants mentions, and all next-step prose references read coherently with the new `derive-tasks` handle.

---

