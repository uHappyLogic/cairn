---
name: capture-milestone-principle-updates
description: Distill reusable answering principles from a just-finished milestone's recorded decisions into the project-wide principle store. This is the optional finish-time follow-up that /finish-current-milestone recommends — run it right after finishing a milestone to harvest everything that milestone's manual answers taught. It walks the milestone's `Manual-answer:` commits, extracts the generalizable keep/eliminate rules behind them, dedups the candidates against each other, then confirms each with you one at a time (revise an overlapping existing principle, or add a new one) against the live store. Use it whenever the user says things like "capture the principles from this milestone", "distill what we learned", "harvest the answering principles", "update the principle store from this milestone", or "run principle capture for the milestone we just finished". It is the new sole writer of milestones/answer_decision_principles.md.
---

# capture-milestone-principle-updates

This is the finish-time harvester of the answer-principle-learning loop. Over a milestone, each
`/answer-open-question` records a decision and commits it with the decision's **rationale in the
commit body** (subject `Manual-answer: <Short Title>`). Those commit bodies are where the reusable
reasoning lives — the alternatives weighed, the trade-off accepted — because the recorded
`## Decisions` prose is deliberately citation-free and provenance-free. This skill reads that finite,
known-up-front set of commits **once the milestone is finished** and distills from them the
generalizable answering principles that future autonomous sweeps can apply.

It is the **sole writer** of `milestones/answer_decision_principles.md` (a single project-wide file at
the `milestones/` root, **above** any one milestone, so principles accumulate across milestones).
Presence of an entry means it is confirmed — there is no status field.

The value is restraint plus user confirmation. A principle governs *every* future autonomous answer,
so a wrong or sloppy one corrupts the highest-value artifact in the loop. This skill therefore
captures only genuinely reusable rules, and never writes the store without the user's explicit
say-so. What changes from the old per-answer capture is the **shape** of the work: instead of judging
one decision the instant it is made, this skill judges a whole milestone's worth of decisions at once
— so it must also dedup the new candidates **against each other**, a problem single-decision capture
never had.

## Usage

```
/capture-milestone-principle-updates
```

Takes no arguments. It is an **optional** follow-up run *after* `/finish-current-milestone` has
already recorded the milestone and cleared the current-milestone pointer to `none`.
`/finish-current-milestone` **recommends** it (never auto-runs it); the user invokes it on purpose.

> This skill writes **only** the principle store at the fixed path
> `milestones/answer_decision_principles.md`. It does **not** touch any milestone's `requirements.md`.
> Like every individual skill here it does **not** commit — it leaves its principle-store edit
> **staged** for the user to review.

## Workflow

### 1. Resolve the just-finished milestone — NOT via `get-current-milestone`

By the time this skill runs, `/finish-current-milestone` has already cleared the current-milestone
pointer to `none`, so the usual `shared/get-current-milestone.md` resolution would find no active
milestone. **Do not call `get-current-milestone`.** Instead, resolve the target milestone from the
**last row of the `## Completed Milestones` table** in `milestones/README.md` — the row
`/finish-current-milestone` appended immediately before recommending this skill.

Read `milestones/README.md`, find the `## Completed Milestones` table, and take its **last** row. The
backtick-quoted path in that row is `<MILESTONE_DIR>` (e.g. `` `milestones/milestone_05_…/` ``). That
same path feeds the commit walk in step 2.

### 2. Walk the milestone's `Manual-answer` commits

Collect the manual-answer commits for this milestone with a **path-scoped** log, using the
`<MILESTONE_DIR>` from step 1:

```
git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md
```

- **The path filter is itself the lower boundary.** `<MILESTONE_DIR>/requirements.md` does not exist
  before `/define-milestone-goal` created it, so no earlier commit can touch it — there is no need
  for a milestone-start marker or recorded base SHA.
- **Exclude sweep auto-answers.** As a guard, inspect each matched commit and **drop any that carries
  an `Answer-Principle:` trailer** — that trailer is the autonomous sweep's signature
  (`Principle-based-answer:` subject), and those answers were *already* derived from a confirmed
  principle, so re-distilling them would be circular. A genuine `/answer-open-question` commit carries
  the `Manual-answer:` subject and **no** `Answer-Principle:` trailer.
