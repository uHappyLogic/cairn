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
## Rewrite Plugin Root References For Antigravity

Make `scripts/migrate_skills_to_agy.py` rewrite every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the copied skills, agents, and shared files to a path resolvable relative to the generated `.agents/plugins/cairn/` tree, then regenerate that tree, closing the milestone-15 follow-up under which those references are copied verbatim and resolve nowhere. Verified when no file under `.agents/plugins/cairn/` contains the literal `${CLAUDE_PLUGIN_ROOT}` and every rewritten reference names a file that exists in the generated tree.

**Verified:**

- `scripts/migrate_skills_to_agy.py` rewrites plugin-root references on the copy: a module-level `rewrite_plugin_root()` replaces the literal `${CLAUDE_PLUGIN_ROOT}` with the generated tree's workspace-relative path (derived from the script's own `plugin_dir`, so it tracks the `plugin_name` argument), and `rewrite_tree()` applies it to every text file already copied under a destination directory.
- The rewrite runs on all three copied trees: `rewrite_tree()` is called once for the skills destination (after the per-skill copy loop, so it covers non-`SKILL.md` files too), once for the agents copy, and once for the shared copy.
- The generated tree was regenerated with `uv run scripts/migrate_skills_to_agy.py`, which completed successfully and rewrote 25 files under `.agents/plugins/cairn/`.
- No file under `.agents/plugins/cairn/` contains the literal `${CLAUDE_PLUGIN_ROOT}`: `grep -rn 'CLAUDE_PLUGIN_ROOT}' .agents` returns nothing, and the stricter `grep -rn 'CLAUDE_PLUGIN_ROOT' .agents` (which also catches the bare `$CLAUDE_PLUGIN_ROOT` of the resolve hint) returns nothing either.
- Every rewritten reference names a file that exists in the generated tree: each of the 7 distinct `.agents/plugins/cairn/shared/<name>.md` paths appearing in the generated files (`answer-procedure`, `answer-with-recommendation-procedure`, `commit-procedure`, `complete-procedure`, `get-current-milestone`, `recommend-procedure`, `task-format`) resolves to an existing file.
- No reference was lost in the rewrite: the source trees hold 47 `${CLAUDE_PLUGIN_ROOT}/shared/` references and the generated tree holds 47 `.agents/plugins/cairn/shared/` references.
- The now-meaningless `` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path) `` hint is dropped from the generated copies in the same pass, with its leading whitespace, so each of the 7 affected sentences still reads correctly across its line wrap.
- The rewrite touches only the copy: `git status --porcelain` lists no file under `skills/`, `agents/`, or `shared/`, so the canonical sources still carry `${CLAUDE_PLUGIN_ROOT}` for Claude Code to resolve.
- Generation is idempotent and the script still parses: a second `uv run scripts/migrate_skills_to_agy.py` leaves the same 25 modified files and no further diff, and `ast.parse` of the script succeeds.
- `CLAUDE.md`'s Development section no longer records the verbatim copy as a known follow-up: it now states that the script rewrites those references to `.agents/plugins/cairn/shared/<name>.md`, drops the resolve hint, and does both only on the copy.

---

## Pass Milestone Directory To Recommend Agent

Change the dispatch prompt in `skills/recommend-all-open-questions/SKILL.md` step 3 to carry the resolved `<MILESTONE_DIR>` alongside the Short Title and the question's full `<open-question>` block, dropping the "plus relevant surrounding requirements" clause so the orchestrator never reads the whole `requirements.md` to build context, and rewrite the Inputs section of `agents/recommend-open-question.md` to name `<MILESTONE_DIR>` as a prompt input the agent uses to read that milestone's `requirements.md` read-only for grounding, replacing the current instruction that it does not resolve the directory. This closes the contradiction where the agent is told not to resolve the directory while the shared recommend core it runs requires reading that milestone's `requirements.md`. Verified by reading both files to confirm the prompt template and the agent's Inputs section agree, and by regenerating the Antigravity tree with `uv run scripts/migrate_skills_to_agy.py` so `.agents/plugins/cairn/` stays byte-identical to the source.

**Verified:**

- `skills/recommend-all-open-questions/SKILL.md` step 3's dispatch prompt template carries `Milestone directory: <MILESTONE_DIR>` alongside `Short Title:` and the question's full `<open-question>` block.
- That template no longer carries the "plus relevant surrounding requirements" clause, and the step states the block is the only requirements text the prompt carries, so the orchestrator never reads the whole `requirements.md` to assemble context.
- `agents/recommend-open-question.md`'s Inputs section names `<MILESTONE_DIR>` as a prompt input the agent uses to read that milestone's `requirements.md` read-only for grounding, and the "do **not** resolve `<MILESTONE_DIR>`" instruction is gone.
- The two files agree: every input the prompt template sends (Short Title, milestone directory, question block) is an input the agent's Inputs section names, and nothing more.
- `uv run scripts/migrate_skills_to_agy.py` ran clean, and `.agents/plugins/cairn/agents/recommend-open-question.md` and `.agents/plugins/cairn/skills/recommend-all-open-questions/SKILL.md` differ from their sources only by the script's documented `${CLAUDE_PLUGIN_ROOT}` path rewrite and resolve-hint drop.

---

## Agent Stages Own Change Set Before Return

