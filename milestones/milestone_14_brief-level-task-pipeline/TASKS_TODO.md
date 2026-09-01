# TASKS TODO

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
