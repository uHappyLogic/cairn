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

## Rename Decisions-Section Heading

Per the milestone's *Decisions-section heading* decision, rename the `requirements.md` section heading `## Implementation decisions` → `## Decisions` everywhere the literal heading string is **written or read** — "implementation" is *dropped entirely*, not replaced (unlike the *Relevant starting state* rename): the section sits inside `requirements.md` under a known structure, so the bare noun is unambiguous and needs no qualifier. This task is also the sole sink for the bare lowercase phrase "implementation decisions" on live surfaces — both the structural-blurb enumerations of the heading names and the few generic-concept prose mentions — so the phrase no longer survives anywhere live. This is a pure heading rename (no skill/agent handle component) and one of the milestone's order-free renames.

**Provides:**
- The new `requirements.md` template heading `## Decisions` (the folded-decisions section), referenced by every reader/writer of the heading and by the docs.

**Notes:**
- The brief's enumerated update list is **not exhaustive** — the Success bar (a case-insensitive zero-hit grep) is the real contract. Two kinds of hits, both in scope: (a) the literal heading `## Implementation decisions` written or read → `## Decisions`; (b) bare lowercase "implementation decisions" prose → drop "implementation" so it reads "decisions". The bare-prose hits split into blurb enumerations (below) **and generic-concept mentions that read as out-of-scope but are not** — `README.md` ~164 "make informed implementation decisions" (which the order-free *Rename Starting-State Heading* task deliberately left for this task), `skills/finish-current-milestone/SKILL.md` ~29 "key implementation decisions" and ~41 "Any significant implementation decisions recorded in `requirements.md`", and the writer skill's ~3 "supports future implementation decisions" / ~68 "make implementation decisions" / ~84 "Do not propose implementation decisions". The bare "implementation" drop reads coherently in every one (e.g. "Any significant **decisions** recorded in `requirements.md`") — no "decisions about implementation" gymnastics are needed. Re-grep the bare phrase (case-insensitive) at the end to confirm none survive.
- **Carve-out symmetry with the *Relevant starting state* rename.** Four blurb lines list BOTH heading names: `CLAUDE.md` (~60), `README.md` (~48), `skills/init-milestone-base-workflow/SKILL.md` (~47), and `milestones/README.md` line 7. On each, change **only** "implementation decisions" → "decisions" and leave the "implementation state" / "starting state" phrase exactly as found — its rename is owned by the order-free *Rename Starting-State Heading* task.
- **`milestones/README.md` line 7 is LIVE** (the structural blurb). The history/Completed sections of that file are frozen — do not touch them.
- Heading writers/template: `skills/define-milestone-goal/SKILL.md` (the emitted `## Implementation decisions` template heading ~57, and the "Do not populate …" list ~85). Heading readers: `shared/answer-procedure.md` (the `### 5. Fold the decision into …` subheading plus the three other mentions ~46/~59/~68), `skills/answer-open-question/SKILL.md` (~37), `skills/highlight-milestone-requirements-open-questions/SKILL.md` (the emitted block heading ~31), `skills/reject-auto-answer/SKILL.md` (~18, ~82), `agents/try-answer-question-by-principle.md` (~41), `skills/try-capture-answer-principle/SKILL.md` (~23), and `CLAUDE.md` (~20, ~70).
- Two readers are **simultaneously being renamed by order-free sibling tasks** — `git grep` the heading/phrase wherever those dirs currently live and change only the heading/phrase, leaving their handle exactly as found: the writer skill `specify-milestone-starting-implementation-state` (→ `specify-milestone-starting-state`; heading-ref ~8, do-not-overwrite list ~86, plus its generic prose ~3/~68/~84) and `try-answer-questions-by-principle` (→ `try-answer-all-questions-by-principle`; ~126).
- This task touches **only** the heading and the "implementation decisions" phrase — it must NOT alter the "implementation state"/"starting state" phrase, any skill/agent handle, or any dispatch string; those belong to their own order-free tasks.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` reference neither the heading nor the phrase (verified by grep), so no manifest edit is needed.
- Per the milestone's *Rename ordering* decision, this task syncs its own `README.md` and `CLAUDE.md` references rather than deferring to a trailing doc-sync pass.
- Do not edit frozen surfaces: historical milestone dirs (`milestone_01_*`, `milestone_02_*`), milestone_03's own `requirements.md`/`TASKS_*`, the history/completed sections of `milestones/README.md`, the `Origin:` provenance lines in `answer_decision_principles.md`, and `.claude/settings.local.json`.

**Success:**
- `git grep -i "implementation decisions"` over live plugin surfaces (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, `.claude-plugin/`, and the live line 7 of `milestones/README.md`) returns zero hits (subsuming both the capitalized `## Implementation decisions` heading form and the lowercase prose form).
- The heading `## Decisions` is the one emitted by the `define-milestone-goal` template and is the heading read by `shared/answer-procedure.md`, `highlight-milestone-requirements-open-questions`, `reject-auto-answer`, the `try-answer-question-by-principle` agent, and the answer-recording chain.
- On the four shared blurb lines, the "implementation state"/"starting state" phrase is left exactly as found (untouched by this task).
- No skill/agent handle or dispatch string is changed by this task.
- The README structural blurb + per-skill table prose and the CLAUDE.md layout/skills-overview/invariants mentions read coherently with the new `## Decisions` heading.

