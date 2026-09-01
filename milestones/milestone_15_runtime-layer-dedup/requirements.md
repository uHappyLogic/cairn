# Milestone 15: Runtime layer de-duplication

## Goal

De-duplicate Cairn's runtime layer (every `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md`) by removing three behavior-neutral classes of restatement: end-of-file `## Rules` sections that echo the workflow above them (retiring the `## Rules` heading across the layer and relocating each surviving unique rule into the step where it acts), editor-facing rationale that belongs in CLAUDE.md invariants (moved into the matching invariant first where not already present, then cut), and cross-file narration of counterparts' roles beyond the one sentence the contract needs. A sentence may be cut only if its content survives earlier in the same file, in a referenced shared procedure, or in a CLAUDE.md invariant; point-of-use constraints, worked examples, and templates rendered once stay. Target roughly 11,000 words removed from the 32,758-word layer, prioritizing the per-task, per-question, and per-pass hot files, verified by a per-file constraint-preservation check and a fresh-context re-audit, with the Antigravity tree regenerated.

## Relevant starting state

## Decisions

## Out of Scope

