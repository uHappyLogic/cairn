# Milestone 20: Recommend Agent Return Robustness

## Goal

Make the `recommend-all-open-questions` sweep robust to a `recommend-open-question` agent return that wraps otherwise well-formed XML sub-elements in surrounding text, so that no valid recommendation is ever dropped: the orchestrator first extracts the sub-element region (first `<alternative` through last `</recommendation>`) from the raw return and runs the existing shape check on that, and when extraction fails it continues the *same* agent session once with a corrective re-emit prompt (never a fresh re-dispatch, which would redo the analysis), falling back to today's skip-with-advisory only when the repair attempt also fails. Rewrite the agent's return contract from the ground up — replacing the accumulated prohibition list with a draft → self-check against the two shape tests → emit final step — and apply the same extraction/repair pattern to another dispatched agent only where it duplicates this exact failure, never as a general audit. Claude Code is the target host and the Antigravity build degrades gracefully where session continuation is unavailable; this deliberately reverses the "discarded whole, never salvaged" invariant.

## Relevant starting state

### The recommend agent's return contract

`agents/recommend-open-question.md` (about 1,100 words) is the read-only per-question subagent. Its step 3 renders the sub-elements (the `<alternative id>` elements with child `<advantage>`/`<drawback>`, zero or more `<applied-principle>` siblings, one `<recommendation option>`), and its step 4 is the return contract: the success return is the bare sub-elements as the final message with **no `DONE` line**, the failure return is `FAILED: <reason>` as the final line with nothing else. Step 4 already states the orchestrator's mechanical test (first non-whitespace text `<alternative`, last `</recommendation>`), says a failing message "is discarded whole and the question is skipped — the well-formed elements inside it are never salvaged", and lists the concrete preambles that fail it (grounding summary, "I have what I need", file lists, a no-principle-bears note, closing remarks). That paragraph was added by commit `2475078` (2026-09-07) after **eight of ten dispatches in the milestone-19 sweep** prefixed otherwise well-formed elements with a grounding summary and were skipped — i.e. the wording-only fix has already been applied once and the failure persists. The agent's prompt from the orchestrator carries the Short Title, the resolved `<MILESTONE_DIR>`, and the full `<open-question>` block; the agent reads `requirements.md`, the live project, and the principle store itself.

### The sweep orchestrator's shape check and skip path

`skills/recommend-all-open-questions/SKILL.md` (about 1,500 words) gathers blocks once via the boundary-line CLI (step 1), skips blocks already carrying a `<recommendation>` element (step 2), dispatches one `cairn:recommend-open-question` agent per surviving block via the `Agent` tool — dispatches are independent and may run in parallel (step 3) — embeds by whole-block-replacement `Edit` (step 4), commits once at the end under `Recommendation-annotation: <milestone_id>` through `shared/commit-procedure.md` (step 5), and reports (step 6). The shape check lives in step 3 and runs on the **raw return**: a `FAILED:` return or any shape miss is a per-question skip, never a run stop — nothing is embedded, the block stays byte-for-byte untouched, and the Short Title plus reason is printed as a git-absent advisory alongside the terse `Recommendations embedded.` line. There is no extraction step, no retry, and no second contact with the agent after its return; a skipped question is retried only by re-running the whole sweep, which re-dispatches fresh (redoing the analysis). The step-6 advisory, the step-5 all-skipped no-op note, and the "never salvaged" wording in the agent are the three places the skip-only behavior is written down in the runtime layer.

### Session continuation available to the orchestrator

