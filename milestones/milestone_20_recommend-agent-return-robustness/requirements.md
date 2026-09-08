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
  <alternative id="Boundary-only">
    The extracted region passes only the two boundary tests (first non-whitespace text &lt;alternative, last &lt;/recommendation&gt;); no further structural check runs, and the repair attempt fires only when those two tests fail.
    <advantage>Matches the goal&apos;s wording literally (&quot;runs the existing shape check on that&quot;), adds no prose to the orchestrator, and can never reject a genuinely usable return through an over-strict test.</advantage>
    <drawback>A region carrying a stray &lt;/open-question&gt; line, a second &lt;recommendation&gt; element, or an option naming no alternative gets embedded as-is, and the boundary-line CLI that gathers, idempotency-skips, lifts, and removes blocks then misreads every later pass on that file — a silent corruption the current whole-message test only happened to exclude.</drawback>
  </alternative>
  <alternative id="Line-anchored checks, one gate">
    The two boundary tests plus a short list of line-grep checks in the same idiom form one acceptance gate — the region contains no &lt;open-question&gt;, &lt;/open-question&gt;, &lt;question&gt;, or &lt;/question&gt; line, exactly one &lt;recommendation opening line, at least one &lt;alternative id line, and the option value (entity-unescaped, case-folded) equals one of those ids — and any miss counts as an extraction failure that triggers the single same-session repair, with the corrective prompt naming the failed test and a second miss falling to skip-with-advisory; stray prose between elements is left to the agent&apos;s self-check because it breaks no consumer.
    <advantage>Every test is a grep over exactly the boundary tokens the downstream CLI consumers depend on, so it protects gather, idempotent skip, the recommendation lift, the alternative lift, and whole-block removal without a parser, and a structural miss is the same recoverable emit defect as a wrapping miss, so one control path (extract → check → repair once → skip) covers both.</advantage>
    <drawback>A well-formed but slightly off return (an id with mismatched entity escaping against its option value, an odd attribute layout) costs a repair round, and the longer test list enlarges both the corrective prompt and the agent&apos;s self-check.</drawback>
  </alternative>
  <alternative id="Two-tier gate">
    The boundary tests gate extraction and are repairable, while the structural checks run afterward as a separate acceptance gate whose failure goes straight to skip-with-advisory with no repair attempt.
    <advantage>Keeps &quot;extraction failure&quot; narrowly defined as the wrapping defect the milestone-19 sweep actually observed, so the repair path stays aimed at one known failure.</advantage>
    <drawback>A structural miss is fixable by the same one-line re-emit in the same session, so skipping without repair drops a valid recommendation the goal says must never be dropped, and two failure classes with different handling is more orchestrator prose than one gate.</drawback>
  </alternative>
  <alternative id="Full XML parse">
    Wrap the extracted region in a synthetic root and validate it with a real XML processor (well-formedness, balanced tags, entity correctness) before embedding.
    <advantage>Catches every malformation, including unbalanced or mis-nested elements that no line-grep list anticipates.</advantage>
    <drawback>Contradicts the plugin&apos;s boundary-line-CLI-never-xmllint convention, rejects otherwise usable returns over a single bare &amp; in prose, and depends on a tool the Antigravity host may not provide.</drawback>
  </alternative>
  <recommendation option="Line-anchored checks, one gate">The checks that matter are the ones protecting the downstream boundary-line consumers (no wrapper or question tags inside the region, exactly one recommendation, its option naming an alternative id), all of which are line greps in the same idiom as the two boundary tests, and a miss on any of them is as recoverable by the same-session re-emit as a wrapping miss, so folding them into one extraction gate with one repair attempt keeps the goal&apos;s no-valid-recommendation-dropped promise without adding a second control path.</recommendation>
</open-question>

