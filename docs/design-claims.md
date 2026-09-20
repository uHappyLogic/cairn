# The design claims of cairn

This page lists the 19 design claims Cairn makes, in six groups, each with the
design that makes it true and one metric for a test. The claims are written in
ASD-STE100 Simplified Technical English, a controlled register whose short
sentences and one-meaning-per-word vocabulary keep each claim unambiguous, so
that it reads the same to a reader and to the author of a test. Each **Metric**
line names the test that would check its claim; no test suite in the repository
runs those tests yet.

## Decisions

### 1. Cairn finds the open questions before the work starts.

- **Design:** The review skill reads the requirements and writes each gap as an
  open question. Task derivation does not start while an open question remains.
- **Metric:** The number of planted gaps found, and the number of review passes
  to convergence.

### 2. Each decision has a record in git.

- **Design:** One answer makes one commit. The commit subject shows how the
  answer was made: manual, recommendation, or alternative. A revert of that
  commit opens the question again.
- **Metric:** Commits per decision (must be 1), and the result of a revert test.

### 3. The person decides. The machine gives advice only.

- **Design:** A recommendation is advice. A principle changes the weight of an
  option. It does not block an option. The user can record a different
  alternative. A goal change shows its effect on the decisions, but does not
  change them.
- **Metric:** The count of decisions recorded without a user command (must be
  0, unless the user started a batch skill).

### 4. Advice comes from the live project and shows its sources.

- **Design:** The recommender reads the project, not its memory. It gives 2 to
  4 real alternatives, each with one advantage and one drawback. It gives one
  recommendation with a direct reason. It names each principle it applied and
  each sibling recommendation it used.
- **Metric:** Judge score for alternative quality, and the count of
  recommendations without a clear option.

### 5. Advice gets better with each milestone.

- **Design:** The capture skill reads the decisions where the user did not
  accept the recommendation. It writes the reasons as principles in one store.
  The recommender reads that store. Principle citations are separate elements,
  so the recorded decision text stays clean.
- **Metric:** Agreement between the recommendation and the recorded decision,
  with and without the store.

### 6. Related questions are answered in the correct order.

- **Design:** A recommendation names each sibling recommendation it depends on.
  The batch answer skill walks that graph from its origins. When an answer
  agrees with a dependent question, the cascade removes the dependency tag.
  When it does not agree, the cascade removes the children of the dependent
  question.
- **Metric:** Golden-file result on a seeded graph, and the count of recorded
  decisions with an out-of-date reason.

## Work

### 7. Each requirement becomes a task, and each task has proof.

- **Design:** Task derivation makes a coverage matrix before it writes the
  tasks. Task completion derives an acceptance bar and records it in the done
  list as `**Verified:**` bullets.
- **Metric:** Recall of requirement IDs in the tasks and in the verified
  bullets.

### 8. Cairn makes the detailed design late, against the live project.

- **Design:** A task holds only a title and 1 to 3 sentences. The completer
  makes the detailed design at completion time. It reads the live deliverables
  of the previous tasks, not a promised contract.
- **Metric:** Task body length, and the count of references that do not match
  the live project.

### 9. Work is bounded: one milestone, one task at a time.

- **Design:** One pointer names the current milestone. The finish skill must
  run before the next milestone starts. Tasks run in dependency order, one at a
  time.
- **Metric:** Pointer state after each skill, and the order of the task
  commits.

## Records

### 10. The repository is the memory.

- **Design:** The milestone files and the git log hold the full record. A new
  session reads them and can answer questions about the project. No chat
  transcript is necessary.
- **Metric:** Score of a new session on a fixed question bank about the
  project.

### 11. The records are machine-readable.

- **Design:** Open questions are XML blocks in one section. A line-oriented CLI
  finds each block by its boundary lines. Each edit is a deterministic
  line-range change.
- **Metric:** Golden-file diff of the document after an answer, a cascade, or
  a prune.

### 12. Repository hygiene is structural.

- **Design:** Each skill stages only its own paths, never all files. Each
  commit subject has a marker that names the skill function. A pass that
  changes nothing makes no commit. The work tree is clean after each skill,
  with two exceptions. The bootstrap skill does not commit and leaves its
  changes staged for the user. A failed run leaves its partial work in the
  tree for the next run. The console shows one status line and does not
  repeat the diff.
- **Metric:** Count of unknown subjects, unscoped stages, and dirty trees after
  a run (each must be 0).

## Efficiency

### 13. Each unit of work runs with the smallest necessary context.

- **Design:** One subagent does one task or one question, and then stops. The
  orchestrator holds no work context. It gets a bare DONE, a bare FAILED, or
  the ready-to-embed elements only. Task bodies are minimal. A shared procedure
  loads only when a step needs it.
- **Metric:** Tokens per task, orchestrator context size as the task count
  increases, and total cost per milestone.

### 14. Unattended batch runs are possible.

- **Design:** The batch skills recommend, answer, and complete all items in one
  run. They gather the items once and run strictly in sequence. The user starts
  them and reads the git log after.
- **Metric:** Milestones completed with 0 user turns after the start, and their
  scores on the other claims.

## Robustness

### 15. A run can stop and continue without loss.

- **Design:** A failed task leaves its partial work in the tree, and the next
  run continues from it. A bad subagent return gets one repair, then a skip,
  never a run stop. The answer skill records the decision before it removes the
  question, so an interruption leaves a safe superset.
- **Metric:** Result of a kill-and-resume test: work continued, not done again.

### 16. When in doubt, cairn keeps the record and flags it.

- **Design:** When the cascade is not sure, it strips the dependent question
  and does not answer it. Review flags a possibly resolved question and does
  not delete it. Bootstrap never overwrites a file. Capture writes the
  principle store, but commits only after the user reads the diff. On
  rejection, it restores the snapshot.
- **Metric:** Count of records lost without a user command (must be 0).

## Engineering

### 17. One source of truth, no drift.

- **Design:** The runtime layer is written once, in `core/`. Each host tree is
  a build of it. Each shared procedure is referenced and never restated. The
  build gate fails on any drift, locally and in CI.
- **Metric:** Result of the drift gate on each commit, and the count of
  restated procedures (must be 0).

### 18. The same behaviour on each host.

- **Design:** No core file names a host. A sentence that depends on a host
  capability names the capability, and the runtime selects the branch. Each
  host is a declarative definition, with no host-specific code.
- **Metric:** Same case scores on each host tree.

### 19. Each skill does one thing, on an explicit command.

- **Design:** Cairn runs only by slash command. Each skill has one function. To
  record an answer, to change the goal, and to review the questions are 3
  different skills. A skill and its agent differ only in where the procedure
  runs: inline or isolated.
- **Metric:** Count of file changes outside the skill's declared paths (must
  be 0).

---

Claims 17 to 19 are about the plugin code, not a user project.
