# TASKS DONE

## Remove Pinned Model From Agent Frontmatter

Delete the `model: opus` frontmatter line from each of the three files under `agents/` (`complete-task.md`, `recommend-open-question.md`, `answer-open-question-with-recommendation.md`) so a dispatched agent inherits the session's model instead of forcing Opus, leaving `name`, `description`, and `color` untouched. Verified when none of the three source agent files carries a `model` key and the regenerated `.agents/plugins/cairn/agents/` tree is byte-identical to the source.

**Verified:**

- No `model` key remains in the frontmatter of any of the three source agent files: `grep -rn '^model:' agents/` returns nothing, and `yaml.safe_load` of each file's frontmatter yields exactly the keys `name`, `description`, `color`.
- The `name`, `description`, and `color` values are untouched in all three files (`complete-task` green, `answer-open-question-with-recommendation` green, `recommend-open-question` teal); `git diff --stat` shows exactly one deleted line and zero added lines per file.
- The Antigravity tree was regenerated with `uv run scripts/migrate_skills_to_agy.py` and `diff -r agents .agents/plugins/cairn/agents` exits 0 — the generated agent tree is byte-identical to the source.

---

## Remove Pinned Model From Skill Frontmatter

Delete the `model: opus` frontmatter line from the two skills that still carry it, `skills/answer-open-question-with-recommendation/SKILL.md` and `skills/answer-open-question-with-alternative/SKILL.md`, leaving `name` and `description` untouched, so that together with the agent task before it nothing in the plugin pins a model. Verified when a grep for a `model:` frontmatter line across `skills/` and `agents/` finds nothing and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

**Verified:**

- Neither source skill frontmatter carries a `model` key: `grep -rn '^model:' skills/ agents/` returns nothing, and `yaml.safe_load` of each of the two files' frontmatter yields exactly the keys `name`, `description`.
- The `name` and `description` values are untouched in both files; `git diff --numstat` shows exactly one deleted line and zero added lines per source file.
- Together with the completed agent task, nothing in the plugin pins a model: no file under `skills/` or `agents/` (or the generated `.agents/plugins/cairn/` tree) contains a `model:` frontmatter line.
- The Antigravity tree was regenerated with `uv run scripts/migrate_skills_to_agy.py` and `diff -r` of `skills`, `agents`, and `shared` against their `.agents/plugins/cairn/` counterparts each exits 0 — the generated tree is byte-identical to the source.

---
## Grayscale-Distinguishable Agent Colors

Replace the `color:` values in the three files under `agents/` (currently `green`, `green`, `teal`) with three colors from Claude Code's supported named agent palette chosen for maximally separated luminance (one light, one mid, one dark, such as `yellow`, `red`, and `blue`), so that no two agents share a value and all three stay tellable apart on a display viewed through a grayscale filter. Verified when the three source files carry three distinct colors whose grayscale renderings are visibly different from each other and the regenerated `.agents/plugins/cairn/agents/` tree is byte-identical to the source.

**Verified:**

- Each of the three files under `agents/` carries a `color:` value drawn from Claude Code's supported named agent palette: `yellow` (`answer-open-question-with-recommendation`), `red` (`complete-task`), `blue` (`recommend-open-question`).
- The three values are distinct — no two agents share a color, replacing the prior `green`/`green`/`teal` set in which two agents collided.
- The three are maximally luminance-separated across the palette: Rec. 601 relative luma of `yellow` = 0.886 (light), `red` = 0.299 (mid), `blue` = 0.114 (dark), so every pairwise gap (0.185, 0.587, 0.772) stays visibly different under a grayscale filter.
- `uv run scripts/migrate_skills_to_agy.py` completed successfully and each file in `.agents/plugins/cairn/agents/` is byte-identical to its source counterpart under `agents/` (`diff` clean for all three).
- The whole change set is exactly the three source agent files and their three generated counterparts, one line changed in each (`git diff --stat`: 6 files, 6 insertions, 6 deletions).

---

## Recommend Sweep Failure Return And Shape Check

Give `agents/recommend-open-question.md` a failure return whose final line is `FAILED: <reason>` while keeping its success return as the bare XML sub-elements with no `DONE` line, and make `skills/recommend-all-open-questions/SKILL.md` check each return before embedding — it must start with `<alternative` and end with `</recommendation>` — treating a `FAILED:` return or any return failing that shape as a per-question skip rather than a run stop: the block is left untouched, the surviving returns are embedded and committed as today, and the skipped Short Titles with their reasons are printed as a git-absent advisory alongside the terse status line. This closes the one asymmetry in the agent layer's return contracts, where a prose, partial, or explanatory subagent reply is currently spliced into `requirements.md` as XML. Verified by reading both files and confirming that a malformed or `FAILED:` return can no longer reach the whole-block-replacement Edit.

**Verified:**

