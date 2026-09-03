# Task format (shared)

This is the single source of truth for the **brief-level** format of one task section in a
milestone's `TASKS_TODO.md`. The `derive-tasks` and `submit-task` skills author sections in
this format, and `shared/complete-procedure.md` parses them.

A task states *what* is to be achieved, not how to achieve it: the completer derives the
flow and the acceptance bar itself against the live project, so anything re-derivable there
is wasted here.

## Task template

Use this exact template for every task section:

```markdown
## <Task Title>

<1–3 sentence description of what this task does, why it is needed in this milestone, and
how it would be verified.>

---
```

That is the whole section: the `##` title heading, the 1–3 sentence description, and the
trailing `---` separator. Fold the "how it would be verified" clause into the description as
prose — it is part of those sentences, never a labeled section of its own.

Nothing else belongs in a task section: there is no steps section, no `Provides` section, no
`Notes` section, no `Success` section, and no other structured done-ness heading under any
name.

The trailing `---` separator after every task section is mandatory —
`shared/complete-procedure.md` parses sections by it.

## Authoring guidelines

- **Title**: 4–8 words, title-cased, and unique within the file. If it would collide with an
  existing title, distinguish it. Uniqueness is load-bearing: the completion procedure
  locates a task by case-insensitive partial heading match.
- **Atomic scope**: the task must be completable in a single completion pass, with no
  decisions left to make mid-task. If a brief secretly contains two independently-buildable
  pieces, author the one that matches its primary intent and surface the leftover to the
  caller so it can decide — do not silently split or merge.
- **No open decisions**: decide *which* approach (traceable to `requirements.md`) — never
  "choose the appropriate approach". That is different from spelling out the work: pick the
  strategy, leave the execution.
- **Quote numeric values, durations, thresholds, and configuration values** directly from
  `requirements.md` — do not paraphrase them.
