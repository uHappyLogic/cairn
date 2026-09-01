# Milestone 15: Runtime layer de-duplication

## Goal

De-duplicate Cairn's runtime layer (every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md`) by removing three behavior-neutral classes of restatement: end-of-file `## Rules` sections that echo the workflow above them (retiring the `## Rules` heading across the layer and relocating each surviving unique rule into the step where it acts), editor-facing rationale that belongs in CLAUDE.md invariants (moved into the matching invariant first where not already present, then cut), and cross-file narration of counterparts' roles beyond the one sentence the contract needs. A sentence may be cut only if its content survives earlier in the same file, in a referenced shared procedure, or in a CLAUDE.md invariant; point-of-use constraints, worked examples, and templates rendered once stay. Target roughly 11,000 words removed from the 32,758-word layer, prioritizing the per-task, per-question, and per-pass hot files, verified by a per-file constraint-preservation check and a fresh-context re-audit, with the Antigravity tree regenerated.

## Relevant starting state

### Runtime layer inventory and load paths

The runtime layer is 33 plain-Markdown files: 23 `skills/*/SKILL.md`, 3 `agents/*.md`, and 7 `shared/*.md`, totalling 32,758 words. A `SKILL.md` is injected into the conversation in full at every invocation; an agent file is the whole system prompt of every dispatched subagent; a `shared/*.md` procedure is read at run time via a `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference (26 files carry such references — `commit-procedure.md` is referenced 24 times, `get-current-milestone.md` 15, `answer-procedure.md` 9, `task-format.md` 5, the other three 2–3 each). Nearly every reference sentence ends with a "the shared procedure owns X; do not restate those mechanics here" tail. Per-run cost multiplies for the dispatched and looped files: `shared/complete-procedure.md` (1,517 words) is loaded once per task by the `complete-task` agent (379 words), `agents/recommend-open-question.md` (1,442) plus `shared/recommend-procedure.md` (898) once per question per sweep, and `skills/review-milestone-requirements/SKILL.md` (1,906) once per loop pass. The largest single files are `capture-milestone-principle-updates` (2,201), `review-milestone-requirements` (1,906), `recommend-all-open-questions` (1,778), `answer-open-question-with-alternative` (1,705), and `answer-all-open-questions-with-recommendation` (1,691).

### `## Rules` sections

29 of the 33 files end in a `## Rules` section, always the last section of the file, totalling 3,688 words (range 34 words in `complete-task` to 279 in both `agents/recommend-open-question.md` and `capture-milestone-principle-updates`). The four files without one are `agents/complete-task.md` and `agents/answer-open-question-with-recommendation.md` (which close instead with `## Return protocol (subagent only)` sections), `shared/get-current-milestone.md`, and `shared/task-format.md`. The sections are mixed: most bullets restate a numbered workflow step above them (in `answer-all-open-questions-with-recommendation` all six bullets repeat steps 1–2c; in the recommend agent the seven rules restate steps 3–4), but some carry constraints stated nowhere else in the file (e.g. `discuss-milestone-goal`'s "Do not create any files", `define-milestone-goal`'s "Do not update CLAUDE.md or milestones/README.md"). `README.md` never mentions `## Rules` sections, so retiring the heading needs no public-doc sync for that aspect.

### CLAUDE.md invariants as the rationale home

`CLAUDE.md` is 6,356 words; its `## Invariants to preserve when editing skills` section is 35 bullets and 4,839 words, and already holds most of the editor-facing rationale in prose form (the milestone-10 agent-vs-orchestrator commit reversal, the "mutation-in-agent, not read-only-subagent" divergence "documented so a later editor does not 'fix' it back", the skill-only rationale for `answer-open-question-with-alternative`, the terse-reporting convention). The runtime files carry the same rationale in paraphrase rather than verbatim — e.g. `answer-all-open-questions-with-recommendation/SKILL.md` line 103 says "This serialized dispatch is the load-bearing reason…", which no CLAUDE.md sentence matches word-for-word, and the phrase "milestone 10 reversed" appears only in CLAUDE.md, not in any runtime file. `CLAUDE.md` is in context only when working inside this repository; a consuming project never loads it, so anything moved there costs nothing at runtime for plugin users. `AGENTS.md` is a symlink to `CLAUDE.md` (commit 24c670e).

### Cross-file narration

Orchestrator/agent/procedure files describe their counterparts at length: `answer-all-open-questions-with-recommendation/SKILL.md` mentions the agent 27 times, `recommend-all-open-questions` 12, `complete-all-tasks` 11; `agents/recommend-open-question.md` mentions the orchestrator 11 times, the other two agents 6–7 each. The shared procedures open with a paragraph explaining which wrappers reference them and what those wrappers own (see the header of `shared/commit-procedure.md`, whose `## The layer rule` section restates the skill-layer commit rule that also lives as a CLAUDE.md invariant).

### Duplicate template in the recommend agent

