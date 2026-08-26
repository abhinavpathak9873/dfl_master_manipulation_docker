"""Local-alignment backend mapping."""

from __future__ import annotations

from dfl_toolbox._backends import BackendFactory

LOCAL_ALIGNERS: dict[str, BackendFactory] = {}


def create(*, backend: str, **options):
    """Construct a reusable local aligner by script-like backend name."""

    from dfl_toolbox.perception._facades import LocalAlignment

    return LocalAlignment(backend=backend, **options)


__all__ = ["LOCAL_ALIGNERS", "create"]
