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
