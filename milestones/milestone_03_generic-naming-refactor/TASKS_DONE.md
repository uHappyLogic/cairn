# TASKS DONE

## Rename Answer-Sweep Orchestrator To Fan-Out Form

Rename the answer-sweep orchestrator skill `try-answer-questions-by-principle` → `try-answer-all-questions-by-principle` (the fan-out grammar `<verb>-all-<plural-object>` form, applied because this orchestrator shares the verb "answer" with its per-item worker) and update every cross-reference to the orchestrator's handle across the plugin. This is one of the milestone's order-free renames; the read-only candidate-elimination subagent `try-answer-question-by-principle` is deliberately NOT renamed.

**Provides:**
- The renamed orchestrator handle and skill directory `try-answer-all-questions-by-principle` (directory name IS the slash-command name), referenced by sibling rename tasks and the docs.

**Notes:**
- The orchestrator handle is the *plural* string `try-answer-questions-by-principle`; the subagent handle is the *singular* `try-answer-question-by-principle`. They are distinct strings — grep the plural form so the singular subagent is left untouched, including its dispatch string inside the orchestrator, which must stay exactly `try-answer-question-by-principle`.
- The live orchestrator-handle references are in: `skills/try-answer-questions-by-principle/SKILL.md` (its own self-references + the directory rename), `skills/reject-auto-answer/SKILL.md`, `skills/try-capture-answer-principle/SKILL.md`, `shared/answer-procedure.md`, `agents/try-answer-question-by-principle.md` (the subagent file names its parent orchestrator), `README.md` (Mermaid workflow node + per-skill reference-table row), `CLAUDE.md` (repository-layout + skills-overview + invariants mentions), and the single live header cross-reference line in `milestones/answer_decision_principles.md`.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` do NOT reference this handle, so no manifest edit is needed.
- Per the milestone's *Rename ordering* decision, this task syncs its own `README.md` and `CLAUDE.md` references rather than deferring to a trailing doc-sync pass.
- Do not edit frozen surfaces: historical milestone dirs (`milestone_01_*`, `milestone_02_*`), milestone_03's own `requirements.md`/`TASKS_*`, the history/completed sections of `milestones/README.md`, the `Origin:` provenance lines in `answer_decision_principles.md`, and `.claude/settings.local.json`.

**Success:**
- `git grep try-answer-questions-by-principle` over live plugin surfaces (`skills/`, `agents/`, `shared/`, `README.md`, `CLAUDE.md`, `.claude-plugin/`, the live lines of `milestones/answer_decision_principles.md`) returns zero hits.
- Directory `skills/try-answer-all-questions-by-principle/` exists with its `SKILL.md`; the old `skills/try-answer-questions-by-principle/` directory no longer exists.
- The subagent handle `try-answer-question-by-principle` is unchanged everywhere it appeared (orchestrator dispatch string, `agents/try-answer-question-by-principle.md`, README, CLAUDE.md).
- The README Mermaid node + skill-table row and the CLAUDE.md invariants read coherently with the new `try-answer-all-questions-by-principle` handle.

---

