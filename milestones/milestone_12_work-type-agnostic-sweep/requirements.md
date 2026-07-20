# Milestone 12: Work-Type-Agnostic Sweep

## Goal

Complete Cairn's transformation into a fully work-type-agnostic workflow by removing every remaining assumption that the work is software engineering — finishing what the Generic Naming Refactor (milestone 3) began. Sweep all behavior files (skills/, agents/, shared/) plus the plugin's own README.md and CLAUDE.md, neutralizing three layers: (1) language — the "You are a Software Engineer" personas, "the code/codebase," "insertion points," "assertions," "exports," and the "tech stack, build/test commands, MCP tools" environment-context wording; (2) the verification mechanism — reframe "build & test / run the verification command" so a task is verified against its Success criteria however the project defines done, deferring to project conventions rather than assuming a build; and (3) examples — replace all software/Unity illustrations (the Creep tower-defense worked example, RailCameraSnapper, "Arc drive technique") with work-type-neutral ones. Stay domain-silent — add no "declare your work type" machinery, since a well-maintained project's CLAUDE.md already supplies domain context. migrate-workspace's references to Cairn's own retired vocabulary stay out of scope (they describe the plugin's history, not the user's work type). Success is proven by a final independent re-audit of the whole plugin returning zero software-engineer-specific findings.

## Relevant starting state

The "project" this milestone changes is the Cairn plugin itself (self-dogfooding): the deliverables are the plugin's own Markdown files under `skills/`, `agents/`, `shared/`, plus root `README.md` and `CLAUDE.md`. There is no build system, no tests, no code — everything is plain Markdown. An audit run at the start of this milestone found software-engineer assumptions in ~16 files across four layers, described below (line references are indicative, not pinned).

### The two shared task cores (deepest SE concentration)

`shared/complete-procedure.md` and `shared/submit-procedure.md` are the single-source-of-truth procedures that drive all task authoring and completion (run inline by the `submit-task`/`complete-task` skills and in isolation by their agents, and by `derive-tasks`). They are the most SE-saturated files: `complete-procedure.md` speaks of "insertion points," "assertion wording," "the live codebase," "source files," "exports," "build/test commands," and "post-edit verification steps"; `submit-procedure.md` frames the deliverable as code ("write the code organically," "read from the code," "the public API"), documents its environment read as "tech stack, MCP tools, build/test commands," and carries a worked Unity tower-defense example (`Creep`, `RegisterWaveStart()`, `AllCreepsDead()`) plus success-criterion models like "Build command exits with code 0" and "Function Z is exported from W." These two files also encode the **verification mechanism** the goal wants reframed — "run the verification command / build & test" — not just vocabulary.

### Agent personas

`agents/submit-task.md` and `agents/complete-task.md` each open with "You are a **Software Engineer** …" (the two cases the user originally spotted). These are one-line persona statements, the shallowest layer.

### "The code / the codebase" framing skills

Several skills treat the deliverable as code and the project as a codebase throughout: `skills/ask-in-milestone-context/SKILL.md` (grounds finished-work answers in "the code those tasks shipped," "the truth is in the code," "live source"), `skills/specify-milestone-starting-state/SKILL.md` (this very skill — "Analyze the current codebase," "meaningful code," "exported functions/classes/types/interfaces," "schemas, database models"), and `skills/derive-tasks/SKILL.md` ("technology boundary or layer … backend API / frontend component / DB schema; or for Unity: scripts / prefabs / scene hierarchy," "existing code," "module, schema, or shared utility"). `agents/recommend-open-question.md`, `shared/recommend-procedure.md`, `skills/discuss-open-question/SKILL.md`, `skills/discuss-new-task/SKILL.md`, and `skills/recommend-all-open-questions/SKILL.md` carry lighter "live code / source files / bug / during development / build X" phrasing.

### Environment-context reading pattern

