# Milestone 7: Answer Open Questions With Recommendation

## Goal

Extract recommendation-recording out of `/answer-open-question` (which reverts to literal-answer only) into a dedicated `/answer-open-question-with-recommendation` SKILL + AGENT pair that lifts a question's embedded recommendation and records it (fold into Decisions, cascade to mooted siblings). Add a `/answer-all-open-questions-with-recommendation` orchestrator that sweeps every open question carrying an embedded recommendation and dispatches the file-editing agent strictly sequentially — one commit per answer — so the per-question work stays out of the orchestrator's context. This deliberately diverges from the read-only-subagent design of `/try-answer-all-questions-by-principle`, isolating the mutation (not reasoning, which is pre-computed) into the agent, and is documented as such.

## Relevant starting state

### `answer-open-question` skill (source of the extraction)

Lives at `skills/answer-open-question/SKILL.md`. Today it carries **two** modes behind one `/answer-open-question <Short Title>. <answer text>` entry, splitting args on the **first `.`** (title before, answer after):

- **Literal-answer path** — the parsed answer text is recorded verbatim.
- **Record-recommendation mode** (the logic this milestone extracts) — selected by the reserved sentinel answer text `record the recommendation`, matched as an **exact whole-string** comparison after trim+lowercase (never a substring). In that mode (step 2) the skill resolves `<MILESTONE_DIR>`, locates the question's contiguous `>`-blockquote run, and lifts the `> **Recommendation:** <chosen option> — <rationale>` anchor content (stripping the `>` and `**Recommendation:**` label) as the `ANSWER`. A **no-embedded-recommendation guard** stops without changes and commits nothing when the block has no anchor or no block matches.

Both modes then hand off to `shared/answer-procedure.md` (step 3) and **commit** (step 4): subject `Manual-answer: <Short Title>`, rationale in the body, path-scoped `git add <MILESTONE_DIR>/requirements.md`, and **no** `Answer-Principle:` trailer. This commit-from-a-single-skill is a deliberate, documented exception to the "individual skills never commit" rule.

### `shared/answer-procedure.md` (the recording core, reused as-is)

The single source of truth for recording one answer, at `shared/answer-procedure.md`. **Execution-neutral**: it takes a resolved `SHORT TITLE` + `ANSWER` and performs locate → analyse → **remove the entire contiguous `>` run** (header plus any embedded recommendation sub-block) → fold the decision into `## Decisions` as clean prose → **cascade** to mooted sibling entries. It says nothing about arg-parsing, committing, or follow-up — the wrappers own those. On a Short-Title mismatch it stops without changes. This milestone's new skill/agent will lift the recommendation and then delegate here unchanged; the cascade step is exactly why the new sweep must serialize mutation.

### Embedded recommendation format (what gets lifted)

Produced by the recommend sweep — orchestrator `skills/recommend-all-open-questions/SKILL.md` plus its read-only subagent `agents/recommend-open-question.md`. It embeds, beneath each unchanged one-line question header, a contiguous `>` sub-block ending in the stable anchor line `> **Recommendation:** <chosen option> — <one-line rationale>`. That anchor is the exact handle this milestone's skill/agent lifts as the answer, so a question is only answerable-with-recommendation once the recommend sweep has annotated it. The recommend sweep is **mutate-but-do-not-commit** and requires no clean tree (it records no decisions, triggers no cascades).

### `try-answer-all-questions-by-principle` + subagent (the design to mirror and diverge from)

Orchestrator `skills/try-answer-all-questions-by-principle/SKILL.md` with read-only subagent `agents/try-answer-question-by-principle.md`. This is the closest structural precedent for the new sweep, and the milestone deliberately diverges from it on one axis. Its shape:

- **Clean-tree precondition** (`git status --porcelain` must be empty) so "one commit = one auto-answer" holds; captures `BASE=$(git rev-parse HEAD)` for the end report.
- **Gather once, order loosely most-significant → least** (a cascade-parent-first proxy), then walk **exactly once** — no outer re-gather loop.
- **Per-question live re-check + skip**: re-reads `requirements.md` before each question because a prior answer's cascade may have removed it.
- **Orchestrator owns ALL mutation and the commit; the subagent is read-only** and returns a verdict only — *"cascades plus one-commit-per-answer require all mutation serialized in the single sequential orchestrator."* This milestone reverses that one choice: it isolates the **mutation** into a file-editing agent (there is no reasoning to isolate, since the recommendation is pre-computed), while keeping strictly-sequential dispatch and graceful skip-on-already-cascaded.
- Commits per answer: subject `Principle-based-answer: <Short Title>`, one repeated `Answer-Principle: <Short Title>` trailer per load-bearing principle.

