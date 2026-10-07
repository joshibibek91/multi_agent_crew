# 5. Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| The Researcher runs two or three times | The guardrail rejected its facts | Normal. Read the guardrail's message in the next attempt |
| The crew stops after the Researcher with an error about sources | The guardrail failed on every retry | The research had facts without links. Check the search is working, or raise `guardrail_max_retries` a little |
| The crew stops and waits | `ASK_A_HUMAN = True` | Type feedback, or press Enter to approve |
| "Task with id ... not found" when replaying | The ID isn't from the latest run, or that task never finished | Run `crewai log-tasks-outputs` and copy an ID from there |
| `crewai: command not found` | The virtual environment isn't on | Activate `.venv` first |
| The same error appears three times | CrewAI is retrying a failing agent | It's one problem, retried. Read the first message |
| The Editor always says `REMOVED: nothing` | It may not see the research, or the draft is genuinely fine | Check its `context`; then check the draft against the research yourself |
| Installing fails on Python 3.14 | CrewAI doesn't support 3.14 yet | Use Python 3.10–3.13 |
