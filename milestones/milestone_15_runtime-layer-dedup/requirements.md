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

### Verification

The fresh-context re-audit audits but never fixes. Its findings become follow-up fix tasks, and a further fresh-context re-audit over the whole runtime layer is queued after those fixes, repeating until a run returns a clean verdict — the audited final state of the files, not the pre-fix state, is what proves the milestone.

Any finding the planned fix tasks do not address is recorded in `temp/milestone_15_findings.md` together with the reason it was not fixed. The loop terminates when a re-audit returns no findings other than those already recorded there: a finding is either fixed, or registered with a stated reason, and there is no third state in which one is silently tolerated.

## Out of Scope

## Open questions

<open-question id="Reporting-step trim depth" status="open">
  <question>Every committing skill&apos;s final step carries the terse-reporting convention in full: the fixed line to print, the list of things not to add, the sentence that the committed diff and git log are the durable record, and the distinct no-op line with its rationale. The CLAUDE.md terse-reporting invariant says the convention is authored inline in each SKILL.md&apos;s final step because there is deliberately no shared report procedure. How far may this milestone trim those steps: down to the bare print instructions (the success line and the no-op line) with all rationale moved to the invariant, or must the fuller convention text stay inline in each file as that invariant currently implies?</question>
  <alternative id="Bare print instructions">
    Trim every reporting step down to the fixed success line, the no-op line, and any file-specific git-absent advisory, relocating the prohibition list and all rationale into the CLAUDE.md terse-reporting invariant.
    <advantage>Largest saving of the four across the roughly fifteen skills carrying the convention (their reporting steps total well over 1,500 words), and leaves exactly one home for the convention instead of fifteen paraphrases.</advantage>
    <drawback>It strips the &quot;and nothing more / no identifier / no next-step pointer&quot; prohibitions, which are the only run-time instruction resisting a model&apos;s default urge to narrate what it just did; a consuming project never loads CLAUDE.md, so the relocated text is invisible where the skill actually executes and the layer&apos;s most drift-prone convention loses its guardrail.</drawback>
  </alternative>
  <alternative id="Cut rationale, keep prohibitions">
    Cut only the justification sentences — that the committed diff and git log are the durable record, and that git holds no durable record of a no-op — whose content the CLAUDE.md invariant already carries, while keeping inline the fixed line string, the file-specific list of what must not be printed, the no-op branch with its per-file trigger, and any git-absent advisory that step owns.
    <advantage>Removes precisely the class the Goal defines as cuttable (rationale whose content survives in a CLAUDE.md invariant) while every imperative that actually shapes the printed output stays at its point of use, which the Goal explicitly protects.</advantage>
    <drawback>Saves less than a full trim and still leaves a per-file instantiation of the convention in every committing skill, so each edit needs a judgment call about where the prohibition ends and the justification begins.</drawback>
  </alternative>
  <alternative id="Leave reporting steps untouched">
    Treat the whole reporting step as point-of-use instruction and exclude it from this milestone&apos;s sweep entirely.
    <advantage>Zero behavior risk on the convention most likely to regress, and no per-file judgment calls to get wrong.</advantage>
    <drawback>Forfeits several hundred words that demonstrably survive in the CLAUDE.md invariant, contradicting the milestone&apos;s own stated cut criterion out of caution rather than evidence.</drawback>
  </alternative>
  <alternative id="Shared report procedure">
    Extract the convention into a new `shared/report-procedure.md` referenced by each committing skill, as 26 files already reference the other shared procedures.
    <advantage>Deduplicates the convention structurally rather than by trimming, so it is stated once and still reaches every runner at run time, including in consuming projects.</advantage>
    <drawback>Contradicts the standing CLAUDE.md invariant that there is deliberately no such file, reopens an architectural decision this milestone did not scope, and buys little — each skill gains a reference sentence while the per-run read reintroduces most of the words.</drawback>
  </alternative>
  <recommendation option="Cut rationale, keep prohibitions">The justification sentences are the only part whose content already lives in the CLAUDE.md invariant and therefore the only part the Goal licenses cutting, whereas the &quot;and nothing more&quot; prohibitions are point-of-use constraints the Goal protects and that a consuming project could never recover, since it never loads CLAUDE.md.</recommendation>
