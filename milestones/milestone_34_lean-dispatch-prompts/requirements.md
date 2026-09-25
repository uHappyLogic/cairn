# Milestone 34: Lean dispatch prompts

## Goal

Dispatch prompts carry only what the orchestrator already holds and the agent cannot fetch itself. The alternatives orchestrator passes each subagent the question's Short Title and the resolved milestone directory, dropping its locate gather and the block from the prompt; the agent fetches its own block with locate and its sibling scope with a new list flag that prints each id with its question text, never reading open_questions.xml whole, while still reading requirements.md whole as prose. The rule is recorded as a CLAUDE.md invariant scoped to dispatched agents, with the whole-file allowance reworded to name the inline runners, and the tool, tests, docs, and host trees updated to match.

## Relevant starting state

### The alternatives orchestrator

`core/skills/provide-alternatives-to-all-open-questions/SKILL.md` gathers in three tool calls: `list`, `list --without-alternatives`, and one `locate` over every id the filter printed, holding each verbatim block as "the block its question's dispatch prompt carries". Its step 3 dispatches `cairn:provide-alternatives-to-open-question` with a fixed three-slot prompt — `Short Title:`, `Milestone directory:`, `Question block:` — and states that the block is the only question text the prompt carries, the subagent reading the milestone's documents itself for grounding. The repair path re-dispatches with "the same prompt plus" the corrective message, so the prompt template has two consumers inside the skill. The other dispatch site, `core/skills/complete-all-tasks/SKILL.md`, already passes its agent only the task's `##` heading text and nothing else; the agent locates the task itself.

### The alternatives agent

`core/agents/provide-alternatives-to-open-question.md` lists three inputs under `## Inputs` — Short Title, the resolved milestone directory, and the question block as "your primary source" — and its step 1 reads `<MILESTONE_DIR>/open_questions.xml` whole with the file-reading tool "exactly as you read `requirements.md`", for the sibling scope, while stating that every locate, list, or lift of a block is a tool call. Its frontmatter description already reads "invoked with that question's Short Title as the prompt"; the description names no block. Its `color` key is stripped only by the Antigravity host definition.

### The shared enumeration half

`core/shared/alternatives-procedure.md` step 1 carries its own copy of the whole-read sentence: the siblings in `open_questions.xml` are "read whole with the file-reading tool, exactly as `requirements.md` is read beside it", scope only, reasoning only. That procedure has two consumers, the dispatched agent and the inline `discuss-open-question`, so any change to its wording lands on an inline runner too. The pick half, `recommend-procedure.md`, is consumed only by inline runners.

### The open-question tool

`core/tools/open_questions.py` (1227 lines, stdlib, 3.9+) offers `list` — bare un-escaped ids, one per line, document order, with `--without-alternatives` and `--without-recommendation` filters — and `locate`, which prints each named block verbatim via `_question_lines`. The model's `Question` dataclass holds `id` and `question` (the `<question>` text, folded to one line on every write, so no question text spans lines); reads print un-escaped values. The subcommand contract is stated in three mirrored places — the module docstring's `Subcommands:` section, the argparse `help` strings, and the docstring's "Output and error contract" — and `list`'s flags are declared on `list_parser` in the argparse block near line 1037. No subcommand today prints a question's text beside its id.

### The test suite

`tests/test_list.py` holds fourteen tests (document order, un-escaped ids via the `entities` fixture, both filters singly and together, empty and bare and fully annotated documents, unchanged document, missing and malformed document, unknown flag as usage error, in-process `main`). `tests/test_locate.py` covers verbatim printing, order, case-folding, dedup, and unknown ids. `tests/test_contract.py` asserts `--help` lists every subcommand name. Golden fixtures live under `tests/fixtures/{annotated,bare,empty,entities}/open_questions.xml`; the `entities` fixture's one id contains `&`, `<`, `>`, `"`, and `'`. Both runs (`uv run pytest` and the 3.9 floor) must pass before a tool change is committed.

### The CLAUDE.md invariants

The sole-writer invariant in `CLAUDE.md` carries the whole-file allowance as one sentence: "A consumer that needs the whole set to reason over reads the file directly, for reasoning only." It is not scoped to inline runners; the inline runners that use it are `review-milestone-requirements`, `recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, `discuss-open-question`, `ask-in-milestone-context`, and `modify-milestone-goal`, each stating it in its own step. The "Dispatched-agent return contracts" invariant is the one existing agent-scoped invariant; there is no invariant on what a dispatch prompt may carry. `docs/design-claims.md` claim 13 ("smallest necessary context") says the orchestrator holds no work context and gets back only bare tokens or ready-to-embed elements, but says nothing about what goes into a prompt.

### The docs

`docs/skill-reference.md` describes the orchestrator's `locate` print as "the block each dispatch prompt carries" and the agent as "given one question's Short Title, its milestone directory, and its block as the tool's `locate` printed it", reading both documents whole. `docs/workflow.md` (lines 55 and 164) names the dispatch and its per-question commit but not the prompt's contents; `docs/ways-of-using-cairn.md` says only "one subagent per question"; `README.md` names neither the prompt nor the agent.

### Host trees and build

`hosts/claude/` and `hosts/antigravity/` are rendered from `core/` by `uv run scripts/build_hosts.py`, each carrying `agents/provide-alternatives-to-open-question.md` and `tools/open_questions.py`; `--check` is the drift gate CI runs before both pytest runs. Antigravity's `settings.toml` strips `color` and has no session-continuation, so its repair arm is the fresh re-dispatch with the same prompt.

### Scale of a whole read

Milestone 33's `open_questions.xml` held three questions and reached about 15 KB at its fullest (after the recommendation pass); its `Alternatives-annotation:` commits numbered three. A subagent dispatched under the current agent reads that whole document plus `requirements.md` in addition to the block already in its prompt, so the block is presently delivered twice.

## Decisions

### The question-text list flag

`list` gains a `--with-question` flag that prints each block on one line in document order: the un-escaped id, a single tab, then the block's un-escaped question text. The tab is unambiguous by construction because every write folds whitespace runs to one space, so neither an id nor a question can contain one; the one-line, bare, un-escaped read contract stays intact. The docstring's `Subcommands:` section, the argparse help, and the output contract each state the tab separator, and tests assert a literal tab.

## Out of Scope