A recurring instruction to read the project's environment from `CLAUDE.md` as "**tech stack, build/test commands, MCP tools, conventions**" appears in `shared/complete-procedure.md`, `shared/submit-procedure.md`, `skills/derive-tasks/SKILL.md`, `skills/specify-milestone-starting-state/SKILL.md`, `skills/init-milestone-base-workflow/SKILL.md`, `skills/discuss-milestone-goal/SKILL.md`, and `skills/finish-current-milestone/SKILL.md` (the last also updates `CLAUDE.md` only for "tech-stack or structural changes," referencing `## Tech Stack` / `## Repository Layout` and "game/codebase"). A `CLAUDE.md` invariant documents this pattern explicitly as the environment-context contract those readers follow.

### Work-type-specific examples

Beyond the `submit-procedure.md` Unity example, illustrative content assumes software/game work in `skills/answer-open-question/SKILL.md` and `skills/discuss-open-question/SKILL.md` (Cinemachine virtual cameras, `RailCameraSnapper`, `ForceCameraPosition`; recurring example question titles "Arc drive technique" and "Player input during swing") and `skills/review-milestone-requirements/SKILL.md` (same game-mechanics example titles). The goal is to replace all such examples with work-type-neutral ones.

### The plugin's own docs

`README.md` (the public, adoption-focused landing page) and `CLAUDE.md` (the invariants Claude itself acts on) both carry SE framing — `CLAUDE.md`'s invariants restate the "tech stack, build/test commands, MCP tools" environment contract and describe skills in code terms; `README.md` pitches the workflow and diagrams to adopters. Both are in scope this milestone. `CLAUDE.md` also carries the full invariant set that any language/mechanism change here must be reconciled against.

### Prior art and the out-of-scope boundary

Milestone 3 ("Generic Naming Refactor") already retired coding-flavored *vocabulary* (implement→complete, backlog drop, heading renames) in a clean break — this milestone finishes the job it started, extending to personas, the verification mechanism, examples, and the docs. `skills/migrate-workspace/SKILL.md` references "implementation state/decisions" and the plugin's own past "refactors," but those describe Cairn's *own* retired artifact vocabulary (migration history), not an assumption about the user's work type, and are out of scope by the goal's explicit exclusion.

## Decisions

## Out of Scope

## Open questions

<open-question id="Replacement example strategy" status="open">
  <question>Which replacement strategy should the neutralized examples use: one canonical work-type-neutral worked example reused consistently across all files (replacing the Creep tower-defense example, RailCameraSnapper, and the recurring Arc-drive/swing question titles), a varied set of examples drawn from different non-software domains, or fully abstract placeholders — and may a rewritten example name a concrete domain (e.g. cooking, event planning) at all, or does that conflict with the goal&apos;s domain-silent stance?</question>
  <alternative id="Canonical neutral example">
    A single work-type-neutral worked example that is concrete but domain-generic (a task producing, say, a document or deliverable with a checkable Success bar), reused consistently everywhere the Creep example, RailCameraSnapper, and the Arc-drive/swing titles appear; concrete illustration is kept, but no specific industry is named.
    <advantage>Maximizes consistency and auditability — one example a reader learns once, one artifact to maintain and to prove domain-silent, and it retains the concreteness a worked example needs to actually teach.</advantage>
    <drawback>A single reused illustration can feel slightly generic in every context, and picking a good domain-generic yet concrete scenario takes more care than grabbing a real domain.</drawback>
  </alternative>
  <alternative id="Varied concrete domains">
    A varied set of examples drawn from several named non-software domains (cooking, event planning, writing), each site illustrated with whichever concrete domain fits best.
    <advantage>Concrete named domains read vividly and actively demonstrate the tool&apos;s range by showing it working across genuinely different fields.</advantage>
    <drawback>Naming concrete industries reintroduces exactly the domain-specific connotation the goal&apos;s domain-silent stance and the re-audit exist to remove — it swaps one assumed work type for several — and multiplies the surface a &quot;zero findings&quot; audit must clear.</drawback>
  </alternative>
  <alternative id="Abstract placeholders">
    Fully abstract structural placeholders throughout (Task A, Component X, &quot;the deliverable meets criterion Z&quot;), naming no domain and no concrete scenario.
    <advantage>Maximally domain-silent with zero risk of the re-audit flagging domain-specific content, and nothing to maintain.</advantage>
    <drawback>Placeholders gut the pedagogical purpose of a worked example — the Creep illustration exists to show a filled-in task concretely, and &quot;Task A provides X&quot; teaches far less than a real, if generic, illustration.</drawback>
  </alternative>
  <applied-principle>Prefer domain-neutral terms</applied-principle>
  <recommendation option="Canonical neutral example">One concrete-but-domain-generic worked example reused everywhere keeps the consistency and teaching value a placeholder set loses, while the domain-neutral principle tips decisively against naming any concrete industry — so examples may stay concrete but must not name a specific domain.</recommendation>
