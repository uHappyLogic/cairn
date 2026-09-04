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

### Description length

The 25-word figure is a hard pass/fail bar: every one of the 24 descriptions (21 `skills/*/SKILL.md`, 3 `agents/*.md`) must be 25 words or fewer, with no exceptions and no escape clause. A description that does not fit is reworded until it does. Because cairn is invoked only by explicit slash command, sibling-skill collision carries no runtime cost and is not grounds for overage; distinguishing a skill from its siblings is a wording problem to solve within the cap. The bar is mechanically verifiable by word count.

### Sentence shape

"A single short sentence" means one independent clause. Qualifying riders set off by commas, an em dash, or parentheses are allowed; the semicolon and the colon are banned outright, because those two marks introduce a second statement or an enumeration and are the route by which deleted mechanics and trigger lists would return under the word cap. The semicolon/colon ban is greppable and pass/fail; the permissive half is judged per description. Descriptions already written with em-dash or parenthetical apposition are not rewritten for punctuation alone.

### YAML plain scalar bar

Every one of the 24 rewritten descriptions must parse as a plain unquoted YAML scalar — no colon-space, no leading indicator character (quote, `#`, `[`, `{`, `&`, `*`, `%`, `@`), no trailing colon. The bar is defined as "the raw frontmatter loads under `yaml.safe_load` with the `description:` line left unquoted", not as a punctuation checklist, and is verified per file plus by a clean `uv run scripts/migrate_skills_to_agy.py`. A short plain declarative sentence satisfies it by default, and the one file that trips it today is being rewritten anyway, so the constraint is close to free while giving the milestone a machine-checkable acceptance criterion. The transpiler's re-quoting fallback stays in place as a net but is never exercised; no transpiler source is touched.

### Agent invocation contract

Each of the three `agents/*.md` descriptions keeps its invocation contract, compressed into the same single sentence as a short clause naming what the prompt carries — for example the task's heading text, or the question's Short Title — rather than left as a second dedicated sentence. That clause costs about five words, so all three agent descriptions still land under the 25-word cap, and it keeps the payload on the only agent-facing surface a dispatcher reads before the agent body loads. The separate "dispatched by X; not called directly by the user" note is provenance and is deleted.

## Out of Scope


## Open questions

