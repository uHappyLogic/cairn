# TASKS DONE

## Add the Question-Text List Flag

Give `list` in `core/tools/open_questions.py` a `--with-question` flag that prints each block on one line in document order as the un-escaped id, a single tab, then the un-escaped question text, changing only the line shape so it composes with `--without-alternatives` and `--without-recommendation` exactly as they select today, with no new refusal path. The docstring's `Subcommands:` section, the argparse help, and the output contract each state the tab separator, and `tests/test_list.py` gains tests asserting a literal tab, un-escaped values via the `entities` fixture, and the flag crossed with each filter alone and together. Verified by `uv run pytest` and the 3.9 floor run both passing and `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

**Verified:**

- `list --with-question` prints each selected block as the un-escaped id, one literal tab, then the un-escaped question text, one per line in document order (`tests/test_list.py` asserts the shape on the `annotated` and `bare` fixtures and un-escaped values on the `entities` fixture); without the flag the output is the bare id list as before, every existing `list` test still passing.
- The flag composes with `--without-alternatives` and `--without-recommendation`, alone and together, the filters selecting exactly the blocks they select without it, including a block whose recommendation alone was stripped; the diff adds no `ToolError`, so no new refusal path exists.
- The tab separator is stated at all three contract sites: the docstring's `Subcommands:` entry for `list`, the docstring's output contract, and the argparse `--with-question` help shown by `list --help`.
- `tests/test_list.py` gained tests asserting a literal tab (and no space beside it), un-escaped values via the `entities` fixture, the flag crossed with each filter alone and with both together, the empty-document and fully-annotated cases, the document left unchanged, and the in-process `main` path.
- `uv run pytest` passed (447 tests), the 3.9 floor run `uv run --no-project --python 3.9 --with pytest pytest` passed (447 tests), and `uv run scripts/build_hosts.py --check` passed after rebuilding `hosts/claude/` and `hosts/antigravity/`.

---

## Runner-Neutral Sibling Scope Wording

Rewrite step 1 of `core/shared/alternatives-procedure.md` so it states only the analytical rule that sibling questions bound this question, supply scope and nothing more, and are never presumed settled, dropping the instruction on how siblings are read so the procedure names no runner class and no reading mechanism. Confirm that `discuss-open-question` still states its own whole read of `open_questions.xml` in its own step, since each consumer now owns its sibling-scope source. Verified by reading the procedure for any remaining reading instruction and by `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

**Verified:**

- Step 1 of `core/shared/alternatives-procedure.md` states only the analytical rule: the milestone's sibling questions bound this question (marking where it ends and another begins, so an option that answers a sibling is left to it), supply scope and nothing more, and are never presumed settled while alternatives are enumerated.
- Step 1 carries no instruction on how siblings are read: a grep of the step for `whole`, `file-reading`, `locate`, `list`, `lift`, `open_questions.py`, `open_questions.xml`, `inline`, `subagent`, `agent`, and `skill` returns nothing, so the procedure names no runner class and no reading mechanism; the retired whole-read sentence and the tool-call sentence are gone.
- `core/skills/discuss-open-question/SKILL.md` step 2 still states its own whole read of `<MILESTONE_DIR>/open_questions.xml` with the file-reading tool (line 43), unchanged, so that consumer owns its sibling-scope source.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/` and `hosts/antigravity/` (only their `shared/alternatives-procedure.md` changed) and `uv run scripts/build_hosts.py --check` passed on the rebuilt trees.

---

## Alternatives Agent Fetches Its Own Question

Rework `core/agents/provide-alternatives-to-open-question.md` so its inputs are only the Short Title and the resolved milestone directory, and it reaches the question document through exactly two tool calls, one `locate` of its own Short Title for its block and one `list --with-question` for sibling scope, stated once as its only source of sibling scope, never running `locate` on a sibling, while still reading `requirements.md` whole as prose. Verified by the agent file naming no question-block input and no whole read of `open_questions.xml`, its description staying within the frontmatter cap, and `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

**Verified:**

- `## Inputs` of `core/agents/provide-alternatives-to-open-question.md` lists exactly two inputs, **Short Title** and **Milestone directory**, and the file names no question-block input: a case-insensitive grep for `question block` returns nothing, and the prompt is stated to carry no question text and no block.
- The agent reaches `open_questions.xml` through exactly two tool calls, both in step 1 as `python3 {{PLUGIN_ROOT}}/tools/open_questions.py …`: one `locate <MILESTONE_DIR> "<Short Title>"` on its own Short Title for its block (the block `locate` printed is the shared procedure's QUESTION input, and its `Error:` line is the `FAILED:` reason), and one `list --with-question <MILESTONE_DIR>` stated once as its only source of sibling scope, with the statement that it never runs `locate` on a sibling.
- The file states no whole read of `open_questions.xml`: every `whole` hit names `requirements.md` (read whole with the file-reading tool as prose, in Inputs and in step 1) or the alternatives return; the retired whole-read sentence over `open_questions.xml` is gone and the file says never to open or search that file itself.
- The frontmatter description is unchanged at 17 words, unquoted, one clause, with no colon or semicolon, within the 25-word cap the build enforces.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/` and `hosts/antigravity/` (only their `agents/provide-alternatives-to-open-question.md` changed) and `uv run scripts/build_hosts.py --check` passed on the rebuilt trees.

---

## Lean Alternatives Dispatch Prompt

Reduce the dispatch in `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` to the two slots the orchestrator already holds, the question's Short Title and the resolved milestone directory, dropping step 1's `locate` gather and the `Question block:` slot so the pass gathers in two `list` calls, with the repair path's re-dispatch still sending the same prompt plus the corrective message. Verified by the skill carrying no `locate` call and no block-holding prose, the per-return pipeline and commit steps unchanged, and `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

**Verified:**

- Step 1 of `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` gathers in two `list` calls (`list` and `list --without-alternatives`), sub-step c is gone, and the skill file contains no `locate` call or mention: a case-insensitive grep for `locate` returns nothing.
- The dispatch template carries exactly two slots, `Short Title:` and `Milestone directory:`, and the `Question block:` slot and all block-holding prose ("Hold these blocks", "the block its question's dispatch prompt carries", "the block is the only question text the prompt carries") are gone; the prompt is stated to carry no question text and no block, the subagent fetching its own block and sibling scope through the tool.
- The repair path's re-dispatch branch still sends the same prompt as the original dispatch with the corrective message appended.
- The per-return pipeline (sub-steps 3a–3d) and step 4 are byte-unchanged: every diff hunk lands in the opening paragraph's gather sentence, step 1, or the step-3 dispatch paragraph, and the frontmatter description is unchanged at 20 words.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/` and `hosts/antigravity/` (only their `skills/provide-alternatives-to-all-open-questions/SKILL.md` changed) and `uv run scripts/build_hosts.py --check` passed on the rebuilt trees.

---
