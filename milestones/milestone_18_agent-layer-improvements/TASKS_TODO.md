# TASKS TODO

## Remove Pinned Model From Agent Frontmatter

Delete the `model: opus` frontmatter line from each of the three files under `agents/` (`complete-task.md`, `recommend-open-question.md`, `answer-open-question-with-recommendation.md`) so a dispatched agent inherits the session's model instead of forcing Opus, leaving `name`, `description`, and `color` untouched. Verified when none of the three source agent files carries a `model` key and the regenerated `.agents/plugins/cairn/agents/` tree is byte-identical to the source.

---
## Remove Pinned Model From Skill Frontmatter

Delete the `model: opus` frontmatter line from the two skills that still carry it, `skills/answer-open-question-with-recommendation/SKILL.md` and `skills/answer-open-question-with-alternative/SKILL.md`, leaving `name` and `description` untouched, so that together with the agent task before it nothing in the plugin pins a model. Verified when a grep for a `model:` frontmatter line across `skills/` and `agents/` finds nothing and the regenerated `.agents/plugins/cairn/` tree is byte-identical to the source.

---
## Grayscale-Distinguishable Agent Colors

Replace the `color:` values in the three files under `agents/` (currently `green`, `green`, `teal`) with three colors from Claude Code's supported named agent palette chosen for maximally separated luminance (one light, one mid, one dark, such as `yellow`, `red`, and `blue`), so that no two agents share a value and all three stay tellable apart on a display viewed through a grayscale filter. Verified when the three source files carry three distinct colors whose grayscale renderings are visibly different from each other and the regenerated `.agents/plugins/cairn/agents/` tree is byte-identical to the source.

---
## Recommend Sweep Failure Return And Shape Check

Give `agents/recommend-open-question.md` a failure return whose final line is `FAILED: <reason>` while keeping its success return as the bare XML sub-elements with no `DONE` line, and make `skills/recommend-all-open-questions/SKILL.md` check each return before embedding — it must start with `<alternative` and end with `</recommendation>` — treating a `FAILED:` return or any return failing that shape as a per-question skip rather than a run stop: the block is left untouched, the surviving returns are embedded and committed as today, and the skipped Short Titles with their reasons are printed as a git-absent advisory alongside the terse status line. This closes the one asymmetry in the agent layer's return contracts, where a prose, partial, or explanatory subagent reply is currently spliced into `requirements.md` as XML. Verified by reading both files and confirming that a malformed or `FAILED:` return can no longer reach the whole-block-replacement Edit.

---
