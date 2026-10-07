# 4. Experiments

Change one thing at a time, then change it back.

---

## 1. The blind editor

In `travel_crew.py`, change the edit task to:

    context=[write_task],

Now the Editor sees **only the draft** — not the research. (We tested this.)

**What you will see:** the Editor still "checks" the draft and often says
`REMOVED: nothing` — but it has nothing to check it against. It is
approving things it cannot verify.

**Then try** removing the `context=` line completely. The Editor sees the
research again, because by default every task sees everything before it.

---

## 2. The poisoned source   ★ the most important one

    python experiments/poisoned_source.py

The Writer and Editor are given research notes with one wrong fact:
*"Bandipur is a 10-minute drive from Pokhara"* (it is roughly 70–80 km).

**What you will usually see:** the wrong fact appears in the article, and
the Editor reports `REMOVED: nothing`. The script tells you at the end.

**Why:** the Editor checks the draft *against the research*. The research
says it — so as far as the Editor can tell, the claim is supported. **A
wrong fact early passes every later check.** No later prompt can fix it.
The fix is at the source: better research, and tools that find real
evidence.

---

## 3. The broken middle

In `travel_crew.py`, give the Writer a model that does not exist:

    llm=LLM(model="gpt-4o-mini-does-not-exist"),

Run the crew.

**What you will see:** the Researcher finishes, then the Writer fails —
CrewAI retries it a few times, then the whole crew stops with an error.

**Now try to save the research:** run `crewai log-tasks-outputs`. Only the
Researcher's task is listed. Try replaying from the Writer — it is not in
the list, so replay cannot start there.

**Why it matters:** the research you paid for is not lost from the log, but
the crew cannot continue from where it crashed. Running again means paying
for the research again. That is the argument for LangGraph's checkpoints
on Day 26.

Remember to change the model back afterwards.

---

## 4. Replay a finished run

1. Run the crew normally, to the end.
2. `crewai log-tasks-outputs` — copy the Writer task's ID (Task 2).
3. Change the Writer's backstory a little, for example: *"You write in a
   lively, excited style."*
4. `python experiments/replay_from_task.py <that ID>`

**What you will see:** the Researcher does **not** run. Only the Writer and
Editor do, using the saved research.

**Why it matters:** when you are improving one agent, you don't have to pay
for the whole crew every time.

---

## 5. Did the third agent earn its cost?

Run the same destination with this Day 24 crew and with your Day 23
two-agent crew. Compare the token counts and the two final articles.

Is the edited article genuinely better — or just shorter, for more money?
**"It did not help" is a perfectly good answer**, if you can show why.
