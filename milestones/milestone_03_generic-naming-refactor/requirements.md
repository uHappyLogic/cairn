# Milestone 3: Generic Naming Refactor

## Goal

Rename Cairn's skills, agents, and file/document artifacts so the plugin reads as a generic idea-to-done workflow rather than a coding-specific one, with consistent naming across the whole plugin. Retire coding-flavored vocabulary — notably 'implement'/'implementation state' and 'backlog' — for domain-neutral terms, while keeping 'milestone' and 'requirements'. Clean break (no aliases); update every cross-reference across skills, agents, shared procedures, README.md, and CLAUDE.md. Exact replacement words left as open questions to be chosen as one coherent vocabulary.

## Relevant implementation state

### Skill inventory (invocable command names)

17 skills, each at `skills/<name>/SKILL.md` where the directory name **is** the slash-command name. Those carrying in-scope coding vocabulary: `implement-backlog-task`, `implement-backlog-tasks` (verb "implement" + "backlog"), `submit-backlog-task`, `populate-backlog`, `discuss-new-backlog-task` ("backlog"), and `specify-milestone-starting-implementation-state` ("implementation"). The rest are neutral but in the consistency audit: `init-milestone-base-workflow`, `discuss-milestone-goal`, `define-milestone-goal`, `highlight-milestone-requirements-open-questions`, `finish-current-milestone`, `goto-next-milestone`, and the answer/principle family (`discuss-open-question`, `answer-open-question`, `try-answer-questions-by-principle`, `try-capture-answer-principle`, `reject-auto-answer`).

### Agent inventory

3 agents at `agents/<name>.md`: `implement-backlog-task`, `submit-backlog-task` (both share a name with the like-named skill but run in isolation), and `try-answer-question-by-principle`. Two carry in-scope vocabulary. Critically, an agent's filename doubles as the **agent type string** that orchestrators dispatch by: `populate-backlog` spawns the `submit-backlog-task` agent, `implement-backlog-tasks` spawns the `implement-backlog-task` agent, and `try-answer-questions-by-principle` spawns `try-answer-question-by-principle`. Renaming an agent file requires updating its dispatch string in the orchestrator.

### Shared procedures

4 files at `shared/`: `implement-procedure.md` ("implement"), `submit-procedure.md`, `answer-procedure.md`, `get-current-milestone.md`. Each is referenced by skills/agents via `${CLAUDE_PLUGIN_ROOT}/shared/<file>.md` (single-source-of-truth pattern). Renaming a shared file requires updating every `${CLAUDE_PLUGIN_ROOT}` reference to it.

### File / document artifacts

Per-milestone files: `requirements.md` (kept), `TASKS_TODO.md`, `TASKS_DONE.md` (the "TASKS" noun is neutral and kept). The `requirements.md` template (authored by `define-milestone-goal`, read by many skills) uses the headings `## Goal`, `## Relevant implementation state`, `## Implementation decisions`, `## Out of Scope` — the first two contain the in-scope phrase "implementation state". Project-wide store: `milestones/answer_decision_principles.md`. Source-of-truth pointer: `milestones/README.md`.

### In-scope vocabulary blast radius

"backlog" appears across ~24 tracked files; "implement"/"implementation" across ~29; `TASKS_TODO`/`TASKS_DONE` are referenced by ~16 files (names kept, but they co-occur with the terms being changed). The heaviest documentation surfaces are `README.md` (Mermaid workflow diagram + per-skill reference) and `CLAUDE.md` (repository layout, skills overview, and a long invariants list naming nearly every skill/agent/shared file). Both must be re-synced after any rename.

### Coupled name strings beyond filenames

Renaming touches more than file paths: (1) plugin descriptions in `.claude-plugin/plugin.json` ("populate backlogs, implement tasks") and `.claude-plugin/marketplace.json`; (2) commit-message conventions emitted by orchestrators (e.g. `Principle-based-answer:` subject and repeated `Answer-Principle:` trailer in `try-answer-questions-by-principle`/`reject-auto-answer`; the per-task commit subjects in `implement-backlog-tasks`); (3) cross-references in prose where skills name other skills as next steps. `.claude/settings.local.json` holds stale local permission entries referencing old paths but is not part of the shipped plugin.

