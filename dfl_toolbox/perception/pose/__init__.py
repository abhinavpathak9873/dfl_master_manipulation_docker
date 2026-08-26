"""Pose-estimation backend mapping."""

from __future__ import annotations

from dfl_toolbox._backends import BackendFactory

POSE_ESTIMATORS: dict[str, BackendFactory] = {}


def create(*, backend: str, **options):
    """Construct a reusable pose estimator by script-like backend name."""

    from dfl_toolbox.perception._facades import PoseEstimator

    return PoseEstimator(backend=backend, **options)


__all__ = ["POSE_ESTIMATORS", "create"]
