# TASKS TODO

## Make Recommend Procedure Principle-Aware

Upgrade the execution-neutral analytical core `shared/recommend-procedure.md` so the shared recommendation logic consults the project-wide answering principles, per the milestone's "Recommendation machinery" decision. Both wrappers — the `discuss-open-question` skill (inline) and the read-only `recommend-open-question` agent — inherit this through the shared core, so the store read must live here once and never be duplicated into the wrappers.

**Provides:**
- `shared/recommend-procedure.md`'s grounding step reads the fixed project-wide principle store `milestones/answer_decision_principles.md` directly and in place (naming that path itself, not taking principles as a caller-supplied input alongside QUESTION) as part of grounding.
- The core states, in execution-neutral prose, the requirement that any confirmed principle which influenced the recommended pick be cited — the logical contract the `recommend-open-question` agent renders as its `> **Applied principle:**` line in a separate downstream task.

**Notes:**
- A bearing confirmed principle is a **weighted advisory factor**, not a binding filter: it is a strong default in favor of its supported option, but merit MAY override it — only for a specific stated reason that must be named in the recommendation. It must never veto a candidate outright.
- When no confirmed principle bears on the question, recommendations are produced exactly as today — the existing alternatives/recommendation contract is otherwise unchanged.
- Keep the file execution-neutral: state the citation requirement logically only. Own **no** `>`-blockquote markup and do **not** specify the `> **Applied principle:**` line rendering — that belongs to the `recommend-open-question` agent (a separate task). Do not duplicate the store read into either wrapper.
- The store is a fixed milestone-independent path above any milestone, so reading it in place preserves the only caller-owned path-freedom that matters (`<MILESTONE_DIR>` resolution), which is unaffected.

**Success:**
- `shared/recommend-procedure.md`'s grounding step names and reads `milestones/answer_decision_principles.md`.
- The procedure describes a bearing principle as a weighted advisory default (strong default with merit-override only for a named reason), requires citing any principle that influenced the pick, and states that behavior is unchanged from today when no principle bears.
- The file contains no `>`-blockquote markup and does not restate the agent's `> **Applied principle:**` line rendering.
- The alternatives (2–4, what-it-is / advantage / drawback) and single-recommendation-with-tie-break contract is otherwise unchanged, and the store read appears only in this file (not duplicated into the two wrappers).

---

## Render Applied-Principle Citation In Sub-block

Add applied-principle citation rendering to the read-only `recommend-open-question` agent, per the milestone's "Recommendation machinery" decision. Now that the shared core `shared/recommend-procedure.md` is principle-aware and surfaces which confirmed principles bore on the recommended pick, the agent — which owns the `>`-blockquote rendering the core deliberately leaves out — must render each bearing principle as its own citation line in the returned sub-block.

**Provides:**
- The `recommend-open-question` agent's rendered sub-block shape includes zero-or-more `> **Applied principle:** <Short Title>` lines — one per bearing confirmed principle — stacked immediately above the single `> **Recommendation:** <chosen option> — <rationale>` anchor, which remains the final line of the contiguous `>` run.

**Notes:**
- The anchor MUST stay the last line of the run: `/answer-open-question-with-recommendation` lifts only that anchor line verbatim, so keeping the citation above it keeps the applied-principle text out of the recorded `## Decisions` prose by construction.
- One `> **Applied principle:** <Short Title>` line per bearing principle — with multiple principles the lines stack, each atomic and independently greppable. No new label, no in-line list syntax; multi-principle is pure repetition of the single-line form.
- Never bake the citation into the anchor rationale — it is always a separate line above the anchor.
- When no principle bears, the sub-block renders exactly as today, with no `> **Applied principle:**` line at all.
- Preserve the existing rendering discipline unchanged: every internal gap is an empty `>` line (never a bare blank line) so the entry stays one contiguous `>` run with the header greppable on line 1, and the return protocol is unchanged (final message is the sub-block only, header excluded). The agent still owns only this rendering — it must not restate the shared core's analytical logic.

**Success:**
- The agent's documented sub-block shape shows zero-or-more `> **Applied principle:** <Short Title>` lines immediately above the `> **Recommendation:** …` anchor, with that anchor still the final line of the run.
- The multi-principle case is one `> **Applied principle:**` line per bearing principle (no in-line list, no new label), and the no-bearing-principle case renders identically to today (no `> **Applied principle:**` line).
- The empty-`>` internal-separation rule, the greppable-header-on-line-1 rule, and the "final message is the sub-block only (header excluded)" return protocol are all preserved.
- The file does not restate the shared core's analytical logic — it adds only the applied-principle line rendering to the existing `>`-blockquote sub-block.