`agents/recommend-open-question.md` renders the full `<open-question>` sub-element XML template twice: once in step 3 "Render the XML sub-elements" (line 77) and again in step 4 "Return the sub-elements only" (line 139), with the surrounding prose repeated in part.

### Antigravity transpile tree

`scripts/migrate_skills_to_agy.py` (136 lines, run via `uv run`) regenerates `.agents/plugins/cairn/` from source: it writes `plugin.json`, copies every `skills/<name>/SKILL.md` (skipping directories ending in `-workspace`) after hard-failing on missing YAML frontmatter or a missing `name`/`description` key, copies extra files in each skill directory, and copies `agents/` wholesale. It does **not** copy `shared/`, and it leaves `${CLAUDE_PLUGIN_ROOT}` references verbatim in the generated files. The checked-in tree (25 files) was last regenerated at commit d898085, after the last source change to `skills/`, `agents/`, or `shared/` (a7dae0f), so it is currently in sync. All 25 source `SKILL.md`/agent files carry frontmatter today.

### Verification conventions

The repository has no build, tests, or dependencies; correctness of skill edits has been judged by reading. Milestone 12 established the proof pattern for a layer-wide prose sweep: two dedicated "Run Independent Zero-Findings Re-Audit" tasks in a fresh context (the first surfaced 7 residuals closed by follow-up tasks, the second returned zero findings). Milestone 9 mandated routing all skill/agent edits through the `skill-creator:skill-creator` skill; later milestones did not repeat that mandate. Word counts are reproducible with `wc -w` over the three directories.

## Decisions

## Out of Scope

## Open questions

<open-question id="Reference-tail treatment" status="open">
  <question>Around 26 runtime files reference a shared procedure with a sentence tail of the form: the shared procedure owns the staging, the guard, and the commit; do not restate those mechanics here. The shared files likewise open and close with boundary statements addressed to editors (this file holds only the commit logic; resolving the milestone dir and parsing arguments are the wrappers&apos; job; never restate them here). Are these tails and boundary statements editor-facing restatement to be cut down to the bare reference sentence (with their content living in the CLAUDE.md shared-procedure invariants), or point-of-use instructions the runner needs that must stay?</question>
</open-question>

<open-question id="Reporting-step trim depth" status="open">
  <question>Every committing skill&apos;s final step carries the terse-reporting convention in full: the fixed line to print, the list of things not to add, the sentence that the committed diff and git log are the durable record, and the distinct no-op line with its rationale. The CLAUDE.md terse-reporting invariant says the convention is authored inline in each SKILL.md&apos;s final step because there is deliberately no shared report procedure. How far may this milestone trim those steps: down to the bare print instructions (the success line and the no-op line) with all rationale moved to the invariant, or must the fuller convention text stay inline in each file as that invariant currently implies?</question>
</open-question>

<open-question id="Invariants section growth" status="open">
  <question>Moving rationale out of runtime files into CLAUDE.md will grow the Invariants section, already 35 bullets and about 4,839 words, and several of those bullets already restate each other. Does this milestone only append or extend the matching invariant when moving rationale in (leaving the section&apos;s existing shape alone), or does it also consolidate the Invariants section itself so CLAUDE.md does not become the new duplication sink?</question>
</open-question>

<open-question id="Antigravity shared-procedure gap" status="open">
  <question>The transpile script that regenerates the Antigravity tree copies skills and agents but not the shared directory, and leaves the CLAUDE_PLUGIN_ROOT references verbatim, so the generated skills point at procedure files that do not exist in that tree. This gap predates the milestone. Is fixing it (copying shared into the generated tree, or rewriting the references) in scope, or does the milestone only regenerate the tree as-is and record the gap as out of scope?</question>
</open-question>

<open-question id="Constraint-check record form" status="deferred">
  <question>The per-file constraint-preservation check must show that every imperative in a file&apos;s original text survives at its point of use, in a referenced shared procedure, or in a CLAUDE.md invariant. Where does the evidence of that check land: only as Verified bullets in the TASKS_DONE entry of the task that edited the file, or as a committed checklist artifact under the milestone directory that the re-audit can read?</question>
</open-question>

<open-question id="Re-audit follow-up policy" status="deferred">
  <question>Milestone 12 ran a first fresh-context re-audit, fixed the residuals it found, then ran a second re-audit that returned zero findings. If this milestone&apos;s fresh-context re-audit finds residual duplication or a lost constraint, is a second zero-findings re-audit required after the fixes, or is one audit plus fixes sufficient?</question>
</open-question>

<open-question id="README sync scope" status="deferred">
  <question>README.md never mentions the Rules sections, but its skill reference and workflow prose describe each skill and the referenced-never-restated doctrine. Does this milestone touch README.md at all, and if so only where the sweep falsifies an existing claim, or does it also add a sentence describing the new runtime-files-never-restate-invariants rule?</question>
</open-question>
