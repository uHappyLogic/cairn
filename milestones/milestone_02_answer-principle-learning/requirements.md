# Milestone 2: Answer Principle Learning Loop

## Goal

Add a project-local learning loop to the requirements-iteration cycle so human answers to open questions accumulate reusable, user-confirmed answering principles (stored in milestones/answer_decision_principles.md as binary in/out entries) that let try-answer-questions-by-principle (renamed from answer-obvious-open-questions) resolve progressively more questions autonomously — with a try-capture-answer-principle skill that records/revises principles, answer-obvious applying only confirmed principles and committing one auto-answer per commit while naming the applied principle in a commit-message trailer, and a reject-auto-answer skill that reverts a bad auto-answer by commit and reopens its question for re-answering.

## Relevant implementation state

### The requirements-iteration loop

The loop this milestone extends is four skills under `skills/`, documented in `README.md` as the "Iterating milestone requirements document" stage (a Mermaid subgraph) plus a per-skill reference section:

- `highlight-milestone-requirements-open-questions` — reads `<MILESTONE_DIR>/requirements.md` and annotates gaps inline as `> **Open question — <Short Title>:** …` (blocking) or `> **Deferred — <Short Title>:** …` blocks. Short Titles are 2–5 word unique handles used to cite a question by name. It only surfaces questions; it never resolves them.
- `discuss-open-question <Short Title>` — purely conversational deliberation on one named entry; ends by offering to invoke `answer-open-question`. Never edits the document.
- `answer-open-question <Short Title>. <answer>` — records a decision: splits its arg on the **first `.`** (title before, answer after), then (a) removes the matched question block, (b) folds the decision into `## Implementation decisions`, (c) cascades to any entry the answer moots. The try-capture-answer-principle skill is expected to be built on this recording mechanism.
- `answer-obvious-open-questions` — the autonomous sweep. Takes no args; processes every Open/Deferred entry **sequentially against the live document** (so cascades apply). For each it forms a recommendation from the real code, then applies a **strength gate**: answer only if a single concrete decision exists, an informed reader would agree on sight, and it is low-risk to reverse — with a higher bar for `Deferred` entries. It records confirmed answers exactly as `answer-open-question` does. Its explicit design value is *restraint* (leave anything contentious). It currently uses no external knowledge source and does not commit.

### Decision recording format

Resolved decisions live as prose under `## Implementation decisions` in `requirements.md`; the answered question block is deleted. There is currently no notion of a per-decision provenance/citation (nothing records *why* or *from what rule* a decision was made) — `answer-obvious` naming an applied principle was a new convention; it is resolved below (Principle citation) to live in a commit-message trailer, not in the document prose.

### Commit conventions (the no-commit invariant)

Per `CLAUDE.md`, individual skills **never commit** — they leave changes staged for the user. The sole exception is the `implement-backlog-tasks` orchestrator, which after each successful task runs `git add -A` then `git commit -m "<task heading>"` (the `##` heading without the prefix). Note `git add -A` stages the entire working tree — the existing precedent does **not** isolate a single logical change, which is directly relevant to the "Auto-answer commit isolation" open question.

### Skill & plugin structure

Skills are one `SKILL.md` per directory under `skills/`; subagents live in `agents/`; reusable procedure snippets live in `shared/` and are referenced from skills via `${CLAUDE_PLUGIN_ROOT}/shared/<file>.md`. All milestone-aware skills resolve `<MILESTONE_DIR>` by following `shared/get-current-milestone.md`, which reads the `Current milestone:` pointer line in `milestones/README.md`. The manifest is `.claude-plugin/plugin.json` (currently `version: 1.0.0`). New skills (try-capture-answer-principle, reject-auto-answer) follow the one-directory-per-skill pattern.

### Principle store — does not exist yet

`milestones/answer_decision_principles.md` does not exist. Its intended location is the `milestones/` **root**, i.e. *above* any `<MILESTONE_DIR>` — so it is shared across all milestones (this is what lets principles accumulate over time). Every existing reader resolves paths relative to `<MILESTONE_DIR>`; this file is the first project-wide, fixed-path artifact the loop would read.

> **Deferred — Missing principle file:** When `milestones/answer_decision_principles.md` does not yet exist (fresh project, before any principle is captured), what is the behavior — does `try-answer-questions-by-principle` treat an absent file as empty and resolve nothing, and does `try-capture-answer-principle` create it on first write?

### Documentation surfaces to update