- **Read the commit bodies, not just the subjects.** The subject only names the answered question; the
  reusable reasoning is in the **body** (`git log` / `git show` of each commit). Phase-1 extraction
  works from those bodies.

If the walk returns **no qualifying commits**, this is the empty-range exit — go straight to step 5
(it is a normal outcome, not an error).

### 3. Phase 1 — extract candidates and dedup them against each other (internal, no user yet)

This phase is entirely internal: no writes, no user prompts. Its job is to turn a pile of commit
bodies into a clean, deduped set of principle candidates.

1. **Extract candidate directives.** From each in-range `Manual-answer` commit body, pull the reusable
   reasoning behind the decision: the realistic alternatives that were weighed, why one was chosen, the
   trade-off accepted. Phrase each as a candidate **keep/eliminate directive** — a rule you could apply
   as a binary in/out test against the candidate answers of a *different future* question.

2. **Drop the non-generalizable ones.** A principle must be a **reusable directive, not a restatement
   of one past decision**. If a commit's rationale is one-off, situation-specific, or simply states no
   reasoning at all (a bare cold answer), it yields **no** candidate — drop it. The commit→principle
   mapping is **many-to-many**: one commit may yield no candidate, and two commits may yield the same
   one.

   - **Restatement (drop):** "Answer-commit identification uses a `Manual-answer:` subject and no
     trailer." Names one question and one answer; cannot judge any *other* question.
   - **Reusable directive (keep):** "When two mechanisms reach the same goal, prefer the one that makes
     a property a hard invariant over one that only enforces it best-effort." A test applicable to an
     unrelated future question's candidates.

3. **Cluster the survivors against each other (cross-candidate dedup).** This is the structurally new
   step batch mode introduces — the retired single-decision capture only ever saw one candidate at a
   time and never had to dedup new candidates among themselves. Where several commits express the
   **same** underlying rule, merge them into one candidate (carrying the strongest phrasing and the
   originating examples). The output of phase 1 is the deduped set of surviving candidates, ranked
   **strongest first** (most clearly generalizable / most load-bearing for future sweeps).

If phase 1 leaves **no** surviving candidate (commits existed but none generalize), go to step 5 —
this converges on the **same** "nothing captured" report as the empty range.

### 4. Phase 2 — confirm and write one candidate at a time, against the live store

Now engage the user. You **may** first display the full surviving pool up front as a "what this
milestone taught" review aid — but **writes still advance one candidate at a time**. Display
granularity and write granularity are separate; never grouped-per-round approval.

Walk the surviving candidates **strongest-first**. For **each** candidate, before writing the next:

1. **Read the entire live `milestones/answer_decision_principles.md`.** It is small and grows slowly,
   so reading it whole is always feasible. If the file is absent or empty, there are no existing
   principles and this candidate will be an add (the file is created on first write).

2. **Decide revise-vs-add by semantic overlap, confirmed by the user — never by title alone, never
   silently.** Find the principles whose *statements* (not just their `### <Short Title>` headings) bear
   on this candidate. An exact (case-insensitive) **title collision is only a strong hint** that
   pre-selects a likely revise target; the deciding test is semantic. Surface the candidate you
   extracted alongside the overlapping existing entries, and let the user make the final call: **revise**
   one existing principle (and how), or **add** a new entry. If nothing overlaps, still present the new
   entry for confirmation before writing. Never auto-merge or auto-add without that confirmation.

3. **Write that one candidate** per the schema in step 4a, applying the user's confirmed choice (add a
   new `### <Short Title>` subsection, or edit an existing one in place).

4. **Re-scan the remaining pool before the next candidate.** Because the write you just made mutated the
   live store, a later candidate that overlapped *this* one may now be best expressed as a **revision of
   what you just wrote** rather than a fresh add. Re-evaluating between every write — not approving a
   static batch — is the whole reason this is an iterating loop. (This is why writes go one at a time:
   per-candidate confirmation honors this re-scan by construction; grouped-per-round would only be safe
   if the group were proven mutually independent, which a handful of principles rarely repays proving.)

