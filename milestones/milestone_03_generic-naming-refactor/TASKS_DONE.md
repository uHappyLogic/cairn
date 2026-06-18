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

## Rename Discuss-New-Backlog-Task To Discuss-New-Task

Drop the redundant `-backlog` segment from the issue-clarification skill — which breaks a vague or oversized issue into clear task-sized briefs and hands each off to the single-task submit skill — renaming `discuss-new-backlog-task` → `discuss-new-task` (`skills/discuss-new-backlog-task/` directory, whose name IS the slash-command name) and updating every cross-reference to its handle across the plugin. Reword surrounding "backlog" prose around this handle to "task"/"the task list" as fits. This is one of the milestone's order-free renames (per *Task-collection noun*).

**Provides:**
- The renamed skill directory `skills/discuss-new-task/` (directory name IS the slash-command name), referenced by the docs.

**Notes:**
- Update only THIS skill's own handle. This skill hands off to the single-task submit skill; that submit skill's handle is owned by its own *Rename Submit-Backlog-Task To Submit-Task* task and is equally order-free. Refer to the submit skill by whatever name it currently has on disk — `git grep` the submit handle wherever that skill currently lives and leave it exactly as you find it; on any line that names both handles, change only `discuss-new-backlog-task` → `discuss-new-task`.
- The handle's live references are in: `skills/discuss-new-backlog-task/SKILL.md` (frontmatter `name:`, the H1, the `/discuss-new-backlog-task` usage + example lines, plus all other self-references and the directory rename), the submit skill's `SKILL.md` (currently `skills/submit-backlog-task/SKILL.md` — it names `/discuss-new-backlog-task` as the route-here-first front-end; grep the handle wherever that skill currently lives), `README.md` (the Mermaid workflow node `/discuss-new-backlog-task` and the per-skill reference-table row `### discuss-new-backlog-task`, plus the prose naming it in the `submit-backlog-task` row), and `CLAUDE.md` (the skills-overview line).
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` do NOT reference this handle (verified by grep), so no manifest edit is needed.
- Per the milestone's *Rename ordering* decision, this task syncs its own `README.md` and `CLAUDE.md` references rather than deferring to a trailing doc-sync pass.
- Do not edit frozen surfaces: historical milestone dirs (`milestone_01_*`, `milestone_02_*`), milestone_03's own `requirements.md`/`TASKS_*`, the history/completed sections of `milestones/README.md`, the `Origin:` provenance lines in `answer_decision_principles.md`, and `.claude/settings.local.json`.

**Success:**
- `git grep discuss-new-backlog-task` over live plugin surfaces (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, `.claude-plugin/`) returns zero hits.
- Directory `skills/discuss-new-task/` exists with its `SKILL.md`; the old `skills/discuss-new-backlog-task/` directory no longer exists.
- The submit skill's handle is left exactly as found (this task does not rename it).
- The README Mermaid node + per-skill reference-table row and the CLAUDE.md skills-overview mention read coherently with the new `discuss-new-task` handle, with surrounding "backlog" prose reworded to "task"/"the task list".

---

## Rename Starting-State Heading And Its Writer Skill

Perform the two tightly-coupled, in-step renames the milestone's *Starting-state heading* and *Naming-scheme depth* decisions pair deliberately: (a) the `requirements.md` section heading `## Relevant implementation state` → `## Relevant starting state` everywhere the literal heading string is **written or read** ("implementation" is *replaced* with "starting", not dropped — "state" needs a temporal qualifier and "starting" names the pre-work baseline accurately for the milestone's whole life); and (b) the writer skill `specify-milestone-starting-implementation-state` → `specify-milestone-starting-state` (drop "implementation" in step with the heading) — directory + all self-references + dispatch/usage handles. These are distinct strings (a heading vs. a command handle) that co-occur in the writer skill's `SKILL.md`; do both. This is one of the milestone's order-free renames.

**Provides:**
- The new `requirements.md` template heading `## Relevant starting state` (the baseline-before-work section), referenced by every reader and by sibling docs.
- The renamed skill directory `skills/specify-milestone-starting-state/` (directory name IS the slash-command name `/specify-milestone-starting-state`), referenced by next-step prose and the docs.

