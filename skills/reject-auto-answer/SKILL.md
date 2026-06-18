---
name: reject-auto-answer
description: Reject one bad auto-answer produced by the /try-answer-all-questions-by-principle sweep — revert its commit (which reopens the answered question) and point the user at re-capturing the principle that produced it. Takes an optional argument: a commit id from the sweep's report, a fragment of the wrong folded decision text in requirements.md, or nothing (defaults to HEAD). Use it whenever the user says things like "undo that auto-answer", "that principle-based answer was wrong", "revert the last sweep answer", "reopen that question", or "the auto-answerer got this one wrong" — it validates the target is a real auto-answer commit, confirms with you, then reverts it staged for review.
---

# reject-auto-answer

This is the correction step of the answer-principle-learning loop. The autonomous sweep
`/try-answer-all-questions-by-principle` commits one auto-answer per commit, each citing the
confirmed principle(s) that produced it in an `Answer-Principle:` trailer. When one of those
auto-answers is wrong, this skill reverts that single commit — which **reopens** the question
it answered — and directs the user to fix the principle behind it so the next sweep does not
reproduce the bad answer.

The reopen is exact and automatic: because the sweep enforces **one commit = one auto-answer**
(see *Auto-answer commit isolation* in `requirements.md`), reverting that commit simultaneously
restores the deleted `Open question` / `Deferred` block **and** removes the folded decision
under `## Decisions` in one shot. So **the revert *is* the reopen** — this skill
never hand-reconstructs the reopened question and never edits the principle store.

This skill is **interactive and single** (one commit per invocation), so it always shows the
resolved commit and confirms before reverting, and refuses rather than guessing whenever the
target is ambiguous or is not a genuine auto-answer commit.

## Usage

```
/reject-auto-answer [optional commit-id | text fragment]
```

The single optional argument has an **overloaded** meaning, resolved in the order below
(step 2). The fragment form is the primary ergonomic entry: a bad auto-answer is usually
discovered by *reading the wrong folded decision prose* in `requirements.md`, so the user
points at that wrong text rather than hunting a commit id.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`
(run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path). The fragment path locates
text inside `<MILESTONE_DIR>/requirements.md`, so this resolution is required — never use a
hardcoded task-list path.

### 1. The auto-answer commit format this skill acts on

The sweep orchestrator owns this format (see *Principle citation* in `requirements.md`); read
the exact strings there rather than re-deriving them. An auto-answer commit:

- has subject `Principle-based-answer: <Short Title>` — `<Short Title>` is the **answered
  question's** handle;
- carries **one or more** `Answer-Principle: <Short Title>` trailer lines (a repeated key, one
  per load-bearing principle);
- touches **only** `requirements.md`.

The validation gate (step 3) checks the last two — touch-only-`requirements.md` **and** at
least one `Answer-Principle:` trailer — to confirm the target is a real auto-answer and not a
manual `requirements.md` commit.

### 2. Resolve the argument to a target commit

Resolve the single optional argument in this order:

- **a. No argument → `HEAD`.** Rejecting the just-made answer of a single-answer sweep is
  argument-free.
- **b. The argument is a valid git rev → use it directly** as the target commit. Test with
  `git rev-parse --verify --quiet '<arg>^{commit}'`; on success, that resolved commit is the
  target. (Commit ids come from the sweep's `git log <BASE>..HEAD` report.)
- **c. Otherwise → treat the argument as a text fragment.** Locate it in
  `<MILESTONE_DIR>/requirements.md` and resolve it to its **introducing** commit with the
  pickaxe, scoped to that file:

  ```
  git log -S'<fragment>' --oneline -- <MILESTONE_DIR>/requirements.md
  ```

  Run from the repo root and use the **full** `<MILESTONE_DIR>/requirements.md` pathspec, not a
  bare `requirements.md` (a bare path will not match from the repo root). `git blame` on the
  region is a fine cross-check when the fragment still appears in the working tree.

  Fragment→commit resolution is fragile when a later cascade or manual edit reworded the
  `## Decisions` region. If the pickaxe returns **no commit** or **more than
  one**, the resolution is unsafe — take the refuse path (step 3, *Refuse rather than revert
  silently*).

### 3. Validate the target before reverting

Both resolution paths feed the **same** gate. The resolved target commit must satisfy **both**:

