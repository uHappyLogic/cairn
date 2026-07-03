# Milestone 8: Principles As Recommendation Advisor

## Goal

Convert the project-wide answering principles from an auto-answer engine into a recommendation advisor. Remove the redundant /try-answer-all-questions-by-principle skill and its try-answer-question-by-principle agent, and make the shared recommendation core (shared/recommend-procedure.md, used by both /recommend-all-open-questions's agent and /discuss-open-question) principle-aware: when a confirmed principle from milestones/answer_decision_principles.md bears on a question, it drives and is cited in the recommended option, otherwise recommendations are produced as today. The principle store's data and format are unchanged — only its consumer pointer moves. Scrub the now-dead auto-answer provenance vocabulary throughout (Principle-based-answer: subject, Answer-Principle: trailer, capture's exclusion grep, the revert-then-re-answer correction wording), and sync CLAUDE.md, README.md, and the principle-store header to the new model.

## Relevant starting state

### Principle store and its current consumer wiring

`milestones/answer_decision_principles.md` is a single project-wide file at the `milestones/` root (above any one milestone), holding user-confirmed answering principles. Each entry is a `### <Short Title>` subsection whose body is a generalizable **keep/eliminate directive** (applied to the candidate answers of a future question) plus an optional `*Origin:*` line; presence means confirmed, no status field. It currently holds four principles. Its **header prose names `try-answer-all-questions-by-principle` as the consumer** ("Each is a reusable keep/eliminate directive that `try-answer-all-questions-by-principle` can apply…" and "written **only** by `capture-milestone-principle-updates`"). The data and per-entry format are what this milestone keeps unchanged — only the consumer pointer moves.

### The auto-answer sweep to be removed

`skills/try-answer-all-questions-by-principle/SKILL.md` is the autonomous orchestrator: it requires a clean tree, gathers open/deferred questions most-significant-first, dispatches the read-only `agents/try-answer-question-by-principle.md` subagent per question (candidate elimination → verdict with a unique survivor + load-bearing principles), records each survivor via `shared/answer-procedure.md`, and commits one auto-answer per commit — subject `Principle-based-answer: <Short Title>`, one repeated `Answer-Principle: <Short Title>` trailer per principle. Both the skill and the agent are the two files to delete. The subagent is read-only; all mutation/commit lives in the orchestrator.

### The recommendation core and its two wrappers (the upgrade target)

`shared/recommend-procedure.md` is the execution-neutral analytical core — ground in live code → enumerate 2–4 honest alternatives (what-it-is / advantage / drawback) → recommend one with a tie-break. It is **not currently principle-aware**: it never reads the principle store. Two wrappers consume it via `${CLAUDE_PLUGIN_ROOT}`: (a) the `discuss-open-question` skill runs it inline in conversation; (b) `agents/recommend-open-question.md` runs it read-only per question and renders the result as the `>`-blockquote sub-block, whose last line is the liftable `> **Recommendation:** <chosen option> — <rationale>` anchor. `skills/recommend-all-open-questions/SKILL.md` orchestrates that agent across all questions (mutate-but-do-not-commit) and repeatedly describes itself as the "argument-free twin of `/try-answer-all-questions-by-principle`" — comparison anchors that break when the twin is deleted.

### Principle capture (writer — retained, lightly scrubbed)

`skills/capture-milestone-principle-updates/SKILL.md` stays the sole writer of the principle store; its manual-answer → principle learning input is untouched. It walks `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md` and **excludes any commit carrying an `Answer-Principle:` trailer** (the sweep's signature) as circular. Once the sweep is gone nothing emits that trailer, so the exclusion becomes vacuous; its step-5 report also points captured principles at `/try-answer-all-questions-by-principle`. Both references are part of the scrub.

### Retired-vocabulary blast radius (thorough scrub)

The now-dead auto-answer provenance vocabulary appears in these live files beyond the two deleted ones. `Principle-based-answer:` / `Answer-Principle:`: `README.md`, `CLAUDE.md`, `skills/answer-open-question/SKILL.md` (documents the trailer's *absence* as the manual-vs-sweep discriminator), `skills/capture-milestone-principle-updates/SKILL.md`, `skills/answer-open-question-with-recommendation/SKILL.md` + `agents/answer-open-question-with-recommendation.md` (the `Recommendation-answer:` subject is defined by contrast against both). The `try-answer` name also appears in `shared/answer-procedure.md`, `skills/answer-all-open-questions-with-recommendation/SKILL.md`, and `skills/recommend-all-open-questions/SKILL.md`. The revert-then-re-answer correction wording lives in `README.md` and `CLAUDE.md` (and the deleted skill).

### CLAUDE.md / README.md sync surface

`CLAUDE.md` carries the full skill roster, pipeline block, layout, and a dense set of invariants that describe the sweep, its read-only-subagent design, its commit rules, and its relationship to capture and the recommend twin. `README.md` mirrors this in the skill reference plus the *Iterating milestone requirements* Mermaid diagram (which has a sweep node/edge). Both need syncing to the recommendation-advisor model — including the principle store's new consumer story.

## Decisions

### Recommendation machinery

A bearing confirmed principle acts as a **weighted advisory factor** in `shared/recommend-procedure.md`, not a binding filter: it is a strong default in favor of its supported option and is cited whenever it influenced the recommended pick. Merit may override a bearing principle, but only for a specific stated reason, which must be named in the recommendation. This keeps principles advisory — consistent with this milestone's reframing of the principle store from a binding auto-answer engine into a recommendation advisor — rather than letting a principle veto a candidate outright.

The principle-aware `shared/recommend-procedure.md` names the fixed store path `milestones/answer_decision_principles.md` directly in its grounding step and reads it in place, rather than taking the confirmed principles as a caller-supplied input alongside QUESTION. This is consistent with the core's existing grounding behavior (which already reads live `requirements.md` and source files directly), preserves the only path-freedom that matters — caller-owned `<MILESTONE_DIR>` resolution, which is unaffected because the store is a fixed milestone-independent path above any milestone — and avoids duplicating the identical store-read into both wrappers.

When a bearing principle is cited in a recommendation, the `recommend-open-question` agent renders that citation as a separate `> **Applied principle:** <Short Title>` line placed above the `> **Recommendation:**` anchor — never baked into the anchor rationale. Because `/answer-open-question-with-recommendation` lifts only the anchor line verbatim, the citation stays out of the recorded `## Decisions` prose, keeping it provenance-free by construction; and `shared/answer-procedure.md`'s whole-run removal clears the extra line on answer. The `> **Applied principle:**` line must sit above the anchor so the "anchor is always the last line" rendering invariant holds.

## Open questions

> **Deferred — Manual-vs-sweep discriminator scrub:** `skills/answer-open-question/SKILL.md` documents the *absence* of an `Answer-Principle:` trailer as the discriminator between manual and sweep auto-answer commits; with the sweep gone that counterpart disappears. Whether to reword it (e.g. against `Recommendation-answer:` as the only other answer subject) or drop the discriminator note entirely — a mechanical wording call best settled while editing.
>
> **Alternatives:**
> - **Drop the discriminator note entirely** — delete the orphaned "no `Answer-Principle:` trailer / its absence marks this a manual vs. auto-answer" sentence and the sweep-mirroring clauses, leaving no replacement; the `Manual-answer:` subject and its surviving `git log --grep='^Manual-answer: '` capture rationale stand on their own. *Advantage:* truest to a dead-vocabulary scrub — it removes what became vacuous when the sweep and the only `Answer-Principle:` emitter disappeared, and invents no new framing. *Drawback:* a reader comparing the two surviving answer subjects (`Manual-answer:` vs `Recommendation-answer:`) gets no in-file sentence spelling out how they differ.
> - **Reword the discriminator against `Recommendation-answer:`** — keep a discriminator sentence but repoint it, e.g. "the `Manual-answer:` subject (not `Recommendation-answer:`) is what marks a capture-harvested manual answer." *Advantage:* preserves an explicit "how this subject differs from its sibling" note for future readers. *Drawback:* manufactures a discriminator the design does not need — the two subjects are already separated solely by the `^Manual-answer:` grep anchor, so a trailer-style "discriminator" note restates existing machinery and risks reading as newly-invented, cutting against a clean scrub.
>
> **Recommendation:** Drop the discriminator note entirely — with the sweep and its `Answer-Principle:` trailer gone there is nothing left to discriminate against, and the `^Manual-answer:` capture grep already carries every fact the subject needs; a repointed discriminator would invent framing the scrub is meant to remove, not relocate.

## Out of Scope

