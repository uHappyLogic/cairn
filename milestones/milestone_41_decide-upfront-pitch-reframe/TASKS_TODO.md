# TASKS TODO

## Rewrite Why Cairn Around Handing Off Execution

Rewrite the three paragraphs of the root README's `## Why Cairn?`: the first opens with the problem of handing off long-running execution (an agent left to run for a long time hits questions nobody decided and either guesses quietly and builds on the guess or stops and waits for a person, so you cannot walk away), the second presents milestones as the mechanism (each milestone first brings its open questions up, has them answered with recorded decisions, and only then derives tasks an agent can complete unattended), and the third keeps work-type neutrality as the supporting point through the environment read from `CLAUDE.md`. The section says once, in plain words, that bringing up all the important questions is the principle Cairn is built toward and that later milestones work toward it, and it adopts no category noun for Cairn ("framework" and "workflow" are not used as identity nouns). Verified when the section is three paragraphs carrying that content and `## How it works` and `## Self-dogfooding` are unchanged word for word.

---

## Lead Design Principles With Claims 1 And 14

Change the root README's `## Design principles` block to three bullets in this order: claim 1 ("Cairn finds the open questions before the work starts.") and claim 14 ("Unattended batch runs are possible.") with new glosses, then claim 2 ("Each decision has a record in git.") with its current gloss, removing the claim 11 and claim 5 bullets so the block surfaces the two claims the new pitch rests on. Verified when each bullet's claim line is verbatim and links to its anchor in `docs/design-claims.md`, the closing link to all nineteen claims is unchanged, and `docs/design-claims.md` itself has no diff.

---

## Carry One-Liner Into Host README Templates

Replace the line under `# Cairn for <Host>` in `scripts/hosts/claude/README.md`, `scripts/hosts/antigravity/README.md`, and `scripts/hosts/codex/README.md` with the root README one-liner verbatim, "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.", then run `uv run scripts/build_hosts.py` so the rebuilt `hosts/` trees ride with the templates. Verified when `uv run scripts/build_hosts.py --check` exits zero and each rendered `hosts/<host>/README.md` carries the one-liner under its title with no milestone-driven line left.

---

## Unify Manifest Descriptions On The One-Liner

Set all five description strings to the README one-liner word for word, "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.": the three plugin manifests (`scripts/hosts/claude/.claude-plugin/plugin.json`, `scripts/hosts/antigravity/plugin.json`, `scripts/hosts/codex/plugins/cairn/.codex-plugin/plugin.json`) and the two Claude marketplace files (the hand-kept root `.claude-plugin/marketplace.json` and the template `scripts/hosts/claude/.claude-plugin/marketplace.json`). This ends the split into a long and a short string and drops the plugin manifests' step list; the `hosts/` trees are rebuilt with `uv run scripts/build_hosts.py` and no release is cut. Verified when `uv run scripts/build_hosts.py --check` exits zero and all five files and their rendered copies carry the one string.

---

## Restate CLAUDE.md Opening Identity Sentence

Reword the first sentence of `## What this repo is` in `CLAUDE.md` so it still names `cairn` as a plugin for Claude Code, Antigravity, and Codex but, in place of "provides a milestone-driven development workflow", states in the editor's own words and plain present tense that it brings a milestone's important questions up to be decided before work starts, so execution can then be handed to agents. The README one-liner is not copied word for word, and milestones stay in the rest of the paragraph as the mechanism. Verified when that sentence is the only change: the `## Milestone Workflow` block at the end of `CLAUDE.md` and everything under `core/skills/init-milestone-base-workflow/` have no diff.

---

## Update Release Skill Distribution Description Pattern

Change the `--description` argument of the `gh repo create` command in `.claude/skills/release-plugin/SKILL.md` to the new distribution pattern: the identity sentence "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently." first, then a shortened pointer giving the host name, the fact that the repository is published from `uHappyLogic/cairn`, and that issues go there, with only the host varying. This fixes the one wording the three live distribution descriptions are then set from, so the printed command and the live descriptions stay identical. Verified when the command carries that pattern with its `<host>` slot and the old "Distribution of the Cairn plugin for <host>, published verbatim by each release of uHappyLogic/cairn. Report issues there." string is gone from the file.

---

## Push Main And Set GitHub Repository Metadata

Push `main` to origin as a plain fast-forward, never forced, so the committed root README rewrite goes public, then in the same task set with `gh` the description of `uHappyLogic/cairn` to the README one-liner word for word followed by the host clause "— for Claude Code, Google Antigravity, and Codex.", and the descriptions of `uHappyLogic/cairn-claude`, `uHappyLogic/cairn-antigravity`, and `uHappyLogic/cairn-codex` to the `--description` pattern in `.claude/skills/release-plugin/SKILL.md` with each host filled in. Also add the topics `codex`, `openai-codex`, `ai-agents`, `autonomous-agents`, `spec-driven-development`, and `requirements` to `uHappyLogic/cairn`, removing none of its fourteen existing topics, which brings the list to GitHub's 20-topic cap. Verified when `origin/main` holds the README commits and `gh repo view` shows the four descriptions as specified and all 20 topics on the root repository.

---
