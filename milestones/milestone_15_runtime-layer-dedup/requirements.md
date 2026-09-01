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

### Shared-procedure reference tails

Shared-procedure reference tails and the shared files' own boundary statements are split by audience, clause by clause. The runner-facing delegation clause — what the referenced file owns, normalized to one short fixed form alongside the inputs the caller supplies — stays, as does every file-specific sentence such as which clean-stop or no-op case the guard covers. The editor-facing imperatives ("do not restate those mechanics here", "never restate them here") and the shared files' editor-addressed boundary paragraphs are cut, after verifying their content is present in the matching CLAUDE.md invariant. This requires a per-file read rather than one sweep-wide substitution. If the per-file constraint-preservation check later shows the normalized owns-X clause delivers nothing the reference sentence and the shared file do not already give the runner, that clause may collapse to the bare reference as a follow-up.

### Terse-reporting steps

Each committing skill's final reporting step is trimmed only of its justification sentences — that the committed diff and `git log` are the durable record, and that git holds no durable record of a no-op — whose content already survives in the CLAUDE.md terse-reporting invariant. Everything that shapes the printed output stays inline at its point of use: the fixed success-line string, the file-specific list of what must not be printed (no identifier, no next-step pointer, nothing more), the no-op branch with its per-file trigger, and any git-absent advisory that step owns. Because a consuming project never loads CLAUDE.md, those prohibitions cannot be relocated there; the boundary between prohibition and justification is a per-file judgment made during the edit, not a sweep-wide substitution. No `shared/report-procedure.md` is created.

### CLAUDE.md Invariants section

The runtime-layer sweep runs append-or-extend only against a frozen Invariants section: rationale moved out of a runtime file extends the matching invariant or is appended as a new bullet, and no existing bullet is reshaped while the sweep is in progress, so every cut stays justified against a stable reference target. Consolidation of the Invariants section itself happens once, in a single dedicated task after the sweep completes and before the fresh-context re-audit, rewriting the section as a whole to merge overlapping bullets and absorb the newly moved rationale with the full post-move content visible. Because that pass rewrites bullets the completed cuts depend on, it carries its own constraint-preservation check over CLAUDE.md rather than inheriting the runtime layer's.

### Verification

The fresh-context re-audit audits but never fixes. Its findings become follow-up fix tasks, and a further fresh-context re-audit over the whole runtime layer is queued after those fixes, repeating until a run returns a clean verdict — the audited final state of the files, not the pre-fix state, is what proves the milestone.

Any finding the planned fix tasks do not address is recorded in `temp/milestone_15_findings.md` together with the reason it was not fixed. The loop terminates when a re-audit returns no findings other than those already recorded there: a finding is either fixed, or registered with a stated reason, and there is no third state in which one is silently tolerated.

The per-file constraint-preservation check is recorded in the pipeline's own `**Verified:**` channel — the `TASKS_DONE.md` entry of the task that edited the file — and no separate checklist artifact is added under the milestone directory, which stays at its three files. The shape is pinned rather than left to the completer: the entry carries the check as an explicit ledger with one bullet per imperative removed or relocated, naming where that imperative now survives (its point of use in the same file, the referenced shared procedure, or the CLAUDE.md invariant). Each editing task's description must therefore pin this ledger shape, since the completer otherwise derives its own bar. Git history supplies the original text the ledger is a claim about, so the re-audit can check each claim against the live file.

### Antigravity transpile tree

`scripts/migrate_skills_to_agy.py` gains a `shared/` copy into the generated tree, mirroring the wholesale `agents/` copytree it already performs, so that every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the generated skills and agents resolves to a file that is actually present. This is in scope because the sweep deletes prose on the grounds that its content survives in a referenced shared procedure, and shipping a regenerated tree whose procedures are absent would undercut the milestone's own deletion rule; the change is small, in the shape of code already in the script, and verifiable here by inspecting the regenerated file list. Rewriting the `${CLAUDE_PLUGIN_ROOT}` reference text itself to an Antigravity-resolvable path stays out of scope — there is no Antigravity runtime, test, or known-good target path in this repository to verify such a transform against — and is recorded as a follow-up.