</open-question>

<open-question id="SE-assumption audit boundary" status="open">
  <question>What counts as a software-engineer-specific finding for the sweep and the final re-audit — in particular, are Cairn&apos;s own operating mechanics (git commits and git-log greps, path-scoped staging, the CLAUDE.md and README.md file names, the consuming project being a git repository) exempt plugin infrastructure or findings to neutralize? Without a decided boundary the &quot;zero findings&quot; success bar is unmeasurable.</question>
  <alternative id="Exempt infrastructure by user-work test">
    Define an SE-specific finding as any text that assumes the user&apos;s own deliverable or domain is software engineering (personas, &quot;the code/codebase,&quot; insertion points, build/test verification, code examples), and exempt Cairn&apos;s own operating mechanics — git commits and git-log greps, path-scoped staging, the CLAUDE.md/README.md file names, the git-repository requirement — as domain-uniform plugin infrastructure and Claude Code conventions.
    <advantage>Reuses the goal&apos;s own already-stated exclusion logic (migrate-workspace is out of scope because it is &quot;plugin history, not the user&apos;s work type&quot;), giving one durable criterion that classifies even cases the audit did not foresee, and leaves the git-based committing architecture the whole CLAUDE.md invariant set depends on intact.</advantage>
    <drawback>The infrastructure-vs-user-work line still needs a judgment call at the margin (e.g. whether &quot;build/test commands&quot; in the environment-context read is an infra mention or a user-work assumption), so &quot;zero findings&quot; is not a purely mechanical check.</drawback>
  </alternative>
  <alternative id="Neutralize git mechanics too">
    Treat Cairn&apos;s git-dependence itself as an SE assumption to abstract away, so the sweep also neutralizes the commit mechanics, the git-log greps, and the git-repository requirement.
    <advantage>Yields maximal domain-neutrality — a non-technical user (say an event planner) arguably finds &quot;git commit&quot; as alien as &quot;the codebase.&quot;</advantage>
    <drawback>Out of all proportion to the goal and destructive: it would gut shared/commit-procedure.md, capture&apos;s ^Manual-answer: git-log grep, and path-scoped staging — the persistence substrate the entire invariant set is built on — when git is the tool&apos;s storage layer, not a claim about the user&apos;s work type.</drawback>
  </alternative>
  <alternative id="Closed exemption allowlist">
    Pin an explicit closed list of exempt items in requirements.md (git commit mechanics, git-log greps, path-scoped staging, CLAUDE.md/README.md file names, the git-repo requirement) and treat every other software-flavored token as a finding.
    <advantage>Makes the &quot;zero findings&quot; bar maximally measurable — the final re-audit checks each candidate against a written list with minimal interpretation.</advantage>
    <drawback>A closed list is brittle: anything the audit meets that was not foreseen (a future MCP-tool mention, an &quot;exit code 0&quot; success model) has no home and forces re-litigation, front-loading enumeration effort while still risking omissions.</drawback>
  </alternative>
  <recommendation option="Exempt infrastructure by user-work test">Adopt the &quot;does this assume the user&apos;s deliverable is software?&quot; criterion and exempt Cairn&apos;s git mechanics and Claude Code file conventions as infrastructure — it reuses the goal&apos;s own migrate-workspace exclusion logic and gives the independent re-auditor a generalizable rule (with the named items as illustrative, not exhaustive, exemptions), which beats the closed allowlist&apos;s brittleness and rightly rejects gutting the git substrate.</recommendation>
</open-question>

