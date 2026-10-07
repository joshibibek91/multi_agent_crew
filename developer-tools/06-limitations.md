# 6. What CrewAI can and can't do — tested, not assumed

Many tutorials say CrewAI "can't" do things it now can. We tested each
claim against CrewAI 1.15.

| Claim you may read | The truth (CrewAI 1.15) |
|---|---|
| "No way to check results in code" | **False.** `Task(guardrail=...)` checks a result and makes the agent retry |
| "No way to ask a human" | **Partly false.** `Task(human_input=True)` asks a person — but only by typing in the terminal |
| "If it stops, you start again from the beginning" | **Mostly true.** `replay` can redo a *finished* run from a chosen task. But a run that *crashed* cannot be continued from the crash |
| "The later agent only sees the previous task" | **False.** By default, each task sees *all* earlier results. Use `context` to narrow it |
| "Errors are vague" | **Partly true.** The first error message is usually clear; repeated retries can make it look like several problems |

## The limits that remain

| Limit | What it means |
|---|---|
| **No crash recovery** | A run that fails in the middle cannot continue from where it stopped |
| **Human review only in the terminal** | No built-in way to pause for a person in a web app and continue later |
| **Errors travel forward** | A wrong fact from the first agent passes every later check |
| **Cost grows with the crew** | Every task receives every earlier result, unless you narrow `context` |
| **Little control over the flow** | Tasks run in a fixed order. Branching and loops are hard to express |

## What real teams do

> Build a first version in CrewAI, to check the idea works. Then rebuild the
> parts that matter in LangGraph — which can save progress after every step,
> continue after a crash, pause for a person and resume later, and branch.

That is Days 25 and 26.
