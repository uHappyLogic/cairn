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

## Rewire Recommendation-Lift To CLI XML Extract

Rewrite the locate (step 2) and lift (step 3) steps of `shared/answer-with-recommendation-procedure.md` — the execution-neutral lift-then-delegate core (input SHORT TITLE only) that composes over `shared/answer-procedure.md` — so they locate the new `<open-question>` XML block and extract its `<recommendation>` element via the milestone's line-oriented CLI idiom instead of lifting the `> **Recommendation:**` blockquote anchor. This is the recommendation-lift half of the Markdown→XML conversion; it pairs with the sibling `shared/answer-procedure.md` locate/remove rewire, and the `answer-open-question-with-recommendation` skill and agent that wrap this procedure are separate tasks.

**Provides:**
- The retained SHORT TITLE-only input contract, now backed by a CLI locate + `<recommendation>` extract that treats one `<open-question …>` / `</open-question>` boundary-token pair as the block unit — the same block the reworked `answer-procedure` locate targets. Locate: match the block whose `id` attribute case-folds equal to the queried Short Title (attribute pulled by attribute-name-anchored regex so match is attribute-order-independent, entity-escaped stored value handled before comparing). Lift: within that block, read the `<recommendation option="...">…</recommendation>` element as a single-element CLI read (one attribute + one text node, no dereferencing of the referenced `<alternative id>`), then derive ANSWER by recombining the `option` attribute value with the element's text as "`<option>` — `<rationale>`" (the old anchor form) after reversing entity-escaping on both parts. That derived ANSWER, with SHORT TITLE, is handed to `shared/answer-procedure.md` unchanged.

