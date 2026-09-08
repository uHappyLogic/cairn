# TASKS DONE

## Rewrite Recommend Agent Return Step

Replace step 4 of `agents/recommend-open-question.md` from the ground up with a draft → self-check → emit step: it opens by naming step 3's rendering as the draft, its only test list is the two shape tests (first non-whitespace text starts with `<alternative`, last non-whitespace text ends with `</recommendation>`), the whole prohibition list and the "discarded whole, never salvaged" wording are dropped, and only the positive "every grounding finding is spent inside the elements" redirect survives as drafting guidance, with the `FAILED: <reason>` last-line failure return kept. Step 3 stays byte-for-byte untouched, and the milestone needs this because the wording-only fix of commit `2475078` already failed once (eight of ten milestone-19 dispatches were skipped); verify by reading the file and confirming step 3 is unchanged, step 4 carries no prohibition list, and the file holds runner-facing instructions only.

**Verified:**

- Step 4 of `agents/recommend-open-question.md` is a draft → self-check → emit step whose opening sentence names step 3's rendering as the draft ("The sub-elements you rendered in step 3 are a **draft**, not yet your final message").
- Step 4's only test list is the two shape tests, as a two-item numbered list: first non-whitespace text is `<alternative`, last non-whitespace text is `</recommendation>`.
- The whole prohibition list (grounding summary, "I have what I need", the facts-found/files-read list, the no-principle-bears note, closing remarks, the "no `DONE` line" item) and the "discarded whole … never salvaged" wording are gone — a grep for each of those phrases over the file returns no match.
- The positive redirect survives as drafting guidance: "Everything your grounding turned up is spent inside the elements — a bearing fact goes into an `<advantage>`, a `<drawback>`, or the rationale; a bearing principle goes into an `<applied-principle>`; the rest is dropped."
- The failure return is kept unchanged: the final paragraph still ends the session with `FAILED: <reason>` as its final line and nothing else.
- Step 3 is byte-for-byte untouched — the md5 of lines 51–98 is `9c7cdd01a6455dd02c6fc52662bfc59b` before and after the edit, and `git diff -U1` shows a single hunk confined to the step-4 region.
- The file holds runner-facing instructions only: the rewritten step 4 carries no rationale, no history of the earlier fix, and no `## Rules` section — every sentence is an instruction to the running agent.

---

## Add Extraction Gate To Recommend Sweep

Rework step 3 of `skills/recommend-all-open-questions/SKILL.md` so a return is judged in this order: first a last-line verdict (a last non-whitespace line beginning `FAILED:` is an explicit failure, skipped with that reason and never repaired, with a `FAILED:` token anywhere else being ordinary text), then extraction of the region from the first `<alternative` through the last `</recommendation>`, then a single acceptance gate over that region combining the two boundary tests with line-grep checks in the boundary-line CLI idiom (no `<open-question>`, `</open-question>`, `<question>`, or `</question>` line; exactly one `<recommendation` opening line; at least one `<alternative id` line; an `option` value, entity-unescaped and case-folded, equal to one of those alternative ids), with every miss producing a reason string that names the failed test. This replaces today's raw-return shape check so surrounding text never drops a valid recommendation; verify by reading the step and confirming the verdict precedes extraction, the gate needs no XML parser, and an accepted region is what reaches the step-4 Edit.

**Verified:**

- Step 3 of `skills/recommend-all-open-questions/SKILL.md` judges every return in one fixed order stated in its opening sentence and carried by the lettered sub-steps — last-line verdict (a), then extraction (b), then the acceptance gate (c) — with each stage running only on what the stage before it passed.
- The last-line verdict runs **before any extraction**: a last non-whitespace line beginning `FAILED:` is an explicit failure, skipped with the text after `FAILED:` as its reason, with no further attempt made on it even when an `<alternative>`…`</recommendation>` region sits above that line, and a `FAILED:` token anywhere else is ordinary text.
- Extraction takes the region from the line holding the first `<alternative` through the line holding the last `</recommendation>`, inclusive, discarding surrounding text as a strip rather than a failure, and fails only when no such line exists.
- A single acceptance gate over that region combines the two boundary tests (first non-whitespace text starts with `<alternative`, last non-whitespace text ends with `</recommendation>`) with the four line-grep checks: no `<open-question>` / `</open-question>` / `<question>` / `</question>` line, exactly one `<recommendation` opening line, at least one `<alternative id` line, and an `option` value — entity-unescaped and case-folded — equal to one of those alternative ids.
- The gate needs no XML parser: it is stated in step 1's line-oriented boundary-line CLI idiom (`awk`/`sed`/`grep` over lines and boundary tokens, never a real XML processor), and every one of its six tests is a first/last-text or line-grep test.
- Every miss produces a reason string naming the failed test — six concrete strings are given, one per test — and a miss, boundary or structural, is an extraction failure that skips that question alone, never a run stop.
- The raw-return shape check is gone: a grep for "shape check" over the file returns no match, and the accepted region — never the raw return — is what reaches step 4's Edit, which step 4's opening sentence now states ("Only the regions step 3's acceptance gate accepted reach this step").
- The file stays runner-facing: the rewritten step carries no rationale, no history, and no `## Rules` section, and steps 0–2 and 4's embedding mechanics are otherwise unchanged.

