# TASKS TODO

## Add Extraction Gate To Recommend Sweep

Rework step 3 of `skills/recommend-all-open-questions/SKILL.md` so a return is judged in this order: first a last-line verdict (a last non-whitespace line beginning `FAILED:` is an explicit failure, skipped with that reason and never repaired, with a `FAILED:` token anywhere else being ordinary text), then extraction of the region from the first `<alternative` through the last `</recommendation>`, then a single acceptance gate over that region combining the two boundary tests with line-grep checks in the boundary-line CLI idiom (no `<open-question>`, `</open-question>`, `<question>`, or `</question>` line; exactly one `<recommendation` opening line; at least one `<alternative id` line; an `option` value, entity-unescaped and case-folded, equal to one of those alternative ids), with every miss producing a reason string that names the failed test. This replaces today's raw-return shape check so surrounding text never drops a valid recommendation; verify by reading the step and confirming the verdict precedes extraction, the gate needs no XML parser, and an accepted region is what reaches the step-4 Edit.

---

## Add Single Repair Attempt To Sweep

Extend step 3 of `skills/recommend-all-open-questions/SKILL.md` so an extraction failure triggers exactly one repair before any skip, as a two-branch instruction: where the host can continue the finished session (Claude Code's `SendMessage` to the returned agent id) send a corrective re-emit message to that same agent, and where it cannot (no continuation equivalent, as under Antigravity, or the handle is gone) re-dispatch one fresh `cairn:recommend-open-question` agent with the same prompt plus the shape reminder; the repaired or second return runs through the same last-line verdict and extraction gate, and only a second miss falls to skip-with-advisory. Repairs happen on arrival inside a single per-return pipeline (check, repair once, re-check, embed or skip) overlapping in-flight dispatches, guarded by a per-question "repair spent" marker, and the corrective message is a fixed one-paragraph template rendered once in the skill with a single slot that quotes both shape tests verbatim, is filled with the same failed-test reason string the gate derives, never quotes the offending prose back, and closes by asking for the sub-elements and nothing else; verify by reading the step and confirming both branches, the on-arrival timing, the spent marker, and the template are present and that no question can be repaired twice.

---

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
