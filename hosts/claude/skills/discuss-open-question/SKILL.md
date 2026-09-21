---
name: discuss-open-question
description: Discuss a named open question in the current milestone requirements, surfacing alternatives, trade-offs, and a recommendation to help the user decide.
---

# discuss-open-question

Facilitates a deliberation on a named `<open-question>` block in the current milestone's `open_questions.xml` where the user cannot give an immediate answer. The goal is a concrete decision by the end of the conversation — not a design document. The skill is purely conversational: it never edits `open_questions.xml`, `requirements.md`, or any other file.

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

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Locate the question

Locating a block by its handle is a deterministic lookup, so it is a call to the plugin's open-question tool — the sole writer of `<MILESTONE_DIR>/open_questions.xml`, and the only way this skill ever locates, lists, or lifts a block:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/open_questions.py locate <MILESTONE_DIR> "<Short Title>"
```

On success it prints the **whole matched block** verbatim — its `<question>` text plus any `<alternative>` / `<applied-principle>` / `<depends-on>` / `<recommendation>` sub-elements the recommend sweep may already have embedded. That block is the question context the deliberation runs on and the **QUESTION** you carry into step 3.

If it fails — no block's `id` matches the title — report the mismatch, quoting the tool's `Error:` line, which lists every id the document holds so the user can retry.

### 2. Gather context

Before forming a view, read any project artifacts — deliverables, documents, or design notes — that bear on the question. Prefer reading the real project state over reasoning from memory. Read `<MILESTONE_DIR>/requirements.md` (the goal, relevant starting state, and recorded decisions) and `<MILESTONE_DIR>/open_questions.xml` (the sibling blocks, with whatever the recommend sweep has embedded in them) **whole** with the file-reading tool, as you read the bearing artifacts. A whole read is for reasoning only; a locate, list, or lift of a block is the tool's job, as in step 1.

### 3. Present the discussion

Open with a concise framing of what is actually at stake — one or two sentences: no preamble, no summary or restatement of the question, no meta-commentary about what you are about to do.

For the analytical core — the realistic alternatives and the single recommendation — read and follow the shared procedure at `${CLAUDE_PLUGIN_ROOT}/shared/recommend-procedure.md`, producing its output **inline in this conversation** as the spine of the deliberation. It owns enumerating the alternatives (each with what-it-is / key advantage / key drawback) and stating one direct recommendation with a tie-break; pass the located block as its **QUESTION** input. Its grounding step overlaps the context you already gathered in step 2 — reuse that reading rather than repeating it. When the core's disclosure duty applies — the recommendation leans on a still-unanswered sibling's recommendation — render it as plain prose in the rationale, naming that sibling's Short Title and the option assumed, never as markup.

Then add the layer that is this skill's own — not part of the shared core:

**What would change your mind** — name one or two conditions under which a different option would be the right call. This helps the user push back productively.

### 4. Continue the conversation

After the opening, invite the user to push back, ask follow-up questions, or narrow the choice. Respond to each follow-up by updating your reasoning — do not simply repeat the prior framing. Keep individual responses tight: a long initial brief is fine, subsequent replies should be shorter. The conversation ends when:

- The user reaches a decision, **or**
- The user explicitly decides to defer further

### 5. On decision

When the user lands on an answer, offer to invoke `/answer-open-question` with that answer to record it. Do not edit either document yourself — that is `answer-open-question`'s responsibility.

If the deliberation instead reveals that the milestone **goal itself** needs to change — not just this question, but the objective the question hangs off — surface that explicitly and offer to invoke `/modify-milestone-goal` with the proposed revised goal. Still do not edit anything yourself; the user confirms the wording and that skill performs the write.

The two offers are not exclusive: a discussion can both resolve the question and conclude the goal must shift. When both apply, run `/modify-milestone-goal` **first**, then `/answer-open-question`, so the answer is recorded — and its implications cascaded — against the revised goal rather than a stale one.