<open-question id="Failed-return detection under extraction" status="open">
  <question>Once the orchestrator extracts a region rather than testing the whole message, how does it recognise an explicit failure return — only a message whose last line is FAILED: &lt;reason&gt;, or a FAILED: line anywhere in the message — and which wins when a message carries both a FAILED: line and an extractable &lt;alternative&gt;…&lt;/recommendation&gt; region?</question>
  <alternative id="Last-line verdict first">
    Before any extraction, read the return&apos;s last non-whitespace line: if it begins with FAILED: the return is an explicit failure and the question is skipped with that reason and no repair attempt; otherwise extraction runs and a FAILED: token anywhere else in the message is ordinary text. A message carrying both an extractable region and a final FAILED: line is therefore a failure — the agent&apos;s final word is its verdict.
    <advantage>It is the same last-line-token convention the complete-task and answer agents&apos; orchestrators already read, it honours the agent&apos;s own contract (FAILED: as the final line is the one alternative to the elements), and it cannot misfire on a FAILED: mention inside element text — a live risk, since this milestone&apos;s own questions and any recommendation on them quote that token verbatim.</advantage>
    <drawback>A region the agent emitted and then retracted with a trailing FAILED: line is dropped rather than salvaged, and a FAILED: line buried above a complete region is silently ignored in favour of the region.</drawback>
  </alternative>
  <alternative id="Any FAILED line wins">
    Treat any line in the message that begins with FAILED: as an explicit failure return, wherever it sits, and let that failure win over an extractable region: the question is skipped with the text after FAILED: as the reason and no repair is attempted.
    <advantage>Nothing the agent flagged as failed at any point can ever reach the whole-block-replacement Edit, and the check is a single grep.</advantage>
    <drawback>It produces false failures: an &lt;alternative&gt;, &lt;drawback&gt;, or &lt;recommendation&gt; whose text begins a line with FAILED: (exactly what a recommendation about failure handling renders) would discard a valid recommendation — the one outcome the milestone goal forbids — and a stray FAILED: in a preamble would override elements the agent went on to emit.</drawback>
  </alternative>
  <alternative id="Region wins over FAILED">
    Run extraction first and embed whatever region passes; consult FAILED: only when no region extracts, using its presence (last line or anywhere) to tell an explicit failure that should be skipped from a malformed return that should get the repair attempt.
    <advantage>It maximises salvage — a valid region is embedded no matter what surrounds it — and uses the FAILED: token purely as the skip-versus-repair discriminator the extraction path needs.</advantage>
    <drawback>It embeds and later commits a region the agent explicitly disowned (elements followed by FAILED: the analysis is incomplete), trusting the least trustworthy kind of message, and it makes the failure test run in a different position from the last-line test the other two orchestrators use.</drawback>
  </alternative>
  <recommendation option="Last-line verdict first">Test the last non-whitespace line for FAILED: before extracting, let that explicit verdict win over any region above it, and treat FAILED: anywhere else as plain text — it keeps one last-line-token convention across all three dispatch sites and is the only rule immune to the FAILED: token appearing legitimately inside element text.</recommendation>
</open-question>