Claude Code's `Agent` tool returns a spawned agent's final message and its agent id; a `SendMessage` to that id continues the same agent with its context intact, whereas a new `Agent` call starts fresh. No cairn skill or agent currently uses `SendMessage` or any form of session continuation — every dispatch site is fire-once (the only "resume" in the layer is `complete-task`'s resume-from-uncommitted-work on a later fresh run). Under Antigravity there is no documented equivalent; the transpiled skill would read the same prose and can only do what the host offers.

### The other two dispatched agents and their orchestrators

`agents/complete-task.md` and `agents/answer-open-question-with-recommendation.md` end with `DONE` or `FAILED: <reason>` as the very last line and hand back no payload. Their orchestrators (`complete-all-tasks` step 2b, `answer-all-open-questions-with-recommendation` step 2c) treat a return without an explicit `DONE`/`FAILED` as `FAILED`, **stop the loop** (report-and-stop, not skip), and never do the agent's work themselves. Their contract is a last-line token, not a whole-message shape, so a message with prose above the final `DONE` line already passes; the only way the same wrapping failure reproduces there is trailing text *after* the `DONE`/`FAILED` line. Nothing in the repo records that failure ever occurring for those two agents.

### Antigravity build and documentation surfaces

`scripts/migrate_skills_to_agy.py` copies `agents/`, `skills/`, and `shared/` into `.agents/plugins/cairn/` and rewrites `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` references to `.agents/plugins/cairn/shared/<name>.md`, dropping the `echo "$CLAUDE_PLUGIN_ROOT"` resolve hint; agent bodies are otherwise copied verbatim, and the checked-in tree currently matches the source for both files except for those rewrites. `CLAUDE.md` carries the governing invariants: the recommend-sweep invariant (orchestrator as sole mutator, whole-block-replacement embed, idempotent skip, recommendation independence) and the "Dispatched-agent return contracts are resumable and shape-checked" invariant, which states the shape check and the per-question skip. `README.md`'s `## Skill reference` entries for `recommend-all-open-questions` and `recommend-open-question (subagent)` describe the bare-sub-elements return but do not mention the shape check or the skip path. The "Runtime files carry no editor-facing prose" invariant means the agent's return-contract rewrite must hold only runner-facing instructions, with the rationale living in `CLAUDE.md`. There is no test suite; agent-layer changes are verified by reading the files and regenerating the Antigravity tree (`uv run scripts/migrate_skills_to_agy.py`, then `diff -r`).

## Decisions

## Out of Scope

## Open questions

<open-question id="Extracted-region acceptance tests" status="open">
  <question>Beyond the two boundary tests (region starts with &lt;alternative, ends with &lt;/recommendation&gt;), what structural checks must the extracted region pass before it is embedded — for example exactly one &lt;recommendation&gt; element, its option attribute naming one of the region&apos;s &lt;alternative id&gt; values, and no stray text or &lt;open-question&gt;/&lt;question&gt; tags between the child elements — and does a check failure count as an extraction failure that triggers the repair attempt?</question>
</open-question>

<open-question id="Failed-return detection under extraction" status="open">
  <question>Once the orchestrator extracts a region rather than testing the whole message, how does it recognise an explicit failure return — only a message whose last line is FAILED: &lt;reason&gt;, or a FAILED: line anywhere in the message — and which wins when a message carries both a FAILED: line and an extractable &lt;alternative&gt;…&lt;/recommendation&gt; region?</question>
</open-question>

<open-question id="Continuation-unavailable fallback" status="open">
  <question>When the host cannot continue the finished agent session (no SendMessage equivalent, as under Antigravity, or the agent handle is gone), does the orchestrator fall back to today&apos;s skip-with-advisory, or to a fresh re-dispatch that redoes the analysis, and how does the skill prose express &quot;continue the same session where the host allows it&quot; so both hosts read one instruction?</question>
</open-question>

<open-question id="Same-failure test for DONE agents" status="open">
  <question>The complete-task and answer-open-question-with-recommendation agents end with a DONE/FAILED last line, so prose above that line already passes their orchestrators; is trailing text after the DONE/FAILED line the &quot;same failure&quot; that warrants applying last-line extraction (and a repair attempt) to those two agents and their orchestrators, or does this milestone leave all four files untouched?</question>
</open-question>

<open-question id="Corrective re-emit prompt wording" status="deferred">
  <question>What the corrective message sent to the continued agent session says — whether it quotes the two shape tests, names what the previous message violated, and asks for nothing but the elements.</question>
</open-question>

<open-question id="Repair timing under parallel dispatch" status="deferred">
  <question>Whether the orchestrator repairs each return as soon as its extraction fails or collects all first returns and then runs the repair attempts, given that dispatches may run in parallel and each repair needs that dispatch&apos;s agent handle.</question>
</open-question>

<open-question id="Repaired-return console advisory" status="deferred">
  <question>Whether a question whose recommendation was embedded only after extraction stripped surrounding text, or only after the repair attempt, is mentioned on the console alongside the terse line, or whether the embedded result alone is the record.</question>
</open-question>

<open-question id="Extracted-region re-indentation" status="deferred">
  <question>How the orchestrator normalises the indentation of an extracted region (for example one emitted at column 0 or inside a fenced code block) to the 2-space-per-level depth of the existing &lt;question&gt; child before the whole-block-replacement Edit.</question>
</open-question>

<open-question id="Agent rewrite boundary" status="deferred">
  <question>Whether the ground-up rewrite of the agent&apos;s return contract replaces only step 4 or merges the step-3 rendering shape and step-4 return into one draft → self-check → emit step, and how much of the current prohibition list survives as the self-check&apos;s test list.</question>
</open-question>
