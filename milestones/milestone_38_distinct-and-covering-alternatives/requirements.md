# Milestone 38: Distinct and covering alternatives

## Goal

Rewrite the enumeration rules of `core/shared/alternatives-procedure.md` so an alternative set maps the decision space instead of shortlisting candidates: every two alternatives differ in substance on at least one axis, the set covers the underlying decision rather than the question's wording (including "drop it / don't do it" where honestly viable), each option states where it stands on each axis in its what-it-is prose, and on a multi-axis question every combination is weighed in reasoning and each viable one described, with no count guideline hiding the growth; `review-milestone-requirements` authors new questions one axis each so that growth is prevented upstream. The change is verified by a one-off re-run of the alternatives pass over historical override cases held outside the repository, and the milestone also writes two uncommitted idea documents under `temp/`: one for a committed benchmark harness, one for further improvements to how `review-milestone-requirements` frames questions (shared premises, splitting existing compound questions). No committed artifact — requirements, open questions, tasks, commit messages, docs — may carry any information from the benchmark data or the private projects it comes from; only aggregate results and generic pattern descriptions are committed.

## Relevant starting state

### Enumeration rules

`core/shared/alternatives-procedure.md` is the single source of the enumeration work: ground in the project (step 1), then enumerate (step 2). It is followed once per question by the read-only `provide-alternatives-to-open-question` subagent, and inline by `discuss-open-question` when the block it deliberates is bare. Step 2 asks for "the genuinely realistic options — typically two to four", bans strawmen and padding, lets a question with one viable path say so, and gives each option three fields: what it is ("one sentence"), key advantage, key drawback. It requires the set to be "complete now" because every later pick chooses from it, but does not say what a complete set is: nothing requires two options to differ in substance, names an axis, or mentions dropping the thing the question is about. Step 1 bounds the question by its siblings (an option that really answers a sibling is left to that sibling), and the procedure forms no preference.

### Restatements of those rules

Two runtime files repeat parts of step 2. The agent file `core/agents/provide-alternatives-to-open-question.md` calls the first field "the what-it-is sentence" in its rendering step, tells the agent to spend every grounding finding inside the three fields, and otherwise defers to the procedure. `core/skills/discuss-open-question/SKILL.md` step 3 says a bare block gets "the 2–4 honest alternatives", and reuses an embedded set exactly as it stands, allowing an option the set lacks only as a marked departure. The orchestrator `core/skills/provide-alternatives-to-all-open-questions/SKILL.md` and `core/shared/recommend-procedure.md` state no count and no enumeration rule: the first only judges and embeds returns, the second takes the set as given and never adds or drops an option.

### How an alternative is stored and reused

An `<alternative id>` element holds the what-it-is text as its own text, with `<advantage>` and `<drawback>` children. The open-question tool's `embed --alternatives` requires at least one alternative and sets no upper count and no length limit; it folds every text to one line and refuses text outside the elements and any unknown element, so a block has no place for a statement about the set as a whole. `lift --alternative` prints `<id> — <what-it-is>`: on the `Alternative-answer:` path that line is the answer folded into `## Decisions` and the commit body, while the recommendation path records `<option> — <rationale>` instead. `capture-milestone-principle-updates` reads each alternative's id and what-it-is text from the answered block's removed diff lines.

### Question authoring

`core/skills/review-milestone-requirements/SKILL.md` is the sole author of question blocks. Step 3 adds each new gap through the tool's `add` and asks for two judgments: a question text that stands on its own (brief, self-contained, question-shaped, never a design proposal) and a unique 2–5 word Short Title. No rule limits how many choices one question may bundle. Step 2 removes a block only when a recorded decision covers it or it repeats another, and flags rather than deletes on doubt; it has no operation that splits or rewrites a block, and `CLAUDE.md` records that boundary as the tidy-vs-record invariant.

### Documentation and rationale

