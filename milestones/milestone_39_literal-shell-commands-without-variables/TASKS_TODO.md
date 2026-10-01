# TASKS TODO

## Add Full-Command Clause to Alternatives Agent

Attach the same full-command clause, in the wording the five tool sites now carry, to the step-1 tool-contract sentence of `core/agents/provide-alternatives-to-open-question.md` ("You reach `open_questions.xml` through exactly two calls …"), stated once with neither fenced call annotated and the commands untouched, because the dispatched agent reads only its own file and its two calls share the command prefix a runner would shorten into a variable. Verified by comparing the clause against the five sites for matching wording, rebuilding `hosts/`, and `uv run scripts/build_hosts.py --check` passing.

---

## Record Literal-Command Invariant in CLAUDE.md

Add one new standalone bullet under `## Invariants to preserve when editing skills` in `CLAUDE.md` recording the shell-splitting failure, the literal-path rule at `commit-procedure.md` and the `complete-task` agent's staging, the full-command rule for every runner that calls the open-question tool more than once (the five sites and the alternatives agent), and why the fix is a prose rule rather than a structural one such as a commit tool; it scopes the invariant to those sites by naming the `capture-milestone-principle-updates` snapshot (`SNAPSHOT="$(mktemp)"`, used quoted) as outside the rule, and leaves the open-question-tool bullet and the committing bullet unchanged with no pointer added. Verified by reading the bullet against the "CLAUDE.md rationale" decisions and, as the milestone's closing check, by `uv run scripts/build_hosts.py --check`, `uv run pytest`, and `uv run --no-project --python 3.9 --with pytest pytest` all passing with no file under `docs/` and no line of the capture skill changed.

---
