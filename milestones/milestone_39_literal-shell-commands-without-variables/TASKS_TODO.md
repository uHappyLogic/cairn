# TASKS TODO

## State Literal-Path Rule in Commit Procedure

Add the shell-neutral literal-path rule to `core/shared/commit-procedure.md` as prose next to each of its two example commands, which stay exactly as written (`git status --porcelain -- <PATHS>` in step 1, `git add <PATHS>` in step 2): every path is written out on the command line as its own argument and none is held in a shell variable, and step 1 also gains the "naming each path explicitly" wording step 2 already has. This is the first of the two provoking sites where a shell that does not split an unquoted variable makes a run fail. Verified by reading both steps against the "Commit procedure examples" decision, rebuilding `hosts/` with `uv run scripts/build_hosts.py`, and `uv run scripts/build_hosts.py --check` passing.

---

## Restate Literal-Path Rule in Complete-Task Agent Staging

Extend the existing `git add` sentence ("naming each path explicitly") in the "Staging contract" section of `core/agents/complete-task.md` with the same shell-neutral wording the commit procedure now carries — each path appears literally on the command line, never through a shell variable — because the dispatched agent reads no other file and stages the largest path set in the workflow. Verified by comparing the two sentences for matching wording, rebuilding `hosts/`, and `uv run scripts/build_hosts.py --check` passing.

---

## Add Full-Command Clause to Five Tool Sites

Add one clause to the tool-contract sentence in the opening paragraph of each of the five multi-call sites (`review-milestone-requirements`, `provide-alternatives-to-all-open-questions`, `recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, and `core/shared/answer-procedure.md`), along the lines of "write the full command shown on every call; never define a variable, alias, or function of your own to stand for it or any part of it", sitting next to the command where the sentence already spells it out and referring to the full command as shown in each fenced block where it does not. The answer sweep's clause is worded to cover every tool call the run makes, including the per-question calls of the procedures it follows (the lift procedure's `lift`, and `answer-procedure.md`'s `locate`, `remove`, and cascade `remove`), while `core/shared/answer-with-recommendation-procedure.md`, every fenced call, and the commands themselves stay untouched and the prose names no host, no shell, and not the plugin-root segment. Verified by finding exactly one such clause in each of the five files, the tool contract still one sentence per site, `hosts/` rebuilt, and `uv run scripts/build_hosts.py --check` passing.

---

## Add Full-Command Clause to Alternatives Agent

Attach the same full-command clause, in the wording the five tool sites now carry, to the step-1 tool-contract sentence of `core/agents/provide-alternatives-to-open-question.md` ("You reach `open_questions.xml` through exactly two calls …"), stated once with neither fenced call annotated and the commands untouched, because the dispatched agent reads only its own file and its two calls share the command prefix a runner would shorten into a variable. Verified by comparing the clause against the five sites for matching wording, rebuilding `hosts/`, and `uv run scripts/build_hosts.py --check` passing.

---

## Record Literal-Command Invariant in CLAUDE.md

Add one new standalone bullet under `## Invariants to preserve when editing skills` in `CLAUDE.md` recording the shell-splitting failure, the literal-path rule at `commit-procedure.md` and the `complete-task` agent's staging, the full-command rule for every runner that calls the open-question tool more than once (the five sites and the alternatives agent), and why the fix is a prose rule rather than a structural one such as a commit tool; it scopes the invariant to those sites by naming the `capture-milestone-principle-updates` snapshot (`SNAPSHOT="$(mktemp)"`, used quoted) as outside the rule, and leaves the open-question-tool bullet and the committing bullet unchanged with no pointer added. Verified by reading the bullet against the "CLAUDE.md rationale" decisions and, as the milestone's closing check, by `uv run scripts/build_hosts.py --check`, `uv run pytest`, and `uv run --no-project --python 3.9 --with pytest pytest` all passing with no file under `docs/` and no line of the capture skill changed.

---
