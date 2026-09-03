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


## Open questions

<open-question id="Word cap enforcement" status="open">
  <question>Is the 25-word figure a hard pass/fail bar that every one of the 24 descriptions must meet, or a target a description may exceed when a shorter wording would stop distinguishing it from a sibling skill?</question>
  <alternative id="Hard cap">
    Treat 25 words as a pass/fail bar every one of the 24 descriptions must meet, with no exceptions and no escape clause; a description that cannot fit is reworded until it does.
    <advantage>It is mechanically verifiable — a task can assert &quot;all 24 descriptions are 25 words or fewer&quot; and a completer can check it with a word count, so the six heaviest descriptions (149–105 words) cannot negotiate their way to a partial trim, which is the exact failure mode the milestone Goal singles out.</advantage>
    <drawback>A few descriptions in tight sibling clusters (the four answer-open-question* skills, complete-task skill vs. agent, recommend-all-open-questions vs. the recommend-open-question agent) must carry their distinguishing trait in very compressed wording, and one or two may read tersely as a result.</drawback>
  </alternative>
  <alternative id="Target with sibling exception">
    Treat 25 words as a target a description may exceed when a shorter wording would stop distinguishing it from a sibling skill, with the author judging each case.
    <advantage>It preserves distinguishability wherever a cluster is genuinely tight, and matches the Goal&apos;s own literal wording (&quot;target: 25 words or fewer&quot;) without reinterpreting it.</advantage>
    <drawback>The exception is self-judged and unbounded — there is no ceiling on the overage and no test a reviewer can apply — and the descriptions most likely to claim it are precisely the six heavy ones carrying 57% of the word budget, so the milestone&apos;s central cut becomes a per-description negotiation.</drawback>
  </alternative>
  <alternative id="Bounded overage ceiling">
    Keep 25 words as the default hard bar but allow a named, hard ceiling (e.g. 35 words) for a description that states a specific sibling-collision reason.
    <advantage>It bounds the escape hatch, so the total always-on budget stays predictable while a genuinely cramped description gets room.</advantage>
    <drawback>It carries two numbers and a per-description justification step, reopening the &quot;does this one qualify?&quot; argument the flat bar exists to end, for a saving measured in a handful of words across at most two or three files.</drawback>
  </alternative>
  <alternative id="Sentence bar only">
    Enforce &quot;a single sentence naming what the skill does&quot; as the real bar and demote 25 words to a non-binding guide.
    <advantage>It enforces the Goal&apos;s actual stated shape rather than a proxy for it, and never forces an awkward truncation.</advantage>
    <drawback>A single sentence can still run 60+ words, so it does not bound the always-on token cost that motivates the milestone at all — and it leaves the word figure in the Goal with no operative meaning.</drawback>
  </alternative>
  <applied-principle>Name by distinctive function</applied-principle>
  <recommendation option="Hard cap">Descriptions here never route anything — cairn is invoked only by explicit slash command, as the Goal and the starting state both record — so sibling collision carries no runtime cost, while a flat pass/fail bar is the only form of the rule the six heaviest descriptions cannot argue their way past; distinctiveness is a wording problem, not a length problem, and every cluster&apos;s separating trait fits inside 25 words.</recommendation>
</open-question>

