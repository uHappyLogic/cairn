# TASKS TODO

## Create Answer-Recording Shared Procedure

Create a new `shared/answer-procedure.md` — peer to `shared/submit-procedure.md` and `shared/implement-procedure.md` — as the single source of truth for recording an answer to an open question. It documents the `locate → analyse → remove → fold → cascade` core: resolve `<MILESTONE_DIR>` via `shared/get-current-milestone.md`, locate the question block by its Short Title, analyse the answer's implications, remove the matched block, fold the decision into `## Implementation decisions` as clean prose (no citation marker), and cascade to any entry the answer moots. This extracts the recording steps currently duplicated in prose across `answer-open-question` (steps 3–4) and `answer-obvious-open-questions` (step 2c). This task creates only the new shared file; rewiring the callers to reference it is a separate downstream task.

**Provides:**
- `shared/answer-procedure.md` — the shared answer-recording procedure, referenced by callers via the `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` idiom (matching how the other shared procedures are referenced).
- Its input contract: a **resolved Short Title** plus the **answer text** (locating-by-title and cascading are shared; obtaining the title/answer is the caller's job).

**Notes:**
- Model the file's shape on `shared/submit-procedure.md` (intro framing → Inputs → the procedure phases → Rules).
- The file MUST be execution-neutral, exactly as `submit-procedure.md` never mentions the `DONE`/`FAILED` protocol. It must NOT mention: arg-parsing (e.g. splitting on the first `.`), committing, the `Answer-Principle:` trailer, the `Principle-based-answer:` subject, or the `try-capture-answer-principle` chain. That neutrality is what lets one file serve both the staged-edit `answer-open-question` skill and the commit-per-answer orchestrator — pulling any of it in would defeat the file's purpose.
- Name the `locate → analyse → remove → fold → cascade` sequence as the content the file must cover; do not expand it into per-step implementation narration beyond what the existing skill prose already carries.

**Success:**
- `shared/answer-procedure.md` exists at the repo root's `shared/` directory.
- It covers all five phases: locate the question by Short Title, analyse implications, remove the matched block, fold the decision into `## Implementation decisions` as clean prose, and cascade to mooted entries.
- It resolves `<MILESTONE_DIR>` by following `shared/get-current-milestone.md` (not a hardcoded path).
- It names its inputs as a resolved Short Title + answer text.
- It contains zero references to committing, trailers (`Answer-Principle:`/`Principle-based-answer:`), arg-parsing, or principle capture.

---

## Create Try-Answer-Question-By-Principle Subagent

Create `agents/try-answer-question-by-principle.md` — the read-only, single-question candidate-elimination subagent the `try-answer-questions-by-principle` orchestrator dispatches once per Open/Deferred question. Given one question (its Short Title plus context), it reads the project-wide principle store, enumerates the realistic candidate answers, keeps only those each supportable by at least one confirmed principle, and returns a structured verdict naming the unique survivor (if any) and the principles that kept it alive. It mutates nothing — it is read-only on both `requirements.md` and the principle store; the orchestrator owns all document mutation and committing.

**Provides:**
- `agents/try-answer-question-by-principle.md` — the per-question elimination subagent, dispatched by the orchestrator.
- Its input contract: one question's **Short Title + context** (supplied by the orchestrator).
- Its verdict return contract (the orchestrator parses this to emit one `Answer-Principle:` trailer line per load-bearing principle): (a) whether exactly one candidate survives (unique-survivor yes/no); (b) the surviving answer; (c) the **full** set of load-bearing principles supporting the survivor, by `### <Short Title>` handle — every principle that genuinely kept the survivor alive, **not** a curated "most important" subset; (d) the candidate set considered. Auto-answer is warranted only when exactly one candidate survives; two-or-more survivors (including the conflicting-principles case, where different principles imply different answers) or zero survivors both yield a "no unique survivor" verdict.

**Notes:**
- The principle store is `milestones/answer_decision_principles.md` at the `milestones/` **root** — above any `<MILESTONE_DIR>`, shared across all milestones. It is the one file the loop reads at a fixed root path and is **not** resolved via `shared/get-current-milestone.md` (every other reader resolves relative to `<MILESTONE_DIR>` — do not default to that here).
- If the principle store is **absent or empty**, treat it as no principles → nothing is supportable → every candidate is eliminated → the verdict is always "no unique survivor". This must be stated in the agent because the behavior lives in the still-open `Deferred — Missing principle file` block, not in `## Implementation decisions`.
- The candidate set must be the realistic alternatives — the same bar `discuss-open-question` uses when enumerating options. The gate is only as strong as the candidate set, so an impoverished set defeats it.
- The "supportable" test must be a genuine fit, not a rationalization. Apply each principle's **statement**, not its optional `*Origin:*` line.
- Model the agent's shape on `agents/implement-backlog-task.md`, but it is **READ-ONLY** and returns the structured verdict as its final message in place of that agent's `DONE`/`FAILED` protocol. There is no strength-gate / judgment-based answering (the removed `answer-obvious` logic): a confirmed principle is the sole basis for keeping a candidate.

**Success:**
- `agents/try-answer-question-by-principle.md` exists with valid agent frontmatter (e.g. `name`, `description`).
- The body describes reading the principle store at the `milestones/` root, enumerating realistic candidate answers, keeping only those supportable by ≥1 confirmed principle, and returning a structured verdict reporting unique-survivor yes/no, the surviving answer, all load-bearing principles, and the candidate set considered.
- It explicitly states the subagent never edits `requirements.md` or the principle store.
- It explicitly states that an absent or empty principle store yields a "no unique survivor" verdict.

---

## Create Try-Capture-Answer-Principle Skill

Create `skills/try-capture-answer-principle/SKILL.md` — the interactive skill that records or revises a confirmed answering principle extracted from a just-made decision, per the *Capture input contract*, *Capture revise-vs-add*, and *Principle entry schema* decisions in `requirements.md`. It is the first writer of the project-wide principle store `milestones/answer_decision_principles.md`. This task authors only the skill; wiring the unconditional chain-off from `answer-open-question` (and the `reject-auto-answer` chain-in) are separate downstream tasks.

**Provides:**
- `skills/try-capture-answer-principle/SKILL.md` — the principle-capture skill.
- `milestones/answer_decision_principles.md` — the project-wide principle store this skill is the sole writer of (created on first write). Per the *Principle entry schema* decision: one principle per `### <Short Title>` subsection — that heading is the unique citable handle the orchestrator writes to the `Answer-Principle:` commit trailer and the key this skill matches on for revise-vs-add.

**Notes:**
- If `milestones/answer_decision_principles.md` does not exist, this skill **creates it on first write**. State this in the skill because the behavior lives in the still-open `Deferred — Missing principle file` block, not in `## Implementation decisions` (mirrors the read-side note in the sibling subagent task).

**Success:**
- `skills/try-capture-answer-principle/SKILL.md` exists with valid skill frontmatter (`name`, `description`) and a "pushy" trigger description.
- It documents the no-required-param entry that analyzes the current conversation anchored on the most recent decision, and the optional free-text focus hint (including the cold-invocation ask-the-user behavior).
- It documents the brief-report-and-exit-without-engaging path when no generalizable principle can be extracted, running the revise-vs-add flow only on a real candidate.
- It documents the semantic-overlap revise-vs-add flow with **mandatory user confirmation** — never revise-vs-add by title alone, never auto-merge/auto-add silently.
- It documents the principle entry schema it writes (one `### <Short Title>` subsection; body = a generalizable keep/eliminate directive, not a restatement of one decision; optional `*Origin:*` line; no status field) and that it creates the store on first write.
- It states the skill leaves its edit staged and never commits.

---

## Rewire Answer-Open-Question Onto Shared Procedure And Capture Chain

Rewire `skills/answer-open-question/SKILL.md` so it no longer restates the answer-recording steps inline and teaches a principle after every manual answer. Keep its arg-parsing front (split the arg on the **first `.`** into Short Title + answer text); replace its current inline recording prose (the locate → remove block → fold into `## Implementation decisions` → cascade steps, roughly today's steps 2–4) with a reference to `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md`, passing the resolved Short Title + answer text; keep its report tail; and add an unconditional chain-off to `try-capture-answer-principle` after recording. Depends on the already-queued *Create Answer-Recording Shared Procedure* and *Create Try-Capture-Answer-Principle Skill* tasks.

**Notes:**
- Reference the shared procedure exactly as the `submit-backlog-task` / `implement-backlog-task` skills reference their shared procedures — via the `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` idiom. Do **not** duplicate or restate the shared procedure's locate/analyse/remove/fold/cascade steps; the whole point is that the recording mechanism now lives in exactly one place.
- The chain-off to `try-capture-answer-principle` is **unconditional** — `answer-open-question` does not gate it. Capture itself analyzes the conversation and self-decides whether anything is worth capturing (and exits briefly when not), so the caller always invokes it. This capture chain lives in the `answer-open-question` skill **only**; the `try-answer-questions-by-principle` orchestrator deliberately never chains to capture (an auto-answer was itself derived from a principle, so capturing would be circular).

**Success:**
- `skills/answer-open-question/SKILL.md` references `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` for the recording core.
- The inline locate → remove → fold → cascade prose (today's recording steps) is gone — replaced by the reference, not duplicated alongside it.
- The skill retains arg parsing that splits on the **first `.`** into Short Title + answer text.
- The skill ends with an **unconditional** invocation of `try-capture-answer-principle` after recording.
- The skill performs no `git commit` (no-commit invariant preserved); edits are left staged.

---

## Rename And Restructure Sweep Into Principle Orchestrator

Rename the existing `skills/answer-obvious-open-questions/` skill to `skills/try-answer-questions-by-principle/` and restructure its `SKILL.md` from a self-contained judgment-based sweep into an **orchestrator** over the read-only `try-answer-question-by-principle` subagent, per the *Orchestrator / subagent architecture*, *Sweep run scope*, *Autonomous answering*, *Auto-answer commit isolation*, *Principle citation*, and *Sweep run report* decisions in `requirements.md`. The old strength-gate / informed-reader judgment logic is **removed entirely** — a confirmed principle (via the subagent's verdict) becomes the sole basis for any auto-answer. Depends on the already-queued *Create Answer-Recording Shared Procedure* and *Create Try-Answer-Question-By-Principle Subagent* tasks.

**Provides:**
- `skills/try-answer-questions-by-principle/SKILL.md` — the renamed orchestrator skill (the `answer-obvious-open-questions` directory and skill `name:` no longer exist); takes no args and sweeps every Open/Deferred entry.
- The auto-answer commit contract that `reject-auto-answer` and the *Sweep run report* depend on: **exactly one auto-answer per commit**, commit **subject** `Principle-based-answer: <Short Title>` (the answered question's handle), and one **trailer** line `Answer-Principle: <Short Title>` **per** load-bearing principle (repeated key, never comma-separated).

**Notes:**
- The directory rename, the frontmatter `name:`, and the in-body invocation example (`/try-answer-questions-by-principle`) must **all** change together; a stale `name:` or `/answer-obvious-open-questions` example is a defect.
- **Never chain to `try-capture-answer-principle`.** This orchestrator replicates the answer-recording mechanism via the shared procedure but must not chain to capture — the auto-answer was itself derived from an existing principle, so capturing would be circular. The capture chain lives **only** in `answer-open-question`. State this explicitly as a negative invariant; it is easy to drop.
- "Clean" tree (the precondition) means `git status --porcelain` produces **no output** — no staged, unstaged, or untracked changes; ignored files are fine. Check **once** at the start; on a dirty tree, abort with an explicit message telling the user to commit pending changes first and re-run.
- The gathered+ordered question list is an **ordering, not a work snapshot**: walk it **once** (a single ordered pass terminates the sweep — answering only removes questions, nothing adds them), but before each dispatch re-check in the **live** document that the question still exists and is unresolved (a prior answer's cascade may have removed it) and **skip** it if not. No outer re-gather / loop-until-no-survivors wrapper. Ordering decides only *which question goes first*, never *whether* one is answered.
- On no unique survivor (two-or-more survive, conflicting principles, or none survive) leave the question **untouched** — no advisory note.
- Record each unique-survivor answer by referencing `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` (remove the block, fold into `## Implementation decisions` as clean prose, cascade) — reference it, do not restate the locate/analyse/remove/fold/cascade steps.
- Read-side of the still-open `Deferred — Missing principle file` block: on a fresh project where `milestones/answer_decision_principles.md` is absent or empty, the subagent finds no supporting principle for any candidate, so the sweep resolves nothing and (committing nothing) prints the no-op report. State this in the skill; the behavior lives in that Deferred block, not in `## Implementation decisions`.

**Success:**
- `skills/try-answer-questions-by-principle/SKILL.md` exists with frontmatter `name: try-answer-questions-by-principle`; the old `skills/answer-obvious-open-questions/` directory is gone; the in-body invocation example reads `/try-answer-questions-by-principle`.
- It documents the clean-tree precondition (`git status --porcelain` empty, checked once) with an **explicit abort message** instructing the user to commit pending changes and re-run, and captures `BASE=$(git rev-parse HEAD)` at start.
- It documents gathering all Open/Deferred questions up front, ordering them loosely most-significant → least, and walking that order **once** with a per-question live re-check + skip — and contains no outer re-gather loop.
- It documents dispatching the read-only `try-answer-question-by-principle` subagent sequentially (one per surviving question) and that the orchestrator owns **all** document mutation and the commit.
- For a unique survivor it references `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` to record the answer (not a restated/parallel recording mechanism), then commits **one auto-answer per commit** (`git add -A` → commit) with subject `Principle-based-answer: <Short Title>` and one `Answer-Principle: <Short Title>` trailer line per load-bearing principle.
- It documents leaving no-unique-survivor questions untouched (no note), and an end-of-run report that prints a single ready-to-run full-message `git log <BASE>..HEAD` (not a `--grep` form) scoped to this invocation's commits, neither re-serializing per-answer details nor enumerating untouched questions — and that says so in one sentence with **no** `git log` command when nothing was committed.
- The old strength-gate / informed-reader judgment logic is removed entirely, and the skill explicitly states it never chains to `try-capture-answer-principle`.

---

## Create Reject-Auto-Answer Skill

Create `skills/reject-auto-answer/SKILL.md` — the interactive, single-shot skill that reverts one bad auto-answer and reopens its question, per the *Reject-auto-answer contract* decision in `requirements.md`. It resolves a single optional positional argument (HEAD default / commit-ish / text fragment), validates the target is a genuine auto-answer commit, confirms with the user, then reverts it with `git revert --no-commit` and directs the user to re-capture. Depends on the already-queued *Create Try-Capture-Answer-Principle Skill* task (the chain-in target for re-capture) and *Rename And Restructure Sweep Into Principle Orchestrator* task (which produces the commit format this skill validates and reverts against).

**Notes:**
- The auto-answer commit format this skill validates and reverts against is owned by the sweep orchestrator and specified in the *Principle citation* decision: subject `Principle-based-answer: <Short Title>`, one or more `Answer-Principle: <Short Title>` trailer lines (repeated key), commit touches only `requirements.md`. Read exact strings there rather than re-deriving them.
- The skill **never edits the principle store** — the revert alone reopens the question (the one-commit-=-one-auto-answer invariant means the revert restores the deleted question block AND removes the folded decision in one shot), so there is no hand-reconstruction of the reopened question and no principle-file write.

**Success:**
- `skills/reject-auto-answer/SKILL.md` exists with valid skill frontmatter (`name`, `description`) and a "pushy" trigger description.
- It documents the overloaded single-optional-arg resolution order: no argument → `HEAD`; argument that is a valid git rev → use directly as the target commit; otherwise → treat as a text fragment, locate it in `<MILESTONE_DIR>/requirements.md`, and resolve to its introducing commit via `git log -S'<fragment>' -- requirements.md` / `git blame`.
- It documents the validation gate that both paths feed: the resolved target must touch only `requirements.md` AND carry at least one `Answer-Principle:` trailer line, refusing otherwise.
- It documents the mandatory display-and-confirm step (show the resolved commit's `Principle-based-answer:` subject and `Answer-Principle:` trailer line(s) before reverting), and that ambiguous / no-match / non-auto-answer resolution reports and asks the user for an explicit commit id rather than reverting silently.
- It documents reverting via `git revert --no-commit <commit-id>`, left **staged and not committed** (no-commit invariant).
- It documents the conflict path: on a revert that cannot apply cleanly, run `git revert --abort`, name the conflicting commit(s), and hand off to the user — never leaving conflict markers or a half-applied revert.
- It documents the closure: the skill never edits the principle store, surfaces the commit's cited `Answer-Principle:` principle set, directs the user to re-capture (the user picks which principle when more than one is cited — the skill does not auto-target one), and may then offer to chain into `try-capture-answer-principle` with a focus hint naming the chosen principle.

---

## Sync README With Principle-Learning Loop

Bring `README.md` — the public, authoritative workflow documentation — fully in sync with the answer-principle-learning loop introduced by this milestone, across both the Mermaid workflow flowchart and the per-skill reference. Rename the sweep everywhere `answer-obvious-open-questions` appears, add coverage for the new skills/subagent/principle store, and document the manual teaching flow alongside the autonomous sweep and the correction loop. This is a documentation-only update; it must run after the new and renamed skills exist. Updating `CLAUDE.md` is a separate concern and out of scope here.

**Notes:**
- The only two old-name occurrences are README.md line ~77 (Mermaid node `ITM2["<b>/answer-obvious-open-questions</b>…"]`, inside the `S2` "Iterating milestone requirements document" subgraph) and line ~162 (per-skill reference heading `### answer-obvious-open-questions`). Line 164's `answer-open-question` is a different skill that must stay.
- Rename the Mermaid node **label-only**: keep the node ID `ITM2`, change only its bracketed text. Node IDs drive the `class` and `linkStyle` references, so a label-only rename touches nothing structural — only the *added* nodes/edges cause churn. The renamed node's description should reflect that the sweep now applies confirmed principles via candidate elimination, requires a clean tree, and commits one auto-answer per commit citing the principle in an `Answer-Principle:` trailer.
- Edge-index hazard: `linkStyle 11,19,23` (around line 137) uses **0-based edge indices in definition order**; those three are the purple dashed loop-back edges (`ITM4→ITM1`, `SM3→SM1`, `D5→IM1`). Any edge added in/around the `S2` subgraph sits before index 23 and **renumbers all three**, silently mis-coloring the wrong edges — so `linkStyle` must be recomputed after adding edges. Any new loop-back edge (the `reject-auto-answer → re-capture` correction loop is the natural candidate) should reuse the dashed `optional` class + purple `linkStyle` styling to stay consistent with the existing repeat edges.
- Flowchart-node convention: only user-invocable slash-command skills get Mermaid nodes — the dispatched subagents (`submit-backlog-task`, `implement-backlog-task` agents) appear nowhere as nodes. So `try-capture-answer-principle` and `reject-auto-answer` (slash commands) get nodes; the `try-answer-question-by-principle` **subagent** gets a per-skill reference entry only, no Mermaid node. The exact node/edge layout within `S2` is the implementer's call.
- Pull the exact terminology (the `Principle-based-answer:` commit subject, the repeated `Answer-Principle:` trailer key, the `milestones/answer_decision_principles.md` root path, the candidate-elimination / unique-survivor gate, the clean-tree precondition) from the now-built skills/agent and requirements, matching the existing README's tone.

**Success:**
- README.md contains zero occurrences of `answer-obvious-open-questions`.
- The Mermaid `S2` node formerly labelled `/answer-obvious-open-questions` (node ID `ITM2`) now reads `/try-answer-questions-by-principle` with a description reflecting confirmed-principle candidate elimination, the clean-tree requirement, and one auto-answer per commit with an `Answer-Principle:` trailer.
- The per-skill reference heading `### answer-obvious-open-questions` is renamed to `### try-answer-questions-by-principle` with a correspondingly updated description.
- New per-skill reference entries exist for `try-capture-answer-principle`, `reject-auto-answer`, and the `try-answer-question-by-principle` subagent.
- README documents the principle store `milestones/answer_decision_principles.md` (project-wide at the `milestones/` root, accumulating confirmed answering principles), the manual `discuss-open-question → answer-open-question → (auto) try-capture-answer-principle` teaching flow, the autonomous `try-answer-questions-by-principle` sweep, and the `reject-auto-answer → re-capture` correction loop.
- The Mermaid diagram still parses, and every node in it is assigned to a `classDef` via a `class` statement (no unstyled node).

---

## Sync CLAUDE.md With Principle-Learning Loop

Bring `CLAUDE.md` — the repository guidance — fully in sync with the answer-principle-learning loop, across its three affected surfaces: the "Repository layout" tree, the "Skills and the workflow they encode" overview block, and the "Invariants to preserve when editing skills" list (including the no-commit invariant). This is a documentation-only update and must run **last**, after every new/renamed skill, agent, and shared file already exists. Keep all additions in the file's existing terse invariant-bullet style. Updating `README.md` is a separate concern, handled by the *Sync README With Principle-Learning Loop* task and out of scope here.

**Notes:**
- The two existing old-name references to replace are at CLAUDE.md line ~36 (the skills-overview block line `answer-obvious-open-questions   ← …`) and line ~64 (the `answer-obvious-open-questions` invariant bullet). After this task no `answer-obvious-open-questions` string may remain anywhere in the file.
- **Repository layout tree**: add `shared/answer-procedure.md` and `agents/try-answer-question-by-principle.md`, and note the project-wide principle store `milestones/answer_decision_principles.md` at the `milestones/` **root** — above any `<MILESTONE_DIR>`, shared across all milestones (this is the one fixed-path, project-wide artifact the loop reads). The tree keeps its generic `skills/<skill-name>/SKILL.md` placeholder line — it does **not** enumerate individual skills; the new skills appear only in the skills-overview block (next note).
- **Skills-overview block**: rename `answer-obvious-open-questions` → `try-answer-questions-by-principle` (the orchestrator) and update its one-line description; add lines for the `try-answer-question-by-principle` subagent (in `agents/`), `try-capture-answer-principle`, and `reject-auto-answer`. Match the existing arrow-aligned `← …` format.
- **Update — do not merely append to — the existing `answer-obvious-open-questions` invariant bullet (line ~64).** It currently describes a removed skill and asserts the recording mechanism is *reused from* `answer-open-question`. Rewrite it so it (a) describes the renamed orchestrator and (b) records that the answer-recording mechanism now lives **only** in `shared/answer-procedure.md`, which both `answer-open-question` and the `try-answer-questions-by-principle` orchestrator reference and never restate — this **supersedes** the prior state where the recording steps were duplicated in prose between `answer-open-question` and the old answer-obvious skill.
- **Update the no-commit invariant (line ~66) to add a SECOND exception** alongside the existing `implement-backlog-tasks` one: `try-answer-questions-by-principle` commits exactly **one auto-answer per commit** — subject `Principle-based-answer: <Short Title>` (the answered question's handle), one repeated `Answer-Principle: <Short Title>` trailer line per load-bearing principle. Keep "individual skills never commit" true by framing both as the named exceptions.
- Add invariant bullets for: the **read-only-subagent split** (the `try-answer-question-by-principle` subagent is read-only on `requirements.md` and the principle store and returns a verdict only; the orchestrator owns **all** document mutation and the commit — a deliberate divergence from the file-editing `implement-backlog-task` agent); the **capture chain direction** (`answer-open-question` unconditionally chains to `try-capture-answer-principle`; the orchestrator **never** chains to capture, which would be circular since the auto-answer was itself derived from a principle); and `reject-auto-answer` (reverts one auto-answer commit, validated to touch only `requirements.md` **and** carry ≥1 `Answer-Principle:` trailer, leaves the revert staged, and never edits the principle store).
- Pull exact strings (`Principle-based-answer:`, `Answer-Principle:`, `milestones/answer_decision_principles.md`, final skill names) from `requirements.md` and the now-built skills/agent/shared files rather than re-deriving them. Match the terse phrasing density of the surrounding invariant bullets; do not pad.

**Success:**
- `CLAUDE.md` contains zero occurrences of `answer-obvious-open-questions`.
- The Repository-layout tree lists `shared/answer-procedure.md` and `agents/try-answer-question-by-principle.md`, and notes `milestones/answer_decision_principles.md` as the project-wide principle store at the `milestones/` root; it keeps its generic `skills/<skill-name>/SKILL.md` placeholder line and does not enumerate individual skill directories.
- The skills-overview block renames the sweep to `try-answer-questions-by-principle` (orchestrator) and adds lines for the `try-answer-question-by-principle` subagent, `try-capture-answer-principle`, and `reject-auto-answer`.
- The former `answer-obvious-open-questions` invariant bullet is rewritten (not duplicated) to describe the renamed orchestrator and to record that the answer-recording mechanism lives only in `shared/answer-procedure.md`, referenced and never restated by both `answer-open-question` and the orchestrator.
- The no-commit invariant names a second exception: `try-answer-questions-by-principle` commits exactly one auto-answer per commit with subject `Principle-based-answer: <Short Title>` and repeated `Answer-Principle: <Short Title>` trailer line(s).
- Invariant bullets exist for the read-only-subagent split (subagent read-only + verdict-only vs. orchestrator owning all mutation/commit, diverging from `implement-backlog-task`), the capture-chain direction (chained only from `answer-open-question`; orchestrator never chains to capture), and `reject-auto-answer`'s revert-validation-stage behavior and never editing the principle store.
- All additions match the existing terse invariant-bullet style.

---