### README sync scope

README.md is touched only where a sweep edit makes an existing claim false: a verification pass over its skill reference and workflow prose that edits solely on a confirmed falsification and adds no new prose. The sweep is behavior-neutral, so the only honest README work is confirming that no existing claim went stale. No sentence describing the runtime-files-never-restate-invariants rule is added — that rule is an authoring convention whose single home is the CLAUDE.md invariant, and repeating it in a user-facing README would recreate the very duplication this milestone removes.

### Frontmatter description scope

The YAML frontmatter `description` fields of the `SKILL.md` and agent files stay outside the three cut classes: no description text is cut for restating its body, keeping the triggering surface Claude Code and the Antigravity transpile read behavior-neutral by construction, since it is the one surface this repository cannot verify. The single exception is falsification: each editing task confirms its file's own description still holds against the edited body and edits it only on a confirmed false claim, adding no new prose and removing no invocation or use-when vocabulary — the same rule the README sync scope decision already applies, so each editing task can state it in one sentence.

### Editing route

Every runtime-file edit in this milestone is made directly against the `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` files with the ordinary editing tools; edits are not routed through the `skill-creator:skill-creator` skill, whose milestone-9 mandate is treated as scoped to that milestone rather than standing. This sweep is precision deletion of existing prose, proved by its own per-file constraint-preservation ledger and the fresh-context re-audit loop rather than by authoring quality, and direct editing is the established practice of every milestone since 9. The rule is uniform across all three directories — `shared/*.md` files are not skills at all — so each editing task's description can state it in one sentence.

## Out of Scope

## Open questions

<open-question id="Re-audit finding scope" status="open">
  <question>What counts as a finding for the fresh-context re-audit whose clean verdict proves the milestone: only lost constraints (an imperative removed from a runtime file with no surviving home, or a `**Verified:**` ledger claim that does not hold against the live file), or also residual restatement the sweep missed (a remaining `## Rules` heading, editor-facing rationale still in a runtime file, cross-file narration beyond the one sentence the contract needs)? The choice fixes what &quot;clean&quot; means and how many fix-and-re-audit rounds the loop can take.</question>
  <alternative id="Loss only">
    A finding is exclusively a preservation regression — an imperative removed from a runtime file with no surviving home, or a `**Verified:**` ledger bullet whose claim does not hold against the live file — checked against git history, with residual restatement explicitly out of scope.
    <advantage>Every finding is a falsifiable claim against a fixed reference (the pre-sweep text in git plus the ledger), so the audit is objective, cheap to adjudicate, and converges in the fewest rounds.</advantage>
    <drawback>A clean verdict would prove only that nothing was broken, not that the sweep did its job — a run that removed almost none of the three restatement classes would still pass, leaving the milestone&apos;s actual objective unverified.</drawback>
  </alternative>
  <alternative id="Loss plus mechanical check">
    The re-audit reports only lost constraints, and completeness is covered separately by mechanical checks the repo already supports — a `grep` for surviving `## Rules` headings and a `wc -w` delta against the 32,758-word baseline.
    <advantage>Splits the objective, machine-checkable part of completeness away from judgment-heavy reading, keeping the audit bounded while still catching the one cut class that has a crisp textual signature.</advantage>
    <drawback>The two classes that actually need reading — editor-facing rationale still sitting in a runtime file, and cross-file narration beyond the one sentence the contract needs — have no grep signature, so most of the completeness surface stays unverified.</drawback>
  </alternative>
  <alternative id="Both classes uniform">
    Both lost constraints and residual restatement count as findings of equal weight, and clean means the run returned neither, with the already-decided `temp/milestone_15_findings.md` valve applying uniformly to any finding of either class.
    <advantage>The clean verdict proves the milestone end to end — nothing lost and nothing missed — with a single criterion the fresh-context auditor can be handed verbatim, exactly as milestone 12 handed over its one criterion.</advantage>
    <drawback>The uniform valve lets a genuine preservation regression be registered with a reason rather than fixed, which quietly undercuts the constraint-preservation guarantee the ledger exists to provide.</drawback>
  </alternative>
  <alternative id="Loss blocking, residual triaged">
    Both classes are findings, but with different dispositions: a lost constraint or false ledger claim must be fixed and cannot be registered away, while a residual-restatement finding is reported and then either fixed or registered in `temp/milestone_15_findings.md` with its reason; clean means zero loss findings and no unregistered residuals.
    <advantage>Gives the clean verdict the full meaning the goal asks for — no regression and no missed restatement — while capping the round count, since the judgment-heavy class can be honestly accepted with a stated reason instead of forcing another fix-and-re-audit cycle.</advantage>
    <drawback>The auditor must classify each finding as well as report it, and the tiering could be misused to wave through real residuals under a thin reason.</drawback>
  </alternative>
  <recommendation option="Loss blocking, residual triaged">The two classes carry genuinely different consequences — a lost constraint is a defect the ledger exists to prevent, a residual is a missed cut that can be honestly accepted — so tiering them is what lets the recorded fix-or-register rule bound the loop without letting a preservation regression be registered away.</recommendation>
