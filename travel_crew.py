"""
Day 24 — A three-agent travel crew (CrewAI)
===========================================

Researcher → Writer → Editor.

New since Day 23:
  • an Editor, who checks the draft against the research (context=...)
  • a guardrail in CODE on the research: every fact needs a web link
  • an optional human review of the final article (ASK_A_HUMAN)

Run it:   python travel_crew.py
          python travel_crew.py Pokhara

Needs in .env:   OPENAI_API_KEY   and   TAVILY_API_KEY
"""

import os
import sys

import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

load_dotenv()

# Set this to True to read and approve the editor's article yourself,
# in the terminal, before the crew finishes.
ASK_A_HUMAN = False


# ---------------------------------------------------------------------------
# The Researcher's tool — the same search as Day 23.
# ---------------------------------------------------------------------------

@tool("search_web")
def search_web(query: str) -> str:
    """Search the web for current facts about a place in Nepal.
    Use it for every fact you report. It returns up to 5 results, each with a
    title, a link and a short summary. If nothing is found, it says so: then
    write "not found" rather than guessing."""
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return "No Tavily API key is configured, so the search could not run."
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={"Authorization": f"Bearer {key}"},
            json={"query": query, "max_results": 5},
            timeout=15,
        )
    except requests.RequestException as error:
        return f"Could not reach the search service: {error}"

    if response.status_code != 200:
        return f"The search failed (status {response.status_code})."
    results = response.json().get("results", [])
    if not results:
        return "No results were found for that search."

    lines = []
    for i, r in enumerate(results, start=1):
        summary = (r.get("content") or "")[:300]
        lines.append(f"{i}. {r.get('title')}\n   {r.get('url')}\n   {summary}")
    return "\n\n".join(lines)


# ---------------------------------------------------------------------------
# A guardrail in CODE on the research.
# A task guardrail checks a task's result before the crew moves on. If it
# fails, the agent is told why and tries again (up to guardrail_max_retries).
# A rule in code cannot be argued with — the Day 22 lesson.
# ---------------------------------------------------------------------------

def check_sources(result):
    """Every fact must have a web link, or say 'not found'."""
    facts = [line for line in result.raw.splitlines()
             if line.strip().startswith(("-", "*", "•"))]
    if not facts:
        return (False, "Give the facts as a bullet list, one fact per line.")

    missing = [f.strip() for f in facts
               if "http" not in f and "not found" not in f.lower()]
    if missing:
        return (False, "These facts have no source link: "
                       f"{missing[:2]}. Add the link, or write 'not found'.")
    return (True, result)


# ---------------------------------------------------------------------------
# The model and the three agents.
# Only the Researcher has a tool: least privilege. If a fact appears that
# was not researched, you know exactly which agent invented it.
# ---------------------------------------------------------------------------

llm = LLM(model="gpt-4o-mini", temperature=0.2)

researcher = Agent(
    role="Nepal Travel Researcher",
    goal="Find current facts about {destination}, each with a source",
    backstory=(
        "You never repeat a claim you cannot point to a source for. "
        "You say plainly when you could not find something."
    ),
    tools=[search_web],
    llm=llm,
    max_iter=5,
    allow_delegation=False,
    verbose=True,
)

writer = Agent(
    role="Travel Writer",
    goal="Write a short, warm travel piece about {destination}",
    backstory=(
        "You write short, clear sentences for first-time visitors. "
        "You use only the facts in the research notes, and give prices in NPR."
    ),
    llm=llm,
    max_iter=3,
    allow_delegation=False,
    verbose=True,
)

editor = Agent(
    role="Travel Editor",
    goal="Check the draft about {destination} against the research",
    backstory=(
        "You remove any claim that is not in the research notes. "
        "You never add new facts. You shorten rather than lengthen."
    ),
    llm=llm,
    max_iter=3,
    allow_delegation=False,
    verbose=True,
)


# ---------------------------------------------------------------------------
# The three tasks.
# ---------------------------------------------------------------------------

research_task = Task(
    description=(
        "Research {destination}. Find what it is known for, the best months "
        "to visit, and roughly what a traveller should budget per day in NPR."
    ),
    expected_output=(
        "A bullet list of 5 facts, one per line, each starting with '- '. "
        "Each fact must end with its source URL. "
        "If you cannot find something, write: not found."
    ),
    agent=researcher,
    guardrail=check_sources,
    guardrail_max_retries=2,
)

write_task = Task(
    description=(
        "Write a short travel piece about {destination} for a first-time "
        "visitor, using only the research notes."
    ),
    expected_output=(
        "Three short paragraphs, under 150 words in total. "
        "Do not add any fact that is not in the research notes."
    ),
    agent=writer,
)

# context=[...] decides what the Editor can see. Without it, the Editor would
# see only the draft — and have nothing to check it against.
edit_task = Task(
    description=(
        "Check the draft about {destination} against the research notes. "
        "Remove any claim the research does not support."
    ),
    expected_output=(
        "The corrected article. Then a line 'REMOVED:' listing anything you "
        "took out and why, or 'REMOVED: nothing'."
    ),
    agent=editor,
    context=[research_task, write_task],
    human_input=ASK_A_HUMAN,
)


crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential,
    verbose=True,
)


if __name__ == "__main__":
    destination = " ".join(sys.argv[1:]) or "Bandipur"
    result = crew.kickoff(inputs={"destination": destination})

    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)
    print(result.raw)
    print("\nTokens used:", result.token_usage.total_tokens)
