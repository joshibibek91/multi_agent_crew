# 2. The new features — exactly what each does

## context — what a task can see

We tested what the Editor receives under each setting:

| `context` setting | Sees the research | Sees the draft |
|---|---|---|
| Not set (the default) | Yes | Yes |
| `[research_task, write_task]` | Yes | Yes |
| `[write_task]` | **No** | Yes |
| `[]` (empty) | No | No |

**By default, every task sees the results of ALL earlier tasks.** As a
crew grows, later tasks receive more and more text — slower, more
expensive, and less focused (the Day 2 lesson).

`context=[...]` lets you choose. We still write it for the Editor, even
though it matches the default here, because it makes the Editor's needs
**visible**, and stays correct if you add more tasks later.

## guardrail — a check in code on a task's result

    research_task = Task(..., guardrail=check_sources, guardrail_max_retries=2)

The function receives the task's result and returns `(True, result)` to
accept it, or `(False, "what is wrong")` to reject it. When rejected, the
agent is shown your message and tries again — up to the retry limit.

We tested it: research without links was rejected, the message reached the
Researcher, and its second try passed.

This is the Day 22 lesson inside CrewAI: **a rule in code cannot be argued
with.**

## human_input — a person reviews the result

    edit_task = Task(..., human_input=True)

After the agent finishes, the crew shows its answer in the terminal and
waits. Type feedback and the agent revises; press Enter to approve.

We tested it: the feedback reached the Editor, it revised, and the crew
finished after approval.

**The limit:** it waits for typing in the terminal. That works for a
script on your laptop — not for a web app with real users.

## replay — re-run a finished crew from one task

    crewai log-tasks-outputs
    python experiments/replay_from_task.py <task ID>

We tested two situations:

| Situation | Result |
|---|---|
| A **finished** run, replayed from the Writer | The Researcher made **0** calls. Its saved result was reused |
| A run that **crashed** at the Writer | Replay **failed**: "Task not found". Only finished tasks are saved |

**Replay is for redoing a finished run** — for example after improving the
Writer's instructions. **It is not crash recovery.**

It also only remembers the **most recent** run.
