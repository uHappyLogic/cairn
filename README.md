<p align="center">
    <img src=".github/assets/readme/cairn-banner.webp" style="height: 10em" alt="Cairn banner"/>
</p>
<p align="center">
  <a href="https://github.com/uHappyLogic/cairn/releases/latest">
    <img alt="Latest Release" src="https://img.shields.io/github/v/release/uHappyLogic/cairn?style=flat&color=22c55e&label=release&display_name=tag" />
  </a>
  <a href="LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-3b82f6?style=flat" />
  </a>
</p>

---

# Cairn

**Mark the path from idea to shipped.**
Milestone-driven development for any stack.

## Why Cairn?

Large-scale software projects fail in predictable ways: the goal drifts during planning, ambiguities pile up before coding starts, the task list grows unbounded, and there's no clear line between "working on it" and "done."

Cairn gives Claude Code a structured, repeatable process for moving an idea from rough goal to shipped code — one milestone at a time. Each milestone is a self-contained unit: you clarify the goal, resolve every open question, derive an ordered task list, complete the tasks, and close out the milestone before moving on. Nothing falls through the cracks because every decision is recorded and every requirement maps to a task.

It works with any tech stack. Skills read your project's environment (tooling, conventions, build commands) from `CLAUDE.md`, so the workflow adapts to whatever you're building.

## Installation

In any Claude Code project, run:

```
/plugin marketplace add uHappyLogic/cairn
```

Then bootstrap the milestones scaffold once in your project root:

```
/init-milestone-base-workflow
```

Run `/init` to document your project's tech stack and tooling in `CLAUDE.md` so skills can read the environment context.

## How it works

Each milestone lives in `milestones/milestone_<N>_<slug>/` and contains three files:

- `requirements.md` — goal, relevant starting state, decisions, and open questions
- `TASKS_TODO.md` — pending tasks ordered by priority (highest first)
- `TASKS_DONE.md` — completed tasks appended in the same format

`milestones/README.md` is the source of truth for which milestone is active. Skills read and write the current-milestone pointer there; it is never ambiguous which milestone is open.

## Workflow pipeline

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'ui-sans-serif, system-ui','lineColor':'#94a3b8','primaryBorderColor':'#475569'},'flowchart':{'wrappingWidth':9999,'curve':'basis'}}}%%
flowchart TD
subgraph S0["⚙️ One-time setup"]
    OT1(["<b>/init</b><br/>one-time project setup: document tech stack/tooling in CLAUDE.md"])
    OT2(["<b>/init-milestone-base-workflow</b><br/>one-time bootstrap: create milestones/ + README, seed pointer"])
end

D0[/"Workflow scaffold ready<br/>milestones/ + CLAUDE.md documented"/]

subgraph S1["🎯 Initializing a milestone"]
    IM1["<b>/discuss-milestone-goal</b><br/>(optional) sharpen a vague idea before defining"]
    IM2["<b>/define-milestone-goal</b><br/>create the milestone directory and seed requirements.md"]
    IM3["<b>/goto-next-milestone</b><br/>advance the current-milestone pointer"]
end

D1[/"Milestone goal defined<br/>requirements.md seeded, pointer active"/]

subgraph S2["❓ Iterating milestone requirements document"]
    ITM0["<b>/specify-milestone-starting-state</b><br/>fill 'Relevant starting state' from the codebase"]
    ITM1["<b>/review-milestone-requirements</b><br/>repeat each pass: reconcile, surface new gaps, check convergence"]
    ITM3["<b>/discuss-open-question</b><br/>(optional) explore one question"]
    ITM4{{"<b>/answer-open-question</b><br/>record the decision"}}
    ITM5["<b>/try-capture-answer-principle</b><br/>(auto after answering) record the reusable principle behind the decision to the project-wide store"]
    ITM2["<b>/try-answer-all-questions-by-principle</b><br/>(optional) autonomously answer questions a confirmed principle settles, by candidate elimination; needs a clean tree; one auto-answer per commit naming the principle in an Answer-Principle trailer"]
    ITM6["<b>/reject-auto-answer</b><br/>(optional) revert a bad auto-answer's commit, reopening its question"]