<open-question id="Environment-context replacement wording" status="open">
  <question>What neutral formula replaces the recurring &quot;tech stack, build/test commands, MCP tools, conventions&quot; environment-context phrase across its seven reader files and the corresponding CLAUDE.md invariant — i.e. what is a work-type-agnostic project&apos;s CLAUDE.md expected to supply (domain context, working conventions, how done is verified?), and does the &quot;run /init once at project setup&quot; pointer survive for non-software projects?</question>
  <alternative id="Neutral enumerated formula">
    Replace the phrase item-for-item with neutral equivalents that keep the enumerated shape — e.g. &quot;the project&apos;s domain context, working conventions, available tools, and how work is verified as done&quot; — and retain a reworded, generalized `/init` pointer.
    <advantage>Keeps the concrete grounding value the phrase exists to provide: each reader is still told to look for the verification convention and the available tools (not just vague &quot;context&quot;), which directly serves the goal&apos;s aim of reframing and foregrounding how &quot;done&quot; is verified.</advantage>
    <drawback>An enumerated list is more edit surface to keep consistent across seven files plus the invariant, and a slot like &quot;available tools&quot; can still faintly echo the old MCP/tooling framing if worded carelessly.</drawback>
  </alternative>
  <alternative id="Abstract umbrella phrase">
    Collapse the enumeration into a single neutral umbrella phrase such as &quot;the project&apos;s working context and conventions,&quot; dropping the itemized list while retaining the `/init` pointer.
    <advantage>Maximally domain-silent and shortest — with nothing enumerated, there is no list item left that could leak a work-type assumption, and it is the least text to keep synchronized.</advantage>
    <drawback>Loses the actionable specificity: readers are no longer pointed at the verification method or the available tools, weakening the exact grounding the phrase was there to supply and leaving the goal&apos;s verification-reframing with no anchor in the reader files.</drawback>
  </alternative>
  <alternative id="Drop phrase and /init pointer">
    Remove both the enumerated phrase and the `/init`-at-setup suggestion, treating `CLAUDE.md` as an opaque context source (&quot;read whatever `CLAUDE.md` documents&quot;), on the view that `/init` is itself coding-flavored setup.
    <advantage>Strips even the faint software residue of a &quot;run `/init` at project setup&quot; onboarding step, going furthest toward domain silence.</advantage>
    <drawback>Over-corrects past the goal&apos;s intent: `/init` is a genuine Claude Code built-in that inspects and documents any project regardless of work type, so dropping the pointer discards real cross-domain onboarding value for a mechanism that is not actually domain-specific.</drawback>
  </alternative>
  <applied-principle>Prefer domain-neutral terms</applied-principle>
  <recommendation option="Neutral enumerated formula">Replace item-for-item with a plain-English neutral enumeration (domain context, working conventions, available tools, how work is verified as done) and keep a generalized `/init` pointer: it satisfies the domain-neutral-terms principle while preserving the concrete verification/tools/conventions grounding the goal wants foregrounded — which the abstract umbrella drops — and retains `/init`, a genuinely cross-domain built-in, which the third option needlessly discards.</recommendation>
</open-question>