---


## Rename Task-Execution Machinery To Complete Vocabulary

Per the milestone's *Task-execution vocabulary* and *Rename ordering* decisions, retire "implement" as the task-execution verb in favor of **"complete"** (plain English in any domain, naming both *doing the work* and *moving the task TODO→DONE*) across the ENTIRE execution machinery, as ONE atomic unit. In a single task rename all of: the orchestrator skill `implement-backlog-tasks` → `complete-all-tasks` (fan-out grammar `<verb>-all-<plural-object>`, since it shares the verb "complete" with its per-item worker); the user-facing skill `implement-backlog-task` → `complete-task`; the agent `agents/implement-backlog-task.md` → `agents/complete-task.md`; the shared procedure `shared/implement-procedure.md` → `shared/complete-procedure.md` (and every `${CLAUDE_PLUGIN_ROOT}/shared/implement-procedure.md` reference — run inline by the `complete-task` skill, in isolation by the `complete-task` agent); the orchestrator's dispatch type-string `subagent_type: "implement-backlog-task"` → `complete-task` (the agent filename IS the dispatch string); and the orchestrator's per-task commit-emission prose. Then update every cross-reference across the whole plugin and rewrite the `.claude-plugin/plugin.json` description one-liner into fully coherent new-vocabulary prose. Keep `finish-current-milestone` exactly as-is — its "finish" verb deliberately does not compete with the task-level "complete".

**Provides:** (informational — this is the terminal task; nothing downstream is authored against it)
- The renamed skill directories `skills/complete-all-tasks/` (orchestrator) and `skills/complete-task/` (user-facing skill), the agent file `agents/complete-task.md`, the shared file `shared/complete-procedure.md`, and the dispatch type-string `complete-task` (directory/file names ARE their handles).

