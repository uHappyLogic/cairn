---
name: capture-milestone-principle-updates
description: Distill reusable answering principles from a named milestone's recorded decisions into the project-wide principle store.
---

# capture-milestone-principle-updates

This is the on-demand harvester of the answer-principle-learning loop. Over a milestone, every
recorded answer is one commit on the milestone's `requirements.md` under one of three subjects —
`Manual-answer:`, `Alternative-answer:`, or `Recommendation-answer: <Short Title>` — whose body carries
the recorded answer and whose diff preserves the analysis the user saw when recording it. This skill
reads that finite, known-up-front set of commits for the milestone you name and distills from them
the generalizable answering principles that the recommendation advisor can apply.

It runs against **any** milestone id whose `milestones/<milestone_id>/requirements.md` exists — the
current milestone, an unfinished one, or one already finished (backfill included). Because every
answer commit lands during the requirements phase, the milestone's finish status carries no
information the harvest needs: a run against a milestone whose questions are still being answered
simply harvests what exists so far, and a later run re-walks the same path to pick up the rest.
Running it right after `/finish-current-milestone` is the natural moment, since the milestone's
answer set is complete by then, but it is never a precondition.

It is the **sole writer** of `milestones/answer_decision_principles.md` (a single project-wide file at
the `milestones/` root, **above** any one milestone, so principles accumulate across milestones).

## Usage

```
/capture-milestone-principle-updates <milestone_id>
```

- `<milestone_id>` (**required**): the milestone directory name under `milestones/`, e.g.
  `milestone_12_user-guide` — exactly as `/specify-milestone-starting-state` takes it. No bare-number
  form is accepted and no number-to-directory resolution exists; the value is used verbatim.

**Example:**
```
/capture-milestone-principle-updates milestone_12_user-guide
```

> This skill writes **only** the principle store at the fixed path
> `milestones/answer_decision_principles.md`. It does **not** touch any milestone's `requirements.md`.
> When a pass composes a store rewrite it writes it in place and — once the user has reviewed the
> working-tree change with `git diff` and confirmed it — **commits** that rewrite itself (step 7); a
> pass that distills nothing, or whose rewrite the user rejects, leaves the store as it stood and
> commits nothing. It imposes no clean-store precondition and does not refuse a milestone already
> captured — both cases pass through a notice-and-confirm guard (step 2), never a stop.

## Workflow

### 1. Locate the milestone

If no `<milestone_id>` argument was given, stop and report that the milestone id is required, showing
the usage above.

Resolve `<MILESTONE_DIR>` as `milestones/<milestone_id>/`. If `milestones/<milestone_id>/requirements.md`
does not exist, **stop without changing anything** and report that the milestone was not found —
list the `milestone_*` directories present under `milestones/` so the caller can retry with one of
them. Directory existence is the only validation; nothing about the milestone's finish status is
consulted.

The same `<milestone_id>` feeds, verbatim, the repeat-capture guard's anchored grep in step 2, the
path-scoped commit walk in step 3, and the commit subject in step 7.

### 2. Start-of-run guards

Two guards run here, before the commit walk. Each is a **one-line notice plus a single proceed
confirmation, never a stop**: on a hit, print the one-line notice, ask once whether to proceed, and
on yes continue exactly as if the guard had not fired. Declining is the user's clean stop — report
it in one line, having read nothing further, changed nothing, and committed nothing. With no hit, a
guard prints nothing and asks nothing; the run continues unchanged.

1. **Repeat-capture guard.** The `Principle-capture: <milestone_id>` commit subject is the record
   that this milestone was already ingested. Grep the history for that exact subject, **anchored on
   both ends**, with `<milestone_id>` verbatim from step 1:

   ```
   git log --grep='^Principle-capture: <milestone_id>$' --format='%h %ad %s' --date=short
   ```

   On a hit, the notice names the prior commit (its short hash, date, and subject) and asks once
   whether to proceed with a repeat capture. Only a committed capture is detectable: this skill
   writes **no empty commit** to record a no-op run (step 7 has no `--allow-empty`), so a prior run
   that changed nothing — an empty commit range, a store left identical to its baseline, or a
   rejected rewrite — leaves no trace here and is not detected.