`README.md` carries both the Mermaid workflow subgraph and a per-skill reference; `CLAUDE.md` carries the repository layout, the skills-and-workflow overview, and the "Invariants to preserve when editing skills" list (including the no-commit invariant). Both will need updates for the new skills, the principle file, and the commit exception.

## Implementation decisions

### Orchestrator / subagent architecture (try-answer-questions-by-principle)

`answer-obvious-open-questions` is **renamed to `try-answer-questions-by-principle`** and restructured as an orchestrator. The orchestrator finds the next unresolved Open/Deferred question and dispatches a sequential `try-answer-question-by-principle` subagent (one per question). The subagent performs the candidate elimination (enumerate the realistic answers, keep those supportable by ≥1 confirmed principle, confirm a unique survivor) and is **read-only on `requirements.md`** — it returns a verdict only: unique-survivor yes/no, the answer, the cited principle, and the candidate set considered. The orchestrator owns **all** document mutation and the commit: for a unique survivor it records the answer via the existing `answer-open-question` mechanism (remove the question block, fold the decision into `## Implementation decisions` as clean prose, cascade), then commits exactly one auto-answer per commit with the applied principle named in the commit's `Answer-Principle:` trailer.

The read-only-subagent split is a **deliberate divergence** from the `implement-backlog-task` agent (which edits files): cascades plus the already-decided clean-tree / one-commit-per-answer invariant require all document mutation serialized in the single sequential orchestrator, whereas the context-heavy candidate elimination is what's worth isolating in a subagent (there the edit *is* the work; here it isn't). **Only the agent is built** — no sibling user-facing skill, since `discuss-open-question` already covers manual single-question handling. If a skill+agent dual is ever wanted, the elimination procedure moves to a `shared/` file per repo convention (mirroring `implement-procedure.md`).

### Sweep run scope (try-answer-questions-by-principle)

