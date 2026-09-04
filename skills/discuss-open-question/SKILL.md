---
name: discuss-open-question
description: Discuss a named open question in the current milestone requirements, surfacing alternatives, trade-offs, and a recommendation to help the user decide.
---

# discuss-open-question

Facilitates a deliberation on a named `<open-question>` block (whether `status="open"` or `status="deferred"`) in the current milestone's `requirements.md` where the user cannot give an immediate answer. The goal is a concrete decision by the end of the conversation — not a design document. The skill is purely conversational: it never edits `requirements.md` or any other file.

## Usage

```
/discuss-open-question <Short Title>
```

The `<Short Title>` must match (case-insensitive) the `id` of an existing `<open-question>` block (either `status="open"` or `status="deferred"`) in the document.

**Example:**
```
/discuss-open-question Getting-started section order
```

## Workflow

### 0. Find the current milestone

Follow `${CLAUDE_PLUGIN_ROOT}/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded task-list path.

### 1. Locate the question

Locating a block by its handle is a deterministic lookup, so query it with the line-oriented CLI (`awk`/`sed`/`grep`) keyed on the `<open-question …>` / `</open-question>` boundary lines — never a real XML processor (`xmllint`). Every `<open-question>` block lives under the single `## Open questions` section of `<MILESTONE_DIR>/requirements.md`, so those boundary lines within that one section enumerate the entire question set.

For each `<open-question …>` opening boundary line, pull its `id` attribute with an attribute-name-anchored regex — `id="([^"]*)"` — so the match is independent of attribute order (`status` may precede or follow `id`). The captured value is stored **entity-escaped**, so reverse the five-predefined-entity substitution on it before comparing — replace `&lt;`→`<`, `&gt;`→`>`, `&quot;`→`"`, `&apos;`→`'`, and `&amp;`→`&` **last**. Then case-fold both that un-escaped `id` and the `<Short Title>` argument and compare: the block whose `id` case-folds equal to the title is the match.

Pull the **whole matched block** — from its `<open-question …>` opening boundary line through the next `</open-question>` closing boundary line — as the question context the deliberation runs on: its `<question>` text plus any `<alternative>` / `<applied-principle>` / `<recommendation>` sub-elements the recommend sweep may already have embedded. That whole block is the **QUESTION** you carry into step 3.

If no block's `id` case-folds equal to the title, report the mismatch and list the available titles — deterministically enumerable by pulling `id="([^"]*)"` from every `<open-question …>` boundary line in the `## Open questions` section — so the user can retry.

### 2. Gather context

Before forming a view, read any project artifacts — deliverables, documents, or design notes — that bear on the question. Prefer reading the real project state over reasoning from memory. Read `requirements.md` and the bearing artifacts **whole** rather than querying via the CLI, which is reserved for the deterministic locate in step 1.

### 3. Present the discussion

Open with a concise framing of what is actually at stake — one or two sentences: no preamble, no summary or restatement of the question, no meta-commentary about what you are about to do.

For the analytical core — the realistic alternatives and the single recommendation — read and follow the shared procedure at `${CLAUDE_PLUGIN_ROOT}/shared/recommend-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), producing its output **inline in this conversation** as the spine of the deliberation. It owns enumerating the alternatives (each with what-it-is / key advantage / key drawback) and stating one direct recommendation with a tie-break; pass the located block as its **QUESTION** input. Its grounding step overlaps the context you already gathered in step 2 — reuse that reading rather than repeating it.

Then add the layer that is this skill's own — not part of the shared core:

**What would change your mind** — name one or two conditions under which a different option would be the right call. This helps the user push back productively.

### 4. Continue the conversation

After the opening, invite the user to push back, ask follow-up questions, or narrow the choice. Respond to each follow-up by updating your reasoning — do not simply repeat the prior framing. Keep individual responses tight: a long initial brief is fine, subsequent replies should be shorter. The conversation ends when:

- The user reaches a decision, **or**
- The user explicitly decides to defer further

### 5. On decision

When the user lands on an answer, offer to invoke `/answer-open-question` with that answer to record it in the document. Do not edit the document yourself — that is `answer-open-question`'s responsibility.

If the deliberation instead reveals that the milestone **goal itself** needs to change — not just this question, but the objective the question hangs off — surface that explicitly and offer to invoke `/modify-milestone-goal` with the proposed revised goal. Still do not edit anything yourself; the user confirms the wording and that skill performs the write.

The two offers are not exclusive: a discussion can both resolve the question and conclude the goal must shift. When both apply, run `/modify-milestone-goal` **first**, then `/answer-open-question`, so the answer is recorded — and its implications cascaded — against the revised goal rather than a stale one.
