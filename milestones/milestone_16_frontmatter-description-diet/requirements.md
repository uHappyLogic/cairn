# Milestone 16: Frontmatter Description Diet

## Goal

Cut every `description` in the plugin's frontmatter — all 21 `skills/*/SKILL.md` and all 3 `agents/*.md` — down to a single short sentence (target: 25 words or fewer) naming only what that skill or agent does. Delete design provenance, mechanics, sequencing, cross-skill references, "Use when…" framing, and trigger-phrase lists outright. Agent descriptions compress their invocation contract into that same one sentence. Descriptions are treated as routing labels, never as a record: cut content is deleted without any obligation to preserve it elsewhere, since cairn is invoked only by explicit slash command and is never auto-discovered. The six heaviest descriptions (review-milestone-requirements 150 words, discuss-new-task 144, capture-milestone-principle-updates 129, recommend-all-open-questions 123, answer-all-open-questions-with-recommendation 113, modify-milestone-goal 106) carry 57% of the framework's ~1341 always-on description words and must be restructured rather than lightly trimmed.

## Relevant starting state

### Frontmatter description inventory

The plugin has 21 `skills/<name>/SKILL.md` files and 3 `agents/<name>.md` files, each carrying a YAML frontmatter `description`. Together they total ~1411 words, all of it always-on context. The distribution is heavily skewed: six descriptions account for 759 words (54%) — `review-milestone-requirements` 149, `discuss-new-task` 143, `capture-milestone-principle-updates` 128, `recommend-all-open-questions` 122, `answer-all-open-questions-with-recommendation` 112, `modify-milestone-goal` 105. The remaining 18 average 36 words, with a long tail of mid-weight ones (`recommend-open-question` agent 76, `answer-open-question-with-alternative` 75, `answer-open-question-with-recommendation` 62, `submit-task` 52, `answer-open-question-with-recommendation` agent 45). The shortest already meet a one-sentence shape (`complete-all-tasks` 16, `ask-in-milestone-context` 18, `define-milestone-goal` 18).

### Content currently carried in descriptions

The heavy descriptions carry four kinds of material beyond a what-it-does statement: **trigger-phrase lists** (`recommend-all-open-questions`, `answer-all-open-questions-with-recommendation`, `capture-milestone-principle-updates`, and `review-milestone-requirements` each enumerate 5 quoted user phrasings); **mechanics** (commit subjects, strict sequencing, dispatch counts, clean-tree preconditions, "commits once at the end of the run"); **design provenance** ("It is the new sole writer of milestones/answer_decision_principles.md", "This is the only skill that mutates an existing milestone's Goal"); and **cross-skill references** (`/review-milestone-requirements`, `/submit-task`, `/derive-tasks`, `/finish-current-milestone` named inside other skills' descriptions). Several are framed as "Use when the user says things like…" rather than as a statement of what the skill does. The three agent descriptions additionally carry an invocation contract naming the expected prompt payload — e.g. `complete-task`: "Invoke with the task's `##` heading text as the prompt" — plus a "dispatched by X; not called directly by the user" note.

### Frontmatter schema and its consumers

Frontmatter keys in use are `name` and `description` everywhere, plus optional `model: opus` (3 skills, 3 agents) and `color` (agents only). `scripts/migrate_skills_to_agy.py` is the one programmatic consumer: it hard-fails with a non-zero exit if a `SKILL.md` lacks frontmatter or is missing `name` or `description`, and it carries a fallback path that re-quotes an unquoted `description:` line when `yaml.safe_load` raises. That fallback is live today — `skills/review-milestone-requirements/SKILL.md` is the one file whose frontmatter does not parse as plain YAML, because its description contains `loop: ` (a colon-space inside an unquoted scalar). The generated Antigravity tree already exists at `.agents/plugins/cairn/`, so any description edit needs a re-run of the transpiler to propagate.

### How cairn is actually invoked

Every skill is invoked by explicit slash command. The project's own working notes (`.scratchpad.md`) drive the whole pipeline as literal one-shot CLI calls — `claude -p "/cairn:review-milestone-requirements" --plugin-dir …`, and the `agy -p "/cairn:…"` equivalents — with the skill named in full. Nothing in the repo relies on description-based matching to select a skill.

### Parallel documentation surfaces

`README.md` carries a `## Skill reference` section with one `###` entry per skill and agent (about 30 entries, several of them multi-paragraph), documenting mechanics, commit subjects, sequencing, and rationale far more fully than any description. `CLAUDE.md` carries the same material again as the invariants list plus a per-skill workflow map. Both are separate from the always-on description surface — neither is loaded to route a skill.

### CLAUDE.md constraints on this layer

Two invariants bear directly on this milestone. The **Skill Frontmatter** invariant requires every `SKILL.md` to carry `name` and `description`, citing the transpiler's hard error. The **runtime files carry no editor-facing prose** invariant (milestone 15) strips rationale from `skills/*/SKILL.md`, `agents/*.md`, and `shared/*.md` bodies, but explicitly exempts frontmatter: "YAML frontmatter `description` fields are outside this rule — they are the triggering surface, edited only to correct a claim the body has falsified." That exemption is why the descriptions still hold provenance and mechanics the bodies no longer do.

## Decisions

## Out of Scope

