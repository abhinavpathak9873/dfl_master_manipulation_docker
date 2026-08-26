"""Segmentation backend mapping."""

from __future__ import annotations

from dfl_toolbox._backends import BackendFactory

SEGMENTERS: dict[str, BackendFactory] = {}


def create(*, backend: str, **options):
    """Construct a reusable segmenter by script-like backend name."""

    from dfl_toolbox.perception._facades import Segmenter

    return Segmenter(backend=backend, **options)


__all__ = ["SEGMENTERS", "create"]
