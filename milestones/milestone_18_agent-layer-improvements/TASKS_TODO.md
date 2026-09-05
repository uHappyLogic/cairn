# TASKS TODO

## Namespaced Agent Names In Orchestrator Dispatch

Rewrite the `subagent_type` dispatch instruction in the three orchestrator skills (`complete-all-tasks`, `answer-all-open-questions-with-recommendation`, `recommend-all-open-questions`) to address each agent by its namespaced registry name, phrased descriptively (the `complete-task` agent under this plugin's namespace, listed by Claude Code as `cairn:complete-task`) rather than the bare name, so resolution stays correct if the plugin is renamed or run under another host, and add one sentence to the relevant `CLAUDE.md` invariant stating that orchestrators address dispatched agents by their namespaced registry name. Verified when all three dispatch sites use the namespaced form, `CLAUDE.md` carries the sentence, and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source skills.

---
## Resumable Failed Task Completion Contract

Replace the `FAILED` return promise in `agents/complete-task.md` that a failed run leaves the working tree exactly as it found it (unimplementable once the task has edited files) with a resumable contract: a failed or interrupted run leaves its partial work uncommitted in the tree, and the carry-out step of `shared/complete-procedure.md` states that any already-uncommitted changes are the previous interrupted run's partial work to continue from rather than redo. The answer agent and the orchestrators stay untouched. Verified when no file under `agents/` or `shared/complete-procedure.md` promises an untouched tree on failure, the resume assumption appears in the carry-out step, and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

---
## Rewrite Plugin Root References For Antigravity

Make `scripts/migrate_skills_to_agy.py` rewrite every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the copied skills, agents, and shared files to a path resolvable relative to the generated `.agents/plugins/cairn/` tree, then regenerate that tree, closing the milestone-15 follow-up under which those references are copied verbatim and resolve nowhere. Verified when no file under `.agents/plugins/cairn/` contains the literal `${CLAUDE_PLUGIN_ROOT}` and every rewritten reference names a file that exists in the generated tree.

---
