# Milestone 42: Stale picks as undeclared dependents

## Goal

When a question is answered by hand (`/answer-open-question` or `/answer-open-question-with-alternative`), the runner names the standing recommendations on other open questions that the answer undermines, and the open-question tool's `remove` reconciles them as dependents of the answered question in the same write as the `<depends-on>`-tagged ones, transitively and keeping their alternatives, so the answer sweep cannot record a pick formed without that answer. Picks the answer does not bear on are left standing, and doubt strips. The milestone also decides whether `/modify-milestone-goal` clears the picks a revision undermines, and implements that if so.

The change is measured by replaying historical stale-pick cases, counting both the stale picks it clears and the unaffected picks it leaves standing. The replay runs outside the repository's tracked files, and no committed artifact carries historical data from it beyond aggregate results.

Out of scope: the answer sweep and `/answer-open-question-with-recommendation`, which both stay as they are, including the sweep's fold-time contradiction rule and its advisory; the recommendation pass and its disclosure duty; conflicts between picks of the same recommendation pass; hand edits to `requirements.md` outside the skills.

## Relevant starting state

## Decisions

## Out of Scope