**Notes:**
- **This task carries the milestone's ONLY ordering constraint: it MUST be executed LAST.** The `implement-backlog-tasks`/`complete-all-tasks` orchestrator re-reads the agent file and the shared procedure fresh from disk on every iteration and dispatches its worker by a fixed agent-type string held in its frozen context — renaming any part of this family before its last use breaks the in-flight run, and splitting it would leave a later dispatch reading a half-renamed procedure. As the explicit "do-by-hand-if-you-prefer" safety valve (per *Rename ordering*), this final rename MAY instead be performed **by hand in the main conversation after the orchestrated run finishes every other task**, so the riskiest step never runs through the self-modifying path.
- **The "commit-subject convention" has no literal format string to change.** The orchestrator commits with `git commit -m "<task heading>"` (around lines 55–58) — the subject is the task's `##` heading verbatim, not the word "implement." So "restate it in the new vocabulary" means rewording the orchestrator's *prose*, not a commit-format token: e.g. the `description:` frontmatter, line ~8 "implements exactly one task", ~36 "Spawn a subagent to implement the task", ~66 "list each task that was implemented", ~73 "never implement tasks directly here". Do not hunt for a nonexistent literal commit string.
- **Execution-family handle/procedure references to update** (the `implement-backlog-task`/`implement-backlog-tasks`/`implement-procedure` tokens): both renamed skills' own `SKILL.md` (frontmatter `name:`, H1, `/…` usage lines, self-references, and the directory renames); `agents/implement-backlog-task.md` (frontmatter `name:` + the `${CLAUDE_PLUGIN_ROOT}/shared/implement-procedure.md` reference + the file rename); `shared/implement-procedure.md` (its own title/body naming the skill+agent+orchestrator, and the file rename); `shared/submit-procedure.md` (~39 names the `implement-backlog-task` agent; ~124 and ~149 name the `/implement-backlog-task` atomic-scope anchor); the issue-clarification skill (currently `skills/discuss-new-backlog-task/` — `/implement-backlog-task` anchors ~66, ~125; its own `-backlog` rename is order-free, so grep the `/implement-backlog-task` token wherever that skill currently lives) and the task-deriver skill (currently `skills/populate-backlog/` — the `/implement-backlog-task` anchor ~57 and the "mirrors the implement side: `implement-backlog-tasks` orchestrates and `implement-backlog-task` does the per-task work" line ~12; grep wherever that skill currently lives); `README.md` (Mermaid nodes `/implement-backlog-tasks` ~88 and `/implement-backlog-task` ~96, the per-skill reference-table rows `### implement-backlog-tasks` ~214 and `### implement-backlog-task` ~218 — note the skill row's body ~220 legitimately cross-refs the orchestrator `/implement-backlog-tasks` for the unattended case, so update both handles and keep that cross-ref intact, plus any altitude/atomic prose naming the handle); and `CLAUDE.md` (the layout lines ~15/~18, the skills-overview lines ~49/~50/~51, and the long invariants list which names this skill+agent+shared file repeatedly — ~71, ~74, ~75 the "Two orchestrators commit" invariant, ~78, ~83, ~84 the inline-vs-isolated distinction, ~85).
- **Terminal verb sweep with a heading carve-out.** This task also owns the plain-English verb "implement" wherever it names task execution — e.g. example phrasings like "Implement X and Y" (in the issue-clarification and deriver skills) and the README altitude/atomic prose — reword to the "complete" vocabulary. It must **NOT** touch the phrases `implementation decisions` / `## Implementation decisions` or `implementation state` / `## Relevant implementation state` — those two heading strings are owned by the order-free *Rename Decisions-Section Heading* and *Rename Starting-State Heading* sibling tasks. Because this runs last, those phrases are already gone; any `-i implement` heading-phrase remnant is a sibling's bug, not this task's to fix.
- **Mixed-handle carve-out (simple, because this runs last).** Several shared lines name sibling handles alongside the execution family (e.g. `CLAUDE.md` ~71 names `try-answer-questions-by-principle`/`try-answer-all-questions-by-principle`; ~78 names the specify/derive handles). By the time this task runs every sibling handle is already at its NEW name — so touch only the execution-family tokens (`implement-backlog-task`, `implement-backlog-tasks`, `implement-procedure`, the verb "implement") and leave everything else exactly as found.
- **Manifest coherence ownership — `.claude-plugin/plugin.json` only.** Its description currently reads "…discuss goals, define milestones, populate backlogs, implement tasks, and archive milestones". This task is the final owner of that one-liner: only now are all renamed handles final, so rewrite the sentence to read cleanly end-to-end in the new vocabulary — retire "implement tasks" and reconcile the earlier "populate backlogs"→"derive tasks" waypoint (left half-done by the *Rename Populate-Backlog To Derive-Tasks* task) into fluent prose. `.claude-plugin/marketplace.json` is grep-confirmed clean ("Milestone-driven development for any stack." — no handle, no "implement"/"populate"), so leave it as-is unless a hit actually appears.
- Do not edit frozen surfaces: historical milestone dirs (`milestone_01_*`, `milestone_02_*`), milestone_03's own `requirements.md`/`TASKS_*`, the history/completed sections of `milestones/README.md`, the `Origin:` provenance lines in `answer_decision_principles.md`, and `.claude/settings.local.json`.

**Success:**
- `git grep complete-all-tasks` resolves to the renamed orchestrator and `git grep complete-task` to the skill + agent; `git grep implement-backlog-task` and `git grep implement-backlog-tasks` over live plugin surfaces (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, `.claude-plugin/`) each return zero hits.
- Directories `skills/complete-all-tasks/` and `skills/complete-task/` exist with their `SKILL.md`; `agents/complete-task.md` and `shared/complete-procedure.md` exist; the old `skills/implement-backlog-tasks/`, `skills/implement-backlog-task/`, `agents/implement-backlog-task.md`, and `shared/implement-procedure.md` no longer exist.
- The orchestrator's dispatch call reads `subagent_type: "complete-task"` and resolves to `agents/complete-task.md`; the `complete-task` skill and agent both reference `${CLAUDE_PLUGIN_ROOT}/shared/complete-procedure.md`.
- A final `git grep -i "implement"` over live plugin surfaces returns zero hits in handles, headings, and dispatch strings (any residual hit is legitimately-remaining plain English only — there should be essentially none).
- `.claude-plugin/plugin.json`'s description one-liner reads coherently end-to-end in the new vocabulary, naming neither "implement tasks" nor "populate backlogs".
- README Mermaid nodes + the per-skill reference-table rows (orchestrator, skill, agent), the CLAUDE.md layout/skills-overview/invariants mentions (including the inline-vs-isolated distinction and the "two orchestrators commit" invariant), and all next-step/atomic-scope prose read coherently with the new `complete-all-tasks` / `complete-task` handles.
- `finish-current-milestone` is unchanged.

