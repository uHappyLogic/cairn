# Milestone 31: Inline answer sweep

## Goal

Make `/answer-all-open-questions-with-recommendation` an inline single-writer skill that dispatches no agent: it gathers the dispatch order with one `walk` call, reads the question set once for context, then for each question in that order runs the shared answer-with-recommendation procedure itself (lift as the re-check, locate, fold, remove with the lifted option, cascade) and commits that answer through the shared commit procedure under the unchanged `Recommendation-answer: <Short Title>` subject with the lifted line as body, one commit per answer, unattended. It records every surviving pick as given and never judges picks; a contradiction it happens to notice is reported once alongside the terse status line while the run proceeds. The end-of-run check is the cheap one: `walk` prints nothing beyond the blocks the cascades stripped, reported as the existing still-skipped advisory, with no document re-read. The `answer-open-question-with-recommendation` agent is deleted as its only consumer goes inline. Both answer procedures take a caller-resolved `MILESTONE_DIR` in place of their own milestone lookup, and every answer runner resolves it once and passes it down; the capture path stays untouched, and the CLAUDE.md invariants, skill reference, workflow, design claims, headless chains, and both host trees are updated to the two-agent, inline-sweep shape.

## Relevant starting state

### The answer sweep (`core/skills/answer-all-open-questions-with-recommendation/SKILL.md`, 135 lines)

The sweep is an orchestrator: it resolves `<MILESTONE_DIR>` through `shared/get-current-milestone.md`, gathers its dispatch order with one `walk` call, walks that order exactly once, and per question runs `lift` as the re-check (a failing `lift` is the skip, never a document read), holds the printed `<option> — <rationale>` line as the commit body, dispatches the `cairn:answer-open-question-with-recommendation` agent strictly sequentially, and on `DONE` commits the index the agent staged under `Recommendation-answer: <Short Title>` with that line as body, behind a nothing-staged guard and never `--allow-empty`. A `FAILED:` or ambiguous return stops the loop; the orchestrator never records an answer itself. It has no clean-tree precondition, reads `open_questions.xml` only through `walk` and `lift`, and reports one terse line, `Recommendations recorded.`, or one distinct no-op sentence, deliberately not enumerating recommendation-less questions. Its cost is measured in this repository's own history: milestone 30's sweep recorded 13 answers between 15:05 and 15:27 on 2026-09-22, about 100 seconds per answer, and each dispatch re-reads the project instructions (`CLAUDE.md`, about 2,950 words), the two answer procedures plus the milestone lookup (about 1,600 words), and the growing `requirements.md` (about 4,200 words for that milestone) before touching one block.

### The dispatched agent (`core/agents/answer-open-question-with-recommendation.md`, 56 lines)

The agent carries `name`, a one-clause `description` ending in its invocation contract, and the Claude-only `color: yellow` key that the Antigravity definition strips. It takes one Short Title, follows `shared/answer-with-recommendation-procedure.md`, then stages exactly `<MILESTONE_DIR>/open_questions.xml` and `<MILESTONE_DIR>/requirements.md` by name without committing, and ends on a bare `DONE` or `FAILED: <reason>` line, the reason taken verbatim from the tool's `Error:` line. The sweep is its only consumer; nothing else dispatches it. It is rendered into `hosts/claude/agents/` and `hosts/antigravity/agents/` beside `complete-task.md` and `provide-alternatives-to-open-question.md`, so both host trees hold three agents today.

### The shared procedures (`core/shared/`)

`answer-with-recommendation-procedure.md` (57 lines) takes one input, SHORT TITLE, resolves the milestone, lifts the block with `lift` (the whole line is ANSWER, the text before the first spaced em dash is RECORDED OPTION), and delegates to `answer-procedure.md`; its opening paragraph names its two consumers as the single-question skill inline and the agent in isolation. `answer-procedure.md` owns locate (a `locate` call), analyse (does the answer moot or force another entry), fold into `## Decisions` before removal, `remove --option` with the lifted id passed verbatim, and the cascade of bare `remove` calls for mooted entries, each fold a separate targeted edit. `commit-procedure.md` takes PATHS, SUBJECT, and optional BODY, runs the dirty-own-path guard (`git status --porcelain -- <PATHS>`), stages the named paths, and commits with `-m "<SUBJECT>" -m "<BODY>"`; it is the mechanism every committing skill uses, including the per-answer commit of the single-question skill. None of the three procedures names an orchestrator-versus-agent split in its inputs.

