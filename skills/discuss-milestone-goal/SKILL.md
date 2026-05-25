---
name: discuss-milestone-goal
description: Analyze an overall goal description and ask clarifying questions to make the milestone goal crisp, complete, and ready for formal definition.
---

# discuss-milestone-goal

Facilitates a structured conversation to sharpen a vague or incomplete milestone goal into a clear, actionable statement ready for `/define-milestone-goal`. The output is a refined goal description — not a document yet.

## Usage

```
/discuss-milestone-goal <overall_goal_description>
```

- `<overall_goal_description>`: a free-form description of what you want the milestone to accomplish.

**Example:**
```
/discuss-milestone-goal add a shooting mechanic where the player can fire at enemies
```

## Workflow

### 1. Read project context

Read `CLAUDE.md` to understand the current milestone, tech stack, and project overview. Read `milestones/README.md` to understand what has already been built in past milestones. This grounds all questions in the real project state.

### 2. Analyze the goal

Identify what is clear, what is ambiguous, and what is missing. Look for:

- **Scope ambiguity** — what exactly is in vs. out?
- **Dependency gaps** — does this assume systems that don't exist yet?
- **Success criteria** — how would you know the milestone is done?
- **Conflicts** — does anything in the goal conflict with the current architecture or existing milestones?

### 3. Open with a crisp framing

Restate the goal in one sentence to show you understood it. Then immediately surface the most important ambiguities as direct questions. Do not pad with preamble or list every possible concern — focus on the two or three questions whose answers would most change the scope.

Format as:

**Understood goal:** one sentence.

**Questions:**
1. ...
2. ...
3. (optional) ...

### 4. Continue the conversation

After each user answer, either:
- Ask the next most important clarifying question, or
- Confirm that the goal is now clear enough to define

Do not ask questions for their own sake. Stop when the goal is specific enough that `/define-milestone-goal` could fill `requirements.md` without further guessing.

### 5. Propose the refined goal

When the conversation reaches a natural close, present a refined goal statement:

**Proposed milestone goal:**
> <one to three sentences that could go directly into the `## Goal` section of requirements.md>

Invite the user to adjust the wording. Once they confirm, suggest invoking `/define-milestone-goal "<refined goal>"` to create the milestone.

## Rules

- Do not create any files. This skill is purely conversational.
- Do not assign a milestone number — that is the user's decision.
- Ask questions one at a time when the user seems overwhelmed; batch them when context is thin and answers are likely short.
- Make a real judgment about what matters: do not list every possible edge case as a question.
- Keep each response short after the opening; the conversation should move fast.
