---
name: modify-milestone-goal
description: Revise the Goal section of the current milestone's requirements.md when the objective itself needs to be reshaped, broadened, narrowed, or corrected.
---

# modify-milestone-goal

Replaces the `## Goal` of the current milestone's `requirements.md` with a revised goal statement and, in the same run, clears the standing picks on open questions that the revision undermines, keeping their alternatives. Everything else the change may have invalidated downstream is left as it stands, for the user and the next review pass. It is the only skill that edits the Goal of an *already-defined* milestone.

## Usage

```
/modify-milestone-goal <new or revised goal text>
```

- `<new or revised goal text>`: either a complete replacement goal statement, or a described change to fold into the existing one (e.g. "also cover a quick-reference section"). If it is a delta, integrate it against the current Goal rather than discarding what is still true.

**Example:**
```
/modify-milestone-goal Broaden the getting-started guide to walk a new user through their first week, not only their first session.
```

## Workflow

### 0. Find the current milestone

Follow `.agents/plugins/cairn/shared/get-current-milestone.md` to resolve `<MILESTONE_DIR>`. Never use a hardcoded path.

### 1. Read the current Goal

Read `<MILESTONE_DIR>/requirements.md` and locate the `## Goal` section. Show the user the current goal text so the change is reviewable against what it replaces.

### 2. Determine the revised Goal

From the argument, settle on the new Goal prose:

- If the argument is a full replacement, use it (lightly cleaned for clarity).
- If it is a delta ("also…", "drop…", "really about…"), integrate it with the existing Goal so the result is a single coherent statement, preserving the parts still true.

If the intended change is genuinely ambiguous, state the revised wording you propose and confirm it with the user before writing. The Goal is the root of the whole requirements tree — getting its wording right matters more than acting fast.

### 3. Analyse the impact (before editing)

Reason about what the new goal may have invalidated. Do **not** write this analysis into the document and do **not** edit those sections — it informs your own reasoning, and its one consequence in the files is the pick clearing of step 5:

- Which `## Decisions` entries the new goal contradicts, moots, or leaves dangling.
- Which open questions it newly settles, newly opens, or makes irrelevant — read `<MILESTONE_DIR>/open_questions.xml` whole with the file-reading tool for this, as you read `requirements.md` in step 1; that whole read is for reasoning only, and every locate, list, lift, and write is a call to the plugin's open-question tool, `python3 .agents/plugins/cairn/tools/open_questions.py <subcommand> <MILESTONE_DIR> …`. Never edit the file yourself.
- Which standing picks the revision undermines. A standing pick is the `<recommendation>` element an open question carries; it was formed under the goal being replaced. For each block carrying one, hold two texts from the read: the what-it-is text of the `<alternative>` its `<recommendation option="…">` names, and the one-line rationale that is the `<recommendation>` element's own text. Read them against the revised Goal and what it directly entails. The pick is **undermined** when either holds:
  - **The option can no longer be carried out.** The recommended alternative, as its what-it-is text reads, cannot be carried out alongside the revised Goal.
  - **The stated reason no longer holds.** The rationale states or plainly presupposes something the revision changed — a fact about the project, a constraint, the scope or aim of the milestone, a sibling's expected outcome — so the reason no longer holds as written, even though the option itself could still be carried out.

  Judge it in prose, from those two texts as they are written. Do not re-form the recommender's judgment: do not weigh the block's other alternatives, ask which option is now best, or decide whether the same option would be picked again for a different reason. **Doubt strips**: a pick only arguably untouched is named, because a cleared block keeps its alternatives and the next run of the recommendation pass re-picks over them, while a stale pick left standing is recorded as a decision. A pick whose option text and rationale text neither conflict with the revised Goal nor rest on anything the revision changed is not named — sharing a topic with the revision is not being undermined by it. Judge each block on its own two texts only: a block whose `<depends-on>` names an undermined block is not named on that account.
- Which `## Out of Scope` entries the new goal now pulls back in (or pushes out).
- If `TASKS_TODO.md` / `TASKS_DONE.md` already hold tasks, which derived or completed tasks the new goal strands, contradicts, or leaves unaddressed.

### 4. Edit the Goal

Replace the body of the `## Goal` section with the revised goal text. Touch nothing else in `requirements.md` — not `## Decisions`, not `## Out of Scope` — and not the task lists. A single targeted edit, not a rewrite of the file.

### 5. Clear the undermined picks

When step 3 named at least one undermined pick, clear them all with one call to the open-question tool, passing every named block's Short Title (its `id` as the document holds it), each as its own quoted argument:

```bash
python3 .agents/plugins/cairn/tools/open_questions.py strip --recommendation <MILESTONE_DIR> "<Short Title>" …
```

The call deletes each named block's `<recommendation>`, `<depends-on>`, and `<applied-principle>` children and keeps its `<alternative>` children, so the block stays a live question for the next `/recommend-all-open-questions` run to re-pick under the revised goal. It touches no other block: a block whose `<depends-on>` names a cleared block keeps its pick and its tag. Do not follow such tags and do not add those blocks to the call — the clearing is not transitive.

This is the only change the skill makes to `open_questions.xml`: no block is removed, added, or reworded, whatever step 3 found the revision to settle, open, or make irrelevant. When step 3 named no undermined pick, or the step-4 edit left the `## Goal` section as it was, make no call.

If the call exits non-zero, stop: print its `Error:` line verbatim, state that the Goal edit stands uncommitted in `requirements.md`, and do not commit.

### 6. Commit the goal revision

Read and follow the shared commit procedure at `.agents/plugins/cairn/shared/commit-procedure.md`, carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: `<MILESTONE_DIR>/requirements.md` (the file whose `## Goal` section it just revised) and `<MILESTONE_DIR>/open_questions.xml` (the document step 5 clears picks from), so a goal revision and the picks it cleared are one commit.
- **SUBJECT** — `Goal-revision: <milestone_id>`.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.

### 7. Confirm

On the success path — the commit in step 6 recorded the revised goal — print exactly one fixed terse status line and nothing else:

```
Goal revised.
```

Do not add the before → after goal text, the downstream-impact analysis from step 3, the picks step 5 cleared, the milestone id, or a next-step pointer. (The step-3 analysis still runs — it informs your own reasoning — but is not printed; the commit's diff is the record of the cleared picks.)

If instead the step-6 dirty-own-path guard fired (the `## Goal` section was unchanged, so nothing was committed), do not print the terse line — print a single concise line stating that nothing changed and briefly why, e.g. `No change — the revised goal matched the existing one; nothing committed.`