end

D2[/"Requirements finalized<br/>all open questions resolved"/]

subgraph S3["🤖 Automated one-shot task derivation and completion"]
    AI1["<b>/derive-tasks</b><br/>convert requirements.md → ordered TASKS_TODO.md"]
    AI2["<b>/complete-all-tasks</b><br/>complete all tasks, committing after each one"]
end

D3[/"Ordered task list completed and committed"/]

subgraph S4["🔧 Semi-manual follow-up and adjustments"]
    SM0["<b>/ask-in-milestone-context</b><br/>(optional, anytime) ask an informational question about the milestone's goal, decisions, done/pending tasks, and the code they produced — read-only, hands off when a next step surfaces"]
    SM1["<b>/discuss-new-task</b><br/>(optional) clarify a new issue discovered mid-flight into one or more briefs, then hand off to /submit-task"]
    SM2["<b>/submit-task</b><br/>add a single new task inline in the conversation, with context available for follow-up tweaks"]
    SM3{{"<b>/complete-task</b><br/> complete a single task inline with the conversation for context, without committing; use when you want to ask follow-ups or tweak the work right after seeing it"}}
end

D4[/"Follow-up adjustments completed"/]

subgraph S5["🏁 Ending a milestone and moving to the next"]
    EM1["<b>/finish-current-milestone</b><br/>record accomplishments; finalize the milestone"]
end

D5[/"Milestone closed<br/>pointer cleared"/]

    OT1 --> OT2 --> D0
    D0 --> IM1 --> IM2 --> IM3
    IM3 --> D1
    D1 --> ITM0 --> ITM1
    ITM1 --> ITM3 --> ITM4
    ITM4 --> ITM5
    ITM4 -.->|repeat until satisfied| ITM1
    ITM4 --> D2
    ITM1 --> ITM2
    ITM2 -.->|on a wrong auto-answer| ITM6
    ITM6 -.->|re-capture the principle| ITM5
    ITM2 --> D2
    D2 --> AI1 --> AI2 --> D3
    D3 --> SM1
    D3 -.->|ask about state/finished work| SM0
    SM1 --> SM2 --> SM3
    SM3 -.->|repeat until satisfied| SM1
    SM3 --> D4
    D4 --> EM1 --> D5
    D5 -.->|next milestone| IM1

    classDef setup  fill:#f1f5f9,stroke:#475569,color:#0f172a;
    classDef init   fill:#eff6ff,stroke:#2563eb,color:#1e3a8a;
    classDef req    fill:#faf5ff,stroke:#9333ea,color:#581c87;
    classDef auto   fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef manual fill:#fff7ed,stroke:#ea580c,color:#7c2d12;
    classDef finish fill:#fef2f2,stroke:#e11d48,color:#881337;
    classDef optional stroke-dasharray:5 4;
    classDef state  fill:#fffbeb,stroke:#d97706,color:#78350f,font-style:italic;

    class OT1,OT2 setup;
    class IM1,IM2,IM3 init;
    class ITM0,ITM1,ITM2,ITM3,ITM4,ITM5,ITM6 req;
    class AI1,AI2 auto;
    class SM0,SM1,SM2,SM3 manual;
    class EM1 finish;
    class IM1,ITM2,ITM3,SM0,SM1,SM3,ITM6 optional;
    class D0,D1,D2,D3,D4,D5 state;

    linkStyle 11,15,24,28 stroke:#9333ea,stroke-width:1.5px;
```

## Skill reference

### `init-milestone-base-workflow`

One-time bootstrap for a project. Creates the `milestones/` directory and `milestones/README.md` with the current-milestone pointer, and ensures `CLAUDE.md` carries the `## Milestone Workflow` guidance. Additive and idempotent — creates missing scaffolding and inserts missing sections into existing files, never overwrites existing content. Run this before any other workflow skill.