<open-question id="Verification fallback without conventions" status="deferred">
  <question>When a consuming project&apos;s CLAUDE.md defines no done-verification convention, what should the reframed completion procedure fall back to — direct inspection of the deliverable against the task&apos;s Success criteria, or something stronger?</question>
  <alternative id="Inspect against Success criteria">
    The completer falls back to examining the produced deliverable directly and checking it criterion-by-criterion against the task&apos;s always-present Success section, using whatever means each criterion itself names (read the artifact, or run a command only where a criterion specifies one).
    <advantage>Always applicable and fully work-type-agnostic — it leans only on the Success section, which shared/submit-procedure.md guarantees every task carries, so it needs no build, no test runner, and no assumption about what the deliverable is.</advantage>
    <drawback>The check is only as rigorous as the Success criteria are concrete — a vague or subjective Success bar yields a correspondingly weak verification, with no independent signal beyond the criteria themselves.</drawback>
  </alternative>
  <alternative id="Require active exercise">
    Fall back to something stronger than inspection — require the completer to actively exercise the deliverable or produce independent evidence it works (a dry run, a sample execution, a re-derived cross-check) before accepting it.
    <advantage>Catches faults that static inspection can miss, giving a stronger done-signal when the project supplied no verification convention of its own.</advantage>
    <drawback>&quot;Exercise it&quot; presumes a runnable, executable deliverable — reintroducing exactly the software-build assumption this milestone is removing, since a document, plan, or recipe cannot be &quot;run,&quot; so the fallback would misfit most non-software work.</drawback>
  </alternative>
  <alternative id="Escalate to the user">
    When no verification convention exists, stop and ask the user to define or perform the verification step rather than applying any automatic fallback.
    <advantage>Surfaces the missing convention explicitly and secures an authoritative human check instead of silently accepting a possibly weak criteria set.</advantage>
    <drawback>Breaks unattended completion — the complete-task agent runs in isolation under the complete-all-tasks orchestrator with no user to ask, so a hard stop on every convention-less project would cripple the batch path.</drawback>
  </alternative>
  <recommendation option="Inspect against Success criteria">Direct inspection against the always-present Success section is the only fallback that stays work-type-agnostic — each criterion checked by the means it names needs no build and no user, whereas the stronger alternatives either presume an executable deliverable or a user that isolated batch completion does not have.</recommendation>
</open-question>

<open-question id="Re-audit execution form" status="deferred">
  <question>How is the final independent re-audit executed so it is genuinely independent of the sweep (e.g. a fresh-context agent auditing the whole plugin against the decided finding criteria), and in what form does it report its findings?</question>
  <alternative id="Fresh-context audit subagent">
    A final milestone task whose completion dispatches a single fresh-context subagent (Cairn&apos;s own read-only agent-dispatch idiom) given only the decided finding criteria from &quot;SE-assumption audit boundary&quot; plus the full file set — skills/, agents/, shared/, README.md, CLAUDE.md — with no access to the sweep&apos;s reasoning, and it returns a structured per-finding list (file path, location, offending phrase, which criterion/layer it violates) plus an explicit zero-findings verdict when clean.
    <advantage>Delivers both properties the goal names at once: a context genuinely separate from the sweep&apos;s rationalizations, and a greppable itemized report that maps one-to-one onto the &quot;zero findings&quot; bar — so a clean pass is objectively checkable and any finding is directly actionable as a follow-up task.</advantage>
    <drawback>A subagent shares the sweep&apos;s underlying model and training priors, so its independence is bounded to different-context misses and does not cover blind spots inherent to the model itself.</drawback>
  </alternative>
  <alternative id="Inline manual re-audit">
    A final task completed inline in the same working context that did the sweep, walking each file against the finding criteria and reporting a pass/fail verdict in prose.
    <advantage>Simplest possible form — no dispatch machinery, and the full milestone context stays available for immediate correction of anything found.</advantage>
    <drawback>It is not independent: the same context that performed the sweep audits its own output, which directly defeats the goal&apos;s &quot;independent re-audit&quot; requirement and tends to inherit the sweep&apos;s blind spots.</drawback>
  </alternative>
  <alternative id="Out-of-band human review">
    The re-audit is performed outside the milestone machinery entirely — a human reviewer or a separate Claude session with no milestone context inspects the plugin and reports findings however they choose.
    <advantage>Maximally independent — a wholly separate reviewer can catch framing the model itself is prone to normalize.</advantage>
    <drawback>It sits outside the workflow, so it cannot be a task-completion checkpoint with an enforceable Success bar, its report form is unstructured, and it is not reliably repeatable as the milestone&apos;s objective proof.</drawback>
  </alternative>
  <recommendation option="Fresh-context audit subagent">A fresh-context subagent auditing the whole file set against the decided finding criteria and returning a structured per-finding list (file, location, phrase, violated criterion) with an explicit zero-findings verdict is the only form that satisfies both the goal&apos;s &quot;independent&quot; and its measurable &quot;zero findings&quot; requirements, and it reuses Cairn&apos;s own agent-dispatch idiom so a clean pass is objectively checkable and any finding drops straight into a follow-up task.</recommendation>
</open-question>
