# TASKS TODO

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

---

## Reconcile README With Flattened Pipeline

Rewrite every passage of the repo-root `README.md` that the flattened brief-level task pipeline invalidates, so the plugin's public documentation describes the design as the prior tasks actually implemented it. That covers the skill-reference entries for `derive-tasks` (currently "delegates detailed task authoring to the `submit-task` agent"), `submit-task`, and `discuss-new-task`, the *Automated one-shot task derivation and completion* section's prose and diagram, and the *How it works* `TASKS_DONE.md` line — leaving no mention of the retired `submit-task` agent or of per-brief delegation anywhere in the file.

**Notes:**
- `README.md` has no repository-layout listing, so the stale references are confined to the *How it works* file list, the pipeline sections, and the `## Skill reference` entries — a full-file grep for `submit-task`, `agent`, and `deleg` is the reliable sweep.
- The *Automated one-shot task derivation and completion* diagram already has no delegation node; its prose is the part to check. Do not restructure the six per-phase diagrams or their `D0`–`D5` seam nodes — they are a deliberate milestone-4 design.
- Not every `submit-task` mention is stale: the user-facing `/submit-task` **skill** references (in the follow-up pipeline section and diagram, the `discuss-new-task` and `ask-in-milestone-context` entries, and the commit section's `Task-submission:` subject) stay. Only agent-implying and full-template wording goes.
- The commit-convention section's "**Dispatched subagents never commit**" rule and its `/derive-tasks` "once at the end of the run" granularity both remain true and correct — `derive-tasks` still commits once at the end, it just no longer dispatches anything.
- The `CLAUDE.md` reconciliation sibling task fixes the same design in the project instructions; mirror its wording — `shared/task-format.md` as the brief-level template's single home, `derive-tasks` and the `submit-task` skill as its two authoring runners, and `complete-task` as the plugin's only remaining skill+agent pair.
- `scripts/migrate_skills_to_agy.py` copies only `skills/` and `agents/`; `README.md` has no generated twin, so this task needs no transpile re-run.
- This task edits `README.md` only.

**Success:**
- `README.md` contains no occurrence of `submit-procedure`, no phrase describing a `submit-task` agent, and no statement that task authoring is delegated per brief to an agent.
- Its `derive-tasks` skill-reference entry states that the skill writes the ordered brief-level tasks into `TASKS_TODO.md` itself, with no delegation step.
- Its `submit-task` and `discuss-new-task` entries describe brief-level output and promise no `Provides`, `Notes`, or `Success` section, nor any other structured done-ness section.
- The *Automated one-shot task derivation and completion* section's prose and diagram describe derivation as a single writing step — no delegation clause, node, or edge.
- The `TASKS_DONE.md` bullet in *How it works* states that a completed entry carries the acceptance bar the completer derived, recorded as a `**Verified:**` bullet list.
- Every agent `README.md` names exists under `agents/`, and its `## Skill reference` contains exactly one `submit-task` entry (the skill).

---

## Regenerate The Antigravity Plugin Tree

Re-run the transpilation (`uv run scripts/migrate_skills_to_agy.py` from the repository root) once every source change of this milestone has landed — the shared format-file rename, the `derive-tasks` rewrite, the `submit-task` agent deletion, the `submit-task` skill lean-down, the completion-procedure rework, and the `CLAUDE.md`/`README.md` reconciliations — and check the regenerated `.agents/plugins/cairn/` tree in. The script rmtree-and-copies `agents/` wholesale, so the generated twin of the deleted `agents/submit-task.md` disappears on its own; this task is what makes the source retirement actually complete in the checked-in generated tree.

**Notes:**
- This task must run **last** in the milestone — it transcribes whatever the root sources say at the moment it runs, so any sibling task landing afterwards would leave the generated tree stale again.
- The script resolves `skills`, `agents`, and `.mcp.json` as **relative** paths, so it must be invoked from the repository root. There is no `.mcp.json` in this repo; the `No source MCP config found at .mcp.json` line it prints is expected output, not a failure.
- Skill directories whose name ends in `-workspace` are skipped by design, so `migrate-workspace` deliberately has no generated twin — its absence is not drift.
- The script may rewrite an unquoted YAML `description:` value into quoted form on its way out, so a generated `SKILL.md` can differ textually from its root source without that being drift.
- It exits 1 with a hard error if any `SKILL.md` is missing `name` or `description` in its frontmatter. If that fires, fix the **root** source file — never hand-edit anything under `.agents/`, which is generated output only.

**Success:**
- `uv run scripts/migrate_skills_to_agy.py` run from the repository root exits 0.
- `.agents/plugins/cairn/agents/submit-task.md` does not exist.
- `.agents/plugins/cairn/agents/` contains exactly one `.md` file per file in the root `agents/` directory, with matching names.
- `.agents/plugins/cairn/skills/` contains exactly one directory, each holding a `SKILL.md`, per root `skills/` subdirectory other than `migrate-workspace`.
- Running the script a second time immediately afterwards leaves `.agents/plugins/cairn/` unchanged (`git status --porcelain .agents/` reports nothing once the regenerated tree is committed).

---
