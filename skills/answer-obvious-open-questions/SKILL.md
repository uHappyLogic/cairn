---
name: answer-obvious-open-questions
description: Sweep the current milestone's requirements for open and deferred questions and resolve only the ones that have a clear, low-risk answer — recording each decision and leaving the genuinely contentious ones untouched for the user to discuss. Use this right after /highlight-milestone-requirements-open-questions to clear out the easy questions in one pass, or whenever the requirements have accumulated several open questions and you want the obvious ones answered before spending time on the hard ones. Trigger it whenever the user says things like "answer the obvious ones", "resolve the clear-cut open questions", "knock out the easy questions", or "auto-answer what you can" about a milestone's open questions.
---

# answer-obvious-open-questions

`highlight-milestone-requirements-open-questions` flags every gap it can see, before anyone has read the actual code. Many of those flags turn out to have one obviously-right answer once you look at the real project state — there is nothing to discuss, only a decision to record. This skill is the cleanup pass for exactly those: it reads each open or deferred question, grounds itself in the live codebase, and **answers only the ones where the choice is clear and low-risk**, leaving every genuinely contentious question exactly as it found it.

The value is the restraint. Answering an easy question saves the user a round-trip; "answering" a hard one by guessing buries a real decision the user needed to make. When in doubt, leave it.

## Usage

```
/answer-obvious-open-questions
```

Takes no arguments — it considers every `Open question` and `Deferred` entry in the current milestone's `requirements.md`.

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded backlog path.

### 1. Collect the questions

Read `<MILESTONE_DIR>/requirements.md` in full. Gather every `Open question — <Title>` and `Deferred — <Title>` entry, in document order. If there are none, say so and stop — there is nothing to do.

### 2. Process each question sequentially against the live document

Work through the questions **one at a time, re-reading the current state of the document between each**. This matters: answering one question may moot another or constrain its answer (see step 2c). If you form all your recommendations up front and apply them as a batch, you will act on stale, possibly contradictory state. Decide and apply one question fully before moving to the next.

For each question:

**a. Form a recommendation from the real project state.** Read the source files, scripts, or design docs the question actually bears on — prefer reading the code over reasoning from memory, exactly as `discuss-open-question` would. Internally weigh the realistic alternatives and settle on the option you'd recommend. You don't write this deliberation into the document; it's how you reach a decision and judge its strength.

**b. Apply the strength gate.** Answer the question **only if all of these hold**:
- You can name a single concrete decision (not "it depends" or "either could work").
- A reasonable, informed person looking at the same code would almost certainly agree on sight — you would not feel the need to lay out alternatives and ask first.
- It is low-risk to reverse if it turns out wrong.

If you find yourself wanting to present options before committing, the recommendation is **not** strong enough — leave the question untouched. This is the same threshold `highlight` uses in reverse ("don't block if a reasonable low-risk choice exists"); here you're confirming that low-risk choice and recording it.

**Deferred entries get a higher bar.** The `Deferred` tag is itself a signal that the decision wants implementation-time context. Default to leaving deferred entries alone. Only resolve one if it's actually a stable architectural choice that was mis-filed as deferred — not a genuine "tune this later".

**c. If the recommendation is strong, record it** the same way `/answer-open-question` does — do not invent a different mechanism:
- **Remove the matched question block** from the document entirely.
- **Fold the decision into `## Implementation decisions`** — add a concise requirement statement under the relevant subsection (or a new subsection), capturing what was decided and any constraint it imposes. (Match the live document's section names; this is where decisions live in `requirements.md`.)
- **Cascade**: if the decision moots another open/deferred entry or forces its answer, remove that entry too and fold any implied constraint into `## Implementation decisions`. Then continue to the next question against this now-updated document.

Make these as separate, targeted edits — one per logical change — rather than one large rewrite of a long file.

**d. If the recommendation is not strong, leave the question exactly as written.** Do not annotate it, soften it, or restructure it. A question left for the user must look untouched.

### 3. Report

Summarise in two short lists:

- **Answered** — for each: the title, the decision in one line, and a one-line rationale for why it was clear-cut. Note any cascaded resolutions.
- **Left for you** — for each: the title and a one-line reason it needs a real decision (what's genuinely at stake / why no single answer dominates).

Then suggest the natural next step for the remaining ones: `/discuss-open-question <Title>` to talk one through, or `/answer-open-question <Title>. <answer>` if the user already knows the call.

## Rules

- Bias hard toward leaving questions alone. The cost of skipping an easy one is a single extra round-trip; the cost of guessing a hard one is a real decision silently made for the user. Restraint is the whole point.
- Resolve questions only by reading the real code, not from memory or assumption.
- Record answers exactly as `/answer-open-question` does — remove the block, fold the decision into `## Implementation decisions`, cascade. Don't introduce a parallel recording format.
- Do not restructure or rewrite existing content beyond removing answered blocks and adding the decisions they produce.
- Do not commit. Like every skill here, this leaves its changes staged for the user to review.
- If answering one question surfaces a brand-new question that wasn't already in the document, mention it in the report but do **not** add it to the document without the user's confirmation.
