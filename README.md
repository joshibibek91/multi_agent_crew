# Day 24 — A Three-Agent Crew, and Where CrewAI Stops

**Researcher → Writer → Editor.** The Researcher finds facts with sources,
the Writer turns them into a short travel piece, and the Editor checks the
piece against the research and removes anything unsupported.

New since Day 23: an **Editor**, a **guardrail in code** on the research,
optional **human review**, and **replay**.

---

## What is in this folder

| File | What it is |
|---|---|
| `travel_crew.py` | **The whole crew**: tool, guardrail, three agents, three tasks |
| `experiments/poisoned_source.py` | Gives the Writer and Editor research with one wrong fact. Does it get caught? |
| `experiments/replay_from_task.py` | Re-runs a finished crew from the Writer, reusing the saved research |
| `requirements.txt` · `.env.example` · `.gitignore` | Setup, the same as Day 23 |
| `developer-tools/` | Seven guides: setup, reference, reading the output, experiments, troubleshooting, limits |

---

## Setup

Same as Day 23 — **Python 3.10 to 3.13** (not 3.14):

    python -m venv .venv
    .venv\Scripts\activate            (Windows)
    source .venv/bin/activate         (Mac or Linux)
    pip install -r requirements.txt
    copy .env.example .env            (then add your OpenAI and Tavily keys)

You can reuse your Day 23 virtual environment and `.env` if you like.

---

## Run it

    python travel_crew.py                    (Bandipur)
    python travel_crew.py Pokhara

    python experiments/poisoned_source.py

    crewai log-tasks-outputs                 (after a finished run: lists task IDs)
    python experiments/replay_from_task.py <Writer task ID>

To review the Editor's article yourself before the crew finishes, set
`ASK_A_HUMAN = True` at the top of `travel_crew.py`.

---

## The three ideas to take away

**1. By default, every task sees everything before it.** `context=[...]`
lets you choose — and narrow — what each task sees.

**2. A wrong fact early passes every later check**, because the later
agents check against the same wrong source. Fix it at the source.

**3. Know exactly what the framework can and can't do.** CrewAI can check
results in code, ask a person, and replay a finished run. It cannot resume
a run that crashed — that is tomorrow's framework.
