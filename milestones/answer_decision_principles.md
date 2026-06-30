# Answer decision principles

Project-wide, confirmed answering principles. Each is a reusable keep/eliminate
directive that `try-answer-all-questions-by-principle` can apply to the candidate
answers of a future open question. Presence here means the principle is
user-confirmed. This file is written **only** by `capture-milestone-principle-updates`.

### Prefer domain-neutral terms

When a question chooses among candidate names or vocabulary, eliminate any candidate that carries a specific domain's connotation (coding, ops, a particular industry) and keep the plain-English option that reads naturally across arbitrary workflows. Cairn is a domain-agnostic workflow tool, so naming that implies one domain is out. Tie-breaker among surviving neutral candidates: prefer the one that doesn't overload a word already reserved for a distinct meaning in the vocabulary.

*Origin: Replace-implement-verb — "complete" chosen over the coding-flavored "execute".*

### Drop-vs-replace by ambiguity

When a question chooses how to retire a qualifier word from a name, eliminate the "drop it entirely" candidate **only if** the bare noun left behind stays unambiguous in its structural context; otherwise keep that candidate out and prefer one that keeps or replaces the qualifier. Bare nouns that name a whole, self-evident thing in their location (e.g. a `## Decisions` section inside a known document) survive being dropped; bare nouns that still need a temporal or relational qualifier to be clear (e.g. "state" — state of what, when?) do not.

*Origin: State-heading-rename — "implementation" was replaced with "starting" (`## Relevant starting state`), not dropped as it was for `## Decisions`, because bare "state" stays ambiguous where bare "decisions" did not.*

### Mutate live machinery last

When a question concerns the order of a change set that modifies the very tooling executing it (a self-hosting / self-modifying refactor), eliminate any candidate ordering that alters an actively-used component before its final use; prefer the ordering that defers each such change to that component's last use and applies it atomically. Machinery that is read fresh each step — re-read files, dispatch strings held in a frozen execution context — breaks the in-flight run the moment it is changed out from under it, so its mutation cannot precede its last use and cannot be split. Corollary: keep every committed state self-consistent by distributing cross-cutting updates into each unit of work, rather than a trailing reconciliation pass that the now-broken machinery could no longer execute.

*Origin: Order-of-renaming — the execution machinery (implement-backlog-tasks orchestrator + implement-backlog-task skill/agent + shared/implement-procedure.md + dispatch type string) is renamed in a single atomic task that is the last one the orchestrated run dispatches.*

### Name by distinctive function

When a question chooses among candidate names that are all accurate, eliminate any candidate that states only a generic action or an incidental mechanism, and keep the one that names the operation's **distinctive responsibility** — the trait that separates it from its sibling operations and that a reader could not re-derive from the generic verb alone. Tie-breaker among surviving candidates: prefer the one whose object-noun keeps consistency with the established naming family for the same kind of artifact.

*Origin: Populate fan-out grammar — `populate-backlog` renamed to `derive-tasks` ("derive" names the distinctive requirements→tasks derivation with proven coverage) rather than the generic `populate-tasks`; object "tasks" keeps consistency with the `complete-task` / `submit-task` / `discuss-new-task` family.*
