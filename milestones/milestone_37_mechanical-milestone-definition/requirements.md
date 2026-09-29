# Milestone 37: Mechanical milestone definition

## Goal

Make /define-milestone-goal fully mechanical. A new stdlib-only Python tool, core/tools/define_milestone.py, takes the title as --title and the goal text on stdin. It works out the milestone number and slug (kebab-case, first 5 words of the title), checks for conflicts, creates open_questions.xml through the open-question tool's code and writes the three Markdown files. It prints the commit subject and the four file paths ready to hand to the commit procedure. On failure it prints one Error: line and leaves nothing behind. The model's only work in the skill is choosing the title, passing the tool's output to the commit procedure and reporting the result.

## Relevant starting state

## Decisions

## Out of Scope

