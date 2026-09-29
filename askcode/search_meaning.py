"""Step 7: find chunks by meaning instead of by shared words.

YOUR CODE. Read HANDOUT.md, Step 7, first.
Check your work with:  pytest tests/test_search_meaning.py

The embedding model runs on your own laptop (askcode/embed.py). It is free and needs
no key; the first run downloads it once, about 67 MB, into the .models folder.
"""

from __future__ import annotations

import math  # noqa: F401  (you will need it)
from collections.abc import Callable

from askcode import embed
from askcode.core import Chunk

def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two vectors: dot(a, b) / (length(a) * length(b)).

    Return 0.0 if either vector has length 0 (all zeros).
    Raise ValueError if the two vectors do not have the same number of numbers.
    """

    if len(a) != len(b):
        raise ValueError("a and b must have the same length")

    len_a = (sum([i**2 for i in a]))**(1/len(a))
    len_b = (sum([i**2 for i in b]))**(1/len(b))

    if len_a == 0 or len_b == 0:
        return 0

    dot = 0
    for i in range(len(a)):
        dot += a[i]*b[i]

    return dot / (len_a * len_b)


class MeaningIndex:
    """Embed every chunk once, then answer many questions quickly (slides 43 to 46)."""

    def __init__(
        self,
        chunks: list[Chunk],
        embed_passages: Callable[[list[str]], list[list[float]]] | None = None,
        embed_query: Callable[[str], list[float]] | None = None,
    ) -> None:
        """Store the chunks and embed all of them, here, once.

        1. If embed_passages or embed_query is None, use embed.embed_passages or
           embed.embed_query. (The tests pass in small fake versions instead.)
        2. The text embedded for a chunk is chunk.name + "\\n" + chunk.text.
        3. Call embed_passages exactly once, with the list of all those texts in the
           order of `chunks`. One call is far faster than one call per chunk.
        4. Keep what you need for search: the chunks, their vectors, and embed_query.
        """

        if embed_passages is None:
            embed_passages = embed.embed_passages

        if embed_query is None:
            embed_query = embed.embed_query

        out = []
        for c in chunks:
            out.append(c.name + "\n" + c.text)

        self.chunks = chunks
        self.vectors = embed_passages(out)
        self.embed_query = embed_query

    def search(self, question: str, k: int = 3) -> list[Chunk]:
        """Return the k chunks whose vectors are closest in meaning to the question.

        1. Embed the question with embed_query, once. Do not embed any chunk here.
        2. Score every chunk with cosine(question vector, chunk vector).
        3. Return the k highest-scoring chunks, highest first. When two chunks have
           the same score, the one that comes first in the chunks list comes first.

        Unlike word search, this always returns k chunks (or every chunk, if there
        are fewer than k), even when none of them is relevant (slide 56).
        """

        question_vector = self.embed_query(question)

        scores = []
        for i, chunk_vector in enumerate(self.vectors):
            scores.append((i, cosine(question_vector, chunk_vector)))

        scores = sorted(scores, key=lambda x: (x[1], -1*x[0])) # the second sort key is for tiebreakers and is negative because of the reverse
        scores.reverse()

        results = []
        for i in range(k):
            results.append(self.chunks[scores[i][0]])

        return results
