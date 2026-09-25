# TASKS TODO

## Runner-Neutral Sibling Scope Wording

Rewrite step 1 of `core/shared/alternatives-procedure.md` so it states only the analytical rule that sibling questions bound this question, supply scope and nothing more, and are never presumed settled, dropping the instruction on how siblings are read so the procedure names no runner class and no reading mechanism. Confirm that `discuss-open-question` still states its own whole read of `open_questions.xml` in its own step, since each consumer now owns its sibling-scope source. Verified by reading the procedure for any remaining reading instruction and by `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

---

## Alternatives Agent Fetches Its Own Question

Rework `core/agents/provide-alternatives-to-open-question.md` so its inputs are only the Short Title and the resolved milestone directory, and it reaches the question document through exactly two tool calls, one `locate` of its own Short Title for its block and one `list --with-question` for sibling scope, stated once as its only source of sibling scope, never running `locate` on a sibling, while still reading `requirements.md` whole as prose. Verified by the agent file naming no question-block input and no whole read of `open_questions.xml`, its description staying within the frontmatter cap, and `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

---

## Lean Alternatives Dispatch Prompt

Reduce the dispatch in `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` to the two slots the orchestrator already holds, the question's Short Title and the resolved milestone directory, dropping step 1's `locate` gather and the `Question block:` slot so the pass gathers in two `list` calls, with the repair path's re-dispatch still sending the same prompt plus the corrective message. Verified by the skill carrying no `locate` call and no block-holding prose, the per-return pipeline and commit steps unchanged, and `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

---

## Record Dispatch Invariants in CLAUDE.md

In the sole-writer invariant of `CLAUDE.md`, reword the whole-file allowance to name its holders as a class, a user-invoked skill running inline in the conversation or a shared procedure followed by one, and add beside it the reading ban that dispatched agents reach the question document only through the tool; then add a new invariant, scoped to dispatched agents, that a dispatch prompt carries only what the orchestrator already holds and the agent cannot fetch itself, holding for both dispatched agents without qualification and with its rationale. Verified by reading the two invariants against the milestone's recorded decisions and by the `complete-task` agent's whole read of `TASKS_TODO.md` needing no carve-out.

---

## Update Docs for Lean Dispatch

Update the `provide-alternatives-to-all-open-questions` and `provide-alternatives-to-open-question` entries of `docs/skill-reference.md` so the pass gathers in two `list` calls with no `locate` and the agent is given only its Short Title and milestone directory, fetching its block with `locate` and its sibling scope with `list --with-question` while reading `requirements.md` whole, and correct any other sentence under `docs/` that describes the prompt's contents or the agent's whole read of `open_questions.xml`. Verified by grepping `docs/` for the retired descriptions and finding none.

---
