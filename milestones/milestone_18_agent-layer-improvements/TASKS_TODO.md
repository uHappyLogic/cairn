# TASKS TODO

## Remove Pinned Model From Skill Frontmatter

Delete the `model: opus` frontmatter line from the two skills that still carry it, `skills/answer-open-question-with-recommendation/SKILL.md` and `skills/answer-open-question-with-alternative/SKILL.md`, leaving `name` and `description` untouched, so that together with the agent task before it nothing in the plugin pins a model. Verified when a grep for a `model:` frontmatter line across `skills/` and `agents/` finds nothing and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

---
## Grayscale-Distinguishable Agent Colors

Replace the `color:` values in the three files under `agents/` (currently `green`, `green`, `teal`) with three colors from Claude Code's supported named agent palette chosen for maximally separated luminance (one light, one mid, one dark, such as `yellow`, `red`, and `blue`), so that no two agents share a value and all three stay tellable apart on a display viewed through a grayscale filter. Verified when the three source files carry three distinct colors whose grayscale renderings are visibly different from each other and the regenerated `.agents/plugins/cairn/agents/` tree is byte-identical to the source.

---
## Recommend Sweep Failure Return And Shape Check

Give `agents/recommend-open-question.md` a failure return whose final line is `FAILED: <reason>` while keeping its success return as the bare XML sub-elements with no `DONE` line, and make `skills/recommend-all-open-questions/SKILL.md` check each return before embedding — it must start with `<alternative` and end with `</recommendation>` — treating a `FAILED:` return or any return failing that shape as a per-question skip rather than a run stop: the block is left untouched, the surviving returns are embedded and committed as today, and the skipped Short Titles with their reasons are printed as a git-absent advisory alongside the terse status line. This closes the one asymmetry in the agent layer's return contracts, where a prose, partial, or explanatory subagent reply is currently spliced into `requirements.md` as XML. Verified by reading both files and confirming that a malformed or `FAILED:` return can no longer reach the whole-block-replacement Edit.

---
## Namespaced Agent Names In Orchestrator Dispatch

Rewrite the `subagent_type` dispatch instruction in the three orchestrator skills (`complete-all-tasks`, `answer-all-open-questions-with-recommendation`, `recommend-all-open-questions`) to address each agent by its namespaced registry name, phrased descriptively (the `complete-task` agent under this plugin's namespace, listed by Claude Code as `cairn:complete-task`) rather than the bare name, so resolution stays correct if the plugin is renamed or run under another host, and add one sentence to the relevant `CLAUDE.md` invariant stating that orchestrators address dispatched agents by their namespaced registry name. Verified when all three dispatch sites use the namespaced form, `CLAUDE.md` carries the sentence, and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source skills.

---
## Resumable Failed Task Completion Contract

Replace the `FAILED` return promise in `agents/complete-task.md` that a failed run leaves the working tree exactly as it found it (unimplementable once the task has edited files) with a resumable contract: a failed or interrupted run leaves its partial work uncommitted in the tree, and the carry-out step of `shared/complete-procedure.md` states that any already-uncommitted changes are the previous interrupted run's partial work to continue from rather than redo. The answer agent and the orchestrators stay untouched. Verified when no file under `agents/` or `shared/complete-procedure.md` promises an untouched tree on failure, the resume assumption appears in the carry-out step, and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

---
## Rewrite Plugin Root References For Antigravity

Make `scripts/migrate_skills_to_agy.py` rewrite every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the copied skills, agents, and shared files to a path resolvable relative to the generated `.agents/plugins/cairn/` tree, then regenerate that tree, closing the milestone-15 follow-up under which those references are copied verbatim and resolve nowhere. Verified when no file under `.agents/plugins/cairn/` contains the literal `${CLAUDE_PLUGIN_ROOT}` and every rewritten reference names a file that exists in the generated tree.

---