### Known gaps

There is no central name registry or alias layer — names are duplicated as directory names, dispatch strings, `${CLAUDE_PLUGIN_ROOT}` references, prose mentions, and doc tables. A "clean break" rename therefore has no single switch; every surface above must be updated together to keep the plugin internally consistent. No build/test harness exists to catch a missed reference — verification is grep-based.

## Implementation decisions

### Task-execution vocabulary

"implement" is retired in favor of **"complete"** as the task-execution verb — chosen over "execute" (the most coding-flavored option, counter to this milestone's goal) and "perform" (neutral but names only the doing, not the move to done). "complete" reads as plain English in any domain and describes the skill's full responsibility: carry out the work *and* move the task TODO→DONE. The execution family becomes `complete-task` (skill + agent), `complete-all-tasks` (orchestrator — per the orchestrator-grammar rule under *Naming-scheme depth*), and `shared/complete-procedure.md`; the agent dispatch string and all prose references to "implementing a task" follow. The lifecycle skill `finish-current-milestone` keeps "finish" so the milestone-level done-state does not compete head-on with the task-level "complete".

### Task-collection noun

"backlog" is **dropped entirely** rather than substituted with another noun — the `TASKS_TODO.md` / `TASKS_DONE.md` artifacts already carry the task noun, so "backlog" was redundant framing. Skill/agent names lose the `-backlog` segment: `submit-backlog-task` → `submit-task` (skill + agent) and `discuss-new-backlog-task` → `discuss-new-task`. In prose, "backlog" becomes "tasks" or "the task list" as fits.

`populate-backlog` is **not** a `-backlog`-segment drop but a full rename to **`derive-tasks`**: its distinctive job is deriving the task list from `requirements.md` with a proven requirement→task coverage matrix, so "derive" names that the tasks logically *follow from* the requirements, and the object "tasks" keeps consistency with the `complete-task` / `submit-task` / `discuss-new-task` family.

### Decisions-section heading

The `requirements.md` template heading `## Implementation decisions` is renamed to **`## Decisions`** — "implementation" is dropped entirely rather than substituted, the same move as the task-collection noun: the section sits inside `requirements.md` under a known structure, so the bare noun is unambiguous and needs no qualifier. Every reader of the heading (`shared/answer-procedure.md`, the `define-milestone-goal` template, `highlight-milestone-requirements-open-questions`, `reject-auto-answer`, the `try-answer-question-by-principle` agent, and the `CLAUDE.md` / `README.md` references) updates to `## Decisions` as part of the rename.

### Starting-state heading

The `requirements.md` template heading `## Relevant implementation state` is renamed to **`## Relevant starting state`** — here "implementation" is *replaced* with "starting" rather than dropped (unlike the `## Decisions` rename). The difference is that "state" needs a temporal qualifier to stay unambiguous, and "starting" precisely names the section's role — the baseline captured *before* the milestone's work begins — and stays accurate for the milestone's whole life, where "current" would go stale once work lands. It also aligns with the writer skill's existing "starting" vocabulary. Every reader/writer of the heading updates: `specify-milestone-starting-implementation-state` (writer), `populate-backlog` and `define-milestone-goal` (readers/template), and the `CLAUDE.md` / `README.md` references.

### Naming-scheme depth

The consistency pass is a **full re-derivation** of the naming scheme, not an in-place swap of only the two flagged terms — currently-neutral names are reshaped where consistency requires it. Concretely:

- The long writer skill `specify-milestone-starting-implementation-state` is renamed to **`specify-milestone-starting-state`**, dropping "implementation" in step with the *Relevant starting state* heading rename.
- **Fan-out orchestrators take the form `<verb>-all-<plural-object>`; their per-item workers stay `<verb>-<singular-object>`**, so an orchestrator and its worker no longer differ by a single trailing "s". This pairs `complete-all-tasks` (orchestrator) with `complete-task` (skill + agent), and renames the answer-sweep orchestrator `try-answer-questions-by-principle` → **`try-answer-all-questions-by-principle`** while its subagent stays `try-answer-question-by-principle`.
- The **`try-` prefix family is kept verbatim** — no `try-`→`attempt-` swap. The prefix is already domain-neutral, so a synonym swap would add churn without serving the milestone's goal; `try-capture-answer-principle` keeps its name.

### Naming grammar

Names conform to a **binding grammar that governs structure only**; word choice within that structure stays case-by-case for readability under the captured answering principles. The answer to "one target grammar vs. case-by-case" is *both, layered* — a binding structural grammar with case-by-case word choice inside it. The grammar ratifies what the decisions above already commit to rather than inventing a new scheme:

- **Baseline form** — every skill/agent name is `<verb>-<object-phrase>`: imperative verb first, hyphen-delimited. This already holds for all current names.
- **Fan-out pair** — a fan-out orchestrator takes `<verb>-all-<plural-object>` and its per-item worker takes `<verb>-<singular-object>` (per *Naming-scheme depth*). The `-all-` form applies only to fan-out pairs that **share a verb** (the orchestrator iterates a pre-existing collection, so without "all" the two names would differ by a single trailing "s" — `complete-all-tasks`/`complete-task`). It does **not** apply to a generator orchestrator that *produces* the collection from another document and whose worker uses a different verb: `derive-tasks` (which spawns the differently-verbed `submit-task` worker) takes no "all".
- **`try-` semantics** — `try-<verb>` marks an operation that may *legitimately no-op* (an attempt), **not** a read-only marker: read-only-ness is an architecture property (the candidate-elimination subagent), not a naming one. The `try-` family is kept verbatim.
- **Word choice is case-by-case** within the structure, governed by the *Prefer domain-neutral terms* and *Drop-vs-replace by ambiguity* principles — this is where redundant qualifiers get dropped or replaced.
- **No mandatory scope prefix** — there is no `milestone-` scope tag. "milestone"/"current-milestone" appears only where the milestone is the actual *object*; since nearly every skill is milestone-scoped, a scope tag would bloat names without adding information.
- **Conventional verbs are grandfathered** — `goto` and `init` stand. This milestone retires coding vocabulary, not grammatical irregularity, so the grammar is **not** a license to regularize names (no `goto`→`go-to`, no `init`→`initialize`).

### Rename ordering

Because this milestone rewrites Cairn with Cairn's own machinery, the rename tasks carry **one** ordering constraint, and it falls entirely on the task-execution machinery. The `implement-backlog-tasks` orchestrator re-reads the agent file and `shared/implement-procedure.md` fresh from disk on every iteration and dispatches its worker by a **fixed agent-type string held in its frozen context**. The moment that family is renamed, the type string no longer resolves and the in-flight run can dispatch nothing further. Therefore the **entire execution machinery — the `implement-backlog-tasks` orchestrator, the `implement-backlog-task` skill and agent, `shared/implement-procedure.md`, and the dispatch type string that wires them together — is renamed in a single atomic task that is the LAST task the orchestrated run dispatches.** It must be atomic: splitting it would leave a later dispatch reading a half-renamed procedure.

All other renames (the answer/principle family, `populate-backlog`/`submit-backlog-task`, `specify-…-state`, the `requirements.md` heading renames) are **order-free among themselves**, because the in-flight implement machinery never reads them. To keep the tree internally consistent at every commit — and to avoid a trailing doc-sync task, which could not run after the execution rename since no working agent type would remain to dispatch to — **every rename task updates all of its own references, including in `README.md` and `CLAUDE.md`**, rather than deferring doc sync to a final pass. As a safety option, the final execution-family rename may instead be performed **by hand** in the main conversation after running the orchestrator on everything else, so the riskiest step never runs through the self-modifying path.

## Open questions

> **Deferred — Manifest-and-commit-wording:** The exact one-line prose in `.claude-plugin/plugin.json` / `marketplace.json` descriptions and any commit-subject/trailer strings that reference renamed handles follow mechanically once the terms above are fixed — settle them during implementation.

## Out of Scope