<open-question id="Sentence shape bar" status="open">
  <question>Beyond word count, what structural constraints does &quot;a single short sentence&quot; impose — is an em-dash or colon continuation clause, a semicolon, or a parenthetical allowed inside the one sentence, or must it be a single plain clause?</question>
  <alternative id="Terminal period only">
    Define &quot;a single short sentence&quot; as exactly one sentence-terminating period and nothing more, leaving all internal punctuation (em-dash, colon, semicolon, parenthetical) unconstrained and letting the word cap plus the Goal&apos;s four content deletions do the whole job.
    <advantage>Adds no rule that is not already load-bearing — the mechanics, provenance, trigger-list and cross-reference bans already forbid the material a tail clause would carry — so the 24 rewrites stay focused on cutting content rather than policing style, and descriptions that already meet the intent (define-milestone-goal&apos;s parenthetical, finish-current-milestone&apos;s em-dash) pass untouched.</advantage>
    <drawback>An em-dash or semicolon tail is precisely how deleted mechanics creep back in under the cap, and this bar offers no independent check against it — a reviewer has only the content ban, which is a judgment call, where a punctuation bar would have been a grep.</drawback>
  </alternative>
  <alternative id="Single plain clause">
    Require one independent clause with no em-dash, colon, semicolon, or parenthetical at all — commas permitted only to separate list items — so every description is a bare subject-verb-object statement.
    <advantage>Maximally mechanical and pass/fail checkable across all 24 files (a single grep for the banned marks), and it structurally forecloses the tail-clause route by which cut mechanics would return.</advantage>
    <drawback>Over-constrains for no token payoff: it forces punctuation-only rewrites of descriptions that already satisfy the milestone&apos;s intent, removes the cheapest way to distinguish near-sibling skills (define- vs modify-milestone-goal, the three answer-open-question variants), and bans em-dash apposition, which is the established voice of every prose surface in this repo.</drawback>
  </alternative>
  <alternative id="One statement, riders allowed">
    Require one independent clause that may carry qualifying riders set off by commas, an em-dash, or parentheses, while banning the semicolon and the colon outright — the two marks whose job is to introduce a second statement or an enumeration, and the ones that would reopen the door to a mechanics or trigger-list tail.
    <advantage>Puts a greppable, unambiguous ban exactly where the smuggling risk is (semicolon and colon), while staying permissive about the em-dash apposition the project already writes in, so no already-conforming description is rewritten for style alone; the colon ban has a second, independent mechanical payoff on the YAML surface, which its own open question can settle without contradicting this bar.</advantage>
    <drawback>The permissive half is a judgment call rather than a test — how long a rider may run, and whether an em-dash tail is a qualifier or a second statement in disguise, still has to be adjudicated per file, so near-miss cases are argued rather than checked.</drawback>
  </alternative>
  <recommendation option="One statement, riders allowed">It is mechanical exactly where enforcement pays (a grep-checkable ban on the two sentence-joining marks that would let cut mechanics back in) and permissive exactly where the repo&apos;s own voice already lives (em-dash and parenthetical apposition), so the bar constrains content creep without generating punctuation-only churn in the descriptions that already meet the intent.</recommendation>
</open-question>

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

