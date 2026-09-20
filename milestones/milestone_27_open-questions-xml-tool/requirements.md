# Milestone 27: Open Questions XML Tool

## Goal

Split the `## Open questions` section out of `requirements.md` into a sibling `<MILESTONE_DIR>/open_questions.xml` — a well-formed XML document under one root element, created empty by `define-milestone-goal`, whose "no `<open-question>` child remains" state is the convergence verdict and the `derive-tasks` precondition — and ship one stdlib-only Python tool inside the plugin (rendered into every host tree, invoked via `{{PLUGIN_ROOT}}`, and the file's sole writer) that owns every deterministic operation over that document: list, locate, add, lift, remove, embed with fragment validation replacing the seven-test acceptance gate, `<depends-on>` reconciliation in exact-id mode with transitive strip, dependent-strip on prune, and the answer sweep's dependency-graph walk. Rewire every skill, agent, and shared procedure that touches open questions from the `awk`/`sed`/`grep` boundary-line idiom onto tool invocations so that runtime prose keeps only judgment (authoring text, significance ranking, judgment-mode reconciliation for literal answers) and the entity-escaping, indentation, and whole-block-replacement contracts become the tool's internals — the aim being maximal token efficiency — while `capture-milestone-principle-updates` keeps its diff-line reconstruction, repointed at the new file. Give the tool a pytest suite run under `uv` in CI beside the drift gate, document Python 3.9+ as a prerequisite checked once by `init-milestone-base-workflow`, sync `CLAUDE.md`, `README.md`, and `docs/`, and provide no migration of or compatibility with pre-split milestones.

## Relevant starting state

## Decisions

## Out of Scope

