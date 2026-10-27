"""Make the ``deepmerge`` package importable in both layouts.

- Staging layout (this worker's directory): the source lives in the
  sibling ``deepmerge-src/`` directory.
- Upstream layout (when these files land in ``deepmerge/tests/`` of a
  checkout): the package lives at the repository root.

The first candidate that actually contains the package wins, so the
staging copy is never shadowed by an unrelated ``deepmerge`` directory.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

for _candidate in (
    os.path.join(_HERE, "..", "deepmerge-src"),
    os.path.join(_HERE, "..", ".."),
):
    _candidate = os.path.normpath(_candidate)
    if os.path.isfile(os.path.join(_candidate, "deepmerge", "__init__.py")):
        if _candidate not in sys.path:
            sys.path.insert(0, _candidate)
        break