---

## Add Single Repair Attempt To Sweep

Extend step 3 of `skills/recommend-all-open-questions/SKILL.md` so an extraction failure triggers exactly one repair before any skip, as a two-branch instruction: where the host can continue the finished session (Claude Code's `SendMessage` to the returned agent id) send a corrective re-emit message to that same agent, and where it cannot (no continuation equivalent, as under Antigravity, or the handle is gone) re-dispatch one fresh `cairn:recommend-open-question` agent with the same prompt plus the shape reminder; the repaired or second return runs through the same last-line verdict and extraction gate, and only a second miss falls to skip-with-advisory. Repairs happen on arrival inside a single per-return pipeline (check, repair once, re-check, embed or skip) overlapping in-flight dispatches, guarded by a per-question "repair spent" marker, and the corrective message is a fixed one-paragraph template rendered once in the skill with a single slot that quotes both shape tests verbatim, is filled with the same failed-test reason string the gate derives, never quotes the offending prose back, and closes by asking for the sub-elements and nothing else; verify by reading the step and confirming both branches, the on-arrival timing, the spent marker, and the template are present and that no question can be repaired twice.

**Verified:**

- Step 3 of `skills/recommend-all-open-questions/SKILL.md` states the judging order as last-line verdict, extraction, acceptance gate, then a single repair attempt when the gate rejects, and the closing sentence of sub-step c routes every extraction/gate miss into that repair instead of an immediate skip ("an extraction failure is never an immediate skip: it takes the single repair attempt of sub-step d").
- Sub-step d grants **exactly one** repair attempt before any skip to a return that passed the last-line verdict but failed extraction (b) or the acceptance gate (c); an explicit `FAILED:` last-line return still gets no repair, as sub-step a's "make no further attempt on it" is unchanged.
- Both branches are present and ordered: continue the same agent session (Claude Code's `SendMessage` to the agent id the `Agent` tool returned, context intact) where the host supports it, and otherwise — no session-continuation equivalent, as under Antigravity, or the handle is gone — one fresh `cairn:recommend-open-question` dispatch with the same prompt plus the corrective message appended as a shape reminder.
- The timing is on-arrival inside a single per-return pipeline: the step's opening sentence names the four stages as "one per-return pipeline" (judge, repair once, re-judge, embed or skip) and d repairs "as it arrives … while the other dispatches are still in flight", explicitly ruling out holding failed returns for a second phase.
- A per-question repair-spent marker is carried — unset at dispatch, set as the repair is issued, repair only when unset — so no question can be repaired twice; a failing return whose marker is already set goes straight to the skip.
- The corrective message is a fixed one-paragraph template rendered exactly once in the skill (one fenced block, no blank line inside it) with the single slot `<failed test>`, quoting both shape tests verbatim ("first non-whitespace text starts with `<alternative`", "last non-whitespace text ends with `</recommendation>`"), filled with the same failed-test reason string b/c derive for the advisory, never quoting the offending prose back, and closing with "Send those sub-elements and nothing else".
- The repaired or second return is re-judged by sub-steps a, b and c exactly as a first return is, and only a second failure is a skip of that question alone with its reason noted for the step-6 advisory, never a run stop.
- The file stays runner-facing: the added prose is instructions to the running orchestrator, with no rationale, no history, and no `## Rules` section.

---

## Report Only Still-Skipped Questions

Update steps 5 and 6 of `skills/recommend-all-open-questions/SKILL.md` so a question whose sub-elements were embedded only after extraction stripped surrounding text or after the single repair attempt gets no console mention at all, the step-6 advisory lists only questions still skipped after the repair path, and the step-5 all-skipped no-op wording describes that post-repair skip. This keeps the terse-reporting rule intact now that recovery exists; verify by reading both steps and confirming a recovered return is reported exactly like a clean one.

**Verified:**

- Step 6 of `skills/recommend-all-open-questions/SKILL.md` prints alongside the terse line **only** the questions step 3 still skipped after the repair path, naming the two cases exactly: a return whose last non-whitespace line began `FAILED:` (sub-step a), or one that failed extraction or the acceptance gate again after its one repair attempt (sub-step d).
- The advisory carries each still-skipped question's Short Title with the reason it was skipped on — the second reason where a repair was spent — one per line, and its git-absent justification is unchanged.
- Step 6 states that a question that was annotated gets no console mention at all, however its return reached step 4 — clean arrival, extraction stripping surrounding text (sub-step b), or acceptance only after the single repair attempt (sub-step d) — so a recovered return is reported exactly like a clean one, with no recovered-or-repaired listing, count, or note.
- Step 5's dirty-own-path no-op wording describes the all-skipped case as "every dispatched question was **still skipped after its repair attempt** in step 3", not a bare step-3 skip.
- Step 6's no-op message wording matches it — "every dispatched question was still skipped after its repair attempt in step 3" — and is still followed by the still-skipped-question advisory when there was one.
- The terse success line `Recommendations embedded.` and its "no annotated-vs-skipped breakdown, no per-question listing" clause are unchanged, so the terse-reporting rule stays intact.
- Only steps 5 and 6 changed (`git diff -U0` shows hunks confined to that region), the file stays runner-facing with no rationale, history, or `## Rules` section, and the frontmatter is untouched.

---
