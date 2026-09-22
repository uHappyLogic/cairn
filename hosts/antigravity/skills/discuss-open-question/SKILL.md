---
name: discuss-open-question
description: Discuss a named open question in the current milestone requirements, surfacing alternatives, trade-offs, and a recommendation to help the user decide.
---

# discuss-open-question

Facilitates a deliberation on a named `<open-question>` block in the current milestone's `open_questions.xml` where the user cannot give an immediate answer. The goal is a concrete decision by the end of the conversation — not a design document. The skill is purely conversational: it never edits `open_questions.xml`, `requirements.md`, or any other file. It works on a block in **any state** — bare, carrying the `<alternative>` set the alternatives pass embedded, or carrying that set plus the `<recommendation>` the recommendation pass picked — and the state decides only where the option set comes from: an embedded alternative set is reused as it stands, never re-enumerated, and a bare block gets its options enumerated here first. The pick is always this skill's own, formed afresh over that set, and shown beside the sweep's standing pick when the block carries one.

## Usage

```
/discuss-open-question <Short Title>
```

The `<Short Title>` must match (case-insensitive) the `id` of an existing `<open-question>` block in `<MILESTONE_DIR>/open_questions.xml`.

**Example:**
```
/discuss-open-question Getting-started section order
```

## Workflow

### 0. Find the current milestone

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Locate the question

Locating a block by its handle is a deterministic lookup, so it is a call to the plugin's open-question tool — the sole writer of `<MILESTONE_DIR>/open_questions.xml`, and the only way this skill ever locates, lists, or lifts a block:

```
python3 .agents/plugins/cairn/tools/open_questions.py locate <MILESTONE_DIR> "<Short Title>"
```

On success it prints the **whole matched block** verbatim — its `<question>` text plus whatever the two annotating passes have embedded so far: the `<alternative>` elements (each with its `id`, what-it-is text, `<advantage>`, and `<drawback>`), and any `<applied-principle>`, `<depends-on>`, and `<recommendation>` children. That block is the question context the deliberation runs on and the **QUESTION** you carry into step 3, and what it holds fixes the block's state for step 3: a block with `<alternative>` elements carries a **frozen alternative set**; one with none is **bare**; a `<recommendation option="…">` element, when present, is the sweep's **standing pick**.

If it fails — no block's `id` matches the title — report the mismatch, quoting the tool's `Error:` line, which lists every id the document holds so the user can retry.

### 2. Gather context

Before forming a view, read any project artifacts — deliverables, documents, or design notes — that bear on the question. Prefer reading the real project state over reasoning from memory. Read `<MILESTONE_DIR>/requirements.md` (the goal, relevant starting state, and recorded decisions) and `<MILESTONE_DIR>/open_questions.xml` (the sibling blocks, with whatever the annotating passes have embedded in them) **whole** with the file-reading tool, as you read the bearing artifacts. A whole read is for reasoning only; a locate, list, or lift of a block is the tool's job, as in step 1.

### 3. Present the discussion

Open with a concise framing of what is actually at stake — one or two sentences: no preamble, no summary or restatement of the question, no meta-commentary about what you are about to do.

The analytical core is two shared procedures followed **inline in this conversation**, in this order, their output the spine of the deliberation. Both have a grounding step that overlaps the context you already gathered in step 2 — reuse that reading rather than repeating it.

**The option set** — fixed first, from the block's state:

- **The block carries `<alternative>` elements.** Reuse them as the option set, exactly as embedded: present each option under its `id` with its what-it-is text, advantage, and drawback, and do not enumerate afresh — the set is the frozen alternative set the two annotating passes own, and the recommendation pass never revisits a block once it has picked, so the options a user will be offered later are these. If your grounding surfaces a genuinely realistic option the set lacks, you may put it on the table, but only **marked plainly as a departure** from the frozen set — say that it is not one of the block's embedded alternatives, so recording it would be a literal answer that matches no `<alternative id>` rather than a pick among the frozen options. Never present a departure unmarked, never silently drop a frozen option — one that a decision recorded since has closed is kept in view and noted as closed, with the decision that closed it — and never rewrite a frozen option's text.
- **The block is bare.** Read and follow `.agents/plugins/cairn/shared/alternatives-procedure.md`, passing the located block as its **QUESTION** input, and enumerate the options here — the 2–4 honest alternatives, each with what-it-is / key advantage / key drawback. That enumerated set is the option set for the rest of the deliberation. It is this conversation's and is written nowhere; the alternatives pass supplies the block's frozen set when it next runs.

**The pick** — then read and follow `.agents/plugins/cairn/shared/recommend-procedure.md`, passing the located block as its **QUESTION** and the option set just fixed — the frozen set, plus any marked departure, or the set enumerated here — as its **ALTERNATIVES**, and state **one recommendation of your own**: a single option named by its label, with a direct rationale and, where two are genuinely equivalent, the one thing that breaks the tie. Form this pick afresh from the set and your grounding, never by adopting or arguing back to whatever the block already carries. When the procedure's disclosure duty applies — the pick leans on a still-unanswered sibling settling on one of its alternatives — render it as plain prose in the rationale, naming that sibling's Short Title and the option assumed, never as markup; a confirmed principle that bore on the pick is likewise cited in prose.

**The standing pick** — when the block carries a `<recommendation option="…">` element, show it **beside** your own, labelled as the sweep's standing pick: its option and its rationale, with any `<applied-principle>` and `<depends-on>` children the block carries as the principles it cited and the sibling options it assumed. Then say **plainly whether the two agree, and why**: when they agree, what both rest on and what your independent read confirms; when they disagree, what the standing pick weighed differently, or what has changed since it was made — a decision recorded since, a sibling assumption in a `<depends-on>` that no longer holds, a departure option the frozen set never offered. Never soften your own pick into agreement, and never omit the standing pick or present it as your own; the user came for an independent read against it. When the block carries no `<recommendation>`, there is nothing to show — your pick stands alone.

Then add the layer that is this skill's own — not part of either shared procedure:

**What would change your mind** — name one or two conditions under which a different option would be the right call. This helps the user push back productively.

### 4. Continue the conversation

After the opening, invite the user to push back, ask follow-up questions, or narrow the choice. Respond to each follow-up by updating your reasoning — do not simply repeat the prior framing. Keep individual responses tight: a long initial brief is fine, subsequent replies should be shorter. The conversation ends when:

- The user reaches a decision, **or**
- The user explicitly decides to defer further

### 5. On decision

When the user lands on an answer, offer to invoke `/answer-open-question` with that answer to record it. Do not edit either document yourself — that is `answer-open-question`'s responsibility. When the answer is one of the block's embedded `<alternative>` elements, say which `id` it is, so the recorded decision can be matched to that option; a marked departure is recorded as the literal answer it is.

If the deliberation instead reveals that the milestone **goal itself** needs to change — not just this question, but the objective the question hangs off — surface that explicitly and offer to invoke `/modify-milestone-goal` with the proposed revised goal. Still do not edit anything yourself; the user confirms the wording and that skill performs the write.

The two offers are not exclusive: a discussion can both resolve the question and conclude the goal must shift. When both apply, run `/modify-milestone-goal` **first**, then `/answer-open-question`, so the answer is recorded — and its implications cascaded — against the revised goal rather than a stale one.
