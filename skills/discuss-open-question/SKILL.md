---
name: discuss-open-question
description: Start a structured conversation about a named open question in the current milestone requirements — surfaces alternatives, trade-offs, and a recommendation to help the user reach a decision.
---

# discuss-open-question

Facilitates a deliberation on a named open question or deferred entry in the current milestone's `requirements.md` where the user cannot give an immediate answer. The goal is a concrete decision by the end of the conversation — not a design document.

## Usage

```
/discuss-open-question <Short Title>
```

The `<Short Title>` must match (case-insensitive) the title of an existing `Open question` or `Deferred` entry in the document.

**Example:**
```
/discuss-open-question Arc drive technique
```

## Workflow

### 0. Find the current milestone

Read `CLAUDE.md` and extract the path from the `## Current Milestone` section (shown in backticks, e.g. `milestones/milestone_11_tbd/`). Use this as `<MILESTONE_DIR>` throughout this workflow.

### 1. Locate the question

Read `<MILESTONE_DIR>/requirements.md`. Find the entry matching the title. If no match is found, report the error and list available titles.

### 2. Gather context

Before forming a view, read any source files, scripts, or design documents that bear on the question. Prefer reading the actual code over reasoning from memory. The goal is to ground the discussion in the real project state.

### 3. Present the discussion

Open with a concise framing of what is actually at stake — one or two sentences, no preamble. Then structure the response as:

**Alternatives** — enumerate the realistic options (typically two to four). For each:
- What it is (one sentence)
- Key advantage
- Key drawback or risk

**Recommendation** — state a single preferred option with a brief rationale. Be direct; avoid hedging. If two options are genuinely equivalent, say so and explain what should break the tie.

**What would change your mind** — name one or two conditions under which a different option would be the right call. This helps the user push back productively.

### 4. Continue the conversation

After the opening, invite the user to push back, ask follow-up questions, or narrow the choice. Respond to each follow-up by updating your reasoning — do not simply repeat the prior framing. The conversation ends when:

- The user reaches a decision, **or**
- The user explicitly decides to defer further

### 5. On decision

When the user lands on an answer, offer to invoke `/answer-open-question` with that answer to record it in the document. Do not edit the document yourself — that is `answer-open-question`'s responsibility.

## Rules

- Do not start with summaries, restating the question at length, or meta-commentary about what you are about to do. Open directly with the substance.
- Do not present more alternatives than are genuinely viable — listing weak options to appear thorough wastes the user's time.
- Make a real recommendation. "It depends" is only acceptable if you also state exactly what it depends on and which condition you think is more likely to hold.
- Do not edit `<MILESTONE_DIR>/requirements.md` — this skill is purely conversational.
- Keep individual responses tight. A long initial brief is fine; subsequent replies in the conversation should be shorter.