<open-question id="Continuation-unavailable fallback" status="open">
  <question>When the host cannot continue the finished agent session (no SendMessage equivalent, as under Antigravity, or the agent handle is gone), does the orchestrator fall back to today&apos;s skip-with-advisory, or to a fresh re-dispatch that redoes the analysis, and how does the skill prose express &quot;continue the same session where the host allows it&quot; so both hosts read one instruction?</question>
  <alternative id="Skip with advisory, host-descriptive prose">
    When the host offers no way to continue the finished agent session, the orchestrator treats the repair attempt as unavailable and takes today&apos;s skip-with-advisory for that question; the skill prose names continuation descriptively — continue the same finished agent session with one follow-up message, which Claude Code offers as SendMessage to the returned agent id — and states that where the host offers no such continuation, or the handle is gone, the question falls straight to the skip, so both hosts read one instruction and Antigravity resolves it to extract-then-skip.
    <advantage>Honors the goal&apos;s explicit &quot;never a fresh re-dispatch&quot; and its named floor (skip-with-advisory), costs Antigravity nothing it does not already pay since the new extraction layer alone catches the dominant prefix-wrapping case (eight of ten milestone-19 skips were well-formed elements behind a grounding summary), and reuses the phrasing pattern the skill already uses for the dispatch name (descriptive capability, Claude Code&apos;s concrete name given as the example) so no transpiler change is needed.</advantage>
    <drawback>Under Antigravity a return that extraction cannot salvage stays un-annotated until the user re-runs the sweep, which then redoes that question&apos;s analysis in a fresh dispatch anyway — the redo cost is pushed to a manual re-run rather than avoided.</drawback>
  </alternative>
  <alternative id="Fresh re-dispatch fallback">
    When continuation is unavailable, the orchestrator instead dispatches one fresh recommend-open-question agent for that question with the same prompt plus the shape reminder, and skips only when that second return also fails extraction; the prose becomes a two-branch instruction — continue the session where the host allows it, otherwise re-dispatch once.
    <advantage>No host ever drops a salvageable question within a single run, so the Antigravity sweep reaches the same annotated set as Claude Code without a manual re-run.</advantage>
    <drawback>Directly contradicts the goal&apos;s &quot;never a fresh re-dispatch, which would redo the analysis&quot;, doubles the per-question cost on exactly the host that cannot repair cheaply, gives no assurance the fresh agent will not wrap its output the same way (the wording-only fix already failed once), and turns the single instruction into a host-detecting branch the runner must evaluate.</drawback>
  </alternative>
  <alternative id="Transpiler strips the continuation step">
    Keep the Claude Code prose naming SendMessage directly, and add a prose-anchored rewrite to scripts/migrate_skills_to_agy.py (in the style of the existing resolve-hint drop) that removes the continuation sentences from the generated Antigravity copy, so each host&apos;s file reads only what that host can do and the Antigravity skill collapses to extract-then-skip.
    <advantage>Each host reads an unconditional instruction with no capability wording to interpret, and the transpiler already has a precedent for dropping Claude-Code-only prose.</advantage>
    <drawback>The transpiler grows a content-aware regex over a whole procedural step rather than a stable backtick token, so any later rewording of the skill silently leaves Claude Code prose in the Antigravity tree or over-strips it, and the source and generated files diverge in behavior rather than only in paths, which the current diff -r verification was built to rule out.</drawback>
  </alternative>
  <recommendation option="Skip with advisory, host-descriptive prose">The goal already forbids a fresh re-dispatch and names skip-with-advisory as the floor, extraction alone recovers the dominant failure on both hosts, and the skill&apos;s existing dispatch-name sentence shows how one descriptive instruction with Claude Code&apos;s concrete name as the example serves both hosts without touching the transpiler.</recommendation>
</open-question>