---

## Reconcile Residual Heading/State Echoes With Completed Renames

Two skills still carry "implementation"-flavored prose that names sections this milestone already renamed, leaving them inconsistent with the shipped vocabulary. `answer-open-question` reports document changes as "implementation-decision updates", which must reflect the renamed `## Decisions` section. `goto-next-milestone` suggests the user "fill in the implementation context", referring to the section now named `## Relevant starting state` (written by `specify-milestone-starting-state`). Reword both so they read as plain, domain-neutral English consistent with the completed renames, without changing what either skill does.

**Notes:**
- The two sites: `skills/answer-open-question/SKILL.md` (the "what changed" reporting line — "implementation-decision updates") and `skills/goto-next-milestone/SKILL.md` (the next-step suggestion — "fill in the implementation context").
- Match the already-shipped vocabulary: decisions live under `## Decisions`; the baseline section is `## Relevant starting state`. Do not reintroduce a retired term.

**Success:**
- `git grep -ni implementation -- skills/answer-open-question skills/goto-next-milestone` returns zero hits.
- Both skills still describe the same behavior (answer-open-question still reports which parts of the document changed; goto-next-milestone still points at filling the starting-state section as the next step).

---

## Retire Coding-Flavored "Implementation Phase" Framing In Highlight-Open-Questions

`highlight-milestone-requirements-open-questions/SKILL.md` repeatedly frames the post-requirements work as "implementation" — the phase, its choices, and when it "begins" (e.g. "ready enough for implementation", "the implementation phase", "leave implementation choices ambiguous", "force a wrong implementation", "before implementation begins", "decided during implementation", "begin implementation"). This is the coding-specific vocabulary the milestone's goal retires so the plugin reads as a generic idea-to-done workflow. Reword these to domain-neutral terms that preserve the skill's logic, keeping the Blocking/Deferred question distinction intact (Blocking = must be resolved before the work starts; Deferred = settle while doing the work).

**Notes:**
- Per the project's *Prefer domain-neutral terms* answering principle, word choice is case-by-case — pick the natural neutral phrasing per sentence (e.g. "the work", "before work begins", "while doing the work", "at completion time"); do not mechanically substitute one fixed token.
- Scope is this one file. Do not touch the protected/renamed handles or headings — only the generic "implementation" prose.

**Success:**
- `git grep -ni implement -- skills/highlight-milestone-requirements-open-questions` returns zero hits.
- The skill still distinguishes Blocking from Deferred questions and still emits the `> **Deferred — <Short Title>:**` annotation format unchanged.

---

## Sweep Scattered Generic "Implementation" Prose From The Authoring/Clarification Skills

Four skills still use the word "implementation"/"implementable" incidentally in prose, leftover coding flavor the milestone's goal retires: `discuss-new-task` ("ambiguous implementation issue", "mid-implementation", "full implementation detail", "independently implementable", "concrete implementation issue" — including in its `description:` frontmatter), `submit-task` ("single implementation issue", "implementation-ready task" — including its `description:` frontmatter), `derive-tasks` ("independently-implementable task briefs", "satisfied by the current implementation" ×2), and `specify-milestone-starting-state` ("internal implementation detail"). Reword each to neutral English that keeps the meaning (e.g. "issue", "mid-flight", "detail", "independently completable", "the existing/current code").

**Notes:**
- Per the *Prefer domain-neutral terms* answering principle, choose phrasing case-by-case; some hits sit in the skills' `description:` frontmatter (their discoverability text) — reword those too, keeping the description's trigger meaning intact.
- Leave the renamed handles/headings and the `complete`/`derive`/`submit` vocabulary already shipped untouched — this task only retires the residual generic "implementation" wording in these four files.

**Success:**
- `git grep -ni implement -- skills/discuss-new-task skills/submit-task skills/derive-tasks skills/specify-milestone-starting-state` returns zero hits.
- Each skill's `description:` frontmatter still reads coherently and conveys the same when-to-use trigger.

---
