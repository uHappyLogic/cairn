---
name: try-answer-all-questions-by-principle
description: Autonomously sweep the current milestone's requirements for open and deferred questions and answer every one a confirmed answering principle already settles — by candidate elimination, committing one auto-answer per commit that names the applied principle in an Answer-Principle trailer. Use this once the project has taught some principles (via the answer-principle-learning loop) and you want the requirements re-swept to resolve everything those principles now cover without re-deciding by hand. Trigger it whenever the user says things like "sweep the open questions", "answer what the principles cover", "run the principle sweep", "auto-answer by principle", or "resolve the questions our principles already settle". Requires a clean working tree.
---

# try-answer-all-questions-by-principle

This is the autonomous sweep at the end of the answer-principle-learning loop. The project
accumulates user-confirmed answering principles in `milestones/answer_decision_principles.md`
(taught via `/answer-open-question`, distilled into the store at milestone finish); this skill re-reads
every open and deferred question in the current milestone and **answers exactly those a
confirmed principle already settles** — leaving everything else untouched.

It is a pure **orchestrator**. It does not judge questions itself: for each one it dispatches
the read-only `try-answer-question-by-principle` subagent, which performs the candidate
elimination (enumerate the realistic answers, keep only those a confirmed principle supports,
look for a unique survivor) and returns a verdict. The orchestrator owns everything the
subagent does not: gathering and ordering the questions, recording each answer in the
document, and committing. There is **no** strength gate, no "an informed reader would agree on
sight" judgment — that earlier logic is gone. A confirmed principle, surfaced by the
subagent's verdict, is the sole basis for any auto-answer.

Because each answer is committed on its own with the applied principle named in an
`Answer-Principle:` trailer, every autonomous decision is traceable and individually
reversible by `/reject-auto-answer`.

## Usage

```
/try-answer-all-questions-by-principle
```

Takes no arguments — it sweeps every `Open question` and `Deferred` entry in the current
milestone's `requirements.md`.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Require a clean working tree

This sweep commits — one auto-answer per commit — so it must start from a pristine tree to
guarantee each commit contains exactly one auto-answer. Run:

```
git status --porcelain
```

If it produces **any** output — staged changes, unstaged changes, or untracked files (ignored
files are fine; porcelain already excludes them) — **abort without changing anything** and
tell the user explicitly:

> The working tree is not clean. Commit (or stash/remove) your pending changes first, then
> re-run `/try-answer-all-questions-by-principle`. This sweep needs a clean tree so each
> auto-answer lands in its own commit.

Reaching a clean tree is a deliberate checkpoint, not a wart: manual answers land already
committed on their own `Manual-answer:` commits, and the user clears any other pending
working-tree changes before escalating to this autonomous sweep. That clean boundary is
what separates human decisions from auto-answers in git history.

On a clean tree, capture the pre-sweep commit so the end-of-run report can scope to exactly
the commits this invocation adds:

```
BASE=$(git rev-parse HEAD)
```

### 2. Gather and order the questions once

Read `<MILESTONE_DIR>/requirements.md` in full. Gather every `Open question — <Short Title>`
and `Deferred — <Short Title>` entry. If there are none, say so and stop.

Order the gathered list **loosely most-significant → least** — answer foundational questions
before the questions that depend on them. This ordering is a proxy for *cascade-parent-first*:
answering a foundational question may moot its dependents via cascade before they are ever
dispatched, which is the safe direction for cascades.

The ordering is a **sequencing heuristic only** — it decides *which question goes first*,
never *whether* a question gets answered. The answer/don't-answer decision is the subagent's
strict candidate elimination; ordering never reintroduces judgment.

You walk this gathered, ordered list **exactly once** (step 3). A single ordered pass
terminates the sweep: answering only ever *removes* questions (cascades moot them) and nothing
adds questions mid-sweep, so the set shrinks monotonically to a fixed point. **Do not wrap
step 3 in an outer re-gather / loop-until-no-survivors loop** — there is no such loop, and
adding one is a defect.

### 3. Walk the order once, dispatching the subagent per surviving question

For each question in the gathered order:

**a. Re-check against the live document.** Re-read `<MILESTONE_DIR>/requirements.md` and
confirm the question still exists and is still unresolved. A prior answer's cascade may have
already removed it; if it is gone, **skip it** and move on. The gathered list is an *ordering,
not a work snapshot* — this live re-check is what keeps the sweep correct as cascades fire.

**b. Dispatch the read-only subagent.** Use the `Agent` tool with
`subagent_type: "try-answer-question-by-principle"` (singular — the per-question subagent), one
dispatch per question. Pass it the question's **Short Title** and **Context** — the full
`requirements.md` block plus any surrounding detail it needs to enumerate candidates honestly:

