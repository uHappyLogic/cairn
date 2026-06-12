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