- **Touches only `requirements.md`.** Check the changed paths:

  ```
  git diff-tree --no-commit-id --name-only -r <commit>
  ```

  This returns repo-root-relative paths, so the single path must equal
  `<MILESTONE_DIR>/requirements.md`. Any other or additional path fails the gate.
- **Carries at least one `Answer-Principle:` trailer.** Extract the trailers:

  ```
  git show -s --format='%(trailers:key=Answer-Principle)' <commit>
  ```

  At least one `Answer-Principle: <Short Title>` line must be present.

**Refuse rather than revert silently.** All of these converge to the **same** behavior — report
what was found and ask the user for an explicit commit id, **never** reverting:

- fragment resolution found **no** match or was **ambiguous** (zero or multiple commits),
- the resolved commit **touches more than just** `requirements.md`,
- the resolved commit **carries no `Answer-Principle:` trailer** (it is a manual
  `requirements.md` edit or some other commit, not an auto-answer).

This is safe because the skill is interactive: when in doubt, hand the decision back to the
user rather than reverting a commit that is not a real auto-answer.

### 4. Display the resolved commit and confirm

Before reverting, **always** show the user the resolved target and get explicit confirmation —
because fragment→commit resolution can land on the wrong commit. Display:

- the commit's `Principle-based-answer: <Short Title>` **subject** (which question it answered),
- its `Answer-Principle: <Short Title>` **trailer line(s)** (which principle(s) produced it),
- the short commit id.

`git show -s --format='%h %s%n%(trailers:key=Answer-Principle)' <commit>` gives all three in one
shot. Only on explicit confirmation proceed to step 5.

### 5. Revert the commit — staged, not committed

Revert the confirmed target without committing:

```
git revert --no-commit <commit-id>
```

Leave the revert **staged and not committed**. This is deliberate (see the *Reject-auto-answer
contract* in `requirements.md`):

- it is consistent with the universal no-commit invariant — every cairn skill leaves its
  changes staged for the user;
- the resulting dirty tree collides with `/try-answer-all-questions-by-principle`'s clean-tree
  abort, which **blocks the next sweep** until the user closes the loop (re-answers the now-open
  question, or fixes the principle). Committing here would only make sense if this skill were
  batch/orchestrated; it is interactive and single.

**Conflict → abort and report.** If a later commit touched the overlapping region so the revert
cannot apply cleanly, run:

```
git revert --abort
```

to restore a clean state, name the conflicting commit(s) to the user, and hand off — **never**
leave conflict markers or a half-applied revert in the tree.

### 6. Close the loop — re-capture the principle

The revert reopened the question, but **this skill never edits the principle store** — the
principle(s) that produced the bad answer are still in
`milestones/answer_decision_principles.md`, so the next sweep would reproduce the same answer.
The correction is therefore not complete at revert. To close the loop:

- **Surface the commit's cited principle set** — the `Answer-Principle: <Short Title>` trailer
  line(s) you displayed in step 4 — and tell the user the question is reopened (the block is
  back, the folded decision is gone).
- **Direct the user to re-capture.** When the commit cited **more than one** principle, the
  user picks which one to revise — **do not auto-target one**.
- You **may then offer to chain into** `/try-capture-answer-principle` with a free-text focus
  hint naming the principle the user chose, so they can revise it. The chain is an offer, not
  automatic.

## Rules

- This skill **never edits the principle store** (`milestones/answer_decision_principles.md`)
  and never hand-reconstructs the reopened question — the `git revert` alone reopens it, by the
  one-commit-=-one-auto-answer invariant.
- **Validate before reverting:** the target must touch **only** `requirements.md` **and** carry
  **at least one** `Answer-Principle:` trailer. On any failure — no match, ambiguous match,
  extra paths, or no trailer — report and ask the user for an explicit commit id; **never revert
  silently**.
- **Always display the resolved commit (subject + trailer line(s)) and confirm** with the user
  before reverting.
- Revert with `git revert --no-commit` and leave it **staged, not committed** (no-commit
  invariant; the dirty tree is what blocks the next sweep until the loop is closed).
- On a revert conflict, run `git revert --abort`, name the conflicting commit(s), and hand off
  to the user — never leave conflict markers or a half-applied revert.
- One commit per invocation: this skill is interactive and single, not a batch tool.
