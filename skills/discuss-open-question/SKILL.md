---
name: discuss-open-question
description: Start a structured conversation about a named open question in the current milestone requirements — surfaces alternatives, trade-offs, and a recommendation to help the user reach a decision.
---

# discuss-open-question

Facilitates a deliberation on a named `<open-question>` block (whether `status="open"` or `status="deferred"`) in the current milestone's `requirements.md` where the user cannot give an immediate answer. The goal is a concrete decision by the end of the conversation — not a design document.

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

Locating a block by its handle is a deterministic lookup, so query it with the line-oriented CLI (`awk`/`sed`/`grep`) keyed on the `<open-question …>` / `</open-question>` boundary lines rather than reading the whole file to eyeball a header — never a real XML processor (`xmllint`). Every `<open-question>` block lives under the single `## Open questions` section of `<MILESTONE_DIR>/requirements.md`, so those boundary lines within that one section enumerate the entire question set.

For each `<open-question …>` opening boundary line, pull its `id` attribute with an attribute-name-anchored regex — `id="([^"]*)"` — so the match is independent of attribute order (`status` may precede or follow `id`). The captured value is stored **entity-escaped**, so reverse the five-predefined-entity substitution on it before comparing — replace `&lt;`→`<`, `&gt;`→`>`, `&quot;`→`"`, `&apos;`→`'`, and `&amp;`→`&` **last**. Then case-fold both that un-escaped `id` and the `<Short Title>` argument and compare: the block whose `id` case-folds equal to the title is the match. Open and deferred blocks share the one `<open-question …>` / `</open-question>` boundary-token pair (they differ only in the `status` attribute value), so the locate is uniform with no type-specific branch.

Pull the **whole matched block** — from its `<open-question …>` opening boundary line through the next `</open-question>` closing boundary line — as the question context the deliberation runs on: its `<question>` text plus any `<alternative>` / `<applied-principle>` / `<recommendation>` sub-elements the recommend sweep may already have embedded. That whole block is the **QUESTION** you carry into step 3.

If no block's `id` case-folds equal to the title, report the mismatch and list the available titles — deterministically enumerable by pulling `id="([^"]*)"` from every `<open-question …>` boundary line in the `## Open questions` section — so the user can retry.

### 2. Gather context

Before forming a view, read any project artifacts — deliverables, documents, or design notes — that bear on the question. Prefer reading the real project state over reasoning from memory. The goal is to ground the discussion in what the project actually contains. This grounding is reason-across work, so read `requirements.md` and the bearing artifacts **whole** rather than querying via the CLI — the CLI is reserved for the deterministic locate in step 1, while forming a genuine view means taking in the surrounding documents and deliverables.

### 3. Present the discussion

Open with a concise framing of what is actually at stake — one or two sentences, no preamble.

For the analytical core — the realistic alternatives and the single recommendation — read and follow the shared procedure at `${CLAUDE_PLUGIN_ROOT}/shared/recommend-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), producing its output **inline in this conversation** as the spine of the deliberation. It is the single source of truth for enumerating the alternatives (each with what-it-is / key advantage / key drawback) and stating one direct recommendation with a tie-break; do not restate those specifics here. Its grounding step overlaps the context you already gathered in step 2 — reuse that reading rather than repeating it. Pass the located question as its **QUESTION** input.

Then add the layer that is this skill's own — not part of the shared core:

**What would change your mind** — name one or two conditions under which a different option would be the right call. This helps the user push back productively.

### 4. Continue the conversation

After the opening, invite the user to push back, ask follow-up questions, or narrow the choice. Respond to each follow-up by updating your reasoning — do not simply repeat the prior framing. The conversation ends when:

- The user reaches a decision, **or**
- The user explicitly decides to defer further

### 5. On decision

When the user lands on an answer, offer to invoke `/answer-open-question` with that answer to record it in the document. Do not edit the document yourself — that is `answer-open-question`'s responsibility.

If the deliberation instead reveals that the milestone **goal itself** needs to change — not just this question, but the objective the question hangs off — surface that explicitly and offer to invoke `/modify-milestone-goal` with the proposed revised goal. Still do not edit anything yourself; the user confirms the wording and that skill performs the write.

The two offers are not exclusive: a discussion can both resolve the question and conclude the goal must shift. When both apply, run `/modify-milestone-goal` **first**, then `/answer-open-question` — the goal is the root the answer hangs off, so recording the answer against the already-revised goal lets `answer-open-question` analyse implications and cascade against the new objective rather than a stale one.

## Rules

- Do not start with summaries, restating the question at length, or meta-commentary about what you are about to do. Open directly with the substance.
- Do not present more alternatives than are genuinely viable — listing weak options to appear thorough wastes the user's time.
- Make a real recommendation. "It depends" is only acceptable if you also state exactly what it depends on and which condition you think is more likely to hold.
- Do not edit `<MILESTONE_DIR>/requirements.md` — this skill is purely conversational.
- Keep individual responses tight. A long initial brief is fine; subsequent replies in the conversation should be shorter.
