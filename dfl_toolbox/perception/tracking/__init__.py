"""Tracking backend mapping."""

from __future__ import annotations

from dfl_toolbox._backends import BackendFactory

TRACKERS: dict[str, BackendFactory] = {}


def create(*, backend: str, **options):
    """Construct a reusable tracker by script-like backend name."""

    from dfl_toolbox.perception._facades import Tracker

    return Tracker(backend=backend, **options)


__all__ = ["TRACKERS", "create"]
