---
name: answer-open-question
description: Answer a named open question in the current milestone requirements document, updating the document to reflect the decision and its downstream implications.
---

# answer-open-question

Resolves a named open question or deferred entry in the current milestone's `requirements.md` by recording the user's answer and propagating its implications through the document.

## Usage

```
/answer-open-question <Short Title>. <answer text>
```

The `<Short Title>` must match (case-insensitive) the title of an existing `Open question` or `Deferred` entry. The `.` character is the separator. Everything after the first `.` is the answer.

**Example:**
```
/answer-open-question Arc drive technique. Use approach B — two Cinemachine virtual cameras per rail axis, blended by Cinemachine's built-in blend system. RailCameraSnapper will activate the appropriate virtual camera on rail switch rather than calling ForceCameraPosition.
```

## Workflow

### 0. Find the current milestone

Read `CLAUDE.md` and extract the path from the `## Current Milestone` section (shown in backticks, e.g. `milestones/milestone_11_tbd/`). Use this as `<MILESTONE_DIR>` throughout this workflow.

### 1. Parse the input

Split the skill args on the first `.` character:
- Before: the question title (trim whitespace)
- After: the answer text (trim whitespace)

If no `.` is found, report a parse error and show the expected format.

### 2. Locate the question

Read `<MILESTONE_DIR>/requirements.md`. Find the `Open question` or `Deferred` entry whose title matches the parsed title (case-insensitive). If no match is found, report the error and list all available titles.

### 3. Analyse the answer

Before editing, reason about:
- Does the answer resolve the question completely, or does it leave a sub-question open?
- Does it introduce a concrete implementation constraint that belongs in the **Requirements** section?
- Does it make any other open question moot, or force a specific answer to one?
- Does it contradict or supersede anything already written in the document?

### 4. Update the document

Make changes in separate, targeted edits — one per logical change (removal, requirements update, cascade). This is safer than a single large replacement on a long document:

**a. Remove the matched block** from the document entirely.

**b. Update the Requirements section** if the answer introduces a decision that meaningfully constrains implementation. Add a concise requirement statement under the relevant subsection (or create a new one if needed).

**c. Cascade to other open questions** if the answer makes another entry moot or implies its answer. Remove each affected entry and, if the implied answer introduces a constraint, fold it into the Requirements section with a brief note.

### 5. Report findings

After editing, briefly state:
- Which question was resolved and how the document changed (resolved block, requirements updates, cascading resolutions)
- Any new open questions the answer may have introduced — surface these but do **not** add them to the document without user confirmation

## Rules

- Title matching is case-insensitive.
- Do not rewrite or restructure existing content — only remove the answered entry and add or amend requirement statements.
- Do not invent implications not directly supported by the answer text.
- If the answer is ambiguous or incomplete, remove what is clearly resolved and ask the user before adding any new open question.