<open-question id="CLAUDE.md invariant update" status="open">
  <question>Does this milestone amend the CLAUDE.md invariants — the &quot;Skill Frontmatter&quot; invariant and the milestone-15 sentence exempting frontmatter descriptions as &quot;the triggering surface, edited only to correct a claim the body has falsified&quot; — to record the one-sentence rule, or does the rule live only in the edited files?</question>
  <alternative id="Extend Skill Frontmatter invariant">
    Amend both bearing invariants: extend the existing Skill Frontmatter bullet so it carries the one-short-sentence description rule (what to name, what to delete, and that descriptions are routing labels rather than a record), and revise the milestone-15 sentence so it no longer claims descriptions are edited only to correct a falsified claim, pointing instead at the Skill Frontmatter bullet as the frontmatter rule&apos;s home.
    <advantage>Every rule about the frontmatter description key ends up in exactly one bullet, and the stale milestone-15 exemption — which would otherwise instruct a future editor to leave descriptions alone — is corrected in the same pass.</advantage>
    <drawback>The Skill Frontmatter bullet grows from a narrow schema requirement (name and description must exist) into a schema-plus-style rule, mixing a transpiler hard-fail constraint with an authoring convention.</drawback>
  </alternative>
  <alternative id="New standalone invariant">
    Add a new standalone invariant bullet for the description diet (its own cross-cutting authoring rule, in the style of the terse-reporting and no-editor-facing-prose bullets), leave the Skill Frontmatter schema bullet as-is, and revise the milestone-15 exemption sentence to defer to the new bullet.
    <advantage>Follows the established shape for cross-cutting authoring conventions, which each earn their own bullet, and keeps the transpiler-driven schema requirement cleanly separate from the style rule.</advantage>
    <drawback>Creates a second invariant bullet governing the same frontmatter key, so a later editor must read both to know the full contract — exactly the split-home duplication milestone 15 spent its effort removing.</drawback>
  </alternative>
  <alternative id="Correct the exemption only">
    Touch CLAUDE.md only to remove or narrow the milestone-15 exemption sentence, without stating the positive one-sentence rule anywhere; the rewritten descriptions themselves are the only expression of the standard.
    <advantage>Minimal CLAUDE.md churn while still eliminating the one sentence this milestone actually falsifies.</advantage>
    <drawback>Leaves no written rule for the next skill author, who must infer the standard by sampling 24 existing descriptions and will predictably regrow trigger lists and mechanics in the first new skill.</drawback>
  </alternative>
  <alternative id="No CLAUDE.md change">
    Leave both invariants untouched; the diet lives only in the edited skills/*/SKILL.md and agents/*.md files as an implicit example.
    <advantage>Zero risk of the invariants list drifting from what the files actually say, and the smallest possible milestone footprint.</advantage>
    <drawback>The milestone-15 sentence stays actively wrong — it would tell a future editor that descriptions are edited only to correct a falsified claim, contradicting a milestone that rewrote all 24 of them for length alone.</drawback>
  </alternative>
  <applied-principle>Mutate live machinery last</applied-principle>
  <recommendation option="Extend Skill Frontmatter invariant">The milestone-15 exemption sentence is falsified by this milestone and cannot be left standing, and folding the one-sentence rule into the existing Skill Frontmatter bullet gives the frontmatter surface a single invariant home rather than a second bullet about the same key.</recommendation>
</open-question>

<open-question id="Parallel doc surfaces scope" status="open">
  <question>Are README.md&apos;s per-skill reference entries and CLAUDE.md&apos;s workflow map left completely untouched, or must they be checked for claims the shortened descriptions falsify?</question>
  <alternative id="Leave untouched">
    Declare README.md&apos;s skill reference and CLAUDE.md&apos;s workflow map explicitly out of scope, on the grounds that shortening a routing label changes no behavior and neither surface quotes or characterizes frontmatter description text.
    <advantage>Cheapest and most honest about the change: the diet is behavior-neutral, so nothing either document asserts about what a skill does can go stale.</advantage>
    <drawback>Zero verification means a genuinely falsified claim would ship unnoticed, and it silently departs from the precedent milestone 15 set for exactly this situation.</drawback>
  </alternative>
  <alternative id="Falsification-only pass">
    Leave both surfaces untouched by default but run one bounded verification pass over them, editing only where a shortened description has made an existing claim demonstrably false, adding no new prose and doing no general tidying.
    <advantage>Reuses milestone 15&apos;s already-confirmed &quot;README sync scope&quot; rule verbatim, so the bound is precedent-tested and one sentence long, and it converts &quot;probably nothing went stale&quot; from an assumption into a checked result at near-zero cost.</advantage>
    <drawback>Very likely a no-op that still consumes a task slot, and an unbounded reader could drift into rewriting README prose that was never falsified.</drawback>
  </alternative>
  <alternative id="Sync both surfaces">
    Actively bring the parallel surfaces into line with the new descriptions — trimming or rewriting README entries and workflow-map lines that now say more than the description does, or documenting the one-sentence rule there.
    <advantage>Would leave a single uniform level of detail across every documentation surface.</advantage>
    <drawback>Inverts the milestone&apos;s own premise: README and CLAUDE.md are the deliberate homes for the mechanics, sequencing, and provenance being deleted from descriptions, so trimming them would destroy content with no other home, at a blast radius far outside the goal.</drawback>
  </alternative>
  <recommendation option="Falsification-only pass">Both surfaces document behavior and this milestone changes none, so the honest scope is not-touched-by-default plus one bounded falsification check — the exact rule milestone 15 already confirmed for a behavior-neutral sweep, costing one sentence to state and almost certainly resolving to a no-op.</recommendation>
</open-question>

<open-question id="Antigravity tree regeneration" status="open">
  <question>Is regenerating the checked-in Antigravity tree at .agents/plugins/cairn/ by re-running scripts/migrate_skills_to_agy.py part of this milestone&apos;s deliverable, or is it left for a later run?</question>
  <alternative id="Regenerate as final task">
    Make regeneration part of this milestone&apos;s deliverable as one closing task that re-runs scripts/migrate_skills_to_agy.py after every description rewrite has landed, committing the regenerated tree.
    <advantage>The checked-in tree never ships contradicting its source: it is in sync today, milestone 15 already established exactly this in-milestone regeneration task, and the run is a single deterministic command whose cost is near zero next to the milestone&apos;s own editing work — and it is what actually delivers the milestone&apos;s token savings to the Antigravity surface rather than only to Claude Code.</advantage>
    <drawback>Adds one task producing a large mechanical diff across 24+ generated files, and any later touch-up to a description silently re-staleing the tree unless the regeneration is genuinely last.</drawback>
  </alternative>
  <alternative id="Defer to a later run">
    Leave .agents/plugins/cairn/ untouched this milestone, edit only the source frontmatter, and record regeneration as follow-up work for a later run.
    <advantage>Keeps the milestone&apos;s committed diff purely about the 24 source descriptions, so the before/after word-count evidence reads cleanly with no generated noise mixed in.</advantage>
    <drawback>Ships a checked-in artifact that knowingly contradicts its source — Antigravity consumers keep loading the ~1411-word descriptions the milestone exists to remove — and it regresses a tree that is currently in sync, converting a solved condition into new debt with no forcing function to repay it.</drawback>
  </alternative>
  <alternative id="Regenerate per description task">
    Re-run the transpiler at the end of every description-editing task so each commit leaves source and generated tree self-consistent.
    <advantage>Every committed state is internally consistent, so no intermediate commit can be checked out with a stale tree.</advantage>
    <drawback>Buys nothing over a single closing run — the transpiler rmtree&apos;s and rewrites skills/, agents/, and shared/ wholesale on each invocation, so the end state is identical — while multiplying the mechanical generated-file diff across every commit in the milestone and burying the description changes the commits are supposed to show.</drawback>
  </alternative>
  <applied-principle>Mutate live machinery last</applied-principle>
  <recommendation option="Regenerate as final task">Regeneration is in scope: the tree is checked into git and currently in sync, so skipping it is an active regression, and milestone 15 already proved a single closing transpiler task is the cheap, correct shape — one run at the end rather than per task, because the transpiler rewrites the whole tree every time and the generated copy is never the machinery executing this milestone, so no in-flight breakage can occur mid-run.</recommendation>
</open-question>
