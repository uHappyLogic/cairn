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
