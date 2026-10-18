# Milestone 9: Golden requirements fixture

## Goal

Fold one decision at a time into the section below, changing no byte the fold did not write.

## Relevant starting state

### Prose decision

A subsection outside `## Decisions` that shares a decision's heading is never a landing point.

## Decisions

### Prose decision

The first decision is one prose paragraph under its own subsection.

It carries a second paragraph, so a fold lands after this one.

### Topical bullets

- **First lead.** A bullet decision under a topical subsection.
- **Second lead.** A bullet whose text wraps
  onto an indented continuation line.

### Render Unicode — Text As Given

Carry `code`, ${VAR}, $(cmd), &amp; entities, and "quotes" through untouched, including zażółć gęślą jaźń.

## Out of Scope

- Anything the fold did not write.