### The single-question skill (`core/skills/answer-open-question-with-recommendation/SKILL.md`)

This skill already runs the lift-then-delegate procedure inline, explicitly never spawning the agent, then follows the commit procedure with PATHS of the two milestone files, SUBJECT `Recommendation-answer: <Short Title>`, and BODY the lifted line. Its clean stop relays the `lift` call's `Error:` line and points at `/recommend-all-open-questions` or a literal `/answer-open-question`. It reports `Answer recorded.` plus the one git-absent advisory (new open questions the decision may raise, never added without confirmation) and then stays available for follow-up. It is the working template for an inline recording step that commits per answer.

### The inline precedent (`core/skills/recommend-all-open-questions/SKILL.md`)

Milestone 30 turned the recommendation pass into an inline skill that dispatches no agent: it gathers its set with one `list` filter, stops naming any block lacking alternatives, reads the whole question set once for reasoning, writes blocks through `embed --recommendation` in any order, commits once per run with the lifted lines as body, then sorts and commits the reorder separately, and prints one of two terse status lines chosen by what the run committed. It is the one existing skill that reasons over the whole question set in the main conversation, and the docs (`docs/workflow.md`, `docs/skill-reference.md`) describe it with the phrase "inline, dispatching no agent".

### Tool surface the sweep uses (`core/tools/open_questions.py`)

`walk` prints the ids of every block carrying a `<recommendation>` in dispatch order (dependency targets first, document order for ties, cycles broken by promoting the document-order-first member) and prints nothing when no such block exists. `lift` prints the one-line answer text or fails with an `Error:` line when the block is absent or carries no `<recommendation>`. `locate` prints the block verbatim; `remove --option` deletes the block and reconciles its dependents in the same write, keeping every `<alternative>`. The test suite under `tests/` exercises the tool only; no test references the agent or the sweep skill beyond `test_walk.py`'s docstring naming "the answer sweep's dispatch order".

### Commit conventions and the capture path

Every recorded recommendation is one commit touching exactly `open_questions.xml` and `requirements.md` under `Recommendation-answer: <Short Title>` with the lifted line as body; the history holds 216 such commits. `capture-milestone-principle-updates` walks these commits path-scoped to `open_questions.xml`, reads subject, body, and diff per commit, treats the `Recommendation-answer:` subject as evidence only, and reconstructs the answered block from the removed diff lines. Revert-then-re-answer correction relies on the same one-commit-per-answer granularity. The commit marker, body, and file set are what the goal leaves unchanged.

### Documentation and invariant surfaces naming the agent

`CLAUDE.md` names the agent in the layout table ("the three dispatched subagents"), the pipeline listing ("skill inline, agent for the sweep"), the "Mutation-in-agent inversion" invariant, the answer-sweep invariant ("the agent stages, the orchestrator commits"), the committing invariant ("an orchestrator commits the index its agent staged … `answer-all-…` per answer"), and the dispatched-agent return contracts ("the other dispatch sites keep a last-line token"). `docs/skill-reference.md` carries a sweep entry describing the orchestrator-agent split and a separate `answer-open-question-with-recommendation (agent)` entry. `docs/workflow.md` describes the sweep only by what it records, `docs/design-claims.md` claim 19 states "a skill and its agent differ only in where the procedure runs: inline or isolated", and `docs/ways-of-using-cairn.md` invokes the sweep on four headless chain lines with `--model "opus"` at `--effort high` or `xhigh`. `CHANGELOG.md` and `milestones/README.md` mention the agent as history only.

### Host build and drift gate

`scripts/build_hosts.py` discovers every `core/agents/*.md` as an agent definition requiring frontmatter and renders it into each host's `agents/` directory per `[layout]`; deleting a core agent file removes it from both trees on the next `uv run scripts/build_hosts.py`, and `--check` fails until the rebuilt trees are committed. The two host definitions differ for agents only in `strip_frontmatter_keys = ["color"]` on Antigravity. CI runs `--check` and both pytest runs in one job with no path filter.

### Console reporting conventions

Success paths print one fixed identifier-free status line per run; only git-absent decision-critical advisories survive beside it, and the sweep invariant already lists "still-skipped questions" among them. No-op passes print one distinct line, and failure paths quote the tool's `Error:` line verbatim. The rule is authored inline in each SKILL.md's reporting step; there is no shared report procedure.

## Decisions

### Milestone resolution

