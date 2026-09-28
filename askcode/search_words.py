"""Step 3: find the chunks that share the most useful words with the question.

YOUR CODE. Read HANDOUT.md, Step 3, first.
Check your work with:  pytest tests/test_search_words.py
"""

from __future__ import annotations

import math  # noqa: F401  (you will need it)
import re

from askcode.core import STOPWORDS, Chunk, words  # noqa: F401


def search_words(question: str, chunks: list[Chunk], k: int = 3) -> list[Chunk]:
   """Return up to k chunks that best match the question by shared words.

   Scoring. The tests check the exact order this produces.

   1. Question words: the set of words(question), minus STOPWORDS.
   2. Chunk words: for each chunk, the set of words(chunk.name + "\\n" + chunk.text).
   3. For each question word w, df(w) is the number of chunks whose word set
      contains w, and N is len(chunks). Ignore question words no chunk contains.
   4. weight(w) = math.log(N / df(w)). A rare word weighs a lot; a word found in
      every chunk weighs 0.
   5. score(chunk) = the sum of weight(w) over the question words the chunk contains,
      rounded with round(score, 6). Rounding makes chunks that match the same words
      tie exactly, whatever order your code adds the weights in.
   6. Return the chunks whose score is greater than 0, highest score first, at most k
      of them. When two chunks have the same score, the one that comes first in
      `chunks` comes first.

   If the question has no words left after step 1, or chunks is empty, return [].

   This is the core idea of BM25, the standard keyword search (slide 45). BM25 adds
   adjustments for how often a word repeats and for chunk length.
   """


   word_regex = r"[A-Za-z0-9]+"

   # Get unique words from question
   q_words = []
   for w in [w.lower().strip() for w in (re.findall(word_regex, question))]:
      if w not in q_words and w not in STOPWORDS:
         q_words.append(w)

   # Get weight of each word in the question
   weights = {}
   for w in q_words:
      df = 0
      for c in chunks:
         if w in [w_tmp.lower() for w_tmp in re.findall(word_regex, c.name + "\n" + c.text)]:
            df += 1
      if df == 0:
         continue
      weights[w] = math.log(len(chunks) / df)

   # Score each chuck
   scores = {} # Map chunk_id to Chunk + score + index combo
   for c in chunks:
      c_words = [w.lower() for w in re.findall(word_regex, c.name + "\n" + c.text)]
      score = 0
      for w in q_words:
         if w in c_words and w in weights:
            score += weights[w]
      chunk_id = c.file + "." + c.name
      if score != 0:
         i = len(scores)
         scores[chunk_id] = [c, score, i]

   # Sort scores from greatest to least; the second sort key is for tiebreakers and is negative because of the reverse
   sorted_scores = sorted(scores, key=lambda k: (scores[k][1], -1*scores[k][2])) # Sort by score
   sorted_scores.reverse()
   return [scores[key][0] for key in sorted_scores[:k]]
