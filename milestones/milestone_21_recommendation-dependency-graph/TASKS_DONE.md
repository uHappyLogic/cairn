# TASKS DONE

## Replace Independence Clause With Disclosure Duty

Rewrite `shared/recommend-procedure.md` step 1 so the "never treat another question's recommendation as an input" clause is replaced by a caller-neutral disclosure duty: when a recommendation leans on a still-open sibling's recommendation, name that sibling and the option assumed. Add the one sentence `skills/discuss-open-question/SKILL.md` needs so its inline run renders that duty as prose. Verified by reading both files: no independence wording remains and the duty is stated once, in the core, with no XML markup.

**Verified:**

- `shared/recommend-procedure.md` step 1 contains no independence wording — no "formed in isolation", no "never treat another question's recommendation as an input".
- Step 1 states a caller-neutral disclosure duty once: when a recommendation leans on a still-open sibling's recommendation, name that sibling and the option assumed.
- The core carries no XML markup for the duty (no `<depends-on>` or other element name).
- `skills/discuss-open-question/SKILL.md` gains exactly one sentence directing its inline run to render that duty as prose (naming sibling and option), without restating the duty's substance or adding markup.
- No other step in either file changes.

---