- `agents/recommend-open-question.md` step 4 states the success return is the bare XML sub-elements with **no `DONE` line**, and adds a failure return whose final line is `FAILED: <reason>` with nothing else returned (no partial sub-elements, no prose standing in for them).
- `skills/recommend-all-open-questions/SKILL.md` step 3 checks every return before embedding: usable only when its first non-whitespace text starts with `<alternative` and its last ends with `</recommendation>`.
- A `FAILED:` return or any return failing that shape check is a per-question skip, not a run stop: nothing is embedded for it, its `<open-question>` block is left byte-for-byte untouched, and the sweep carries on with the other questions.
- Surviving returns are embedded and committed as before: step 4's whole-block-replacement Edit and step 5's once-at-end path-scoped `Recommendation-annotation:` commit are otherwise unchanged, with step 5's no-op note extended to the all-skipped case.
- Step 6 prints the skipped questions' Short Titles with their reasons as a git-absent advisory alongside the terse `Recommendations embedded.` line (and alongside the no-op line when the guard fired).
- Reading both files confirms a malformed or `FAILED:` return can no longer reach step 4's whole-block-replacement Edit — step 3 states explicitly that such a return never reaches it.
- The Antigravity tree was regenerated with `uv run scripts/migrate_skills_to_agy.py`; `diff -r agents .agents/plugins/cairn/agents` and the per-file diff of the changed skill both exit 0.

---
## Namespaced Agent Names In Orchestrator Dispatch

Rewrite the `subagent_type` dispatch instruction in the three orchestrator skills (`complete-all-tasks`, `answer-all-open-questions-with-recommendation`, `recommend-all-open-questions`) to address each agent by its namespaced registry name, phrased descriptively (the `complete-task` agent under this plugin's namespace, listed by Claude Code as `cairn:complete-task`) rather than the bare name, so resolution stays correct if the plugin is renamed or run under another host, and add one sentence to the relevant `CLAUDE.md` invariant stating that orchestrators address dispatched agents by their namespaced registry name. Verified when all three dispatch sites use the namespaced form, `CLAUDE.md` carries the sentence, and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source skills.

**Verified:**

- `skills/complete-all-tasks/SKILL.md`'s dispatch step sets `subagent_type` to the namespaced registry name, phrased descriptively as the `complete-task` agent under this plugin's namespace, listed by Claude Code as `cairn:complete-task`.
- `skills/answer-all-open-questions-with-recommendation/SKILL.md`'s step 2b does the same for `cairn:answer-open-question-with-recommendation`.
- `skills/recommend-all-open-questions/SKILL.md`'s step 3 does the same for `cairn:recommend-open-question`, keeping its "(singular — the per-question subagent)" gloss.
- `grep -rn subagent_type skills agents shared` returns only those three sites and no bare quoted agent name remains.
- `CLAUDE.md`'s "Committing is a property of the skill layer" invariant — the one carrying the orchestrator/dispatched-agent layer contract — gained one **Dispatch naming** sentence stating that an orchestrator addresses each dispatched agent by its namespaced registry name, so resolution survives a plugin rename or another host.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`, and `diff -r --exclude='*-workspace' skills .agents/plugins/cairn/skills`, `diff -r agents .agents/plugins/cairn/agents`, and `diff -r shared .agents/plugins/cairn/shared` all exit 0.

---
## Resumable Failed Task Completion Contract

Replace the `FAILED` return promise in `agents/complete-task.md` that a failed run leaves the working tree exactly as it found it (unimplementable once the task has edited files) with a resumable contract: a failed or interrupted run leaves its partial work uncommitted in the tree, and the carry-out step of `shared/complete-procedure.md` states that any already-uncommitted changes are the previous interrupted run's partial work to continue from rather than redo. The answer agent and the orchestrators stay untouched. Verified when no file under `agents/` or `shared/complete-procedure.md` promises an untouched tree on failure, the resume assumption appears in the carry-out step, and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

**Verified:**

- `agents/complete-task.md` no longer promises an untouched tree on failure: its closing return-protocol sentence now states that a `FAILED` return leaves whatever partial work it managed uncommitted in the working tree, never reverted or cleaned up, so a later run resumes from it instead of starting over.
- The carry-out step (`### 3. Carry out the task`) of `shared/complete-procedure.md` opens with the resume assumption: uncommitted changes already in the tree may be a previous failed or interrupted run's partial work, to be read, continued from, and carried in the running list of touched paths rather than redone or reverted, with unrelated uncommitted changes left alone.
- The added paragraph keeps `shared/complete-procedure.md` execution-neutral — it describes the state of the tree only, and still mentions no return protocol, no commit step, and no follow-up.
- No file under `agents/` and no line of `shared/complete-procedure.md` promises an untouched tree on failure for the completion path: `grep -rn 'exactly as it found it\|exactly as you found it' agents/ shared/complete-procedure.md` returns only `agents/answer-open-question-with-recommendation.md`'s pre-edit clean-stop instruction, which the task holds out of scope ("the answer agent and the orchestrators stay untouched") and which stays implementable because that agent's failure modes fire before it edits anything.
- The answer agent, the recommend agent, and the three orchestrator skills are unmodified: `git status --porcelain` lists exactly `agents/complete-task.md`, `shared/complete-procedure.md`, and their two generated counterparts.
- `uv run scripts/migrate_skills_to_agy.py` regenerated `.agents/plugins/cairn/`, and `diff -r agents .agents/plugins/cairn/agents` and `diff -r shared .agents/plugins/cairn/shared` both exit 0 — the generated tree is byte-identical to the source.

---