### SKILL + AGENT wrapper pattern (the model for the new pair)

Cairn already ships two skill+agent pairs — `complete-task` (`skills/complete-task/SKILL.md` + `agents/complete-task.md`, over `shared/complete-procedure.md`) and `submit-task` (over `shared/submit-procedure.md`). The established convention: a single **execution-neutral shared procedure** referenced via `${CLAUDE_PLUGIN_ROOT}` by both wrappers; the **skill runs it inline** in the user's conversation (context survives for follow-up, never spawns the agent, leaves changes staged); the **agent runs it in an isolated context** and adds the `DONE` / `FAILED: <reason>` return protocol, with committing left to the orchestrator. Both carry `model: opus` frontmatter. The only difference between skill and agent is *where* the procedure runs. The new `answer-open-question-with-recommendation` pair follows this pattern, but its agent additionally **mutates** `requirements.md` (the divergence noted above).

### Milestone resolution and pointer

`shared/get-current-milestone.md` is the single resolver for `<MILESTONE_DIR>`, read from the `Current milestone:` line in `milestones/README.md`. Every skill/agent that touches the current milestone follows it rather than hardcoding a path; the new skill, agent, and orchestrator must do the same.

### Documentation surfaces to sync (known scope)

`CLAUDE.md` (the repository-layout listing, the skills-and-workflow pipeline block, and the detailed **Invariants to preserve** list) and `README.md` (skill reference plus the per-phase Mermaid workflow diagrams, notably the requirements-loop phase) both document the answer/recommend skills in full. Adding one skill+agent pair and one orchestrator, and narrowing `answer-open-question` to literal-only, will require synchronized edits across both — including a **new invariant** documenting the deliberate file-editing-agent divergence so it is not later "fixed" toward the read-only-subagent norm.

## Decisions

### Sweep commit ownership

In `/answer-all-open-questions-with-recommendation`, the file-editing agent commits its own answer: it stages **path-scoped** (`git add <MILESTONE_DIR>/requirements.md`, never `git add -A`) and makes its own commit, returning only `DONE`/`FAILED` to the orchestrator. The orchestrator purely dispatches and sequences — it never commits. The agent owns the "one commit = one answer" guarantee: path-scoped staging so a dirty working tree cannot contaminate its commit, and no partial commit on `FAILED` (its failure path leaves the tree as it found it). This is a **second** deliberate divergence from Cairn's "individual skills/agents never commit" norm — layered on top of the milestone's intended mutation-in-agent divergence — and must be documented with its own invariant so it is not later "fixed" back toward `complete-task`'s "committing is the orchestrator's job."

### Recommendation-answer commit subject

Recommendation-derived answers — from both the single-question `/answer-open-question-with-recommendation` skill and the `/answer-all-open-questions-with-recommendation` sweep agent — commit under the distinct subject `Recommendation-answer: <Short Title>`, which matches neither the `^Manual-answer:` nor the `Principle-based-answer:` grep, so finish-time `/capture-milestone-principle-updates` never harvests them. The rationale: the harvestable artifact is the commit body, and for a recommendation-answer that body is the `recommend-open-question` agent's rationale (batch-accepted on the sweep path), not user-deliberated reasoning; keeping these outside both capture greps preserves the principle store's provenance with no change to capture's grep logic. This distinct subject is the honest git-log discriminator, matching the house style where the subject/trailer *is* the provenance marker.

### Standalone skill commit

The single-question `/answer-open-question-with-recommendation` **skill** commits inline: it records the recommendation-derived answer (fold into `## Decisions`, cascade to mooted siblings) and then commits its own path-scoped `requirements.md` edit (`git add <MILESTONE_DIR>/requirements.md`, never `git add -A`), mirroring `answer-open-question`, the committing mode it is extracted from — under the `Recommendation-answer: <Short Title>` subject fixed above. The commit-vs-stage line tracks what a skill *produces*, not whether it has an isolated-agent twin: decision-recorders commit their decision atomically with a greppable subject, while work-producers (`complete-task`/`submit-task`) leave changes staged. This standalone skill records a decision, so it joins the committing category rather than the staging one, widening the "individual skills never commit" exception from one skill to two — a deliberate, documented broadening (not a proliferating ad-hoc exception list).