`docs/skill-reference.md` has one entry per skill: its `discuss-open-question` entry repeats "2–4 honest alternatives", and its entries for the alternatives pass, the subagent, and the review skill describe mechanics without an enumeration or authoring rule of this kind. `docs/design-claims.md` claim 4 states that the recommender "gives 2 to 4 real alternatives, each with one advantage and one drawback" and names a judge score for alternative quality as its metric; the page says no suite runs that test. The `CLAUDE.md` invariants explain why the enumeration and pick halves stay two files and how the two passes run, and say nothing about what makes a set complete.

### Build and verification

Runtime prose is edited under `core/` and rendered into `hosts/claude/` and `hosts/antigravity/` by `uv run scripts/build_hosts.py`; the committed trees must pass `--check`. `.claude-plugin/marketplace.json` points the maintainer's install at `./hosts/claude`, so a session in this working copy runs the rebuilt tree. The pytest suite under `tests/` covers only the Python tools, so no test reads the prose this milestone changes.

### Re-running the alternatives pass

The pass annotates only blocks carrying no `<alternative>`; a block that already has a set is regenerated by the tool's bare `strip` followed by a re-run. Each subagent receives the question's Short Title and the milestone directory and grounds itself in the working tree it runs in, and the orchestrator makes one `Alternatives-annotation:` commit per annotated question in that repository. `docs/ways-of-using-cairn.md` documents the headless form, `claude -p "/cairn:provide-alternatives-to-all-open-questions"` with a model and an effort setting. The tool stops on its `Error:` line for a milestone that has no `open_questions.xml`.

### Benchmark material outside the repository

`temp/` is listed in `.gitignore`. It holds the idea note `temp/orthogonal-alternatives-idea.md` and the directory `temp/orthogonal-alternatives-bench/`, with the extracted override commits, their judged verdicts, and a transcript scan. In aggregate, of 106 manual answers that replaced a block already carrying alternatives, 65 refined a listed option, 20 took a direction no option represented, 12 took a combination on an axis the set never laid out, and 9 rejected a premise every option shared; 13 sets held near-duplicate options, and 20 cases are rated strong candidates for a re-run. The most frequent missing direction is not doing the thing the options vary.

### Known gaps

No benchmark harness, eval directory, or judge exists in the repository. Neither idea document the goal names exists under `temp/` yet.

## Decisions

### Question authoring

- `review-milestone-requirements` step 3 gains the one-axis rule as a third requirement on the question text — each question asks one choice — and names no test for detecting a second axis; detection is left to the author's judgment, as with the step's other authoring rules. Designing a detection test is left to a separate future milestone: the candidate tests (an independent-settlement test, surface-wording cues, an option-grid preview, and an independence test prompted by wording cues) are carried into the uncommitted `temp/` idea document on how `review-milestone-requirements` frames questions.
- Choices in one gap that constrain each other, so that not every pairing is viable, are authored by `review-milestone-requirements` as a single multi-axis question, a named exception to the one-axis rule. Both choices are asked at once, and the enumeration weighs every combination in reasoning and describes only the viable ones.

### Enumeration rules

- Step 2 of `alternatives-procedure.md` opens with a mandatory axes-first move: before any candidate is drafted, the enumerator names the axes the underlying decision turns on, then builds the options as positions on those axes (on a multi-axis question, as combinations weighed in reasoning). Distinctness and coverage are stated as the tests the resulting set must pass.
- Step 2 carries its own explicit instruction, separate from the general coverage requirement, to weigh on every question the direction of not doing the thing the question is about. That direction is listed as an option when it is honestly viable and left out otherwise, with no dedicated place recording that it was considered.
- A degree or parameter value counts as an axis like any other: the set lists a separate alternative for each degree or value at which the key advantage or drawback genuinely changes, and values whose trade-off is the same are merged into one option described by its range.
- The what-it-is field drops its one-sentence limit for a content bound with no count: it holds only what the option is, meaning its position on each axis, and any reason for or against it belongs in the advantage and drawback fields. Its length follows from how many positions there are to state.
- Postponing the decision is not a separate direction: it counts as one form of the "not in this milestone" direction, so a set lists at most one option for not doing the thing now, and the answer text says whether that means never or later.
- Premise-finding is folded into the axis work rather than stated as a rule of its own: each assumption the question's wording takes for granted is treated as one more axis of the decision, with accepting and rejecting it as its values, so rejecting a premise comes out of the same step that lays out the other axes.
- Sibling questions still bound a set's coverage, so no option varies on a sibling-owned axis. The enumeration step requires each option to name any sibling-owned axis its viability depends on, stated as a condition in its drawback without naming the expected outcome.