### `discuss-milestone-goal <overall_goal_description>`

Facilitates a structured conversation to sharpen a vague goal into a clear, actionable statement. Produces a refined goal description ready for `/define-milestone-goal`. Creates no files.

### `define-milestone-goal <overall_goal_description>`

Creates a new `milestones/milestone_<N>_<slug>/` directory with `requirements.md` (Goal section filled), plus empty `TASKS_TODO.md` and `TASKS_DONE.md`. Does **not** activate the milestone.

### `specify-milestone-starting-state <milestone_id>`

Reads the milestone goal, explores the project using the environment documented in `CLAUDE.md`, and writes a concise technical summary into the `## Relevant starting state` section of `requirements.md`. Sets up the context needed to make informed decisions.

### `review-milestone-requirements`

The repeatable engine of the requirements-iteration loop. Each pass over the current milestone's `requirements.md` does three jobs: **reconciles** the existing question set against what's already decided (prunes a block a recorded decision now covers, dedups repeats), **surfaces** genuinely new gaps the latest decisions exposed, and **reports convergence** — whether any `Open question` blocks remain (which `/derive-tasks` forbids) or the requirements are ready to derive tasks. Run it after `/specify-milestone-starting-state` to open the questions, then re-run after every answer or two — earlier answers keep opening new ones. It never answers questions or records decisions itself; it shapes and reports the open-questions state for the answering skills to resolve.

### The answer-principle-learning loop

Open questions get resolved two ways, and the project *learns* from every manual answer. Confirmed answering principles accumulate in `milestones/answer_decision_principles.md` — a single project-wide store at the `milestones/` **root**, above any one milestone, so principles carry across milestones. Each principle is a reusable keep/eliminate directive that future autonomous answers can apply.

- **Manual teaching flow** — `/discuss-open-question → /answer-open-question → (auto) /try-capture-answer-principle`. You deliberate a question, record the answer, and `answer-open-question` automatically offers to generalize the rule behind it into a confirmed principle.
- **Autonomous sweep** — `/try-answer-all-questions-by-principle` re-sweeps the requirements and auto-answers exactly the questions those confirmed principles already settle, one traceable commit per answer.
- **Correction loop** — `/reject-auto-answer → re-capture`. If the sweep gets one wrong, reject reverts that commit (reopening the question) and points you back to `/try-capture-answer-principle` to revise the offending principle so the next sweep does better.

### `discuss-open-question <question_name>`

Opens a structured conversation about a named open question in `requirements.md`. Surfaces alternatives, trade-offs, and a recommendation to help reach a decision.

### `answer-open-question <question_name>`

Records the resolution of a named open question in `requirements.md`, updating the document to reflect the decision and its downstream implications. After recording, it automatically chains into `/try-capture-answer-principle` to offer to generalize the decision into a reusable answering principle.

### `try-capture-answer-principle [focus_hint]`

Extracts a reusable answering principle from a decision just made and records it in the project-wide principle store `milestones/answer_decision_principles.md`. Runs automatically after `/answer-open-question`, and is also directly invocable with an optional free-text focus hint. It analyzes the conversation's deliberation, exits quietly when nothing generalizes, and only ever proposes a revise-or-add for you to confirm — never editing the store silently. It is the **sole writer** of the principle store.

### `try-answer-all-questions-by-principle`

The autonomous sweep. Re-reads every open and deferred question in the current milestone's `requirements.md` and answers exactly those a confirmed principle already settles, by **candidate elimination** — enumerate the realistic answers, keep only those a confirmed principle supports, and auto-answer only when a single survivor remains. Requires a clean working tree, and commits **one auto-answer per commit**: subject `Principle-based-answer: <question>`, with each applied principle named in an `Answer-Principle:` trailer line. It is a pure orchestrator — it dispatches the read-only `try-answer-question-by-principle` subagent per question and owns all recording and committing. On a fresh project with no principles taught yet, it resolves nothing.