**Notes:**
- This is a shared **procedure file**, not a skill or agent, so it is edited directly with `Edit` — the milestone's skill-creator constraint applies only to `skills/`+`agents/` files.
- The XML contract and CLI idiom are already decided — do not re-invent them or reach for `xmllint`/an XML processor. Read and follow these `requirements.md` `## Decisions` subsections: **Recommendation lift mapping** (ANSWER is the `option` attribute value recombined with the element text as "`<option>` — `<rationale>`", a single-element read with no `<alternative id>` dereference), **XML special-char escaping** (reverse the five-predefined-entity substitution on the lifted `option` value and rationale text, un-escaping `&amp;` last, so the recorded prose is clean unescaped text), **CLI query tooling** (line-oriented `awk`/`sed`/`grep` on the `<open-question …>` / `</open-question>` boundary lines), **id match case-sensitivity** (case-fold both the queried Short Title and the block's `id` before comparing), **Boundary-line tag contract** (extract attributes by attribute-name-anchored regex like `id="([^"]*)"`, order-independent), and **Applied-principle placement** (`<applied-principle>` is a sibling of `<recommendation>`, so a `<recommendation>`-only extract never touches a citation and ANSWER stays provenance-free by construction).
- The no-anchor guard becomes a **no-`<recommendation>`-element guard**: when no block's `id` matches SHORT TITLE, or the matched block contains no `<recommendation>` element (the recommend sweep never annotated it), stop cleanly without changing anything and report why — the same clean-stop semantics as today.
- Only the locate + lift (steps 2 and 3) change. Step 4 — delegate the resolved SHORT TITLE and derived ANSWER to `shared/answer-procedure.md` — is unchanged, as is the rule that this file never restates the recording core's locate/analyse/remove/fold/cascade steps.

**Success:**
- Step 2 (locate) describes a concrete CLI operation that finds the `<open-question>` block by case-folded `id` match, extracting the `id` by attribute-name-anchored regex and accounting for the stored `id` being entity-escaped when comparing.
- Step 3 (lift) describes extracting the `<recommendation option="...">…</recommendation>` element as a single-element read (one attribute + one text node, no `<alternative id>` dereference), and derives ANSWER as the `option` value recombined with the rationale text as "`<option>` — `<rationale>`".
- The lift reverses entity-escaping on both the `option` value and the rationale text using the fixed five-predefined-entity reverse-substitution map, un-escaping `&amp;` last, so lifting a sample annotated block yields a "`<option>` — `<rationale>`" answer with all entities un-escaped.
- The guard fires cleanly — stops without changing anything and reports why — when no block's `id` matches SHORT TITLE, or when the matched block carries no `<recommendation>` element.
- Step 4 still delegates the resolved SHORT TITLE + derived ANSWER to `shared/answer-procedure.md` unchanged, and the file still does not restate that core's steps.
- No `> **Recommendation:**` anchor reference or `>`-blockquote / contiguous-`>`-run vocabulary remains anywhere in the file.

---

## Render Recommendation As XML Sub-Elements

Rewrite the rendering step (step 3) and the final-message template (step 4) of the `recommend-open-question` agent — the read-only per-question recommendation subagent, the non-interactive twin of `discuss-open-question` — so it returns the alternatives / applied-principle / recommendation as the `<open-question>` block's XML sub-elements instead of the `>`-prefixed blockquote run. This is the recommendation-render half of the Markdown→XML conversion; the `recommend-all-open-questions` orchestrator that embeds these returned sub-elements into the existing block is a separate task, as is the CLI answer path that later lifts the `<recommendation>` element.

**Provides:**
- The XML sub-element shape the `recommend-all-open-questions` orchestrator embeds into an existing `<open-question>` block: one `<alternative id="...">` element per realistic option, each carrying the shared core's three fields (what-it-is text plus child `<advantage>` and `<drawback>` elements for the strongest reason for and the main cost against); zero or more `<applied-principle>` elements, one per bearing principle, each a direct child of `<open-question>` and a sibling of `<recommendation>` (never its child), and none at all when no principle bears; and a single `<recommendation option="...">…</recommendation>` element whose `option` attribute references the winning `<alternative id="...">` by its id and whose element text is the one-line rationale. All element text and attribute values (id and option included) are entity-escaped with the five predefined entities; nesting is indented 2 spaces per level relative to the block's base column. The agent returns exactly these sub-elements — never the `<open-question>` wrapper or the `<question>` element, which the orchestrator owns.

**Notes:**
- The edit to `agents/recommend-open-question.md` must be made through the `skill-creator:skill-creator` skill, not by editing the agent file directly.
- The full XML contract is already decided — do not re-invent it. Read these `requirements.md` `## Decisions` subsections and render exactly to them: **Applied-principle placement** (`<applied-principle>` is a direct child of `<open-question>` and a sibling — never a child — of `<recommendation>`, one element per bearing principle, none when none bears), **Recommendation lift mapping** (`<recommendation option="...">…</recommendation>` where `option` references the winning `<alternative id>` and the element text is the rationale, so the later lift is a single-element read), **XML special-char escaping** (the five predefined entities on all element text and attribute values, id and option included), and **Block indentation** (2-space indent per nesting level relative to the block's base column).
- Keeping the `<applied-principle>` citations structurally disjoint siblings preserves the provenance-free-by-construction property: the answer path lifts only the `<recommendation>` element, so a citation can never leak into a recorded `## Decisions` decision. The citation must therefore **never** be baked into the `<recommendation>` element's text — it lives only in its own sibling `<applied-principle>` element(s).
- The analytical core is unchanged: the agent still follows `shared/recommend-procedure.md` (step 2) for the alternatives + single recommendation without restating it — only the rendering (step 3) and the returned template (step 4) change. The agent stays strictly read-only and the isolation rule (never treat a sibling question's recommendation as an input) is unchanged.

**Success:**
- Step 3's rendering instructions describe the XML sub-elements per the requirements.md `## Decisions`: `<alternative id="...">` per option with what-it-is text and child `<advantage>`/`<drawback>`, zero-or-more sibling `<applied-principle>` elements (one per bearing principle, none when none bears), and one `<recommendation option="...">…</recommendation>` whose `option` references an `<alternative id>` and whose text is the rationale — all entity-escaped, 2-space-indented per nesting level relative to the base column.
- The step-4 final-message template shows exactly the returned sub-elements (`<alternative>` … `<applied-principle>` … `<recommendation>`) and explicitly excludes the `<open-question>` wrapper and the `<question>` element, with nothing before or after the sub-elements.
- No `>`-prefixed blockquote rendering, empty-`>` separation, or `> **Recommendation:**` anchor vocabulary remains anywhere in the agent file (description, workflow, or rules).
- The agent remains read-only (mutates nothing), still defers the analytical core to `shared/recommend-procedure.md` without restating it, and retains the isolation rule against treating a sibling question's recommendation as an input.
- The `<recommendation>` element's text carries no applied-principle citation; any citation appears only in a sibling `<applied-principle>` element.

---