---

## Scrub Retired Sweep Vocabulary From Workflow-Logic Files

Remove every now-dead reference to the deleted auto-answer sweep and its `Principle-based-answer:` / `Answer-Principle:` provenance vocabulary from the plugin's live skill/agent/shared-procedure layer, per the milestone's "Manual-vs-sweep discriminator scrub" decision and its "Retired-vocabulary blast radius" starting-state note. This is a reference/vocabulary scrub only — each touched file must keep its real semantics; nothing changes but the dead cross-references. Scope is exactly `skills/`, `agents/`, and `shared/`; do **not** touch `CLAUDE.md`, `README.md`, `milestones/answer_decision_principles.md`, or any past-milestone document (those are separate tasks / immutable history).

**Notes:**
- Per-file intent (preserve all surrounding semantics):
  - `skills/answer-open-question/SKILL.md`: DROP the manual-vs-sweep discriminator note entirely (do not repoint it) — delete the orphaned sentence(s) documenting the *absence* of an `Answer-Principle:` trailer as the manual-vs-sweep discriminator, including their sweep-mirroring clauses (e.g. the `Manual-answer:` subject "mirroring the sweep's `Principle-based-answer:`" phrasing), with no replacement. The literal-answer path, first-`.` split, the retired `record the recommendation` redirect guard, and the `Manual-answer:` commit rules stay UNCHANGED; the `Manual-answer:` subject and its `git log --grep='^Manual-answer: '` collectability must still read correctly without naming the sweep.
  - `skills/capture-milestone-principle-updates/SKILL.md`: remove the now-vacuous `Answer-Principle:`-trailer exclusion clause on its `git log --grep='^Manual-answer: '` walk (nothing emits that trailer anymore), and repoint/remove its step-5 report line that points captured principles at `/try-answer-all-questions-by-principle`. Its manual-answer→principle learning input and sole-writer role stay untouched.
  - `skills/answer-open-question-with-recommendation/SKILL.md` and `agents/answer-open-question-with-recommendation.md`: rewrite the `Recommendation-answer:` subject's contrast framing (currently defined against BOTH `^Manual-answer:` and `Principle-based-answer:`) so it no longer names the deleted sweep's vocabulary, while keeping the distinct `Recommendation-answer: <Short Title>` subject and its finish-time-capture-never-harvests rationale intact.
  - `shared/answer-procedure.md`: remove/repoint the `try-answer-all-questions-by-principle`-named reference so the execution-neutral core no longer names the deleted sweep (its "run by an orchestrator" framing can survive without the dead name).
  - `skills/answer-all-open-questions-with-recommendation/SKILL.md`: remove/repoint the `try-answer`-named references to the deleted sweep (the "deliberate divergence" and "commit ownership" comparisons must stand on their own or against a surviving sibling).
  - `skills/recommend-all-open-questions/SKILL.md`: rewrite the repeated "argument-free twin of `/try-answer-all-questions-by-principle`" comparison anchors so the skill is described on its own terms (or against a surviving sibling) without referencing the deleted sweep — preserving its real behavior description (mutate-but-do-not-commit, idempotent, argument-free, path-scoped staging).
- This task runs *after* the sweep-file deletion task, so the two deleted files (`skills/try-answer-all-questions-by-principle/`, `agents/try-answer-question-by-principle.md`) already do not exist — every surviving reference to them is dead and must go.
- Behavior is preserved everywhere: no commit subject, grep pattern, procedure step, or return protocol changes beyond the reference removal.

**Success:**
- `grep -rn 'try-answer\|Answer-Principle\|Principle-based-answer' skills/ agents/ shared/` returns no live reference to the deleted sweep or its provenance vocabulary.
- In `skills/answer-open-question/SKILL.md` the manual-vs-sweep discriminator sentence(s) are gone with no replacement, and the rest of the skill (literal-answer path, first-`.` split, `record the recommendation` redirect guard, `Manual-answer:` commit rules) is unchanged.
- In `skills/capture-milestone-principle-updates/SKILL.md` the `Answer-Principle:` exclusion clause and the `/try-answer-all-questions-by-principle` step-5 pointer are both gone, and its `git log --grep='^Manual-answer: '` learning input and sole-writer role are intact.
- The `Recommendation-answer: <Short Title>` subject and its capture-never-harvests rationale survive in both `skills/answer-open-question-with-recommendation/SKILL.md` and `agents/answer-open-question-with-recommendation.md` without naming `^Manual-answer:` or `Principle-based-answer:` as the contrast.
- No behavior described in any touched file is altered beyond the reference removal, and no file outside `skills/`, `agents/`, `shared/` is modified.