<open-question id="Same-failure test for DONE agents" status="open">
  <question>The complete-task and answer-open-question-with-recommendation agents end with a DONE/FAILED last line, so prose above that line already passes their orchestrators; is trailing text after the DONE/FAILED line the &quot;same failure&quot; that warrants applying last-line extraction (and a repair attempt) to those two agents and their orchestrators, or does this milestone leave all four files untouched?</question>
  <alternative id="Leave all four untouched">
    Scope the extraction/repair pattern to the recommend agent and its sweep only, leaving agents/complete-task.md, agents/answer-open-question-with-recommendation.md, and the complete-all-tasks and answer-all-open-questions-with-recommendation orchestrators byte-for-byte as they are.
    <advantage>It honours the goal&apos;s own test — apply the pattern only where an agent duplicates this exact failure, never as a general audit — and the repo holds no evidence the DONE agents ever failed this way: every milestone-19 task completion and every recommendation-answer dispatch passed on the existing last-line-token contract.</advantage>
    <drawback>If a DONE agent ever does append a closing remark after its DONE line, its orchestrator still reads that as an ambiguous return and report-and-stops the whole loop rather than salvaging a return whose verdict was actually present.</drawback>
  </alternative>
  <alternative id="Full extraction and repair for DONE agents">
    Apply the milestone&apos;s pattern to both DONE agents and their orchestrators — rewrite each agent&apos;s return contract as draft → self-check → emit, have each orchestrator extract the last DONE/FAILED line from the raw return, and continue the same agent session once with a corrective re-emit prompt when no such line is found.
    <advantage>Every dispatched agent in the plugin then shares one uniform return-robustness contract, so a future editor finds a single pattern rather than two.</advantage>
    <drawback>It is the general audit the goal explicitly forbids: it touches four files to fix a failure nothing in the repo records, and the failure is not even the same mechanism — the recommend sweep discards a payload-bearing return on a whole-message shape test, while the DONE agents hand back a bare token checked by its last line, where prose above already passes.</drawback>
  </alternative>
  <alternative id="Tolerant last-line detection only">
    Leave both agents untouched and change only the two orchestrators&apos; return handling so they read the last line matching DONE or FAILED: wherever it sits in the message, tolerating trailing text with no repair attempt and no session continuation.
    <advantage>A one-sentence change per orchestrator closes the only reproduction path (trailing text after the token) without any of the repair machinery or the agent rewrite.</advantage>
    <drawback>It still edits two files on speculation — no occurrence is recorded — and a token-anywhere read weakens the contract, since a FAILED: line quoted mid-message and a DONE verdict at the end can now be confused in a way the strict last-line rule prevents.</drawback>
  </alternative>
  <recommendation option="Leave all four untouched">The goal admits another agent only where it duplicates this exact failure, and the DONE agents do not: their return is a bare last-line token with no payload to salvage, prose above it already passes, and the repo records zero occurrences of trailing text — so touching them would be precisely the general audit the goal rules out.</recommendation>
</open-question>

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

<open-question id="Repair timing under parallel dispatch" status="deferred">
  <question>Whether the orchestrator repairs each return as soon as its extraction fails or collects all first returns and then runs the repair attempts, given that dispatches may run in parallel and each repair needs that dispatch&apos;s agent handle.</question>
  <alternative id="Repair on arrival">
    The orchestrator handles each dispatch&apos;s return as it arrives: extract, shape-check, and when extraction fails send the corrective re-emit prompt to that agent&apos;s handle immediately, while the other dispatches are still running, so step 3 stays one per-return pipeline (check, repair once, re-check, embed or skip).
    <advantage>Repairs overlap with still-running dispatches, so the sweep&apos;s wall-clock stays close to the slowest single question plus one repair, and each handle is used at the moment its notification delivers it, with no held list of handles and raw returns to bookkeep.</advantage>
    <drawback>First returns and repaired returns interleave in arbitrary order, so the orchestrator must remember per question whether the repair was already spent to guarantee the single corrective attempt and never repair twice.</drawback>
  </alternative>
  <alternative id="Collect then repair">
    The orchestrator waits until every first return has arrived, then runs the repair attempts for the failed subset as a second phase (in parallel via each held handle), and only then embeds.
    <advantage>A clean two-phase narrative that is easy to state in skill prose: dispatch all, gather all, repair the failed set, gather again, then embed, with the repair set known once and no interleaving of first and second returns.</advantage>
    <drawback>No repair can start before the slowest first dispatch returns, so with the milestone-19 pattern (eight of ten failing) the whole repair round serialises behind the last first return, and the orchestrator must hold every failed return&apos;s handle and raw text idle across that wait.</drawback>
  </alternative>
  <alternative id="Sequential dispatch with inline repair">
    Drop parallel dispatch: dispatch one question, extract, repair inline if needed, embed or skip, then dispatch the next.
    <advantage>Simplest possible control flow: exactly one live handle at any time, no per-question state, and the repair-once rule is trivially enforced.</advantage>
    <drawback>Gives up the parallelism step 3 already grants (dispatches are independent by the recommendation-independence invariant), multiplying wall-clock by the question count for no correctness gain.</drawback>
  </alternative>
  <recommendation option="Repair on arrival">Each return is independent and its embed is a whole-block replacement of its own block, so nothing is gained by synchronising before repair; repairing as each extraction fails keeps step 3 a single per-return pipeline, uses the handle the moment the notification hands it over, and lets repairs overlap in-flight dispatches, while the only added cost is a one-bit per-question &quot;repair spent&quot; marker.</recommendation>
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

