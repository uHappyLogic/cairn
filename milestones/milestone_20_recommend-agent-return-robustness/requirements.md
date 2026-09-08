# Milestone 20: Recommend Agent Return Robustness

## Goal

Make the `recommend-all-open-questions` sweep robust to a `recommend-open-question` agent return that wraps otherwise well-formed XML sub-elements in surrounding text, so that no valid recommendation is ever dropped: the orchestrator first extracts the sub-element region (first `<alternative` through last `</recommendation>`) from the raw return and runs the existing shape check on that, and when extraction fails it continues the *same* agent session once with a corrective re-emit prompt where the host allows it (never a fresh re-dispatch there, which would redo the analysis), and where the host cannot continue the session (no continuation equivalent, or the agent handle is gone) it re-dispatches one fresh agent with the same prompt plus the shape reminder — falling back to today's skip-with-advisory only when the repair attempt, or that second return, also fails extraction. Rewrite the agent's return contract from the ground up — replacing the accumulated prohibition list with a draft → self-check against the two shape tests → emit final step — and apply the same extraction/repair pattern to another dispatched agent only where it duplicates this exact failure, never as a general audit. Claude Code is the target host and the Antigravity build takes the fresh re-dispatch branch where session continuation is unavailable; this deliberately reverses the "discarded whole, never salvaged" invariant.

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

### Continuation-unavailable fallback

When the host cannot continue the finished agent session (no `SendMessage` equivalent, as under Antigravity, or the agent handle is gone), the orchestrator falls back to a **fresh re-dispatch**, not straight to the skip: it dispatches one fresh `recommend-open-question` agent for that question with the same prompt plus the shape reminder, and skips with advisory only when that second return also fails extraction. The skill prose expresses this as a two-branch instruction — continue the same session where the host allows it, otherwise re-dispatch once. This fallback is limited to the continuation-unavailable case; where continuation is available the same-session corrective re-emit remains the repair path, and the Goal's "never a fresh re-dispatch" clause is to be read as governing that case only.

### Scope of the extraction/repair pattern

The extraction and repair pattern is scoped to the `recommend-open-question` agent and the `recommend-all-open-questions` sweep only: `agents/complete-task.md`, `agents/answer-open-question-with-recommendation.md`, and the `complete-all-tasks` and `answer-all-open-questions-with-recommendation` orchestrators are left byte-for-byte untouched. Trailing text after a `DONE`/`FAILED` line is not the same failure the Goal admits another agent for — those returns are bare last-line tokens with no payload to salvage, prose above the token already passes their check, and the repo records zero occurrences of trailing text — so changing them would be precisely the general audit the Goal rules out.

### Failed-return detection under extraction

The orchestrator recognises an explicit failure return by a **last-line verdict tested before extraction**: it reads the return's last non-whitespace line first, and if that line begins with `FAILED:` the return is an explicit failure — the question is skipped with that reason and no repair attempt is made, even when an extractable `<alternative>`…`</recommendation>` region sits above it. Only when the last line is not a `FAILED:` line does extraction run, and a `FAILED:` token appearing anywhere else in the message is then ordinary text with no special meaning. This keeps one last-line-token convention across all three dispatch sites and is the only rule immune to the `FAILED:` token appearing legitimately inside element text.

### Extracted-region acceptance checks

The extracted region is accepted by a single gate that combines the two boundary tests (first non-whitespace text starts with `<alternative`, last ends with `</recommendation>`) with a short list of line-grep checks in the same idiom: the region contains no `<open-question>`, `</open-question>`, `<question>`, or `</question>` line, exactly one `<recommendation` opening line, at least one `<alternative id` line, and an `option` value (entity-unescaped, case-folded) equal to one of those `<alternative>` ids. Any miss — boundary or structural — counts as an extraction failure and triggers the single same-session repair attempt, with the corrective prompt naming the failed test; a second miss falls to skip-with-advisory. Stray prose between the child elements is left to the agent's own self-check, because it breaks no consumer. The check list is deliberately confined to greps over the boundary tokens the downstream boundary-line CLI depends on — gather, idempotent skip, the recommendation lift, the alternative lift, and whole-block removal — so the gate needs no XML parser and no second control path.

### Agent rewrite boundary

The ground-up rewrite replaces **step 4 of `agents/recommend-open-question.md` only**: step 3 stays the untouched rendering specification (element shape, indentation, entity escaping), and step 4 becomes a draft → self-check → emit step whose only test list is the two shape tests (first non-whitespace text starts with `<alternative`, last ends with `</recommendation>`), which subsume every entry of the current prohibition list. That prohibition list is dropped whole, keeping only the positive "every grounding finding is spent inside the elements" redirect as drafting guidance, and step 4 opens by naming step 3's rendering as the draft so the self-check cannot be bypassed by treating step 3's output as the final message.

### Repair timing under parallel dispatch

The orchestrator repairs each return on arrival: as each dispatch's return comes back it extracts, checks, and — when extraction fails — sends the corrective re-emit prompt to that agent's handle immediately, while the other dispatches are still in flight, rather than holding every failed return and running the repairs as a second phase once the slowest first return has landed. Step 3 therefore stays a single per-return pipeline (check, repair once, re-check, embed or skip), and repairs overlap in-flight dispatches. Because first and repaired returns then interleave in arbitrary order, the orchestrator carries a per-question "repair spent" marker so the single corrective attempt is never spent twice.

## Out of Scope

## Open questions