### Sweep cascade ordering

The `/answer-all-open-questions-with-recommendation` orchestrator adopts both of the principle sweep's mechanisms. It gathers questions once in most-significant-first order (a cascade-parent-first proxy), and before dispatching each question's file-editing agent it re-reads `requirements.md` and skips the question when a prior answer's cascade has already removed its block. The agent's `shared/answer-procedure.md` step-2 stop-on-missing-block stays as a backstop. The rationale: a file-editing dispatch is expensive, so the cheap orchestrator-side re-read/skip earns its keep by avoiding whole agent spin-ups on already-mooted blocks, and most-significant-first ordering is what makes that gate actually fire (parent answered first → dependent's block already gone).

### Lift-procedure placement

The "lift the embedded `> **Recommendation:**` anchor, then delegate to `shared/answer-procedure.md`" logic lives in a **new execution-neutral shared procedure `shared/answer-with-recommendation-procedure.md`**, referenced via `${CLAUDE_PLUGIN_ROOT}` by both the `/answer-open-question-with-recommendation` skill and its agent. That shared file takes SHORT TITLE, locates the question's blockquote run, lifts and strips the `> **Recommendation:**` anchor (with the no-anchor guard), then delegates to `shared/answer-procedure.md` with the derived ANSWER. This is the only option that both satisfies the one-place DRY invariant and preserves `answer-procedure.md`'s execution-neutrality; the tie-breaker is that neutral core's ANSWER-as-input contract, shared with literal `answer-open-question` and the principle sweep, which must never inherit lift behavior — so the lift belongs in its own execution-neutral procedure that composes over the recording core, exactly as `complete-task`/`submit-task` layer their shared procedures.

## Open questions

> **Deferred — answer-open-question redirect:** After the record-recommendation mode and its `record the recommendation` sentinel are removed from `answer-open-question`, decide whether that skill points users to the new `/answer-open-question-with-recommendation` or simply drops the mode with no pointer.
>
> **Alternatives:**
> - **Brief pointer line in `answer-open-question`** — add a documentation sentence in the skill's intro/Rules naming `/answer-open-question-with-recommendation` as the new home of the removed mode. *Advantage:* aids migration discovery with minimal effort and no runtime logic. *Drawback:* it is passive docs a muscle-memory user typing the old `<Title>. record the recommendation` form never reads, so it does not stop that phrase from being recorded literally and committed as the decision; it also adds cross-skill coupling to a skill that no longer does the thing.
> - **Clean drop, no pointer** — remove the sentinel intro, step 2, Example, and Rules entirely, relying on the recommend sweep's step-6 pointer and the README/CLAUDE.md edits (already being updated to name the new skill) for discovery. *Advantage:* zero coupling and the smallest, cleanest skill, fully honoring the literal-only revert. *Drawback:* a user typing the old sentinel form gets `record the recommendation` silently recorded as their answer and committed under `Manual-answer:` (even feeding finish-time principle capture) — a real, silent wrong-answer trap for exactly the migrating users the question worries about.
> - **Recognize the sentinel only to emit a redirect** — keep a small guard: when the answer text is exactly the old sentinel, stop without recording and print "this moved to `/answer-open-question-with-recommendation`." *Advantage:* intercepts the muscle-memory command at the exact moment of the trap — preventing the silent literal record + bad commit — while its message also serves discovery; it fits the skill's existing clean-stop-and-point pattern (no-anchor guard, Short-Title mismatch). *Drawback:* retains a sliver of sentinel-awareness in a skill meant to become literal-only, a small ongoing maintenance surface.
>
> **Recommendation:** Recognize the sentinel only to emit a redirect — it uniquely prevents a migrating user's old `<Title>. record the recommendation` command from silently recording the sentinel phrase as a committed decision, and its redirect message subsumes the passive pointer's discovery value; the recommend sweep's step-6 pointer plus README/CLAUDE.md remain the primary discovery path, so this guard is targeted migration scaffolding, not a revived feature.

## Out of Scope

