Use the `invoke_subagent` tool, one entry in its `Subagents` array per surviving question, each
entry's `TypeName` set to the name this plugin registers the
`provide-alternatives-to-open-question` agent (singular — the per-question subagent) under,
`provide-alternatives-to-open-question`, and its `Role` naming the question. Pass it, as the
entry's `Prompt`, that question's **Short Title**, the `<MILESTONE_DIR>` resolved in step 0, and
the `<scratch dir>` created in sub-step **a**, and nothing else — the three values the
orchestrator already holds:
