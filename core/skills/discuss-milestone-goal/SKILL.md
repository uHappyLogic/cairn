---
name: discuss-milestone-goal
description: Analyze an overall goal description and ask clarifying questions to make the milestone goal crisp, complete, and ready for formal definition.
---

# discuss-milestone-goal

Facilitates a structured conversation to sharpen a vague or incomplete milestone goal into a clear, actionable statement ready for `/define-milestone-goal`. The output is a refined goal description and the one directory the milestone is placed at — not a document yet: this skill is purely conversational and creates no files, and both proposals are the user's to confirm.

## Usage

```
/discuss-milestone-goal <overall_goal_description>
```

- `<overall_goal_description>`: a free-form description of what you want the milestone to accomplish.

**Example:**
```
/discuss-milestone-goal add a getting-started guide that walks a new user through their first session
```

## Workflow

### 1. Read project context

Read `{{CONTEXT_FILE}}` to understand the current milestone, the project's domain context, and project overview. Read `milestones/README.md` to understand what has already been built in past milestones. This grounds all questions in the real project state.

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

Ask questions one at a time when the user seems overwhelmed; batch them when context is thin and answers are likely short. Keep each response short after the opening — the conversation should move fast. Do not ask questions for their own sake. Stop when the goal is specific enough that `/define-milestone-goal` could fill `requirements.md` without further guessing.

### 5. Propose the refined goal

When the conversation reaches a natural close, present a refined goal statement:

**Proposed milestone goal:**
> <one to three sentences that could go directly into the `## Goal` section of requirements.md>

Invite the user to adjust the wording, then go on to the placement.

### 6. Propose the placement

From the refined goal, name the one directory that holds the core of the work — the code, module, or package the milestone is about — reading the project's actual layout to find it. Go as deep in the tree as the core allows, and propose the root, `.`, only when the core is the project itself. Work the milestone also needs outside that directory (documentation kept elsewhere, a shared configuration file, a test tree beside the package) is adjacent and does not widen the proposal: never move up to cover it, or to the root for safety, since a milestone placed higher overlaps every milestone placed beneath it and so runs one at a time with all of them. The directory must already exist in the working tree, because the definition refuses one that does not; when the core does not exist yet, propose its nearest existing ancestor, or say that the user can create the directory first. That one directory is the whole proposal, and the refined goal does not restate it.

**Proposed placement:** `<scope>`, the directory's path relative to the workspace root.

Invite the user to adjust it. Once both the goal and the placement are confirmed, suggest invoking `/define-milestone-goal --at <scope> <refined goal>` to create the milestone; the definition takes the placement as given.