<open-question id="YAML plain scalar requirement" status="open">
  <question>Must every rewritten description parse as a plain unquoted YAML scalar — no colon-space, no leading quote character — so the transpiler&apos;s re-quoting fallback stops being exercised, or is staying within that fallback acceptable?</question>
  <alternative id="Hard plain-scalar bar">
    Every one of the 24 rewritten descriptions must parse as a plain unquoted YAML scalar — no colon-space, no leading indicator character (quote, #, [, {, &amp;, *, %, @), no trailing colon — verified by loading each file&apos;s raw frontmatter with yaml.safe_load and by a clean uv run scripts/migrate_skills_to_agy.py, leaving the transpiler&apos;s re-quoting fallback present but never exercised.
    <advantage>The constraint is close to free — a 25-word plain declarative sentence satisfies it by default, and the single file that trips it today is being rewritten anyway — while converting an otherwise unverifiable prose goal into a deterministic one-command pass/fail gate that also covers the three agents/*.md files the transpiler never parses at all.</advantage>
    <drawback>&quot;No colon-space, no leading quote&quot; is an incomplete statement of YAML plain-scalar rules, so the bar has to be defined as &quot;parses under yaml.safe_load with the line unquoted&quot; rather than as that two-item checklist, and it forecloses a few natural phrasings (any X: Y construction in a description).</drawback>
  </alternative>
  <alternative id="Fallback acceptable">
    Rewrite descriptions for brevity only and impose no YAML constraint, letting the transpiler&apos;s existing re-quoting fallback absorb any description that still fails to parse plainly.
    <advantage>Keeps the milestone purely a prose diet with zero added mechanics, and the fallback demonstrably works today on the one file that needs it.</advantage>
    <drawback>Leaves a fragile safety net load-bearing — the fallback only matches a single-line description: prefix and naively escapes quotes without handling backslashes — and forfeits a free verification gate on a milestone that otherwise has almost no objective acceptance criteria, since the sole offending description is being rewritten regardless.</drawback>
  </alternative>
  <alternative id="Quote every description">
    Require each rewritten description to be wrapped in explicit double quotes, making it parse regardless of punctuation.
    <advantage>Uniformly parse-safe with no need to reason about plain-scalar indicator rules at all, and the fallback skips already-quoted lines by construction.</advantage>
    <drawback>Breaks the existing house style — all 24 descriptions are unquoted today — and forces backslash-escaping in the several descriptions that legitimately contain a double quote, adding exactly the kind of mechanical noise this milestone is trying to remove.</drawback>
  </alternative>
  <alternative id="Bar plus fallback removal">
    Impose the plain-scalar bar and additionally delete the re-quoting branch from scripts/migrate_skills_to_agy.py, so a non-plain description hard-fails the transpiler.
    <advantage>Enforcement by construction — the rule can never silently regress, because the build breaks the moment a future description violates it.</advantage>
    <drawback>Expands the milestone from frontmatter prose into transpiler source, which the Goal does not cover, and removes a tolerance net that a consuming project or fork may still rely on.</drawback>
  </alternative>
  <recommendation option="Hard plain-scalar bar">Require it: a short plain sentence already satisfies the bar, the one violating file is being rewritten anyway, and it buys the milestone a real machine-checkable acceptance criterion — while leaving the fallback in place as a net rather than dragging transpiler surgery into a prose diet.</recommendation>
</open-question>

<open-question id="Agent invocation contract retention" status="open">
  <question>When an agent description compresses to one sentence, must it still name the expected prompt payload (for example complete-task&apos;s &quot;##&quot; heading text), or is the payload contract dropped because the dispatching orchestrator already specifies it?</question>
  <alternative id="Compress into the sentence">
    Keep the payload contract but fold it into the single sentence as a short clause naming what the prompt carries (for example &quot;…given the task&apos;s heading text&quot; or &quot;…for the question named by its Short Title&quot;), while deleting the separate &quot;Dispatched by X; not called directly by the user&quot; note as the provenance this milestone targets.
    <advantage>It is what the Goal already states agent descriptions must do (&quot;Agent descriptions compress their invocation contract into that same one sentence&quot;), it costs about five words so all three agents still land well under 25, and it keeps the payload on the only agent-facing surface a dispatcher sees before it forms a prompt — the agent body&apos;s Input section is not loaded until after dispatch.</advantage>
    <drawback>It adds a second clause to every agent sentence, which pushes the three agent descriptions toward whatever multi-clause shape the sibling Sentence shape bar question settles, and it spends words on a contract that all three current orchestrators already hard-code in their dispatch templates.</drawback>
  </alternative>
  <alternative id="Drop the contract">
    Cut the payload contract entirely, leaving each agent description as a bare what-it-does sentence, on the grounds that the dispatching orchestrator&apos;s SKILL.md already specifies the exact prompt and the agent body restates the input.
    <advantage>It is the shortest result and the redundancy is real — complete-all-tasks, recommend-all-open-questions, and answer-all-open-questions-with-recommendation each embed a literal prompt template, so no live dispatch path reads the payload out of the description.</advantage>
    <drawback>It contradicts the milestone Goal&apos;s explicit sentence about agent descriptions, so adopting it would require a goal revision first; and it leaves the routing surface silent about the payload for any dispatch that is not one of the three templated ones — a hand-dispatch, a future orchestrator, or a maintainer reading the agent list.</drawback>
  </alternative>
  <alternative id="Exempt agents from one sentence">
    Let the three agent descriptions keep a second, dedicated contract sentence (the current &quot;Invoke with … as the prompt.&quot; form), exempting agents from the one-sentence rule the 21 skills follow.
    <advantage>Nothing is lost or reworded, and the contract stays a distinct, greppable statement rather than a subordinate clause.</advantage>
    <drawback>It carves an exception into the milestone&apos;s central rule for 3 of 24 files, and the live evidence is against it: a trailing contract sentence is exactly what gets clipped — in this session&apos;s own agent listing complete-task renders as &quot;Invoke with the task&apos;s&quot; with the payload cut off, whereas a clause inside the main sentence sits early enough to survive.</drawback>
  </alternative>
  <recommendation option="Compress into the sentence">Keep it, folded into the one sentence: the Goal already mandates compressing the invocation contract rather than dropping it, the payload name costs about five words, and the description is the only agent-facing surface a dispatcher reads before the agent body loads — while the &quot;dispatched by X; not called directly&quot; note is provenance and goes.</recommendation>
</open-question>