### `try-answer-question-by-principle` (subagent)

Read-only candidate-elimination subagent dispatched once per question by `/try-answer-all-questions-by-principle` — not user-invocable. Reads the principle store, enumerates the realistic candidate answers, keeps only those a confirmed principle supports, and returns a verdict naming the unique survivor (if any) and the load-bearing principles. It mutates nothing; the orchestrator owns all document edits and commits.

### `reject-auto-answer [commit-id | text_fragment]`

Reverts one bad auto-answer from the sweep. Takes an optional argument — a commit id from the sweep's report, a fragment of the wrong folded decision text in `requirements.md`, or nothing (defaults to `HEAD`). It validates the target is a genuine auto-answer commit (touches only `requirements.md`, carries an `Answer-Principle:` trailer), shows it for confirmation, then `git revert --no-commit`s it — which **reopens** the answered question — leaving the revert staged. It never edits the principle store; it points you to re-capture the principle behind the bad answer so the next sweep does not reproduce it.

### `derive-tasks`

Converts the current milestone's `requirements.md` into `TASKS_TODO.md` — a complete, dependency-ordered list of atomic, AI-executable tasks. Decomposes the milestone into high-level briefs, proves every requirement is covered, then delegates detailed task authoring to the `submit-task` agent. Requires all open questions to be resolved first.

### `discuss-new-task <issue description>`

Clarifies a rough or oversized issue discovered mid-flight into one or more clear, task-sized briefs through a short conversation, then hands each off to `/submit-task`. Use it when the affected system, desired behavior, or verification isn't yet clear, or when one issue is really several tasks.

### `submit-task <issue description>`

Adds a single, already-clear issue to `TASKS_TODO.md`. Triages for duplicates and decides where the task belongs, then authors and inserts the task **inline, in the current conversation** so the authoring context stays available for follow-up tweaks. For vague or multi-task issues, route through `/discuss-new-task` first.

### `complete-all-tasks`

Orchestrator: completes all tasks in `TASKS_TODO.md` top to bottom, spawning one subagent per task and committing after each success. Stops on first failure.

### `complete-task <task_name>`

Completes a single named task from `TASKS_TODO.md` **inline, in the current conversation**. Running inline keeps the work context (what changed, why, how it was verified) in the conversation so you can ask follow-up questions or request tweaks right after. Changes are left staged — use `/complete-all-tasks` to complete the whole task list unattended with automatic commits.

### `ask-in-milestone-context <question>`

Answers a free-form, informational question about the current milestone — its goal, recorded decisions, done and pending tasks, and the actual code those tasks produced — grounding the answer in the live files and source rather than memory. **Read-only and conversational**, usable any time: use it to look back on finished work ("how did task X end up handling Y?", "where did we put Z?"), to take stock ("what's left and why?"), or to surface context before deciding what to do next. When the answer reveals a concrete next step, it offers the right skill — `/discuss-open-question`, `/submit-task` or `/discuss-new-task`, `/discuss-milestone-goal`, `/complete-task` — but performs none of their work itself.

### `finish-current-milestone`

Verifies all tasks are done, writes a completion summary to `milestones/README.md`, and updates `CLAUDE.md` only for lasting tech-stack or structural changes. Clears the current-milestone pointer — run `/goto-next-milestone` after.

### `goto-next-milestone <number> <title>`

Creates the next milestone directory with empty starter files and updates the current-milestone pointer in `milestones/README.md`. Only runnable after `/finish-current-milestone` has cleared the active pointer.

## Self-dogfooding

This repository runs its own workflow on itself. The `milestones/` directory, `milestones/README.md`, and the active milestone directory (`milestones/milestone_01_public-release-prep/`) are live workflow artifacts produced by Cairn's own skills — the requirements, task list, and completed tasks for the current milestone are all right there in the repo. If you want to see what a real milestone looks like end-to-end, look no further.

## License

MIT — see [LICENSE](LICENSE).