### Verification

- The one-axis authoring rule is verified with a synthetic compound fixture: a small throwaway milestone under `temp/` whose `requirements.md` deliberately leaves a gap with two or more independent axes, against which `review-milestone-requirements` is run in a scratch working copy to check that it authors one question per axis. The fixture holds one independent pair and one coupled pair, so both the split and its interdependence exception are exercised.
- The one-off check re-runs all 20 historical cases already rated strong candidates (16 where the answer took a direction no option represented, 4 where it took a combination on an axis the set never laid out) and adds no other missed-direction cases.
- The check also re-runs control cases: a small fixed sample of the refinement overrides, the manual answers that refined an option the historical set already listed. For each, it checks that the re-run set still holds that option's direction and has no near-duplicate or filler options.
- The check runs a paired single baseline: the unchanged `alternatives-procedure.md`, taken from the commit before the rewrite, is run once on every re-run case with the same model and effort setting as the new-rules run, and each case's two sets are compared side by side.
- Each case runs in a clone outside this working copy: the source repository is cloned into a scratch directory (for example under the system temp directory), the parent of the answer commit is checked out, and the alternatives pass runs there with the rebuilt `hosts/claude` plugin tree loaded explicitly. The clone is deleted once its set has been read, and the source repository is only ever read.
- If the check falls short of its bar, the milestone revises the enumeration wording once and re-runs the check. If it still falls short after that single round, the milestone records the aggregate shortfall and finishes with the best wording it has.
- Whether a re-run set contains the direction the historical answer took is decided by a separate judge agent with its own context, given only the historical answer, the recorded missing direction, and the re-run set, and not told which rule version produced the set. The user receives only its verdicts.
- The check sets no absolute pass share: the change counts as verified when the new rules recover the missing direction in clearly more of the same cases than the unchanged rules recover when run with the same model, with the margin for "clearly more" fixed before the runs.
- Both the new-rules run and the baseline run use `--model "opus"` at `--effort high`, the setting the alternatives pass actually runs at in the maintainer's chains, on every re-run case and control case. The two runs of a case are made back to back, so the `opus` alias resolves to the same release for both.

### Documentation

- `docs/skill-reference.md` states the new rules briefly in the entries they govern: the enumeration rules in the `discuss-open-question`, `provide-alternatives-to-all-open-questions`, and alternatives-subagent entries, and the one-axis rule in the `review-milestone-requirements` entry. Claim 4's Design in `docs/design-claims.md` is rewritten to say the alternatives are distinct and cover the decision, with no count; its Metric line stays as it is. `docs/workflow.md` is not edited, and `CLAUDE.md` is not edited under this decision, its invariant entry being decided separately.
- `CLAUDE.md` gains a dedicated invariant bullet explaining why an alternative set must be distinct and covering (every two options differ in substance on an axis, and the set covers the underlying decision, including dropping the thing where viable), why the "two to four" count guideline was removed and must not be restored, why each option states its axis positions, and how the one-axis authoring rule in `review-milestone-requirements` stops the set from growing. It states the rule and its generic failure patterns without measurement figures.

## Out of Scope

