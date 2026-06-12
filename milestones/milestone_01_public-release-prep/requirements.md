# Milestone 1: Public Release Preparation

## Goal

Prepare the plugin for public release on GitHub: rename it to a tech-stack-agnostic name, move the current-milestone source of truth out of CLAUDE.md into a grep-able line in milestones/README.md read through a shared snippet (updating all skills/agents that touch the pointer), add an MIT license and a public adoption-focused README, and make the repo installable as its own single-plugin Claude Code marketplace — while keeping the self-dogfooding setup visible as a credibility showcase.

## Relevant implementation state

### Plugin identity and manifest

The plugin is named `workflow` in `.claude-plugin/plugin.json` (version `1.0.0`, author Lukasz Kosiak). That manifest is the only file under `.claude-plugin/`. The name `workflow` also appears in user-facing prose — `README.md`'s title is "Workflow Claude Plugin" and `CLAUDE.md` calls the repo "A Claude Code plugin (`workflow`)". A rename to a tech-stack-agnostic name must touch the manifest `name` field plus these prose references.

### Current-milestone pointer (source of truth)

The "which milestone is current" pointer is duplicated in two files and read directly out of `CLAUDE.md` by most skills. `CLAUDE.md` and `milestones/README.md` each carry a `## Current Milestone` section; the milestone path appears in backticks. Both must agree, and an invariant in `CLAUDE.md` requires them to stay in sync.

- **Readers** (extract `<MILESTONE_DIR>` from `CLAUDE.md`'s `## Current Milestone` section): `agents/submit-backlog-task.md`, `shared/implement-procedure.md`, and the skills `answer-open-question`, `discuss-new-backlog-task`, `discuss-open-question`, `highlight-milestone-requirements-open-questions`, `implement-backlog-tasks`, `populate-backlog`, `submit-backlog-task`. The `implement-backlog-task` skill resolves it via the shared procedure. `define-milestone-goal` reads the milestone *number* from both `CLAUDE.md` and `milestones/README.md`.
- **Writers** (update the `## Current Milestone` section in *both* files): `finish-current-milestone` (clears to "none"), `goto-next-milestone` (points to next), `init-milestone-base-workflow` (seeds "none yet" placeholder).

The current format is prose ("**Milestone 1 — …** (`path`)"), parsed by reading the section and extracting the backticked path — not a single grep-able line. Moving the source of truth into a grep-able line in `milestones/README.md` and routing all readers through a shared snippet touches every file listed above.

### Skill/agent layout

Skills live one-per-directory under `skills/<name>/SKILL.md` (14 skills). Two subagents live in `agents/` (`implement-backlog-task.md`, `submit-backlog-task.md`). The shared implement procedure is `shared/implement-procedure.md`, referenced via `${CLAUDE_PLUGIN_ROOT}`. A new `/get-current-milestone` skill would be a new `skills/get-current-milestone/SKILL.md` directory; no such skill exists today.

### README and public-facing docs

`README.md` exists and is thorough but developer/maintainer-facing: it documents the workflow pipeline, skill reference, and file structure. It is not adoption-focused — there is no installation section, no marketplace-add instructions, and no "what problem this solves / why use it" framing for a new user. The README's framing also assumes the reader is editing the plugin rather than installing it.

### License

No `LICENSE` file exists anywhere in the repo. Adding MIT licensing is a from-scratch addition (license file plus, optionally, a manifest/README reference).

### Marketplace installability

There is no `marketplace.json` (Claude Code marketplace manifest) anywhere in the repo — only the plugin manifest `.claude-plugin/plugin.json`. The repo is therefore not yet installable as its own single-plugin marketplace; making it so requires adding the marketplace manifest that lists this plugin. This is a gap, not a modification.

### Self-dogfooding setup

The repo runs its own workflow on itself: `milestones/` with `milestones/README.md`, the active `milestones/milestone_1_public-release-prep/` directory, and the `## Current Milestone` pointer in `CLAUDE.md` are all live workflow artifacts produced by the plugin's own skills. `.claude/settings.json` enables only the external `skill-creator` plugin (the workflow plugin's skills are invoked from the repo directly, not via an enabled-plugins entry). Any rename or pointer-format change must keep these dogfooding artifacts working, since they double as the public credibility showcase.

## Implementation decisions

### MIT license copyright line

The MIT `LICENSE` file carries the copyright line **`Copyright (c) 2026 Lukasz Kosiak`** — the manifest author and the current year. Any manifest/README license reference uses the same holder.

### Grep-able pointer line format

The current-milestone pointer in `milestones/README.md` is a **single line with a fixed prefix sentinel and a backticked path**, sitting under the `## Current Milestone` heading:

```
Current milestone: `milestones/milestone_<N>_<slug>/`
```

The inactive/finished state is the literal line `Current milestone: none`.

- The shared snippet matches the line by its unique `Current milestone:` prefix, takes the **backticked span** as `<MILESTONE_DIR>`, and treats `none` as "no active milestone" — the state `goto-next-milestone` checks for.
- **Writers** (`finish-current-milestone`, `goto-next-milestone`, `init-milestone-base-workflow`) overwrite the whole line, so the `none`↔path swap is a one-line change in a single file.
- The `## Current Milestone` heading is kept for document structure. **No human-readable title is mixed into the machine line** — titles live in the heading and the Completed Milestones table. (Folding free-text title into the matched line is exactly what made the current prose format un-grep-able.)

