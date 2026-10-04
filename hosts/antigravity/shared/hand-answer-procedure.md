# Hand-answer procedure (shared core)

This is the single source of truth for recording one open question's answer **given by
hand** in a milestone: a literal answer, or an alternative the user named. It composes over
`shared/answer-procedure.md` (the recording core): it names the standing picks on the other
open questions that the answer undermines, then delegates the actual recording to that core
unchanged, handing it those names. It is followed inline by the `answer-open-question` and
`answer-open-question-with-alternative` skills. The caller supplies the inputs below and
wraps the result; this file describes only the work itself — read, judge, delegate.

A standing pick is the `<recommendation>` element an open question carries. It was formed
before this answer existed, and nothing records what it took for granted beyond a
`<depends-on>` tag, so a pick the answer undermines is named here, where the answer is in
hand, and cleared in the same write that removes the answered block.

## Inputs

This procedure records one hand answer given four inputs the caller supplies, the last
optional:

- **MILESTONE_DIR** — the already-resolved directory of the milestone the question belongs
  to, the `<MILESTONE_DIR>` every path below uses. The caller resolves it; this procedure
  never looks the milestone up, and hands it on to the recording core as that core's own
  `MILESTONE_DIR` input.
- **SHORT TITLE** — the resolved handle of an existing `<open-question>` block to answer
  (its `id`, compared case-insensitively). The caller has already obtained it.
- **ANSWER** — the answer text for that question, as the caller will have it recorded.
- **RECORDED OPTION** *(optional)* — the alternative id the caller lifted as the decision,
  when it lifted one. This procedure hands it on as given, or hands on nothing when the
  caller passed nothing; it never derives it.

The UNDERMINED PICKS input of the recording core is **not** an input here — this procedure
*derives* it, by the judgment of step 2.

## Procedure

### 1. Read the standing picks

Read `<MILESTONE_DIR>/open_questions.xml` whole with the file-reading tool. The read shows
every block with its `<alternative>`, `<applied-principle>`, `<depends-on>`, and
`<recommendation>` children. That whole read is for reasoning only: every locate, list,
lift, and write is a call to the plugin's open-question tool, and the recording core makes
them. Never edit the file yourself.

The blocks to judge are every block **other than the answered one** that carries a
`<recommendation>` element. A block with no `<recommendation>` has no pick to undermine and
is not judged. The answered block's own `<recommendation>` plays no part: the judgment of
step 2 runs on every hand answer, whether or not the option being recorded is the one that
element names.

### 2. Name the picks the answer undermines

For each block to judge, hold two texts from the read: the what-it-is text of the
`<alternative>` its `<recommendation option="…">` names, and the one-line rationale that is
the `<recommendation>` element's own text. Read them against ANSWER and what ANSWER directly
entails. The pick is **undermined** when either holds:

- **The option can no longer be carried out.** The recommended alternative, as its
  what-it-is text reads, cannot be carried out alongside the decision ANSWER records.
- **The stated reason no longer holds.** The rationale states or plainly presupposes
  something ANSWER changed — a fact about the project, a constraint, a sibling's expected
  outcome — so the reason no longer holds as written, even though the option itself could
  still be carried out.

Judge it in prose, from those two texts as they are written. Do not re-form the
recommender's judgment: do not weigh the block's other alternatives, ask which option is now
best, or decide whether the same option would be picked again for a different reason. The
question is only whether this pick, as written, still stands beside the answer. A
`<depends-on>` tag settles nothing here either way: the tool reconciles the tagged
dependents of the answered block itself, and a tagged block is judged by the same two tests
as any other.

**Strip on doubt.** When a pick is only arguably untouched — the option arguably still fits,
or the rationale arguably rests on the changed thing — name it. A named block keeps its
alternatives and the next run of the recommendation pass re-picks over them; a stale pick
left standing is recorded as a decision.

**Leave standing what the answer does not bear on.** A pick whose option text and rationale
text neither conflict with ANSWER nor rest on anything it changed is not named. Sharing a
topic with the answered question is not bearing on it, and doubt means doubt about a pick
the answer touches, not a reason to name every pick.

The Short Titles of the undermined blocks, each the block's `id` as the document holds it,
are **UNDERMINED PICKS**. When no pick is undermined there is none to pass.

### 3. Delegate to the recording core

Hand the given **MILESTONE_DIR**, **SHORT TITLE**, and **ANSWER**, the **RECORDED OPTION**
when the caller supplied one, and the **UNDERMINED PICKS** named in step 2 (nothing for that
input when step 2 named none) to `.agents/plugins/cairn/shared/answer-procedure.md` and follow it
unchanged. That procedure owns the recording work (locate, analyse, fold, remove, cascade)
and passes the names to the tool as given; this procedure only reads, judges, and
delegates, and reports nothing about the picks it named.
