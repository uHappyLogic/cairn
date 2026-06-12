# TASKS TODO



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

## Add Marketplace Manifest

Creates `.claude-plugin/marketplace.json` so the repo is installable as its own single-plugin Claude Code marketplace via `/plugin marketplace add uHappyLogic/cairn`. No marketplace manifest exists today; this is a from-scratch addition that lives side by side with the existing `.claude-plugin/plugin.json` (the recommended single-plugin convention), per requirements.md "Marketplace manifest path and shape."

**Notes:**
- This task must run after "Rename Plugin to Cairn in Manifest and CLAUDE.md" — the plugin entry `name` in `marketplace.json` must equal `cairn`, and that name is established by the rename task. Verify the `name` field in `.claude-plugin/plugin.json` is `"cairn"` before writing the manifest.

**Success:**
- `.claude-plugin/marketplace.json` exists with the exact shape: top-level `name` of `"cairn"` (kebab-case), `owner.name` of `"Lukasz Kosiak"`, and a single `plugins` array entry with `name: "cairn"`, `source: "."`, and `description: "Milestone-driven development for any stack."`.
- The `name` value in the `plugins` entry matches the `name` field in `.claude-plugin/plugin.json`.
- No files other than `.claude-plugin/marketplace.json` are modified by this task.

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
