# Answer decision principles

Project-wide, confirmed answering principles. Each is a reusable keep/eliminate
directive. When a principle bears on an open question, the principle-aware
recommendation core `shared/recommend-procedure.md` — used by `/discuss-open-question`
and by `/recommend-all-open-questions`'s `recommend-open-question` agent — applies it
as a **weighted advisory factor** that drives, and is cited in, the recommended option
(rather than silently filtering a candidate). Presence here means the principle is
user-confirmed (there is no status field). This file is written **only** by
`capture-milestone-principle-updates`.

### Prefer domain-neutral terms

When a question chooses among candidate names or vocabulary, eliminate any candidate that carries a specific domain's connotation (coding, ops, a particular industry) and keep the plain-English option that reads naturally across arbitrary workflows. Cairn is a domain-agnostic workflow tool, so naming that implies one domain is out. Tie-breaker among surviving neutral candidates: prefer the one that doesn't overload a word already reserved for a distinct meaning in the vocabulary.

*Origin: Replace-implement-verb — "complete" chosen over the coding-flavored "execute".*

### Drop-vs-replace by ambiguity

When a question chooses how to retire a qualifier word from a name, eliminate the "drop it entirely" candidate **only if** the bare noun left behind stays unambiguous in its structural context; otherwise keep that candidate out and prefer one that keeps or replaces the qualifier. Bare nouns that name a whole, self-evident thing in their location (e.g. a `## Decisions` section inside a known document) survive being dropped; bare nouns that still need a temporal or relational qualifier to be clear (e.g. "state" — state of what, when?) do not.

*Origin: State-heading-rename — "implementation" was replaced with "starting" (`## Relevant starting state`), not dropped as it was for `## Decisions`, because bare "state" stays ambiguous where bare "decisions" did not.*

### Mutate live machinery last

When a question orders a change set that modifies the very tooling executing it, eliminate any ordering that alters an actively-used component before its final use; prefer the ordering that defers each such change to that component's last use and applies it atomically. Machinery read fresh each step breaks the in-flight run the moment it is changed out from under it. Corollary: distribute cross-cutting updates into each unit of work so every committed state stays self-consistent, rather than a trailing pass the now-broken machinery could no longer execute.

*Origin: Order-of-renaming — the execution machinery (implement-backlog-tasks orchestrator + implement-backlog-task skill/agent + shared/implement-procedure.md + dispatch type string) is renamed in a single atomic task that is the last one the orchestrated run dispatches.*

### Name by distinctive function

When a question chooses among candidate names that are all accurate, eliminate any candidate that states only a generic action or an incidental mechanism, and keep the one that names the operation's **distinctive responsibility** — the trait that separates it from its sibling operations and that a reader could not re-derive from the generic verb alone. Tie-breaker among surviving candidates: prefer the one whose object-noun keeps consistency with the established naming family for the same kind of artifact.

*Origin: Populate fan-out grammar — `populate-backlog` renamed to `derive-tasks` ("derive" names the distinctive requirements→tasks derivation with proven coverage) rather than the generic `populate-tasks`; object "tasks" keeps consistency with the `complete-task` / `submit-task` / `discuss-new-task` family.*

### Required input over optional branch

When a question chooses how a shared procedure obtains a value its callers can resolve once, eliminate the candidate that adds an optional input and branches on whether it was supplied, and the candidate that keeps a redundant lookup because the goal's scope wording shields the contract. Keep the candidate that makes the value a required input every caller resolves once and passes down, even when that widens the edit to runners the goal did not name: one uniform shape across runners outweighs the extra edits.

*Origin: Milestone resolution per question — `MILESTONE_DIR` became a required input of both answer procedures, resolved once per caller, over an optional pre-resolved input or a per-question re-lookup.*

### Report only unrecoverable signals

When a question asks whether a run should print an advisory about items it skipped or left behind, eliminate the advisory when another mechanism already records or recovers those items by construction, such as the commit diffs of the run or a later pass's own filter; keep an advisory only for a signal git does not hold and no later pass surfaces. Per-item output and state kept across a loop buy nothing when the next pass finds the same items on its own.

*Origin: Skipped-question report source — the sweep enumerates no skipped question, because the commit diffs record stripped blocks and the next recommendation pass finds them through its own filter.*

### Description over retirement note

When a question asks whether a durable instructions file should carry a retirement note or a do-not-restore ban for a design the file no longer describes, eliminate the note when the positive description of the current shape already rules the retired design out; keep an explicit ban only where the current description leaves the retired shape a natural reading. Keep measurement-bound figures out of durable rationale, since they go stale; the history belongs in the changelog and the milestone record.

*Origin: Retired-agent rationale home — the mutation-in-agent inversion invariant was deleted with no retirement clause, because the inline sweep description already rules the recording agent out.*

### Strongest setting on the whole-set judgment

When a question allocates model strength, effort, or budget across pipeline stages, eliminate the candidate that mirrors one setting across every stage. Keep the one that puts the strongest setting on the stage making one whole-set judgment per run, and the cheaper setting on the per-item fan-out whose cost scales with item count, provided a per-item miss costs one item's redo rather than a run. That a stage's output is frozen does not earn it the strongest setting; only an unbounded miss cost does.

*Origin: Headless chain alternatives line — the per-question alternatives fan-out runs at the cheaper model and the once-per-run recommendation pass at the stronger one, over the mirror pick that put one strong setting on both lines.*

### Check tier claims against the live environment

When a candidate's ranking rests on a claim about the environment outside the repository — which model is the stronger tier, which host has a capability, what a CLI accepts — eliminate any pick that carries that claim from memory or from the analysis's own assumption. Keep only a pick whose claim was checked against the live source, such as the CLI's model list or the host's documentation, before it was weighted: a recommendation built on an inverted premise inverts its own conclusion while still reading as sound.

*Origin: Headless chain alternatives line — the embedded analysis treated fable as the mid tier and opus as the strong model; the CLI lists both as family aliases with Fable the more capable, so the mirror pick's strength placement inverted.*
