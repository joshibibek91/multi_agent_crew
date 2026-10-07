"""
Experiment — replay a finished run from one task.
=================================================

CrewAI saves each task's result after a run. Replay re-runs the crew from
a task you choose, and REUSES the saved results of every task before it.

    Step 1:  python travel_crew.py                   (a full, finished run)
    Step 2:  crewai log-tasks-outputs                (lists the saved tasks and their IDs)
    Step 3:  python experiments/replay_from_task.py <the Writer task's ID>

Watch the boxes: the Researcher does not run again. Only the Writer and the
Editor do — so you don't pay for the research twice.

Important: replay only works from a task that FINISHED. If a run crashes
in the middle, the crashed task was never saved, so you cannot replay from
it. Replay is for REDOING a finished run, not for recovering from a crash.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from travel_crew import crew

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    task_id = sys.argv[1]
    try:
        result = crew.replay(task_id=task_id)
    except ValueError as error:
        print(f"\nReplay failed: {error}")
        print("Run 'crewai log-tasks-outputs' to see the IDs you can use.")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("REPLAYED RESULT")
    print("=" * 70)
    print(result.raw)