The find-milestone step is removed from both `answer-with-recommendation-procedure.md` and `answer-procedure.md`; `MILESTONE_DIR` becomes a required input that every caller resolves once through `get-current-milestone.md` and passes in, the outer procedure handing it on to the recording core. The callers are `answer-open-question`, `answer-open-question-with-alternative` (which already resolves and holds it before delegating), the single-question `answer-open-question-with-recommendation` skill, and the inline sweep, which resolves it once per run so every `lift`, `locate`, `remove`, and commit in the run uses the directory it walked. Neither procedure branches on whether the input was supplied, matching how the alternatives agent already receives an already-resolved milestone directory.

### Skipped-question reporting

The sweep names no skipped question. A question whose `lift` call fails mid-run, whether because an earlier cascade removed it as moot or stripped its pick, is skipped silently: the run prints only its terse status line or its no-op line, keeps no record of failed lifts during the loop, and adds no end-of-run call to find them. The commit diffs record the stripped blocks, and the next `/recommend-all-open-questions` pass picks them up through its `list --without-recommendation` filter. The CLAUDE.md invariant that stripped dependents get no console advisory stands unchanged.

### New-question reporting

The sweep carries no new-question advisory. Beside its terse status line it prints only the contradiction advisory the goal names, when it noticed a contradiction, and the end-of-run completeness anomaly, when the check fires; it does not report new open questions a recorded decision may have raised, even though it now records inline. Those are left for the next `/review-milestone-requirements` pass, the sole author of question blocks. The single-question answer skills keep their new-question advisory unchanged.

### End-of-run completeness check

The sweep keeps one end-of-run `walk` call as a completeness check, not as a skipped-question advisory. A single pass either records a block or finds it stripped or removed by a cascade, so `walk` is expected to print nothing; any id it does print means a recommendation-bearing block was left unrecorded, and the sweep reports that as an anomaly beside its terse status line, alongside the contradiction advisory. The check never finds, records, or names skipped questions, so the skipped-question decision stands, and the run still does no document re-read. The goal's end-of-run sentence, which describes the `walk` print as the still-skipped advisory, is to be revised through `/modify-milestone-goal` to describe this completeness check instead.

### Retired agent in the invariants

The "Mutation-in-agent inversion" invariant is deleted from `CLAUDE.md`, and the answer-sweep invariant is rewritten to describe only the inline shape, with no mention of the retired per-question recording agent and no retirement clause or reason. The inline description itself rules the agent out; the agent's history stays in `CHANGELOG.md`, `milestones/README.md`, and this milestone's commits.

### Whole-set context read

Before the loop the sweep reads `open_questions.xml` and `requirements.md` in the milestone directory whole, once, with the file-reading tool, for reasoning only — the idiom the review, recommendation, and discuss skills already use for whole-set reasoning. The snapshot gives the answer core's analyse step and the contradiction advisory their view of every sibling and recorded decision. The skill text keeps it apart from the live reads: the `walk` call still gathers and orders, the `lift` call stays the per-question re-check and skip, and the answer core's `locate` print and the live `requirements.md` take precedence over the snapshot once cascades land. The snapshot never gathers, orders, re-checks, or confirms a skip.

### Mid-question failure handling

When any tool call fails after a question's decision has been folded into `requirements.md`, the sweep stops the whole run at once: it reports that question's Short Title with the tool's `Error:` line quoted verbatim and leaves the question's uncommitted edits in the working tree as they are, with no rollback, snapshot, or skip-and-continue. Every earlier answer is already committed, so what remains is the fold-before-remove superset (or, when a cascade `remove` failed, the recorded answer plus a partial cascade), a resumable tree rather than an untouched one, matching the `complete-task` return promise. The sweep never writes `open_questions.xml` outside the tool to undo such a state, and never continues past it, so a stranded fold cannot ride into the next answer's commit.

### Headless chain sweep settings

All four answer-sweep lines in `docs/ways-of-using-cairn.md` (the mixed-agent review and executing-tasks chains, and both lines of the stuck-milestone chain) move from `--model "opus"` at `--effort high` or `xhigh` to `--model "fable" --effort high`, the same settings as the `/cairn:recommend-all-open-questions` line. Opus suited the sweep when each question cost a fresh dispatch re-reading everything; inline, the whole-set context is paid once per run, and the run that holds the growing `requirements.md` across sequential folds and cascades has the same shape as the recommend line. Each affected way's settings sentence is rewritten to say so. Under milestone 30's run-before-record rule, the page edit lands only after a confirming run of the new settings on this repository.

## Out of Scope