</open-question>

<open-question id="Invariants section growth" status="open">
  <question>Moving rationale out of runtime files into CLAUDE.md will grow the Invariants section, already 35 bullets and about 4,839 words, and several of those bullets already restate each other. Does this milestone only append or extend the matching invariant when moving rationale in (leaving the section&apos;s existing shape alone), or does it also consolidate the Invariants section itself so CLAUDE.md does not become the new duplication sink?</question>
  <alternative id="Append only">
    Move each piece of runtime-file rationale into the matching CLAUDE.md invariant by extending that bullet or appending a new one, and leave the Invariants section&apos;s existing shape, ordering, and cross-bullet overlap exactly as they are.
    <advantage>Keeps the milestone&apos;s blast radius entirely on the runtime layer, where the ~11,000-word target, the per-file constraint-preservation check, and the fresh-context re-audit all live, and costs plugin consumers nothing since CLAUDE.md never loads outside this repository.</advantage>
    <drawback>Ships exactly the duplication the milestone exists to remove, merely relocated: a 35-bullet, 4,841-word section that is already 76% of CLAUDE.md and already restates itself across the answer/recommend cluster grows further, so the next session in this repo pays the cost the runtime layer stopped paying.</drawback>
  </alternative>
  <alternative id="Consolidate inline">
    Treat consolidation as part of each move: whenever rationale lands in an invariant, also merge or rewrite the neighbouring bullets it overlaps, so the section is de-duplicated continuously as the sweep proceeds.
    <advantage>Each invariant is touched exactly once, needs no extra task, and the person merging has the runtime file&apos;s original wording in hand at the moment of the merge.</advantage>
    <drawback>Makes the sweep&apos;s own reference target move underneath it — every cut is justified by &quot;this survives in a CLAUDE.md invariant&quot;, so rewriting those invariants mid-sweep means earlier cuts point at bullets that no longer read as they did when the cut was justified, and both the per-file check and the re-audit must chase a mutating target.</drawback>
  </alternative>
  <alternative id="Consolidate in a final pass">
    Run the runtime-layer sweep append-or-extend only, against a frozen Invariants section, then close the milestone with one dedicated consolidation task that rewrites the whole section — merging the overlapping bullets and absorbing the newly moved rationale — before the fresh-context re-audit.
    <advantage>Gets both properties: the sweep runs against a stable, additive-only reference target, and the section is consolidated once with the full post-move content visible, so merges are made against what the invariants actually say at the end rather than guessed at mid-flight.</advantage>
    <drawback>Adds a task and a second editing regime, and because that pass rewrites bullets the just-completed cuts depend on, it must carry its own constraint-preservation check over CLAUDE.md rather than inheriting the runtime layer&apos;s.</drawback>
  </alternative>
  <applied-principle>Mutate live machinery last</applied-principle>
  <recommendation option="Consolidate in a final pass">The Invariants section is the reference every cut in this sweep is justified against, so it must stay frozen while the sweep runs and be consolidated once afterwards — which de-duplicates CLAUDE.md without the milestone&apos;s own verification chasing a moving target.</recommendation>
</open-question>

