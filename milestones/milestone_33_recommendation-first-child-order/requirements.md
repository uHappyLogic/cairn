# Milestone 33: Recommendation-first child order

## Goal

Change the open-question tool's canonical child order so that a block carrying a `<recommendation>` renders, after its `<question>`, its `<applied-principle>` and `<depends-on>` elements, then the `<recommendation>`, then the alternative the recommendation names, then the remaining alternatives in their existing relative order; a block without a recommendation keeps today's order. The reordering lives entirely in the tool's renderer, so it is deterministic and applied on every write, with no skill prose positioning elements. `sort` keeps ordering blocks only, and a block keeps its reordered alternatives after `strip --recommendation`.

## Relevant starting state

### The open-question tool's renderer

`core/tools/open_questions.py` parses `open_questions.xml` into a `Question` dataclass (`question`, `alternatives` list, `principles`, `depends_on`, optional `recommendation`) and every write goes through `save_document` → `render_document` → `_question_lines`, which emits a block's children in one fixed order: `<question>`, the `<alternative>` elements in list order, `<applied-principle>`, `<depends-on>`, `<recommendation>`. The order ignores whether a recommendation is present. The parser (`_parse_children`) accepts children in any order and stores alternatives in document order, so whatever order the renderer writes becomes the stored list order on the next load. `cmd_locate` prints a block by calling `_question_lines` directly, on the assumption that the file always holds the serializer's own output.

### The tool's documented contract

The module docstring (also the `--help` text) states the canonical form: "each block's children grouped by kind in the fixed order <question>, the <alternative> elements (in their relative order), <applied-principle>, <depends-on>, <recommendation>". The `embed` help says a fragment's children are "written grouped by kind in the canonical order". `sort` (`sort_order`, `cmd_sort`) reorders whole blocks only (recommendation-bearing blocks in `walk` order first, then the rest) and writes only when a block moved.

### Writers that touch alternatives and recommendations

`embed_fragment` under `--recommendation` sets `principles`, `depends_on`, and `recommendation` and leaves `alternatives` untouched. Under `--alternatives` it takes the fragment's alternatives in their returned order. `strip_recommendation` clears the three recommendation-half fields and keeps `alternatives` in its current list order. `strip_question` also clears the alternatives. `remove --option`'s cascade strips dependents through `strip_recommendation`. `lift` reads the model, not line positions, so it is order-independent.

### Test suite

`tests/test_format.py` pins the canonical child order in `NON_CANONICAL`/`CANONICAL` (`test_render_normalizes_indentation_child_order_whitespace_and_escaping`), and it runs golden round-trips over `tests/fixtures/{annotated,bare,empty,entities}/open_questions.xml`. The `annotated` fixture holds recommendation-bearing blocks in today's order (recommendation last), so it must change for the round-trip identity to hold. `tests/test_embed.py` covers misordered fragments being grouped by kind (`test_embed_groups_misordered_children_by_kind`). The suite runs under both the pinned interpreter and the 3.9 floor.

### Runtime prose and docs that describe the order

`core/skills/recommend-all-open-questions/SKILL.md` says child order is the tool's (around line 194) and that the pass "never touches a block's `<alternative>` children" (line 25). `docs/skill-reference.md` and `docs/workflow.md` say `embed --recommendation` writes the block "with its `<alternative>` children untouched". `core/skills/capture-milestone-principle-updates/SKILL.md` reconstructs the answered block from removed diff lines keyed on tags, and it reads the alternatives "in document order" as "the options the user saw". Its extraction is element-agnostic, but that order will now put the recommended alternative first. No skill prose positions elements itself. Every host tree under `hosts/` is rendered from `core/` by `scripts/build_hosts.py` and must be rebuilt with the change.

## Decisions

### Unmatched recommendation option

A recommendation-bearing block whose `<recommendation>` option names none of its `<alternative>` ids is still rendered recommendation half first (`<applied-principle>`, `<depends-on>`, `<recommendation>` ahead of all alternatives); only the promotion is skipped, so the alternatives keep their existing relative order. The renderer rule is one stable move of the at most one alternative the option names, so an option naming nothing promotes nothing. The parser keeps accepting such a block and no write fails on it, so `strip --recommendation` remains the repair path; the mismatch continues to surface where it is refused today, at `remove --option`.

### Documents in the old order

An `open_questions.xml` written before this change converts lazily: it keeps the recommendation last until an existing writer (`add`, a `strip` that changes something, `embed`, `remove`, or a `sort` that moves a block) next saves it, and the reorder happens then. Nothing beyond the renderer changes — `sort` keeps its "writes only when a block moved" rule, read-only subcommands stay non-writing, and no conversion subcommand or migration is added.

### Alternatives-untouched contract wording

Every site claiming the recommendation pass or `embed --recommendation` leaves a block's `<alternative>` children untouched (the `recommend-all-open-questions` SKILL.md, `docs/skill-reference.md`, `docs/workflow.md`, and the CLAUDE.md invariants) is reworded to the frozen-set guarantee these files already use: the pass never adds, drops, or edits an alternative. None of those sites mentions child order; the order is stated once, in the tool's module docstring and `--help` canonical-form contract.

## Out of Scope