### Current-milestone pointer read mechanism

Readers resolve `<MILESTONE_DIR>` through a shared snippet (e.g. `shared/get-current-milestone.md`) referenced via `${CLAUDE_PLUGIN_ROOT}`, following the existing `shared/implement-procedure.md` pattern. That snippet is the single source of truth for the grep-able-line read logic; each reader carries a one-line instruction pointing at it rather than restating the read. **No `/get-current-milestone` skill is added** — inline skills cannot return a value to a caller, so a skill would add indirection without real encapsulation, whereas the shared snippet gives a genuine single source of truth at one line per reader.

### CLAUDE.md pointer role

The current-milestone pointer is **removed from `CLAUDE.md` entirely** — `milestones/README.md` becomes the sole source of truth. The workflow holds no opinion about `CLAUDE.md`: it neither reads nor writes a pointer there, and maintains no `## Current Milestone` section (live or stub) in it.

- Every skill/agent that currently reads or writes the pointer is refactored to depend on the `milestones/README.md` pointer instead. **Readers** resolve `<MILESTONE_DIR>` via the shared snippet against `milestones/README.md`. **Writers** (`finish-current-milestone`, `goto-next-milestone`, `init-milestone-base-workflow`) update only `milestones/README.md` — touching one file, not two.
- The "keep `CLAUDE.md` and `milestones/README.md` in sync" invariant is **dropped**, not rewritten.
- A repo may keep its own `CLAUDE.md` content freely, but no skill or agent depends on it. (The separate `## Milestone Workflow` guidance block that `init-milestone-base-workflow` seeds is documentation, not a pointer dependency, and is untouched by this decision.)

### Milestone number derivation

The grep-able pointer line carries **only the milestone path** — no explicit number field. The milestone number is re-derived from the path slug (`milestone_<NN>_<slug>`), never stored twice. Directories use a **zero-padded two-digit number** (`milestone_01_<slug>`, `milestone_02_<slug>`, …) so listings sort lexically past 9 milestones. `define-milestone-goal` determines the next number by scanning `milestones/` for `milestone_<NN>_*` directories, parsing each number as an integer (leading zeros stripped), taking `max(N) + 1`, and re-formatting it zero-padded to two digits; this works identically whether the pointer is active or `none` (finished) and removes any stored "current number" that could drift out of sync. Readers that re-derive the number from a path slug likewise strip leading zeros.

### Plugin name and tagline

The plugin is renamed to **Cairn**. The manifest `name`, repo slug, and install URL all use the single lowercase token `cairn`. The rename propagates into `.claude-plugin/plugin.json`, the marketplace manifest, the README title, and all prose references (replacing `workflow` / "Workflow Claude Plugin").

The public tagline is **"Mark the path from idea to shipped."**, carried with the supporting subtitle **"Milestone-driven development for any stack."** The tagline is benefit-first and echoes the cairn trail-marker metaphor; the stack-agnostic point is demoted to the subtitle rather than headlined.

### GitHub repository and install slug

The GitHub repository changes to match the new plugin name. A new public repo named `cairn` (single lowercase token) is created under the account **uHappyLogic** — there is no existing remote, so this is naming a fresh repo, not renaming one in place. The canonical install slug is **`uHappyLogic/cairn`** (owner written `uHappyLogic`; GitHub resolves it case-insensitively). The README's marketplace-add instructions use `/plugin marketplace add uHappyLogic/cairn`, and any other install URL / `owner/repo` reference in public docs uses the same slug.

### Marketplace manifest path and shape

For a repository that ships exactly one plugin at the repo root, the best-practice layout is followed: the marketplace manifest lives at **`.claude-plugin/marketplace.json`**, side by side with `plugin.json` in the same `.claude-plugin/` directory (the recommended single-plugin convention — both files coexist).

The manifest lists the one plugin with its `source` pointing at the repo root:

```json
{
  "name": "cairn",
  "owner": { "name": "Lukasz Kosiak" },
  "plugins": [
    {
      "name": "cairn",
      "source": ".",
      "description": "Milestone-driven development for any stack."
    }
  ]
}
```

- Required fields only, per the current Claude Code marketplace schema: top-level `name` (kebab-case) and `owner.name`, plus a `plugins` array whose single entry carries `name` and `source`. A plugin `description` is included for the marketplace listing.
- The plugin entry's `source` is the literal `"."` — the plugin root is the repo root (where `.claude-plugin/plugin.json` sits), so no subdirectory path is needed.
- The plugin `name` (`cairn`) matches `.claude-plugin/plugin.json`'s `name`; `owner.name` matches the manifest author (`Lukasz Kosiak`). Install remains `/plugin marketplace add uHappyLogic/cairn`.

### README content disposition

The adoption-focused README is a **complete rewrite** (authored fresh, not patched), but **not a pure replacement**. The existing content is split by audience:

- **Carried forward into the new README, condensed:** the pipeline overview and the skill reference. These are adoption material — a new user's "how do I use this" — so they belong on the public landing page.
- **Dropped from the README:** the genuinely maintainer-only content (deep file-structure docs, altitude/invariant rules). This already lives in `CLAUDE.md` and stays there; it is not relocated.

No `CONTRIBUTING.md` and no `docs/` directory are created. The milestone produces **one** public README that serves as both landing page and user manual, replacing the maintainer-internals framing of the current file.

## Out of Scope