Change the two file-editing agents so each path-scoped `git add`s its own change set and returns only `DONE` or `FAILED: <reason>` with no hand-back payload: `agents/complete-task.md` stages the paths recorded while carrying out the task plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md` (dropping its path hand-back section), and `agents/answer-open-question-with-recommendation.md` stages `<MILESTONE_DIR>/requirements.md` (dropping its lifted-recommendation hand-back), while `skills/complete-all-tasks/SKILL.md` and `skills/answer-all-open-questions-with-recommendation/SKILL.md` commit the already-staged index under their existing subjects, the answer orchestrator lifting the `<recommendation>` text for its commit body from the block during its pre-dispatch re-check rather than from the agent, and the `CLAUDE.md` invariants describing the hand-back are updated to the stage-then-return arrangement, with `shared/commit-procedure.md` and `shared/complete-procedure.md` left execution-neutral. Staging is not committing, so the agents-never-commit rule holds. Verified when neither agent file mentions handing back paths or recommendation text, both orchestrators commit without a hand-back input, and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

**Verified:**

- `agents/complete-task.md` carries a staging step that `git add`s the recorded created/edited paths plus `<MILESTONE_DIR>/TASKS_TODO.md` and `<MILESTONE_DIR>/TASKS_DONE.md`, naming each explicitly and never `git add -A`, on the success path only.
- Its path hand-back section is gone and its `DONE` line carries no payload; the `FAILED` line still leaves partial work in the tree, unstaged and uncommitted.
- `agents/answer-open-question-with-recommendation.md` carries a staging step that `git add`s `<MILESTONE_DIR>/requirements.md` path-scoped, its lifted-recommendation hand-back is gone, and its `DONE` line carries no payload.
- Neither agent file mentions handing back paths or recommendation text (`grep` for hand-back phrasing over `agents/*.md` returns nothing), and neither commits — both state that staging is not committing and that the orchestrator commits the index they leave.
- `skills/complete-all-tasks/SKILL.md` step 2c commits the already-staged index under `Tasklist-completion: <descriptor>` with the task heading in the commit body, behind a nothing-staged no-op guard, taking no hand-back input and staging nothing itself.
- `skills/answer-all-open-questions-with-recommendation/SKILL.md` step 2a lifts the `<recommendation>` text as `<option> — <rationale>` during the pre-dispatch re-check, and step 2c commits the already-staged index under `Recommendation-answer: <Short Title>` with that lifted text as the body, behind a nothing-staged no-op guard.
- `CLAUDE.md`'s repository-layout line, the `answer-with-recommendation-procedure` invariant, the sweep invariant, and the skill-layer commit invariant all describe the stage-then-return arrangement; no `CLAUDE.md` or `README.md` prose still says an agent hands paths or recommendation text back.
- `shared/commit-procedure.md` and `shared/complete-procedure.md` are unmodified (`git status --porcelain shared/` is empty), so both stay execution-neutral.
- `uv run scripts/migrate_skills_to_agy.py` ran clean and regenerated exactly the four affected files under `.agents/plugins/cairn/`, which differ from their sources only by the script's documented `${CLAUDE_PLUGIN_ROOT}` path rewrite and resolve-hint drop.

---

## Fold Decision Before Removing Question Block

Reorder the recording core in `shared/answer-procedure.md` so the decision is folded into `## Decisions` (currently step 5) before the matched `<open-question>` block is removed (currently step 4), keeping the cascade step last and the three edits separate, and update the step references in `shared/answer-with-recommendation-procedure.md` and the `CLAUDE.md` invariant that narrate the locate → remove → fold → cascade order. Today a failure or interruption between the removal and the fold leaves the block gone and the decision unrecorded, so the next sweep no longer gathers the question and it is silently lost; folding first leaves a harmless superset state instead. Verified by reading the procedure to confirm the fold precedes the removal, confirming no runtime or invariant text still states remove-then-fold, and regenerating the Antigravity tree with `uv run scripts/migrate_skills_to_agy.py` so `.agents/plugins/cairn/` stays byte-identical to the source.

**Verified:**

- `shared/answer-procedure.md` step 4 is "Fold the decision into `## Decisions`" and step 5 is "Remove the answered block", so the fold precedes the removal in the recording core.
- Step 5 removes the same `<open-question …>`…`</open-question>` boundary-line span located in step 2 and instructs re-running the boundary-line query first, because the step 4 fold shifted those line numbers.
- Step 6 is still the cascade and remains last, and the closing paragraph still requires steps 4–6 as three separate targeted edits (fold, removal, cascade).
- The procedure's own summary line reads "locate, analyse, fold, remove, cascade".
- `shared/answer-with-recommendation-procedure.md` step 4 narrates the delegated recording work as "(locate, analyse, fold, remove, cascade)".
- The `CLAUDE.md` repository-layout line and the answer-recording invariant both narrate locate → fold → remove → cascade, and the invariant states the fold-before-removal order is deliberate, why (interruption leaves a harmless superset instead of a silently lost question), and that removal re-queries the shifted boundary lines.
- No runtime file (`skills/`, `agents/`, `shared/`) or `CLAUDE.md`/`README.md` prose still states remove-then-fold: the three other narration sites (`skills/answer-open-question/SKILL.md`, `skills/answer-open-question-with-recommendation/SKILL.md`, `agents/answer-open-question-with-recommendation.md`) now read "fold/remove", and `skills/answer-open-question-with-alternative/SKILL.md` names the fold before the block removal.
- `uv run scripts/migrate_skills_to_agy.py` ran clean, and each regenerated file under `.agents/plugins/cairn/` differs from its source only by the script's documented `${CLAUDE_PLUGIN_ROOT}` path rewrite.

---