<open-question id="Corrective re-emit prompt wording" status="deferred">
  <question>What the corrective message sent to the continued agent session says — whether it quotes the two shape tests, names what the previous message violated, and asks for nothing but the elements.</question>
  <alternative id="Fixed test-quoting instruction">
    A frozen one-paragraph template rendered once in the orchestrator skill, sent unchanged to every continued session: re-emit the recommendation as the bare sub-elements only, with the two shape tests quoted verbatim (first non-whitespace text starts with &lt;alternative, last ends with &lt;/recommendation&gt;) and an explicit &quot;nothing before, nothing after&quot; clause, but no statement of what the previous message did wrong.
    <advantage>A single fixed string with no per-return composition, so the repair step is as mechanical as the shape check itself and reads identically under Claude Code and the Antigravity transpile; the agent still holds its finished analysis in context, so the exact bar is all it needs to re-emit.</advantage>
    <drawback>An agent whose miss was structural rather than a wrapping preamble (a missing &lt;/recommendation&gt; because it emitted a trailing note, an included &lt;open-question&gt; wrapper) gets no pointer to its actual defect and may repeat it, spending the one repair attempt.</drawback>
  </alternative>
  <alternative id="Test-quoting plus violated-test naming">
    The same frozen template with one slot: the orchestrator fills in which of the two tests the previous message failed (the same reason string it already derives for the step-6 skip advisory, e.g. &quot;your last message ended after &lt;/recommendation&gt; with a closing remark&quot;), without quoting the offending prose back, then asks for the elements and nothing else.
    <advantage>Names the defect the agent must remove using a reason the orchestrator computes anyway for the advisory, so the single repair attempt is aimed rather than blind at zero extra composition cost, and the template stays a fixed string rendered once with one slot.</advantage>
    <drawback>The slot makes the orchestrator responsible for phrasing the failure accurately per return; a vague or wrong reason string could steer the agent toward fixing the wrong end of its message.</drawback>
  </alternative>
  <alternative id="Bare elements-only nudge">
    A one-line message such as &quot;Reply with only the XML sub-elements, nothing else&quot; that neither quotes the tests nor names the violation, relying on the agent&apos;s own step-4 contract for the exact shape.
    <advantage>Shortest possible message, trivially host-neutral, and adds no prose to the skill.</advantage>
    <drawback>The agent already had the two tests in its own contract and still failed them (eight of ten dispatches in the milestone-19 sweep), so a nudge that restates less than the contract is the wording-only fix the milestone exists to move past and is the least likely to repair in one try.</drawback>
  </alternative>
  <recommendation option="Test-quoting plus violated-test naming">Quote both shape tests so the agent re-runs its own self-check against the exact bar, fill the one slot with the failure reason the orchestrator already records for the advisory so the repair is aimed, and close with an elements-only request; this keeps the message a fixed single-slot template while making the one repair attempt count.</recommendation>
</open-question>

<open-question id="Repaired-return console advisory" status="deferred">
  <question>Whether a question whose recommendation was embedded only after extraction stripped surrounding text, or only after the repair attempt, is mentioned on the console alongside the terse line, or whether the embedded result alone is the record.</question>
  <alternative id="Embedded result alone">
    Neither extraction nor a successful repair attempt is mentioned on the console; a question whose elements arrived wrapped or re-emitted is treated exactly like a clean return, and only the still-skipped questions appear in the step-6 advisory.
    <advantage>Matches the terse-reporting rule&apos;s test for what survives alongside the terse line — an advisory must be both git-absent and decision-critical — since the embedded block is in the diff and is identical in kind to a clean return, so nothing about the user&apos;s decision on the question changed; it also makes the wrapping failure the routine non-event the milestone goal sets out to make it, like complete-procedure&apos;s silent resume from partial work.</advantage>
    <drawback>The sweep loses its only signal of how often the agent&apos;s rewritten return contract still fails (extraction or repair firing on most dispatches would be invisible), so a contract regression surfaces only once the repair attempt also fails and a question is actually skipped.</drawback>
  </alternative>
  <alternative id="Advisory for every recovered return">
    Alongside the terse line, print one line per question whose elements were embedded only after extraction or only after the repair attempt, naming the Short Title and which path recovered it.
    <advantage>Keeps the agent&apos;s return-contract health visible run by run, so the user can see whether the ground-up rewrite actually stopped the wrapping rather than merely masking it.</advantage>
    <drawback>Re-narrates a success path the diff already records, contradicting the terse-reporting rule&apos;s decision-critical test, and given that eight of ten milestone-19 returns were wrapped it would list most questions on most sweeps, burying the real skip advisory in noise.</drawback>
  </alternative>
  <alternative id="Advisory for repair only">
    Extraction-only recoveries stay silent, but a question embedded only after the session-continuation repair attempt is listed in the step-6 advisory with its Short Title.
    <advantage>The repair is the rarer, costlier, and more fallible event (a re-emit can drift from the first analysis), so flagging only it keeps the advisory infrequent and meaningful while routine text-stripping stays a non-event.</advantage>
    <drawback>Introduces a second tier of recovered-but-succeeded reporting the step-6 rule must define, and still prints a success-path line the commit already records; the re-emitted region passes the same checks as a clean return, so the line reports how the elements arrived, not anything different about what was embedded.</drawback>
  </alternative>
  <recommendation option="Embedded result alone">The embedded block is the record: a recovered return changes nothing the user must decide, so under the terse-reporting rule it earns no console line — and if re-emit drift is the real worry, that belongs in the extracted-region acceptance checks, not in the report.</recommendation>
</open-question>