</open-question>

<open-question id="Step-less rule placement" status="deferred">
  <question>When a retired `## Rules` section carries a unique rule that constrains the whole skill rather than any one numbered step (e.g. discuss-milestone-goal&apos;s &quot;Do not create any files&quot;), where in the file does it survive — the opening description, the step whose output it most constrains, or a single sentence at the point the file first could violate it — without regrowing a Rules-like list under a different heading?</question>
  <alternative id="Opening description">
    Fold each step-less rule into the file&apos;s existing opening description paragraph as prose — one sentence continuing the blurb that already states what the skill does and does not do — never as a bullet list.
    <advantage>Scope matches scope: a constraint on the whole skill lands in the one place that already states the whole skill&apos;s boundaries, and several files (`discuss-milestone-goal`&apos;s &quot;not a document yet&quot;, `define-milestone-goal`&apos;s &quot;Does not populate the remaining sections&quot;) already carry a near-identical sentence there, so the relocation extends existing prose instead of inventing a home.</advantage>
    <drawback>The opening paragraph becomes the accumulation site for every step-less rule in a file, so a skill with three or four of them risks a run-on scope blurb that is a Rules list in prose clothing unless the no-bullet-list constraint is enforced per file.</drawback>
  </alternative>
  <alternative id="Nearest step">
    Attach each step-less rule to the numbered step whose output it most constrains, matching the goal&apos;s stated default of relocating a surviving rule into the step where it acts.
    <advantage>One uniform relocation rule for the whole sweep — no separate step-less category, and the point-of-use discipline already decided for the terse-reporting steps applies unchanged.</advantage>
    <drawback>It misstates the constraint&apos;s scope: pinning &quot;Do not create any files&quot; to one step of a five-step conversational skill implies the other four are unconstrained, and choosing which step it &quot;most&quot; constrains is an arbitrary per-file call that a re-audit cannot check against anything.</drawback>
  </alternative>
  <alternative id="First-violation point">
    Place each step-less rule as a single sentence at the earliest point in the file where the skill could first violate it.
    <advantage>Gives a deterministic, mechanically checkable placement rule that puts the prohibition ahead of the behavior it forbids.</advantage>
    <drawback>For most of the real cases the first violation point is step 1 or earlier — a purely conversational skill could create a file at any step — so the rule collapses into the opening description anyway while adding a per-file judgment that has to be made and defended.</drawback>
  </alternative>
  <alternative id="Per-file judgment">
    Fix no placement rule; let each editing task pick whichever of the three homes fits that rule, with only the no-Rules-like-list constraint binding sweep-wide.
    <advantage>Mirrors the precedent already set for the terse-reporting steps and the reference tails, where the milestone accepted a per-file read over a sweep-wide substitution.</advantage>
    <drawback>Placement here has no per-file signal to judge on the way a reporting step does, so the freedom buys nothing and costs consistency: the same class of rule ends up in three different places across 29 files, and the fresh-context re-audit gets no fixed target to verify against.</drawback>
  </alternative>
  <recommendation option="Opening description">A rule that constrains the whole skill belongs where the whole skill&apos;s boundaries are already stated, and the opening blurb is that place — it is one named location the re-audit can check, it needs no arbitrary &quot;which step&quot; call, and in the named examples it merely extends a sentence the file already has; the no-Rules-list requirement is met by pinning the form as prose folded into the existing paragraph, never a bullet list under any heading.</recommendation>