2. **Dirty-store guard.** Check whether the store already carries uncommitted changes:

   ```
   git status --porcelain -- milestones/answer_decision_principles.md
   ```

   On any output, the notice states that `milestones/answer_decision_principles.md` has uncommitted
   changes and asks once whether to proceed. On proceed, the **working-tree file — not `HEAD` — is
   the baseline** every later step reads and the store rewrite composes over: the pending edits stay
   in place and are built on, never discarded or diffed away.

### 3. Walk the milestone's answer commits

Collect every answer commit for this milestone — all three provenances — with a **path-scoped**
log, using the `<milestone_id>` from step 1 verbatim in the path:

```
git log --format='%h %s' -E --grep='^(Manual-answer|Alternative-answer|Recommendation-answer): ' -- milestones/<milestone_id>/requirements.md
```

- **The path filter is itself the lower boundary.** `milestones/<milestone_id>/requirements.md` does
  not exist before `/define-milestone-goal` created it, so no earlier commit can touch it — there is
  no need for a milestone-start marker or recorded base SHA. It is also the only boundary on the
  harvest: no finish marker or upper bound is applied.
- **Every subject is `<Marker>: <Short Title>`.** The marker names the provenance and the remainder
  is the answered question's Short Title — the `id` of the `<open-question>` block the answer removed.

If the walk returns **no qualifying commits**, this is the empty-range exit — go straight to step 8
(it is a normal outcome, not an error).

Otherwise, for **each** commit, read three things and build one per-commit record from them.

**Read the subject, the body, and the diff.**

```
git show <hash> --format='%s%n%n%b' -- milestones/<milestone_id>/requirements.md
```

- **Subject → provenance and Short Title.** Split on the first `: `. The marker is the provenance
  (`Manual-answer`, `Alternative-answer`, `Recommendation-answer`); the remainder is the Short Title.
- **Body → the recorded answer as written.** Drop git trailers first — the trailing run of `Key: value`
  lines such as `Co-Authored-By:` and `Claude-Session:` — and keep the rest verbatim. What the body
  holds differs by provenance: a `Manual-answer:` body is the user's rationale when deliberation was in
  context, otherwise the literal answer text; a `Recommendation-answer:` body is the lifted
  "`<option>` — `<rationale>`" of the recommendation; an `Alternative-answer:` body is the chosen
  alternative's "`<id>` — `<what-it-is>`". No user rationale exists on either lifted path.
- **Diff → the block the user saw, and the decision they recorded.** `shared/answer-procedure.md`
  folds the decision into `## Decisions` and then removes the whole `<open-question>` block, so the
  diff's **removed lines** (`-` prefix) hold the full block as it stood when the answer was recorded and
  its **added lines** (`+` prefix) hold the new `## Decisions` entry. Locate the answered block among
  the removed lines by its opening boundary `-<open-question id="…"` whose `id` matches the Short Title
  (case-insensitive, entity-unescaped, attribute order immaterial) and read through its
  `-</open-question>` closing line. Any **other** removed block in the same diff is a cascaded sibling
  the answer mooted — it is not the answered block and contributes nothing to this record. From the
  answered block reconstruct, reversing the five predefined XML entities (`&lt;` `&gt;` `&quot;`
  `&apos;`, then `&amp;` last) on every value:
  - the `<question>` text;
  - each `<alternative id="…">` — its `id`, its **what-it-is** text (the element's own text before its
    first child), and its `<advantage>` / `<drawback>` children — in document order: these are the
    options the user saw;
  - every `<applied-principle>Short Title</applied-principle>` line — the store entries the recommender
    cited (zero or more; each is one store `### <Short Title>`);
  - the `<recommendation option="…">…</recommendation>` element — its `option` attribute and its
    rationale text — or **none** when the block carries no `<recommendation>` element. A block the
    recommend sweep never annotated has only a `<question>`; an answer recorded before the block form
    existed removes no `<open-question>` at all (its removed lines are a `> **Deferred — …:**` or
    `> **Open — …:**` blockquote). Both are the **no-recommendation** case, never an error.

