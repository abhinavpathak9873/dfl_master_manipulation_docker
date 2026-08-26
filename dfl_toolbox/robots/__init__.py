"""Concrete robot adapters and their direct selection mapping.

Add imports and mapping entries here as real robot/mode adapters are built.
"""

from __future__ import annotations

from dfl_toolbox._backends import BackendFactory

ROBOTS: dict[tuple[str, str], BackendFactory] = {}

__all__ = ["ROBOTS"]
