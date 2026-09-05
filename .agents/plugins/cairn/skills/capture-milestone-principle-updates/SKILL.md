---
name: capture-milestone-principle-updates
description: Distill reusable answering principles from a just-finished milestone's recorded decisions into the project-wide principle store.
---

# capture-milestone-principle-updates

This is the finish-time harvester of the answer-principle-learning loop. Over a milestone, each
`/answer-open-question` records a decision and commits it with the decision's **rationale in the
commit body** (subject `Manual-answer: <Short Title>`). This skill reads that finite, known-up-front
set of commits **once the milestone is finished** and distills from them the generalizable answering
principles that the recommendation advisor can apply.

It is the **sole writer** of `milestones/answer_decision_principles.md` (a single project-wide file at
the `milestones/` root, **above** any one milestone, so principles accumulate across milestones).

## Usage

```
/capture-milestone-principle-updates
```

Takes no arguments. It is an **optional** follow-up run *after* `/finish-current-milestone` has
already recorded the milestone and cleared the current-milestone pointer to `none`.

> This skill writes **only** the principle store at the fixed path
> `milestones/answer_decision_principles.md`. It does **not** touch any milestone's `requirements.md`.
> When a pass distills a new or revised principle it **commits** that principle-store edit itself
> (step 5); a pass that distills none changes no file and commits nothing.

## Workflow

### 1. Resolve the just-finished milestone — NOT via `get-current-milestone`

By the time this skill runs, `/finish-current-milestone` has already cleared the current-milestone
pointer to `none`, so the usual `shared/get-current-milestone.md` resolution would find no active
milestone. **Do not call `get-current-milestone`.** Instead, resolve the target milestone from the
**last row of the `## Completed Milestones` table** in `milestones/README.md` — the row
`/finish-current-milestone` appended for the milestone it just finished.

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
- **Read the commit bodies, not just the subjects.** The subject only names the answered question; the
  reusable reasoning is in the **body** (`git log` / `git show` of each commit). Phase-1 extraction
  works from those bodies.

If the walk returns **no qualifying commits**, this is the empty-range exit — go straight to step 6
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

3. **Cluster the survivors against each other (cross-candidate dedup).** Where several commits
   express the **same** underlying rule, merge them into one candidate (carrying the strongest
   phrasing and the originating examples). The output of phase 1 is the deduped set of surviving candidates, ranked
   **strongest first** (most clearly generalizable / most load-bearing for future recommendations).

If phase 1 leaves **no** surviving candidate (commits existed but none generalize), go to step 6 —
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
   static batch — is the whole reason this is an iterating loop.

**Termination is deterministic.** The candidate pool is the finite, known-up-front set of surviving
candidates from phase 1. Each confirmation resolves one (add / revise / decline) and removes it, so the
pool shrinks monotonically. The loop ends when every commit's rationale has been considered and every
surviving candidate is resolved with no pending merges.

#### 4a. Entry schema

Each entry is one principle per subsection:

```markdown
### <Short Title>

<The principle as a generalizable keep/eliminate directive — a reusable decision
rule that can be applied to the candidate answers of a future question, not a
restatement of one past decision.>

*Origin: <originating question or example>*
```

- **`### <Short Title>` heading — the handle.** A 2–5 word unique name, mirroring the open-question
  Short-Title convention. This is the key this skill matches on for revise-vs-add. No separate ID scheme.
- **Body — the directive in prose.** A generalizable keep/eliminate rule, not a restatement of the
  originating decision.
- **`*Origin:*` line — optional.** A pointer to the originating question or example, to aid human
  auditing and future overlap judgments. Omit it when there is nothing useful to record. What is
  applied is the *statement*, not the origin.
- **No status field.** Presence in the file means confirmed.

### 5. Commit the principle-store update

Read and follow the shared commit procedure at `.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: the fixed-path store `milestones/answer_decision_principles.md` (a `milestones/`-root artifact, **not** any `<MILESTONE_DIR>` file — this skill writes only that store).
- **SUBJECT** — `Principle-capture: <milestone_id>` (the `<MILESTONE_DIR>` resolved in step 1), the marker naming this skill's distinctive principle-capture function.

A pass that distilled no new principle — the empty commit range, in-range commits that none generalize, or the user declining every candidate — leaves `milestones/answer_decision_principles.md` unchanged; a pass whose confirmed revise/add actually edited the store commits that edit. The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.

### 6. Report

- **If at least one principle was written,** print exactly one fixed terse status line and nothing
  else:

  `Principles captured.`

  Carry no principle `### <Short Title>`, no add/revision breakdown, and no commit subject, and print
  no next-step or recommendation-advisor pointer.
- **If nothing was captured** — the empty commit range (step 2) **or** in-range commits that none
  generalize (step 3) **or** the user declined every candidate — report it in a **single line**: there
  are no `Manual-answer` principles in range to distill (write nothing, commit nothing). This is the
  distinct one-line no-op message for a pass whose dirty-own-path guard fired, never a collapse into
  `Principles captured.`; all three cases **converge on this identical terminal report**.