**Classify the commit by two tests, in this order.**

1. **Agreement — did the recorded option match the removed recommendation?** First derive the
   **recorded option** per provenance:
   - `Recommendation-answer:` — the body text before its first spaced em dash (` — `) is the option;
     it is the lifted recommendation, so agreement holds by construction.
   - `Alternative-answer:` — the body text before its first ` — ` is the chosen alternative's `id`.
   - `Manual-answer:` — the alternative whose `id` the body or the added `## Decisions` entry names
     outright, or, when no `id` is named verbatim, the alternative whose what-it-is text the recorded
     decision plainly matches; when the decision matches none of the removed alternatives, the recorded
     option is a fresh one outside the analysis.

   Then compare that recorded option against the removed `<recommendation>`'s `option` attribute
   (trimmed, case-insensitive, both entity-unescaped) and assign exactly one class:
   - **`non-override`** — the block carried **no** `<recommendation>` element (assigned before any
     comparison; only a `Manual-answer:` can land here, and it is still a principle source).
   - **`agrees`** — the recorded option equals the recommended option (every
     `Recommendation-answer:`, plus any `Alternative-answer:` or `Manual-answer:` that recorded the
     recommended option).
   - **`overrides`** — a recommendation existed and the recorded option is a different alternative or a
     fresh option.

