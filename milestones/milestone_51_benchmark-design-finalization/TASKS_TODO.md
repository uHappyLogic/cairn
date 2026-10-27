# TASKS TODO

## Draft Run Isolation And Environment Rules

Rewrite the draft's isolation, one-run, and manifest text for the four isolation decisions: web search and fetch stay enabled with each run's tool calls, queries, fetched URLs, and network-reaching shell commands recorded, a run that reached the benchmark repository, its run branches, or its Pages site marked contaminated and the text stating, consistently with the void policy, whether such a run is excluded or re-run; a fresh host configuration directory per run from a committed content-versioned template reached through CLAUDE_CONFIG_DIR, recorded in the manifest in place of the `user_config` digests, credentials injected from outside and the directory deleted with the clone after the Run: commit; confinement by a dedicated unprivileged benchmark user on the development Mac with no container or second machine; and a content-versioned environment definition listed among the shared inputs that the pre-flight probes the live machine against. Verify by reading the sections against the four decisions and gap 4.

---

## Draft Run Ending And Sequencing Rules

Rewrite the draft's one-run procedure, manifest, and phase text so the harness classifies how each invocation ends and voids a run on the first infrastructure failure (recorded with a void marker naming cause and invocation, excluded from rating, never a phase-2 parent, replaced by a fresh run from the same parent, nothing retried, a distinct void line printed), detects a stop by matching each cairn invocation's final message against the delivery's per-line allowlist of fixed success and no-op lines with a detected stop ending the chain as a non-zero exit does and the first stopping line recorded as `invocations.first_stop`, sets no time, turn, or spend limit while recording wall-clock duration, runs strictly sequentially behind a run lock with the phase-2 start reworded as a queue-ordering rule, and only asserts a root `index.html` exists, recording a null entry otherwise with the hand-set exception removed. Verify by reading the procedure, the manifest, and the phase-2 text against the five decisions and gaps 5, 6, 8, and 13.

---

## Draft Rater Scope And Calibration Rules

Rewrite the draft's rater section for the four rating decisions: the rater receives the entry file plus every file in the run's tree reachable from it by load or link, followed transitively, and nothing else; a not-proved verdict gets one more attempt by a fresh rater session under the same rater definition and only a second not-proved scores zero, the not-proved count counting survivors only; one randomly chosen run per scenario per prompt is re-rated blind under the same rater version with scores using the first rating only and no threshold applied; and a calibration set per prompt version, one reference artifact plus deliberately broken variants so every test line is failed by at least one and reference items for each reading line, with recorded verdicts, which a rater version must reproduce exactly through the normal rating path, a single mismatch refusing it, before it may rate the set. Verify by reading the section against the four decisions and gaps 7 and 8.

---

## Draft Comparison Set And Input Versioning

Rewrite the draft's comparison-set, input, and trend text: a set is five versions (the seed tag, one prompt version per phase, the operator definition, the rater definition, and one pinned host CLI version the pre-flight refuses a run against when the installed one differs, a new rater version re-rating existing runs into a new set without re-running); it declares before its first scored run a roster holding at least the stated minimum scenarios and three phase-1 runs per scenario each with its own phase-2 child and no stopping rule; the checklist and hidden-requirement entries are frozen by blob hash before that run with a changed statement starting a new set and a changed check line a new rating version; a superseded set carries an authored one-line reason without which regeneration refuses; the trend restarts as a labeled segment on every input change with nothing re-run; and everything stays public with a canary, a dated contamination flag read from published training cutoffs, and a rotation rule. Verify by reading the text against the seven decisions and gaps 11, 12, 15, and 16.

---

## Draft README Table And Radar Rework

Rewrite the draft's README page section and the rank paragraph: the table's and the radar's openings recast as refutable expectations naming the table and the curves as what would refute them, each score cell carrying its minimum and maximum beside the mean as `82 (76–88)` with cost, time, invocations, and sessions staying means, ranks shared within a tie margin derived from the set's own per-run noise with cost playing no part, the hidden axis keeping its equal third with the stated reason, one declared reference scenario per family drawn on the radar whatever the ranking, five curves with the clarify family's rows and curve added, the voided-run count and causes beside the runs column, the repeat-rating agreement line and the lost column's noise floor, and the generated list of superseded sets with versions, input diff, reason, and link. Verify by reading the section against the nine decisions it carries and gaps 11, 16, and 18.

---

## Separate Draft Examples From Cairn Claims

Pass over the whole draft so every concrete example value (scenario ids, the manifest's plugin and host versions, model ids) is kept but stated once as a hypothetical example tracking no real version, while every statement about the current content of a Cairn document or tool, the tested-claim count in `docs/design-claims.md` first, points at that document without restating a value that moves. Verify by searching the draft for version numbers, model ids, and Cairn document references and confirming each is a marked example or a pointer.

---

## Audit Gap Coverage And Remove Report

Read `ideas/benchmark_design_gaps.md` gap by gap against the finished draft, confirm each of the eighteen ends as a decision written into the draft, adopted, adapted, or rejected with its reason stated in the text, write in any reason still missing, then remove the report as the milestone's last change so the draft is the single document under `ideas/` handed to the benchmark repository. Verify that the file is gone from the working tree and reachable only in git history from `aeb280a`, and that the draft refers to the report nowhere.

---