</open-question>

<open-question id="Word-count shortfall handling" status="deferred">
  <question>If applying the three cut classes under the cut rule (a sentence goes only when its content survives elsewhere) removes materially fewer than the roughly 11,000 words the goal targets, is the shortfall reported and accepted as the honest result, or are further cuts sought? The cut rule, not the count, is the stated constraint, so the count&apos;s role at verification time should be pinned.</question>
  <alternative id="Report the shortfall">
    The roughly 11,000-word figure is a non-binding estimate: the sweep applies the three cut classes under the cut rule, the actual removal is measured with `wc -w` over the three directories and reported (per class and in total) alongside the per-file constraint-preservation ledgers, and whatever number results is the honest outcome — a shortfall is never a trigger for additional cuts.
    <advantage>It keeps the goal&apos;s own stated hierarchy intact — the cut rule is the constraint and the count is a target — so no edit is ever made because a number was missed, which is the only way the sweep stays behavior-neutral by construction.</advantage>
    <drawback>Nothing in the count itself distinguishes &quot;the rule genuinely yields less&quot; from &quot;the sweep was applied incompletely&quot;, so a large shortfall leans entirely on the fresh-context re-audit loop to catch a timid pass.</drawback>
  </alternative>
  <alternative id="Shortfall triggers a completeness re-check">
    A materially short measured total triggers one bounded re-pass over the layer that re-applies the same three cut classes under the same unchanged cut rule to confirm nothing in scope was missed; whatever survives that re-check is then reported and accepted, with no new cut class and no relaxed rule.
    <advantage>It separates a genuine low yield from an incomplete sweep without loosening the deletion rule by a single clause.</advantage>
    <drawback>It adds a conditional verification pass that largely duplicates the already-decided fresh-context re-audit loop, and putting a numeric trigger on it quietly re-introduces the count as a forcing function on the editor.</drawback>
  </alternative>
  <alternative id="Cut until the target is met">
    The roughly 11,000 words is treated as a floor: if the three classes under the cut rule fall short, further cuts are sought beyond those classes (or the survives-elsewhere rule is relaxed) until the count is reached.
    <advantage>The milestone delivers the headline number its goal states, so the stated objective is met exactly as written.</advantage>
    <drawback>It inverts the goal&apos;s own constraint — the count becomes binding and the cut rule negotiable — which licenses removing point-of-use constraints, worked examples, or templates whose content survives nowhere, making the sweep no longer behavior-neutral.</drawback>
  </alternative>
  <recommendation option="Report the shortfall">The goal names the cut rule as the constraint and the count only as a rough target, so the measured removal is reported, never enforced; sweep completeness is already owned by the fresh-context re-audit loop and its findings ledger, which is where a timid pass should surface rather than in a word-count trigger that would pressure edits the cut rule does not license.</recommendation>
</open-question>
