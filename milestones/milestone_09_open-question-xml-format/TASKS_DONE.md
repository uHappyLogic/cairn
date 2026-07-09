# TASKS DONE

## Author Open Questions As XML Blocks

Rewrite the `review-milestone-requirements` skill — the sole author of open-question blocks — so that when it surfaces a new open or deferred question it authors a well-formed, indented `<open-question>` XML block instead of a one-line Markdown blockquote header. This is the authoring half of the milestone's Markdown→XML conversion; the recommendation sub-elements and the CLI query/answer paths are separate tasks.

**Provides:**
- The authored open-question block shape that downstream recommendation-render, CLI-query, and answer/reconcile tasks match against: a `<open-question id="Short Title" status="open|deferred">` opening tag on a single physical line (attributes id-first, double-quoted, entity-escaped), a `<question>` child carrying the entity-escaped question text at a 2-space indent, and a `</open-question>` closing boundary tag at the same base column. The review skill authors only these three lines — the `<alternative>` / `<applied-principle>` / `<recommendation>` children are added later by the recommend path.

**Notes:**
- The edit to `skills/review-milestone-requirements/SKILL.md` must be made through the `skill-creator:skill-creator` skill, not by editing the SKILL.md file directly.
- The full XML contract is already decided — do not re-invent it. Read these `requirements.md` `## Decisions` subsections and author exactly to them: **Open/Deferred encoding** (single `<open-question>` element, `status="open"|"deferred"`), **Question-block placement** (all blocks under the single `## Open questions` section, never inline next to a requirement; each `<question>` self-contained), **Boundary-line tag contract** (single-line opening tag, id-first attribute order, double quotes), **Block indentation** (2-space per nesting level, boundary tags at base column), **XML special-char escaping** (the five predefined entities on element text and attribute values), and **id match case-sensitivity** (Short Title stays the stable, case-insensitively-matched locate handle).
- Physical adjacency to the originating requirement is lost under the consolidated `## Open questions` section, so the authoring guidance must require each `<question>` to stand alone.

**Success:**
- The skill's step-3 authoring instructions emit the `<open-question id="..." status="open|deferred">` … `<question>` … `</open-question>` XML shape exactly per the requirements.md `## Decisions`: single-line id-first double-quoted opening tag, 2-space-indented `<question>` child, closing boundary tag at the base column, and entity-escaped element text and attribute values.
- No blockquote-header authoring instruction (`> **Open question — …` or `> **Deferred — …`) remains anywhere in the skill — description, workflow steps, or rules.
- The reconciliation step describes removing a whole block from its `<open-question …>` boundary line to its `</open-question>` boundary line (not a `>`-prefixed run).
- The convergence report keys on `status="open"` blocks remaining as the `/derive-tasks` precondition, with deferred (`status="deferred"`) blocks allowed to carry forward.
- The skill still reads the whole `requirements.md` for reconciliation and gap-surfacing (the reason-across / read-whole operations).
- A sample block authored per the updated instructions has deterministically greppable boundary lines, with `id` and `status` extractable by attribute-name-anchored regex (e.g. `id="([^"]*)"`).

---

## Rewire Answer-Procedure Locate And Remove To CLI

Rewrite the locate (step 2) and remove (step 4) steps of `shared/answer-procedure.md` — the execution-neutral recording core (inputs SHORT TITLE + ANSWER) — so they operate on the new `<open-question>` XML block via the milestone's decided line-oriented CLI idiom instead of the Markdown blockquote header. This is the answering-core half of the Markdown→XML conversion; the `<recommendation>`-lift in `shared/answer-with-recommendation-procedure.md` and the wrapper skills are separate tasks that compose over this unchanged SHORT TITLE + ANSWER core.

**Provides:**
- The retained SHORT TITLE + ANSWER recording contract, now backed by a CLI locate/remove that treats one `<open-question …>` / `</open-question>` boundary-token pair as the block unit — the same block the `answer-with-recommendation-procedure` locate/lift step and the wrapper skills target. Locate: match the block whose `id` attribute case-folds equal to the queried Short Title (attribute extracted by attribute-name-anchored regex so match is attribute-order-independent, entity-escaped stored value handled before comparing). Remove: delete the block from its opening boundary line through its closing `</open-question>` boundary line.

**Notes:**
- This is a shared **procedure file**, not a skill or agent, so it is edited directly with `Edit` — the milestone's skill-creator constraint applies only to `skills/`+`agents/` files.
- The CLI idiom is already decided — do not re-invent or reach for `xmllint`/an XML processor. Read and follow these `requirements.md` `## Decisions` subsections: **CLI query tooling** (line-oriented `awk`/`sed`/`grep` keyed on the `<open-question …>` / `</open-question>` boundary lines, never a real XML processor), **id match case-sensitivity** (case-fold both the queried Short Title and the block's `id` before comparing — preserving today's case-insensitive locate contract with zero regression), **Boundary-line tag contract** (extract `id` by attribute-name-anchored regex like `id="([^"]*)"`, order-independent), **XML special-char escaping** (the stored `id` is entity-escaped, so handle the five predefined entities when comparing), and **Open/Deferred encoding** (one `<open-question>` element with `status`, so open and deferred blocks share one boundary-token pair and status is irrelevant to locate/remove).
- Only steps 2 (locate) and 4 (remove) become CLI operations. Steps 3/5/6 — analyse implications, fold the decision into `## Decisions` as clean citation-free prose, cascade to mooted entries — stay whole-document read-and-reason operations per the query-where-it-pays convention (deterministic locate/extract/remove via CLI; reason-across via reading the whole file).
- The stop-on-missing-block behavior is retained: when no block's `id` matches, stop without changes and list the available ids — which the CLI can enumerate deterministically from the boundary lines.

**Success:**
- Step 2 (locate) describes a concrete CLI operation that finds the `<open-question>` block by case-folded `id` match, extracts the `id` by attribute-name-anchored regex (attribute-order-independent), and accounts for the stored `id` being entity-escaped when comparing.
- Step 4 (remove) describes deleting the block from its `<open-question …>` opening boundary line through its `</open-question>` closing boundary line via a deterministic CLI operation, replacing the old "remove the entire contiguous `>`-prefixed run" step.
- Open and deferred blocks are handled uniformly through the single `<open-question …>` / `</open-question>` boundary-token pair, with no type-specific locate/remove branch.
- The stop-on-missing-block path remains and lists the available ids on a mismatch (deterministically enumerable via the CLI).
- No `>`-blockquote / contiguous-`>`-run vocabulary remains anywhere in the file.
- Steps 3, 5, and 6 still read the whole document to reason, and the clean-prose / no-citation-marker / targeted-edits rules are unchanged.

---
