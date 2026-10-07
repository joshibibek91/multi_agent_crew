# 1. Setup guide

This project uses the same setup as Day 23.

- **Python 3.10, 3.11, 3.12 or 3.13.** CrewAI does not support 3.14 yet.
- An **OpenAI** key and a **Tavily** key, in `.env`.

    python -m venv .venv
    .venv\Scripts\activate            (Windows)
    pip install -r requirements.txt
    copy .env.example .env

If you already have the Day 23 environment, you can activate that one
instead, and copy your Day 23 `.env` into this folder.

Then:

    python travel_crew.py

To try the human review, open `travel_crew.py` and set:

    ASK_A_HUMAN = True

The crew will stop after the Editor, show you the article, and wait for
you to type feedback — or press Enter to approve.
