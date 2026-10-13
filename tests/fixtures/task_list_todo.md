# TASKS TODO

## Build The Parser First

Write the parser that reads the whole file into its heading and sections, so every later write renders from one model. Verified by its round trip on the golden files.

---

## Keep A Body Separator Line

A body may hold a separator line of its own that is not the section's end.

---

The line above stays body text, because the next non-blank line is this prose rather than a heading.

---

## Render Unicode — Text As Given

Carry `code`, ${VAR}, $(cmd), &amp; entities, and "quotes" through untouched, including non-ASCII text like zażółć gęślą jaźń.

---