**Termination is deterministic.** The candidate pool is the finite, known-up-front set of surviving
candidates from phase 1. Each confirmation resolves one (add / revise / decline) and removes it, so the
pool shrinks monotonically. The loop ends when every commit's rationale has been considered and every
surviving candidate is resolved with no pending merges. There is no fuzzy "are we done?" judgment.

#### 4a. Entry schema (carried forward verbatim)

Each entry is one principle per subsection:

```markdown
### <Short Title>

<The principle as a generalizable keep/eliminate directive — a reusable decision
rule that can be applied to the candidate answers of a future question, not a
restatement of one past decision.>

*Origin: <originating question or example>*
```

- **`### <Short Title>` heading — the handle.** A 2–5 word unique name, mirroring the open-question
  Short-Title convention. This is the citable key the autonomous sweep writes to its `Answer-Principle:`
  commit trailer, and the key this skill matches on for revise-vs-add. No separate ID scheme.
- **Body — the directive in prose.** A generalizable keep/eliminate rule, not a restatement of the
  originating decision.
- **`*Origin:*` line — optional.** A pointer to the originating question or example, to aid human
  auditing and future overlap judgments. Omit it when there is nothing useful to record. The sweep
  applies the *statement*, not the origin.
- **No status field.** Presence in the file means confirmed.

### 5. Report

- **If at least one principle was written,** briefly state, per principle, its `### <Short Title>`,
  whether it was an add or a revision, and that it is now available to
  `/try-answer-all-questions-by-principle`. Remind the user the principle-store edit is **staged, not
  committed**, for them to review.
- **If nothing was captured** — the empty commit range (step 2) **or** in-range commits that none
  generalize (step 3) **or** the user declined every candidate — report it in a **single line**: there
  are no `Manual-answer` principles in range to distill (write and stage nothing). These cases
  **converge on the identical terminal report** rather than branching into a distinct empty-range
  message; the empty range is simply the natural floor of the normal flow.

## Rules

- This skill is the **sole writer** of `milestones/answer_decision_principles.md`. Never write it
  without explicit user confirmation of the revise-or-add choice for each candidate (step 4.2).
- **Resolve `<MILESTONE_DIR>` from the last row of the `## Completed Milestones` table in
  `milestones/README.md` — explicitly NOT via `shared/get-current-milestone.md`.** The current-milestone
  pointer is already `none` when this skill runs.
- Walk **only** `git log --grep='^Manual-answer: ' -- <MILESTONE_DIR>/requirements.md`, and **exclude
  any matched commit carrying an `Answer-Principle:` trailer** (those are sweep auto-answers). Read the
  commit **bodies** for the rationale.
- Phase 1 is **internal** (extract → drop non-generalizable → cross-candidate dedup, no user); phase 2
  is **strongest-first, per-candidate** revise-vs-add against the **live** store with a **re-scan of the
  remaining pool after every write**. Confirm and write **one candidate at a time** — never
  grouped-per-round. Display granularity (an optional up-front pool preview) is separate from write
  granularity.
- A captured principle must be a **generalizable keep/eliminate directive**, not a restatement of one
  decision. The commit→principle mapping is many-to-many; a decision with no articulated rationale
  yields nothing — that empty result is correct, not a gap to fill.
- Carry the entry schema forward verbatim: `### <Short Title>` heading + prose keep/eliminate directive
  + optional `*Origin:*` line; **presence means confirmed; no status field.**
- An **empty commit range is a normal exit**, reported with the **same** single-line "nothing to
  distill" message as the "commits exist but none generalize" case — not a distinct branch.
- Write **only** `milestones/answer_decision_principles.md`. **Never** touch any `requirements.md`, and
  never resolve `<MILESTONE_DIR>` via `get-current-milestone`.
- **Do not commit.** Like every individual skill here, this leaves its edit to the principle store
  **staged** for the user to review.
