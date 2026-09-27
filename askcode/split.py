"""Step 2: split the codebase into chunks, one per function or method.

YOUR CODE. Read HANDOUT.md, Step 2, first.
Check your work with:  pytest tests/test_split.py
"""

from __future__ import annotations

import ast  # noqa: F401  (you will need it)
from pathlib import Path

from askcode import CORPUS_DIR
from askcode.core import Chunk


def split_file(path: Path, root: Path) -> list[Chunk]:
    """Return one Chunk for every function and method in the Python file at `path`.

    Rules. The tests check every one.

    1. Make a chunk for each `def` or `async def` that sits directly in the module,
       and for each `def` or `async def` that sits directly in a class that sits
       directly in the module. Nothing else becomes a chunk: not code outside
       functions, not a class with no methods, not a function nested inside another
       function, not a class nested inside a class, and not a function defined inside
       an `if`, `try`, `for`, `while` or `with` block at module level.
    2. name is the function name, or "ClassName.method_name" for a method.
    3. start_line is the line of the `def`, or the line of the first decorator if the
       function has decorators. end_line is the last line of the function.
       Both count from 1.
    4. text is exactly the source lines start_line to end_line, joined with "\\n".
       Split the file's text on "\\n" (not with str.splitlines) so your line numbers
       agree with the ones ast reports.
    5. file is the path of `path` relative to `root`, written with forward slashes,
       e.g. "sessions.py" or "sub/module.py".
    6. Return the chunks in the order they appear in the file.

    Hint: ast.parse(source) gives you a tree. tree.body lists the top-level
    statements. A function node has .name, .lineno, .end_lineno and .decorator_list,
    and each decorator node has its own .lineno. A class node has .name and .body.
    Read the file with encoding="utf-8".
    """

    out = []
    out_file = str(path).replace(str(root).strip("/") + "/", "").strip("/")
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    for a in tree.body:
      if isinstance(a, ast.FunctionDef):
         start = a.lineno - len(a.decorator_list)
         out.append(Chunk(
            name=a.name,
            start_line=start,
            end_line=a.end_lineno,
            text="\n".join(text.split("\n")[start - 1 : a.end_lineno]),
            file=out_file,
         ))
      elif isinstance(a, ast.ClassDef):
         for b in a.body:
            if isinstance(b, ast.FunctionDef):
               start = b.lineno - len(b.decorator_list)
               out.append(Chunk(
                  name=f"{a.name}.{b.name}",
                  start_line=start,
                  end_line=b.end_lineno,
                  text="\n".join(text.split("\n")[start - 1 : b.end_lineno]),
                  file=out_file,
               ))

    return out


def split_corpus(root: Path = CORPUS_DIR) -> list[Chunk]:
    """Return the chunks of every .py file under `root`, including subfolders.

    Process the files in order of their relative path, written with forward slashes
    and sorted as plain strings. Keep each file's chunks in file order.
    For the requests codebase this returns 230 chunks.
    """

    out = []
    files = sorted(list(Path(root).rglob("*")))
    for _file in files:
      out += split_file(_file, root)

    return out