<open-question id="Antigravity shared-procedure gap" status="open">
  <question>The transpile script that regenerates the Antigravity tree copies skills and agents but not the shared directory, and leaves the CLAUDE_PLUGIN_ROOT references verbatim, so the generated skills point at procedure files that do not exist in that tree. This gap predates the milestone. Is fixing it (copying shared into the generated tree, or rewriting the references) in scope, or does the milestone only regenerate the tree as-is and record the gap as out of scope?</question>
  <alternative id="Out of scope, recorded">
    Regenerate the Antigravity tree exactly as the current script produces it, and record the missing-shared gap under &quot;## Out of Scope&quot; (optionally as a follow-up milestone item) without touching scripts/migrate_skills_to_agy.py.
    <advantage>Keeps a prose-dedup milestone entirely inside the Markdown runtime layer, changing no tooling and adding no verification burden the repository (no build, no tests) is equipped to carry.</advantage>
    <drawback>The sweep&apos;s own deletion rule permits cutting a sentence when its content &quot;survives in a referenced shared procedure&quot; — a premise that is false in the generated tree, so this milestone knowingly makes the Antigravity output materially worse than the tree it regenerates.</drawback>
  </alternative>
  <alternative id="Copy shared into tree">
    Add a shared/ copy to the transpile script mirroring the existing wholesale agents/ copytree, regenerate, and leave the ${CLAUDE_PLUGIN_ROOT} reference text untouched in both trees.
    <advantage>A roughly four-line change in the same shape as code already in the script makes every referenced procedure file actually present in the generated tree, restoring the &quot;content survives in the shared procedure&quot; premise the dedup depends on, and it is verifiable here by inspecting the regenerated file list.</advantage>
    <drawback>It fixes only file presence, not path resolution: if Antigravity does not expand ${CLAUDE_PLUGIN_ROOT}, the tree still cannot load the procedures, so the gap may be closed only halfway while looking closed.</drawback>
  </alternative>
  <alternative id="Copy and rewrite references">
    Copy shared/ into the generated tree and additionally rewrite each ${CLAUDE_PLUGIN_ROOT}/shared/&lt;name&gt;.md reference in the 22 generated skill and agent files to a path the Antigravity tree resolves.
    <advantage>The only option that produces an end-to-end loadable Antigravity plugin, closing a pre-existing defect completely rather than partially.</advantage>
    <drawback>It introduces a generated-vs-source content divergence and a text transform whose correctness cannot be verified in this repository — there is no Antigravity runtime, no test, and no known-good target path — turning a Markdown milestone into unverifiable tooling work.</drawback>
  </alternative>
  <recommendation option="Copy shared into tree">Fixing is in scope but only to the extent this milestone can prove correct: the sweep deletes prose on the grounds that it survives in a referenced shared procedure, so shipping a regenerated tree whose procedures are absent would undercut the milestone&apos;s own deletion rule, while copying shared/ is a small change in the shape of the script&apos;s existing agents/ copy and is checkable by inspection — the unverifiable reference rewrite stays out of scope and is recorded as a follow-up.</recommendation>
</open-question>

