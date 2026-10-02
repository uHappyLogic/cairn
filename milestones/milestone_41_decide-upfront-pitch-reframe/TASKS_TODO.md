# TASKS TODO

## Update Release Skill Distribution Description Pattern

Change the `--description` argument of the `gh repo create` command in `.claude/skills/release-plugin/SKILL.md` to the new distribution pattern: the identity sentence "Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently." first, then a shortened pointer giving the host name, the fact that the repository is published from `uHappyLogic/cairn`, and that issues go there, with only the host varying. This fixes the one wording the three live distribution descriptions are then set from, so the printed command and the live descriptions stay identical. Verified when the command carries that pattern with its `<host>` slot and the old "Distribution of the Cairn plugin for <host>, published verbatim by each release of uHappyLogic/cairn. Report issues there." string is gone from the file.

---

## Push Main And Set GitHub Repository Metadata

Push `main` to origin as a plain fast-forward, never forced, so the committed root README rewrite goes public, then in the same task set with `gh` the description of `uHappyLogic/cairn` to the README one-liner word for word followed by the host clause "— for Claude Code, Google Antigravity, and Codex.", and the descriptions of `uHappyLogic/cairn-claude`, `uHappyLogic/cairn-antigravity`, and `uHappyLogic/cairn-codex` to the `--description` pattern in `.claude/skills/release-plugin/SKILL.md` with each host filled in. Also add the topics `codex`, `openai-codex`, `ai-agents`, `autonomous-agents`, `spec-driven-development`, and `requirements` to `uHappyLogic/cairn`, removing none of its fourteen existing topics, which brings the list to GitHub's 20-topic cap. Verified when `origin/main` holds the README commits and `gh repo view` shows the four descriptions as specified and all 20 topics on the root repository.

---
