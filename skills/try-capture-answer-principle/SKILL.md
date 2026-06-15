---
name: try-capture-answer-principle
description: Extract a reusable, user-confirmed answering principle from a decision just made about a milestone open question, and record it in the project-wide principle store (milestones/answer_decision_principles.md). Runs automatically after /answer-open-question records a manual answer, and is also directly invocable to generalize a specific decision. Use it whenever the user says things like "capture that as a principle", "remember this for next time", "turn that decision into a rule", "teach the auto-answerer", or "save this answering principle" — and after answering an open question when the reasoning behind the call looks reusable. It analyzes the conversation, exits quietly when nothing generalizes, and only ever proposes a revise-or-add to the user — never editing the store silently.
---

# try-capture-answer-principle

The autonomous sweep `try-answer-questions-by-principle` can only resolve an open question when a **confirmed answering principle** covers it. This skill is how those principles get into the store: it watches a real decision being made, asks "is there a reusable rule behind this, beyond this one question?", and — only when there is — records it as a generalizable keep/eliminate directive that future sweeps can apply.

The principles live in `milestones/answer_decision_principles.md` (a single project-wide file at the `milestones/` root, **above** any one milestone, so principles accumulate across milestones). This skill is the **sole writer** of that file — presence of an entry means it is confirmed.

The value is restraint plus user confirmation. A principle governs *every* future autonomous answer, so a wrong or sloppy one corrupts the highest-value artifact in the loop. This skill therefore captures only genuinely reusable rules, and never writes the store without the user's explicit say-so.

## Usage

```
/try-capture-answer-principle [optional free-text focus hint]
```

- **No argument (the primary entry).** Its main use is as an unconditional chain-off appended to `/answer-open-question`: after a manual answer is recorded, that skill invokes this one. Because capture runs **inline in the same conversation**, the full deliberation — the alternatives weighed in any `/discuss-open-question`, the trade-off articulated, the decision reached — is in context. Capture analyzes that conversation **anchored on the most recent decision**.
- **Free-text focus hint (optional).** A short phrase naming which decision to generalize, used to disambiguate a conversation that covered several decisions, or when `/reject-auto-answer` chains in to revise a specific offending principle (the hint names that principle).

This skill takes **no required parameter** and does **not** take a `(Short Title, decision prose)` payload — a principle generalizes the *rule behind* a decision, which lives in the deliberation (the alternatives, the trade-off), not in the clean prose folded into `## Implementation decisions`. The conversation is the source.

> Note: this skill writes **only** the principle store at the fixed path `milestones/answer_decision_principles.md`. It does **not** touch any milestone's `requirements.md`, so it does **not** resolve `<MILESTONE_DIR>` and must not call `get-current-milestone`.

## Workflow

### 1. Identify the decision to generalize

Settle on the single decision this run is about:

- **Chained from `/answer-open-question` (no hint):** anchor on the **most recent decision** in the conversation — the answer just recorded.
- **A focus hint was given:** use it to pick the decision (or the existing principle, when `/reject-auto-answer` chains in to revise one) the user pointed at.
- **Invoked cold with no relevant deliberation in context:** do **not** silently no-op and do **not** guess. **Ask the user** which decision they want to generalize, then continue.

### 2. Judge whether a reusable principle can be extracted

Look at the deliberation behind the chosen decision: the realistic alternatives that were weighed, the reason one was chosen over the others, the trade-off that was accepted. Ask whether that reasoning generalizes into a rule that could decide a **different future question**.

A principle must be a **reusable directive, not a restatement of one past decision** — this is the whole point of capturing it. It has to be phrased so it can be applied as a keep/eliminate test against the realistic candidate answers to a *future* question ("binary in/out": applied to a candidate, the principle says in = supportable/keep, or out = eliminate).

Contrast the two:

- **Restatement (do not capture):** "Auto-answer commit isolation uses a clean tree then commit, not scoped staging." This names one question and one answer; it cannot judge a candidate for any *other* question.
- **Reusable directive (capture this):** "When choosing between mechanisms that achieve the same goal, prefer the one that makes a property a hard invariant over one that only enforces it best-effort — even at some cost in flexibility." This is a test you can apply to the candidate answers of an unrelated future question.

