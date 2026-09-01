# Milestone 14: Brief-level task pipeline

## Goal

Flatten the task pipeline to brief-level tasks: derive-tasks writes its ordered briefs directly into TASKS_TODO.md (same ## heading + --- section format, brief-level detail only — no Provides/Notes/Success sections), retiring the submit-task agent and the per-brief dispatch loop. shared/complete-procedure.md is reworked to derive each task's acceptance bar itself from the task description plus requirements.md, and to resolve cross-task references by reading prior tasks' live deliverables (tasks run in order). The user-facing submit-task skill is leaned down to author the same brief-level format, keeping all tasks in TASKS_TODO.md at one consistent altitude; CLAUDE.md invariants and README.md are reconciled to the flattened design.

## Relevant starting state

### derive-tasks skill

`skills/derive-tasks/SKILL.md` owns decomposition and coverage only: it decomposes `requirements.md` into high-level briefs (each naming the affected system, desired behavior, and how it would be verified — explicitly no file paths, contract surface, or success criteria), proves coverage via a requirement→brief traceability matrix, orders briefs by dependency, initializes `TASKS_TODO.md` to a bare `# TASKS TODO` header, then spawns the `submit-task` agent once per brief, strictly sequentially, with `POSITION: append`. Its rules forbid it from authoring task bodies itself ("never author the task yourself as a fallback"). It commits once at the end of the run under `Task-derivation: <milestone_id>`, path-scoped to `TASKS_TODO.md`. Its step-2 precondition still scans for the retired `> **Open question` blockquote form rather than the current `<open-question>` XML blocks — a stale idiom that will be touched when the file is rewritten.

### submit-task agent

`agents/submit-task.md` is the bulk per-brief authoring subagent whose **sole caller is derive-tasks**. It takes BRIEF + POSITION from its prompt, runs `shared/submit-procedure.md` in isolation, never commits, and returns `DONE: "<task title>" — <where inserted>` (flagging any leftover second piece per the atomic-scope rule) or `FAILED: <reason>`. Retiring it leaves no other consumer of the agent.

### submit-task skill

`skills/submit-task/SKILL.md` is the user-facing entry (and the handoff target of `/discuss-new-task`). It owns triage (duplicate detection against TODO/DONE, scope check against the milestone) and the position decision (`before:`/`after:`/`append`) from the whole-task-list view, then runs `shared/submit-procedure.md` inline so the authoring context survives, and commits under `Task-submission: <task title>`. Its authored output is currently the full-template task; only the authoring core changes when tasks lean down — triage, positioning, and the commit wrapper are format-independent.

### shared/submit-procedure.md — the task template

The single source of truth for the task body template: `## <Title>`, a 1–3 sentence description, optional **Provides** (the forward contract — names/thresholds sibling tasks reference before the task is built), optional **Notes** (non-obvious gotchas), mandatory **Success** (verification-only criteria), and a mandatory trailing `---` separator. It also holds the "task is a contract, not a script" altitude doctrine and the authoring guidelines (title shape, quote-numeric-values, atomic scope, no open decisions). It is execution-neutral (BRIEF + POSITION in, insertion at the given position, no ordering decisions) and is consumed by exactly two runners: the `submit-task` skill (inline) and the `submit-task` agent (isolated). With the agent retired it drops to one consumer, which under the project's "shared = source of truth across ≥2 runners" convention means its surviving content belongs inlined in the skill.

### shared/complete-procedure.md — the completion contract

The single source of truth for completing one task, consumed by the `complete-task` skill (inline) and the `complete-task` agent (isolated, spawned per task by `complete-all-tasks`). It locates the task as a `##` section terminated by `---` (case-insensitive partial heading match, clean stop listing available headings on a miss), parses description + optional **Provides**/**Notes** + **Success**, already owns flow derivation ("the task gives you the goal, not a procedure — you own the design"), verifies criterion-by-criterion against the **Success** section in step 4 (with `CLAUDE.md`'s done-verification convention when one exists), records touched paths as it edits, and moves the section TODO→DONE. Its step-4 verification gate and the step-1/step-3 references to Provides/Notes/Success are the parts coupled to the rich template; the `##`/`---` section mechanics are format-independent and already match the brief-level shape.

### Completion wrappers

`skills/complete-task/SKILL.md` (inline, commits `Task-completion:` with recorded paths + the two task-list files), `agents/complete-task.md` (isolated, hands recorded paths back above its `DONE` line, never commits), and `skills/complete-all-tasks/SKILL.md` (pure orchestrator, one subagent per task top-to-bottom, commits per task under `Tasklist-completion:` with the heading in the body). All three couple to the task format only through `shared/complete-procedure.md`; their return protocols, path hand-back, and commit mechanics are unaffected by a leaner task body.

### discuss-new-task

`skills/discuss-new-task/SKILL.md` clarifies a vague or oversized issue into one or more task-sized briefs and hands each off to the `/submit-task` skill. The handoff shape (a brief) is unchanged by this milestone; with brief-level tasks the handoff brief maps near-1:1 onto the final task body instead of being fleshed out further.

### Documentation coupled to the current design

`CLAUDE.md` carries invariants this milestone invalidates: the repo-layout entries for `agents/submit-task.md` and `shared/submit-procedure.md`, the "derive-tasks owns decomposition and coverage only; must not author task bodies" invariant, the task-body-template single-source invariant, the task-altitude split ("what can be re-derived at completion time"), and the "submit-task exists as both skill and agent" invariant. `README.md` describes the same design in its skill reference (`derive-tasks` "delegates detailed task authoring to the submit-task agent", `submit-task`, `discuss-new-task`) and in the automation-pipeline section/diagram.

### Antigravity transpilation

`scripts/migrate_skills_to_agy.py` regenerates `.agents/plugins/cairn/` from the root sources: it rmtree-and-copies `agents/` wholesale, so deleting `agents/submit-task.md` and re-running the script removes the generated twin. The generated tree is checked in, so a source retirement is not complete until the script has been re-run.

## Decisions

### Legacy task-list handling

The reworked shared/complete-procedure.md knows only the brief-level task shape (clean cutover): legacy Provides/Notes/Success sections in existing task lists carry no privileged status and are read as ordinary body prose feeding the derived acceptance bar. migrate-workspace stays untouched — old-format task lists drain naturally, since the ##/--- section mechanics are unchanged.

### Brief template home

The brief-level task template and its authoring guidance live in a single shared file — the slimmed successor of `shared/submit-procedure.md`, stripped to just the template and its authoring guidelines (the milestone-resolution, context-loading, and POSITION-insertion steps drop out, since the two skills now handle those differently) — referenced via `${CLAUDE_PLUGIN_ROOT}` by both `derive-tasks` and the leaned-down `submit-task` skill. Two runners author the format and a third (`shared/complete-procedure.md`) parses it, so the shared-is-source-of-truth-across-at-least-two-runners convention is satisfied and drift between the batch and ad-hoc authoring paths is ruled out by construction. The file is renamed to describe the task format rather than a submit procedure, since the insertion and positioning steps no longer live in it.

### Brief body contents

A brief-level task section is the `##` heading, a 1–3 sentence description, and the trailing `---` separator — nothing else. The loose "how it would be verified" clause stays part of the body as prose folded into those sentences rather than a labeled section, so no structured done-ness section survives to regrow (the completer still derives the formal acceptance bar from the description plus `requirements.md`). All four current authoring guidelines carry over to brief authoring unchanged — atomic scope, no open decisions, quote numeric values from `requirements.md`, and unique 4–8 word titles — since each is format-independent; title uniqueness in particular is load-bearing, because the completion procedure locates a task by case-insensitive partial heading match.

### Acceptance-bar record

The completer records the acceptance bar it derived from the task description plus `requirements.md` in the `TASKS_DONE.md` entry: `shared/complete-procedure.md`'s TODO→DONE move becomes move-plus-augment, appending the derived bar to the section it writes into `TASKS_DONE.md`, so each finished entry carries the brief plus the bar the work was actually verified against. This keeps a durable statement of what done meant once the authored Success section is retired, in the one file the completion procedure already writes and later milestone grounding already reads — a single-file change with no wrapper contract, so the completion wrappers' return protocols and commit mechanics are unaffected.

## Out of Scope

## Open questions

<open-question id="Done-entry bar rendering" status="deferred">
  <question>When the reworked shared/complete-procedure.md appends the derived acceptance bar to a finished task&apos;s TASKS_DONE.md entry, what rendering shape does the appended bar take (e.g. a labeled criteria list under the description vs. folded prose), so finished entries stay consistently readable for later milestone grounding?</question>
</open-question>