<open-question id="Constraint-check record form" status="deferred">
  <question>The per-file constraint-preservation check must show that every imperative in a file&apos;s original text survives at its point of use, in a referenced shared procedure, or in a CLAUDE.md invariant. Where does the evidence of that check land: only as Verified bullets in the TASKS_DONE entry of the task that edited the file, or as a committed checklist artifact under the milestone directory that the re-audit can read?</question>
  <alternative id="Verified bullets only">
    The constraint-preservation evidence lands solely as the completer&apos;s derived `**Verified:**` bullets in the TASKS_DONE.md entry of the task that edited each file, in whatever shape the completer derives from the task description plus requirements.md.
    <advantage>Adds nothing to the pipeline — it reuses the one evidence channel `shared/complete-procedure.md` already writes and later milestones already read, so there is no new artifact, no new writer, and no risk of a record drifting from the files it describes.</advantage>
    <drawback>Leaves the shape unpinned: a completer may satisfy it with a single coarse bullet asserting that all constraints survived, which proves nothing a fresh-context re-audit could check imperative by imperative.</drawback>
  </alternative>
  <alternative id="Verified bullets as constraint ledger">
    Same channel and same file, but the milestone pins the shape: each edited file&apos;s TASKS_DONE.md entry carries the constraint check as an explicit ledger — one bullet per imperative removed or relocated, naming where it now survives (its point of use in the same file, the referenced shared procedure, or the CLAUDE.md invariant).
    <advantage>Gives the re-audit a checkable per-imperative claim to verify against the live file while staying inside the existing three-file milestone structure and the existing `**Verified:**` label, with git history supplying the original text the ledger is a claim about.</advantage>
    <drawback>Makes some TASKS_DONE.md entries long for the heavily-edited hot files, and depends on the editing task&apos;s description pinning the ledger shape since the completer otherwise derives the bar freely.</drawback>
  </alternative>
  <alternative id="Committed checklist artifact">
    A separate committed file under the milestone directory (e.g. a per-file constraint checklist) collects every imperative and its surviving destination across the whole sweep, and the fresh-context re-audit reads that file.
    <advantage>Concentrates the whole sweep&apos;s preservation evidence in one place, readable end-to-end without walking every TASKS_DONE.md entry, and survives as a standalone audit trail.</advantage>
    <drawback>Introduces a fourth file into a milestone directory that CLAUDE.md says contains exactly three, with no skill that writes, updates, or reads it — so it is hand-maintained and free to drift — and feeding the sweep&apos;s own record to the re-audit works against the independence milestone 12 established by giving its auditor only the criteria and the file set.</drawback>
  </alternative>
  <recommendation option="Verified bullets as constraint ledger">Keep the evidence in the pipeline&apos;s own `**Verified:**` channel rather than inventing an unowned fourth milestone file, but pin it to one bullet per relocated imperative naming its destination, so the re-audit has a claim it can check against the live file and git-recoverable original instead of a bare assertion.</recommendation>
</open-question>

<open-question id="README sync scope" status="deferred">
  <question>README.md never mentions the Rules sections, but its skill reference and workflow prose describe each skill and the referenced-never-restated doctrine. Does this milestone touch README.md at all, and if so only where the sweep falsifies an existing claim, or does it also add a sentence describing the new runtime-files-never-restate-invariants rule?</question>
  <alternative id="README untouched">
    Declare README.md entirely out of scope for this milestone, on the grounds that the sweep is behavior-neutral by construction, and leave every existing claim as it stands.
    <advantage>Zero cost and zero churn in a user-facing document that a behavior-neutral prose sweep has no reason to invalidate.</advantage>
    <drawback>It assumes rather than checks: README&apos;s skill-reference entries already narrate internals (which shared procedure owns which mechanics, which sub-elements the recommend subagent returns, what a file&apos;s sections contain), so a sweep edit could silently falsify one with nobody looking.</drawback>
  </alternative>
  <alternative id="Falsification-only sync">
    Touch README.md only where a sweep edit makes an existing claim false — a verification pass over the skill reference and workflow prose that edits solely on a confirmed falsification and adds no new prose.
    <advantage>Keeps the public document truthful with the smallest possible blast radius, and covers the one real risk — README describes runtime internals per skill — without importing a contributor-only authoring convention into a document written for plugin users.</advantage>
    <drawback>Spends a verification pass whose expected outcome is no edit at all, and leaves the new never-restate-invariants rule documented nowhere a contributor reading only README would find it.</drawback>
  </alternative>
  <alternative id="Sync plus doctrine sentence">
    Do the falsification sync and additionally add a sentence to README describing the new runtime-files-never-restate-invariants rule, alongside the existing How-skills-commit convention prose.
    <advantage>Makes the authoring rule discoverable to a contributor who reads only README, giving the milestone&apos;s central doctrine a public statement rather than a repository-internal one.</advantage>
    <drawback>Restates an editor-facing invariant in a third place — precisely the class of duplication this milestone exists to remove — inside a user-facing document whose readers never author runtime files, and creates a new sentence that must itself be kept in sync with the CLAUDE.md invariant.</drawback>
  </alternative>
  <recommendation option="Falsification-only sync">The sweep is behavior-neutral, so the only honest README work is confirming no existing claim went stale; the never-restate rule is an authoring convention whose single home is the CLAUDE.md invariant, and repeating it in a user-facing README would recreate the very duplication this milestone removes.</recommendation>
</open-question>