2. **Body — deliberated or bare?** Apply the **bare-cold-answer test** step 5 already uses: the body is
   **`deliberated`** when, beyond stating the decision, it states the reasoning behind it — the
   alternatives weighed, why one was chosen, the trade-off accepted — and **`bare`** when it is only the
   decision itself (the literal answer or a lifted element's text) with no reason stated. Read the
   trailer-stripped body as a whole; an inline "because" clause the user typed makes it deliberated. By
   construction every `Alternative-answer:` and `Recommendation-answer:` body is **`bare`** — it is
   lifted element text carrying no user rationale (the recommendation body holds the recommender's
   reasoning, not the user's, which is not what this test looks for). Only a `Manual-answer:` body can
   be `deliberated`.

**The per-commit record.** Hold one record per commit, in walk order, with these fields — this is
what steps 4, 5, and 6 consume:

| Field | Value |
|---|---|
| `hash` | the commit's short hash |
| `provenance` | `Manual-answer` \| `Alternative-answer` \| `Recommendation-answer` |
| `short_title` | the Short Title from the subject |
| `body` | the trailer-stripped body, verbatim |
| `recorded_decision` | the added `## Decisions` entry text from the diff |
| `question` | the removed `<question>` text |
| `alternatives` | ordered list of (`id`, what-it-is, advantages, drawbacks) the user saw; empty when the block carried none |
| `applied_principles` | list of cited store Short Titles; empty when none |
| `recommendation` | (`option`, rationale), or `none` |
| `recorded_option` | the option derived in test 1 (an alternative `id`, or the fresh-option text) |
| `agreement` | `non-override` \| `agrees` \| `overrides` |
| `body_class` | `deliberated` \| `bare` |
| `override_rationale` | filled by step 4: the user's stated (or accepted best-guess) reason for the override; `none` for every commit step 4 did not prompt or the user skipped |

### 4. Prompt for override rationales

The walk has now told you which answers overrode the recommendation the user saw — but an override
commit often records **no reason**: the user picked a different option and the body holds only the
option, not the why. That why is the guideline the recommender lacked, so this step asks for it, once
per such commit, before anything is distilled.

**Eligibility — prompt only for an override commit carrying no user rationale.** A commit is
prompted exactly when its record has `agreement` = `overrides` **and** `body_class` = `bare`. That is:

- **every non-agreeing `Alternative-answer:`** — its body is the lifted "`<id>` — `<what-it-is>`",
  never a user rationale; and
- **a non-agreeing `Manual-answer:` whose body is the bare literal answer**, judged by the same
  bare-cold-answer test as step 3's body classification.

Every other commit is **never prompted**:

- a **deliberated `Manual-answer:`** body (`body_class` = `deliberated`) is read as the user's own
  answer to the why and is not re-prompted, even when it overrides;
- an **agreeing answer** (`agreement` = `agrees`) — every `Recommendation-answer:`, and any
  `Alternative-answer:` or `Manual-answer:` that recorded the recommended option — has nothing to
  explain: asking why the alternative was preferred would rest on a false premise;
- a **non-override `Manual-answer:`** (`agreement` = `non-override`) saw no recommendation, so there
  was nothing to prefer the answer over; it stays a principle source through its body in step 5.

If no commit is eligible, this step prints nothing, asks nothing, and the run continues to step 5.

**Open with a one-shot choice.** Before the first prompt, tell the user how many commits are eligible
and ask **once** how to handle them:

- **accept every best guess** — each eligible commit takes its best guess as its `override_rationale`,
  with no per-prompt review;
- **skip every prompt** — each eligible commit's `override_rationale` is `none`;
- **review one at a time** — walk the individual prompts below.

The two blanket choices exist so a backfill run over an older milestone the user no longer remembers
stays workable in one answer instead of a prompt per commit.

**Each prompt shows the skill's best guess.** Per eligible commit, in walk order, show:

- the Short Title and the `<question>` text;
- the **recommended option** (`recommendation.option`) with a one-line digest of its rationale;
- the **recorded option** (`recorded_option`) — the alternative `id` and its what-it-is text, or the
  fresh-option text when the decision matched none of the removed alternatives;
- the **best guess** at why the user preferred the recorded option, derived from three things and
  nothing else: the removed `alternatives` (in particular the recorded alternative's `<advantage>`
  children and the recommended alternative's `<drawback>` children), the removed `recommendation` (the
  reasoning the user evidently did not accept), and the `recorded_option` (or, for a fresh option, the
  `recorded_decision` text stating what none of the alternatives offered). Phrase it as one or two
  sentences in the user's voice — the trade-off they appear to have weighed the other way — not yet as
  a store directive; distilling is step 5's job.

Then ask the user to **accept the guess**, **state their own reason** in a sentence or two, or
**skip**. Each prompt is skippable on its own: a skip records `override_rationale` = `none` for that
commit and moves to the next; an accepted guess or a typed reason becomes that commit's
`override_rationale`. Never revise, drop, or re-prompt a commit once answered.

**Output.** Every per-commit record now carries its `override_rationale`. The prompted rationale is
what step 5 reads as the commit's reasoning in place of its bare body, so an override the user
explained here yields candidates exactly as a deliberated `Manual-answer:` body does, while a skipped
one stays a bare answer and is dropped by step 5's non-generalizable filter.

### 5. Phase 1 — extract override candidates, read acceptance evidence, dedup (internal, no user yet)

This phase is entirely internal: no writes, no user prompts. It reads the per-commit records from
steps 3 and 4 twice over, for two different outputs: **new principle candidates** come only from the
commits that carry the user's own reasoning, while every commit that **accepted** the recommendation
supplies **evidence about entries already in the store** and nothing else. Both outputs feed phase 2.

1. **Extract candidate directives — from override reasoning and deliberated manual bodies only.** A
   candidate's source is the reasoning the recommender lacked, so a commit is a candidate source
   exactly when it carries the user's reasoning, read from one of these places:

   - an **override commit** (`agreement` = `overrides`) — its `override_rationale` when step 4 filled
     one, otherwise its `body` when `body_class` = `deliberated` (a deliberated `Manual-answer:`
     override); an override that was skipped in step 4 and has a bare body carries no reasoning and
     yields no candidate;
   - a **non-override `Manual-answer:`** (`agreement` = `non-override`) — its `body`: the recommender
     never weighed in, so a decision it did not get to see is precisely a guideline it lacks;
   - a **deliberated agreeing `Manual-answer:`** (`agreement` = `agrees`, `body_class` = `deliberated`)
     — its `body`: agreement suppresses the override prompt, never source eligibility, and the
     deliberated rationale the commit carries is still the user's own reasoning.

   Nothing else yields a candidate. An **accepted `Recommendation-answer:` never yields a candidate**:
   its body is the recommender's own reasoning, lifted verbatim, so it cannot supply the guideline the
   recommender lacked. An **agreeing `Alternative-answer:` yields none** either: its body is only the
   chosen alternative's text, and there was no override to explain — whereas a **deliberated agreeing
   `Manual-answer:` still does**, through its body. Source eligibility is thus governed by the reasoning
   a commit carries, never by its subject alone.

   From each eligible source pull the reusable reasoning behind the decision: the realistic
   alternatives that were weighed, why one was chosen, the trade-off accepted. Phrase each as a
   candidate **keep/eliminate directive** — a rule you could apply as a binary in/out test against the
   candidate answers of a *different future* question.

2. **Drop the non-generalizable ones.** A principle must be a **reusable directive, not a restatement
   of one past decision**. If a source's rationale is one-off, situation-specific, or simply states no
   reasoning at all (a bare cold answer), it yields **no** candidate — drop it. The commit→principle
   mapping is **many-to-many**: one commit may yield no candidate, and two commits may yield the same
   one.

   - **Restatement (drop):** "Answer-commit identification uses a `Manual-answer:` subject and no
     trailer." Names one question and one answer; cannot judge any *other* question.
   - **Reusable directive (keep):** "When two mechanisms reach the same goal, prefer the one that makes
     a property a hard invariant over one that only enforces it best-effort." A test applicable to an
     unrelated future question's candidates.

3. **Cluster the survivors against each other (cross-candidate dedup).** Where several commits
   express the **same** underlying rule, merge them into one candidate (carrying the strongest
   phrasing and the originating examples). The candidate output of phase 1 is the deduped set of
   surviving candidates, ranked **strongest first** (most clearly generalizable / most load-bearing for
   future recommendations).

4. **Read acceptance evidence from the agreeing commits.** Every commit with `agreement` = `agrees` —
   each accepted `Recommendation-answer:`, plus any `Alternative-answer:` or `Manual-answer:` that
   recorded the recommended option — is **evidence only**: it is never mined for a candidate, but its
   record says something about entries already in the store. Two signals, both read from fields the
   step-3 diff read already filled — **no further read of git or the store is needed**:

   - **Reinforcement — from `applied_principles`.** Each removed `<applied-principle>` line names a
     store entry the recommender cited and the user then accepted: that citation **reinforces** the
     entry and **shields it from being pruned or narrowed in this pass**. An agreeing
     `Alternative-answer:` or `Manual-answer:` reinforces its cited entries exactly as an accepted
     `Recommendation-answer:` does.
   - **Contradiction — from `recommendation`.** The accepted recommendation's rationale is reasoning
     the user endorsed. Where that accepted rationale **contradicts** an existing store entry — it
     argues for what the entry's directive would eliminate, or against what it would keep — **flag**
     that entry **for the salvage path** phase 2 applies to contradicted entries. An entry both
     reinforced and flagged in the same pass keeps its shield: it is not pruned or narrowed, and the
     salvage path must find a form that fits both.

   An **override** commit's `applied_principles` are read against its reasoning by the same
   contradiction test: a cited entry that steered the recommendation the user rejected is flagged
   when the override rationale contradicts it, and untouched when the override turned on something
   else.

**Output.** Phase 1 hands phase 2 two sets: the ranked **candidate set** from steps 1–3, and the
**evidence set** from step 4 — the store entries **reinforced** in this pass (each with the commits
that cited it) and the entries **flagged** as contradicted (each with the commit whose reasoning
contradicts it). Phase 2 never prunes or narrows a reinforced entry, and routes each flagged entry to
the salvage path.

If phase 1 leaves **no** surviving candidate **and** no flagged entry (commits existed but none
generalize and none contradict the store), go to step 8 — this converges on the **same** "nothing
captured" report as the empty range. Reinforcement alone changes nothing in the store.

### 6. Phase 2 — compose the whole-store rewrite and write it in place

Phase 2 turns the two phase-1 sets into **one** proposed store and writes it **once**. There is no
per-candidate loop: every change — add, revision, prune, merge, generalization, shortening — is
composed together over the baseline and lands in a single in-place write of
`milestones/answer_decision_principles.md`. The write is not the confirmation: the user reviews the
resulting working-tree change with `git diff`, and the single confirmation that gates the commit is
step 7's. This step prints **no diff and no store content** to the conversation — the working tree is
the review surface.

1. **Read the baseline whole.** Read the entire live `milestones/answer_decision_principles.md` as it
   stands in the working tree — the baseline fixed in step 2, whether or not it matches `HEAD`. It is
   small and grows slowly, so reading it whole is always feasible. If the file is absent or empty, the
   baseline is the header paragraph alone with no entries, and the write below creates the file.

2. **Compose the proposed store over the baseline.** Hold the baseline's entries in context and decide,
   for the whole set at once, what the store should read after this milestone. Apply these moves
   together, as one composition — never as a sequence of writes:

   - **Place each candidate** from the phase-1 ranked set, strongest first. Find the baseline entries
     whose *statements* (not just their `### <Short Title>` headings) bear on it; an exact
     case-insensitive title collision is only a strong hint that pre-selects a likely revise target —
     the deciding test is semantic overlap. Where an entry overlaps, the candidate becomes a
     **revision** of that entry (its directive restated so it carries both); where none does, it
     becomes an **add** as a new `### <Short Title>` entry. A candidate that overlaps an entry another
     candidate is already revising folds into that same revision rather than adding a near-duplicate,
     and two candidates that would each add the same rule become one add.
   - **Resolve each flagged entry** from the phase-1 evidence set that no candidate's revision already
     resolved. Current reasoning — the accepted or override rationale that flagged it — takes
     precedence over the entry as it stands, and the entry is **salvaged** before it is dropped: try
     these four forms **in this fixed order** and take the first that fits, where a form fits when the
     resulting entry still predicts both the accepted citations the entry earned and the reasoning
     that flagged it:
     1. **Narrow its scope clause.** Every entry opens with an explicit scope clause; tighten it until
        the contradicting case falls outside the rule while every accepted citation stays inside.
     2. **Generalize it** so the prior accepted citations and the override both fit — restate the
        directive at the altitude where both are instances of one rule.
     3. **Replace it with a fresh directive** when its premise is wrong — what the accepted citations
        and the override jointly support is a different rule, not a wider or narrower one.
     4. **Delete it** only when nothing survives — no form predicts both, so the entry is pruned.

     When two forms fit equally, break the tie by whichever yields the **shortest entry that still
     predicts both** the prior accepted citations and the override. The form chosen is part of this
     composition and is visible in the working-tree change the user reviews with `git diff` before
     step 7's confirmation — a narrowed clause, a generalized or replaced directive, or a removed
     entry — with no separate account of the choice printed.
   - **Honor the shield.** An entry **reinforced** by a citation in this pass is never pruned or
     narrowed — not by a revision, not by a flagged-entry salvage. For a reinforced-and-flagged entry
     the ladder's first and last rungs are therefore unavailable: the salvage must find a
     generalizing or replacing form that fits both, and never deletes it.
   - **Merge plain duplicates.** Two entries — baseline, new, or one of each — that plainly state the
     same rule become one entry carrying the stronger phrasing under one `### <Short Title>`.
   - **Hold every directive to the compactness bar.** A directive should run roughly **40–80 words**.
     One that exceeds about **100** words is flagged for shortening, and the deciding standard is the
     qualitative test — **as short as it can be while still reading as an intuitive rule** — so a
     directive keeps a condition or corollary it genuinely needs and sheds everything else. The
     numbers are a soft target under that test, never a hard cap.
   - **No ceiling on entry count.** Prune by contradiction and merge by overlap are the only count
     control; never drop or merge an entry to hit a size.

   **What may touch which entry.** A **substantive** change — adding an entry, or pruning, narrowing,
   generalizing, or replacing what an entry *decides* — requires this milestone's own evidence: a
   candidate that overlaps it or a flag that names it. **Form-only hygiene** — shortening a directive
   past the ~100-word flag, and merging two entries that plainly duplicate each other — may reach
   **any** entry, evidenced by this milestone or not, with the applied test unchanged: evidence gates
   what a rule decides, not how tersely it is written. An entry that is neither evidenced, nor over
   the bar, nor a duplicate passes through verbatim.

   Every entry in the composed store follows the schema in step 6a: one `### <Short Title>` heading per
   entry, the directive in prose, and — when kept — the `*Origin:*` line as a **single-line pointer**
   to the originating question (a revised or merged entry keeps one such line, pointing at the question
   a revise-vs-salvage judgment or a human auditor would read). The header paragraph above the first
   entry is carried over unchanged.

   If the composed store is **identical to the baseline** — every candidate resolved into an entry
   that already says it, no flag changed an entry, and no hygiene applied — there is nothing to write:
   take no snapshot, write nothing, and go to step 8 (a nothing-captured outcome, like the empty range).

3. **Snapshot the store immediately before the first write.** Copy the baseline as it stands in the
   working tree to a temporary file outside the repository and hold its path:

   ```
   SNAPSHOT="$(mktemp)" && cp milestones/answer_decision_principles.md "$SNAPSHOT"
   ```

   If the store does not exist yet, record the snapshot as *absent* instead. This snapshot — not
   `HEAD` — is the restore point for the rewrite (in the clean case it simply equals `HEAD`; after a
   dirty-store proceed it preserves the user's own edits), and nothing else is written before it is
   taken.

4. **Write the composed store in place, once.** Replace the full content of
   `milestones/answer_decision_principles.md` with the composed store in a single write. Do not stage
   or commit it, and print no diff and no store content to the conversation: the working-tree change
   is what the user reviews with `git diff` before step 7's confirmation.

**Termination is deterministic.** The composition is one pass over two finite sets fixed by phase 1 —
the ranked candidates and the flagged entries — each resolved into the composed store, so the phase
ends when the one write lands.

#### 6a. Entry schema

Each entry is one principle per subsection:

```markdown
### <Short Title>

<The principle as a generalizable keep/eliminate directive — a reusable decision
rule that can be applied to the candidate answers of a future question, not a
restatement of one past decision.>

*Origin: <originating question or example>*
```

- **`### <Short Title>` heading — the handle.** A 2–5 word unique name, mirroring the open-question
  Short-Title convention. This is the key this skill matches on for revise-vs-add. No separate ID scheme.
- **Body — the directive in prose.** A generalizable keep/eliminate rule, not a restatement of the
  originating decision, held to step 6's compactness bar (roughly 40–80 words, flagged past about 100).
- **`*Origin:*` line — optional, single-line.** A one-line pointer to the originating question or
  example, to aid human auditing and future overlap judgments. Omit it when there is nothing useful to
  record. What is applied is the *statement*, not the origin.
- **No status field.** Presence in the file means confirmed.

### 7. Review, confirm, and commit the principle-store update

This step runs only after step 6 wrote the composed store. A pass that wrote nothing — the empty
commit range (step 3), no surviving candidate and no flagged entry (step 5), or a composed store
identical to its baseline (step 6) — went straight to step 8 and never reaches this step or the
shared commit procedure: with nothing of its own written, running that procedure would let its
dirty-own-path guard commit the user's edits admitted by step 2's dirty-store guard under this
skill's subject. No empty commit is written to record such a run either.

**The write was not the confirmation; this is.** The working tree is the only review surface. Tell
the user, in one line, that the composed store has been written to
`milestones/answer_decision_principles.md` and is ready to review with
`git diff -- milestones/answer_decision_principles.md`, and ask **once** whether to commit it. Print
no diff and no store content yourself. Exactly one confirmation gates the commit — there is no
per-entry or per-change confirmation, and there is none for the write itself.

**Review rounds.** The user reviews the working-tree change and may request changes in
conversation — reword an entry, undo a prune, keep two merged entries separate, tighten or loosen a
directive, drop a hygiene shortening. Each round, **re-edit `milestones/answer_decision_principles.md`
in place** to carry the request, still composing under step 6's rules (the step-6a entry schema, the
evidence gate on what an entry decides, the compactness bar), then ask the same confirmation again.
Take **no new snapshot** — the step-6 snapshot stays the restore point for the whole loop — and print
no diff after a round either; the user re-reads `git diff`. A reply that is neither an explicit
acceptance nor an explicit rejection is a change request or a question: handle it and ask again.
There is no round limit; the loop ends only on one of the two answers below.

**On acceptance — commit.** Read and follow the shared commit procedure at `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` (run `echo "$CLAUDE_PLUGIN_ROOT"` if you need to resolve the path), carrying out its steps yourself. Supply it these two inputs:

- **PATHS** — this skill's own change set: the fixed-path store `milestones/answer_decision_principles.md` (a `milestones/`-root artifact, **not** any `<MILESTONE_DIR>` file — this skill writes only that store).
- **SUBJECT** — `Principle-capture: <milestone_id>`, with `<milestone_id>` the argument from step 1 used verbatim (e.g. `Principle-capture: milestone_12_user-guide`), the marker naming this skill's distinctive principle-capture function.

The shared procedure owns the path-scoped staging, the dirty-own-path no-op guard, and the commit.
The rewrite is committed as it stands after the last review round, over the working-tree baseline,
so edits admitted in step 2 ride in the same commit. Once the commit lands, discard the snapshot
(`rm -f "$SNAPSHOT"`) and go to step 8 (captured).

**On explicit rejection — restore the snapshot and exit without committing.** Restore the store
from the step-6 snapshot, **not from `HEAD`**:

```
cp "$SNAPSHOT" milestones/answer_decision_principles.md && rm -f "$SNAPSHOT"
```

When the snapshot was recorded as *absent*, remove the file the write created instead
(`rm milestones/answer_decision_principles.md`). Either way the store stands exactly as it did
before the first write: in the clean case that is `HEAD`; after a dirty-store proceed it is the
user's own uncommitted edits, which survive intact. Then **exit explicitly — do not invoke
`shared/commit-procedure.md`**, not even for its guard: stage nothing and commit nothing. The
procedure's dirty-own-path guard would read the user's surviving edits as this pass's change and
commit them under `Principle-capture: <milestone_id>`, which is why the rejection path never reaches
it. No empty commit records the rejection. Go to step 8 (nothing captured).

### 8. Report

- **If the rewrite was committed** (step 7, acceptance), print exactly one fixed terse status line
  and nothing else:

  `Principles captured.`

  Carry no principle `### <Short Title>`, no add/revision breakdown, and no commit subject, and print
  no next-step or recommendation-advisor pointer. A rewrite that was written but not committed
  never earns this line.
- **If nothing was captured**, report it in a **single line** — distinct from the terse success
  line, never a collapse into `Principles captured.` — stating that nothing was captured, that
  nothing was committed, and briefly which case ended the run. The four cases share this one-line
  shape and differ only in that brief reason:
  - **empty commit range** (step 3): no answer commits touch this milestone's `requirements.md`;
  - **no candidates** (step 5): commits were in range, but none generalizes and none contradicts
    the store;
  - **composed store identical to its baseline** (step 6): everything the milestone teaches is
    already in the store, so nothing was written;
  - **rejection** (step 7): the rewrite was declined and the store restored to its pre-write state.

  Each is the distinct one-line no-op message for a pass that changed none of its own paths — git
  holds no record of a no-op, so the console must carry it.
