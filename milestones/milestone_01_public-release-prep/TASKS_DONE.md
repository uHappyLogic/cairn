# TASKS DONE

## Establish Grep-able Pointer Line and Shared Snippet

This task establishes the new current-milestone pointer contract that the rest of the pointer refactor depends on. It converts the `## Current Milestone` section in `milestones/README.md` from its current prose form to a single grep-able sentinel line pointing at the correct active directory, and creates `shared/get-current-milestone.md` as the single source of truth for how all readers resolve `<MILESTONE_DIR>`.

**Provides:**
- The grep-able pointer line contract in `milestones/README.md`: a single line under the `## Current Milestone` heading with the fixed prefix `Current milestone:` followed by a backticked path (e.g. `Current milestone: \`milestones/milestone_01_public-release-prep/\``) when active, or the literal line `Current milestone: none` when inactive.
- `shared/get-current-milestone.md` — the shared snippet (referenced via `${CLAUDE_PLUGIN_ROOT}`) that is the single source of truth for reading the pointer: grep `milestones/README.md` for the unique `Current milestone:` prefix, extract the backticked span as `<MILESTONE_DIR>`, and treat the token `none` in that position as "no active milestone."

**Notes:**
- The active directory on disk is `milestones/milestone_01_public-release-prep/` (zero-padded two-digit number). The current prose line in `milestones/README.md` references `milestone_1_public-release-prep/` without padding; the converted line must use the corrected padded path.
- This task owns only the `## Current Milestone` section of `milestones/README.md` and the new `shared/get-current-milestone.md`. Do not modify any reader skills/agents, writer skills, or `CLAUDE.md` — those are later tasks that depend on this foundation.
- No human-readable title goes into the machine line itself — titles live in the `## Current Milestone` heading and the Completed Milestones table, per the "Grep-able pointer line format" decision in `requirements.md`.

**Success:**
- `milestones/README.md` contains exactly one line matching the prefix `Current milestone:`, and that line reads `Current milestone: \`milestones/milestone_01_public-release-prep/\``.
- `shared/get-current-milestone.md` exists and unambiguously specifies: (a) match the `Current milestone:` prefix in `milestones/README.md`, (b) extract the backticked span as `<MILESTONE_DIR>`, (c) treat the token `none` in that position as "no active milestone."
- No reader skills/agents, no writer skills, and no `CLAUDE.md` have been modified.

---

## Migrate All Pointer Readers to Shared Snippet

Refactor every skill/agent that currently resolves `<MILESTONE_DIR>` by parsing `CLAUDE.md`'s `## Current Milestone` section to instead resolve it through `shared/get-current-milestone.md` (created by "Establish Grep-able Pointer Line and Shared Snippet"), referenced via `${CLAUDE_PLUGIN_ROOT}`. After this task, no reader parses `CLAUDE.md` for the pointer; each carries a one-line reference to the shared snippet as the single source of truth.

**Notes:**
- The full reader list (per requirements.md "Current-milestone pointer (source of truth)"): `agents/submit-backlog-task.md`, `shared/implement-procedure.md`, and the skills `answer-open-question`, `discuss-new-backlog-task`, `discuss-open-question`, `highlight-milestone-requirements-open-questions`, `implement-backlog-tasks`, `populate-backlog`, `submit-backlog-task`.
- The `implement-backlog-task` skill resolves the pointer transitively via `shared/implement-procedure.md` — once that shared file is updated, the skill is covered without a direct edit. Verify this is the case; do not double-edit the skill.
- Do not modify `define-milestone-goal` (its milestone-number reading is owned by a separate task), and do not touch writer skills (`finish-current-milestone`, `goto-next-milestone`, `init-milestone-base-workflow`) or `CLAUDE.md`.
- This task depends on "Establish Grep-able Pointer Line and Shared Snippet" being completed first; `shared/get-current-milestone.md` must already exist.

**Success:**
- Every file in the reader list (`agents/submit-backlog-task.md`, `shared/implement-procedure.md`, and the seven named skills) references `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`.
- None of those files contain logic that reads or parses `CLAUDE.md`'s `## Current Milestone` section for the pointer.
- `skills/implement-backlog-task/SKILL.md` is not directly modified (it is covered via the shared procedure).
- Writer skills and `define-milestone-goal` are unmodified.

---

## Migrate Pointer Writers Off CLAUDE.md

Refactor the three writer skills (`finish-current-milestone`, `goto-next-milestone`, `init-milestone-base-workflow`) so they update the current-milestone pointer by overwriting the single grep-able `Current milestone:` line in `milestones/README.md` only — no longer writing any pointer into `CLAUDE.md`. This makes `milestones/README.md` the sole source of truth for the pointer, as decided in requirements.md "CLAUDE.md pointer role." The existing `## Current Milestone` section in `CLAUDE.md` must not be removed or modified here; that cleanup belongs to a later task.

**Notes:**
- `goto-next-milestone` currently reads the "none" state from `CLAUDE.md`'s `## Current Milestone` section. After this task it reads the grep-able `Current milestone:` line from `milestones/README.md`; the gate passes when that line equals the literal `Current milestone: none` (bare token, no backticks — per the pointer line format in requirements.md "Grep-able pointer line format").
- `init-milestone-base-workflow`'s idempotency short-circuit currently requires `milestones/`, `milestones/README.md`, and a `## Current Milestone` section in `CLAUDE.md`. After this task the CLAUDE.md condition is dropped — presence of the grep-able `Current milestone:` line in `milestones/README.md` (alongside `milestones/`) is sufficient to declare the project already initialized.

**Success:**
- `skills/finish-current-milestone/SKILL.md` contains no instruction to write to `CLAUDE.md`'s pointer section; it writes the literal line `Current milestone: none` into `milestones/README.md` only.
- `skills/goto-next-milestone/SKILL.md` contains no instruction to write to `CLAUDE.md`'s pointer section; it writes `Current milestone: \`<path>\`` into `milestones/README.md` only, and its "none" gate reads the grep-able `Current milestone:` line from `milestones/README.md`.
- `skills/init-milestone-base-workflow/SKILL.md` seeds `Current milestone: none` in `milestones/README.md` when creating the file, does not write a pointer into `CLAUDE.md`, and its idempotency check no longer requires `CLAUDE.md` to have a `## Current Milestone` section.
- `CLAUDE.md` is unmodified by this task.
- No skills or agents outside the three named writers are modified.

---
