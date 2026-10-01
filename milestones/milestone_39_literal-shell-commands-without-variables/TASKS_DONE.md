# TASKS DONE

## State Literal-Path Rule in Commit Procedure

Add the shell-neutral literal-path rule to `core/shared/commit-procedure.md` as prose next to each of its two example commands, which stay exactly as written (`git status --porcelain -- <PATHS>` in step 1, `git add <PATHS>` in step 2): every path is written out on the command line as its own argument and none is held in a shell variable, and step 1 also gains the "naming each path explicitly" wording step 2 already has. This is the first of the two provoking sites where a shell that does not split an unquoted variable makes a run fail. Verified by reading both steps against the "Commit procedure examples" decision, rebuilding `hosts/` with `uv run scripts/build_hosts.py`, and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- Step 1 of `core/shared/commit-procedure.md` still shows the example command exactly as `git status --porcelain -- <PATHS>`.
- Step 2 still shows the example command exactly as `git add <PATHS>`.
- Step 1's prose next to its command now says "naming each path explicitly: every path is written out on the command line as its own argument, and none is held in a shell variable".
- Step 2's prose next to its command carries the same sentence in matching wording ("naming each path explicitly: every path is written out on the command line as its own argument, and none is held in a shell variable").
- The added prose names no host and no particular shell, keeps the PATHS name, and adds no numbered-placeholder or concrete-instance example.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/shared/commit-procedure.md` and `hosts/antigravity/shared/commit-procedure.md`, and `uv run scripts/build_hosts.py --check` passed.

---

## Restate Literal-Path Rule in Complete-Task Agent Staging

Extend the existing `git add` sentence ("naming each path explicitly") in the "Staging contract" section of `core/agents/complete-task.md` with the same shell-neutral wording the commit procedure now carries — each path appears literally on the command line, never through a shell variable — because the dispatched agent reads no other file and stages the largest path set in the workflow. Verified by comparing the two sentences for matching wording, rebuilding `hosts/`, and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- The `git add` sentence in the "Staging contract" section of `core/agents/complete-task.md` now reads "naming each path explicitly: every path is written out on the command line as its own argument, and none is held in a shell variable", stated in that section directly.
- That wording matches the step-2 sentence of `core/shared/commit-procedure.md` ("naming each path explicitly: every path is written out on the command line as its own argument, and none is held in a shell variable") word for word.
- The rest of the staging contract (the `git add -A` ban, tree-wide selection ban, success-path-only staging) is unchanged, and the added prose names no host and no particular shell.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/agents/complete-task.md` and `hosts/antigravity/agents/complete-task.md`, and `uv run scripts/build_hosts.py --check` passed.

---

## Add Full-Command Clause to Five Tool Sites

Add one clause to the tool-contract sentence in the opening paragraph of each of the five multi-call sites (`review-milestone-requirements`, `provide-alternatives-to-all-open-questions`, `recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, and `core/shared/answer-procedure.md`), along the lines of "write the full command shown on every call; never define a variable, alias, or function of your own to stand for it or any part of it", sitting next to the command where the sentence already spells it out and referring to the full command as shown in each fenced block where it does not. The answer sweep's clause is worded to cover every tool call the run makes, including the per-question calls of the procedures it follows (the lift procedure's `lift`, and `answer-procedure.md`'s `locate`, `remove`, and cascade `remove`), while `core/shared/answer-with-recommendation-procedure.md`, every fenced call, and the commands themselves stay untouched and the prose names no host, no shell, and not the plugin-root segment. Verified by finding exactly one such clause in each of the five files, the tool contract still one sentence per site, `hosts/` rebuilt, and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- Each of the five files (`core/skills/review-milestone-requirements/SKILL.md`, `core/skills/provide-alternatives-to-all-open-questions/SKILL.md`, `core/skills/recommend-all-open-questions/SKILL.md`, `core/skills/answer-all-open-questions-with-recommendation/SKILL.md`, `core/shared/answer-procedure.md`) carries exactly one full-command clause ("written out in full … never through a variable, alias, or function of your own defined to stand for the command or any part of it"), found once per file by grep.
- Each clause is added to the existing tool-contract sentence in the file's opening paragraph, which stays one sentence; no new sentence and no copy elsewhere in the file.
- In `review-milestone-requirements` and `answer-procedure.md` the clause sits directly after the spelled-out command; in the two annotating passes and the answer sweep it refers to the call "as its fenced block shows it".
- The answer sweep's clause covers every tool call the run makes, naming this skill's own calls and the per-question calls of the procedures it follows: the lift procedure's `lift` and the answer procedure's `locate`, `remove`, and cascade `remove`.
- `core/shared/answer-with-recommendation-procedure.md` is unchanged, no fenced call and no command line is changed (the diff touches only opening-paragraph prose), and the added prose names no host, no shell, and not the plugin-root segment.
- `uv run scripts/build_hosts.py` rebuilt the five files in both `hosts/claude/` and `hosts/antigravity/`, and `uv run scripts/build_hosts.py --check` passed.

---

## Add Full-Command Clause to Alternatives Agent

Attach the same full-command clause, in the wording the five tool sites now carry, to the step-1 tool-contract sentence of `core/agents/provide-alternatives-to-open-question.md` ("You reach `open_questions.xml` through exactly two calls …"), stated once with neither fenced call annotated and the commands untouched, because the dispatched agent reads only its own file and its two calls share the command prefix a runner would shorten into a variable. Verified by comparing the clause against the five sites for matching wording, rebuilding `hosts/`, and `uv run scripts/build_hosts.py --check` passing.

**Verified:**

- The step-1 tool-contract sentence of `core/agents/provide-alternatives-to-open-question.md` ("You reach `open_questions.xml` through **exactly two** calls …") now carries, directly after the spelled-out command, the clause "written out in full on every call, never through a variable, alias, or function of your own defined to stand for the command or any part of it".
- That clause matches the wording of the five tool sites word for word (checked against `review-milestone-requirements` and `core/shared/answer-procedure.md`, which also place it directly after the spelled-out command), and it appears exactly once in the file, found by grep.
- The sentence stays one sentence ending in "and never open or search the file yourself:", neither fenced call (`locate`, `list --with-question`) gets anything beside it, and no command line is changed (the diff touches only that sentence).
- The added prose names no host, no shell, and not the plugin-root segment.
- `uv run scripts/build_hosts.py` rebuilt `hosts/claude/agents/provide-alternatives-to-open-question.md` and `hosts/antigravity/agents/provide-alternatives-to-open-question.md`, and `uv run scripts/build_hosts.py --check` passed.

---
