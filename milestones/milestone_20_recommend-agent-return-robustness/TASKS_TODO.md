# TASKS TODO

## Report Only Still-Skipped Questions

Update steps 5 and 6 of `skills/recommend-all-open-questions/SKILL.md` so a question whose sub-elements were embedded only after extraction stripped surrounding text or after the single repair attempt gets no console mention at all, the step-6 advisory lists only questions still skipped after the repair path, and the step-5 all-skipped no-op wording describes that post-repair skip. This keeps the terse-reporting rule intact now that recovery exists; verify by reading both steps and confirming a recovered return is reported exactly like a clean one.

---

## Record Salvage Reversal In CLAUDE Invariants

Revise the `CLAUDE.md` invariants — the "Dispatched-agent return contracts are resumable and shape-checked" invariant, the recommend-sweep invariant, and the repository-layout line for the recommend agent — so they state the new behaviour and its rationale: the last-line verdict before extraction, the region extraction and acceptance gate, the single repair as continue-same-session versus fresh re-dispatch (Antigravity taking the re-dispatch branch), repair-on-arrival with the spent marker, the fixed single-slot corrective template, silent recovered returns, the agent's step-4-only draft → self-check → emit rewrite, and the deliberate reversal of "discarded whole, never salvaged", plus the scope boundary that `complete-task`, `answer-open-question-with-recommendation` and their orchestrators stay untouched because trailing text after a last-line token is not the same failure. The milestone needs this so a later editor does not restore the skip-only behaviour; verify by reading the invariants against the finished agent and skill files for contradiction.

---

## Update README Recommend Sweep Entries

Revise the `README.md` skill-reference entries for `recommend-all-open-questions` and `recommend-open-question (subagent)` so they describe the extraction of the sub-element region, the single repair attempt (same-session re-emit or fresh re-dispatch) and the skip-with-advisory that follows only a second failure, and the agent's draft → self-check → emit return. Verify by reading the two entries against the finished skill and agent files for consistency.

---

## Regenerate Antigravity Plugin Tree

Run `uv run scripts/migrate_skills_to_agy.py` so `.agents/plugins/cairn/` picks up the rewritten agent and sweep skill, confirming the transpiled skill reads the same two-branch repair prose and therefore takes the fresh re-dispatch branch where session continuation is unavailable. Verify with `diff -r` between the source and generated trees showing only the expected `${CLAUDE_PLUGIN_ROOT}` reference rewrites and dropped resolve hints.

---