**Notes:**
- Two independent string families, both in scope here. The **heading** `## Relevant implementation state` and the **skill handle** `specify-milestone-starting-implementation-state` are different strings — grep each separately; only the writer skill's `SKILL.md` carries both at once.
- The Success bar is the **bare** phrase `git grep "implementation state"` → zero, so the rename must catch every occurrence — the `## Relevant implementation state` heading itself **and** every bare-prose "implementation state" / "the implementation state section" mention (these read as "starting state" / "the starting state section" once renamed). Enumerated surfaces below; re-grep the bare phrase at the end to confirm none survive.
- Heading writers/template: `skills/specify-milestone-starting-implementation-state/SKILL.md` (the `description:` frontmatter, the H1-intro line, the "only surface implementation state …" line ~31, the `### 4. Write the implementation state` subheading ~52, the "Draft the … `## Relevant implementation state` section" line ~54, the emitted `## Relevant implementation state` code-block heading ~57, and the "Replace the (empty) `## Relevant implementation state` section" line ~72) and `skills/define-milestone-goal/SKILL.md` (the emitted `## Relevant implementation state` template heading at line ~55, the "Do not populate …" line at ~85, and the bare "fill in the implementation state section" prose at line ~80). Heading readers: `skills/highlight-milestone-requirements-open-questions/SKILL.md` (the `## Relevant implementation state` block + its `<description of …>` placeholder), and the task-deriver skill (two **Relevant implementation state** prose mentions — currently `skills/populate-backlog/SKILL.md`, but its `derive-tasks` rename is order-free, so `git grep` the phrase wherever that skill currently lives). Structural-blurb surfaces listing the heading names: `skills/init-milestone-base-workflow/SKILL.md` (the "`requirements.md` — goal, relevant implementation state, …" line it emits, ~47) and `README.md` line ~48 (the same blurb in the file-structure section). Doc references: `README.md` (Mermaid node label + the per-skill table description naming `## Relevant implementation state`), `CLAUDE.md` (the layout-line "fills 'Relevant implementation state'" and the file-structure line "Goal, Relevant implementation state, implementation decisions, open questions").
- Skill-handle references beyond the renamed dir + its own `SKILL.md` (frontmatter `name:`, H1, `/specify-milestone-starting-implementation-state` usage + example lines): next-step prose in `skills/define-milestone-goal/SKILL.md` (lines ~8 and ~80) and `skills/goto-next-milestone/SKILL.md` (line ~51), plus `README.md` (Mermaid node `/specify-milestone-starting-implementation-state` + the per-skill reference-table row header `### specify-milestone-starting-implementation-state <milestone_id>`) and `CLAUDE.md` (the skills-overview layout line at ~37 and the environment-context invariant at ~78).
- **LIVE structural blurb on `milestones/README.md` line 7** is in scope: `` - `requirements.md` — goal, relevant implementation state, implementation decisions, open questions `` — change only the lowercase phrase "relevant implementation state" → "relevant starting state" on this one live line. The history/Completed sections of that file are frozen — do not touch them.
- **Carve-out on shared lines:** several in-scope lines also contain the phrase "implementation decisions" / `## Implementation decisions`, which belongs to a *separate* `## Decisions` rename task — change **only** the starting-state string on those lines and leave "implementation decisions" exactly as found (e.g. `CLAUDE.md` file-structure line ~60, `define-milestone-goal` "Do not populate …" line ~85, the writer skill's H1-intro line that names the `## Implementation decisions` conversation, the two structural-blurb lines `README.md` ~48 and `skills/init-milestone-base-workflow/SKILL.md` ~47, and `milestones/README.md` line 7). Also leave the writer skill's "Sets up the context needed to make informed implementation decisions." / table description in `README.md` ~164 untouched on the "implementation decisions" clause.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` reference neither the heading nor this handle (verified by grep), so no manifest edit is needed.
- Per the milestone's *Rename ordering* decision, this task syncs its own `README.md` and `CLAUDE.md` references rather than deferring to a trailing doc-sync pass.
- Do not edit frozen surfaces: historical milestone dirs (`milestone_01_*`, `milestone_02_*`), milestone_03's own `requirements.md`/`TASKS_*`, the history/completed sections of `milestones/README.md`, the `Origin:` provenance lines in `answer_decision_principles.md`, and `.claude/settings.local.json`.

**Success:**
- `git grep "implementation state"` over live plugin surfaces (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, `.claude-plugin/`, and the live line 7 of `milestones/README.md`) returns zero hits.
- `git grep specify-milestone-starting-implementation-state` over those same live surfaces returns zero hits.
- The new heading `## Relevant starting state` is the one emitted by the `define-milestone-goal` template and the writer skill, and is the heading read by `highlight-milestone-requirements-open-questions` and `populate-backlog`.
- Directory `skills/specify-milestone-starting-state/` exists with its `SKILL.md`; the old `skills/specify-milestone-starting-implementation-state/` directory no longer exists.
- On every shared line, the phrase "implementation decisions" / `## Implementation decisions` is left exactly as found (untouched by this task).
- The README Mermaid node + per-skill reference-table row and the CLAUDE.md layout/skills-overview/invariants mentions read coherently with both the new `## Relevant starting state` heading and the new `specify-milestone-starting-state` handle.

---

