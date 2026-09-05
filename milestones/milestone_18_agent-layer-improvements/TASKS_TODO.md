# TASKS TODO

## Remove Pinned Model From Agent Frontmatter

Delete the `model: opus` frontmatter line from each of the three files under `agents/` (`complete-task.md`, `recommend-open-question.md`, `answer-open-question-with-recommendation.md`) so a dispatched agent inherits the session's model instead of forcing Opus, leaving `name`, `description`, and `color` untouched. Verified when none of the three source agent files carries a `model` key and the regenerated `.agents/plugins/cairn/agents/` tree is byte-identical to the source.

---
## Grayscale-Distinguishable Agent Colors

Replace the `color:` values in the three files under `agents/` (currently `green`, `green`, `teal`) with three colors from Claude Code's supported named agent palette chosen for maximally separated luminance (one light, one mid, one dark, such as `yellow`, `red`, and `blue`), so that no two agents share a value and all three stay tellable apart on a display viewed through a grayscale filter. Verified when the three source files carry three distinct colors whose grayscale renderings are visibly different from each other and the regenerated `.agents/plugins/cairn/agents/` tree is byte-identical to the source.

---
