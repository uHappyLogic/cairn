# TASKS TODO

## Lean Alternatives Dispatch Prompt

Reduce the dispatch in `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` to the two slots the orchestrator already holds, the question's Short Title and the resolved milestone directory, dropping step 1's `locate` gather and the `Question block:` slot so the pass gathers in two `list` calls, with the repair path's re-dispatch still sending the same prompt plus the corrective message. Verified by the skill carrying no `locate` call and no block-holding prose, the per-return pipeline and commit steps unchanged, and `uv run scripts/build_hosts.py --check` passing on the rebuilt host trees.

---

## Record Dispatch Invariants in CLAUDE.md

In the sole-writer invariant of `CLAUDE.md`, reword the whole-file allowance to name its holders as a class, a user-invoked skill running inline in the conversation or a shared procedure followed by one, and add beside it the reading ban that dispatched agents reach the question document only through the tool; then add a new invariant, scoped to dispatched agents, that a dispatch prompt carries only what the orchestrator already holds and the agent cannot fetch itself, holding for both dispatched agents without qualification and with its rationale. Verified by reading the two invariants against the milestone's recorded decisions and by the `complete-task` agent's whole read of `TASKS_TODO.md` needing no carve-out.

---

## Update Docs for Lean Dispatch

Update the `provide-alternatives-to-all-open-questions` and `provide-alternatives-to-open-question` entries of `docs/skill-reference.md` so the pass gathers in two `list` calls with no `locate` and the agent is given only its Short Title and milestone directory, fetching its block with `locate` and its sibling scope with `list --with-question` while reading `requirements.md` whole, and correct any other sentence under `docs/` that describes the prompt's contents or the agent's whole read of `open_questions.xml`. Verified by grepping `docs/` for the retired descriptions and finding none.

---
