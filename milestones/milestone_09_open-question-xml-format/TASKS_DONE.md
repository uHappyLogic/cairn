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
