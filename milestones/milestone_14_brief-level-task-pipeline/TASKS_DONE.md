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

## Lean Down The Submit-Task Skill

Rewrite the authoring core of `skills/submit-task/SKILL.md` so the ad-hoc path produces brief-level tasks: instead of running the retired `shared/submit-procedure.md`, the skill authors the task section in the format defined by `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md` and then locates the insertion point and inserts the section itself, since the POSITION-insertion step no longer lives in the shared file. Everything format-independent stays as it is — the triage, the position decision, and the `Task-submission: <task title>` commit wrapper. This is what keeps every entry in `TASKS_TODO.md` at one consistent brief-level altitude whichever path authored it.

**Provides:**
- `skills/submit-task/SKILL.md` as a brief-level author referencing `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md`, with the insertion step (position anchors and the mandatory trailing `---`) owned by the skill itself.

**Notes:**
- The insertion semantics moving into this skill are the ones dropped from the shared file: `append` adds at the end, `before: <Title>` inserts immediately before that section's `##` heading line, `after: <Title>` inserts immediately after that section's trailing `---`, an unfound anchor falls back to appending (and says so), existing sections are never modified or reordered, and the `---` separator is mandatory because `shared/complete-procedure.md` parses sections by it.
- "Retire The Submit-Task Agent" already strips this file's agent references (the "for bulk authoring… spawns the `submit-task` **agent**" paragraph and the two never-spawn/never-delegate prohibitions), so the inline-never-spawn-the-agent stance is moot by the time this task runs — do not reintroduce it, and drop any surviving "the agent can't"/"only the context differs" framing for the inline authoring rationale (keeping the inline context for follow-up is still the reason, just no longer stated as a contrast with an agent).
- The intro prose and the YAML `description` both promise a "fully-specified"/"properly formatted task" with contract surface and success criteria; both need to read brief-level. The frontmatter must keep its `name` and `description` keys — `scripts/migrate_skills_to_agy.py` hard-errors without them.
- Steps 0–3 (milestone resolution, triage reads, duplicate/scope triage, position decision) and steps 5–6 (the commit hand-off to `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, the terse `Task submitted.` line, the no-op message, and the too-vague → `/discuss-new-task` stop) are format-independent and stay behaviourally unchanged.
- Re-running the transpilation script to regenerate `.agents/plugins/cairn/` is a milestone-wide sweep, not part of this task.

**Success:**
- `skills/submit-task/SKILL.md` references `${CLAUDE_PLUGIN_ROOT}/shared/task-format.md` and contains no occurrence of `submit-procedure`.
- It contains no reference to a `submit-task` agent and no spawn/delegate prohibition.
- It carries an insertion step covering `append`, `before: <Title>`, `after: <Title>`, the unfound-anchor append fallback, and the mandatory trailing `---`.
- Neither its authored-output description nor its YAML `description` promises `Provides`, `Notes`, or `Success` sections, or any other structured done-ness section.
- It still contains the duplicate/scope triage step, the position-decision step, the commit step supplying `<MILESTONE_DIR>/TASKS_TODO.md` and `Task-submission: <task title>` to `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`, the terse `Task submitted.` line, and its no-op message.
- Its YAML frontmatter still carries both `name` and `description`.

---

## Rework Completion Procedure For Brief Tasks

Rework `shared/complete-procedure.md` so it knows only the brief-level task shape: it derives each task's formal acceptance bar itself from the task description plus `<MILESTONE_DIR>/requirements.md` (replacing the retired authored **Success** section as the step-4 verification gate), and resolves cross-task references by reading prior tasks' live deliverables rather than an authored **Provides** contract. Its TODO→DONE move becomes move-plus-augment, appending the derived bar to the `TASKS_DONE.md` entry so each finished entry records what done actually meant. This is what makes the completion path self-sufficient once tasks carry brief-level detail only.

**Provides:**
- `shared/complete-procedure.md` as the brief-level completion contract: acceptance bar derived from description + `requirements.md`, cross-task references resolved from prior tasks' live deliverables.
- The `**Verified:**` bold label introducing the per-criterion bullet list appended to each `TASKS_DONE.md` entry — the label later milestone grounding reads, deliberately distinct from the retired template's `**Success:**`.

**Notes:**
- Clean cutover per the recorded decision: legacy **Provides**/**Notes**/**Success** sections in existing task lists get **no** privileged parsing — they are read as ordinary body prose feeding the derived bar. Do not add a compatibility branch, and leave `migrate-workspace` untouched.
- The section-location mechanics are format-independent and stay exactly as they are: the `##` heading through its trailing `---`, case-insensitive partial heading match, and the clean stop listing available headings on a miss.
- The whole "Honor the two optional sections" block in step 3 goes, along with step 1's parse-Provides/Notes/Success instruction and step 4's re-read-the-**Success**-section framing; step 4 stays criterion-by-criterion and still applies `CLAUDE.md`'s done-verification convention when one exists.
- Step 3's recorded-paths running list stays as-is — the wrappers read that set — as does the file's execution-neutrality (no commit steps, no `DONE`/`FAILED` protocol).
- Wrapper contracts are untouched by this task: `skills/complete-task/SKILL.md`, `agents/complete-task.md`, and `skills/complete-all-tasks/SKILL.md` couple to the task format only through this file, so do not edit them.
- `scripts/migrate_skills_to_agy.py` copies only `agents/` and `skills/` into `.agents/plugins/cairn/`; `shared/` has no generated twin, so this change needs no transpile re-run.

**Success:**
- `shared/complete-procedure.md` contains no instruction to parse or honor a **Provides**, **Notes**, or **Success** section, and no other privileged handling of them.
- It states that the acceptance bar is derived from the task description plus `<MILESTONE_DIR>/requirements.md`, and step 4 verifies against that derived bar criterion-by-criterion, still applying `CLAUDE.md`'s done-verification convention when one exists.
- It states that cross-task references are resolved by reading prior tasks' live deliverables, given that tasks run in order.
- Its TODO→DONE step appends the derived bar to the `TASKS_DONE.md` entry as a bold-labeled bullet list under the description — one bullet per criterion, inside the same `##`/`---` section — under a label distinct from `**Success:**`.
- It still locates the task by case-insensitive partial `##`-heading match and still stops cleanly listing the available headings on a miss.
- It still contains no commit step and no `DONE`/`FAILED` return protocol.

**Verified:**

- `shared/complete-procedure.md` contains no instruction to parse or honor a **Provides**, **Notes**, or **Success** section, and no other privileged handling of them — a grep for those labels returns nothing, and the new "The task shape" section states that no part of a task body gets privileged parsing.
- It states that the acceptance bar is derived from the task description plus `<MILESTONE_DIR>/requirements.md` (step 2), and step 4 verifies against that derived bar criterion-by-criterion, still applying `CLAUDE.md`'s done-verification convention when one exists with direct inspection as the fallback.
- It states that cross-task references are resolved by reading prior tasks' live deliverables, given that tasks run in order (the task-shape section and step 3).
- Its TODO→DONE step (step 5) is a move-plus-augment that appends the derived bar to the `TASKS_DONE.md` entry as a `**Verified:**`-labeled bullet list under the description — one bullet per criterion, inside the same `##`/`---` section — a label distinct from the retired `**Success:**`.
- It still locates the task by case-insensitive partial `##`-heading match, from the `##` heading through its trailing `---`, and still stops cleanly listing the available headings on a miss.
- It still contains no commit step and no `DONE`/`FAILED` return protocol; the only remaining mentions of committing are the pre-existing wrapper-framing disclaimer and the record-paths clarification.

---

## Reconcile CLAUDE.md With Flattened Pipeline

Rewrite every `CLAUDE.md` layout entry, skills-pipeline listing line, and invariant that the flattened brief-level task pipeline invalidates, so the repo's own project instructions describe the design as the prior tasks actually implemented it. That covers the layout entries for the deleted `agents/submit-task.md` and for the renamed `shared/task-format.md`, the pipeline lines for `derive-tasks`/`submit-task`/`discuss-new-task`, and the invariants for derive-tasks' delegation, the task-body template, task altitude, and the retired submit-task skill+agent pair.

**Provides:**
- `CLAUDE.md` as the reconciled description of the flattened pipeline — the wording a sibling `README.md` reconciliation mirrors: `shared/task-format.md` as the brief-level template's single home, `derive-tasks` and the `submit-task` skill as its two authoring runners with `shared/complete-procedure.md` as its parser, and `complete-task` as the plugin's only remaining skill+agent pair.

**Notes:**
- Three `submit-procedure`/agent references sit **outside** the brief's enumeration and are easy to miss: the commit invariant's commit-free shared-procedure list (which names `submit-procedure.md`), the "Both shared procedures … always resolve `<MILESTONE_DIR>` by following `shared/get-current-milestone.md`" invariant (`shared/task-format.md` no longer resolves anything — milestone resolution now lives in `derive-tasks` and the `submit-task` skill), and the `shared/submit-procedure.md` layout line's "followed inline by the skill and in isolation by the agent" framing.
- Not every `submit-task` mention is stale: references to the user-facing `/submit-task` **skill** (e.g. in the `ask-in-milestone-context` invariant and the commit invariant's per-skill subject list, where `Task-submission: <task title>` is unchanged) stay. Only agent-implying wording goes.
- The recorded decisions fix the replacement wording: clean cutover on legacy `Provides`/`Notes`/`Success` sections (no compatibility branch, `migrate-workspace` untouched), the brief template's home in the shared file referenced by both authoring runners, and the completer recording its derived bar as a `**Verified:**` bullet list in the `TASKS_DONE.md` entry.
- `scripts/migrate_skills_to_agy.py` copies only `skills/` and `agents/`; `CLAUDE.md` has no generated twin, so this task needs no transpile re-run.
- This task edits `CLAUDE.md` only — `README.md` and the generated `.agents/` tree belong to sibling tasks.

**Success:**
- `CLAUDE.md` contains no occurrence of `submit-procedure` and no occurrence of `agents/submit-task.md`.
- It contains no phrase describing a `submit-task` agent — no "submit-task agent", no spawn/dispatch-per-brief step, and no listing of `submit-task` as a skill+agent pair.
- Its repository-layout section lists `shared/task-format.md`, and every `shared/` and `agents/` path it names exists on disk.
- Its skills-pipeline listing contains exactly one `submit-task` line (the skill), and its `derive-tasks` line says the skill writes the briefs into `TASKS_TODO.md` itself.
- Its task-template invariant names `shared/task-format.md` as the single home of a brief-level template (`##` title, 1–3 sentence description, trailing `---`) with the four carried-over authoring guidelines, and describes no authored `Provides`, `Notes`, or `Success` section.
- Its task-altitude invariant states that the completer derives the acceptance bar from the task description plus `requirements.md`, resolves cross-task references from prior tasks' live deliverables, and records the bar as a `**Verified:**` bullet list in the `TASKS_DONE.md` entry.

**Verified:**

- `CLAUDE.md` contains no occurrence of `submit-procedure` and no occurrence of `agents/submit-task.md` (both greps return 0).
- It contains no phrase describing a retired per-brief authoring agent — no "submit-task agent" string, no spawn/dispatch-per-brief step, and no listing of `submit-task` as a skill+agent pair; the only surviving `skill+agent pair` mention states that `submit-task` has no agent counterpart and `complete-task` is the plugin's only remaining pair.
- Its repository-layout section lists `shared/task-format.md` (replacing the retired `shared/submit-procedure.md` entry, with the `agents/submit-task.md` entry deleted), and every `shared/` and `agents/` path that section names exists on disk.
- Its skills-pipeline listing contains exactly one `submit-task` line (the skill, marked "skill only, no agent"), and its `derive-tasks` line says the skill writes those briefs directly into `TASKS_TODO.md` itself, delegating nothing.
- Its task-template invariant names `shared/task-format.md` as the single home of the brief-level template (`##` title heading, 1–3 sentence description with the how-it-would-be-verified clause folded in as prose, mandatory trailing `---`) with the four carried-over authoring guidelines (unique 4–8 word title, atomic scope, no open decisions, quote numeric values from `requirements.md`), and describes no authored `Provides`, `Notes`, or `Success` section — the only mentions of those labels are explicit negations.
- Its task-altitude invariant states that `shared/complete-procedure.md` derives the formal acceptance bar itself from the task description plus `requirements.md`, resolves every cross-task reference by reading the prior task's live deliverable, and records the derived bar in the `TASKS_DONE.md` entry as a `**Verified:**`-labeled bullet list, one bullet per criterion, inside the same `##`/`---` section.
- The three references outside the brief's enumeration are reconciled: the commit invariant's commit-free shared-procedure list no longer names `submit-procedure.md`, the milestone-resolution invariant now names `shared/complete-procedure.md`, `derive-tasks`, and the `submit-task` skill (noting `shared/task-format.md` resolves nothing), and the completion-procedure invariant now reads "derive the acceptance bar … verify against that derived bar … move TODO→DONE augmented with it".
- Only `CLAUDE.md` changed: `git status --porcelain` reports `M CLAUDE.md` and nothing else, and no transpile re-run was needed since the script copies only `skills/` and `agents/`.

---