```
Judge this single open question by confirmed answering principles.

Short Title: <Short Title>

Context:
<the question's full Open question / Deferred block, plus relevant surrounding requirements>
```

Wait for the agent to return its verdict. The subagent is **read-only** — it mutates nothing
and returns a verdict only (unique-survivor yes/no, the surviving answer, the load-bearing
principles by `### <Short Title>` handle, and the candidate set considered). The orchestrator
owns **all** document mutation and the commit.

**c. On a unique survivor, record the answer.** When the verdict is `Unique survivor: yes`,
record it by reading and following `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` (run
`echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out every step
yourself in this conversation. Pass the verdict's **Short Title** as its `SHORT TITLE` input
and the verdict's **Surviving answer** as its `ANSWER` input. That procedure owns locating the
matching block, analysing implications, removing the block, folding the decision into
`## Decisions` as clean prose, and cascading to any entries the answer moots.
**Do not restate those steps here, and do not invent a parallel recording format.**

**d. Commit exactly this one auto-answer.** Immediately after recording (so the commit
contains only this single `requirements.md` edit), commit:

```
git add -A
git commit -m "Principle-based-answer: <Short Title>" \
  --trailer "Answer-Principle: <Principle Short Title>" \
  [--trailer "Answer-Principle: <next Principle Short Title>" …]
```

- The **subject** is `Principle-based-answer: <Short Title>` where `<Short Title>` is the
  **answered question's** handle — the subject says *which question*.
- Emit **one `--trailer "Answer-Principle: <Short Title>"` line per load-bearing principle**
  the verdict listed, using each principle's `### <Short Title>` handle — the trailer says
  *which principle(s)*. This is a **repeated trailer key** (git-idiomatic, exactly like
  `Co-authored-by:`), never a comma-separated single line. List **every** load-bearing
  principle the verdict named — this is the complete supporting set, not a curated subset.

The clean-tree precondition guarantees the `git add -A` can only stage the single
`requirements.md` edit just made, so "one commit = one auto-answer" holds by construction and
the tree returns to clean for the next question.

**e. On no unique survivor, leave the question untouched.** When the verdict is
`Unique survivor: no` — two-or-more survivors, conflicting principles implying different
answers, or zero survivors — make **no** change: do not answer it, do not annotate it, do not
add an advisory note. A question left for the user must look exactly as it was found.

### 4. Report

When the gathered order is exhausted, report once:

- **If the sweep committed at least one auto-answer**, print a single ready-to-run command
  that shows exactly this invocation's commits with their full messages (so the
  `Answer-Principle:` trailers are visible in one shot), and direct the user to it — they pass
  any commit id from it to `/reject-auto-answer` to undo a bad answer:

  ```
  git log <BASE>..HEAD
  ```

  Substitute the literal `BASE` value captured in step 1. Use the plain range form — **not**
  a `--grep='Principle-based-answer:'` form, which would also surface every past run's
  auto-answers. Do **not** re-serialize per-answer details in the report: the subject and
  trailers already live in git, and reprinting them would create a second place the citation
  must stay in sync.

- **If the sweep committed nothing** (empty/absent principle store, or no unique survivor
  anywhere), say so in one sentence and print **no** `git log` command — an empty
  `BASE..HEAD` range would only confuse.

Do **not** enumerate the untouched questions: they remain visible as `Open question` /
`Deferred` blocks in `requirements.md` and via re-running
`/review-milestone-requirements`, so listing them here would just duplicate
the live document.

## Rules

- **Never feed an auto-answer into principle capture.** This orchestrator replicates the
  answer-recording mechanism (via the shared procedure) but its auto-answers must **never**
  become the basis for a captured principle. Every auto-answer was itself *derived from* an
  existing confirmed principle, so capturing a principle from it would be circular.
- A confirmed principle (via the subagent's verdict) is the **sole** basis for any auto-answer.
  The old strength-gate / informed-reader judgment logic is gone — do not reintroduce it.
- On a **fresh project** where `milestones/answer_decision_principles.md` is absent or empty,
  the subagent finds no supporting principle for any candidate, so every question yields "no
  unique survivor", the sweep resolves nothing, commits nothing, and prints the no-op report.
  That is correct: principles must first be taught via the manual
  `/discuss-open-question → /answer-open-question` flow, with principles distilled into the
  store at milestone finish.
- Walk the gathered order **once**, with a per-question live re-check + skip. There is **no**
  outer re-gather loop.
- The orchestrator owns all document mutation and the commit; the `try-answer-question-by-principle`
  subagent is read-only and returns a verdict only.
- Record answers **only** via `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` — never a
  parallel recording format.
- Commit **exactly one auto-answer per commit**: subject `Principle-based-answer: <Short Title>`,
  one repeated `Answer-Principle: <Short Title>` trailer line per load-bearing principle.
