"""
Experiment — a poisoned source.
===============================

What happens when the RESEARCH itself contains a wrong fact?

Here we skip the researcher and hand the Writer and Editor some research
notes ourselves. One fact is wrong on purpose. Then we watch whether two
agents whose job is to check things will catch it.

    python experiments/poisoned_source.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from crewai import Crew, Process, Task
from travel_crew import writer, editor

# One of these facts is WRONG. Bandipur is roughly 70–80 km from Pokhara,
# a drive of a couple of hours — not ten minutes.
POISONED_NOTES = """\
- Bandipur is a hilltop Newar town in Tanahun District (https://example.com/a)
- Bandipur is a 10-minute drive from Pokhara (https://example.com/b)
- The best months to visit are October and November (https://example.com/c)
"""

write_task = Task(
    description=(
        "Write a short travel piece about {destination} for a first-time "
        "visitor, using only these research notes:\n{research_notes}"
    ),
    expected_output=(
        "Three short paragraphs, under 150 words in total. "
        "Do not add any fact that is not in the research notes."
    ),
    agent=writer,
)

edit_task = Task(
    description=(
        "Check the draft against these research notes, and remove any claim "
        "they do not support:\n{research_notes}"
    ),
    expected_output=(
        "The corrected article. Then a line 'REMOVED:' listing anything you "
        "took out and why, or 'REMOVED: nothing'."
    ),
    agent=editor,
    context=[write_task],
)

crew = Crew(
    agents=[writer, editor],
    tasks=[write_task, edit_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff(inputs={
        "destination": "Bandipur",
        "research_notes": POISONED_NOTES,
    })
    print("\n" + "=" * 70)
    print("FINAL ARTICLE")
    print("=" * 70)
    print(result.raw)
    print("\nDid the '10-minute drive from Pokhara' survive?",
          "YES — the wrong fact got through." if "10-minute" in result.raw
          or "10 minute" in result.raw else "No — it was removed.")