(That reusable form is the model — see the *Principle entry schema* example in `requirements.md`, "Invariant over best-effort", which is exactly this decision generalized.)

**If no generalizable principle can be extracted** — the decision was a one-off, situation-specific, or just not worth generalizing — **report that briefly and exit without engaging the user further.** Do not run the revise-vs-add flow on a non-candidate. Only a real candidate proceeds to step 3.

### 3. Decide revise-vs-add — by semantic overlap, with user confirmation

This step never edits the store on its own judgment. Decide between revising an existing principle and adding a new one **by semantic overlap, confirmed by the user — never by title alone, and never silently.**

1. **Read the entire `milestones/answer_decision_principles.md`.** It is small and grows slowly, so reading it whole is always feasible. If the file does not exist or is empty, there are no existing principles — this will be an add (step 4 creates the store).
2. **Find the principles whose *statements* (not just their `### <Short Title>` headings) bear on the candidate** — the ones that overlap in meaning, even if they are filed under a different title. An exact (case-insensitive) **title collision is only a strong hint** that pre-selects a likely revise target; it is not the deciding test. The deciding test is semantic.
3. **Surface the related set to the user and let them make the final call:** revise one of the existing principles (and how), or add a new entry. Show the candidate principle you extracted and the overlapping existing entries so the choice is informed.
4. **Never auto-merge or auto-add without that confirmation.** If nothing overlaps, still present the new entry for confirmation before writing.

### 4. Write the entry per the principle schema

Apply the user's confirmed choice to `milestones/answer_decision_principles.md`:

- **Add:** append a new subsection. **If the file does not exist, create it on first write** (this skill is its sole writer).
- **Revise:** edit the body (and, if the user chose, the heading) of the existing `### <Short Title>` subsection in place.

Each entry follows this schema — one principle per subsection:

```markdown
### <Short Title>

<The principle as a generalizable keep/eliminate directive — a reusable decision
rule that can be applied to the candidate answers of a future question, not a
restatement of one past decision.>

*Origin: <originating question or example>*
```

- **`### <Short Title>` heading — the handle.** A 2–5 word unique name, mirroring the open-question Short-Title convention. This is the citable key the sweep writes to the `Answer-Principle:` commit trailer, and the key this skill matches on for revise-vs-add. No separate ID scheme.
- **Body — the directive in prose.** Generalizable keep/eliminate rule, per step 2. Not a restatement of the originating decision.
- **`*Origin:*` line — optional.** A pointer to the originating question or example, to aid human auditing and future overlap judgments. Omit it when there is nothing useful to record. The sweep applies the *statement*, not the origin.
- **No status field.** Presence in the file means confirmed.

### 5. Report

Briefly state what was captured: the principle's `### <Short Title>`, whether it was added or a revision of an existing entry, and that it is now available to `try-answer-questions-by-principle`. If nothing was captured (step 2 found no candidate, or the user declined), say so in one line.

## Rules

- This skill is the **sole writer** of `milestones/answer_decision_principles.md`. Never write it without explicit user confirmation of the revise-or-add choice (step 3).
- Decide revise-vs-add by **semantic overlap with user confirmation** — never by title alone, never auto-merge or auto-add silently.
- A captured principle must be a **generalizable keep/eliminate directive**, not a restatement of one decision. If the reasoning does not generalize, capture nothing.
- When no generalizable principle can be extracted, **report briefly and exit without engaging the user** — only a real candidate runs the revise-vs-add flow.
- Invoked cold with no relevant deliberation in context, **ask the user** which decision to generalize rather than guessing or no-op'ing.
- Write **only** the principle store at `milestones/answer_decision_principles.md`; never touch `requirements.md`, and never resolve `<MILESTONE_DIR>`.
- **Do not commit.** Like every skill here, this leaves its edit to the principle store staged for the user to review.
