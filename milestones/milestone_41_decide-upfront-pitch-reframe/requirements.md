# Milestone 41: Decide-upfront pitch reframe

## Goal

Reframe Cairn's public pitch around one identity: Cairn is the framework that brings all the important questions up to be decided upfront, so you can hand long-running execution to agents confidently. This replaces the milestone-driven identity on every surface that describes Cairn: the root README's first screen (tagline, one-liner, loop diagram) and `## Why Cairn?`, the three host README templates, the plugin and marketplace manifest descriptions, `CLAUDE.md`'s opening description, and the four GitHub repository descriptions. The claim is stated at full strength as the guiding principle later milestones work toward, with milestones presented as the mechanism and work-type neutrality as a supporting point.

## Relevant starting state

### Root README first screen

`README.md` opens with a three-badge row and a centered four-row adoption table, then `# Cairn`, the bold tagline "Mark the path from idea to shipped.", and the one-liner "Milestone-driven development for your coding agent — any kind of work, one milestone at a time." Directly below is one mermaid loop diagram, `define → review → provide alternatives → recommend → answer → derive → complete`, with a dashed `answer → review` return edge labelled "until no open questions remain". Its seven nodes sit in three colour classes (`init`, `req`, `auto`) and it gives the question loop and execution equal visual weight; `## Installation` follows.

### Root README `## Why Cairn?` and the sections below it

`## Why Cairn?` is three paragraphs: the predictable failures of large projects (goal drift, piled-up ambiguities, unbounded task lists, no line between working and done), Cairn as "a structured, repeatable process" run one milestone at a time, and work-type neutrality through the environment context in `CLAUDE.md`. Open questions appear only as one step in the second paragraph's list, and neither long-running nor unattended execution is mentioned. `## Design principles` then presents claims 11, 2, and 5 as verbatim claim lines linked to `docs/design-claims.md`, and `## How it works` describes the four milestone files and links the three other docs pages.

### Host README templates

`scripts/hosts/claude/README.md`, `scripts/hosts/antigravity/README.md`, and `scripts/hosts/codex/README.md` each carry a two-badge strip, `# Cairn for <Host>`, and the root one-liner verbatim, followed by a distribution paragraph, the generated-file note, and that host's installation section. They hold no tagline, no diagram, and no "Why Cairn?" text. The build renders each into `hosts/<host>/README.md`, and a release publishes that tree into `uHappyLogic/cairn-<host>`.

### Manifest descriptions

The three plugin manifests (`scripts/hosts/claude/.claude-plugin/plugin.json`, `scripts/hosts/antigravity/plugin.json`, `scripts/hosts/codex/plugins/cairn/.codex-plugin/plugin.json`) share one description string: "Milestone-driven development workflow — discuss goals, define milestones, derive and complete tasks, and archive milestones". Two marketplace files carry a second string, "Milestone-driven development for any stack.": the hand-kept root `.claude-plugin/marketplace.json` and the template `scripts/hosts/claude/.claude-plugin/marketplace.json`. The Codex marketplace template `scripts/hosts/codex/.agents/plugins/marketplace.json` has no description field. The build's 25-word description cap applies to skill and agent frontmatter only, not to these strings, and `scripts/set_version.py` writes only the version in the root marketplace file.

### `CLAUDE.md` opening description

`## What this repo is` begins "A plugin (`cairn`) for Claude Code, Antigravity, and Codex that provides a milestone-driven development workflow." and continues with what the plugin ships and the idea-to-archival arc. `AGENTS.md` is a symlink to this file. The `## Milestone Workflow` section at the end of the file ("This project uses the milestone-driven workflow.") is the block the bootstrap skill writes into every user project from its template in `core/skills/init-milestone-base-workflow/SKILL.md`; it is runtime wording, not a pitch surface.

### GitHub repository descriptions

The four descriptions are set by hand through `gh` and live in no tracked file. `uHappyLogic/cairn` reads "Milestone-driven development workflow for Claude Code and Google Antigravity.", which predates the Codex host, and its fourteen topics include `milestones`, `project-management`, and `workflow` but none for Codex. The three distribution repositories share the pattern "Distribution of the Cairn plugin for <host>, published verbatim by each release of uHappyLogic/cairn. Report issues there.", which names no identity; that string is also the `--description` argument of the `gh repo create` command the release skill prints for a missing repository (`.claude/skills/release-plugin/SKILL.md`).

### Design claims the new identity rests on

`docs/design-claims.md` already states both halves of the new pitch as claims, each with a design and a metric: claim 1, "Cairn finds the open questions before the work starts.", and claim 14, "Unattended batch runs are possible." Neither is among the three claims the README's `## Design principles` block surfaces. The page records that only claim 11's test is run by the repository's suite, so no measurement backs "all the important questions"; milestone 38's paired re-run of the alternatives rules fell short of its margin and was recorded as unverified.

### Other pages that describe Cairn

`docs/workflow.md`, `docs/skill-reference.md`, and `docs/ways-of-using-cairn.md` open with intros that describe the page, not the product, and carry no pitch sentence. `docs/ways-of-using-cairn.md` holds the headless command chains that are the concrete form of handing execution to agents. `CONTRIBUTING.md` and the issue forms carry no product description.

### How a change reaches users

Edits under `scripts/hosts/` require `uv run scripts/build_hosts.py` and a commit of the rebuilt `hosts/` trees so that `--check` passes. The rendered manifests and host READMEs reach the distribution repositories and installed plugins only with the next `/release-plugin` run; the latest release is 1.8.0. The root README and the GitHub repository descriptions take effect as soon as they are pushed or set.

## Decisions

### Identity one-liner

The one-liner is a declarative sentence with Cairn as its subject, naming no category noun, that states only the decide-upfront identity and adds no tail: "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently." It is used verbatim under the title of the root README and of all three host README templates. Milestones and work-type neutrality leave the first line and are carried by the diagram and `## Why Cairn?`.

### Product noun

The pitch surfaces adopt no category noun for Cairn. Each pitch sentence makes Cairn the subject of what it does. "Plugin" stays only as a plain fact in installation and distribution text; "framework" and "workflow" are not used as identity nouns.

### README tagline

The bold line "Mark the path from idea to shipped." is replaced, in the same place, by a new tagline that keeps the cairn trail-marker image and points it at the decide-upfront identity: the path is marked before the walk, so the walk can be handed off. The one-liner stays below it as the plain statement, and the two are worded together so they do not say the same thing twice.

### Claim strength disclosure

The short surfaces state the claim as plain present-tense fact with no qualifier: the one-liner, tagline, host README templates, manifest descriptions, the `CLAUDE.md` opening, and the GitHub repository descriptions. The root README's `## Why Cairn?` section says once, in plain words, that bringing up all the important questions is the principle Cairn is built toward and that later milestones work toward it; it may also say that the claim is not yet measured.

## Out of Scope

