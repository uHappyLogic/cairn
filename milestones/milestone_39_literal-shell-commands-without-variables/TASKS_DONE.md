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
