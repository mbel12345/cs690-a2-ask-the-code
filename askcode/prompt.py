"""Step 4, part A: the five-part prompt from the Week 3 slides.

YOUR CODE. Read HANDOUT.md, Step 4, first.
Check your work with:  pytest tests/test_prompt.py
"""

from __future__ import annotations

from askcode.core import NO_CODE, Chunk, Prompt, format_chunk  # noqa: F401


def build_prompt_five_part(question: str, chunks: list[Chunk]) -> Prompt:
   """Build the prompt your pipeline sends to the AI.

   Requirements. The tests check each one.

   1. prompt.system holds the five parts from slide 6. Each part starts on its own
      line with its label, in this order:
         Goal:
         Inputs and outputs:
         Rules:
         Example:
         Reply format:
   2. Rules tell the model to answer only from the code shown, and, when that code
      does not answer the question, to reply with the answer
      "not found in the code shown" and null for both file and line.
   3. Example holds one sample question and its correct reply written as a JSON
      object with the keys "answer", "file" and "line". Do not use one of your own
      ten questions.
   4. Reply format asks for exactly one JSON object with the keys "answer" (a string),
      "file" (a string or null) and "line" (an integer or null), with nothing before
      or after it.
   5. prompt.system is the same text for every question and every set of chunks.
      It is the stable part of the prompt, so it goes first (slide 26).
   6. prompt.user is a line "Code:", then every chunk shown with format_chunk(chunk)
      in the order given, separated by blank lines, then a line "Question:", then
      the question. The question comes last. If chunks is empty, put NO_CODE under
      "Code:" instead.
   """

   user = "Code:" + ("\n".join([format_chunk(c) for c in chunks]) if len(chunks) > 0 else NO_CODE)
   user += f"Question: {question}"
   return Prompt(
      system="""
Goal: Answer the user's requestion about the requests codebase. Return the file and method that answers the question. Return "not found in the code shown" if the method cannot be round. It should return "null" for the file and function in this case.
Inputs and outputs: Inputs - A question (str) that asks about the requests library. Outputs - json object that contains "answer", "file", and "line".
Rules: Only use the code shown in the "Code:" section. Do not look on the internet or any other source.
Example: {"answer": "You access the text attribute of the response", "file": "models.py", "line": 909}
Reply format: json object that contains "answer", "file", and "line".
      """,
      user=user
   )