<open-question id="Extracted-region re-indentation" status="deferred">
  <question>How the orchestrator normalises the indentation of an extracted region (for example one emitted at column 0 or inside a fenced code block) to the 2-space-per-level depth of the existing &lt;question&gt; child before the whole-block-replacement Edit.</question>
</open-question>

<open-question id="Agent rewrite boundary" status="deferred">
  <question>Whether the ground-up rewrite of the agent&apos;s return contract replaces only step 4 or merges the step-3 rendering shape and step-4 return into one draft → self-check → emit step, and how much of the current prohibition list survives as the self-check&apos;s test list.</question>
  <alternative id="Replace step 4 only">
    Keep step 3 as the untouched rendering specification (element shape, indentation, entity escaping) and rewrite step 4 alone as a draft → self-check against exactly the two shape tests → emit step, dropping the prohibition list whole and keeping only the positive &quot;every grounding finding is spent inside the elements&quot; redirect as drafting guidance.
    <advantage>The failure was a wrapping failure, not a rendering failure, so the rewrite lands exactly where the defect is; step 3 stays a stable, greppable rendering contract that the CLAUDE.md applied-principle invariant and the orchestrator&apos;s embed step already rely on, and the two tests subsume every listed prohibition (any preamble fails the first, any closing remark fails the second) so nothing is lost by cutting the list.</advantage>
    <drawback>Leaves the draft &quot;render&quot; and the emit &quot;check&quot; in two steps, so a runner could still treat step 3&apos;s output as its final message and skip the step-4 check unless step 4 opens by naming step 3&apos;s output as the draft.</drawback>
  </alternative>
  <alternative id="Merge steps 3 and 4">
    Fold the rendering shape and the return contract into a single draft → self-check → emit step, where the draft is rendered to step 3&apos;s current shape, the self-check tests the two shape tests plus the structural rendering rules (one &lt;recommendation&gt;, its option naming an &lt;alternative id&gt;, escaping), and the emit is the checked draft.
    <advantage>One step owns the whole path from analysis to final message, so the draft-and-check mechanic cannot be skipped by stopping after rendering, and the self-check can also catch structural slips the orchestrator would otherwise have to test for.</advantage>
    <drawback>Produces one very long step that mixes a content spec with a message-discipline mechanic, widens the self-check beyond the two tests the goal names (encroaching on the structural checks that are the orchestrator&apos;s concern), and churns the rendering prose that was never the source of the failure.</drawback>
  </alternative>
  <alternative id="Prohibitions become tests">
    Rewrite step 4 as draft → self-check → emit but carry the current prohibition list forward as the self-check&apos;s named tests (no grounding summary, no file list, no no-principle note, no closing remark) alongside the two shape tests.
    <advantage>Preserves the concrete, observed failure patterns from the milestone-19 sweep so the runner recognises its own habitual preambles by name rather than only by boundary test.</advantage>
    <drawback>Reproduces the mechanism that already failed once (commit 2475078 added exactly this list and eight of ten dispatches still wrapped their output), and every listed pattern is already caught by the two boundary tests, so the extra tests add length without adding coverage and reintroduce an enumeration the goal explicitly says to replace.</drawback>
  </alternative>
  <recommendation option="Replace step 4 only">The defect is the final-message wrapping, not the rendering, so the rewrite should replace step 4 with a draft → self-check → emit step whose only test list is the two shape tests (which subsume every current prohibition), keep step 3 as the stable rendering contract, and open step 4 by naming step 3&apos;s rendering as the draft so the check cannot be bypassed.</recommendation>
</open-question>
