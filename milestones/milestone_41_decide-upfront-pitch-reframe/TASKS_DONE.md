# TASKS DONE

## Replace Root README Tagline And One-Liner

In the root `README.md` title block, replace the bold tagline with "Mark the path first, then hand off the walk." and the line below it with the one-liner "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", so the first screen states the decide-upfront identity as plain fact with no category noun and no tail. Verified when both new lines sit under `# Cairn` in the same two places, each exactly once, and neither "Mark the path from idea to shipped." nor the old milestone-driven one-liner remains in the file.

**Verified:**

- The bold tagline under `# Cairn` in the root `README.md` (line 28, the old tagline's place) reads exactly `**Mark the path first, then hand off the walk.**`.
- The line directly below it (line 29, the old one-liner's place) reads exactly "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", with no category noun and no tail.
- `grep -c` finds each of the two new lines exactly once in `README.md`.
- `grep -c` finds neither "Mark the path from idea to shipped" nor "Milestone-driven development for your coding agent" in `README.md` (zero matches each).
- `git diff -- README.md` shows those two lines as the file's only change (2 insertions, 2 deletions).

---

## Regroup First-Screen Diagram Into Two Subgraphs

Rework the root `README.md` mermaid diagram so define, review, provide alternatives, recommend, and answer sit inside a subgraph titled for deciding upfront and derive and complete sit inside a second subgraph titled for handing execution to agents, with the answer-to-derive edge crossing between them labelled as the handoff and the three colour classes (`init`, `req`, `auto`) reduced to two, one per group. All seven skill-named nodes, the left-to-right layout, and the dashed "until no open questions remain" return edge from answer to review are kept, so the picture shows the new identity instead of giving the question loop and execution equal weight. Verified when the block parses as valid mermaid and shows exactly that structure.

**Verified:**

- The root `README.md` mermaid block, extracted and passed to the mermaid library's `mermaid.parse`, parses without error as a `flowchart-v2` diagram, while a deliberately broken copy of it is rejected with a parse error.
- The parsed diagram's direction is `LR`, and its seven skill-named nodes are `define`, `review`, `provide alternatives`, `recommend`, `answer`, `derive`, and `complete`, with labels unchanged.
- The parsed diagram holds exactly two subgraphs: `upfront`, titled "Decide upfront", containing define, review, alternatives, recommend, and answer; and `agents`, titled "Hand execution to agents", containing derive and complete.
- The `answer -> derive` edge is a solid edge labelled "handoff" and is the only edge between the two subgraphs.
- The `answer -> review` return edge is dotted and labelled "until no open questions remain".
- The remaining edges are the solid chain `define -> review -> alternatives -> recommend -> answer` and `derive -> complete`, seven edges in all.
- The block defines exactly two colour classes, `decide` (the five nodes of the first subgraph) and `execute` (the two nodes of the second); `grep` finds no `classDef init`, `classDef req`, or `classDef auto` in `README.md`.
- `git diff -- README.md` shows changes only inside the mermaid block (lines 34 to 56); the `%%{init}%%` line, `flowchart LR`, and everything outside the block are unchanged.

---

## Rewrite Why Cairn Around Handing Off Execution

Rewrite the three paragraphs of the root README's `## Why Cairn?`: the first opens with the problem of handing off long-running execution (an agent left to run for a long time hits questions nobody decided and either guesses quietly and builds on the guess or stops and waits for a person, so you cannot walk away), the second presents milestones as the mechanism (each milestone first brings its open questions up, has them answered with recorded decisions, and only then derives tasks an agent can complete unattended), and the third keeps work-type neutrality as the supporting point through the environment read from `CLAUDE.md`. The section says once, in plain words, that bringing up all the important questions is the principle Cairn is built toward and that later milestones work toward it, and it adopts no category noun for Cairn ("framework" and "workflow" are not used as identity nouns). Verified when the section is three paragraphs carrying that content and `## How it works` and `## Self-dogfooding` are unchanged word for word.

**Verified:**

- The root `README.md` section `## Why Cairn?` holds exactly three paragraphs (three non-blank lines between its heading and `## Design principles`).
- The first paragraph opens with the problem of handing long-running execution to an agent: an agent left to run for a long time hits questions nobody decided, either guesses quietly and builds on the guess or stops and waits for a person, and so you cannot walk away.
- The second paragraph presents milestones as the mechanism: each milestone first brings its open questions up, has them answered with recorded decisions, and only then derives tasks an agent can complete unattended.
- The third paragraph carries work-type neutrality as the supporting point: skills read the project's environment from `CLAUDE.md`, so the same sequence fits any kind of work.
- The section says exactly once, in plain words, that bringing up all the important questions is the principle Cairn is built toward and that later milestones work toward it (`grep` finds "principle Cairn is built toward" once, in the second paragraph, which also says the claim is not yet a measured result).
- The section adopts no category noun for Cairn: a case-insensitive `grep` for "framework" or "workflow" over the section finds nothing, and every sentence about Cairn makes it the subject of what it does.
- `git diff -- README.md` shows three changed lines, 106, 108, and 110, all inside `## Why Cairn?`; `## How it works`, `## Self-dogfooding`, and everything else in the file are unchanged word for word.

---

## Lead Design Principles With Claims 1 And 14

Change the root README's `## Design principles` block to three bullets in this order: claim 1 ("Cairn finds the open questions before the work starts.") and claim 14 ("Unattended batch runs are possible.") with new glosses, then claim 2 ("Each decision has a record in git.") with its current gloss, removing the claim 11 and claim 5 bullets so the block surfaces the two claims the new pitch rests on. Verified when each bullet's claim line is verbatim and links to its anchor in `docs/design-claims.md`, the closing link to all nineteen claims is unchanged, and `docs/design-claims.md` itself has no diff.

**Verified:**

- The root `README.md` section `## Design principles` holds exactly three bullets, in the order claim 1, claim 14, claim 2.
- The first bullet's claim line reads "Cairn finds the open questions before the work starts." verbatim, matching the `### 1.` heading of `docs/design-claims.md`, and links to `docs/design-claims.md#1-cairn-finds-the-open-questions-before-the-work-starts`; its gloss is new.
- The second bullet's claim line reads "Unattended batch runs are possible." verbatim, matching the `### 14.` heading, and links to `docs/design-claims.md#14-unattended-batch-runs-are-possible`; its gloss is new.
- The third bullet is the claim 2 bullet, "Each decision has a record in git." linked to `docs/design-claims.md#2-each-decision-has-a-record-in-git`, with its gloss unchanged (the line does not appear in `git diff -- README.md`).
- `grep -c` finds neither "The records are machine-readable" nor "Advice gets better with each milestone" in `README.md` (zero matches), so the claim 11 and claim 5 bullets are gone.
- The closing line "All nineteen claims, each with its design and a metric to test it, are in [docs/design-claims.md](docs/design-claims.md)." is unchanged; `git diff -- README.md` shows 2 insertions and 2 deletions, all inside the bullet list.
- `git diff --quiet -- docs/design-claims.md` exits zero: the claims page has no diff.

---

## Carry One-Liner Into Host README Templates

Replace the line under `# Cairn for <Host>` in `scripts/hosts/claude/README.md`, `scripts/hosts/antigravity/README.md`, and `scripts/hosts/codex/README.md` with the root README one-liner verbatim, "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", then run `uv run scripts/build_hosts.py` so the rebuilt `hosts/` trees ride with the templates. Verified when `uv run scripts/build_hosts.py --check` exits zero and each rendered `hosts/<host>/README.md` carries the one-liner under its title with no milestone-driven line left.

**Verified:**

- In each of `scripts/hosts/claude/README.md`, `scripts/hosts/antigravity/README.md`, and `scripts/hosts/codex/README.md`, the line under the `# Cairn for <Host>` title (line 12) reads exactly "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", the same string as the one-liner on line 29 of the root `README.md`.
- `uv run scripts/build_hosts.py` rebuilt `hosts/antigravity/`, `hosts/claude/`, and `hosts/codex/`, and `uv run scripts/build_hosts.py --check` then exits zero.
- Each rendered `hosts/claude/README.md`, `hosts/antigravity/README.md`, and `hosts/codex/README.md` carries the one-liner on line 12, directly under its title on line 10, and `grep -c` finds it exactly once per file.
- A case-insensitive `grep -c` for "milestone-driven" finds zero matches in all three templates and all three rendered READMEs.
- `git diff --stat` shows six changed files, the three templates and their three rendered copies, each with 1 insertion and 1 deletion.

---

## Unify Manifest Descriptions On The One-Liner

Set all five description strings to the README one-liner word for word, "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.": the three plugin manifests (`scripts/hosts/claude/.claude-plugin/plugin.json`, `scripts/hosts/antigravity/plugin.json`, `scripts/hosts/codex/plugins/cairn/.codex-plugin/plugin.json`) and the two Claude marketplace files (the hand-kept root `.claude-plugin/marketplace.json` and the template `scripts/hosts/claude/.claude-plugin/marketplace.json`). This ends the split into a long and a short string and drops the plugin manifests' step list; the `hosts/` trees are rebuilt with `uv run scripts/build_hosts.py` and no release is cut. Verified when `uv run scripts/build_hosts.py --check` exits zero and all five files and their rendered copies carry the one string.

**Verified:**

- The `description` value in each of the five source files (`scripts/hosts/claude/.claude-plugin/plugin.json`, `scripts/hosts/antigravity/plugin.json`, `scripts/hosts/codex/plugins/cairn/.codex-plugin/plugin.json`, the root `.claude-plugin/marketplace.json`, and `scripts/hosts/claude/.claude-plugin/marketplace.json`) reads exactly "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", the same string as the one-liner on line 29 of the root `README.md`.
- `uv run scripts/build_hosts.py` rebuilt `hosts/antigravity/`, `hosts/claude/`, and `hosts/codex/`, and `uv run scripts/build_hosts.py --check` then exits zero.
- The four rendered copies (`hosts/claude/.claude-plugin/plugin.json`, `hosts/claude/.claude-plugin/marketplace.json`, `hosts/antigravity/plugin.json`, `hosts/codex/plugins/cairn/.codex-plugin/plugin.json`) carry the same string as their `description`, so a `grep` for `"description"` over the JSON files under `.claude-plugin`, `scripts/hosts`, and `hosts` finds nine lines holding one value.
- A case-insensitive `grep` for "milestone-driven development" finds no JSON file under `.claude-plugin`, `scripts/hosts`, or `hosts`: both the short string and the plugin manifests' step list are gone.
- The root marketplace file and the four rendered manifests load as valid JSON, and the root marketplace file's `version` is still `1.8.0`: no release was cut.
- `git diff --stat` shows nine changed files, the five sources and their four rendered copies, each with 1 insertion and 1 deletion.

---

## Restate CLAUDE.md Opening Identity Sentence

Reword the first sentence of `## What this repo is` in `CLAUDE.md` so it still names `cairn` as a plugin for Claude Code, Antigravity, and Codex but, in place of "provides a milestone-driven development workflow", states in the editor's own words and plain present tense that it brings a milestone's important questions up to be decided before work starts, so execution can then be handed to agents. The README one-liner is not copied word for word, and milestones stay in the rest of the paragraph as the mechanism. Verified when that sentence is the only change: the `## Milestone Workflow` block at the end of `CLAUDE.md` and everything under `core/skills/init-milestone-base-workflow/` have no diff.

**Verified:**

- The first sentence of `## What this repo is` in `CLAUDE.md` (line 7) reads "A plugin (`cairn`) for Claude Code, Antigravity, and Codex that brings a milestone's important questions up to be decided before work starts, so execution can then be handed to agents.": it still names `cairn` as a plugin for the three hosts and states the identity in plain present tense with no qualifier.
- `grep -c` finds neither "provides a milestone-driven development workflow" nor the README one-liner's wording "brings all the important questions up to be decided upfront" in `CLAUDE.md` (zero matches each), so the old phrase is gone and the one-liner is not copied word for word.
- The rest of the paragraph is unchanged and still carries milestones as the mechanism, ending "one milestone at a time."
- `git diff --stat` shows `CLAUDE.md` as the only changed file, with 1 insertion and 1 deletion, both on line 7; the `## Milestone Workflow` block at the end of the file still reads "This project uses the milestone-driven workflow." and is outside the diff.
- `git diff --quiet -- core/skills/init-milestone-base-workflow` exits zero: nothing under the bootstrap skill has a diff.
- `AGENTS.md` is still a symlink to `CLAUDE.md` and was not edited directly.

---

