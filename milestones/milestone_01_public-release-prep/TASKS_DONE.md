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

## Remove CLAUDE.md Pointer Section and Sync Invariant

Remove the `## Current Milestone` section from `CLAUDE.md` entirely, drop the "keep `CLAUDE.md` and `milestones/README.md` in sync" invariant, update all remaining "source of truth" and pointer-dependency language in `CLAUDE.md` to name only `milestones/README.md`, and correct the header prose in `milestones/README.md` to the same effect. This is the final documentation cleanup that makes `milestones/README.md` the sole source of truth for the pointer, valid only after all readers and writers have been migrated off `CLAUDE.md` by the preceding tasks.

**Notes:**
- The `## Milestone Workflow` guidance block in `CLAUDE.md` (seeded by `init-milestone-base-workflow`) must stay intact — only the sentence within it that names `CLAUDE.md` as a pointer source of truth needs to be corrected; do not remove the block.
- In `milestones/README.md`, only the header prose (the "source of truth" sentence near the top) is in scope. The `## Current Milestone` heading and its machine pointer line (established by "Establish Grep-able Pointer Line and Shared Snippet") must not be modified.
- Multiple spots in `CLAUDE.md` carry pointer-dependency language beyond the single obvious invariant bullet: the skill pipeline descriptions for `init-milestone-base-workflow`, `finish-current-milestone`, and `goto-next-milestone`; the "Milestone file structure" section's source-of-truth sentence; the `init-milestone-base-workflow` invariant bullet; and the invariant asserting the `submit-backlog-task` agent and shared implement procedure read `CLAUDE.md`. All must be updated.

**Success:**
- `grep "## Current Milestone" CLAUDE.md` returns no results — the section heading and all content beneath it are gone.
- `CLAUDE.md` contains no invariant bullet or prose asserting that `CLAUDE.md` and `milestones/README.md` must be kept in sync, or that `CLAUDE.md` is a source of truth for the current-milestone pointer.
- All "source of truth for which milestone is current" language remaining in `CLAUDE.md` names only `milestones/README.md`.
- The header prose in `milestones/README.md` no longer names `CLAUDE.md` as a source of truth for the pointer and no longer instructs keeping both files in sync.
- The `## Current Milestone` heading and its machine pointer line in `milestones/README.md` are unchanged from before this task ran.

---

## Rename Plugin to Cairn in Manifest and CLAUDE.md

Update the plugin's proper name from `workflow` to `cairn` in `.claude-plugin/plugin.json` (the `name` field) and in the one `CLAUDE.md` sentence that identifies the plugin by its backticked proper name. This is the foundation of the Cairn rename (requirements.md "Plugin name and tagline") for the files in scope — the README rewrite and `.claude-plugin/marketplace.json` creation are handled by separate tasks.

**Notes:**
- The only proper-name instance in `CLAUDE.md` is the opening sentence: `A Claude Code plugin (\`workflow\`) that implements a milestone-driven development workflow.` The backticked `workflow` is the plugin name; the trailing "milestone-driven development workflow" is the generic concept and must not change.
- All other appearances of the word "workflow" in `CLAUDE.md` — the `## Milestone Workflow` heading, "the milestone-driven workflow", skill names like `init-milestone-base-workflow` — are either the generic concept or skill-directory identifiers, not the plugin's proper name. Leave them untouched.

**Success:**
- `.claude-plugin/plugin.json` `name` field equals `"cairn"`.
- `CLAUDE.md` no longer contains the string `` plugin (`workflow`) ``; the opening description reads `` A Claude Code plugin (`cairn`) ``.
- The `## Milestone Workflow` heading, the phrase "milestone-driven development workflow", and all skill/directory names containing `workflow` in `CLAUDE.md` are unchanged.
- No files other than `.claude-plugin/plugin.json` and `CLAUDE.md` are modified by this task.

---

## Add MIT License File

Add a `LICENSE` file at the repo root containing the canonical MIT License text. No license file exists anywhere in the repo today; this is a from-scratch addition. The file establishes the legal basis for public release.

**Success:**
- `LICENSE` exists at the repo root.
- The file contains the standard MIT License text with the copyright line exactly `Copyright (c) 2026 Lukasz Kosiak`.
- No other files are modified by this task.

---

## Adopt Zero-Padded Two-Digit Milestone Numbering

Update `define-milestone-goal` to derive the next milestone number by scanning `milestones/` for `milestone_<NN>_*` directories — parsing each directory's numeric portion as an integer (stripping leading zeros), taking `max(N) + 1`, and formatting the result zero-padded to two digits — rather than reading the number from `CLAUDE.md`. The milestone directory it creates must use this zero-padded two-digit name. Any other location in the repo that parses a milestone number from a path slug must also strip leading zeros when interpreting it.

**Notes:**
- When `milestones/` contains no `milestone_<NN>_*` directories (cold start), treat `max(N)` as `0` so the first number is `1`, formatted `01`.
- The live directory on disk is already `milestones/milestone_01_public-release-prep/` (zero-padded), so no directory rename is needed — only the skill logic must match the convention.
- `goto-next-milestone` scans `milestones/` for a defined-but-not-yet-active directory; verify whether it derives a milestone number from a slug and, if so, ensure it strips leading zeros.