---

## Repoint Principle-Store Header To Advisor Model

Rewrite the header prose of the project-wide principle store `milestones/answer_decision_principles.md` — the intro lines above the first `### <Short Title>` entry — so it names the recommendation advisor as the consumer instead of the deleted auto-answer sweep, per the milestone goal ("The principle store's data and format are unchanged — only its consumer pointer moves" / "sync … the principle-store header to the new model"). The header currently says each principle is a keep/eliminate directive that `try-answer-all-questions-by-principle` applies to the candidate answers of a future question; the confirmed principles are now applied by the principle-aware recommendation core `shared/recommend-procedure.md` (used by `/discuss-open-question` and by `/recommend-all-open-questions`'s `recommend-open-question` agent) as a weighted advisory factor that drives and is cited in a recommendation, rather than a candidate-elimination directive for an auto-answer sweep.

**Notes:**
- Touch ONLY the header prose (lines above the first `### <Short Title>` entry). Do NOT modify, reword, reorder, or remove any of the four `### <Short Title>` principle entries or their `*Origin:*` lines — the store's data and per-entry format are explicitly unchanged this milestone.
- The keep/eliminate framing describes each entry's *body*, which is unchanged; only the header sentence about *who consumes the principles and how* is updated (from candidate-elimination-for-a-sweep to weighted-advisory-factor-in-a-recommendation).
- Two surviving facts must be preserved in spirit: presence in the file means the principle is user-confirmed (there is no status field), and this file is written **only** by `capture-milestone-principle-updates`.
- This is a docs-sync task on the store's header only; it is deliberately separate from the workflow-logic scrub task, which excludes `milestones/answer_decision_principles.md`.

**Success:**
- The header of `milestones/answer_decision_principles.md` no longer names `try-answer-all-questions-by-principle`.
- The header describes the confirmed principles as applied by the principle-aware recommendation core `shared/recommend-procedure.md` (via `/discuss-open-question` and the `/recommend-all-open-questions` recommend sweep) as a weighted advisory factor that drives and is cited in a recommendation.
- The "presence means user-confirmed (no status field)" fact and the "written only by `capture-milestone-principle-updates`" fact both survive in the rewritten header.
- All four `### <Short Title>` principle entries and their `*Origin:*` lines are byte-for-byte unchanged (a `git diff` of the file shows only header lines changed).

---

## Sync CLAUDE.md To The Recommendation-Advisor Model

End-to-end sync of `CLAUDE.md` — the agent-facing project spec carrying the repository layout, the skill roster / pipeline block, and the dense invariant set — to the recommendation-advisor model this milestone establishes, now that all the logic changes exist (sweep deleted, recommend core principle-aware, `> **Applied principle:**` citation rendered, workflow-logic vocabulary scrubbed, principle-store header repointed). This is a faithful sync that matches the house style of dense, precise invariants — remove everything describing the deleted auto-answer sweep, preserve everything still true and unrelated, and add/adjust the invariants that document the new model.

**Notes:**
- This is the last task of the milestone and runs after every logic change and the `skills/`/`agents/`/`shared/` scrub. `CLAUDE.md` is out of scope for the "Scrub Retired Sweep Vocabulary From Workflow-Logic Files" task (which touches only `skills/`, `agents/`, `shared/`) and for the principle-store header task — this task owns `CLAUDE.md` alone. `README.md` is a separate sync surface **not** covered here.
- Removal scope (delete, do not repoint): drop `skills/try-answer-all-questions-by-principle` and `agents/try-answer-question-by-principle.md` from the layout section, the pipeline / skill-roster block, and every invariant that describes the sweep — its read-only-subagent design, its clean-working-tree precondition, its `Principle-based-answer:` subject + one-repeated-`Answer-Principle:`-trailer-per-principle commit rules, its most-significant-first gather, and its "orchestrator owns all mutation / subagent returns a verdict only" divergence note.
- Vocabulary scrub: remove the now-dead `Principle-based-answer:` / `Answer-Principle:` provenance vocabulary everywhere `CLAUDE.md` mentions it. This includes the `answer-open-question` invariant that documents the trailer's *absence* as the manual-vs-sweep discriminator — **drop** that discriminator framing entirely (no replacement), consistent with the milestone's "Manual-vs-sweep discriminator scrub" decision; the `Manual-answer:` subject and its `^Manual-answer:` capture-grep collectability must still read correctly without naming the sweep. Also update the "revert-then-re-answer" correction-flow wording that leans on the deleted sweep so it no longer depends on it.
- Repoint the comparison anchors that describe `recommend-all-open-questions` (and its `recommend-open-question` subagent) as the "argument-free twin of `try-answer-all-questions-by-principle`" so they no longer reference the deleted sweep, while preserving the real behavioral facts (mutate-but-do-not-commit, idempotent, sole mutator, path-scoped `git add`, no clean-tree precondition).
- New-model invariants to add/adjust (match the existing dense invariant voice): (a) `shared/recommend-procedure.md` is now **principle-aware** — its grounding step reads the fixed-path store `milestones/answer_decision_principles.md` in place, and a bearing confirmed principle is a **weighted advisory factor** (strong default in favor of its supported option, merit-override-only-with-a-named-reason, never a binding filter/veto) that is **cited**, not silently applied; (b) the `recommend-open-question` agent renders each bearing principle as a `> **Applied principle:** <Short Title>` line stacked above the last-line `> **Recommendation:**` anchor (one line per bearing principle, pure repetition for the multi-principle case), so the lifted anchor stays provenance-free by construction; (c) the principle store's consumer is now the recommendation core — applied by `/discuss-open-question` and the recommend sweep — while `capture-milestone-principle-updates` stays its **sole writer**.
- Keep `capture-milestone-principle-updates`'s description accurate now that its `Answer-Principle:`-trailer exclusion is vacuous/removed (nothing emits that trailer anymore); its `git log --grep='^Manual-answer: '` manual-answer walk and sole-writer role are unchanged.
- Update the committing-skills / committing-orchestrators accounting so it no longer counts the deleted sweep's commit behavior (the "two orchestrators commit" tally and the `Principle-based-answer:` one-auto-answer-per-commit rule), while leaving the still-true facts about the other committers — `answer-open-question` (`Manual-answer:`), `answer-open-question-with-recommendation` (`Recommendation-answer:`), the answer-with-recommendation agent, and `complete-all-tasks` — intact.
- Preserve everything in `CLAUDE.md` still true and unrelated to the sweep; do not rewrite unrelated invariants.

**Success:**
- `grep -n 'try-answer\|Answer-Principle\|Principle-based-answer' CLAUDE.md` returns nothing referencing the deleted sweep.
- `CLAUDE.md`'s layout, pipeline / skill-roster block, and invariants describe the principle-aware recommend core, the `> **Applied principle:**` citation rendering, and the advisor-consumer story, with no surviving description of the auto-answer sweep, its subagent, its clean-tree precondition, or its provenance vocabulary.
- The `answer-open-question` invariant no longer frames the missing `Answer-Principle:` trailer as the manual-vs-sweep discriminator, and the `Manual-answer:` subject + `^Manual-answer:` capture collectability still read correctly.
- The `recommend-all-open-questions` invariants no longer call it (or its subagent) a twin of the deleted sweep, yet still state mutate-but-do-not-commit, idempotent, sole-mutator, and path-scoped staging.
- The revert-then-re-answer correction-flow wording no longer depends on the deleted sweep.
- The committing accounting no longer counts the sweep's commit behavior, and all invariants unrelated to the sweep remain intact.

---

## Sync README.md To The Recommendation-Advisor Model

End-to-end sync of `README.md` — the public, adoption-facing workflow documentation carrying the per-skill `## Skill reference`, the per-phase Mermaid diagrams, and the answer-principle / correction-flow prose — to the recommendation-advisor model this milestone establishes, now that every logic change and the `CLAUDE.md` sync exist (sweep deleted, recommend core principle-aware, `> **Applied principle:**` citation rendered, workflow-logic vocabulary scrubbed, principle-store header repointed). This is a faithful sync in the public-docs register — remove everything describing the deleted auto-answer sweep, preserve everything still true and unrelated, and keep the public-facing tone and structure. This is a sync, not a rewrite.

**Notes:**
- This is a `README.md`-only task and is deliberately separate from the `CLAUDE.md` sync (which touches only `CLAUDE.md`), the `skills/`/`agents/`/`shared/` vocabulary scrub, and the principle-store header task — `README.md` is out of scope for all three.
- Skill reference: delete the `### try-answer-all-questions-by-principle` entry and the `### try-answer-question-by-principle (subagent)` entry outright, and remove every mention of the deleted sweep or its subagent from other skills' descriptions (e.g. the `answer-open-question` `Manual-answer:`/no-`Answer-Principle:`-trailer discriminator prose, the `capture-milestone-principle-updates` `Answer-Principle:`-trailer exclusion clause, and the `Recommendation-answer:` subject's "matches neither the `Manual-answer:` nor the `Principle-based-answer:` grep" contrast — repoint that contrast so it no longer names the deleted sweep while keeping the never-harvested rationale).
- *Iterating milestone requirements* Mermaid diagram: remove the `ITM2["/try-answer-all-questions-by-principle"]` node, its incoming edge `ITM1 --> ITM2`, its correction edge `ITM2 -.->|wrong auto-answer: revert + re-answer| ITM4`, and its terminal edge `ITM2 --> D2`, then re-wire so the diagram stays connected and valid — the `ITM5` recommend → `ITM6`/`ITM8` answer-with-recommendation path to `D2` remains. Also drop `ITM2` from the `class …req;` list and the `class …optional;` list so no classDef references a deleted node. Preserve the per-phase `req`/`optional`/`state` styling and the `D1`/`D2` parallelogram seam-node conventions.
- Repoint the recommend sweep's "argument-free twin of `/try-answer-all-questions-by-principle`" comparison anchor (in the `recommend-all-open-questions` skill-reference entry) so it no longer references the deleted sweep, while preserving its real behavioral facts (batch form of `/discuss-open-question`, sole mutator, idempotent, mutate-but-do-not-commit, path-scoped `git add`, no clean-tree precondition).
- Scrub the dead `Principle-based-answer:` / `Answer-Principle:` provenance vocabulary everywhere `README.md` mentions it, and update the "revert-then-re-answer" correction-flow wording (in the *Iterating milestone requirements* flow prose and the **Correction loop** bullet of the answer-principle-learning-loop section) so it no longer depends on the deleted sweep.
- Update the answer-principle-learning-loop prose (`### The answer-principle-learning loop` and its bullets) to the advisor model: confirmed principles now feed the principle-aware recommendation core `shared/recommend-procedure.md` (used by `/discuss-open-question` and by `/recommend-all-open-questions`'s `recommend-open-question` agent) as a **weighted advisory factor** that drives and is cited in a recommendation (rendered by the agent as a `> **Applied principle:**` line above the `> **Recommendation:**` anchor), rather than powering an auto-answer sweep. Drop the **Autonomous sweep** bullet describing `/try-answer-all-questions-by-principle`. `capture-milestone-principle-updates` remains the store's sole writer.
- Keep `capture-milestone-principle-updates`'s skill-reference description accurate now that nothing emits an `Answer-Principle:` trailer (its exclusion clause is vacuous/removed); its `git log --grep='^Manual-answer: '` walk and sole-writer role are unchanged.
- Preserve everything in `README.md` still true and unrelated to the sweep; do not rewrite unrelated skill entries, diagrams, or prose.

**Success:**
- `grep -n 'try-answer\|Answer-Principle\|Principle-based-answer' README.md` returns nothing referencing the deleted sweep.
- The `## Skill reference` section no longer contains a `try-answer-all-questions-by-principle` entry or a `try-answer-question-by-principle` subagent entry.
- The *Iterating milestone requirements* Mermaid diagram has no `ITM2` node or edge and no classDef line referencing `ITM2`, still renders as a valid connected `flowchart TD`, and retains the `recommend → answer-with-recommendation → D2` path and the `D1`/`D2` seam nodes with their per-phase styling.
- The revert-then-re-answer correction-flow wording no longer depends on the deleted sweep, and the recommend sweep is no longer described as a twin of it.
- The answer-principle-learning-loop prose describes the confirmed principles as a weighted advisory factor feeding `shared/recommend-procedure.md` (cited as an applied-principle line in a recommendation), with `capture-milestone-principle-updates` still the sole writer, and no surviving **Autonomous sweep** bullet.
- No file other than `README.md` is modified by this task.

---
