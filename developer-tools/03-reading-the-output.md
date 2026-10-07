# 3. Reading the output

You will see the same boxes as Day 23 — `🤖 Agent Started`,
`🔧 Tool Execution`, `✅ Agent Final Answer` — now for three agents.
Three new things to look for:

## 1. The guardrail rejecting a result

If the research fails `check_sources`, the Researcher runs again, and is
given your message, such as:

    These facts have no source link: [...]. Add the link, or write 'not found'.

Count how many times the Researcher answers. One answer means it passed
first time. Two or three means the guardrail sent it back.

## 2. The human review prompt

With `ASK_A_HUMAN = True`, after the Editor's final answer the crew shows
the article and waits for you to type. Nothing more happens until you do.

## 3. Retries before a crash

If an agent's model fails, CrewAI retries it automatically before giving
up. In our test, a crashing Writer was tried **three times** before the
crew stopped with the error. Repeated identical error messages are those
retries — not three separate problems.

## The check that matters most

The Editor's answer ends with a `REMOVED:` line. Read it:

- `REMOVED: nothing` on a draft with an unsupported claim means the Editor
  missed it.
- A list of removed claims means it did its job — check that each removal
  was right.