**Success:**
- `skills/define-milestone-goal/SKILL.md` contains no instruction to read a milestone number from `CLAUDE.md` or from `milestones/README.md`'s pointer.
- `skills/define-milestone-goal/SKILL.md` derives the next number by scanning `milestones/` for `milestone_<NN>_*` directories, parsing each numeric portion as a leading-zero-stripped integer, taking `max + 1`, and formatting the result zero-padded to two digits (e.g. `01`, `02`, …, `10`).
- The directory name `define-milestone-goal` creates follows `milestone_<NN>_<slug>/` with a two-digit zero-padded number.
- No file in the repo that parses a milestone number from a path slug treats leading zeros as significant (i.e. `01` is parsed as integer `1`, not skipped or misread).

---

## Add Marketplace Manifest

Creates `.claude-plugin/marketplace.json` so the repo is installable as its own single-plugin Claude Code marketplace via `/plugin marketplace add uHappyLogic/cairn`. No marketplace manifest exists today; this is a from-scratch addition that lives side by side with the existing `.claude-plugin/plugin.json` (the recommended single-plugin convention), per requirements.md "Marketplace manifest path and shape."

**Notes:**
- This task must run after "Rename Plugin to Cairn in Manifest and CLAUDE.md" — the plugin entry `name` in `marketplace.json` must equal `cairn`, and that name is established by the rename task. Verify the `name` field in `.claude-plugin/plugin.json` is `"cairn"` before writing the manifest.

**Success:**
- `.claude-plugin/marketplace.json` exists with the exact shape: top-level `name` of `"cairn"` (kebab-case), `owner.name` of `"Lukasz Kosiak"`, and a single `plugins` array entry with `name: "cairn"`, `source: "."`, and `description: "Milestone-driven development for any stack."`.
- The `name` value in the `plugins` entry matches the `name` field in `.claude-plugin/plugin.json`.
- No files other than `.claude-plugin/marketplace.json` are modified by this task.

---

## Replace Pipeline Diagram with Mermaid Flowchart

Replace the plain-text fenced block in README.md's "Workflow pipeline" section (currently lines ~40–68) with an equivalent `mermaid` fenced flowchart. The diagram must cover the full skill sequence from `init-milestone-base-workflow` through `goto-next-milestone`, and must represent the open-questions trio (`highlight-milestone-requirements-open-questions` → `discuss-open-question` → `answer-open-question`) as an actual cycle with a back-edge, not a static box.

**Notes:**
- The current block opens with a bare ` ``` ` fence (no language tag) at approximately line 42. Replacing it requires changing the opening fence to ` ```mermaid ` and rewriting the contents as a valid Mermaid flowchart.
- `discuss-open-question` is labeled "(optional)" in the ASCII art; preserve that intent in the Mermaid graph (e.g. via a label on the edge or a note in the node label).
- The back-edge must point from the end of the loop (`answer-open-question`) back to `highlight-milestone-requirements-open-questions` so the cycle is explicit rather than implied by a surrounding box.
- The prose paragraph immediately after the closing fence (line ~70: "Run `highlight-milestone-requirements-open-questions` as many times…") stays unchanged.

**Success:**
- README.md's "Workflow pipeline" section contains a ` ```mermaid ` fenced block (not a bare ` ``` ` fence).
- The Mermaid block includes all twelve steps: `init-milestone-base-workflow`, `/init`, `discuss-milestone-goal`, `define-milestone-goal`, `specify-milestone-starting-implementation-state`, `highlight-milestone-requirements-open-questions`, `discuss-open-question`, `answer-open-question`, `populate-backlog`, `implement-backlog-tasks`, `finish-current-milestone`, `goto-next-milestone`.
- The block contains a back-edge from `answer-open-question` (or equivalent loop-end node) pointing back to `highlight-milestone-requirements-open-questions`.
- No other section of README.md is modified.

---

## Rewrite README for Public Adoption

Replace `README.md` with a complete, freshly authored adoption-focused rewrite that serves as both the landing page and the user manual. The current file is maintainer/developer-facing with no installation section, no "why use this" framing, and no marketplace-add instructions; this task makes it a public-facing document. The rewrite splits existing content by audience — carrying forward the condensed pipeline overview and skill reference, and dropping the maintainer-only content that already lives in `CLAUDE.md`.

**Notes:**
- This is a full rewrite, not a patch. The existing content is split by audience: adoption-relevant content (pipeline overview, skill reference) is condensed and carried forward; maintainer-only content (deep file-structure docs, altitude/invariant rules from `CLAUDE.md`'s Invariants section) is dropped entirely and must NOT be relocated.
- The self-dogfooding setup (the repo runs its own workflow on itself — `milestones/` and the active milestone directory are live workflow artifacts) must remain visible as a credibility showcase.
- By the time this task runs, `.claude-plugin/plugin.json` already carries `name: "cairn"` and `.claude-plugin/marketplace.json` already exists — so the install command and naming are consistent and can be referenced directly.
- No `CONTRIBUTING.md` and no `docs/` directory are created; the milestone produces exactly one public README.

**Success:**
- `README.md` opens with `# Cairn`, followed by the tagline **"Mark the path from idea to shipped."** and the subtitle **"Milestone-driven development for any stack."**
- `README.md` contains an installation section whose install command is `/plugin marketplace add uHappyLogic/cairn`.
- `README.md` contains a "what problem this solves / why use it" section aimed at a first-time visitor.
- `README.md` contains a condensed pipeline overview (the ordered skill sequence from bootstrap through milestone archival).
- `README.md` contains a skill reference section.
- `README.md` contains no deep file-structure documentation (no table or prose describing the `.claude-plugin/`, `skills/`, `agents/`, `shared/` layout as a maintainer reference) and no altitude/invariant rules.
- No `CONTRIBUTING.md` file exists in the repo after this task runs.
- No `docs/` directory exists in the repo after this task runs.
- No files other than `README.md` are modified by this task.

---
