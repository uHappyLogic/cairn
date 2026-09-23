# Milestone 32: Unified task-completion subject

## Goal

Every task-completion commit uses the same subject, `Task-completion: <Task Title>`, where `<Task Title>` is the task's `##` heading text, verbatim. `/complete-all-tasks` stops using the fixed `Tasklist-completion: complete one milestone task` subject and its heading-in-body commits, and commits subject-only, the same as inline `/complete-task`. The runtime files, the docs that describe these commits (`docs/skill-reference.md`, `docs/workflow.md`), and the rebuilt `hosts/` trees are all brought into line, and existing history is left as it is.

## Relevant starting state

### The two task-completion runners

`core/skills/complete-task/SKILL.md` (inline) and `core/skills/complete-all-tasks/SKILL.md` (orchestrator) are the only two places a task-completion commit is made; both run `core/shared/complete-procedure.md`, and the dispatched `core/agents/complete-task.md` stages its change set path-scoped but never commits. The inline skill's step 2 hands the shared commit procedure two inputs, PATHS and the subject `Task-completion: <task heading>`, with no BODY, so it already commits subject-only under the task heading. The orchestrator's step 2c does not use the commit procedure: it commits the agent-staged index itself with `git commit -m "<subject>" -m "<body>"` behind a `git diff --cached --quiet` nothing-staged guard, under the subject `Tasklist-completion: <descriptor>` (the only descriptor ever used is `complete one milestone task`), with the task's `##` heading text as the body. Step 2b already holds that heading verbatim as `<TASK_NAME>` for the agent prompt, so the subject can be built from it without any new lookup.

### Shared commit procedure

`core/shared/commit-procedure.md` takes PATHS, SUBJECT, and an optional BODY, and composes nothing itself: a caller supplying no BODY gets a subject-only commit. Its step 1 guard checks PATHS with `git status --porcelain`, which the orchestrator cannot use as-is because it stages nothing itself and knows the agent's paths only through the staged index; that is why the orchestrator carries its own `git diff --cached --quiet` guard and its own `git commit` line.

### Docs that describe these commits

Three sentences describe the two commits: `docs/skill-reference.md` line 81 (`complete-all-tasks` entry: `Tasklist-completion:` subject with the heading in the body) and line 85 (`complete-task` entry: `Task-completion:` subject); `docs/workflow.md` line 164 (`## How skills commit`, listing `Task-completion:` among the example markers and stating that `/complete-all-tasks` commits once per task, without naming its subject). `core/skills/ask-in-milestone-context/SKILL.md` line 54 states that the task-to-commit mapping is best-effort and "not keyed on the heading in the subject line", a claim that becomes false once every completion subject carries the heading. `CLAUDE.md` line 95 names the orchestrator's per-task commit and its nothing-staged guard but no subject. `README.md`, `CHANGELOG.md`, and `docs/ways-of-using-cairn.md` name neither subject.

### Built host trees

`hosts/claude/` and `hosts/antigravity/` each hold a rendered copy of both SKILL.md files, byte-identical to `core/` apart from the `{{PLUGIN_ROOT}}` substitution; the four rendered files are the only `hosts/` files mentioning either subject. `uv run scripts/build_hosts.py --check` passes at HEAD (version 1.7.0), so the rebuild after the `core/` edit is the whole `hosts/` change.

### Existing history

`git log` holds 218 commits under `Tasklist-completion: complete one milestone task` (heading in the body) and 3 under `Task-completion: <heading>`. No skill or script reads either marker: `capture-milestone-principle-updates` greps only the three answer markers, and `/release-plugin` greps `Milestone-finish:` and `Principle-capture:`. The release skill's fallback for a range with no finished milestone reads commit bodies "where a subject is not self-explanatory", which is the only consumer that benefits from the heading moving into the subject. Milestone ledgers 14, 15, 16, 18, 25, and 29 quote the old `Tasklist-completion:` behaviour as a record of their time and are not runtime or docs files.

## Decisions

### Orchestrator commit mechanics

`/complete-all-tasks` keeps committing the agent-staged index itself in step 2c, behind its own `git diff --cached --quiet` nothing-staged guard and its own `git commit` with no pathspec; it is not routed through `core/shared/commit-procedure.md`, whose PATHS-first contract stays unchanged, and the `complete-task` agent's return contract stays unchanged. The only changes to step 2c are the subject, which becomes `Task-completion: <TASK_NAME>` built from the heading step 2b already holds, and the removal of the `-m "<body>"` argument and the heading-in-body sentence, so the orchestrator commits subject-only.

### Ask-in-context git-history claim

The step 2 sentence of `core/skills/ask-in-milestone-context/SKILL.md` that calls the task-to-commit mapping "not keyed on the heading in the subject line" is rewritten as a marker-agnostic heading search: completion commits carry the task heading, so searching commit subjects and bodies for the heading text usually finds the commit, while the mapping stays best-effort and the fall-back to the live files and the "never the sole source" rule are kept. The sentence names neither the `Task-completion:` nor the retired `Tasklist-completion:` marker and describes no era of history.

### Workflow doc subject wording

In the `## How skills commit` paragraph of `docs/workflow.md`, the clause "`/complete-all-tasks` commits once per task" is extended to name its subject, `Task-completion: <task heading>` with no body, the same subject inline `/complete-task` uses, so the orchestrator is no longer the one batch skill in that paragraph whose subject goes unnamed.

## Out of Scope