A single `try-answer-questions-by-principle` invocation sweeps **every** Open/Deferred entry — it is a batch, not a one-question-per-invocation tool (manual single-question handling is already `discuss-open-question`'s job, and the *Sweep run report* / clean-tree precondition already assume a batch that produces multiple commits).

The orchestrator **gathers all current Open/Deferred questions up front and orders them loosely most-significant → least**, then walks that order **once**, dispatching the read-only `try-answer-question-by-principle` subagent per question. The significance ordering is a proxy for **cascade-parent-first**: answering a foundational question first lets its cascade moot dependent questions before those dependents are ever dispatched — the safe direction for cascades.

The gathered list is an **ordering, not a work snapshot**: before each dispatch the orchestrator re-checks the question still exists and is unresolved in the **live** document (a prior answer's cascade may have already removed it) and skips it if so. This preserves the existing "process sequentially against the live document (so cascades apply)" property.

**A single ordered pass terminates the sweep.** Answering only ever *removes* questions — cascades moot them, and nothing adds questions mid-sweep (surfacing new ones is `highlight-milestone-requirements-open-questions`'s job) — so the question set shrinks monotonically to a fixed point. The loop terminates when the gathered, ordered list is exhausted; there is **no** outer re-gather/loop-until-no-survivors-remain wrapper.

The significance ordering is an **orchestrator-side sequencing heuristic only** — it decides *which question goes first*, never *whether* a question is answered. The answer/don't-answer gate stays strict candidate-elimination (see *Principle match threshold*), so ordering does not reintroduce the judgment the loop is built to remove, and it is consistent with the orchestrator owning all sequencing while the subagent stays per-question and read-only.

### Answer-recording shared procedure (shared/answer-procedure.md)

The answer-recording core — locate the question block by Short Title → analyse the answer's implications → remove the matched block → fold the decision into `## Implementation decisions` as clean prose → cascade to any entry the answer moots — is extracted into a new `shared/answer-procedure.md`, the single source of truth for recording an answer (mirroring `shared/implement-procedure.md` and `shared/submit-procedure.md`). It resolves `<MILESTONE_DIR>` via `shared/get-current-milestone.md` and takes a **resolved Short Title + answer text** as inputs (locating and cascading are shared; obtaining the title/answer is the caller's job).

The file is **execution-neutral**: it must not mention arg-parsing, committing, the `Answer-Principle:` trailer, or the `try-capture-answer-principle` chain — exactly as `submit-procedure.md` never mentions the `DONE`/`FAILED` protocol. That neutrality is what lets one file serve both a staged-edit skill and a commit-per-answer orchestrator.

Both callers reference it via `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` and wrap it with only their own concerns:

- **`answer-open-question`** keeps its arg-parsing front (split the arg on the first `.` into Short Title + answer) and its tail — the report plus the unconditional `try-capture-answer-principle` chain-off.
- **`try-answer-questions-by-principle`** (orchestrator) keeps its clean-tree precondition, the candidate-elimination subagent dispatch (which supplies the Short Title + answer + cited principle), and the per-answer `git add -A` + commit carrying the `Answer-Principle:` trailer — and **never** chains to capture (the auto-answer was itself derived from a principle, so capture would be circular).

A new entry in `CLAUDE.md`'s "Invariants to preserve" list records that the answer-recording mechanism lives **only** in `shared/answer-procedure.md`; `answer-open-question` and the orchestrator reference it and never restate the steps. This supersedes the current state where the recording steps are duplicated in prose between `answer-open-question` (steps 3–4) and `answer-obvious-open-questions` (step 2c).

### Autonomous answering (try-answer-questions-by-principle)

`answer-obvious-open-questions` resolves a question **only** when a confirmed principle from `milestones/answer_decision_principles.md` covers it. The current strength-gate / judgment-based answering logic is **removed entirely** — the principle file becomes the sole source of autonomous answers. Questions no principle covers are left untouched (no advisory note). Consequences, accepted: (a) on a fresh milestone with an empty principle file the sweep resolves nothing until principles are taught via the manual `discuss-open-question → try-capture-answer-principle` flow; (b) a one-off obvious question that isn't worth generalizing into a principle will not be auto-answered and needs a manual answer. The win is that every committed auto-answer cites a principle, so the `reject-auto-answer → re-capture` correction loop can always trace and revise it.

### Principle match threshold (try-answer-questions-by-principle)

A confirmed principle is "applied" to an open question by **candidate elimination**, not by dictating an answer in isolation: `answer-obvious-open-questions` enumerates the realistic answers to the question, keeps those each supportable by at least one confirmed principle, and auto-answers **only if exactly one survives** — naming every load-bearing principle that supports the survivor, one per commit-message trailer line (see *Principle citation*). If two or more survive, the question is left for the user to decide. If none survive, the question is left untouched. The "supportable" test must be a genuine fit rather than a rationalization, and the candidate set must be the realistic alternatives (the same bar `discuss-open-question` uses when enumerating options) — the gate is only as strong as the candidate set. This deliberately trades coverage for near-zero wrong answers, consistent with the loop's restraint value.

**Conflicting principles** are subsumed by this rule: when more than one confirmed principle bears on a question and they imply different answers, more than one alternative survives elimination, so the question is deferred to the user rather than auto-answered.

### Auto-answer commit isolation (try-answer-questions-by-principle)

`answer-obvious-open-questions` requires a **clean working tree** and aborts otherwise. "Clean" means `git status --porcelain` produces no output — no staged changes, no unstaged changes, and **no untracked files**; ignored files remain fine and do not block (porcelain excludes them, and `git add -A` can never stage them). It checks cleanliness **once at the start** and refuses to run if the tree is dirty. Each auto-answer is then an edit-`requirements.md`-then-`git add -A`-then-commit cycle, so every commit contains **exactly one auto-answer** (one commit per answer) and the tree returns to clean for the next.

This is chosen over scoped staging (`git add requirements.md` only) because it makes "one commit = one auto-answer" a hard invariant that the `reject-auto-answer` revert-by-commit loop depends on, rather than a best-effort that breaks when `requirements.md` itself already has pending edits. Because the precondition guarantees a pristine start, the per-answer `git add -A` (kept to match the `implement-backlog-tasks` commit precedent — and equivalent to `git add requirements.md` under this precondition) can only stage the single `requirements.md` edit the orchestrator just made, so the invariant holds by construction. Accepted consequence: any stray untracked file **anywhere in the repo** blocks a sweep until it is committed or removed — the deliberate cost of making one-commit-per-answer a hard invariant rather than best-effort.

**Reaching a sweepable tree is a manual commit by design, not a wart to smooth over.** The iteration skills that precede a sweep — `answer-open-question` and `try-capture-answer-principle` — are dirty-tolerant (they leave their edits staged per the no-commit invariant); **only** the `try-answer-questions-by-principle` orchestrator requires a clean tree. So the user hand-commits their manual answers and freshly-captured principles before running a sweep, and that commit is the deliberate checkpoint separating human decisions from autonomous auto-answers in git history. The friction is localized to the single moment of escalating to the autonomous sweep — the rest of the loop needs no clean tree — so no new commit mechanism is introduced and the no-commit invariant stays universal across single skills. The orchestrator's clean-tree abort **must print an explicit message** telling the user to commit their pending changes first and re-run, so the abort's reason and fix are self-evident rather than a confusing failure.

### Principle citation (commit-message trailer)

The applied principle(s) are named in **commit-message trailer** line(s) on the auto-answer commit — one `Answer-Principle: <Short Title>` line per supporting principle (see below) — **not** inline in `requirements.md`. The folded decision under `## Implementation decisions` reads as clean prose with no citation marker, so the document carries **zero permanent citation bloat**; the principle provenance lives in git history. The trailer value is the principle's `### <Short Title>` handle from `answer_decision_principles.md`.

When the surviving answer is supported by **more than one** confirmed principle, the commit lists **every principle whose support was load-bearing** — one `Answer-Principle: <Short Title>` line per principle, a **repeated trailer key** (git-idiomatic, exactly like `Co-authored-by:`), never a comma-separated single line. "Load-bearing" means the principle genuinely contributed to keeping the surviving candidate alive; this is not a curated "most important" subset (that would reintroduce the judgment call the trailer exists to remove). `reject-auto-answer`'s "cites a principle" validation passes when **at least one** such line is present.

The auto-answer commit's **subject line** is `Principle-based-answer: <Short Title>`, where `<Short Title>` is the **answered question's** handle. So subject says *which question* and trailer says *which principle*. The fixed `Principle-based-answer:` prefix makes auto-answer commits greppable and eyeball-able in a one-line `git log` — its only real consumer is the user auditing history, since `reject-auto-answer` is handed the commit id by the sweep's report rather than parsing the subject. This is chosen over a bare heading (the `implement-backlog-tasks` precedent, which would leave autonomous commits with no marker distinguishing them from manual ones) and over conventional-commits style (a convention foreign to this repo).

`reject-auto-answer` performs its "cites a principle" validation by checking the target commit's message for **at least one** `Answer-Principle:` trailer line (alongside confirming the commit touches only `requirements.md`). The structured trailer is also the unambiguous signal distinguishing an auto-answer commit from a manual `answer-open-question` edit (which is staged, never committed) or any other `requirements.md` commit.

### Sweep run report (try-answer-questions-by-principle)

At sweep start the orchestrator captures `BASE=$(git rev-parse HEAD)`; the clean-tree precondition guarantees this is the pre-sweep state. The end-of-run report does **not** re-serialize per-answer details — they already live in git (subject `Principle-based-answer: <question>`, trailer `Answer-Principle: <principle>`), so reprinting them would duplicate history and create a second place the citation must stay in sync. Instead the report prints a single ready-to-run, full-message `git log <BASE>..HEAD` scoped to exactly the commits this invocation added (full message so the `Answer-Principle:` trailers are visible in one shot; **not** a `--grep='Principle-based-answer:'` form, which would also surface every past run's auto-answers). `reject-auto-answer` takes its commit id from that `git log` output.

Untouched questions are **deliberately not enumerated**: they remain visible as Open/Deferred blocks in `requirements.md` and via re-running `highlight-milestone-requirements-open-questions`, so listing them in the report would duplicate the live document. If the sweep committed nothing (empty principle file, or no unique survivor anywhere), the report says so in one sentence and prints no `git log` command — an empty `BASE..HEAD` range would only confuse.

### Principle entry schema (answer_decision_principles.md)

`milestones/answer_decision_principles.md` is a markdown file with **one principle per `### <Short Title>` subsection**, mirroring the open-question Short-Title convention. The schema is:

- **`### <Short Title>` heading — the handle.** This is the unique citable name `try-answer-questions-by-principle` writes to the `Answer-Principle:` commit-message trailer when it records an auto-answer, and the key `try-capture-answer-principle` matches on to decide revise-vs-add. No separate ID scheme.
- **Subsection body — the principle, in prose, as a generalizable decision rule.** It must be phrased so it can be applied as a keep/eliminate test against the realistic candidate answers to a *future* question (this is the operative meaning of "binary in/out": applied to a candidate answer, a principle says in = supportable/keep or out = eliminate). The body must be a **reusable directive, not a restatement of one past decision** — that distinction is what makes a principle worth capturing, and `try-capture-answer-principle` is responsible for enforcing that phrasing.
- **Optional `*Origin: <originating question or example>*` line** may follow the statement to aid human auditing and `try-capture-answer-principle`'s overlap judgment; omitted when there is nothing useful to record. The elimination subagent applies the **statement**, not the origin.
- **No per-entry status field.** Presence in the file means confirmed, because `try-capture-answer-principle` is the sole writer.

Example entry:

```markdown
### Invariant over best-effort

When choosing between mechanisms that achieve the same goal, prefer the one that makes a property a hard invariant over one that only enforces it best-effort — even at some cost in flexibility.

*Origin: Auto-answer commit isolation — clean-tree-then-commit over scoped staging.*
```

### Capture revise-vs-add (try-capture-answer-principle)

`try-capture-answer-principle` decides whether a just-made decision revises an existing principle or mints a new entry by **semantic overlap with user confirmation — never by title alone, and never silently**. It reads the entire `milestones/answer_decision_principles.md` (always feasible: the file is small and grows slowly), identifies the existing principles whose **statements** (not just `### <Short Title>` headings) bear on the decision, and surfaces that related set to the user with the choice: revise one of them, or add a new entry. An exact (case-insensitive) **title collision is only a strong hint** that pre-selects a likely revise target; the deciding test is semantic and the **user makes the final call**. `try-capture-answer-principle` never auto-merges or auto-adds without that confirmation.

This **refines, and does not contradict, the Principle entry schema decision**: the `### <Short Title>` heading remains the identity/citation key, while this rule closes the cross-title semantic-overlap gap (a new decision can overlap a principle filed under a different title). Rationale: the principle store governs every future autonomous answer, so a wrong silent merge/add corrupts the highest-value artifact in the loop; keeping the human as confirmer is consistent with `try-capture-answer-principle` being the sole writer of the file and with the loop's restraint / user-confirmed value, and mirrors how `answer-open-question` and `discuss-open-question` offer-then-confirm rather than acting on their own.

### Capture input contract (try-capture-answer-principle)

`try-capture-answer-principle` is an interactive skill that takes **no required parameter**. Its primary entry is an **unconditional chain-off appended to the `answer-open-question` skill**: after recording a decision, `answer-open-question` invokes it. Capture then **analyzes the current conversation** — the alternatives surfaced (including any `discuss-open-question` deliberation, which is in context because capture runs inline in the same conversation), the reasoning, and the decision just reached — **anchored on that most recent decision**, to judge whether a generalizable principle can be extracted. This conversation is the correct source rather than a passed `(Short Title, decision prose)` payload: a principle generalizes the *rule behind* a decision, which lives in the deliberation (the alternatives weighed, the trade-off articulated), not in the clean prose folded into `## Implementation decisions`.

If no generalizable principle can be extracted, capture **reports briefly and exits without engaging the user**; only on a real candidate does it run the revise-vs-add flow (see *Capture revise-vs-add*). The chain lives in the `answer-open-question` skill **only** — the autonomous sweep (`try-answer-questions-by-principle`) replicates the recording mechanism rather than invoking the skill, so auto-answers never trigger capture, which would be circular (the auto-answer was itself derived from an existing principle).

Capture is **also directly invocable** with an **optional free-text focus hint** — to disambiguate a conversation that covered several decisions, and so `reject-auto-answer` can chain in to revise a specific offending principle. Invoked cold with no relevant deliberation in context, it asks the user which decision to generalize rather than silently no-op'ing.

### Reject-auto-answer contract (reject-auto-answer)

`reject-auto-answer` reverts one bad auto-answer via `git revert --no-commit <commit-id>`, taking the commit id from `try-answer-questions-by-principle`'s report.

`reject-auto-answer` takes a **single optional positional argument with an overloaded meaning**, plus a zero-arg default, resolved in this order: (a) no argument → target `HEAD`; (b) the argument resolves as a commit-ish (a valid git rev) → use it directly as the target commit; (c) otherwise → treat the argument as a **text fragment**, locate it in `<MILESTONE_DIR>/requirements.md`, and resolve it to its introducing commit via `git log -S'<fragment>' -- requirements.md` / `git blame`. The fragment path is the primary ergonomic entry because a bad auto-answer is typically discovered by *reading the wrong folded decision prose* in `requirements.md`, not by auditing `git log` — so the user points at the wrong text rather than hunting a commit id. The explicit commit-id path is retained because the **Sweep run report** already hands the user exact commit ids in its `git log <BASE>..HEAD` output, and the zero-arg `HEAD` default makes rejecting the just-made answer of a single-answer sweep argument-free.

Both paths feed the same validation gate (below): the resolved target commit must touch only `requirements.md` and carry at least one `Answer-Principle:` trailer. Because fragment→commit resolution can be fragile when a later cascade or manual edit has reworded the `## Implementation decisions` region, the skill **must display the resolved commit — its `Principle-based-answer: <question>` subject and `Answer-Principle:` trailer line(s) — and confirm with the user before reverting**. If resolution is ambiguous, finds no match, or lands on a non-auto-answer commit, it reports and asks the user for an explicit commit id rather than reverting silently; this is safe because the skill is interactive and single.

The **Auto-answer commit isolation** invariant (one commit = one auto-answer) is what makes the revert exact: it simultaneously restores the deleted question block and removes the folded decision, so **the revert *is* the reopen** — the skill is essentially revert + report, with no hand-reconstruction of the reopened question.

- **Staged, not committed.** The revert is left staged — consistent with the no-commit invariant, and because the resulting dirty tree collides with `try-answer-questions-by-principle`'s clean-tree abort, which deliberately blocks the next sweep until the user closes the loop (re-answers, or fixes the principle). Committing would only win if `reject-auto-answer` were batch/orchestrated; it is interactive and single.
- **Validate the target before reverting.** `reject-auto-answer` confirms the target commit touches only `requirements.md` and cites a principle, refusing otherwise — so the reopen cannot restore garbage from a non-auto-answer commit.
- **Conflict → abort and report.** If a later commit touched the overlapping region and the revert cannot apply cleanly, `reject-auto-answer` runs `git revert --abort` to restore a clean state, names the conflicting commit(s), and hands off to the user — never leaving conflict markers or a half-applied revert.
- **Re-capture closes the loop.** `reject-auto-answer` itself **never edits the principle store** — it only reverts the commit (reopening the question) and reports. But the principle(s) that produced the bad answer remain in the store, so the next sweep would reproduce the answer; the correction is therefore not complete at revert. `reject-auto-answer` surfaces the commit's cited principle set (its `Answer-Principle:` trailer line(s)) and directs the user to re-capture. When the commit cites **more than one** principle, the user picks which to revise (the skill does not auto-target one); `reject-auto-answer` may then offer to chain into `try-capture-answer-principle` with a focus hint naming the chosen principle.

### Skill names (final)

The new and renamed skills take these final names, aligned with the established `<imperative-verb>-<domain-noun-object>` convention:

- **`try-capture-answer-principle`** — records/revises a confirmed answering principle. Named for its object (the *principle*, not the answer), which avoids colliding with `answer-open-question`.
- **`reject-auto-answer`** — flags a bad auto-answer, reverts its commit, and reopens the question. The object is the `auto-answer` it acts on; the intent-level verb `reject` is deliberately chosen over the git-mechanism verb `revert` (no other skill names its implementation).
- **`try-answer-questions-by-principle`** (orchestrator) and **`try-answer-question-by-principle`** (subagent) — the renamed sweep, as already decided above (renamed from `answer-obvious-open-questions`).

### Authoring approach (skill-creator)

The new and renamed skills are built with the `skill-creator:skill-creator` skill, scoped to its **drafting and description-writing guidance** — SKILL.md anatomy, "pushy" trigger descriptions to combat undertriggering, progressive disclosure, and the imperative / explain-the-why writing style. Its **eval/benchmark/iterate machinery is skipped** (`evals.json`, baseline-vs-with-skill subagent runs, the browser eval-viewer, `aggregate_benchmark`, the `run_loop.py` description optimizer): cairn's skills are deterministic markdown procedures with no single objectively-gradable output, so that harness adds ceremony without signal.

Where skill-creator's defaults conflict with cairn's conventions, **cairn's conventions take precedence** — one `SKILL.md` per directory, shared procedures referenced via `${CLAUDE_PLUGIN_ROOT}/shared/…`, the skill/agent dual pattern, the altitude split, the "Invariants to preserve" list, and the required `README.md` + `CLAUDE.md` updates (skill-creator's instinct to bundle `scripts/` or split `references/` generally does not apply here).

Optional later exception: if triggering accuracy specifically needs measuring, a one-off run of just the `run_loop.py` description optimizer — not the full output-grading harness — is acceptable.

## Out of Scope

## Open questions