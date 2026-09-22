# TASKS TODO

## Headless Chains Add Alternatives Line

Update `docs/ways-of-using-cairn.md`: insert `claude -p "/cairn:provide-alternatives-to-all-open-questions" --dangerously-skip-permissions --model "opus" --effort xhigh` between the review and recommend lines of every chain carrying a recommend line, change every `/cairn:recommend-all-open-questions` line to `--model "fable" --effort high`, and rewrite each affected way's settings sentence to name the two settings (the stuck-milestone way no longer states that every line runs at max). Ordered last because the two skills must exist before the page records them. Verified by every fenced line being runnable as written and the page's three sibling links intact.

---
