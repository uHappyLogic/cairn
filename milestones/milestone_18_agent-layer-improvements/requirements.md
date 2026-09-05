# Milestone 18: Agent Layer Improvements

## Goal

A best-effort, open-ended bucket for improvements to cairn's agent layer, taken in its wide sense: the three agents/*.md files, the orchestrator skills that dispatch them, the shared procedures they run in isolation, and the DONE/FAILED return contract between them. Tasks are submitted individually via /submit-task rather than derived from requirements; the milestone has no fixed target and finishes when the submitted queue is empty and the maintainer declares it done. Seed items: drop the pinned model: field from the agent frontmatter so agents inherit the session model, and change the agent color: values so the three remain distinguishable on a grayscale display.

## Relevant starting state

### The three agent files

The agent layer is `agents/complete-task.md` (306 words), `agents/answer-open-question-with-recommendation.md` (415 words), and `agents/recommend-open-question.md` (839 words). Each carries four frontmatter keys: `name`, `description`, `color`, and `model`. All three pin `model: opus`; the colors are `green`, `green`, and `teal`, so two agents already share a color and the third differs from them only in hue. Two user-facing skills also pin `model: opus` in their frontmatter (`skills/answer-open-question-with-recommendation/SKILL.md` and `skills/answer-open-question-with-alternative/SKILL.md`); no other skill carries a `model` or `color` key. Nothing in the repo documents why `model` or `color` were set, and no invariant in `CLAUDE.md` governs either key (the Skill Frontmatter invariant covers only `name` and `description`).

### Dispatch sites and prompt contracts

Three orchestrator skills dispatch agents via the `Agent` tool with `subagent_type` set to the agent name. `complete-all-tasks` sends `Complete the task named: "<TASK_NAME>"` and runs one task at a time. `answer-all-open-questions-with-recommendation` sends a two-line prompt carrying the Short Title and runs strictly sequentially because each dispatch mutates the shared `requirements.md`. `recommend-all-open-questions` sends the Short Title plus the full `<open-question>` block and surrounding requirements as context and may dispatch in parallel because the agent is read-only. Each orchestrator treats a return with no explicit status as `FAILED`, stops the loop on the first failure, and never performs the agent's work itself as a fallback.

### Return and hand-back contracts

Every agent ends with `DONE` or `FAILED: <reason>` as its final line, and each has a different hand-back payload above that line: `complete-task` lists the paths it created or edited so the orchestrator can stage them path-scoped; `answer-open-question-with-recommendation` hands back the lifted "`<option>` — `<rationale>`" text for the commit body; `recommend-open-question` has no `DONE` line at all and instead returns the bare XML sub-elements as its whole final message. A `FAILED` return must leave the working tree untouched. No agent commits; the orchestrator commits after each return via `shared/commit-procedure.md`.

### Shared procedures the agents run in isolation

`complete-task` runs `shared/complete-procedure.md`; `answer-open-question-with-recommendation` runs `shared/answer-with-recommendation-procedure.md`, which composes over `shared/answer-procedure.md`; `recommend-open-question` runs `shared/recommend-procedure.md`. All are execution-neutral (no return protocol, no committing) and are referenced by `${CLAUDE_PLUGIN_ROOT}` path, which the agent body tells the runner to resolve with `echo "$CLAUDE_PLUGIN_ROOT"` if needed. Each of the three shared files is also run inline by a user-facing skill, so an edit to a procedure reaches both the inline and the isolated path.

### Antigravity transpilation of agents

`scripts/migrate_skills_to_agy.py` copies `agents/` into `.agents/plugins/cairn/agents/` with a plain `copytree` and no per-file processing: unlike `skills/*/SKILL.md`, whose frontmatter is parsed and checked for `name`/`description`, agent frontmatter is neither validated nor rewritten, so whatever `model` and `color` values the source carries are shipped verbatim to the generated tree. The generated tree is checked in, and the current one is byte-identical to the source agents (milestone 16 closed with a regeneration). `${CLAUDE_PLUGIN_ROOT}` references are copied unrewritten, a recorded follow-up from milestone 15.

### Documentation surfaces that describe the agents

`CLAUDE.md` carries the agent-related invariants (read-only-subagent norm, the mutation-in-agent divergence of the answer agent, agents-never-commit, the description rules) and its repository-layout block names each agent file. `README.md`'s `## Skill reference` has entries for the two per-question subagents and describes the `complete-task` agent inside the `complete-all-tasks` and `complete-task` entries. Neither surface mentions `model` or `color`, so a frontmatter-only change touches no prose. There is no build or test suite; a change to the agent layer is verified by regenerating the Antigravity tree and reading the diff.

## Decisions

## Out of Scope

